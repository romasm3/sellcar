from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .constants import can_create_listing, can_create_free_listing, FREE_LISTING_DAYS
from .image_validation import split_valid_images
from .models import (
    Listing,
    ListingImage,
    VehicleType,
    SubCategory,
    FuelType,
)
from .views import (
    _int_or_none,
    _float_or_none,
    get_coordinates_for_location,
    _send_listing_published_email,
    _send_saved_listing_updated_emails,
    _send_saved_listing_price_drop_emails,
    COUNTRY_FLAGS,
)


# ═══════════════════════════════════════════════════════════
# BOATS — Boats & Water Transport (vehicle_type slug='boats')
# Atskira forma, free-text Make/Model, boat-specific laukai.
# NEnaudoja cars draft session — paprastas create+edit per vieną POST.
# ═══════════════════════════════════════════════════════════

BOATS_SUBCATEGORY_SLUGS = {
    'boats', 'yachts', 'motorboats', 'sailboats',
    'jet-skis', 'inflatable-boats', 'fishing-boats', 'other-watercraft',
}

# Medžiaga (boat_material) — 'Other' pirmas
BOAT_MATERIAL_CHOICES = [
    ('', '---------'),
    ('aluminium', _('Aluminium')),
    ('steel', _('Steel')),
    ('fiberglass', _('Fiberglass / Plastic')),
    ('wood', _('Wood')),
    ('pvc', _('PVC / Rubber')),
    ('other', _('Other')),
]


def _resolve_boats_subcategory(slug):
    """Pagal slug grąžina boats SubCategory (vehicle_type=boats)."""
    if not slug:
        return None
    return SubCategory.objects.filter(
        vehicle_type__slug='boats', slug=slug
    ).first()


def _boats_country_choices():
    _all = list(Listing.COUNTRY_CHOICES)
    _us = [c for c in _all if c[0] == 'US']
    _rest = sorted([c for c in _all if c[0] != 'US'], key=lambda x: x[1])
    return [
        (code, f"{COUNTRY_FLAGS.get(code, '🌍')} {name}")
        for code, name in (_us + _rest)
    ]


