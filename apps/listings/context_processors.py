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
from django.urls import NoReverseMatch, reverse
from django.utils.translation import gettext_lazy as _


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

# ═══════════════════════════════════════════════════════════════════
# RODYMO JUNGIKLIAI
#
# Vienoje vietoje surašyti laikini įjungta/išjungta jungikliai, kad
# funkciją būtų galima grąžinti pakeitus VIENĄ eilutę, o kodo trinti
# nereikėtų.
# ═══════════════════════════════════════════════════════════════════

# Trys miniatiūros kortelės nuotraukos apačioje. Išjungta, kol skelbimų
# su keliomis nuotraukomis mažai — kortelė švaresnė, o paspaudus vis tiek
# atsidaro skelbimas. Nuotraukų skaitiklis („6/8") lieka visada.
THUMBS_ENABLED = False

# Kompaktiška paieška antraštėje (kategorija · vieta · markė · 🔍).
# Išjungta 2026-08-27: antraštė tapo ankšta, o ta pati paieška yra
# puslapio viduje. Kodas lieka vietoje — įjungti = True.
ANTRASTES_PAIESKA = False


def rodymo_jungikliai(request):
    return {'THUMBS_ENABLED': THUMBS_ENABLED,
            'ANTRASTES_PAIESKA': ANTRASTES_PAIESKA}


# ═══════════════════════════════════════════════════════════════════
# ANTRINĖ NAVIGACIJA — vienas sąrašas juostai ir telefono meniu
#
# Punktą įjungti/išjungti = pakeisti PIRMĄ reikšmę (True/False). Kodo
# trinti nereikia — išjungtas punktas tiesiog nerenderinamas.
#
#   (rodyti, etiketė, maršruto vardas)
#
# `None` maršrutas reiškia, kad puslapio dar nėra — toks punktas gali
# būti tik išjungtas (kitaip nuoroda vestų į niekur).
# ═══════════════════════════════════════════════════════════════════

SEC_NAV_ITEMS = [
    (True,  _('Įmonės ir servisai'), 'imones:sarasas'),
    (False, _('Finansavimas'),      None),                     # puslapio dar nėra
    (False, _('Pasiūlymai verslui'), 'advertise'),
    (False, _('Autokatalogas'),     None),                     # puslapio dar nėra
    (False, _('Straipsniai'),       'tips_guides'),
    (True,  _('Pagalba'),           'help_center'),
    (True,  _('Apie mus'),          'about_us'),
    (True,  _('Partneriai'),         'partneriai'),
    (False, _('PRO pardavimas'),    'accounts:become_dealer'),
]


def antrine_navigacija(request):
    """Įjungti antrinės navigacijos punktai su adresais."""
    punktai = []
    for rodyti, etikete, marsrutas in SEC_NAV_ITEMS:
        if not rodyti or not marsrutas:
            continue
        try:
            punktai.append({'label': etikete, 'url': reverse(marsrutas)})
        except NoReverseMatch:          # maršruto nebėra — punkto nerodom
            continue
    return {'sec_nav': punktai}


# ═══════════════════════════════════════════════════════════════════
# FORMŲ KLAIDOS — error_fields / error_messages visuose šablonuose
#
# Kad šablone veiktų tai, ko tikimasi:
#     class="... {% if 'contact_terms' in error_fields %}field-invalid{% endif %}"
#
# View'as gali paduoti savo (formos_klaidos.kontekstas()) — tada laimi jo.
# Jei nepadavė, klaidos atpažįstamos iš `messages` pagal tekstą, todėl
# senų 28 formų perrašinėti nereikia.
#
# TINGIAI: `messages` iteravimas pažymi jas panaudotomis, o tai reikštų,
# kad ir sėkmės pranešimai dingtų nespėję pasirodyti. SimpleLazyObject
# užtikrina, kad į juos būtų kreipiamasi TIK tada, kai šablonas iš
# tikrųjų paprašo error_fields.
# ═══════════════════════════════════════════════════════════════════
def form_error_fields(request):
    from django.utils.functional import SimpleLazyObject
    from django.contrib.messages import get_messages
    from apps.listings import formos_klaidos

    def _surinkti():
        try:
            tekstai = [str(m) for m in get_messages(request)]
        except Exception:
            return {'error_fields': [], 'error_messages': {}}
        return formos_klaidos.kontekstas(tekstai)

    return {
        'error_fields': SimpleLazyObject(lambda: _surinkti()['error_fields']),
        'error_messages': SimpleLazyObject(lambda: _surinkti()['error_messages']),
        'form_errors': SimpleLazyObject(lambda: _surinkti()['form_errors']),
    }


