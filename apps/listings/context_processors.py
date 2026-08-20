def saved_searches_count(request):
    if not request.user.is_authenticated:
        return {'new_searches_count': 0}
    from .models import SavedSearch, Listing
    # Skaitiklis rodo, KIEK NAUJŲ SKELBIMŲ atsirado pagal išsaugotas paieškas.
    # Skaičiuojami skirtingi skelbimai: dvi persidengiančios paieškos (o jų
    # pasitaiko — vartotojai išsaugo tą patį kelis kartus) to paties skelbimo
    # du kartus nebeskaičiuoja.
    new_ids = set()
    searches = SavedSearch.objects.filter(user=request.user)
    for search in searches:
        params = search.query_params
        qs = Listing.objects.filter(status='active')
        if params.get('category'):
            qs = qs.filter(vehicle_type__slug=params['category'])
        if params.get('brand'):
            qs = qs.filter(brand_id=params['brand'])
        if params.get('model'):
            qs = qs.filter(model_id=params['model'])
        if params.get('price_min'):
            qs = qs.filter(price__gte=params['price_min'])
        if params.get('price_max'):
            qs = qs.filter(price__lte=params['price_max'])
        if params.get('year_min'):
            qs = qs.filter(year__gte=params['year_min'])
        if params.get('year_max'):
            qs = qs.filter(year__lte=params['year_max'])
        if params.get('fuel_type'):
            qs = qs.filter(fuel_type_id=params['fuel_type'])
        if params.get('transmission'):
            qs = qs.filter(transmission_id=params['transmission'])
        if params.get('state_filter'):
            qs = qs.filter(country='US', state=params['state_filter'])
        elif params.get('country_filter'):
            qs = qs.filter(country=params['country_filter'])
        if search.last_viewed_at:
            qs = qs.filter(created_at__gt=search.last_viewed_at)
        new_ids.update(qs.values_list('id', flat=True))
    return {'new_searches_count': len(new_ids)}


def saved_listings_count(request):
    if not request.user.is_authenticated:
        return {'saved_listings_count': 0}
    from .models import SavedListing
    return {'saved_listings_count': SavedListing.objects.filter(user=request.user).count()}