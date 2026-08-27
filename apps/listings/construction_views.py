import os
import re
import unicodedata
from datetime import date

from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .constants import can_create_listing, can_create_free_listing, FREE_LISTING_DAYS
from .image_validation import split_valid_images
from .models import Listing, ListingImage, VehicleType, SubCategory, FuelType
from .views import (
    _int_or_none,
    _float_or_none,
    get_coordinates_for_location,
    _send_listing_published_email,
    _send_saved_listing_updated_emails,
    _send_saved_listing_price_drop_emails,
    COUNTRY_FLAGS,
)
from apps.listings import brands as brand_source


# ═══════════════════════════════════════════════════════════
# STATYBINĖ TECHNIKA (vehicle_type slug='construction')
#
# DVI subkategorijos = DVI skirtingos formos, ne viena su jungikliu:
#   construction-machinery   — 21 laukas, su Marke ir Kuro tipu
#   construction-attachments — 8 laukai, be Markės, Mėnesio, SDK, Galios
# Iš 21 technikos lauko priedai dalinasi tik 8, todėl vienas šablonas su
# {% if %} aplink pusę laukų būtų neskaitomas. Bendra lieka čia:
# subkategorijų logika, markės, kontaktai, nuotraukos.
#
# Ypatumų ši kategorija NETURI (0 checkbox'ų) — skirtingai nei priekabos
# ar žemės ūkis, todėl Equipment eilučių nekuriam.
# ═══════════════════════════════════════════════════════════

CONSTR_VT_SLUG = 'construction'
MACHINERY_SUB = 'construction-machinery'
ATTACHMENTS_SUB = 'construction-attachments'



# Markės — iš bendros Brand lentelės (šeima „construction"). Anksčiau čia
# buvo skaitomas atskiras .txt failas; failas lieka repozitorijoje
# kaip seed'as, bet formos ir filtrai ima iš DB.
def _brand_names():
    from apps.listings import brands as brand_source
    return list(brand_source.brands_qs('construction').values_list('name', flat=True))


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


CONSTR_BRANDS = _BrandList()


# ─── Tipas → naršymo subkategorija ───
# 'forklifts' sąmoningai be atitikmens: šakinių krautuvų etalono 39 tipų
# sąraše nėra — autogide tai „Krovimo ir sandėliavimo technika" (sec 20).
CONSTR_TYPE_TO_SUBCATEGORY = {
    'buldozeris': 'bulldozers',
    'ekskavatorius_krautuvas': 'excavators',
    'ekskavatorius_griovimo': 'excavators',
    'ekskavatorius_ratinis': 'excavators',
    'ekskavatorius_viksrinis': 'excavators',
    'mini_ekskavatorius': 'excavators',
    'automobilinis_krautuvas': 'loaders',
    'frontalinis_krautuvas': 'loaders',
    'kausinis_krautuvas': 'loaders',
    'mini_krautuvas': 'loaders',
    'zirklinis_krautuvas': 'loaders',
    'automobilinis_kranas': 'cranes',
    'kranas': 'cranes',
    'manipuliatorius': 'cranes',
    'automobilinis_bokstelis': 'cranes',
    'betono_gamybos_irenginys': 'concrete-mixers',
    'betonvezis': 'concrete-mixers',
    'tankinimo_technika': 'compactors',
    'vibracines_plokstes': 'compactors',
    'vibrovolai': 'compactors',
    'volai': 'compactors',
}
CONSTR_DEFAULT_SUBCATEGORY = 'other-construction'


def _resolve_subcategory(slug):
    if not slug:
        return None
    return SubCategory.objects.filter(
        vehicle_type__slug=CONSTR_VT_SLUG, slug=slug
    ).first()


def _subcategory_for(constr_type):
    """Tipas → subkategorija. Persiskaičiuoja KAS IŠSAUGOJIMĄ."""
    slug = CONSTR_TYPE_TO_SUBCATEGORY.get(constr_type, CONSTR_DEFAULT_SUBCATEGORY)
    return _resolve_subcategory(slug)