@login_required
def boats_listing_create(request):
    """Create + Edit boats listing (single page, one POST).

    URL:       /create/boats/?new=1&subcategory=<slug>
    URL EDIT:  /create/boats/?edit=<pk>
    """
    boats_vt = VehicleType.objects.filter(slug='boats').first()
    if not boats_vt:
        messages.error(request, 'Boats category not configured.')
        return redirect('listing_list')

    # ═══ EDIT MODE ═══
    edit_pk = _int_or_none(request.GET.get('edit')) or _int_or_none(request.POST.get('edit'))
    is_edit_mode = bool(edit_pk)
    listing = None

    if is_edit_mode:
        listing = get_object_or_404(Listing, pk=edit_pk, seller=request.user)
        if not listing.vehicle_type or listing.vehicle_type.slug != 'boats':
            messages.error(request, 'Boats edit is only available for boats listings.')
            return redirect('listing_edit_hub', pk=edit_pk)

    # ═══ LIMIT GUARD (CREATE only) ═══
    if not is_edit_mode:
        can_create, active_count, limit = can_create_listing(request.user)
        if not can_create:
            messages.error(
                request,
                f'You have reached your active listings limit ({active_count}/{limit}). '
                f'Upgrade your account to create more listings.',
            )
            return redirect('listing_upgrade')

    # ═══ Subcategory: iš ?subcategory (create) arba esamo listing (edit) ═══
    if is_edit_mode:
        selected_sub = listing.subcategory
    else:
        selected_sub = _resolve_boats_subcategory(request.GET.get('subcategory'))

    # ═══════════════════════════════════════════════════════════
    # POST
    # ═══════════════════════════════════════════════════════════
    if request.method == 'POST':
        target = listing if is_edit_mode else None
        old_price = float(target.price) if (is_edit_mode and target.price) else 0

        # CREATE — naują listing kuriam tik POST metu (ne draft)
        if not is_edit_mode:
            target = Listing(
                seller=request.user,
                vehicle_type=boats_vt,
                status='draft',
            )
            # subcategory iš POST hidden
            sub = _resolve_boats_subcategory(request.POST.get('subcategory'))
            target.subcategory = sub
            selected_sub = sub

        errors = []

        # ─── Make / Model (free text) ───
        target.boat_make_text = (request.POST.get('boat_make_text', '') or '').strip()
        target.boat_model_text = (request.POST.get('boat_model_text', '') or '').strip()

        # ─── Condition (required) ───
        condition = request.POST.get('condition', '')
        if not condition:
            errors.append(_('Būklė yra privaloma'))
        target.condition = condition

        # ─── Type (required) ───
        boat_type = request.POST.get('boat_type', '')
        if not boat_type:
            errors.append(_('Tipas yra privalomas'))
        target.boat_type = boat_type

        # ─── Year (required) ───
        year = _int_or_none(request.POST.get('year'))
        if not year:
            errors.append(_('Metai yra privalomi'))
        else:
            target.year = year

        # ─── Boat-specific ───
        target.boat_material = request.POST.get('boat_material', '') or ''
        target.boat_length_m = _float_or_none(request.POST.get('boat_length_m'))
        target.boat_width_m = _float_or_none(request.POST.get('boat_width_m'))
        target.boat_engine_count = _int_or_none(request.POST.get('boat_engine_count'))
        target.sdk_number = (request.POST.get('sdk_number', '') or '').strip()

        # ─── Reused fields ───
        target.seats = request.POST.get('seats', '') or ''
        target.color = request.POST.get('color', '') or ''
        target.power = _int_or_none(request.POST.get('power'))

        # ─── Boat engine + fuel tank + feature checkboxes ───
        target.boat_engine_type = request.POST.get('boat_engine_type', '') or ''
        target.boat_fuel_tank_l = _float_or_none(request.POST.get('boat_fuel_tank_l'))
        target.boat_liftable_engine = request.POST.get('boat_liftable_engine') == 'on'
        target.boat_propeller = request.POST.get('boat_propeller') == 'on'
        target.boat_water_turbine = request.POST.get('boat_water_turbine') == 'on'

        ft_id = _int_or_none(request.POST.get('fuel_type'))
        if ft_id:
            try:
                target.fuel_type = FuelType.objects.get(pk=ft_id)
            except FuelType.DoesNotExist:
                target.fuel_type = None
        else:
            target.fuel_type = None

        # Listing modelis turi mileage NOT NULL (validator min 0) — boats nenaudoja
        if target.mileage is None:
            target.mileage = 0

        # ─── Price ───
        price = _float_or_none(request.POST.get('price'))
        if price is None or price <= 0:
            errors.append(_('Kaina yra privaloma'))
        else:
            target.price = price
        target.negotiable = request.POST.get('negotiable') == 'on'
        target.export_price = _float_or_none(request.POST.get('export_price'))
        target.taxes_extra = request.POST.get('taxes_extra') == 'on'
        target.open_to_trade = request.POST.get('open_to_trade') == 'on'

        # ─── Special features (reuse boolean fields) ───
        target.has_warranty = request.POST.get('has_warranty') == 'on'
        target.available_on_lease = request.POST.get('available_on_lease') == 'on'

        # ─── Description + Video ───
        target.description = request.POST.get('description', '') or ''
        target.video_url = request.POST.get('video_url', '') or ''

        # ─── Location + Contact ───
        country = request.POST.get('country', 'US')
        target.country = country
        if country == 'US':
            state = request.POST.get('state', '')
            if not state:
                errors.append(_('Valstija yra privaloma'))
            if hasattr(target, 'state'):
                target.state = state
            target.city = request.POST.get('city', '') or '—'
        else:
            city = request.POST.get('city', '')
            if not city:
                errors.append(_('Miestas yra privalomas'))
            target.city = city
            if hasattr(target, 'state'):
                target.state = ''

        target.postal_code = request.POST.get('postal_code', '') or ''
        target.address = request.POST.get('address', '') or ''
        target.hide_exact_address = request.POST.get('hide_exact_address') == 'on'

        # Phone → profile
        phone_val = (request.POST.get('phone', '') or '').strip()
        if not phone_val:
            errors.append(_('Telefonas yra privalomas'))
        elif hasattr(request.user, 'profile'):
            request.user.profile.phone_number = phone_val
            request.user.profile.save(update_fields=['phone_number'])

        # Terms (CREATE only)
        if not is_edit_mode and not request.POST.get('agree_terms'):
            errors.append(_('Turite sutikti su taisyklėmis'))

        # ─── Title ───
        title_parts = []
        if target.boat_make_text:
            title_parts.append(target.boat_make_text)
        if target.boat_model_text:
            title_parts.append(target.boat_model_text)
        if target.year:
            title_parts.append(str(target.year))
        if not title_parts:
            type_label = dict(Listing.BOAT_TYPE_CHOICES).get(boat_type, '')
            if type_label:
                title_parts.append(type_label)
            elif selected_sub:
                title_parts.append(selected_sub.name)
        target.title = ' '.join(title_parts) or 'Boat listing'

        new_images, _image_errors = split_valid_images(
            request.FILES.getlist('images')
        )
        errors.extend(_image_errors)

        if errors:
            for e in errors:
                messages.error(request, e)
            return _render_boats_form(
                request, listing=target,
                selected_sub=selected_sub,
                is_edit_mode=is_edit_mode,
                posted=request.POST,
            )

        # ─── Coordinates ───
        lat, lng = get_coordinates_for_location(target.city, target.country, request.POST)
        target.latitude = lat
        target.longitude = lng

        try:
            target.save()
        except Exception as e:
            messages.error(request, f'Save failed: {e}')
            return _render_boats_form(
                request, listing=target,
                selected_sub=selected_sub,
                is_edit_mode=is_edit_mode,
                posted=request.POST,
            )

        # ─── Photos ───
        existing_count = target.images.count()
        for i, image in enumerate(new_images[:40]):
            try:
                ListingImage.objects.create(
                    listing=target,
                    image=image,
                    is_main=(existing_count == 0 and i == 0),
                    order=existing_count + i,
                )
            except Exception as e:
                print(f"[boats] image upload failed: {e}")

        # ═══ EDIT: notify + redirect ═══
        if is_edit_mode:
            try:
                new_price = float(target.price)
                if new_price != old_price and old_price > 0:
                    if new_price < old_price:
                        _send_saved_listing_price_drop_emails(target, old_price, new_price)
                    else:
                        _send_saved_listing_updated_emails(target, 'Listing updated')
                else:
                    _send_saved_listing_updated_emails(target, 'Listing updated')
            except (ValueError, TypeError):
                pass
            messages.success(request, 'Listing updated successfully.')
            return redirect('listing_edit_hub', pk=target.pk)

        # ═══ CREATE: free tier vs paid plan ═══
        is_free, active_count, free_limit = can_create_free_listing(request.user)
        if is_free:
            target.activate(days=FREE_LISTING_DAYS)
            _send_listing_published_email(target, request.user)
            return redirect(
                reverse('listing_success', kwargs={'pk': target.pk}) + '?action=published'
            )
        return redirect('listing_select_plan', pk=target.pk)

    # ═══ GET ═══
    return _render_boats_form(
        request, listing=listing,
        selected_sub=selected_sub,
        is_edit_mode=is_edit_mode,
        posted=None,
    )


