import json

from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from apps.listings import brands as brand_source

from .constants import can_create_listing, can_create_free_listing, FREE_LISTING_DAYS
from .equipment_registry import RENT_EQUIPMENT_DEFINITION
from .image_validation import split_valid_images
from .models import (
    Listing, ListingImage, VehicleType, SubCategory, FuelType, Transmission,
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
# TRANSPORTO NUOMA (vehicle_type slug='rental')
#
# Penkios etalono sekcijos → KETURIOS formos: automobilių ir limuzinų
# nuoma skiriasi tik trim laukais (kėbulas, durys, metalikas), todėl
# dalinasi vienu šablonu; subkategorija imama iš formos lauko `rent_kind`,
# ne iš URL (žr. SKILL.md — dažniausia projekto klaida).
#
# Kitos trys formos dengia po vieną subkategoriją, todėl jų subkategorija
# fiksuota (kaip construction priedų forma).
#
# „Nuomos kaina parai" saugoma bendrame `price` lauke — privaloma visur.
# Valandinė kaina — `rent_price_hour`.
# ═══════════════════════════════════════════════════════════

RENT_VT_SLUG = 'rental'


# Formos raktas → (subkategorijos slug'as, markių failas, šablonas)
FORM_SPEC = {
    'car':     (('car-rental', 'limo-wedding-rental'), 'nuomos-auto-markes.txt',
                'listings/rental_car_create.html'),
    'moto':    (('motorcycle-rental',), 'nuomos-moto-markes.txt',
                'listings/rental_moto_create.html'),
    'minibus': (('minibus-touring-water-rental',), 'nuomos-mikroautobusu-markes.txt',
                'listings/rental_minibus_create.html'),
    'heavy':   (('heavy-trailer-rental',), 'nuomos-sunkiojo-markes.txt',
                'listings/rental_heavy_create.html'),
}

# Subkategorija → forma (redagavimo dispečeriui ir pikeriui)
SUB_TO_FORM = {
    sub: form for form, (subs, _f, _t) in FORM_SPEC.items() for sub in subs
}

# rent_type reikšmės pagal sekciją (etalonas: sec 33 septynios, sec 34 šešios)
MINIBUS_RENT_TYPES = ('bus', 'water', 'moto_rental', 'passenger_minibus',
                      'cargo_minibus', 'towed_house', 'touring_car')
HEAVY_RENT_TYPES = ('road_train', 'agri_constr', 'truck', 'tractor_unit',
                    'warehouse', 'trailer')

# Etalone motociklų nuomos kuro tipai — tik trys
MOTO_FUEL_NAMES = ('Petrol', 'Diesel', 'Electric')
# Pavarų dėžė nuomoje — dvi (Mechaninė / Automatinė)
RENT_TRANSMISSION_NAMES = ('Manual', 'Automatic')


def _form_rent_types(form_key):
    if form_key == 'minibus':
        return MINIBUS_RENT_TYPES
    if form_key == 'heavy':
        return HEAVY_RENT_TYPES
    return ()


# Nuomos forma savo markių sąrašo neturi — kaip autogide, markės imamos
# iš atitinkamos pardavimo kategorijos šeimos. Automobilių ir motociklų
# nuoma turi po vieną šeimą, mikroautobusų ir sunkiojo — po kelias,
# priklausomai nuo pasirinkto „Tipo".
FORM_FIXED_SCOPE = {'car': 'cars', 'moto': 'motorcycles'}


def brands_by_type(form_key):
    """{rent_type: [markių pavadinimai]} — sąrašas persijungia pagal Tipą."""
    out = {}
    for rent_type in _form_rent_types(form_key):
        scope = brand_source.scope_for(rent_type=rent_type)
        if not scope:
            continue
        out[rent_type] = list(
            brand_source.brands_qs(scope).values_list('name', flat=True))
    return out


def brands_for(form_key, rent_type=''):
    """Markės formai. Be pasirinkto Tipo — visų tos formos šeimų sąjunga,
    kad nė viena markė nebūtų nepasiekiama (autogide tokiu atveju
    parodomas automobilių sąrašas — akivaizdi jų klaida)."""
    scope = FORM_FIXED_SCOPE.get(form_key)
    if scope:
        return list(brand_source.brands_qs(scope).values_list('name', flat=True))
    by_type = brands_by_type(form_key)
    if rent_type and rent_type in by_type:
        return by_type[rent_type]
    names = set()
    for values in by_type.values():
        names.update(values)
    return sorted(names, key=lambda n: n.lower())


def get_rent_equipment():
    """3 nuomos sąlygų ypatumai (idempotentiškai sukuriami)."""
    grouped = []
    for cat_key, cat_label, names in RENT_EQUIPMENT_DEFINITION:
        items = [Equipment.objects.get_or_create(category=cat_key, name=n)[0]
                 for n in names]
        grouped.append({'key': cat_key, 'label': cat_label, 'items': items})
    return grouped


def _resolve_sub(slug):
    return SubCategory.objects.filter(
        vehicle_type__slug=RENT_VT_SLUG, slug=slug).first()


def _country_choices():
    # Šalys — vienas sąrašas visai svetainei (apps/listings/salys.py)
    from apps.listings import salys
    return salys.plokscias()


# ═══════════════════════════════════════════════════════════
# BENDRAS SRAUTAS
# ═══════════════════════════════════════════════════════════

def _handle(request, form_key, parse_fields):
    """Vienas create+edit POST srautas (boats patternas).

    parse_fields(request, target, errors) — formai specifiniai laukai;
    grąžina subkategorijos slug'ą (arba None, jei forma dengia vieną).
    """
    subs, _brand_file, template = FORM_SPEC[form_key]

    vt = VehicleType.objects.filter(slug=RENT_VT_SLUG).first()
    if not vt:
        messages.error(request, _('Transporto nuomos kategorija nesukonfigūruota.'))
        return redirect('listing_list')

    edit_pk = _int_or_none(request.GET.get('edit')) or _int_or_none(request.POST.get('edit'))
    is_edit_mode = bool(edit_pk)
    listing = None

    if is_edit_mode:
        listing = get_object_or_404(Listing, pk=edit_pk, seller=request.user)
        if not listing.vehicle_type or listing.vehicle_type.slug != RENT_VT_SLUG:
            messages.error(request, _('Ši forma skirta tik nuomos skelbimams.'))
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

        # ─── bendri visoms nuomos formoms ───
        rent_type_posted = (request.POST.get('rent_type', '') or '').strip()
        brand_scope = (brand_source.scope_for(rent_type=rent_type_posted)
                       or FORM_FIXED_SCOPE.get(form_key, ''))
        brand = brand_source.posted_brand(
            request, 'rent_brand_text', brand_scope)
        if not brand:
            errors.append(_('Markė yra privaloma'))
        target.rent_brand_text = brand[:80]

        model = (request.POST.get('constr_model_text', '') or '').strip()
        if not model:
            errors.append(_('Modelis yra privalomas'))
        target.constr_model_text = model[:32]

        year = _int_or_none(request.POST.get('year'))
        if not year:
            errors.append(_('Metai yra privalomi'))
        else:
            target.year = year

        price = _float_or_none(request.POST.get('price'))
        if price is None or price <= 0:
            errors.append(_('Nuomos kaina parai yra privaloma'))
        else:
            target.price = price
        target.rent_price_hour = _float_or_none(request.POST.get('rent_price_hour'))
        target.negotiable = request.POST.get('negotiable') == 'on'

        target.mileage = _int_or_none(request.POST.get('mileage')) or 0
        target.power = _int_or_none(request.POST.get('power'))
        target.color = request.POST.get('color', '') or ''
        target.description = request.POST.get('description', '') or ''
        target.video_url = request.POST.get('video_url', '') or ''

        # ─── formai specifiniai ───
        sub_slug = parse_fields(request, target, errors) or subs[0]
        target.subcategory = _resolve_sub(sub_slug)

        # ─── kontaktai ───
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

        parts = [p for p in (target.rent_brand_text, target.constr_model_text) if p]
        if target.year:
            parts.append(str(target.year))
        target.title = ' '.join(str(p) for p in parts)[:200] or 'Rental'

        new_images, img_errors = split_valid_images(request.FILES.getlist('images'))
        errors.extend(img_errors)

        if errors:
            for e in errors:
                messages.error(request, e)
            return _render(request, form_key, target, is_edit_mode, request.POST)

        target.latitude, target.longitude = get_coordinates_for_location(target.city, target.country, request.POST)

        try:
            target.save()
        except Exception as e:
            messages.error(request, f'Save failed: {e}')
            return _render(request, form_key, target, is_edit_mode, request.POST)

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
                print(f"[rental] image upload failed: {e}")

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

    return _render(request, form_key, listing, is_edit_mode, None)


def _render(request, form_key, listing, is_edit_mode, posted):
    subs, _brand_file, template = FORM_SPEC[form_key]

    user_phone = ''
    if hasattr(request.user, 'profile') and request.user.profile.phone_number:
        user_phone = request.user.profile.phone_number

    selected_equipment = []
    if listing and listing.pk:
        selected_equipment = [
            str(i) for i in listing.equipment_items.values_list('equipment_id', flat=True)]
    elif posted:
        selected_equipment = posted.getlist('equipment')

    # rent_kind — TIK automobilių/limuzinų formai; iš POST, iš įrašo arba iš URL
    rent_kind = ''
    if len(subs) > 1:
        if posted:
            rent_kind = posted.get('rent_kind', '')
        elif listing and listing.subcategory:
            rent_kind = listing.subcategory.slug
        else:
            rent_kind = request.GET.get('sub') or subs[0]
        if rent_kind not in subs:
            rent_kind = subs[0]

    rent_type_values = (MINIBUS_RENT_TYPES if form_key == 'minibus'
                        else HEAVY_RENT_TYPES if form_key == 'heavy' else ())
    fuel_qs = FuelType.objects.all().order_by('name')
    if form_key == 'moto':
        fuel_qs = fuel_qs.filter(name__in=MOTO_FUEL_NAMES)

    return render(request, template, {
        'form_key': form_key,
        'is_edit_mode': is_edit_mode,
        'listing': listing,
        'edit_listing_id': listing.pk if (listing and listing.pk) else None,
        'rent_kind': rent_kind,
        'kind_choices': [
            ('car-rental', _('Automobilių nuoma')),
            ('limo-wedding-rental', _('Limuzinų, vestuvių transporto nuoma')),
        ],
        'brand_choices': brands_for(
            form_key, getattr(listing, 'rent_type', '') or ''),
        'brands_by_type_json': json.dumps(brands_by_type(form_key),
                                          ensure_ascii=False),
        'type_choices': [(v, l) for v, l in Listing.RENT_TYPE_CHOICES
                         if v in rent_type_values],
        'body_type_choices': Listing.BODY_TYPE_CHOICES,
        'door_choices': Listing.DOOR_CHOICES,
        'color_choices': Listing.COLOR_CHOICES,
        'cooling_choices': Listing.COOLING_TYPE_CHOICES,
        'motorcycle_type_choices': Listing.MOTORCYCLE_TYPE_CHOICES,
        'trailer_kind_choices': Listing.TRAILER_KIND_CHOICES,
        'wheel_formula_choices': Listing.WHEEL_FORMULA_CHOICES,
        'fuel_types': fuel_qs,
        'transmissions': Transmission.objects.filter(
            name__in=RENT_TRANSMISSION_NAMES).order_by('name'),
        'equipment_by_category': [] if form_key == 'moto' else get_rent_equipment(),
        'selected_equipment': selected_equipment,
        'years': list(range(timezone.now().year, 1914, -1)),
        'country_choices': _country_choices(),
        'us_states': Listing.US_STATE_CHOICES,
        'user_phone': user_phone,
        'posted': posted,
    })


# ═══════════════════════════════════════════════════════════
# KETURIOS FORMOS
# ═══════════════════════════════════════════════════════════

@login_required
def rental_car_create(request):
    """sec 31 + 32 — automobilių ir limuzinų / vestuvių transporto nuoma."""
    def parse(request, target, errors):
        # Subkategorija — IŠ FORMOS, kas išsaugojimą; URL tik preselekcijai
        kind = request.POST.get('rent_kind', '')
        if kind not in FORM_SPEC['car'][0]:
            kind = FORM_SPEC['car'][0][0]

        target.modification = (request.POST.get('modification', '') or '').strip()[:32]
        target.engine_capacity = _float_or_none(request.POST.get('engine_capacity'))
        ft_id = _int_or_none(request.POST.get('fuel_type'))
        target.fuel_type = FuelType.objects.filter(pk=ft_id).first() if ft_id else None
        tr_id = _int_or_none(request.POST.get('transmission'))
        target.transmission = Transmission.objects.filter(pk=tr_id).first() if tr_id else None

        seats = _int_or_none(request.POST.get('seats_count'))
        if not seats:
            errors.append(_('Sėdimų vietų skaičius yra privalomas'))
        target.seats_count = seats

        # Kėbulas / durys / metalikas — tik automobilių nuomoje
        if kind == 'car-rental':
            body = request.POST.get('body_type', '')
            if not body:
                errors.append(_('Kėbulo tipas yra privalomas'))
            target.body_type = body
            target.doors = request.POST.get('doors', '') or ''
            target.metallic = request.POST.get('metallic') == 'on'
        else:
            target.body_type = ''
            target.doors = ''
            target.metallic = False

        target.fuel_tank_capacity_l = _int_or_none(request.POST.get('fuel_tank_capacity_l'))
        target.fuel_consumption_combined = _float_or_none(
            request.POST.get('fuel_consumption_combined'))
        return kind

    return _handle(request, 'car', parse)


@login_required
def rental_moto_create(request):
    """sec 35 — motociklų nuoma (etalone ypatumų neturi)."""
    def parse(request, target, errors):
        mtype = request.POST.get('motorcycle_type', '')
        if not mtype:
            errors.append(_('Motociklo tipas yra privalomas'))
        target.motorcycle_type = mtype

        target.engine_capacity_cc = _int_or_none(request.POST.get('engine_capacity_cc'))
        target.cooling_type = request.POST.get('cooling_type', '') or ''
        target.metallic = request.POST.get('metallic') == 'on'
        ft_id = _int_or_none(request.POST.get('fuel_type'))
        target.fuel_type = FuelType.objects.filter(pk=ft_id).first() if ft_id else None
        return None

    return _handle(request, 'moto', parse)


@login_required
def rental_minibus_create(request):
    """sec 33 — mikroautobusų, turistinio ir vandens transporto nuoma."""
    def parse(request, target, errors):
        rtype = request.POST.get('rent_type', '')
        if rtype not in MINIBUS_RENT_TYPES:
            errors.append(_('Tipas yra privalomas'))
            rtype = ''
        target.rent_type = rtype

        seats = _int_or_none(request.POST.get('seats_count'))
        if not seats:
            errors.append(_('Sėdimų vietų skaičius yra privalomas'))
        target.seats_count = seats
        target.sleeping_seats = _int_or_none(request.POST.get('sleeping_seats'))

        ft_id = _int_or_none(request.POST.get('fuel_type'))
        target.fuel_type = FuelType.objects.filter(pk=ft_id).first() if ft_id else None
        tr_id = _int_or_none(request.POST.get('transmission'))
        target.transmission = Transmission.objects.filter(pk=tr_id).first() if tr_id else None
        target.engine_capacity = _float_or_none(request.POST.get('engine_capacity'))
        target.fuel_tank_capacity_l = _int_or_none(request.POST.get('fuel_tank_capacity_l'))
        target.fuel_consumption_combined = _float_or_none(
            request.POST.get('fuel_consumption_combined'))
        return None

    return _handle(request, 'minibus', parse)


@login_required
def rental_heavy_create(request):
    """sec 34 — sunkiojo transporto ir priekabų nuoma."""
    def parse(request, target, errors):
        rtype = request.POST.get('rent_type', '')
        if rtype not in HEAVY_RENT_TYPES:
            errors.append(_('Tipas yra privalomas'))
            rtype = ''
        target.rent_type = rtype

        target.trailer_kind = request.POST.get('trailer_kind', '') or ''
        target.wheel_formula = request.POST.get('wheel_formula', '') or ''
        target.payload_kg = _int_or_none(request.POST.get('payload_kg'))
        target.fork_length_m = _float_or_none(request.POST.get('fork_length_m'))
        target.curb_weight = _int_or_none(request.POST.get('curb_weight'))
        target.gross_weight_kg = _int_or_none(request.POST.get('gross_weight_kg'))
        ft_id = _int_or_none(request.POST.get('fuel_type'))
        target.fuel_type = FuelType.objects.filter(pk=ft_id).first() if ft_id else None
        return None

    return _handle(request, 'heavy', parse)