def _type_for_subcategory(slug):
    """Atvirkštinis — iš URL TIK preselekcijai."""
    if not slug:
        return ''
    matches = [t for t, s in CONSTR_TYPE_TO_SUBCATEGORY.items() if s == slug]
    return matches[0] if len(matches) == 1 else ''


def _country_choices():
    _all = list(Listing.COUNTRY_CHOICES)
    _us = [c for c in _all if c[0] == 'US']
    _rest = sorted([c for c in _all if c[0] != 'US'], key=lambda x: x[1])
    return [
        (code, f"{COUNTRY_FLAGS.get(code, '🌍')} {name}")
        for code, name in (_us + _rest)
    ]


def _base_context(request, listing, is_edit_mode, posted):
    """Abiem formoms bendras kontekstas."""
    user_phone = ''
    if hasattr(request.user, 'profile') and request.user.profile.phone_number:
        user_phone = request.user.profile.phone_number
    return {
        'is_edit_mode': is_edit_mode,
        'listing': listing,
        'edit_listing_id': listing.pk if (listing and listing.pk) else None,
        'condition_choices': [
            (v, l) for v, l in Listing.CONDITION_CHOICES if v in ('used', 'new')
        ],
        'years': list(range(timezone.now().year, 1914, -1)),
        'months': list(range(1, 13)),
        'country_choices': _country_choices(),
        'us_states': Listing.US_STATE_CHOICES,
        'user_phone': user_phone,
        'posted': posted,
    }


def _save_common(request, target, errors, require_month=True):
    """Laukai, kuriuos pildo abi formos."""
    condition = request.POST.get('condition', '')
    if not condition:
        errors.append(_('Būklė yra privaloma'))
    else:
        target.condition = condition

    target.constr_model_text = (request.POST.get('constr_model_text', '') or '').strip()[:32]

    year = _int_or_none(request.POST.get('year'))
    month = _int_or_none(request.POST.get('month'))
    if year:
        target.year = year
    elif require_month:
        errors.append(_('Metai yra privalomi'))
    else:
        target.year = target.year or timezone.now().year
    if require_month and not month:
        errors.append(_('Mėnuo yra privalomas'))
    if year and month:
        try:
            target.first_registration = date(year=year, month=month, day=1)
        except (ValueError, TypeError):
            pass

    # Kaina ABIEM formoms NEPRIVALOMA (skiriasi nuo kitų kategorijų)
    target.price = _float_or_none(request.POST.get('price')) or 0
    target.export_price = _float_or_none(request.POST.get('export_price'))
    target.taxes_extra = request.POST.get('taxes_extra') == 'on'
    target.negotiable = request.POST.get('negotiable') == 'on'

    target.curb_weight = _int_or_none(request.POST.get('curb_weight'))
    target.length_m = _float_or_none(request.POST.get('length_m'))
    target.width_m = _float_or_none(request.POST.get('width_m'))
    target.height_m = _float_or_none(request.POST.get('height_m'))

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

    return errors


def _finish(request, target, is_edit_mode, old_price, new_images):
    """Bendra pabaiga: koordinatės, save, nuotraukos, laiškai, redirect."""
    lat, lng = get_coordinates_for_location(target.city, target.country, request.POST)
    target.latitude, target.longitude = lat, lng
    target.save()

    existing = target.images.count()
    for i, image in enumerate(new_images[:36]):
        try:
            ListingImage.objects.create(
                listing=target, image=image,
                is_main=(existing == 0 and i == 0), order=existing + i,
            )
        except Exception as e:
            print(f"[construction] image upload failed: {e}")

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