# ═══════════════════════════════════════════════════════════════════
# ANTRAŠTĖS PAIEŠKA — kompaktiška juosta visuose puslapiuose
#
# Trys laukai (kategorija · vieta · markė) siunčia TUOS PAČIUS
# parametrus, kaip paieškos panelė ir detali paieška:
#     category=<slug> · city=<tekstas> (+country_filter) ·
#     brand=<id> arba q=<tekstas>
# Todėl rezultatų puslapyje jie jau būna pažymėti — antro filtrų
# rinkinio nėra.
#
# Kategorijų sąrašas — iš to paties šaltinio kaip visur:
# _get_visible_vehicle_types() + _kategorijos_vardas() (vardai iš
# paieškos panelių konfigūracijos, nes VehicleType.name dar angliškas).
# ═══════════════════════════════════════════════════════════════════

def antrastes_paieska(request):
    # Išjungus jungiklį nedarom nė vienos užklausos — juostos vis tiek
    # niekas nerenderins.
    if not ANTRASTES_PAIESKA:
        return {}

    from apps.listings.views import paieskos_kategorijos

    kategorijos = paieskos_kategorijos(request.user)

    get = request.GET
    kat = (get.get('category') or get.get('section') or '').strip()
    marke_id = (get.get('brand') or '').strip()
    marke_tekstas = (get.get('q') or '').strip()
    if marke_id and kat:
        from apps.listings.brand_api import brand_name
        marke_tekstas = brand_name(kat, marke_id) or marke_tekstas

    return {
        'hdr_kategorijos': kategorijos,
        'hdr_pradine': {
            'kategorija': kat,
            'vieta': (get.get('city') or '').strip(),
            'salis': (get.get('country_filter') or '').strip(),
            'markeId': marke_id,
            'marke': marke_tekstas,
        },
    }


# ═══════════════════════════════════════════════════════════════════
# ŠALIS — VIENA REIKŠMĖ VISAI SVETAINEI
#
# Šalis nėra atskiras kiekvieno puslapio filtras. Pakeitus ją bet kur
# (paieškos panelės juostoje, šoninėje juostoje, /imones/), ji galioja
# visur: procesorius kviečiamas kiekvienam puslapiui, o reikšmė imama
# iš vienos vietos — salies_juosta.pasirinkta().
#
# TINGIAI: kiekiai reikalauja GROUP BY per skelbimus, o dauguma
# puslapių šalies juostos net nerodo. SimpleLazyObject užtikrina, kad
# užklausa įvyktų tik tada, kai šablonas iš tikrųjų paprašo sąrašo.
# ═══════════════════════════════════════════════════════════════════
def salis(request):
    from django.utils.functional import SimpleLazyObject, lazy
    from apps.listings import salies_juosta

    saugykla = {}

    def _visas():
        # Penkios reikšmės, viena užklausa: be šito kešo kiekvienas
        # tingusis objektas perskaičiuotų sąrašą iš naujo.
        if not saugykla:
            saugykla.update(salies_juosta.kontekstas(request))
        return saugykla

    def _lauk(raktas):
        return SimpleLazyObject(lambda: _visas()[raktas])

    # Kiekis eina į {% blocktrans count %}, o daugiskaitos formulė daro
    # „n % 100" — SimpleLazyObject tokio veiksmo neturi ir šablonas
    # nulūžta. lazy(..., int) nusikopijuoja int metodus, tad veikia.
    kiekis = lazy(lambda: _visas()['salies_kiekis'], int)

    return {
        'salies_kodas': _lauk('salies_kodas'),
        'salies_zemas': _lauk('salies_zemas'),
        'salies_vardas': _lauk('salies_vardas'),
        'salies_kiekis': kiekis(),
        'salies_sarasas': _lauk('salies_sarasas'),
    }
