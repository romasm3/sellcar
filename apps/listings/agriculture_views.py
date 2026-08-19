import os
import re
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
from .models import (
    Listing,
    ListingImage,
    VehicleType,
    SubCategory,
    Equipment,
    ListingEquipment,
)
from .views import (
    _int_or_none,
    _float_or_none,
    get_coordinates_for_location,
    _send_listing_published_email,
    _send_saved_listing_updated_emails,
    _send_saved_listing_price_drop_emails,
    COUNTRY_FLAGS,
    AGRICULTURE_SUBCATEGORY_SLUGS,
)


# ═══════════════════════════════════════════════════════════
# ŽEMĖS ŪKIO TECHNIKA, PADARGAI (vehicle_type slug='agriculture')
#
# Sekamas trailers patternas: vienas view, create+edit per vieną POST,
# jokio draft session — listing kuriamas tik POST metu.
#
# subcategory išvedama iš formos lauko „Tipas" ir persiskaičiuoja kas
# išsaugojimą; iš URL imama TIK preselekcija (trucks/parts klaida, kur
# subkategorija buvo hardcodinta, nekartojama).
# ═══════════════════════════════════════════════════════════

AGRI_VT_SLUG = 'agriculture'

# ─── Markės ───
# 700 reikšmių iš management/commands/zemes-ukio-markes.txt (ten jau guli
# brands.txt, models.txt — projekto įprotis). Skaitoma kartą importo metu.
BRANDS_PATH = os.path.join(
    os.path.dirname(__file__), 'management', 'commands', 'zemes-ukio-markes.txt'
)


def _load_brands():
    """Markės iš failo; dublikatai (Pöttinger/Pottinger) sujungiami."""
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
    # „Kita" visada pabaigoje
    rest = [n for n in out if n.casefold() != 'kita']
    other = [n for n in out if n.casefold() == 'kita']
    return rest + other


AGRI_BRANDS = _load_brands()


def _slug(name):
    x = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '_', x).strip('_')


# ─── Tipas → naršymo subkategorija ───
# Likusios 35 tipo reikšmės krenta į 'other-agricultural'.
# 'forestry-machines' sąmoningai be atitikmens: etalono „Tipas" sąraše
# miško technikos nėra — autogide tai atskira kategorija (mūsų 'forestry').
AGRI_TYPE_TO_SUBCATEGORY = {
    'traktorius':             'tractors',
    'kombainas':              'combines',
    'purkstuvai_pakabinami':  'sprayers',
    'purkstuvai_prikabinami': 'sprayers',
    'plugai':                 'ploughs',
    'kultivatorius':          'cultivators',
    'presai':                 'balers',
}
AGRI_DEFAULT_SUBCATEGORY = 'other-agricultural'


# ─── Ypatumai (9) — Equipment eilutės su 'agri_*' prefiksu ───
# Pavadinimai TIKSLIAI sutampa su paieškos konfigūracijomis; nesutapus
# checkbox'ai tyliai nebūtų rodomi paieškoje.
# Apibrėžimai gyvena equipment_registry — juos turi matyti ir
# `seed_equipment` komanda, ir 0063 migracija.
from .equipment_registry import AGRI_EQUIPMENT_DEFINITION  # noqa: E402


def get_agri_equipment():
    """Ypatumai, sugrupuoti šablonui (idempotentiškai sukuriami)."""
    grouped = []
    for cat_key, cat_label, names in AGRI_EQUIPMENT_DEFINITION:
        items = []
        for name in names:
            obj, _created = Equipment.objects.get_or_create(
                category=cat_key, name=name,
            )
            items.append(obj)
        grouped.append({'key': cat_key, 'label': cat_label, 'items': items})
    return grouped


def _resolve_subcategory(slug):
    if not slug:
        return None
    return SubCategory.objects.filter(
        vehicle_type__slug=AGRI_VT_SLUG, slug=slug
    ).first()


