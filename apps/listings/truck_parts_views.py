from .search_params import sanitize as sanitize_search_params
# ═══════════════════════ BROWSE + ADVANCED SEARCH ═══════════════════════
# Pridėti prie truck_for_parts_views.py GALO.
# Naudoja modulio TRUCK_PART_CATEGORIES → dalių grupės sutampa su create forma.

def _truck_part_groups():
    groups, total = [], 0
    for key, label in TRUCK_PART_CATEGORIES:
        items = list(Equipment.objects.filter(category=key).order_by('name'))
        if items:
            groups.append({'key': key, 'label': label, 'items': items})
            total += len(items)
    return groups, total


def _truck_country_choices():
    # Šalys — vienas sąrašas visai svetainei (apps/listings/salys.py)
    from apps.listings import salys
    return salys.plokscias()


def _tp_clean_list(values):
    return [v for v in values if v not in (None, '')]


def truck_parts_browse(request):
    # Sugadintos skaitinės reikšmės (?price_min=abc) tyliai išmetamos.
    request.GET = sanitize_search_params(request.GET)
    from django.db.models import Q
    from django.utils import timezone
    from datetime import timedelta

    qs = (
        Listing.objects
        .filter(
            vehicle_type__slug='parts',
            subcategory__slug=TRUCK_FOR_PARTS_SUBCATEGORY_SLUG,
            status='active',
        )
        .select_related('truck_brand', 'fuel_type')
        .prefetch_related('images')
    )
    G = request.GET

    part_types = _tp_clean_list(G.getlist('part_types'))
    if part_types:
        qs = qs.filter(listingequipment__equipment_id__in=part_types).distinct()

    brand_id = _int_or_none(G.get('truck_brand'))
    if brand_id:
        qs = qs.filter(truck_brand_id=brand_id)

    truck_types = _tp_clean_list(G.getlist('truck_type'))
    if truck_types:
        qs = qs.filter(truck_type__in=truck_types)

    model_q = (G.get('truck_model_text', '') or '').strip()
    if model_q:
        qs = qs.filter(truck_model_text__icontains=model_q)

    conditions = _tp_clean_list(G.getlist('condition'))
    if conditions:
        qs = qs.filter(condition__in=conditions)

    fuel_id = _int_or_none(G.get('fuel_type'))
    if fuel_id:
        qs = qs.filter(fuel_type_id=fuel_id)

    year_min = _int_or_none(G.get('year_min'))
    year_max = _int_or_none(G.get('year_max'))
    if year_min is not None:
        qs = qs.filter(year__gte=year_min)
    if year_max is not None:
        qs = qs.filter(year__lte=year_max)

    p_min = _int_or_none(G.get('power_min'))
    p_max = _int_or_none(G.get('power_max'))
    if p_min is not None:
        qs = qs.filter(power__gte=p_min)
    if p_max is not None:
        qs = qs.filter(power__lte=p_max)

    price_min = _int_or_none(G.get('price_min'))
    price_max = _int_or_none(G.get('price_max'))
    if price_min is not None:
        qs = qs.filter(price__gte=price_min)
    if price_max is not None:
        qs = qs.filter(price__lte=price_max)

    country = G.get('country_filter', '')
    if country:
        qs = qs.filter(country=country)
    state = G.get('state_filter', '')
    if state:
        qs = qs.filter(state=state)
    city = (G.get('city', '') or '').strip()
    if city:
        qs = qs.filter(city__icontains=city)

    posted = _int_or_none(G.get('posted_within'))
    if posted:
        qs = qs.filter(created_at__gte=timezone.now() - timedelta(days=posted))

    # seller_type — UI yra, bet filtras priklauso nuo profile lauko (kaip moto: kol kas off)
    # if G.get('seller_type'):
    #     qs = qs.filter(seller__profile__seller_type=G.get('seller_type'))

    q = (G.get('part_query', '') or '').strip()
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(oem_code__icontains=q))

    qs = qs.order_by('-created_at')

    part_groups, total_pt = _truck_part_groups()
    current_year = timezone.now().year

    context = {
        'listings': qs,
        'total_count': qs.count(),
        'truck_brands': TruckBrand.objects.all().order_by('name'),
        'truck_type_choices': Listing._meta.get_field('truck_type').choices,
        'fuel_types': FuelType.objects.all().order_by('name'),
        'condition_choices': Listing.CONDITION_CHOICES,
        'part_groups': part_groups,
        'part_types_total': total_pt,
        'country_choices': _truck_country_choices(),
        'us_states': Listing.US_STATE_CHOICES,
        'years': list(range(current_year + 1, 1949, -1)),
        'sel_part_types': [str(x) for x in part_types],
        'sel_conditions': conditions,
        'sel_truck_types': truck_types,
    }
    return render(request, 'listings/truck_parts_browse.html', context)


def truck_parts_advanced_search(request):
    from django.utils import timezone
    G = request.GET
    part_groups, total_pt = _truck_part_groups()
    current_year = timezone.now().year
    context = {
        'truck_brands': TruckBrand.objects.all().order_by('name'),
        'truck_type_choices': Listing._meta.get_field('truck_type').choices,
        'fuel_types': FuelType.objects.all().order_by('name'),
        'condition_choices': Listing.CONDITION_CHOICES,
        'part_groups': part_groups,
        'part_types_total': total_pt,
        'country_choices': _truck_country_choices(),
        'us_states': Listing.US_STATE_CHOICES,
        'years': list(range(current_year + 1, 1949, -1)),
        'sel_part_types': [v for v in G.getlist('part_types') if v],
        'sel_conditions': [v for v in G.getlist('condition') if v],
        'sel_truck_types': [v for v in G.getlist('truck_type') if v],
    }
    return render(request, 'listings/truck_parts_advanced.html', context)