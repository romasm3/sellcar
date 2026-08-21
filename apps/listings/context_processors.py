import re

_PHONE_UA = re.compile(
    r'iphone|ipod|android.+mobile|windows phone|blackberry|bb10|opera mini|'
    r'mobile.+firefox|silk|iemobile', re.I)
_TABLET_UA = re.compile(r'ipad|android(?!.*mobile)|tablet|kindle|playbook', re.I)


def device_kind(request):
    """Ar tai telefonas/planšetė — sprendžiama SERVERYJE.

    Rezultatų puslapyje šoninė filtrų juosta telefone neturi būti ne
    paslėpta, o visai neatiduota (taip elgiasi ir etalonas). Tam reikia
    žinoti įrenginį prieš renderinant, o CSS lūžio taškas čia nepadeda.
    Riba ta pati kaip visur — telefonas ir planšetė iki 1024 px.
    """
    ua = request.META.get('HTTP_USER_AGENT', '')
    phone = bool(_PHONE_UA.search(ua)) or bool(_TABLET_UA.search(ua))
    return {'is_phone': phone}


from apps.listings.search_config.panels import is_active


# Kategorijos, turinčios paieškos panelę. Vienas sąrašas: pagal jį
# sprendžiama ir kurią panelę renderinti, ir kur veda kategorijos nuoroda.
PANEL_SLUGS = {'cars', 'motorcycles', 'motogear', 'moto-tyres', 'quad-tyres',
               'trucks', 'wheels', 'boats', 'trailers', 'agriculture',
               'construction', 'loading-equipment', 'forestry', 'bicycles',
               'electronics', 'services', 'rental', 'camping-houses', 'parts'}


# Sekcijos kategorijos viduje. Etalone jos yra atskiri „…" sąrašo punktai,
# ne mygtukai panelėje, todėl ir pas mus pasirinkimas ateina adresu
# ?section=<kategorija>&sekcija=<sekcija>.
SECTIONS = {
    'rental': ('car-rental', 'limo-wedding-rental', 'motorcycle-rental',
               'minibus-touring-water-rental', 'heavy-trailer-rental'),
    'trucks': ('main', 'semi-trucks-tractors', 'buses',
               'vehicle-transporters', 'municipal-transport'),
    'construction': ('main', 'construction-attachments'),
    'parts': ('car', 'moto', 'truck', 'agri-special-parts', 'accessories-tuning'),
    'wheels': ('tyre', 'rim'),
}
SECTION_DEFAULT = {'rental': 'car-rental', 'trucks': 'main', 'construction': 'main',
                   'parts': 'car', 'wheels': 'tyre'}

# Senos nuorodos su ?subcategory=<id> turi veikti toliau.
LEGACY_SUBCAT_SECTION = {
    '294': 'limo-wedding-rental',
    '295': 'motorcycle-rental',
    '296': 'heavy-trailer-rental',
    '317': 'minibus-touring-water-rental',
    '198': 'buses',
}


def search_panel_tab(request):
    """Kuri kategorijos panelė renderinama — viena, ne visos 19.

    Šaltinis tas pats, kurį jau naudojo Alpine init(): ?section= arba
    ?category=. Nežinomas slug'as krinta į „cars", kad puslapis niekada
    neliktų be panelės.
    """
    tab = (request.GET.get('section') or request.GET.get('category') or '').strip()
    if tab == 'tires':
        tab = 'wheels'
    tab = tab if tab in PANEL_SLUGS else 'cars'

    # Sekcija kategorijos viduje (nuoma, sunkusis, statybinė). Pasirinkimas
    # ateina iš kategorijų sąrašo, ne iš mygtukų juostos panelėje, todėl
    # serveris renderina tik vienos sekcijos laukus.
    return {'sp_tab': tab, 'sp_sekcija': resolve_section(tab, request.GET)}


def resolve_section(tab, params):
    """Kuri sekcija kategorijos viduje — vienas skaičiavimas.

    Naudoja ir puslapio kontekstas, ir /panele/<kategorija>/ fragmentas,
    kad perjungus kategoriją gautum lygiai tą patį, ką ir perkrovus.
    """
    sek = (params.get('sekcija') or '').strip()
    if not sek:
        legacy = (params.get('subcategory') or '').strip()
        sek = LEGACY_SUBCAT_SECTION.get(legacy, legacy)
    if sek not in SECTIONS.get(tab, ()):
        sek = SECTION_DEFAULT.get(tab, '')
    return sek


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