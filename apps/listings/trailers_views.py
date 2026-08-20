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
    TRAILERS_SUBCATEGORY_SLUGS,
)
from apps.listings import brands as brand_source


# ═══════════════════════════════════════════════════════════
# TRAILERS — Priekabos / Puspriekabės (vehicle_type slug='trailers')
# Sekamas boats patternas: vienas view, create+edit per vieną POST,
# jokio draft session — listing kuriamas tik POST metu.
#
# Tipas (Priekaba/Puspriekabė) ir Paskirtis (22) yra ORTOGONALŪS:
# puspriekabė gali būti ir šaldytuvas, ir savivartė. Todėl Tipas gyvena
# atskirame lauke, o subcategory išvedama iš Paskirties — NE hardcodinama
# (trucks_views.py:172 klaida, kur ?subcategory= ignoruojamas).
# ═══════════════════════════════════════════════════════════

# TRAILERS_SUBCATEGORY_SLUGS importuojamas iš views.py (žr. importą aukščiau) —
# ten jis gyvena, kad listing_create pikeris jį matytų be ciklinio importo.

# Paskirtis → naršymo subkategorija (9 esamos DB eilutės).
# Kelios paskirtys sąmoningai krenta į tą pačią subkategoriją.
TRAILER_PURPOSE_TO_SUBCATEGORY = {
    'car_trailer':        'car-trailers',
    'for_car_transport':  'car-trailers',
    'car_carrier':        'car-trailers',
    'tipper':             'tipper-trailers',
    'refrigerator':       'refrigerator-trailers',
    'insulated_body':     'refrigerator-trailers',
    'tarpaulin':          'curtainsider-trailers',
    'flatbed_tarpaulin':  'curtainsider-trailers',
    'platform':           'flatbed-trailers',
    'flatbed':            'flatbed-trailers',
    'touring':            'caravans',
    'watercraft':         'boat-trailers',
}

# Likusios paskirtys (cisterninė, gyvuliams, konteinerių važiuoklė, miškavežio,
# betonvežio, keičiamas kėbulas, krovininė, motociklų, traktoriaus, kita)
# neturi savo naršymo segmento — jos eina į 'other-trailers'.
TRAILER_DEFAULT_SUBCATEGORY = 'other-trailers'

# Puspriekabė be konkrečios paskirties atitikmens — savas segmentas.
TRAILER_SEMI_SUBCATEGORY = 'semi-trailers'


# ─── Būklė — tik Naudotos / Naujos (Listing.CONDITION_CHOICES turi ir
#     'damaged', kurio autogidas priekaboms nesiūlo) ───
TRAILER_CONDITION_CHOICES = [
    (v, l) for v, l in Listing.CONDITION_CHOICES if v in ('used', 'new')
]

# ─── Euro standartas — Euro 1..6 + Kitas (be euro6d, kurio priekabos neturi) ───
TRAILER_EURO_CHOICES = [
    (v, l) for v, l in Listing.EURO_STANDARD_CHOICES
    if v in ('euro1', 'euro2', 'euro3', 'euro4', 'euro5', 'euro6', 'other')
]

# ─── Bendras ratų skaičius: 2–13 + >13 ───
TRAILER_WHEEL_COUNT_CHOICES = (
    [(str(n), str(n)) for n in range(2, 14)] + [('13plus', '>13')]
)

# ─── Ašys (gamintojas) — 20 reikšmių ───
TRAILER_AXLE_MAKES = [
    'ALKO', 'BPW', 'BPW eco', 'Daimler', 'Fontenax', 'Fruehauf', 'Gigant',
    'Granning', 'Hendrickson', 'Kassbohrer', 'Kitos', 'Knott', 'Kogel',
    'Krone', 'Mercedes-Benz', 'ROR', 'SAF', 'Schmitz Cargobull', 'SMB',
    'Trailor',
]