def _subcategory_for(agri_type):
    """Tipas → subkategorija (visada iš formos, ne iš URL)."""
    slug = AGRI_TYPE_TO_SUBCATEGORY.get(agri_type, AGRI_DEFAULT_SUBCATEGORY)
    return _resolve_subcategory(slug)


def _type_for_subcategory(slug):
    """Atvirkštinis mapping'as — pikerio subkategorija preselektina Tipą.

    Grąžina '' kai subkategorija dengia kelis tipus (sprayers,
    other-agricultural) — tada vartotojas renkasi pats.
    """
    if not slug:
        return ''
    matches = [t for t, s in AGRI_TYPE_TO_SUBCATEGORY.items() if s == slug]
    return matches[0] if len(matches) == 1 else ''


def _country_choices():
    _all = list(Listing.COUNTRY_CHOICES)
    _us = [c for c in _all if c[0] == 'US']
    _rest = sorted([c for c in _all if c[0] != 'US'], key=lambda x: x[1])
    return [
        (code, f"{COUNTRY_FLAGS.get(code, '🌍')} {name}")
        for code, name in (_us + _rest)
    ]


@login_required
def agriculture_listing_create(request):
    """Create + Edit žemės ūkio technikos skelbimą (vienas puslapis).

    URL:       /create/agriculture/?new=1&subcategory=<slug>
    URL EDIT:  /create/agriculture/?edit=<pk>
    """
    vt = VehicleType.objects.filter(slug=AGRI_VT_SLUG).first()
    if not vt:
        messages.error(request, _('Žemės ūkio technikos kategorija nesukonfigūruota.'))
        return redirect('listing_list')

    edit_pk = _int_or_none(request.GET.get('edit')) or _int_or_none(request.POST.get('edit'))
    is_edit_mode = bool(edit_pk)
    listing = None

    if is_edit_mode:
        listing = get_object_or_404(Listing, pk=edit_pk, seller=request.user)
        if not listing.vehicle_type or listing.vehicle_type.slug != AGRI_VT_SLUG:
            messages.error(request, _('Ši forma skirta tik žemės ūkio technikos skelbimams.'))
            return redirect('listing_edit_hub', pk=edit_pk)

    if not is_edit_mode:
        can_create, active_count, limit = can_create_listing(request.user)
        if not can_create:
            messages.error(
                request,
                f'You have reached your active listings limit ({active_count}/{limit}). '
                f'Upgrade your account to create more listings.',
            )
            return redirect('listing_upgrade')

    if is_edit_mode:
        selected_sub = listing.subcategory
        preselected_type = listing.agri_type
    else:
        picked = request.GET.get('subcategory', '')
        selected_sub = _resolve_subcategory(picked)
        preselected_type = _type_for_subcategory(picked)

    # ═══════════════════════════════════════════════════════════
    # POST
    # ═══════════════════════════════════════════════════════════
    if request.method == 'POST':
        target = listing if is_edit_mode else None
        old_price = float(target.price) if (is_edit_mode and target.price) else 0

        if not is_edit_mode:
            target = Listing(seller=request.user, vehicle_type=vt, status='draft')

        errors = []

        condition = request.POST.get('condition', '')
        if not condition:
            errors.append(_('Būklė yra privaloma'))
        else:
            target.condition = condition

        agri_type = request.POST.get('agri_type', '')
        if not agri_type:
            errors.append(_('Tipas yra privalomas'))
        target.agri_type = agri_type

        agri_kind = request.POST.get('agri_kind', '')
        if not agri_kind:
            errors.append(_('Padargas / Savaeigė yra privalomas'))
        target.agri_kind = agri_kind

        brand = (request.POST.get('agri_brand_text', '') or '').strip()
        if not brand:
            errors.append(_('Markė yra privaloma'))
        target.agri_brand_text = brand[:80]
        target.agri_model_text = (request.POST.get('agri_model_text', '') or '').strip()[:20]

        year = _int_or_none(request.POST.get('year'))
        month = _int_or_none(request.POST.get('month'))
        if not year:
            errors.append(_('Metai yra privalomi'))
        else:
            target.year = year
        if not month:
            errors.append(_('Mėnuo yra privalomas'))
        if year and month:
            try:
                target.first_registration = date(year=year, month=month, day=1)
            except (ValueError, TypeError):
                pass

        # Subkategorija VISADA iš formos, ne iš URL
        target.subcategory = _subcategory_for(agri_type) or selected_sub
        selected_sub = target.subcategory

        target.title = (request.POST.get('title', '') or '').strip()[:50]
        target.sdk_number = (request.POST.get('sdk_number', '') or '').strip()[:8]

        # ─── Papildomi (skaičiai) ───
        target.engine_hours = _int_or_none(request.POST.get('engine_hours'))
        target.power = _int_or_none(request.POST.get('power'))
        target.working_width_m = _float_or_none(request.POST.get('working_width_m'))
        target.curb_weight = _int_or_none(request.POST.get('curb_weight'))
        target.gross_weight_kg = _int_or_none(request.POST.get('gross_weight_kg'))
        target.payload_kg = _int_or_none(request.POST.get('payload_kg'))
        target.truck_volume_m3 = _float_or_none(request.POST.get('truck_volume_m3'))

        if target.mileage is None:
            target.mileage = 0

        price = _float_or_none(request.POST.get('price'))
        if price is None or price <= 0:
            errors.append(_('Kaina yra privaloma'))
        else:
            target.price = price
        target.export_price = _float_or_none(request.POST.get('export_price'))
        target.taxes_extra = request.POST.get('taxes_extra') == 'on'
        target.negotiable = request.POST.get('negotiable') == 'on'

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

        if not target.title:
            parts = [p for p in (target.agri_brand_text, target.agri_model_text) if p]
            if target.year:
                parts.append(str(target.year))
            if not parts:
                parts.append(dict(Listing.AGRI_TYPE_CHOICES).get(agri_type, '') or 'Agriculture')
            target.title = ' '.join(str(p) for p in parts)[:200]

        new_images, _img_errors = split_valid_images(request.FILES.getlist('images'))
        errors.extend(_img_errors)

        if errors:
            for e in errors:
                messages.error(request, e)
            return _render_form(request, listing=target, selected_sub=selected_sub,
                               preselected_type=agri_type, is_edit_mode=is_edit_mode,
                               posted=request.POST)

        lat, lng = get_coordinates_for_location(target.city, target.country)
        target.latitude, target.longitude = lat, lng

        try:
            target.save()
        except Exception as e:
            messages.error(request, f'Save failed: {e}')
            return _render_form(request, listing=target, selected_sub=selected_sub,
                               preselected_type=agri_type, is_edit_mode=is_edit_mode,
                               posted=request.POST)

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
                print(f"[agriculture] image upload failed: {e}")

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

    return _render_form(request, listing=listing, selected_sub=selected_sub,
                        preselected_type=preselected_type, is_edit_mode=is_edit_mode,
                        posted=None)


def _render_form(request, listing=None, selected_sub=None, preselected_type='',
                 is_edit_mode=False, posted=None):
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

    return render(request, 'listings/agriculture_listing_create.html', {
        'is_edit_mode': is_edit_mode,
        'listing': listing,
        'edit_listing_id': listing.pk if (listing and listing.pk) else None,
        'selected_sub': selected_sub,
        'subcategory_name': selected_sub.name if selected_sub else '',
        'preselected_type': preselected_type,
        'selected_month': selected_month,
        'type_choices': Listing.AGRI_TYPE_CHOICES,
        'kind_choices': Listing.AGRI_KIND_CHOICES,
        'brand_choices': AGRI_BRANDS,
        'condition_choices': [
            (v, l) for v, l in Listing.CONDITION_CHOICES if v in ('used', 'new')
        ],
        'equipment_by_category': get_agri_equipment(),
        'selected_equipment': selected_equipment,
        'months': list(range(1, 13)),
        'years': list(range(timezone.now().year, 1914, -1)),
        'country_choices': _country_choices(),
        'us_states': Listing.US_STATE_CHOICES,
        'user_phone': user_phone,
        'posted': posted,
    })
