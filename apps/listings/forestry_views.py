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
from .image_validation import split_valid_images
from .models import Listing, ListingImage, VehicleType, FuelType
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
# MIŠKO ŪKIO TECHNIKA (vehicle_type slug='forestry')
#
# Sekamas boats patternas: vienas view, create+edit per vieną POST.
#
# Trys dalykai, kuriais ši kategorija skiriasi nuo ankstesnių:
#   • subkategorijų NĖRA — subcategory lieka NULL, pikeris veda tiesiai
#     į formą per CREATE_URL_BY_VEHICLE_TYPE (kaip loading-equipment)
#   • ypatumų NĖRA — Equipment eilučių nekuriam (kaip construction)
#   • mėnesio lauko NĖRA — tik Metai, todėl first_registration nepildom
#
# Nauji tik du laukai; visa kita perpanaudota iš construction / agriculture.
# ═══════════════════════════════════════════════════════════

FOREST_VT_SLUG = 'forestry'

BRANDS_PATH = os.path.join(
    os.path.dirname(__file__), 'management', 'commands', 'misko-markes.txt'
)


def _load_brands():
    def norm(s):
        s = unicodedata.normalize('NFKD', s.casefold())
        return ''.join(c for c in s if not unicodedata.combining(c))

    seen, out = set(), []
    try:
        with open(BRANDS_PATH, encoding='utf-8') as fh:
            for line in fh:
                name = line.strip()
                if not name:
                    continue
                key = norm(name)
                if key in seen:
                    continue
                seen.add(key)
                out.append(name)
    except OSError:
        return []
    rest = [n for n in out if n.casefold() not in ('kita', 'kitas')]
    other = [n for n in out if n.casefold() in ('kita', 'kitas')]
    return rest + other


FOREST_BRANDS = _load_brands()


def _country_choices():
    _all = list(Listing.COUNTRY_CHOICES)
    _us = [c for c in _all if c[0] == 'US']
    _rest = sorted([c for c in _all if c[0] != 'US'], key=lambda x: x[1])
    return [
        (code, f"{COUNTRY_FLAGS.get(code, '🌍')} {name}")
        for code, name in (_us + _rest)
    ]


@login_required
def forestry_listing_create(request):
    """URL: /create/forestry/?new=1  |  ?edit=<pk>"""
    vt = VehicleType.objects.filter(slug=FOREST_VT_SLUG).first()
    if not vt:
        messages.error(request, _('Miško ūkio technikos kategorija nesukonfigūruota.'))
        return redirect('listing_list')

    edit_pk = _int_or_none(request.GET.get('edit')) or _int_or_none(request.POST.get('edit'))
    is_edit_mode = bool(edit_pk)
    listing = None

    if is_edit_mode:
        listing = get_object_or_404(Listing, pk=edit_pk, seller=request.user)
        if not listing.vehicle_type or listing.vehicle_type.slug != FOREST_VT_SLUG:
            messages.error(request, _('Ši forma skirta tik miško ūkio technikos skelbimams.'))
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

        forest_type = request.POST.get('forest_type', '')
        if not forest_type:
            errors.append(_('Tipas yra privalomas'))
        target.forest_type = forest_type

        brand = (request.POST.get('forest_brand_text', '') or '').strip()
        if not brand:
            errors.append(_('Markė yra privaloma'))
        target.forest_brand_text = brand[:80]
        target.constr_model_text = (request.POST.get('constr_model_text', '') or '').strip()[:32]

        year = _int_or_none(request.POST.get('year'))
        if not year:
            errors.append(_('Metai yra privalomi'))
        else:
            target.year = year
        # Mėnesio lauko ši kategorija neturi — first_registration nepildom

        target.power = _int_or_none(request.POST.get('power'))
        target.constr_drive_type = request.POST.get('constr_drive_type', '') or ''
        target.sdk_number = (request.POST.get('sdk_number', '') or '').strip()[:8]

        price = _float_or_none(request.POST.get('price'))
        if price is None or price <= 0:
            errors.append(_('Kaina yra privaloma'))
        else:
            target.price = price
        target.export_price = _float_or_none(request.POST.get('export_price'))
        target.taxes_extra = request.POST.get('taxes_extra') == 'on'
        target.negotiable = request.POST.get('negotiable') == 'on'

        # ─── Papildomi ───
        target.wheel_formula = request.POST.get('wheel_formula', '') or ''
        ft_id = _int_or_none(request.POST.get('fuel_type'))
        target.fuel_type = FuelType.objects.filter(pk=ft_id).first() if ft_id else None
        target.fuel_tank_capacity_l = _int_or_none(request.POST.get('fuel_tank_capacity_l'))
        # Matmenys METRAIS — tie patys laukai kaip statybinėje technikoje
        target.length_m = _float_or_none(request.POST.get('length_m'))
        target.width_m = _float_or_none(request.POST.get('width_m'))
        target.height_m = _float_or_none(request.POST.get('height_m'))
        target.engine_hours = _int_or_none(request.POST.get('engine_hours'))
        target.curb_weight = _int_or_none(request.POST.get('curb_weight'))
        target.gross_weight_kg = _int_or_none(request.POST.get('gross_weight_kg'))
        target.technical_inspection_year = _int_or_none(request.POST.get('technical_inspection_year'))
        target.technical_inspection_month = _int_or_none(request.POST.get('technical_inspection_month'))
        target.vin = (request.POST.get('vin', '') or '').strip()[:17]

        target.description = request.POST.get('description', '') or ''
        target.video_url = request.POST.get('video_url', '') or ''

        if target.mileage is None:
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

        parts = [p for p in (target.forest_brand_text, target.constr_model_text) if p]
        if target.year:
            parts.append(str(target.year))
        if not parts:
            parts.append(dict(Listing.FOREST_TYPE_CHOICES).get(forest_type, '') or 'Forestry')
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

        existing = target.images.count()
        for i, image in enumerate(new_images[:36]):
            try:
                ListingImage.objects.create(
                    listing=target, image=image,
                    is_main=(existing == 0 and i == 0), order=existing + i,
                )
            except Exception as e:
                print(f"[forestry] image upload failed: {e}")

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

    return render(request, 'listings/forestry_listing_create.html', {
        'is_edit_mode': is_edit_mode,
        'listing': listing,
        'edit_listing_id': listing.pk if (listing and listing.pk) else None,
        'type_choices': Listing.FOREST_TYPE_CHOICES,
        'drive_type_choices': Listing.CONSTR_DRIVE_TYPE_CHOICES,
        'wheel_formula_choices': [c for c in Listing.WHEEL_FORMULA_CHOICES if c[0]],
        'brand_choices': FOREST_BRANDS,
        'fuel_types': FuelType.objects.all().order_by('name'),
        'condition_choices': [
            (v, l) for v, l in Listing.CONDITION_CHOICES if v in ('used', 'new')
        ],
        'months': list(range(1, 13)),
        'years': list(range(timezone.now().year, 1914, -1)),
        'inspection_years': list(range(timezone.now().year, timezone.now().year + 6)),
        'country_choices': _country_choices(),
        'us_states': Listing.US_STATE_CHOICES,
        'user_phone': user_phone,
        'posted': posted,
    })
