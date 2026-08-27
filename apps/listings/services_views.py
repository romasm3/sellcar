from datetime import date

from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext as _
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .constants import can_create_listing, can_create_free_listing, FREE_LISTING_DAYS
from .equipment_registry import SVC_EQUIPMENT_DEFINITION
from .image_validation import split_valid_images
from .models import (
    Listing, ListingImage, VehicleType, Equipment, ListingEquipment,
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
# PASLAUGOS (vehicle_type slug='services')
#
# Plokščia kategorija (loading-equipment / forestry patternas): etalone
# subkategorijų nėra, todėl subcategory lieka NULL, o pikeris veda tiesiai
# į šią formą per CREATE_URL_BY_VEHICLE_TYPE.
#
# Du skirtumai nuo visų kitų kategorijų:
#   1. Pavadinimą rašo pats vartotojas (niekur negeneruojam iš markės).
#   2. Kaina NEPRIVALOMA — tuščia virsta 0 ir rodoma „Sutartinė kaina".
#
# Listing.year / mileage yra NOT NULL be default, o paslaugose jų nėra,
# todėl užpildom techniškai (einamieji metai / 0) ir niekur nerodom.
# ═══════════════════════════════════════════════════════════

SVC_VT_SLUG = 'services'

TITLE_MAX = 50          # etalone f_99 maxlength=50


def get_svc_equipment():
    """18 paslaugų varnelių, sugrupuotų šablonui (idempotentiškai kuriamos)."""
    grouped = []
    for cat_key, cat_label, names in SVC_EQUIPMENT_DEFINITION:
        items = [Equipment.objects.get_or_create(category=cat_key, name=n)[0]
                 for n in names]
        grouped.append({'key': cat_key, 'label': cat_label, 'items': items})
    return grouped


def _country_choices():
    # Šalys — vienas sąrašas visai svetainei (apps/listings/salys.py)
    from apps.listings import salys
    return salys.plokscias()


@login_required
def services_listing_create(request):
    """URL: /create/services/?new=1  |  ?edit=<pk>"""
    vt = VehicleType.objects.filter(slug=SVC_VT_SLUG).first()
    if not vt:
        messages.error(request, _('Paslaugų kategorija nesukonfigūruota.'))
        return redirect('listing_list')

    edit_pk = _int_or_none(request.GET.get('edit')) or _int_or_none(request.POST.get('edit'))
    is_edit_mode = bool(edit_pk)
    listing = None

    if is_edit_mode:
        listing = get_object_or_404(Listing, pk=edit_pk, seller=request.user)
        if not listing.vehicle_type or listing.vehicle_type.slug != SVC_VT_SLUG:
            messages.error(request, _('Ši forma skirta tik paslaugų skelbimams.'))
            return redirect('listing_edit_hub', pk=edit_pk)
    else:
        can_create, active_count, limit = can_create_listing(request.user)
        if not can_create:
            messages.error(
                request,
                f'You have reached your active listings limit ({active_count}/{limit}). '
                f'Upgrade your account to create more listings.',
            )
            return redirect('listing_upgrade')

    if request.method == 'POST':
        target = listing if is_edit_mode else Listing(
            seller=request.user, vehicle_type=vt, status='draft')
        old_price = float(target.price) if (is_edit_mode and target.price) else 0
        errors = []

        title = (request.POST.get('title', '') or '').strip()
        if not title:
            errors.append(_('Pavadinimas yra privalomas'))
        target.title = title[:TITLE_MAX]

        service_type = request.POST.get('service_type', '')
        if not service_type:
            errors.append(_('Paslaugos tipas yra privalomas'))
        target.service_type = service_type

        # Kaina neprivaloma: tuščia = 0 → šablonuose „Sutartinė kaina"
        price = _float_or_none(request.POST.get('price'))
        target.price = price if (price and price > 0) else 0
        target.negotiable = request.POST.get('negotiable') == 'on'

        target.description = request.POST.get('description', '') or ''
        target.video_url = request.POST.get('video_url', '') or ''

        # Techniniai NOT NULL laukai — paslaugose neturi prasmės, nerodomi
        if not target.year:
            target.year = timezone.now().year
        target.mileage = 0

        country = request.POST.get('country', 'US')
        target.country = country
        if country == 'US':
            state = request.POST.get('state', '')
            if not state:
                errors.append(_('Valstija yra privaloma'))
            target.state = state
            target.city = request.POST.get('city', '') or '—'
        else:
            city = request.POST.get('city', '')
            if not city:
                errors.append(_('Miestas yra privalomas'))
            target.city = city
            target.state = ''
        target.address = request.POST.get('address', '') or ''

        phone_val = (request.POST.get('phone', '') or '').strip()
        if not phone_val:
            errors.append(_('Telefonas yra privalomas'))
        elif hasattr(request.user, 'profile'):
            request.user.profile.phone_number = phone_val
            request.user.profile.save(update_fields=['phone_number'])

        if not is_edit_mode and not request.POST.get('agree_terms'):
            errors.append(_('Turite sutikti su taisyklėmis'))

        new_images, img_errors = split_valid_images(request.FILES.getlist('images'))
        errors.extend(img_errors)

        if errors:
            for e in errors:
                messages.error(request, e)
            return _render_form(request, target, is_edit_mode, request.POST)

        target.latitude, target.longitude = get_coordinates_for_location(target.city, target.country, request.POST)

        try:
            target.save()
        except Exception as e:
            messages.error(request, f'Save failed: {e}')
            return _render_form(request, target, is_edit_mode, request.POST)

        ListingEquipment.objects.filter(listing=target).delete()
        for eid in request.POST.getlist('equipment'):
            try:
                ListingEquipment.objects.create(listing=target, equipment_id=int(eid))
            except (ValueError, TypeError):
                continue

        existing = target.images.count()
        for i, image in enumerate(new_images[:36]):
            try:
                ListingImage.objects.create(
                    listing=target, image=image,
                    is_main=(existing == 0 and i == 0), order=existing + i,
                )
            except Exception as e:
                print(f"[services] image upload failed: {e}")

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
            messages.success(request, _('Skelbimas atnaujintas.'))
            return redirect('listing_edit_hub', pk=target.pk)

        is_free, _c, _l = can_create_free_listing(request.user)
        if is_free:
            target.activate(days=FREE_LISTING_DAYS)
            _send_listing_published_email(target, request.user)
            return redirect(
                reverse('listing_success', kwargs={'pk': target.pk}) + '?action=published')
        return redirect('listing_select_plan', pk=target.pk)

    return _render_form(request, listing, is_edit_mode, None)


def _render_form(request, listing, is_edit_mode, posted):
    user_phone = ''
    if hasattr(request.user, 'profile') and request.user.profile.phone_number:
        user_phone = request.user.profile.phone_number

    selected_equipment = []
    if listing and listing.pk:
        selected_equipment = [
            str(i) for i in listing.equipment_items.values_list('equipment_id', flat=True)]
    elif posted:
        selected_equipment = posted.getlist('equipment')

    # ?type= — preselekcija iš pikerio („Automobilių supirkimas" veda čia
    # su type=car_buying, nes etalone tai paslaugos tipas, ne kategorija)
    current_type = ''
    if posted:
        current_type = posted.get('service_type', '')
    elif listing:
        current_type = listing.service_type or ''
    if not current_type:
        _url_type = request.GET.get('type', '')
        if _url_type in dict(Listing.SERVICE_TYPE_CHOICES):
            current_type = _url_type

    return render(request, 'listings/services_listing_create.html', {
        'is_edit_mode': is_edit_mode,
        'listing': listing,
        'current_type': current_type,
        'edit_listing_id': listing.pk if (listing and listing.pk) else None,
        'type_choices': Listing.SERVICE_TYPE_CHOICES,
        'title_max': TITLE_MAX,
        'equipment_by_category': get_svc_equipment(),
        'selected_equipment': selected_equipment,
        'country_choices': _country_choices(),
        'us_states': Listing.US_STATE_CHOICES,
        'user_phone': user_phone,
        'posted': posted,
    })