# ─── Padangų likutis % — 10, 20 ... 100 ───
TRAILER_TYRE_PCT_CHOICES = [(str(p), f'{p}%') for p in range(10, 101, 10)]

# ─── TA iki — metai 2025–2030 ───
TRAILER_INSPECTION_YEARS = list(range(2025, 2031))

# ─── Markės — 195 (autogidas.lt tvarka, 'Kita' pabaigoje) ───
# Laisvas tekstas, ne FK: skirtingai nuo trucks, "Modelis" čia yra laisvas
# tekstas, todėl brand→model kaskados nereikia (kaip boats boat_make_text).
# Markės — iš bendros Brand lentelės (šeima „trailers", 192).
# Anksčiau sąrašas gyveno čia, Python konstantoje.
def _trailer_brand_names():
    from apps.listings import brands as brand_source
    return list(brand_source.brands_qs('trailers').values_list('name', flat=True))


class _BrandList:
    """Tingus sąrašas — DB neliečiama importo metu."""

    def _names(self):
        return _trailer_brand_names()

    def __iter__(self):
        return iter(self._names())

    def __len__(self):
        return len(self._names())

    def __contains__(self, item):
        return item in self._names()

    def __getitem__(self, idx):
        return self._names()[idx]


TRAILER_BRANDS = _BrandList()


# ═══════════════════════════════════════════════════════════
# YPATUMAI — 25 checkbox'ai.
# Saugoma kaip Equipment eilutės su 'trailer_*' kategorija (trucks patternas,
# trucks_views.py:361) — jokios migracijos nereikia, o item.id lieka stabilus.
# Cars/moto/truck equipment neliečiamas.
# ═══════════════════════════════════════════════════════════
# Apibrėžimai gyvena equipment_registry — juos turi matyti ir
# `seed_equipment` komanda, ir 0063 migracija.
from .equipment_registry import TRAILER_EQUIPMENT_DEFINITION  # noqa: E402


def _get_trailer_equipment():
    """Trailer ypatumai, sugrupuoti šablonui.

    Kiekvienas item idempotentiškai sukuriamas Equipment lentelėje su
    'trailer_*' kategorijos prefiksu, kad nesimaišytų su cars/moto/truck.
    """
    grouped = []
    for cat_key, cat_label, item_names in TRAILER_EQUIPMENT_DEFINITION:
        items = []
        for name in item_names:
            obj, _created = Equipment.objects.get_or_create(
                category=cat_key,
                name=name,
            )
            items.append(obj)
        grouped.append({
            'key': cat_key,
            'label': cat_label,
            'items': items,
        })
    return grouped


def _resolve_trailers_subcategory(slug):
    """Pagal slug grąžina trailers SubCategory (vehicle_type=trailers)."""
    if not slug:
        return None
    return SubCategory.objects.filter(
        vehicle_type__slug='trailers', slug=slug
    ).first()


def _subcategory_for(purpose, kind):
    """Paskirtis (+ Tipas) → naršymo subkategorija.

    Puspriekabė be aiškaus paskirties atitikmens lieka 'semi-trailers',
    kad naršymo segmentas neliktų tuščias.
    """
    slug = TRAILER_PURPOSE_TO_SUBCATEGORY.get(purpose)
    if not slug:
        slug = (
            TRAILER_SEMI_SUBCATEGORY if kind == 'semi_trailer'
            else TRAILER_DEFAULT_SUBCATEGORY
        )
    return _resolve_trailers_subcategory(slug)


def _purpose_for_subcategory(slug):
    """Atvirkštinis mapping'as — pikerio subkategorija preselektina Paskirtį.

    Grąžina '' kai subkategorija dengia kelias paskirtis (car-trailers,
    other-trailers, semi-trailers) — tada vartotojas renkasi pats.
    """
    if not slug:
        return ''
    matches = [
        p for p, s in TRAILER_PURPOSE_TO_SUBCATEGORY.items() if s == slug
    ]
    return matches[0] if len(matches) == 1 else ''