def _guard(request, is_edit_mode, edit_pk, expect_attachment):
    """Bendri patikrinimai; grąžina (listing, redirect|None)."""
    listing = None
    if is_edit_mode:
        listing = get_object_or_404(Listing, pk=edit_pk, seller=request.user)
        if not listing.vehicle_type or listing.vehicle_type.slug != CONSTR_VT_SLUG:
            messages.error(request, _('Ši forma skirta tik statybinės technikos skelbimams.'))
            return None, redirect('listing_edit_hub', pk=edit_pk)
        is_attach = bool(listing.constr_attach_type) or (
            listing.subcategory and listing.subcategory.slug == ATTACHMENTS_SUB
        )
        if is_attach != expect_attachment:
            target_url = ('/create/construction/attachment/?edit=%d' if is_attach
                          else '/create/construction/?edit=%d') % edit_pk
            return None, redirect(target_url)
    else:
        can_create, active_count, limit = can_create_listing(request.user)
        if not can_create:
            messages.error(
                request,
                f'You have reached your active listings limit ({active_count}/{limit}). '
                f'Upgrade your account to create more listings.',
            )
            return None, redirect('listing_upgrade')
    return listing, None


# ═══════════════════════════════════════════════════════════
# A) STATYBINĖ TECHNIKA (section 24)
# ═══════════════════════════════════════════════════════════
@login_required
def construction_listing_create(request):
    """URL: /create/construction/?new=1&subcategory=<slug>  |  ?edit=<pk>"""
    vt = VehicleType.objects.filter(slug=CONSTR_VT_SLUG).first()
    if not vt:
        messages.error(request, _('Statybinės technikos kategorija nesukonfigūruota.'))
        return redirect('listing_list')

    edit_pk = _int_or_none(request.GET.get('edit')) or _int_or_none(request.POST.get('edit'))
    is_edit_mode = bool(edit_pk)
    listing, bail = _guard(request, is_edit_mode, edit_pk, expect_attachment=False)
    if bail:
        return bail

    if is_edit_mode:
        preselected_type = listing.constr_type
    else:
        preselected_type = _type_for_subcategory(request.GET.get('subcategory', ''))

    if request.method == 'POST':
        target = listing if is_edit_mode else Listing(
            seller=request.user, vehicle_type=vt, status='draft')
        old_price = float(target.price) if (is_edit_mode and target.price) else 0
        errors = []

        constr_type = request.POST.get('constr_type', '')
        if not constr_type:
            errors.append(_('Tipas yra privalomas'))
        target.constr_type = constr_type
        target.constr_attach_type = ''

        brand = brand_source.posted_brand(request, 'constr_brand_text', 'construction')
        if not brand:
            errors.append(_('Markė yra privaloma'))
        target.constr_brand_text = brand[:80]

        # Subkategorija VISADA iš formos
        target.subcategory = _subcategory_for(constr_type)

        target.sdk_number = (request.POST.get('sdk_number', '') or '').strip()[:8]
        target.power = _int_or_none(request.POST.get('power'))
        target.constr_drive_type = request.POST.get('constr_drive_type', '') or ''
        target.wheel_formula = request.POST.get('wheel_formula', '') or ''
        target.mileage = _int_or_none(request.POST.get('mileage')) or 0
        target.fuel_tank_capacity_l = _int_or_none(request.POST.get('fuel_tank_capacity_l'))
        target.engine_hours = _int_or_none(request.POST.get('engine_hours'))
        target.payload_kg = _int_or_none(request.POST.get('payload_kg'))

        ft_id = _int_or_none(request.POST.get('fuel_type'))
        target.fuel_type = FuelType.objects.filter(pk=ft_id).first() if ft_id else None

        errors = _save_common(request, target, errors, require_month=True)

        if not is_edit_mode and not request.POST.get('agree_terms'):
            errors.append(_('Turite sutikti su taisyklėmis'))

        parts = [p for p in (target.constr_brand_text, target.constr_model_text) if p]
        if target.year:
            parts.append(str(target.year))
        if not parts:
            parts.append(dict(Listing.CONSTR_TYPE_CHOICES).get(constr_type, '') or 'Construction')
        target.title = ' '.join(str(p) for p in parts)[:200]

        new_images, img_errors = split_valid_images(request.FILES.getlist('images'))
        errors.extend(img_errors)

        if errors:
            for e in errors:
                messages.error(request, e)
            return _render_machinery(request, target, preselected_type,
                                     is_edit_mode, request.POST)
        return _finish(request, target, is_edit_mode, old_price, new_images)

    return _render_machinery(request, listing, preselected_type, is_edit_mode, None)


