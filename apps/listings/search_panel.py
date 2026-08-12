# apps/listings/search_panel.py
# ═══════════════════════════════════════════════════════════
# Paieškos panelės DALYS tab'o duomenys.
#
# Trys subkategorijos (kaip autogide):
#   car   → single-part-or-kit      → listing_list?category=parts
#   moto  → single-moto-part        → moto_parts_browse
#   truck → whole-truck-for-parts   → truck_parts_browse
#
# Laukai panelėje ir GET param'ai sutampa 1:1 su tais, kuriuos
# browse view'ai jau priima — naujų filtrų čia nekuriam.
# ═══════════════════════════════════════════════════════════

from django.db.models import Count
from django.utils.translation import gettext_lazy as _

from .models import (
    Brand,
    Equipment,
    Listing,
    MotorcycleBrand,
    SubCategory,
    TruckBrand,
    VehicleType,
)

PARTS_VT_SLUG = 'parts'

# (raktas, subkategorijos slug, etiketė)
PARTS_PANEL_SUBS = (
    ('car', 'single-part-or-kit', _('Automobilių, mikroautobusų dalys')),
    ('moto', 'single-moto-part', _('Motociklų dalys')),
    ('truck', 'whole-truck-for-parts', _('Sunkiojo transporto dalys')),
)

# Kurios subkategorijos rodomos „Detalės kategorija" select'e (car tab)
CAR_PART_SUBCATEGORY_SLUGS = ('single-part-or-kit', 'whole-car-for-parts')

# count endpoint'o raktai → subkategorijos raktas
COUNT_KEY_TO_SUB = {
    'parts': 'car',
    'moto-parts': 'moto',
    'truck-parts': 'truck',
}


def _parts_base_qs(user=None):
    """Vieši parts skelbimai (naudoja tą patį _public_listings_qs kaip visur)."""
    from .views import _public_listings_qs
    return _public_listings_qs(user).filter(vehicle_type__slug=PARTS_VT_SLUG)


def _int_or_none(value):
    if value in (None, ''):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _equipment_groups(categories):
    """[(key, label)] → [{'key','label','items'}] tik su neturščiomis grupėmis."""
    groups = []
    for key, label in categories:
        items = list(Equipment.objects.filter(category=key).order_by('name'))
        if items:
            groups.append({'key': key, 'label': label, 'items': items})
    return groups


def _brands_with_counts(model, qs, field_name):
    """Markių sąrašas su skelbimų kiekiais, rūšiuotas kaip cars tab'e."""
    counts = {
        row[field_name]: row['c']
        for row in qs.values(field_name).annotate(c=Count('id'))
    }
    brands = [
        {'id': b.id, 'name': b.name, 'listing_count': counts.get(b.id, 0)}
        for b in model.objects.all().order_by('name')
    ]
    brands.sort(key=lambda b: (-b['listing_count'], b['name']))
    return brands


def parts_panel_context(user=None):
    """Visas DALYS tab'o kontekstas (flyout + trys formos)."""
    from .moto_part_views import MOTO_PART_CATEGORIES
    from .truck_for_parts_views import TRUCK_PART_CATEGORIES

    base = _parts_base_qs(user)

    sub_ids = {
        s.slug: s.id
        for s in SubCategory.objects.filter(vehicle_type__slug=PARTS_VT_SLUG)
    }
    sub_counts = {
        row['subcategory__slug']: row['c']
        for row in base.values('subcategory__slug').annotate(c=Count('id'))
    }

    subs = [
        {
            'key': key,
            'slug': slug,
            'id': sub_ids.get(slug, ''),
            'label': label,
            'count': sub_counts.get(slug, 0),
        }
        for key, slug, label in PARTS_PANEL_SUBS
    ]

    car_qs = base.filter(subcategory__slug='single-part-or-kit')
    moto_qs = base.filter(subcategory__slug='single-moto-part')
    truck_qs = base.filter(subcategory__slug='whole-truck-for-parts')

    return {
        'parts_subs': subs,
        'parts_car_subcats': [
            {
                'id': sub_ids.get(slug, ''),
                'name': SubCategory.objects.filter(slug=slug).values_list('name', flat=True).first() or slug,
                'count': sub_counts.get(slug, 0),
            }
            for slug in CAR_PART_SUBCATEGORY_SLUGS
            if slug in sub_ids
        ],
        'parts_brands': _brands_with_counts(Brand, car_qs, 'brand_id'),
        'parts_moto_brands': _brands_with_counts(
            MotorcycleBrand, moto_qs, 'motorcycle_brand_id'
        ),
        'parts_truck_brands': _brands_with_counts(
            TruckBrand, truck_qs, 'truck_brand_id'
        ),
        'parts_moto_groups': _equipment_groups(MOTO_PART_CATEGORIES),
        'parts_truck_groups': _equipment_groups(TRUCK_PART_CATEGORIES),
    }