def _trailers_country_choices():
    _all = list(Listing.COUNTRY_CHOICES)
    _us = [c for c in _all if c[0] == 'US']
    _rest = sorted([c for c in _all if c[0] != 'US'], key=lambda x: x[1])
    return [
        (code, f"{COUNTRY_FLAGS.get(code, '🌍')} {name}")
        for code, name in (_us + _rest)
    ]


@login_required
def trailers_listing_create(request):
    """Create + Edit trailer listing (single page, one POST).

    URL:       /create/trailers/?new=1&subcategory=<slug>
    URL EDIT:  /create/trailers/?edit=<pk>
    """
    trailers_vt = VehicleType.objects.filter(slug='trailers').first()
    if not trailers_vt:
        messages.error(request, _('Priekabų kategorija nesukonfigūruota.'))
        return redirect('listing_list')

    # ═══ EDIT MODE ═══
    edit_pk = _int_or_none(request.GET.get('edit')) or _int_or_none(request.POST.get('edit'))
    is_edit_mode = bool(edit_pk)
    listing = None

    if is_edit_mode:
        listing = get_object_or_404(Listing, pk=edit_pk, seller=request.user)
        if not listing.vehicle_type or listing.vehicle_type.slug != 'trailers':
            messages.error(request, _('Ši forma skirta tik priekabų skelbimams.'))
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
        preselected_purpose = listing.trailer_purpose
    else:
        picked_slug = request.GET.get('subcategory', '')
        selected_sub = _resolve_trailers_subcategory(picked_slug)
        preselected_purpose = _purpose_for_subcategory(picked_slug)

    # ═══════════════════════════════════════════════════════════
    # POST
    # ═══════════════════════════════════════════════════════════
    if request.method == 'POST':
        target = listing if is_edit_mode else None
        old_price = float(target.price) if (is_edit_mode and target.price) else 0

        if not is_edit_mode:
            target = Listing(
                seller=request.user,
                vehicle_type=trailers_vt,
                status='draft',
            )

        errors = []

        # ─── Būklė (required) ───
        condition = request.POST.get('condition', '')
        if not condition:
            errors.append(_('Būklė yra privaloma'))
        else:
            target.condition = condition

        # ─── Tipas (required) ───
        trailer_kind = request.POST.get('trailer_kind', '')
        if not trailer_kind:
            errors.append(_('Tipas yra privalomas'))
        target.trailer_kind = trailer_kind

        # ─── Markė (required) / Modelis ───
        brand_text = brand_source.posted_brand(request, 'trailer_brand_text', 'trailers')
        if not brand_text:
            errors.append(_('Markė yra privaloma'))
        target.trailer_brand_text = brand_text[:80]
        target.trailer_model_text = (request.POST.get('trailer_model_text', '') or '').strip()[:80]

        # ─── Metai + Mėnuo (required) ───
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

        # ─── Paskirtis (required) → subcategory ───
        purpose = request.POST.get('trailer_purpose', '')
        if not purpose:
            errors.append(_('Paskirtis yra privaloma'))
        target.trailer_purpose = purpose
        # Subkategorija VISADA išvedama iš formos, o ne hardcodinama.
        target.subcategory = _subcategory_for(purpose, trailer_kind) or selected_sub
        selected_sub = target.subcategory

        # ─── Ratai / ašys ───
        target.trailer_wheel_count = request.POST.get('trailer_wheel_count', '') or ''
        target.trailer_axle_make = request.POST.get('trailer_axle_make', '') or ''
        axle_count = request.POST.get('trailer_axle_count', '') or ''
        target.trailer_axle_count = axle_count

        # ─── Pakaba ir padangos ×3 ───
        # Rodomų blokų skaičių valdo JS, bet serveris irgi apkarpo: jei ašių
        # 1, antros/trečios ašies duomenys neišsaugomi (kad neliktų šiukšlių
        # persigalvojus formoje).
        visible_axles = {'1': 1, '2': 2, '3': 3, '3plus': 3, 'other': 3}.get(axle_count, 0)
        for idx in (1, 2, 3):
            if idx <= visible_axles:
                setattr(target, f'trailer_susp_{idx}', request.POST.get(f'trailer_susp_{idx}', '') or '')
                setattr(target, f'trailer_tyre_pct_{idx}', _int_or_none(request.POST.get(f'trailer_tyre_pct_{idx}')))
                setattr(target, f'trailer_tyre_size_{idx}', (request.POST.get(f'trailer_tyre_size_{idx}', '') or '').strip()[:40])
            else:
                setattr(target, f'trailer_susp_{idx}', '')
                setattr(target, f'trailer_tyre_pct_{idx}', None)
                setattr(target, f'trailer_tyre_size_{idx}', '')

        # ─── Euro standartas / SDK / VIN ───
        target.euro_standard = request.POST.get('euro_standard', '') or ''
        target.sdk_number = (request.POST.get('sdk_number', '') or '').strip()[:50]
        target.vin = (request.POST.get('vin', '') or '').strip()

        # ─── Matmenys (mm) — perpanaudoti truck_* laukai ───
        target.truck_height_mm = _int_or_none(request.POST.get('truck_height_mm'))
        target.truck_length_mm = _int_or_none(request.POST.get('truck_length_mm'))
        target.truck_width_mm = _int_or_none(request.POST.get('truck_width_mm'))

        # ─── Masės / tūris ───
        target.gross_weight_kg = _int_or_none(request.POST.get('gross_weight_kg'))
        target.curb_weight = _int_or_none(request.POST.get('curb_weight'))
        target.truck_volume_m3 = _float_or_none(request.POST.get('truck_volume_m3'))
        target.payload_kg = _int_or_none(request.POST.get('payload_kg'))

        # ─── Spalva ───
        target.color = request.POST.get('color', '') or ''

        # ─── TA iki ───
        target.technical_inspection_year = _int_or_none(request.POST.get('technical_inspection_year'))
        target.technical_inspection_month = _int_or_none(request.POST.get('technical_inspection_month'))

        # Listing.mileage yra NOT NULL — priekabos jo nenaudoja
        if target.mileage is None:
            target.mileage = 0

        # ─── Kaina ───
        price = _float_or_none(request.POST.get('price'))
        if price is None or price <= 0:
            errors.append(_('Kaina yra privaloma'))
        else:
            target.price = price
        target.export_price = _float_or_none(request.POST.get('export_price'))
        target.taxes_extra = request.POST.get('taxes_extra') == 'on'
        target.negotiable = request.POST.get('negotiable') == 'on'
        target.open_to_trade = request.POST.get('open_to_trade') == 'on'

        # ─── Komentarai + Video ───
        target.description = request.POST.get('description', '') or ''
        target.video_url = request.POST.get('video_url', '') or ''

        # ─── Vieta + kontaktai (contact_block.html laukai) ───
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

        # ─── Pavadinimas ───
        title_parts = []
        if target.trailer_brand_text:
            title_parts.append(target.trailer_brand_text)
        if target.trailer_model_text:
            title_parts.append(target.trailer_model_text)
        if target.year:
            title_parts.append(str(target.year))
        if not title_parts and selected_sub:
            title_parts.append(selected_sub.name)
        target.title = ' '.join(title_parts) or 'Trailer listing'

        new_images, _image_errors = split_valid_images(
            request.FILES.getlist('images')
        )
        errors.extend(_image_errors)

        if errors:
            for e in errors:
                messages.error(request, e)
            return _render_trailers_form(
                request, listing=target,
                selected_sub=selected_sub,
                preselected_purpose=purpose,
                is_edit_mode=is_edit_mode,
                posted=request.POST,
            )

        lat, lng = get_coordinates_for_location(target.city, target.country)
        target.latitude = lat
        target.longitude = lng

        try:
            target.save()
        except Exception as e:
            messages.error(request, f'Save failed: {e}')
            return _render_trailers_form(
                request, listing=target,
                selected_sub=selected_sub,
                preselected_purpose=purpose,
                is_edit_mode=is_edit_mode,
                posted=request.POST,
            )

        # ─── Ypatumai (ListingEquipment) ───
        eq_ids = request.POST.getlist('equipment')
        ListingEquipment.objects.filter(listing=target).delete()
        for eid in eq_ids:
            try:
                ListingEquipment.objects.create(listing=target, equipment_id=int(eid))
            except (ValueError, TypeError):
                continue

        # ─── Nuotraukos ───
        existing_count = target.images.count()
        for i, image in enumerate(new_images[:36]):
            try:
                ListingImage.objects.create(
                    listing=target,
                    image=image,
                    is_main=(existing_count == 0 and i == 0),
                    order=existing_count + i,
                )
            except Exception as e:
                print(f"[trailers] image upload failed: {e}")

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
            messages.success(request, _('Skelbimas atnaujintas.'))
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
    return _render_trailers_form(
        request, listing=listing,
        selected_sub=selected_sub,
        preselected_purpose=preselected_purpose,
        is_edit_mode=is_edit_mode,
        posted=None,
    )


