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
    # Raktai TRUMPI — tokie pat kaip parts_subs ir parts_config_subs
    # (anksčiau čia buvo subkategorijų slug'ai, todėl „Žemės ūkio, spec.
    # dalys" ir „Aksesuarai, Tuning" panelės likdavo tuščios).
    'parts': ('car', 'moto', 'truck', 'agri', 'accessories'),
    'wheels': ('tyre', 'rim'),
    'services': ('main', 'car-buying'),
}
SECTION_DEFAULT = {'rental': 'car-rental', 'trucks': 'main', 'construction': 'main',
                   'parts': 'car', 'wheels': 'tyre', 'services': 'main'}

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
    sekcija = resolve_section(tab, request.GET)
    return {'sp_tab': tab, 'sp_sekcija': sekcija,
            'sp_back': _panel_back(request, tab, sekcija)}


# Į grįžimo adresą nekeliauja puslapiavimas, rikiavimas ir vidiniai
# jungikliai — tik patys filtrai.
_BACK_DROP = ('category', 'subcategory', 'sidebar', 'page', 'sort',
              'search_id', 'issaugoti', 'section', 'sekcija')


def _panel_back(request, tab, sekcija):
    """Kur grįžtama iš telefono filtro reikšmės ekrano (/pasirinkti/).

    Turi vesti atgal Į PANELĘ, ne į rezultatus. Su `?category=` to
    padaryti negalima: listing_list mato kategoriją ir peradresuoja į
    rezultatų puslapį (?sidebar=1), todėl pasirinkus vieną reikšmę
    paieška startuodavo nespaudus „Skelbimai". Kategorija todėl
    perduodama `?section=` — jį panelė supranta, o rezultatų
    peradresavimo jis neįjungia.

    Jau pasirinkti filtrai lieka adrese: kitaip antras pasirinkimas
    ištrintų pirmą (adresas buvo pastovus, be esamų parametrų).
    """
    params = request.GET.copy()
    for key in _BACK_DROP:
        params.pop(key, None)
    params['section'] = tab
    if sekcija:
        params['sekcija'] = sekcija
    return '/?' + params.urlencode()


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
    # Filtrus taiko ta pati funkcija kaip /searches/ puslapyje — kitaip
    # skaitiklis ir sąrašas prasilenktų, o sąrašinės reikšmės (kelios
    # markės vienoje paieškoje) čia versdavo 500.
    from .views import _paieskos_qs, _sarasu, _viena

    new_ids = set()
    searches = SavedSearch.objects.filter(user=request.user)
    for search in searches:
        params = search.query_params or {}
        qs = _paieskos_qs(request, params)

        for raktas, laukas in (('fuel_type', 'fuel_type_id'),
                               ('transmission', 'transmission_id')):
            reiksmes = [v for v in _sarasu(params.get(raktas)) if str(v).isdigit()]
            if len(reiksmes) == 1:
                qs = qs.filter(**{laukas: reiksmes[0]})
            elif reiksmes:
                qs = qs.filter(**{laukas + '__in': reiksmes})

        if params.get('state_filter'):
            qs = qs.filter(country='US', state=_viena(params['state_filter']))
        elif params.get('country_filter'):
            qs = qs.filter(country=_viena(params['country_filter']))

        if search.last_viewed_at:
            qs = qs.filter(created_at__gt=search.last_viewed_at)
        new_ids.update(qs.values_list('id', flat=True))
    return {'new_searches_count': len(new_ids)}


def saved_listings_count(request):
    if not request.user.is_authenticated:
        return {'saved_listings_count': 0}
    from .models import SavedListing
    return {'saved_listings_count': SavedListing.objects.filter(user=request.user).count()}