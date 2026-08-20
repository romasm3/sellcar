import os
import unicodedata
from datetime import date

from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext as _
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .constants import can_create_listing, can_create_free_listing, FREE_LISTING_DAYS
from .equipment_registry import CAMP_EQUIPMENT_DEFINITION
from .image_validation import split_valid_images
from .models import (
    Listing, ListingImage, VehicleType, FuelType, Transmission,
    Equipment, ListingEquipment,
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
# TURISTINIAI NAMELIAI (vehicle_type slug='camping-houses')
#
# Sekamas boats patternas: vienas view, create+edit per vieną POST.
#
# Ši kategorija artimesnė AUTOMOBILIAMS nei technikai — 24 laukai
# perpanaudoti (rida, spalva, pavarų dėžė, varantieji ratai, darbinis
# tūris, defektai, ratlankiai, sėdimos/miegamos vietos ir kt.).
#
# Subkategorijų NĖRA → subcategory lieka NULL, pikeris veda tiesiai į
# formą per CREATE_URL_BY_VEHICLE_TYPE.
#
# „Tinka su B kat. teisėmis" yra Listing LAUKAS (b_licence_ok), ne
# Equipment eilutė — jis filtruojamas ir greitojoje panelėje.
#
# Ypatumai — savi 52 su 'camp_' prefiksu. Automobilių ypatumai suvesti
# angliškai, todėl sutampa tik „ESP"; be prefikso paieška griebtų
# automobilių eilutę ir grąžintų 0 rezultatų.
# ═══════════════════════════════════════════════════════════

CAMP_VT_SLUG = 'camping-houses'


# Pavarų dėžė — etalonas siūlo tik dvi; Transmission turi ir CVT/Semi-automatic
CAMP_TRANSMISSION_NAMES = ('Manual', 'Automatic')

# Padangų likutis % — 5..100 po 5
CAMP_TYRE_PCT_CHOICES = [(p, f'{p}%') for p in range(5, 101, 5)]

# Pavarų skaičius 3..12
CAMP_GEARBOX_SPEEDS = list(range(3, 13))


# Markės — iš bendros Brand lentelės (šeima „campers"). Anksčiau čia
# buvo skaitomas atskiras .txt failas; failas lieka repozitorijoje
# kaip seed'as, bet formos ir filtrai ima iš DB.
def _brand_names():
    from apps.listings import brands as brand_source
    return list(brand_source.brands_qs('campers').values_list('name', flat=True))


class _BrandList:
    """Tingus sąrašas — DB neliečiama importo metu."""

    def _names(self):
        return _brand_names()

    def __iter__(self):
        return iter(self._names())

    def __len__(self):
        return len(self._names())

    def __contains__(self, item):
        return item in self._names()

    def __getitem__(self, idx):
        return self._names()[idx]


CAMP_BRANDS = _BrandList()


def get_camp_equipment():
    """52 ypatumai, sugrupuoti šablonui (idempotentiškai sukuriami)."""
    grouped = []
    for cat_key, cat_label, names in CAMP_EQUIPMENT_DEFINITION:
        items = []
        for name in names:
            obj, _created = Equipment.objects.get_or_create(
                category=cat_key, name=name,
            )
            items.append(obj)
        grouped.append({'key': cat_key, 'label': cat_label, 'items': items})
    return grouped


def _country_choices():
    _all = list(Listing.COUNTRY_CHOICES)
    _us = [c for c in _all if c[0] == 'US']
    _rest = sorted([c for c in _all if c[0] != 'US'], key=lambda x: x[1])
    return [
        (code, f"{COUNTRY_FLAGS.get(code, '🌍')} {name}")
        for code, name in (_us + _rest)
    ]


@login_required
def camping_listing_create(request):
    """URL: /create/camping-houses/?new=1  |  ?edit=<pk>"""
    vt = VehicleType.objects.filter(slug=CAMP_VT_SLUG).first()
    if not vt:
        messages.error(request, _('Turistinių namelių kategorija nesukonfigūruota.'))
        return redirect('listing_list')

    edit_pk = _int_or_none(request.GET.get('edit')) or _int_or_none(request.POST.get('edit'))
    is_edit_mode = bool(edit_pk)
    listing = None

    if is_edit_mode:
        listing = get_object_or_404(Listing, pk=edit_pk, seller=request.user)
        if not listing.vehicle_type or listing.vehicle_type.slug != CAMP_VT_SLUG:
            messages.error(request, _('Ši forma skirta tik turistinių namelių skelbimams.'))
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

        camp_type = request.POST.get('camp_type', '')
        if not camp_type:
            errors.append(_('Tipas yra privalomas'))
        target.camp_type = camp_type

        brand = (request.POST.get('camp_brand_text', '') or '').strip()
        if not brand:
            errors.append(_('Markė yra privaloma'))
        target.camp_brand_text = brand[:80]

        model = (request.POST.get('constr_model_text', '') or '').strip()
        if not model:
            errors.append(_('Modelis yra privalomas'))
        target.constr_model_text = model[:32]

        target.sleeping_seats = _int_or_none(request.POST.get('sleeping_seats'))
        target.seats = request.POST.get('seats', '') or ''

        year = _int_or_none(request.POST.get('year'))
        month = _int_or_none(request.POST.get('month'))
        if not year:
            errors.append(_('Metai yra privalomi'))
        else:
            target.year = year
        if year and month:
            try:
                target.first_registration = date(year=year, month=month, day=1)
            except (ValueError, TypeError):
                pass

        target.sdk_number = (request.POST.get('sdk_number', '') or '').strip()[:8]

        price = _float_or_none(request.POST.get('price'))
        if price is None or price <= 0:
            errors.append(_('Kaina yra privaloma'))
        else:
            target.price = price
        target.export_price = _float_or_none(request.POST.get('export_price'))
        target.taxes_extra = request.POST.get('taxes_extra') == 'on'
        target.negotiable = request.POST.get('negotiable') == 'on'

        # ─── Papildomi (automobiliniai laukai) ───
        ft_id = _int_or_none(request.POST.get('fuel_type'))
        target.fuel_type = FuelType.objects.filter(pk=ft_id).first() if ft_id else None
        target.fuel_tank_capacity_l = _int_or_none(request.POST.get('fuel_tank_capacity_l'))
        target.modification = (request.POST.get('modification', '') or '').strip()[:32]
        target.engine_capacity = _float_or_none(request.POST.get('engine_capacity'))
        target.technical_inspection_year = _int_or_none(request.POST.get('technical_inspection_year'))
        target.technical_inspection_month = _int_or_none(request.POST.get('technical_inspection_month'))
        target.mileage = _int_or_none(request.POST.get('mileage')) or 0
        target.color = request.POST.get('color', '') or ''
        target.rim_size = (request.POST.get('rim_size', '') or '').strip()[:20]
        target.tyre_condition_pct = _int_or_none(request.POST.get('tyre_condition_pct'))
        target.gearbox_speeds = _int_or_none(request.POST.get('gearbox_speeds'))
        target.drive_type = request.POST.get('drive_type', '') or ''
        tr_id = _int_or_none(request.POST.get('transmission'))
        target.transmission = Transmission.objects.filter(pk=tr_id).first() if tr_id else None
        target.power = _int_or_none(request.POST.get('power'))
        target.defects = request.POST.get('defects', '') or 'none'
        target.b_licence_ok = request.POST.get('b_licence_ok') == 'on'

        target.description = request.POST.get('description', '') or ''
        target.video_url = request.POST.get('video_url', '') or ''

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

        parts = [p for p in (target.camp_brand_text, target.constr_model_text) if p]
        if target.year:
            parts.append(str(target.year))
        if not parts:
            parts.append(dict(Listing.CAMP_TYPE_CHOICES).get(camp_type, '') or 'Camper')
        target.title = ' '.join(str(p) for p in parts)[:200]

        new_images, img_errors = split_valid_images(request.FILES.getlist('images'))
        errors.extend(img_errors)

        if errors:
            for e in errors:
                messages.error(request, e)
            return _render_form(request, target, is_edit_mode, request.POST)

        lat, lng = get_coordinates_for_location(target.city, target.country)
        target.latitude, target.longitude = lat, lng

        try:
            target.save()
        except Exception as e:
            messages.error(request, f'Save failed: {e}')
            return _render_form(request, target, is_edit_mode, request.POST)

        eq_ids = request.POST.getlist('equipment')
        ListingEquipment.objects.filter(listing=target).delete()
        for eid in eq_ids:
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
                print(f"[camping] image upload failed: {e}")

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
                reverse('listing_success', kwargs={'pk': target.pk}) + '?action=published'
            )
        return redirect('listing_select_plan', pk=target.pk)

    return _render_form(request, listing, is_edit_mode, None)