def _render_trailers_form(request, listing=None, selected_sub=None,
                          preselected_purpose='', is_edit_mode=False, posted=None):
    """Render trailers form. `listing` may be unsaved (POST error) or saved (edit)."""

    user_phone = ''
    if hasattr(request.user, 'profile') and request.user.profile.phone_number:
        user_phone = request.user.profile.phone_number

    selected_equipment = []
    if listing and listing.pk:
        selected_equipment = [
            str(eid) for eid in
            listing.equipment_items.values_list('equipment_id', flat=True)
        ]
    elif posted:
        selected_equipment = posted.getlist('equipment')

    # Mėnuo: edit režimu iš first_registration, po klaidos — iš POST
    selected_month = ''
    if posted:
        selected_month = posted.get('month', '')
    elif listing and listing.first_registration:
        selected_month = str(listing.first_registration.month)

    context = {
        'is_edit_mode': is_edit_mode,
        'listing': listing,
        'edit_listing_id': listing.pk if (listing and listing.pk) else None,
        'selected_sub': selected_sub,
        'subcategory_slug': selected_sub.slug if selected_sub else '',
        'subcategory_name': selected_sub.name if selected_sub else '',
        'preselected_purpose': preselected_purpose,
        'selected_month': selected_month,

        'condition_choices': TRAILER_CONDITION_CHOICES,
        'kind_choices': Listing.TRAILER_KIND_CHOICES,
        'purpose_choices': Listing.TRAILER_PURPOSE_CHOICES,
        'axle_count_choices': Listing.TRAILER_AXLE_COUNT_CHOICES,
        'suspension_choices': Listing.TRAILER_SUSPENSION_CHOICES,
        'brand_choices': TRAILER_BRANDS,
        'axle_make_choices': TRAILER_AXLE_MAKES,
        'wheel_count_choices': TRAILER_WHEEL_COUNT_CHOICES,
        'tyre_pct_choices': TRAILER_TYRE_PCT_CHOICES,
        'euro_choices': TRAILER_EURO_CHOICES,
        'color_choices': Listing.COLOR_CHOICES,
        'inspection_years': TRAILER_INSPECTION_YEARS,
        'months': list(range(1, 13)),
        'years': list(range(timezone.now().year + 1, 1914, -1)),

        'equipment_by_category': _get_trailer_equipment(),
        'selected_equipment': selected_equipment,

        'country_choices': _trailers_country_choices(),
        'us_states': Listing.US_STATE_CHOICES,
        'user_phone': user_phone,
        'posted': posted,
    }
    return render(request, 'listings/trailers_listing_create.html', context)