def _render_boats_form(request, listing=None, selected_sub=None, is_edit_mode=False, posted=None):
    """Render boats form. `listing` may be unsaved (POST error) or saved (edit)."""

    user_phone = ''
    if hasattr(request.user, 'profile') and request.user.profile.phone_number:
        user_phone = request.user.profile.phone_number

    context = {
        'is_edit_mode': is_edit_mode,
        'listing': listing,
        'edit_listing_id': listing.pk if (listing and listing.pk) else None,
        'selected_sub': selected_sub,
        'subcategory_slug': selected_sub.slug if selected_sub else '',
        'subcategory_name': selected_sub.name if selected_sub else '',
        'fuel_types': FuelType.objects.all().order_by('name'),
        'material_choices': BOAT_MATERIAL_CHOICES,
        'boat_type_choices': Listing.BOAT_TYPE_CHOICES,
        'engine_type_choices': Listing.BOAT_ENGINE_TYPE_CHOICES,
        'condition_choices': Listing.CONDITION_CHOICES,
        'seats_choices': Listing.SEATS_CHOICES,
        'color_choices': Listing.COLOR_CHOICES,
        'country_choices': _boats_country_choices(),
        'us_states': Listing.US_STATE_CHOICES,
        'years': list(range(timezone.now().year + 1, 1949, -1)),
        'user_phone': user_phone,
        'posted': posted,
    }
    return render(request, 'listings/boats_listing_create.html', context)