def _render_form(request, listing, is_edit_mode, posted):
    user_phone = ''
    if hasattr(request.user, 'profile') and request.user.profile.phone_number:
        user_phone = request.user.profile.phone_number

    selected_equipment = []
    if listing and listing.pk:
        selected_equipment = [
            str(i) for i in listing.equipment_items.values_list('equipment_id', flat=True)
        ]
    elif posted:
        selected_equipment = posted.getlist('equipment')

    selected_month = ''
    if posted:
        selected_month = posted.get('month', '')
    elif listing and listing.first_registration:
        selected_month = str(listing.first_registration.month)

    return render(request, 'listings/camping_listing_create.html', {
        'is_edit_mode': is_edit_mode,
        'listing': listing,
        'edit_listing_id': listing.pk if (listing and listing.pk) else None,
        'selected_month': selected_month,
        'type_choices': Listing.CAMP_TYPE_CHOICES,
        'brand_choices': CAMP_BRANDS,
        'condition_choices': [
            (v, l) for v, l in Listing.CONDITION_CHOICES if v in ('used', 'new')
        ],
        'seats_choices': Listing.SEATS_CHOICES,
        'color_choices': Listing.COLOR_CHOICES,
        'defect_choices': Listing.DEFECT_CHOICES,
        'drive_type_choices': Listing.DRIVE_TYPE_CHOICES,
        'tyre_pct_choices': CAMP_TYRE_PCT_CHOICES,
        'gearbox_speeds': CAMP_GEARBOX_SPEEDS,
        'fuel_types': FuelType.objects.all().order_by('name'),
        'transmissions': Transmission.objects.filter(
            name__in=CAMP_TRANSMISSION_NAMES).order_by('name'),
        'equipment_by_category': get_camp_equipment(),
        'selected_equipment': selected_equipment,
        'months': list(range(1, 13)),
        'years': list(range(timezone.now().year, 1914, -1)),
        'inspection_years': list(range(timezone.now().year, timezone.now().year + 6)),
        'country_choices': _country_choices(),
        'us_states': Listing.US_STATE_CHOICES,
        'user_phone': user_phone,
        'posted': posted,
    })
