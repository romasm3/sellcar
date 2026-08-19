import os
import unicodedata

from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext as _
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .constants import can_create_listing, can_create_free_listing, FREE_LISTING_DAYS
from .equipment_registry import BIKE_EQUIPMENT_DEFINITION
from .image_validation import split_valid_images
from .models import (
    Listing, ListingImage, VehicleType, SubCategory, Equipment, ListingEquipment,
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
# EL. PASPIRTUKAI, RIEDŽIAI, DVIRAČIAI (vehicle_type slug='bicycles')
#
# Pikeryje subkategorijų žingsnio NĖRA (kaip etalone) — einam tiesiai į
# formą per CREATE_URL_BY_VEHICLE_TYPE. Bet subkategorija vis tiek
# užpildoma: ji IŠVEDAMA IŠ FORMOS lauko `bike_type` ir persiskaičiuoja
# kas išsaugojimą (žr. SKILL.md — subkategorija iš formos, ne iš URL).
#
# „Elektrinis riedis" DB atitikmens neturi (`bicycles` yra paprasti
# dviračiai), todėl jam subcategory lieka NULL.
# ═══════════════════════════════════════════════════════════

BIKE_VT_SLUG = 'bicycles'

BRANDS_PATH = os.path.join(
    os.path.dirname(__file__), 'management', 'commands', 'paspirtuku-markes.txt')

# bike_type → subkategorijos slug'as (None = paliekam NULL)
BIKE_TYPE_TO_SUBCATEGORY = {
    'e_scooter': 'electric-scooters',
    'e_bike': 'electric-bikes',
    'e_board': None,
}


def _norm(value):
    value = unicodedata.normalize('NFKD', value.casefold())
    return ''.join(c for c in value if not unicodedata.combining(c))


def _load_brands():
    seen, out = set(), []
    try:
        with open(BRANDS_PATH, encoding='utf-8') as fh:
            for line in fh:
                name = line.strip()
                if not name or _norm(name) in seen:
                    continue
                seen.add(_norm(name))
                out.append(name)
    except OSError:
        return []
    rest = [n for n in out if _norm(n) not in ('kita', 'kitas')]
    other = [n for n in out if _norm(n) in ('kita', 'kitas')]
    return rest + other


BIKE_BRANDS = _load_brands()


def _subcategory_for(bike_type):
    """Tipas → subkategorija. Persiskaičiuoja KAS IŠSAUGOJIMĄ."""
    slug = BIKE_TYPE_TO_SUBCATEGORY.get(bike_type)
    if not slug:
        return None
    return SubCategory.objects.filter(
        vehicle_type__slug=BIKE_VT_SLUG, slug=slug).first()


def get_bike_equipment():
    """12 ypatumų, sugrupuotų šablonui (idempotentiškai kuriamos)."""
    grouped = []
    for cat_key, cat_label, names in BIKE_EQUIPMENT_DEFINITION:
        items = [Equipment.objects.get_or_create(category=cat_key, name=n)[0]
                 for n in names]
        grouped.append({'key': cat_key, 'label': cat_label, 'items': items})
    return grouped


def _country_choices():
    _all = list(Listing.COUNTRY_CHOICES)
    _us = [c for c in _all if c[0] == 'US']
    _rest = sorted([c for c in _all if c[0] != 'US'], key=lambda x: x[1])
    return [(code, f"{COUNTRY_FLAGS.get(code, '🌍')} {name}")
            for code, name in (_us + _rest)]


@login_required
def bicycles_listing_create(request):
    """URL: /create/bicycles/?new=1  |  ?edit=<pk>"""
    vt = VehicleType.objects.filter(slug=BIKE_VT_SLUG).first()
    if not vt:
        messages.error(request, _('Paspirtukų kategorija nesukonfigūruota.'))
        return redirect('listing_list')

    edit_pk = _int_or_none(request.GET.get('edit')) or _int_or_none(request.POST.get('edit'))
    is_edit_mode = bool(edit_pk)
    listing = None

    if is_edit_mode:
        listing = get_object_or_404(Listing, pk=edit_pk, seller=request.user)
        if not listing.vehicle_type or listing.vehicle_type.slug != BIKE_VT_SLUG:
            messages.error(request, _('Ši forma skirta tik paspirtukų, riedžių ir dviračių skelbimams.'))
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

        condition = request.POST.get('condition', '')
        if not condition:
            errors.append(_('Būklė yra privaloma'))
        else:
            target.condition = condition

        bike_type = request.POST.get('bike_type', '')
        if not bike_type:
            errors.append(_('Tipas yra privalomas'))
        target.bike_type = bike_type
        # Subkategorija — iš formos, kas išsaugojimą
        target.subcategory = _subcategory_for(bike_type)

        brand = (request.POST.get('bike_brand_text', '') or '').strip()
        if not brand:
            errors.append(_('Gamintojas yra privalomas'))
        target.bike_brand_text = brand[:80]

        target.constr_model_text = (request.POST.get('constr_model_text', '') or '').strip()[:32]

        price = _float_or_none(request.POST.get('price'))
        if price is None or price <= 0:
            errors.append(_('Kaina yra privaloma'))
        else:
            target.price = price
        target.negotiable = request.POST.get('negotiable') == 'on'

        # ─── techniniai (vienetai sutampa su esamais stulpeliais) ───
        target.power_w = _int_or_none(request.POST.get('power_w'))
        target.max_speed_kmh = _int_or_none(request.POST.get('max_speed_kmh'))
        target.curb_weight = _int_or_none(request.POST.get('curb_weight'))
        target.payload_kg = _int_or_none(request.POST.get('payload_kg'))
        target.range_km = _int_or_none(request.POST.get('range_km'))
        target.color = request.POST.get('color', '') or ''

        target.battery_ah = _float_or_none(request.POST.get('battery_ah'))
        target.battery_pct = _int_or_none(request.POST.get('battery_pct'))
        target.charge_time_h = _float_or_none(request.POST.get('charge_time_h'))
        target.tyre_kind = request.POST.get('tyre_kind', '') or ''
        target.wheel_diameter_in = _float_or_none(request.POST.get('wheel_diameter_in'))
        target.max_incline_deg = _int_or_none(request.POST.get('max_incline_deg'))

        target.description = request.POST.get('description', '') or ''
        target.video_url = request.POST.get('video_url', '') or ''

        # Metai neprivalomi; `year` yra NOT NULL — tuščius keičiam einamaisiais
        year = _int_or_none(request.POST.get('year'))
        target.year = year or timezone.now().year
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

        # Pavadinimo lauko etalone nėra — generuojam
        parts = [p for p in (target.bike_brand_text, target.constr_model_text) if p]
        type_label = dict(Listing.BIKE_TYPE_CHOICES).get(bike_type, '')
        if not parts and type_label:
            parts.append(str(type_label))
        elif type_label:
            parts.append(str(type_label))
        target.title = ' '.join(str(p) for p in parts)[:200] or 'Paspirtukas'

        new_images, img_errors = split_valid_images(request.FILES.getlist('images'))
        errors.extend(img_errors)

        if errors:
            for e in errors:
                messages.error(request, e)
            return _render_form(request, target, is_edit_mode, request.POST)

        target.latitude, target.longitude = get_coordinates_for_location(
            target.city, target.country)

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
                print(f"[bicycles] image upload failed: {e}")

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

    return render(request, 'listings/bicycles_listing_create.html', {
        'is_edit_mode': is_edit_mode,
        'listing': listing,
        'edit_listing_id': listing.pk if (listing and listing.pk) else None,
        'type_choices': Listing.BIKE_TYPE_CHOICES,
        'brand_choices': BIKE_BRANDS,
        'condition_choices': [(v, l) for v, l in Listing.CONDITION_CHOICES
                              if v in ('used', 'new')],
        'color_choices': Listing.COLOR_CHOICES,
        'tyre_kind_choices': Listing.TYRE_KIND_CHOICES,
        'equipment_by_category': get_bike_equipment(),
        'selected_equipment': selected_equipment,
        'years': list(range(timezone.now().year, 1914, -1)),
        'country_choices': _country_choices(),
        'us_states': Listing.US_STATE_CHOICES,
        'user_phone': user_phone,
        'posted': posted,
    })