def _render_machinery(request, listing, preselected_type, is_edit_mode, posted):
    ctx = _base_context(request, listing, is_edit_mode, posted)
    selected_month = ''
    if posted:
        selected_month = posted.get('month', '')
    elif listing and listing.first_registration:
        selected_month = str(listing.first_registration.month)
    ctx.update({
        'selected_month': selected_month,
        'preselected_type': preselected_type,
        'type_choices': Listing.CONSTR_TYPE_CHOICES,
        'drive_type_choices': Listing.CONSTR_DRIVE_TYPE_CHOICES,
        'wheel_formula_choices': [c for c in Listing.WHEEL_FORMULA_CHOICES if c[0]],
        'brand_choices': CONSTR_BRANDS,
        'fuel_types': FuelType.objects.all().order_by('name'),
    })
    return render(request, 'listings/construction_listing_create.html', ctx)


# ═══════════════════════════════════════════════════════════
# B) STATYBINĖS TECHNIKOS PRIEDAI (section 16)
# Be Markės, Mėnesio, SDK, Galios, Kuro tipo, Ridos, Motovalandų.
# ═══════════════════════════════════════════════════════════
@login_required
def construction_attachment_create(request):
    """URL: /create/construction/attachment/?new=1  |  ?edit=<pk>"""
    vt = VehicleType.objects.filter(slug=CONSTR_VT_SLUG).first()
    if not vt:
        messages.error(request, _('Statybinės technikos kategorija nesukonfigūruota.'))
        return redirect('listing_list')

    edit_pk = _int_or_none(request.GET.get('edit')) or _int_or_none(request.POST.get('edit'))
    is_edit_mode = bool(edit_pk)
    listing, bail = _guard(request, is_edit_mode, edit_pk, expect_attachment=True)
    if bail:
        return bail

    if request.method == 'POST':
        target = listing if is_edit_mode else Listing(
            seller=request.user, vehicle_type=vt, status='draft')
        old_price = float(target.price) if (is_edit_mode and target.price) else 0
        errors = []

        attach_type = request.POST.get('constr_attach_type', '')
        if not attach_type:
            errors.append(_('Tipas yra privalomas'))
        target.constr_attach_type = attach_type
        target.constr_type = ''
        target.constr_brand_text = ''

        # Priedai VISADA patenka į savo subkategoriją
        target.subcategory = _resolve_subcategory(ATTACHMENTS_SUB)

        errors = _save_common(request, target, errors, require_month=False)

        if not is_edit_mode and not request.POST.get('agree_terms'):
            errors.append(_('Turite sutikti su taisyklėmis'))

        label = dict(Listing.CONSTR_ATTACH_TYPE_CHOICES).get(attach_type, '')
        parts = [p for p in (str(label), target.constr_model_text) if p]
        target.title = ' '.join(parts)[:200] or 'Attachment'

        new_images, img_errors = split_valid_images(request.FILES.getlist('images'))
        errors.extend(img_errors)

        if errors:
            for e in errors:
                messages.error(request, e)
            return _render_attachment(request, target, is_edit_mode, request.POST)
        return _finish(request, target, is_edit_mode, old_price, new_images)

    return _render_attachment(request, listing, is_edit_mode, None)


def _render_attachment(request, listing, is_edit_mode, posted):
    ctx = _base_context(request, listing, is_edit_mode, posted)
    ctx['attach_type_choices'] = Listing.CONSTR_ATTACH_TYPE_CHOICES
    return render(request, 'listings/construction_attachment_create.html', ctx)