def parts_count_qs(sub_key, params, user=None):
    """Queryset panelės „Skelbimai N" mygtukui.

    Tie patys param'ai, kuriuos priima atitinkamas browse view'as —
    tik tie, kuriuos panelė realiai rodo.
    """
    qs = _parts_base_qs(user)

    def _get(key):
        value = params.get(key)
        return value.strip() if isinstance(value, str) else value

    def _getlist(key):
        if hasattr(params, 'getlist'):
            return [v for v in params.getlist(key) if v]
        value = params.get(key)
        return [value] if value else []

    if sub_key == 'car':
        subcategory = _int_or_none(_get('subcategory'))
        if subcategory:
            qs = qs.filter(subcategory_id=subcategory)
        else:
            qs = qs.filter(subcategory__slug__in=CAR_PART_SUBCATEGORY_SLUGS)
        if _int_or_none(_get('brand')):
            qs = qs.filter(brand_id=_int_or_none(_get('brand')))
        if _int_or_none(_get('model')):
            qs = qs.filter(model_id=_int_or_none(_get('model')))
        # Miestas ir kuro tipas — listing_list juos jau filtruoja
        if _int_or_none(_get('fuel_type')):
            qs = qs.filter(fuel_type_id=_int_or_none(_get('fuel_type')))
        city = _get('city')
        if city:
            qs = qs.filter(city__icontains=city)

    elif sub_key == 'moto':
        # browse view'as ima tik status='active' — laikomės to paties
        qs = qs.filter(subcategory__slug='single-moto-part', status='active')
        if _int_or_none(_get('motorcycle_brand')):
            qs = qs.filter(motorcycle_brand_id=_int_or_none(_get('motorcycle_brand')))
        if _int_or_none(_get('motorcycle_model')):
            qs = qs.filter(motorcycle_model_id=_int_or_none(_get('motorcycle_model')))
        part_types = _getlist('part_types')
        if part_types:
            qs = qs.filter(equipment_items__equipment_id__in=part_types).distinct()

    elif sub_key == 'truck':
        qs = qs.filter(subcategory__slug='whole-truck-for-parts', status='active')
        if _int_or_none(_get('truck_brand')):
            qs = qs.filter(truck_brand_id=_int_or_none(_get('truck_brand')))
        model_text = _get('truck_model_text')
        if model_text:
            qs = qs.filter(truck_model_text__icontains=model_text)
        part_types = _getlist('part_types')
        if part_types:
            qs = qs.filter(equipment_items__equipment_id__in=part_types).distinct()

    else:
        return qs.none()

    # Bendri laukai visoms trims formoms
    if _int_or_none(_get('year_min')) is not None:
        qs = qs.filter(year__gte=_int_or_none(_get('year_min')))
    if _int_or_none(_get('year_max')) is not None:
        qs = qs.filter(year__lte=_int_or_none(_get('year_max')))
    if _int_or_none(_get('price_min')) is not None:
        qs = qs.filter(price__gte=_int_or_none(_get('price_min')))
    if _int_or_none(_get('price_max')) is not None:
        qs = qs.filter(price__lte=_int_or_none(_get('price_max')))

    # Tekstinė paieška — kiekvienas browse view'as turi savo param'ą:
    #   car   → listing_list priima „search" (tik title)
    #   moto  → moto_parts_browse: part_query (title | oem_code)
    #   truck → truck_parts_browse: part_query (title | oem_code)
    from django.db.models import Q

    if sub_key == 'car':
        search = _get('search')
        if search:
            qs = qs.filter(title__icontains=search)
    else:
        part_query = _get('part_query')
        if part_query:
            qs = qs.filter(
                Q(title__icontains=part_query) | Q(oem_code__icontains=part_query)
            )

    return qs
