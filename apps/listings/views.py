import json
from django.utils.translation import gettext_lazy as _
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_POST
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from django.db.models import Count, Q, Sum, Avg
from django.db import transaction
from decimal import Decimal
from django.db import transaction
from decimal import Decimal
from django.utils import timezone
from .constants import can_create_listing
from .image_validation import ImageValidationError, split_valid_images, validate_images
from .search_panel import (
    COUNT_KEY_TO_SUB, parts_count_qs, parts_panel_context,
    apply_trailer_filters, trailers_panel_context,
)
from .search_config import panels as panel_config
from .forms import (
    Step1BasicInfoForm,
    Step2MediaForm,
    Step3VehicleDataForm,
    Step4EquipmentForm,
    Step5PriceForm,
    Step6DescriptionForm,
    Step7ContactForm,
)
from .models import (
    Listing,
    ListingImage,
    ListingView,
    ListingImpression,
    SalesRecord,
    Model,
    SubModel,
    SubCategory,
    Equipment,
    ListingEquipment,
    VehicleType,
    Brand,
    FuelType,
    Transmission,
    SavedListing,
)
from datetime import date, timedelta, datetime

NEW_LISTING_DAYS = 3
RENEW_RATE_LIMIT_HOURS = 1

# ═══════════════════════════════════════════════════════════
# EQUIPMENT CATEGORIES — Cars-only filter (no truck_*, no gear)
# ═══════════════════════════════════════════════════════════
CARS_EQUIPMENT_CATEGORIES = [
    ('interior', _('Interior')),
    ('exterior', _('Exterior')),
    ('electronics', _('Electronics')),
    ('safety', _('Safety & Security')),
    ('audio_video', _('Audio, Video & Connectivity')),
    ('other', _('Other Features')),
    ('electric', _('Electric vehicle features')),
]

CATEGORY_VEHICLE_TYPES = {
    'cars': ['Car', 'Automobile', 'Automobilis', 'Lengvasis automobilis'],
    'vans': ['Van', 'Bus', 'Minibus', 'Mikroautobusas', 'Autobusas'],
    'motorcycles': ['Motorcycle', 'Motorbike', 'Motociklas'],
    'trucks': ['Truck', 'Lorry', 'Sunkvezimis', 'Krovininis'],
    'parts': ['Parts', 'Dalys', 'Auto parts'],
    'tires': ['Tires', 'Wheels', 'Padangos', 'Ratlankiai'],
    'boats': ['Boat', 'Yacht', 'Valtis', 'Jachta', 'Vandens transportas'],
    'trailers': ['Trailer', 'Priekaba', 'Puspriekabe'],
    'construction': ['Construction', 'Excavator', 'Statybos technika', 'Ekskavatorius'],
    'agriculture': ['Tractor', 'Agricultural', 'Traktorius', 'Zemes ukio technika'],
    'bicycles': ['Bicycle', 'Scooter', 'Dviratis', 'Paspirtukas'],
    'services': ['Service', 'Paslauga', 'Paslaugos'],
    'rental': ['Rental', 'Nuoma', 'Transporto nuoma'],
}

CATEGORY_ICONS = {
    'cars': '🚗', 'vans': '🚐', 'motorcycles': '🏍️', 'trucks': '🚛',
    'parts': '⚙️', 'tires': '🛞', 'boats': '🚤', 'trailers': '🚚',
    'construction': '🏗️', 'agriculture': '🚜', 'bicycles': '🚲',
    'services': '🔧', 'rental': '🔑', 'planes': '✈️', 'planes-parts': '🔩',
    'camping-houses': '🏕️',
}

CITY_COORDINATES = {
    'vilnius': (54.6872, 25.2797), 'kaunas': (54.8985, 23.9036),
    'klaipeda': (55.7033, 21.1443), 'siauliai': (55.9349, 23.3137),
    'panevezys': (55.7348, 24.3575), 'alytus': (54.3963, 24.0459),
    'marijampole': (54.5594, 23.3500), 'mazeikiai': (56.3167, 22.3333),
    'jonava': (55.0833, 24.2833), 'utena': (55.5000, 25.6000),
    'riga': (56.9496, 24.1052), 'tallinn': (59.4370, 24.7536),
    'warsaw': (52.2297, 21.0122), 'berlin': (52.5200, 13.4050),
    'amsterdam': (52.3676, 4.9041), 'paris': (48.8566, 2.3522),
    'rome': (41.9028, 12.4964), 'madrid': (40.4168, -3.7038),
    'london': (51.5074, -0.1278),
}

COUNTRY_COORDINATES = {
    'US': (37.0902, -95.7129), 'LT': (55.1694, 23.8813),
    'LV': (56.8796, 24.6032), 'EE': (58.5953, 25.0136),
    'PL': (51.9194, 19.1451), 'DE': (51.1657, 10.4515),
    'NL': (52.1326, 5.2913), 'BE': (50.5039, 4.4699),
    'FR': (46.2276, 2.2137), 'IT': (41.8719, 12.5674),
    'ES': (40.4637, -3.7492), 'AT': (47.5162, 14.5501),
    'CZ': (49.8175, 15.4730), 'SK': (48.6690, 19.6990),
    'HU': (47.1625, 19.5033), 'RO': (45.9432, 24.9668),
    'BG': (42.7339, 25.4858), 'SE': (60.1282, 18.6435),
    'DK': (56.2639, 9.5018), 'FI': (61.9241, 25.7482),
    'NO': (60.4720, 8.4689), 'GB': (55.3781, -3.4360),
    'IE': (53.1424, -7.6921), 'CH': (46.8182, 8.2275),
}

CARS_DRAFT_SESSION_KEY = 'active_cars_draft_id'

# ═══════════════════════════════════════════════════════════
# PUBLIC CATEGORIES — visiem matomos modal'e
# Kai kategorija ready — pridėk slug čia, taps live visiem
# ═══════════════════════════════════════════════════════════
PUBLIC_VEHICLE_TYPE_SLUGS = {
    'cars',
    'motorcycles',
    'tires',
    'parts',
    'agriculture',
    'vans',
    'trucks',
    'trailers',
    'rental',
    'electronics',
    'services',
    'car-buying',
    'loading-equipment',
    'construction',
    'forestry',
    'camping-houses',
    'boats',
    'bicycles',
    # Etaloniniame medyje šitų nėra, bet paliktos matomos su „Netrukus“ žyma.
    'planes',
    'planes-parts',
}

# ═══════════════════════════════════════════════════════════
# KURIOS KATEGORIJOS TURI VEIKIANČIĄ CREATE FORMĄ
# Publikuota (matoma) ≠ įgyvendinta (galima pildyti). Kategorijos, kurių
# čia nėra, pikeryje rodomos pilkos su „Netrukus“ ir nepaspaudžiamos —
# anksčiau jos vesdavo į aklavietę (7 žingsnių srautas išjungtas,
# žr. listing_create), palikdamos DB tuščią „Untitled draft“.
# Parašius naują formą — įrašyk slug čia.
# ═══════════════════════════════════════════════════════════
IMPLEMENTED_VEHICLE_TYPE_SLUGS = {
    'cars',
    'camping-houses',
    'vans',
    'rental',
    'services',
    'electronics',
    'car-buying',
    'bicycles',
    'forestry',
    'loading-equipment',
    'construction',
    'agriculture',
    'motorcycles',
    'tires',
    'parts',
    'trucks',
    'trailers',
    'boats',
}

# Subkategorijos ĮGYVENDINTOSE kategorijose, kurios formos vis dar neturi.
# Pikeryje tokios rodomos pilkos su „Netrukus“, kad vartotojas neatsidurtų
# 404 puslapyje ar aklavietėje. Šiuo metu tuščias: „Automobilis dalimis“
# atidarytas visiems (buvo staff_only), o „Motociklas dalimis“ gavo savo
# formą (moto_for_parts_views).
UNIMPLEMENTED_SUBCATEGORY_SLUGS = set()

# Subkategorijos, kurias aptarnauja bendra „atskiros dalies“ forma
# (parts_listing_create). Ji sukasi apie PartCategory medį, ne apie
# SubCategory, todėl viena forma tinka visoms trims.
PARTS_GENERIC_FORM_SLUGS = {
    'single-part-or-kit',
    'single-truck-part',
    'agri-special-parts',
    'accessories-tuning',
}

# ═══════════════════════════════════════════════════════════
# PIKERYJE NERODOMOS KATEGORIJOS (net staff'ui)
# Nei publikavimo, nei įgyvendinimo klausimas — šitos tiesiog nėra
# viršutinio lygio įrašai etaloniniame medyje:
#   • tractor-units / car-carriers / municipal — sugerti į „Sunkusis
#     transportas“ subkategorijomis (0058), bet patys VT palikti DB
#   • planes / planes-parts — etalone jų nėra
# DB eilutės NETRINAMOS: skelbimai, naršymas ir admin toliau veikia.
# ═══════════════════════════════════════════════════════════
PICKER_HIDDEN_VEHICLE_TYPE_SLUGS = {
    'tractor-units',
    'car-carriers',
    'municipal',
    'planes',
    'planes-parts',
}

# Kategorijos BE subkategorijų — pikeris veda tiesiai į šią formą.
# Kategorijos SU subkategorijomis čia nefigūruoja: jos pirma atidaro
# subkategorijų sąrašą, o nukreipimą daro listing_create POST šaka.
CREATE_URL_BY_VEHICLE_TYPE = {
    'cars':     '/create/cars/quick/',
    'loading-equipment': '/create/loading-equipment/?new=1',
    'forestry': '/create/forestry/?new=1',
    'camping-houses': '/create/camping-houses/?new=1',
    'services': '/create/services/?new=1',
    'electronics': '/create/electronics/?new=1',
    'bicycles': '/create/bicycles/?new=1',
    # Mikroautobusai savos formos NETURI — kaip ir etalone. Pikerio punktas
    # atidaro nukreipimo puslapį, iš kurio einama į automobilių arba
    # sunkiojo transporto formą (žr. minibus_category_choice).
    'vans': '/create/minibuses/',
    # Autogide „Automobilių supirkimas" nėra atskira kategorija, o paslaugos
    # tipas. Pikerio eilutę paliekam (vartotojai jos ieško), bet vedam į
    # paslaugų formą su iš anksto parinktu tipu — skelbimas atsiduria ten,
    # kur jį ras paieška.
    'car-buying': '/create/services/?new=1&type=car_buying',
    'boats':    '/create/boats/?new=1',
    'trailers': '/create/trailers/?new=1',
}

# Nuomos subkategorija → kuri iš keturių formų ją aptarnauja.
# Šaltinis — rental_views.SUB_TO_FORM (čia pakartota, kad views.py
# neimportuotų rental_views ir neatsirastų ciklinis importas).
RENTAL_SUB_TO_FORM = {
    'car-rental': 'car',
    'limo-wedding-rental': 'car',
    'motorcycle-rental': 'moto',
    'minibus-touring-water-rental': 'minibus',
    'heavy-trailer-rental': 'heavy',
}

# ═══════════════════════════════════════════════════════════
# PIKERIO SUBKATEGORIJŲ MEDIS (etaloninis sąrašas ir tvarka)
# Kategorijos, kurių čia nėra, pikeryje rodomos BE subkategorijų.
# DB eilutės neliečiamos — jos tebenaudojamos naršyme ir formų viduje
# (pvz. boats 8 potipiai), tik pikeryje nerodomos.
# ═══════════════════════════════════════════════════════════
PICKER_SUBCATEGORY_SLUGS = {
    # ─── Su subkategorijomis ───
    'motorcycles': ['motorcycles', 'moto-gear'],
    'tires':       ['tyres', 'rims'],
    'parts':       ['car-parts', 'moto-parts', 'truck-parts',
                    'agri-special-parts', 'accessories-tuning'],
    'trucks':      ['trucks', 'semi-trucks-tractors', 'vehicle-transporters',
                    'buses', 'municipal-transport'],
    'rental':      ['car-rental', 'limo-wedding-rental', 'motorcycle-rental',
                    'minibus-touring-water-rental', 'heavy-trailer-rental'],
    'construction': ['construction-machinery', 'construction-attachments'],

    # ─── Etalone be subkategorijų, nors DB jų turi ───
    # Eilutės DB paliekamos (naršymas, formų vidus), tik pikeryje neberodomos.
    'vans':         [],
    'agriculture':  [],
    'trailers':     [],
    'boats':        [],
    'bicycles':     [],
    'services':     [],
    'planes':       [],
    'planes-parts': [],
}

# ═══ MOTO GEAR slugs (3rd level subcategories) — used by listing_create ═══
MOTO_GEAR_SLUGS = {
    'helmets', 'protective-gear', 'boots', 'pants',
    'suits', 'bags', 'gloves', 'jackets', 'other-gear',
}

# Parent ("Apranga, šalmai, aksesuarai") — no gear type preselected.
MOTO_GEAR_PARENT_SLUG = 'moto-gear'

# ═══ CONSTRUCTION subcategory slugs — used by listing_create ═══
# Priedai turi savo formą; technikos tipai — bendrą.
CONSTRUCTION_ATTACHMENT_SUB = 'construction-attachments'
CONSTRUCTION_SUBCATEGORY_SLUGS = {
    'bulldozers', 'compactors', 'concrete-mixers', 'cranes', 'excavators',
    'forklifts', 'loaders', 'other-construction', 'construction-machinery',
}

# ═══ AGRICULTURE subcategory slugs — used by listing_create ═══
AGRICULTURE_SUBCATEGORY_SLUGS = {
    'tractors', 'combines', 'sprayers', 'ploughs', 'cultivators',
    'balers', 'forestry-machines', 'other-agricultural',
}

# ═══ TRAILERS subcategory slugs — used by listing_create ═══
# Gyvena čia, o ne trailers_views.py, nes trailers_views importuoja iš views.py
# (ciklinis importas). trailers_views persiima šitą aibę.
TRAILERS_SUBCATEGORY_SLUGS = {
    'semi-trailers', 'car-trailers', 'boat-trailers', 'curtainsider-trailers',
    'tipper-trailers', 'refrigerator-trailers', 'flatbed-trailers',
    'caravans', 'other-trailers',
}


def get_coordinates_for_location(city, country_code):
    if city:
        city_lower = city.lower().strip()
        if city_lower in CITY_COORDINATES:
            return CITY_COORDINATES[city_lower]
    if country_code and country_code in COUNTRY_COORDINATES:
        return COUNTRY_COORDINATES[country_code]
    return (54.8985, 23.9036)


def _int_or_none(value):
    if value in (None, ''):
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def _float_or_none(value):
    if value in (None, ''):
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def _get_visible_vehicle_types(user):
    """Staff mato visas kategorijas, kiti — tik PUBLIC_VEHICLE_TYPE_SLUGS."""
    qs = VehicleType.objects.all().order_by('order')
    if user.is_authenticated and user.is_staff:
        return qs
    return qs.filter(slug__in=PUBLIC_VEHICLE_TYPE_SLUGS)


def _picker_subcategory_slugs(vt_slug):
    """Pikeryje rodomos subkategorijos šitam VT (arba None = rodyti visas)."""
    return PICKER_SUBCATEGORY_SLUGS.get(vt_slug)


def _get_picker_vehicle_types(user):
    """VT sąrašas create pikeriui, papildytas dviem vėliavėlėmis.

    is_implemented   — ar yra veikianti create forma (jei ne, rodoma pilka
                       su „Netrukus“ ir nepaspaudžiama)
    has_subs         — ar atidaryti subkategorijų sąrašą, ar vesti tiesiai
                       į formą. Anksčiau tai buvo hardcodinta pagal slug
                       ('cars'/'boats'), dabar išvedama iš medžio.
    """
    vts = list(_get_visible_vehicle_types(user))
    sub_counts = dict(
        SubCategory.objects.filter(parent__isnull=True)
        .values_list('vehicle_type_id')
        .annotate(n=Count('id'))
        .values_list('vehicle_type_id', 'n')
    )
    vts = [v for v in vts if v.slug not in PICKER_HIDDEN_VEHICLE_TYPE_SLUGS]
    for vt in vts:
        vt.is_implemented = vt.slug in IMPLEMENTED_VEHICLE_TYPE_SLUGS
        picker_subs = _picker_subcategory_slugs(vt.slug)
        if picker_subs is not None:
            vt.has_subs = bool(picker_subs)
        else:
            vt.has_subs = bool(sub_counts.get(vt.pk))
        vt.create_url = CREATE_URL_BY_VEHICLE_TYPE.get(vt.slug, '')
    return vts


def _route_category_pick(request, vehicle_type_id, subcategory_id, subcategory_slug):
    """Kategorijos pasirinkimas → redirect į tinkamą create formą.

    Vienas maršrutizavimo šaltinis: naudoja ir listing_create POST šaka,
    ir be-JS GET dispatcheris (?pick_vt= / ?pick_sub=). Grąžina redirect
    arba None, jei nieko tinkamo nerasta.
    """
    vt_slug = (
        VehicleType.objects.filter(pk=vehicle_type_id)
        .values_list('slug', flat=True).first()
    )

    # ═══ „NETRUKUS“ GUARD ═══
    # Pikeris tokių nebeleidžia paspausti, bet užklausa gali ateiti ir
    # tiesiogiai. Be šito guard'o būtų sukuriamas tuščias draft'as ir
    # vartotojas grąžinamas į pikerį — taip DB atsirado „Untitled draft“.
    if vt_slug not in IMPLEMENTED_VEHICLE_TYPE_SLUGS:
        messages.info(request, _('Ši kategorija dar ruošiama.'))
        return redirect('/create/?step=1')
    if subcategory_slug in UNIMPLEMENTED_SUBCATEGORY_SLUGS:
        messages.info(request, _('Ši kategorija dar ruošiama.'))
        return redirect('/create/?step=1')

    # ═══ LISTING LIMIT GUARD ═══
    can_create, active_count, limit = can_create_listing(request.user)
    if not can_create:
        messages.error(
            request,
            f'You have reached your active listings limit ({active_count}/{limit}). '
            f'Upgrade your account to create more listings.',
        )
        return redirect('listing_upgrade')

    # ═══ Kategorija BE subkategorijų → tiesiai į savo formą ═══
    # cars / boats / trailers. Be šito jos nukristų į išjungtą 7 žingsnių
    # srautą (/create/?step=2), t. y. atgal į pikerį.
    if not subcategory_slug and vt_slug in CREATE_URL_BY_VEHICLE_TYPE:
        return redirect(CREATE_URL_BY_VEHICLE_TYPE[vt_slug])

    # ═══ TRANSPORTO NUOMA → keturios formos penkioms subkategorijoms ═══
    # Automobilių ir limuzinų nuoma dalinasi viena forma; subkategorija
    # ten renkama formos lauke, URL ?sub= tik preselekcijai.
    if vt_slug == 'rental':
        _form = RENTAL_SUB_TO_FORM.get(subcategory_slug or 'car-rental', 'car')
        _url = f'/create/rental/{_form}/?new=1'
        if _form == 'car' and subcategory_slug:
            _url += f'&sub={subcategory_slug}'
        return redirect(_url)

    if subcategory_slug == 'motorcycles':
        return redirect('/create/motorcycle/?new=1')

    if subcategory_slug in MOTO_GEAR_SLUGS:
        return redirect(f'/create/motogear/?subcategory={subcategory_slug}&new=1')

    # Parent picked directly (no 3rd level chosen) — open the gear
    # form anyway, with the type select left empty.
    if subcategory_slug == MOTO_GEAR_PARENT_SLUG:
        return redirect('/create/motogear/?new=1')

    # ═══ TYRES / RIMS → atskiri wheels create puslapiai ═══
    if subcategory_slug == 'rims':
        return redirect('/create/rims/')
    if 'tyre' in subcategory_slug or 'tire' in subcategory_slug:
        return redirect('/create/tyres/')

    # ═══ SUNKUSIS TRANSPORTAS → trucks forma ═══
    # Subkategorija perduodama toliau (Vilkikai / Autotraukiniai / Autobusai /
    # Komunalinis) — trucks_views ją įrašo, o ne hardcodina į 'trucks'.
    if vt_slug == 'trucks' and subcategory_slug:
        return redirect(f'/create/trucks/?new=1&subcategory={subcategory_slug}')

    # ═══ DALYS → viena bendra „atskiros dalies“ forma ═══
    # parts_listing_create sukasi apie PartCategory medį, todėl ta pati forma
    # tinka ir „Žemės ūkio, spec. dalims“, ir „Aksesuarams, Tuning“ — trūko
    # tik nukreipimo. ?for= išsaugo, KURI subkategorija buvo pasirinkta.
    if subcategory_slug in PARTS_GENERIC_FORM_SLUGS:
        return redirect(f"{reverse('parts_category_select')}?for={subcategory_slug}")
    if subcategory_slug == 'single-moto-part':
        return redirect('moto_part_create')
    if subcategory_slug == 'whole-car-for-parts':
        return redirect('/create/car-for-parts/?new=1')
    if subcategory_slug == 'whole-moto-for-parts':
        return redirect('/create/moto-for-parts/?new=1')
    if subcategory_slug == 'whole-truck-for-parts':
        return redirect('/create/truck-for-parts/?new=1')

    # ═══ STATYBINĖ TECHNIKA → dvi skirtingos formos ═══
    if subcategory_slug == CONSTRUCTION_ATTACHMENT_SUB:
        return redirect('/create/construction/attachment/?new=1')
    if subcategory_slug in CONSTRUCTION_SUBCATEGORY_SLUGS:
        return redirect(
            f'/create/construction/?new=1&subcategory={subcategory_slug}'
        )

    # ═══ ŽEMĖS ŪKIO TECHNIKA → atskira forma ═══
    # Subkategorija perduodama tik Tipo preselekcijai; įrašant ji
    # persiskaičiuoja iš formos lauko.
    if subcategory_slug in AGRICULTURE_SUBCATEGORY_SLUGS:
        return redirect(
            f'/create/agriculture/?new=1&subcategory={subcategory_slug}'
        )

    # ═══ TRAILERS → atskira priekabų forma ═══
    # Subkategorija perduodama toliau — forma ją naudoja Paskirties
    # preselekcijai ir persiskaičiuoja išsaugant.
    if subcategory_slug in TRAILERS_SUBCATEGORY_SLUGS:
        return redirect(f'/create/trailers/?new=1&subcategory={subcategory_slug}')

    # ═══ ATSARGINĖ ŠAKA ═══
    # Anksčiau čia buvo sukuriamas cars draft'as ir vartotojas siunčiamas
    # į /create/?step=2 — išjungtą 7 žingsnių srautą, kuris iškart grąžina
    # atgal į pikerį. Rezultatas: tuščias „Untitled draft" DB ir niekur
    # nevedantis paspaudimas. Dabar eilutės nekuriam.
    #
    # Kiekviena įgyvendinta kategorija turi savo šaką aukščiau arba įrašą
    # CREATE_URL_BY_VEHICLE_TYPE; jei atsidūrėm čia — formos tam VT dar nėra.
    messages.info(request, _('Ši kategorija dar ruošiama.'))
    return redirect('/create/?step=1')


@login_required
def minibus_category_choice(request):
    """/create/minibuses/ — nukreipimo puslapis, kaip autogidas.

    Mikroautobusai nėra atskira kategorija nei etalono pikeryje, nei jo
    paieškoje: lengvieji (iki 3,5 t, B kat.) dedami į automobilius,
    sunkesni — į sunkvežimius, autobusai — į autobusus. Savos formos
    nekuriam, tik parodom tuos pačius tris kelius.
    """
    return render(request, 'listings/minibus_choice.html', {
        'options': [
            {
                'title': _('Mikroautobusas, kuriam vairuoti pakanka B kategorijos'),
                'hint': _('iki 3,5 t — keleivinis arba krovininis'),
                'target': _('Automobiliai'),
                'url': '/create/cars/quick/',
                'icon': 'cars',
            },
            {
                'title': _('Mikroautobusas, kuriam nepakanka B kategorijos'),
                'hint': _('virš 3,5 t'),
                'target': _('Sunkusis transportas → Sunkvežimiai'),
                'url': '/create/trucks/?new=1&subcategory=trucks',
                'icon': 'trucks',
            },
            {
                'title': _('Autobusas'),
                'hint': _('keleiviams vežti'),
                'target': _('Sunkusis transportas → Autobusai'),
                'url': '/create/trucks/?new=1&subcategory=buses',
                'icon': 'vans',
            },
        ],
    })


def _build_picker_tree(user):
    """Visas pikerio medis vienu kartu — root + 2 ir 3 lygio panelės.

    Anksčiau subkategorijos buvo traukiamos dviem AJAX užklausomis, todėl
    pikeris be JS neveikė. Dabar viskas atiduodama iš karto: JS tik
    perjungia paneles, o be JS naršoma ?vt= / ?sub= nuorodomis.
    """
    vts = _get_picker_vehicle_types(user)

    subs_by_vt = {}
    for s in (SubCategory.objects
              .filter(parent__isnull=True, vehicle_type__in=vts)
              .order_by('order', 'name')):
        subs_by_vt.setdefault(s.vehicle_type_id, []).append(s)

    children_by_parent = {}
    for c in (SubCategory.objects
              .filter(parent__isnull=False, vehicle_type__in=vts)
              .order_by('order', 'name')):
        children_by_parent.setdefault(c.parent_id, []).append(c)

    def decorate(sub):
        sub.is_implemented = sub.slug not in UNIMPLEMENTED_SUBCATEGORY_SLUGS
        sub.kids = children_by_parent.get(sub.pk, [])
        for k in sub.kids:
            k.is_implemented = k.slug not in UNIMPLEMENTED_SUBCATEGORY_SLUGS
            k.kids = []
        return sub

    tree = []
    for vt in vts:
        allowed = _picker_subcategory_slugs(vt.slug)
        rows = subs_by_vt.get(vt.pk, [])
        if allowed is not None:
            by_slug = {s.slug: s for s in rows}
            rows = [by_slug[sl] for sl in allowed if sl in by_slug]
        vt.subs = [decorate(s) for s in rows]
        vt.has_subs = bool(vt.subs)
        tree.append(vt)
    return tree


    # ⋯ DAUGIAU flyout — pilnas kategorijų sąrašas.
    # Formatas: (category_slug, pavadinimas, emoji, subcategory_id|None)
    MORE_ITEMS_SPEC = [
        ('agriculture',       'Žemės ūkio technika, padargai',        '🚜', None),
        ('trucks',            'Sunkvežimiai',                         '🚚', None),
        ('tractor-units',     'Vilkikai',                             '🚛', None),
        ('car-carriers',      'Autotraukiniai, autovežiai',           '🛻', None),
        ('trucks',            'Autobusai',                            '🚌', 198),
        ('municipal',         'Komunalinio ūkio transportas',         '🧹', None),
        ('trailers',          'Priekabos / Puspriekabės',             '🛞', None),
        ('rental',            'Automobilių nuoma',                    '🔑', None),
        ('rental',            'Limuzinų, vestuvių transporto nuoma',  '🥂', 294),
        ('rental',            'Motociklų nuoma',                      '🏍', 295),
        ('rental',            'Mikroautobusų, turistinio, vandens tr. nuoma', '🚐', 317),
        ('rental',            'Sunkiojo transporto, priekabų nuoma',  '🚛', 296),
        ('electronics',       'Video, audio, navigacijos',            '📻', None),
        ('services',          'Paslaugos',                            '🔧', None),
        ('car-buying',        'Automobilių supirkimas',               '💰', None),
        ('loading-equipment', 'Krovimo ir sandėliavimo technika',     '📦', None),
        ('construction',      'Statybinė technika',                   '🏗', None),
        ('construction',      'Statybinės technikos priedai',         '⚙', 297),
        ('forestry',          'Miško ūkio technika',                  '🌲', None),
        ('camping-houses',    'Turistiniai nameliai',                 '🏕', None),
        ('boats',             'Vandens transportas',                  '⛵', None),
        ('bicycles',          'El. paspirtukai, riedžiai, dviračiai', '🛴', None),
    ]
    
    
    def build_more_items(counts=None):
        counts = counts or {}
        items = []
        for slug, name, icon, sub_id in MORE_ITEMS_SPEC:
            items.append({
                'slug':   slug,
                'name':   name,
                'icon':   icon,
                'sub_id': sub_id,
                'is_sub': sub_id is not None,
                'count':  counts.get((slug, sub_id)),
            })
        return items


# ═══════════════════════════════════════════════════════════
# GROUPED EQUIPMENT — for listing_detail autogidas-style display
# ═══════════════════════════════════════════════════════════

EQUIPMENT_CATEGORY_LABELS = {
    'interior': 'Interior',
    'exterior': 'Exterior',
    'electronics': 'Electronics',
    'safety': 'Safety & Security',
    'audio_video': 'Audio, Video & Connectivity',
    'other': 'Other',
    'electric': 'Electric vehicle features',
    'gear': 'Gear',
    'truck_cabin': 'Cabin',
    'truck_body': 'Body',
    'truck_electronics': 'Electronics',
    'truck_safety': 'Safety',
    'truck_audio_video': 'Audio/Video',
    'truck_other': 'Other',
    'trailer_body': 'Kėbulas ir įranga',
    'trailer_chassis': 'Važiuoklė',
    'trailer_safety': 'Sauga',
    'trailer_other': 'Kita',
    'agri_drivetrain': 'Pavaros ir važiuoklė',
    'agri_mount': 'Prikabinimas',
    'agri_other': 'Kita',
    'load_cabin': 'Kabina ir apsauga',
    'load_hydraulics': 'Hidraulika ir mechanizmai',
    'load_platform': 'Platforma ir atramos',
    'load_surface': 'Važiuoklė ir paviršius',
    'camp_electronics': 'Elektronika ir multimedija',
    'camp_assist': 'Vairavimo pagalba',
    'camp_safety': 'Sauga',
    'camp_interior': 'Interjeras ir buitis',
    'camp_other': 'Kita įranga',
    'rent_terms': 'Nuomos sąlygos',
    'svc_repair': 'Remontas ir diagnostika',
    'svc_other': 'Kita',
    'elec_features': 'Ypatumai',
    'bike_features': 'Ypatumai',
}

EQUIPMENT_CATEGORY_ORDER = [
    'interior', 'exterior', 'electronics', 'safety',
    'audio_video', 'other', 'electric',
    'truck_cabin', 'truck_body', 'truck_electronics',
    'truck_safety', 'truck_audio_video', 'truck_other',
    'trailer_body', 'trailer_chassis', 'trailer_safety', 'trailer_other',
    'agri_drivetrain', 'agri_mount', 'agri_other',
    'load_cabin', 'load_hydraulics', 'load_platform', 'load_surface',
    'camp_electronics', 'camp_assist', 'camp_safety', 'camp_interior', 'camp_other',
    'rent_terms',
    'svc_repair', 'svc_other',
    'elec_features',
    'bike_features',
    'gear',
]


def _build_grouped_equipment(listing):
    """Returns equipment grouped by category for autogidas-style detail page."""
    grouped = []
    items_by_cat = {}
    for item in listing.equipment_items.select_related('equipment').all():
        cat = item.equipment.category
        items_by_cat.setdefault(cat, []).append(item.equipment.name)

    for cat in EQUIPMENT_CATEGORY_ORDER:
        if cat in items_by_cat:
            grouped.append({
                'key': cat,
                'label': EQUIPMENT_CATEGORY_LABELS.get(cat, cat.title()),
                'items': sorted(items_by_cat[cat]),
            })
    return grouped


# ═══════════════════════════════════════════════════════════
# GROUPED EQUIPMENT — for listing_detail autogidas-style display
# ═══════════════════════════════════════════════════════════

EQUIPMENT_CATEGORY_LABELS = {
    'interior': 'Interior',
    'exterior': 'Exterior',
    'electronics': 'Electronics',
    'safety': 'Safety & Security',
    'audio_video': 'Audio, Video & Connectivity',
    'other': 'Other',
    'electric': 'Electric vehicle features',
    'gear': 'Gear',
    'truck_cabin': 'Cabin',
    'truck_body': 'Body',
    'truck_electronics': 'Electronics',
    'truck_safety': 'Safety',
    'truck_audio_video': 'Audio/Video',
    'truck_other': 'Other',
    'trailer_body': 'Kėbulas ir įranga',
    'trailer_chassis': 'Važiuoklė',
    'trailer_safety': 'Sauga',
    'trailer_other': 'Kita',
    'agri_drivetrain': 'Pavaros ir važiuoklė',
    'agri_mount': 'Prikabinimas',
    'agri_other': 'Kita',
    'load_cabin': 'Kabina ir apsauga',
    'load_hydraulics': 'Hidraulika ir mechanizmai',
    'load_platform': 'Platforma ir atramos',
    'load_surface': 'Važiuoklė ir paviršius',
    'camp_electronics': 'Elektronika ir multimedija',
    'camp_assist': 'Vairavimo pagalba',
    'camp_safety': 'Sauga',
    'camp_interior': 'Interjeras ir buitis',
    'camp_other': 'Kita įranga',
    'rent_terms': 'Nuomos sąlygos',
    'svc_repair': 'Remontas ir diagnostika',
    'svc_other': 'Kita',
    'elec_features': 'Ypatumai',
    'bike_features': 'Ypatumai',
}

EQUIPMENT_CATEGORY_ORDER = [
    'interior', 'exterior', 'electronics', 'safety',
    'audio_video', 'other', 'electric',
    'truck_cabin', 'truck_body', 'truck_electronics',
    'truck_safety', 'truck_audio_video', 'truck_other',
    'trailer_body', 'trailer_chassis', 'trailer_safety', 'trailer_other',
    'agri_drivetrain', 'agri_mount', 'agri_other',
    'load_cabin', 'load_hydraulics', 'load_platform', 'load_surface',
    'camp_electronics', 'camp_assist', 'camp_safety', 'camp_interior', 'camp_other',
    'rent_terms',
    'svc_repair', 'svc_other',
    'elec_features',
    'bike_features',
    'gear',
]


def _build_grouped_equipment(listing):
    """Returns equipment grouped by category for autogidas-style detail page."""
    grouped = []
    items_by_cat = {}
    for item in listing.equipment_items.select_related('equipment').all():
        cat = item.equipment.category
        items_by_cat.setdefault(cat, []).append(item.equipment.name)

    for cat in EQUIPMENT_CATEGORY_ORDER:
        if cat in items_by_cat:
            grouped.append({
                'key': cat,
                'label': EQUIPMENT_CATEGORY_LABELS.get(cat, cat.title()),
                'items': sorted(items_by_cat[cat]),
            })
    return grouped


# ═══════════════════════════════════════════════════════════
# EMAIL HELPERS
# ═══════════════════════════════════════════════════════════

def _send_listing_published_email(listing, user):
    try:
        from apps.listings.emails.sender import send_scenario
        send_scenario(
            code='listing_published',
            to_email=user.email,
            to_user=user,
            context={
                'user_name': user.first_name or user.username,
                'listing_title': listing.title,
                'listing_price_display': f'{listing.currency_symbol}{int(listing.price)}',
                'listing_url': f'{settings.SITE_URL}{listing.get_absolute_url()}',
                'active_days': Listing.DEFAULT_ACTIVE_DAYS,
            },
        )
    except Exception as e:
        print(f"[email] listing_published failed: {e}")


def _send_listing_sold_confirmation_email(listing, user, display_sold):
    try:
        from apps.listings.emails.sender import send_scenario
        days_active = 0
        if listing.created_at:
            days_active = (timezone.now() - listing.created_at).days

        send_scenario(
            code='listing_sold_confirmation',
            to_email=user.email,
            to_user=user,
            context={
                'user_name': user.first_name or user.username,
                'listing_title': listing.title,
                'listing_price_display': f'{listing.currency_symbol}{int(listing.price)}',
                'days_active': days_active,
                'display_sold': display_sold,
                'sold_display_days': Listing.SOLD_DISPLAY_DAYS,
            },
        )
    except Exception as e:
        print(f"[email] listing_sold_confirmation failed: {e}")


def _send_saved_listing_sold_emails(listing):
    try:
        from apps.listings.emails.sender import send_scenario

        saved_by_users = SavedListing.objects.filter(
            listing=listing
        ).select_related('user')

        similar_url = (
            f'{settings.SITE_URL}/?brand={listing.brand_id}'
            if listing.brand_id else f'{settings.SITE_URL}/'
        )

        for saved in saved_by_users:
            user = saved.user
            if not user or not user.email:
                continue
            if user == listing.seller:
                continue

            send_scenario(
                code='saved_listing_sold',
                to_email=user.email,
                to_user=user,
                context={
                    'user_name': user.first_name or user.username,
                    'listing_title': listing.title,
                    'listing_price_display': f'{listing.currency_symbol}{int(listing.price)}',
                    'similar_url': similar_url,
                },
            )
    except Exception as e:
        print(f"[email] saved_listing_sold failed: {e}")


def _send_saved_listing_updated_emails(listing, change_summary):
    try:
        from apps.listings.emails.sender import send_scenario

        saved_by_users = SavedListing.objects.filter(
            listing=listing
        ).select_related('user')

        for saved in saved_by_users:
            user = saved.user
            if not user or not user.email:
                continue
            if user == listing.seller:
                continue

            send_scenario(
                code='saved_listing_updated',
                to_email=user.email,
                to_user=user,
                context={
                    'user_name': user.first_name or user.username,
                    'listing_title': listing.title,
                    'listing_price_display': f'{listing.currency_symbol}{int(listing.price)}',
                    'change_summary': change_summary,
                    'listing_url': f'{settings.SITE_URL}{listing.get_absolute_url()}',
                },
            )
    except Exception as e:
        print(f"[email] saved_listing_updated failed: {e}")


def _send_saved_listing_price_drop_emails(listing, old_price, new_price):
    try:
        from apps.listings.emails.sender import send_scenario

        drop_amount = old_price - new_price
        drop_percent = int(round((drop_amount / old_price) * 100)) if old_price > 0 else 0
        sym = listing.currency_symbol

        saved_by_users = SavedListing.objects.filter(
            listing=listing
        ).select_related('user')

        for saved in saved_by_users:
            user = saved.user
            if not user or not user.email:
                continue
            if user == listing.seller:
                continue

            send_scenario(
                code='saved_listing_price_drop',
                to_email=user.email,
                to_user=user,
                context={
                    'listing_title': listing.title,
                    'old_price_display': f'{sym}{int(old_price)}',
                    'new_price_display': f'{sym}{int(new_price)}',
                    'drop_amount_display': f'{sym}{int(drop_amount)}',
                    'drop_percent': drop_percent,
                    'listing_url': f'{settings.SITE_URL}{listing.get_absolute_url()}',
                },
            )
    except Exception as e:
        print(f"[email] saved_listing_price_drop failed: {e}")


def _send_listing_saved_by_users_email(listing, saver_user):
    try:
        from apps.listings.emails.sender import send_scenario

        seller = listing.seller
        if not seller or not seller.email:
            return

        if saver_user == seller:
            return

        send_scenario(
            code='listing_saved_by_users',
            to_email=seller.email,
            to_user=seller,
            context={
                'user_name': seller.first_name or seller.username,
                'listing_title': listing.title,
                'listing_price_display': f'{listing.currency_symbol}{int(listing.price)}',
                'listing_url': f'{settings.SITE_URL}{listing.get_absolute_url()}',
                'total_saves': listing.saved_by.count(),
            },
        )
    except Exception as e:
        print(f"[email] listing_saved_by_users failed: {e}")


def _send_listing_first_views_email(listing):
    try:
        from apps.listings.emails.sender import send_scenario

        seller = listing.seller
        if not seller or not seller.email:
            return

        send_scenario(
            code='listing_first_views',
            to_email=seller.email,
            to_user=seller,
            context={
                'user_name': seller.first_name or seller.username,
                'listing_title': listing.title,
                'listing_price_display': f'{listing.currency_symbol}{int(listing.price)}',
                'views_count': listing.views_count,
                'listing_url': f'{settings.SITE_URL}{listing.get_absolute_url()}',
            },
        )
    except Exception as e:
        print(f"[email] listing_first_views failed: {e}")


def _send_listing_views_milestone_email(listing, milestone):
    try:
        from apps.listings.emails.sender import send_scenario

        seller = listing.seller
        if not seller or not seller.email:
            return

        send_scenario(
            code='listing_views_milestone',
            to_email=seller.email,
            to_user=seller,
            context={
                'user_name': seller.first_name or seller.username,
                'listing_title': listing.title,
                'listing_price_display': f'{listing.currency_symbol}{int(listing.price)}',
                'views_count': listing.views_count,
                'milestone': milestone,
                'listing_url': f'{settings.SITE_URL}{listing.get_absolute_url()}',
            },
        )
    except Exception as e:
        print(f"[email] listing_views_milestone failed: {e}")


# ═══════════════════════════════════════════════════════════
# CATEGORY BREAKDOWN — used by my_listings dropdown
# ═══════════════════════════════════════════════════════════

def _build_category_breakdown(user):
    VT_CHILD_NAMES = {
        'cars': 'Cars',
        'motorcycles': 'Motorcycles',
        'vans': 'Vans',
        'trucks': 'Trucks',
        'parts': 'Parts',
        'tires': 'Tires & Wheels',
        'boats': 'Boats',
        'trailers': 'Trailers',
        'construction': 'Construction',
        'agriculture': 'Agriculture',
        'bicycles': 'Bicycles',
        'services': 'Services',
        'rental': 'Rental',
        'other': 'Other',
    }

    MERGED_VT_SLUGS = {'trucks'}

    rows = (
        Listing.objects.filter(seller=user)
        .values(
            'vehicle_type__id', 'vehicle_type__name', 'vehicle_type__slug',
            'subcategory__id', 'subcategory__name', 'subcategory__slug',
        )
        .annotate(count=Count('id'))
    )

    groups = {}
    for r in rows:
        vt_slug = r['vehicle_type__slug'] or 'other'
        vt_name = r['vehicle_type__name'] or 'Other'
        if vt_slug not in groups:
            groups[vt_slug] = {
                'group_name': vt_name,
                'group_slug': vt_slug,
                'group_count': 0,
                'children': [],
                '_merge_all': vt_slug in MERGED_VT_SLUGS,
            }
        groups[vt_slug]['group_count'] += r['count']

        if vt_slug in MERGED_VT_SLUGS:
            continue

        if r['subcategory__slug']:
            sub_slug = r['subcategory__slug']
            sub_name = r['subcategory__name']
            value = f'{vt_slug}:{sub_slug}'
        else:
            sub_slug = vt_slug
            sub_name = VT_CHILD_NAMES.get(vt_slug, vt_slug.replace('-', ' ').title())
            value = vt_slug

        groups[vt_slug]['children'].append({
            'name': sub_name,
            'slug': sub_slug,
            'count': r['count'],
            'value': value,
        })

    for vt_slug, g in groups.items():
        if g.get('_merge_all') and g['group_count'] > 0:
            g['children'].append({
                'name': VT_CHILD_NAMES.get(vt_slug, vt_slug.replace('-', ' ').title()),
                'slug': vt_slug,
                'count': g['group_count'],
                'value': vt_slug,
            })

    for g in groups.values():
        g['children'].sort(key=lambda c: c['name'])
        g.pop('_merge_all', None)

    return sorted(groups.values(), key=lambda g: g['group_name'])


# ═══════════════════════════════════════════════════════════
# SHADOW BAN / PUBLIC LISTINGS helper
# ═══════════════════════════════════════════════════════════

def _public_listings_qs(request_user=None):
    now = timezone.now()
    sold_cutoff = now - timedelta(days=Listing.SOLD_DISPLAY_DAYS)

    qs = Listing.objects.filter(
        Q(status='active') |
        Q(status='sold', sold_at__gte=sold_cutoff)
    )

    if request_user and request_user.is_authenticated and request_user.is_superuser:
        return qs
    return qs.filter(is_shadow_banned=False)


# ═══════════════════════════════════════════════════════════
# STATISTICS helpers
# ═══════════════════════════════════════════════════════════

def _get_client_ip(request):
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    if xff:
        return xff.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '')


def _track_listing_view(request, listing):
    user = request.user if request.user.is_authenticated else None

    if user:
        if user == listing.seller or user.is_superuser:
            return

    ip = _get_client_ip(request)
    one_hour_ago = timezone.now() - timedelta(hours=1)

    qs = ListingView.objects.filter(listing=listing, viewed_at__gte=one_hour_ago)
    if user:
        qs = qs.filter(user=user)
    elif ip:
        qs = qs.filter(user__isnull=True, ip_address=ip)
    else:
        return

    if qs.exists():
        return

    ListingView.objects.create(
        listing=listing,
        user=user,
        ip_address=ip or None,
    )
    listing.views_count = (listing.views_count or 0) + 1
    listing.save(update_fields=['views_count'])

    if listing.views_count >= 10 and not listing.first_views_notified_at:
        _send_listing_first_views_email(listing)
        listing.first_views_notified_at = timezone.now()
        listing.save(update_fields=['first_views_notified_at'])

    MILESTONES = [100, 500, 1000]
    current_milestone = 0
    for m in MILESTONES:
        if listing.views_count >= m:
            current_milestone = m
    if current_milestone > (listing.last_views_milestone or 0):
        _send_listing_views_milestone_email(listing, current_milestone)
        listing.last_views_milestone = current_milestone
        listing.save(update_fields=['last_views_milestone'])


def _track_listing_impressions(request, listings):
    user = request.user if request.user.is_authenticated else None
    ip = _get_client_ip(request)

    if not listings:
        return

    listings_to_track = []
    for listing in listings:
        if user:
            if user == listing.seller or user.is_superuser:
                continue
        listings_to_track.append(listing)

    if not listings_to_track:
        return

    impressions = [
        ListingImpression(
            listing=l,
            user=user,
            ip_address=ip or None,
        )
        for l in listings_to_track
    ]
    ListingImpression.objects.bulk_create(impressions)

    from django.db.models import F
    ids = [l.pk for l in listings_to_track]
    Listing.objects.filter(pk__in=ids).update(impressions_count=F('impressions_count') + 1)


def listing_list(request):
    from django.db.models import Count, Case, When, IntegerField, Value
    from itertools import groupby

    if request.GET.get('category') == 'motorcycles':
        # Auto-redirect to moto-gear if subcategory is gear-related
        subcategory_id = request.GET.get('subcategory')
        if subcategory_id:
            try:
                sub = SubCategory.objects.get(id=subcategory_id)
                if 'gear' in sub.slug.lower() or 'gear' in sub.name.lower():
                    return redirect('/browse/?category=moto-gear')
            except SubCategory.DoesNotExist:
                pass
        from . import motorcycles_views
        return motorcycles_views.motorcycles_list(request)

    if request.GET.get('category') == 'moto-gear':
        from . import motogear_views
        return motogear_views.motogear_list(request)

    # ═══ MIKROAUTOBUSAI → ten, kur skelbimai iš tikrųjų gyvena ═══
    # VT `vans` nebenaudojamas (etalone tokios kategorijos nėra), bet DB
    # lieka. Nukreipiam pagal subkategoriją, kad senos nuorodos neprarastų
    # prasmės: keleiviniai ir iki 3,5 t → automobiliai su kėbulo filtru,
    # virš 3,5 t → sunkvežimiai, kemperiai → turistiniai nameliai.
    if request.GET.get('category') == 'vans':
        _sub = _subcategory_slug_from(request.GET) or ''
        _params = request.GET.copy()
        _params.pop('subcategory', None)
        if _sub in ('cargo-minibuses-over-3-5t',):
            _params['category'] = 'trucks'
            _params['subcategory'] = 'trucks'
        elif _sub == 'campers':
            _params['category'] = 'camping-houses'
        else:
            _params['category'] = 'cars'
            _params.setdefault('body_type', 'minibus')
        return redirect(f"{reverse('listing_list')}?{_params.urlencode()}")

    # ═══ AUTOMOBILIŲ SUPIRKIMAS → paslaugos su pritaikytu tipo filtru ═══
    # Autogide tai ne kategorija, o vienas iš 24 paslaugų tipų, todėl
    # skelbimai gyvena `services` VT su service_type='car_buying'.
    # Atskiras car-buying VT DB lieka, bet nebenaudojamas — visos senos
    # nuorodos ir navigacijos punktas persiadresuoja čia.
    if request.GET.get('category') == 'car-buying':
        _params = request.GET.copy()
        _params['category'] = 'services'
        _params.setdefault('service_type', 'car_buying')
        return redirect(f"{reverse('listing_list')}?{_params.urlencode()}")

    # ═══ TYRES & WHEELS → redirect į WheelListing browse ═══
    if request.GET.get('category') in ('tires', 'wheels'):
        wheel_type = 'tyre'
        subcategory_id = request.GET.get('subcategory')
        if subcategory_id:
            try:
                sub = SubCategory.objects.get(id=subcategory_id)
                if 'rim' in sub.slug.lower() or 'rim' in sub.name.lower() or 'ratlank' in sub.name.lower():
                    wheel_type = 'rim'
            except SubCategory.DoesNotExist:
                pass
        return redirect(f'/browse/wheels/?type={wheel_type}')

    _now = timezone.now()
    _three_days_ago = _now - timedelta(days=NEW_LISTING_DAYS)

    from django.db.models import F
    from django.db.models.functions import Greatest, Coalesce

    listings = _public_listings_qs(request.user).select_related(
        'brand', 'model', 'submodel', 'fuel_type', 'transmission', 'vehicle_type'
    ).annotate(
        effective_date=Greatest(
            'created_at',
            Coalesce('last_boosted_at', 'created_at'),
        ),
    ).annotate(
        sort_priority=Case(
            When(star_level=2, star_expires_at__gt=_now, then=Value(500)),
            When(star_level=1, star_expires_at__gt=_now, then=Value(400)),
            When(effective_date__gt=_three_days_ago, then=Value(200)),
            default=Value(100),
            output_field=IntegerField(),
        )
    ).order_by('-sort_priority', '-effective_date')

    brand_counts = {
        item['brand_id']: item['count']
        for item in _public_listings_qs(request.user).values('brand_id').annotate(count=Count('id'))
    }
    brands_qs = Brand.objects.all().order_by('name')
    brands = [
        {'id': b.id, 'name': b.name, 'count': brand_counts.get(b.id, 0),
         'listing_count': brand_counts.get(b.id, 0)}
        for b in brands_qs
    ]
    brands.sort(key=lambda b: (-b['listing_count'], b['name']))

    current_year = timezone.now().year
    years = list(range(current_year + 1, 1989, -1))
    fuel_types = FuelType.objects.all().order_by('name')
    transmissions = Transmission.objects.all().order_by('name')

    category_filter = request.GET.get('category', 'cars')
    brand_filter = request.GET.get('brand')
    model_filter = request.GET.get('model')
    submodel_filter = request.GET.get('submodel')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    year_min = request.GET.get('year_min')
    year_max = request.GET.get('year_max')
    fuel_type_filter = request.GET.get('fuel_type')
    transmission_filter = request.GET.get('transmission')
    search_query = request.GET.get('search', '')
    country_filter = request.GET.get('country_filter', '')
    state_filter = request.GET.get('state_filter', '')

    if category_filter:
        listings = listings.filter(vehicle_type__slug=category_filter)
    subcategory_filter = request.GET.get('subcategory')
    if subcategory_filter:
        # Priima ir id, ir slug'ą — kaip filter_listings. Nuomos panelė
        # siunčia slug'ą (jis skaitomas URL'e ir stabilus), o be šito
        # šaka mestų ValueError: Field 'id' expected a number.
        if str(subcategory_filter).isdigit():
            listings = listings.filter(subcategory_id=subcategory_filter)
        else:
            listings = listings.filter(subcategory__slug=subcategory_filter)

    # ═══ PRIEKABOS — išplėstiniai laukai (dar ne konfigūracijoje) ═══
    if category_filter == 'trailers':
        listings = apply_trailer_filters(listings, request.GET)

    # ═══ DEKLARATYVUS SLUOKSNIS ═══
    _sub_slug = _subcategory_slug_from(request.GET)
    listings = panel_config.apply_panel_filters(
        listings, category_filter, request.GET, sub_slug=_sub_slug)
    listings = panel_config.apply_panel_filters(
        listings, category_filter, request.GET, source='advanced', sub_slug=_sub_slug)

    if search_query:
        listings = listings.filter(title__icontains=search_query)
    if brand_filter:
        listings = listings.filter(brand_id=brand_filter)
    if model_filter:
        listings = listings.filter(model_id=model_filter)
    if submodel_filter:
        listings = listings.filter(submodel_id=submodel_filter)
    if price_min:
        listings = listings.filter(price__gte=price_min)
    if price_max:
        listings = listings.filter(price__lte=price_max)
    if year_min:
        listings = listings.filter(year__gte=year_min)
    if year_max:
        listings = listings.filter(year__lte=year_max)
    if fuel_type_filter:
        listings = listings.filter(fuel_type_id=fuel_type_filter)
    body_type_filter = [v for v in request.GET.getlist('body_type') if v]
    if body_type_filter:
        listings = listings.filter(body_type__in=body_type_filter)
    if state_filter:
        listings = listings.filter(country='US', state=state_filter)
    elif country_filter:
        listings = listings.filter(country=country_filter)

    # ═══ Posted within (24h, 3d, 7d, 30d) ═══
    posted_within = request.GET.get('posted_within')
    if posted_within:
        try:
            days = int(posted_within)
            if days == 1:
                cutoff = timezone.now() - timedelta(hours=24)
            else:
                cutoff = timezone.now() - timedelta(days=days)
            listings = listings.filter(created_at__gte=cutoff)
        except (ValueError, TypeError):
            pass

    # ═══ Mileage range ═══
    mileage_min = request.GET.get('mileage_min')
    mileage_max = request.GET.get('mileage_max')
    if mileage_min:
        listings = listings.filter(mileage__gte=mileage_min)
    if mileage_max:
        listings = listings.filter(mileage__lte=mileage_max)

    # ═══ Transmission ═══
    transmission_filter = request.GET.get('transmission')
    if transmission_filter:
        listings = listings.filter(transmission_id=transmission_filter)

    # ═══ Defects ═══
    defects_filter = request.GET.get('defects')
    if defects_filter:
        listings = listings.filter(defects=defects_filter)

    # ═══ City ═══
    city_filter_val = request.GET.get('city', '').strip()
    if city_filter_val:
        listings = listings.filter(city__icontains=city_filter_val)

    # ═══ Text search via 'q' (sidebar uses 'q', top filter uses 'search') ═══
    q_param = request.GET.get('q', '').strip()
    if q_param:
        listings = listings.filter(title__icontains=q_param)

    # ═══ VIN required ═══
    if request.GET.get('has_vin'):
        listings = listings.exclude(vin__isnull=True).exclude(vin='')

    # ═══ Trade-in accepted ═══
    if request.GET.get('feat_trade_in'):
        listings = listings.filter(open_to_trade=True)

    # ═══ Special features ═══
    if request.GET.get('feat_warranty'):
        listings = listings.filter(has_warranty=True)
    if request.GET.get('feat_lease'):
        listings = listings.filter(available_on_lease=True)
    if request.GET.get('feat_sport'):
        listings = listings.filter(is_sport_ready=True)
    if request.GET.get('feat_disabled'):
        listings = listings.filter(disabled_friendly=True)
    if request.GET.get('feat_service_book'):
        listings = listings.filter(has_service_book=True)
    if request.GET.get('feat_us_import'):
        listings = listings.filter(imported_from_us=True)

    # ═══ Sort logika ═══
    sort_param = request.GET.get('sort', 'newest')
    if sort_param == 'price_asc':
        listings = listings.order_by('price', '-created_at')
    elif sort_param == 'price_desc':
        listings = listings.order_by('-price', '-created_at')
    elif sort_param == 'mileage_asc':
        listings = listings.order_by('mileage', '-created_at')
    elif sort_param == 'mileage_desc':
        listings = listings.order_by('-mileage', '-created_at')
    elif sort_param == 'year_asc':
        listings = listings.order_by('year', '-created_at')
    elif sort_param == 'year_desc':
        listings = listings.order_by('-year', '-created_at')
    elif sort_param == 'newest_renewed':
        # Priority: jei yra last_boosted_at — naudoja jį, kitaip created_at
        from django.db.models import F, Case, When, DateTimeField
        listings = listings.annotate(
            sort_date=Case(
                When(last_boosted_at__isnull=False, then=F('last_boosted_at')),
                default=F('created_at'),
                output_field=DateTimeField(),
            )
        ).order_by('-sort_date')
    else:
        # Default: newest (created_at desc)
        listings = listings.order_by('-created_at')
    if request.GET.get('feat_multi_keys'):
        listings = listings.filter(multiple_keys=True)
    if request.GET.get('feat_power_boost'):
        listings = listings.filter(power_boosted=True)
    if request.GET.get('feat_pneumatic'):
        listings = listings.filter(pneumatic_suspension=True)
    if request.GET.get('feat_remote_start'):
        listings = listings.filter(remote_start=True)
    if request.GET.get('feat_spare_wheel'):
        listings = listings.filter(spare_wheel=True)

    # ═══ Valid inspection / Hide auctions / Seller type ═══
    if request.GET.get('valid_inspection'):
        listings = listings.filter(valid_inspection=True)
    if request.GET.get('hide_auctions'):
        listings = listings.filter(is_auction=False)
    seller_type_filter = request.GET.get('seller_type')
    if seller_type_filter:
        listings = listings.filter(seller_type=seller_type_filter)

    models = []
    if brand_filter:
        models = Model.objects.filter(brand_id=brand_filter).order_by('name')

    saved_ids = []
    if request.user.is_authenticated:
        saved_ids = list(SavedListing.objects.filter(
            user=request.user
        ).values_list('listing_id', flat=True))

    listings_list = list(listings[:60])
    _track_listing_impressions(request, listings_list)

    # ═══ Equipment filter — sidebar checkboxes (cars-only) ═══
    equipment_ids_selected = request.GET.getlist('equipment')
    if equipment_ids_selected:
        for eid in equipment_ids_selected:
            listings = listings.filter(equipment_items__equipment_id=eid)
        listings_list = list(listings[:60])

    CARS_CAT_KEYS = [k for k, _ in CARS_EQUIPMENT_CATEGORIES]
    CARS_CAT_LABELS = dict(CARS_EQUIPMENT_CATEGORIES)
    all_equipment_qs = Equipment.objects.filter(
        category__in=CARS_CAT_KEYS
    ).order_by('category', 'name')
    equipment_by_category = [
        (cat_key, CARS_CAT_LABELS.get(cat_key, cat_key), list(items))
        for cat_key, items in groupby(all_equipment_qs, key=lambda x: x.category)
    ]

    new_listing_ids = [
        l.id for l in listings_list
        if l.created_at >= timezone.now() - timedelta(days=NEW_LISTING_DAYS)
    ]

    categories_qs = _get_visible_vehicle_types(request.user)
    categories = sorted(
        [
            {
                'value': vt.slug,
                'label': vt.name,
                'icon': CATEGORY_ICONS.get(vt.slug, '🚗'),
            }
            for vt in categories_qs
        ],
        key=lambda x: (0 if x['value'] == 'cars' else 1, x['label'])
    )

    _now_tabs = timezone.now()
    _tabs_base = _public_listings_qs(request.user).select_related(
        'brand', 'model', 'fuel_type', 'transmission'
    )

    # 1. Pirmiausia: mokami featured listings (rodomi viršuje)
    featured_paid = list(
        _tabs_base.filter(
            featured_until__gt=_now_tabs,
        ).order_by('-featured_until')[:6]
    )

    # 2. Užpildym iki 6 su žvaigždutiniais (jei featured neužtenka)
    if len(featured_paid) < 6:
        remaining = 6 - len(featured_paid)
        featured_ids = [l.pk for l in featured_paid]
        starred = list(
            _tabs_base.filter(
                star_level__gte=1,
                star_expires_at__gt=_now_tabs,
            ).exclude(pk__in=featured_ids)
            .order_by('-star_level', '-star_count', '-last_boosted_at')[:remaining]
        )
        tab_featured = featured_paid + starred
    else:
        tab_featured = featured_paid

    tab_newest = list(_tabs_base.order_by('-created_at')[:6])
    tab_popular = list(_tabs_base.order_by('-views_count')[:6])
    tab_expensive = list(_tabs_base.filter(price__gt=0).order_by('-price')[:6])

    # Moto brands ir wheel counts — search panel

    try:

        from .models import MotorcycleBrand

        moto_brands = list(MotorcycleBrand.objects.all().order_by('name'))

    except Exception:

        moto_brands = []

    try:

        from .models import WheelListing

        wheel_counts = {

            'tyre': WheelListing.objects.filter(status='active', wheel_type='tyre').count(),

            'rim': WheelListing.objects.filter(status='active', wheel_type='rim').count(),

        }

    except Exception:

        wheel_counts = {'tyre': 0, 'rim': 0}

    # ═══ MORE flyout — fiksuotas plokščias sąrašas (autogidas tvarka), be nested subų ═══
    _vt_counts = {
        r['vehicle_type__slug']: r['c']
        for r in _public_listings_qs(request.user)
            .values('vehicle_type__slug').annotate(c=Count('id'))
    }
    _sub_counts = {
        r['subcategory_id']: r['c']
        for r in _public_listings_qs(request.user)
            .filter(subcategory__isnull=False)
            .values('subcategory_id').annotate(c=Count('id'))
    }

    _car_buying_count = _public_listings_qs(request.user).filter(
        vehicle_type__slug='services', service_type='car_buying').count()

    # (slug, pavadinimas, svg_path_d, subcategory_id|None)
    MORE_ITEMS_SPEC = [
        ('agriculture',       'Žemės ūkio technika, padargai',        'M4 17a2 2 0 104 0 2 2 0 00-4 0zM15 17a3 3 0 106 0 3 3 0 00-6 0zM6 15V8h5l3 4M9 8V5h4', None),
        ('trucks',            'Sunkvežimiai',                         'M3 6h10v9H3zM13 9h4l3 3v3h-7M6 18a1.5 1.5 0 100-3 1.5 1.5 0 000 3zM17 18a1.5 1.5 0 100-3 1.5 1.5 0 000 3z', None),
        ('tractor-units',     'Vilkikai',                             'M3 7h7v8H3zM10 10h4l3 3v2h-7M6 18a1.5 1.5 0 100-3 1.5 1.5 0 000 3zM14 18a1.5 1.5 0 100-3 1.5 1.5 0 000 3z', None),
        ('car-carriers',      'Autotraukiniai, autovežiai',           'M2 8h12v7H2zM14 10h5l1 2v3h-6M5 18a1.5 1.5 0 100-3 1.5 1.5 0 000 3zM16 18a1.5 1.5 0 100-3 1.5 1.5 0 000 3zM4 6l3 2M8 6l3 2', None),
        ('trucks',            'Autobusai',                            'M4 5h16v11H4zM4 9h16M7 20a1.5 1.5 0 100-3 1.5 1.5 0 000 3zM17 20a1.5 1.5 0 100-3 1.5 1.5 0 000 3z', 198),
        ('municipal',         'Komunalinio ūkio transportas',         'M4 8h8v7H4zM12 10h4l4 2v3h-8M7 18a1.5 1.5 0 100-3 1.5 1.5 0 000 3zM16 18a1.5 1.5 0 100-3 1.5 1.5 0 000 3zM6 8V5h4v3', None),
        ('trailers',          'Priekabos / Puspriekabės',             'M3 7h14v8H3zM17 12h4M9 18a1.5 1.5 0 100-3 1.5 1.5 0 000 3z', None),
        ('rental',            'Automobilių nuoma',                    'M15 7a4 4 0 11-1 3l-6 6H5v-2l6-6a4 4 0 013-1z', None),
        ('rental',            'Limuzinų, vestuvių transporto nuoma',  'M2 12h20v4H2zM4 12l2-4h9l3 4M6 19a1.5 1.5 0 100-3 1.5 1.5 0 000 3zM18 19a1.5 1.5 0 100-3 1.5 1.5 0 000 3z', 294),
        ('rental',            'Motociklų nuoma',                      'M5 17a3 3 0 100-6 3 3 0 000 6zM19 17a3 3 0 100-6 3 3 0 000 6zM8 14h5l3-4h3M11 10h4', 295),
        ('rental',            'Mikroautobusų, turistinio, vandens tr. nuoma', 'M3 8h13v8H3zM16 11h3l2 3v2h-5M6 19a1.5 1.5 0 100-3 1.5 1.5 0 000 3zM15 19a1.5 1.5 0 100-3 1.5 1.5 0 000 3zM6 8v8M10 8v8', 317),
        ('rental',            'Sunkiojo transporto, priekabų nuoma',  'M3 6h10v9H3zM13 9h4l3 3v3h-7M6 18a1.5 1.5 0 100-3 1.5 1.5 0 000 3zM17 18a1.5 1.5 0 100-3 1.5 1.5 0 000 3z', 296),
        ('electronics',       'Video, audio, navigacijos',            'M3 5h18v11H3zM8 20h8M12 16v4', None),
        ('services',          'Paslaugos',                            'M14 7a3 3 0 00-4 4l-6 6 2 2 6-6a3 3 0 004-4l-2 2-2-2z', None),
        ('car-buying',        'Automobilių supirkimas',               'M5 11l1-4h8l2 4M4 11h14v4H4zM7 18a1.5 1.5 0 100-3 1.5 1.5 0 000 3zM15 18a1.5 1.5 0 100-3 1.5 1.5 0 000 3zM19 8l2 1-1 2', None),
        ('loading-equipment', 'Krovimo ir sandėliavimo technika',     'M4 4v13h4M8 17a1.5 1.5 0 100 3 1.5 1.5 0 000-3zM14 17a1.5 1.5 0 100 3 1.5 1.5 0 000-3zM10 8h6v6h-6zM4 4h3', None),
        ('construction',      'Statybinė technika',                   'M3 20h14M5 20v-6l6-3 6 3M9 11V7l4-2 4 2v4M6 20v-4h4v4', None),
        ('construction',      'Statybinės technikos priedai',         'M12 8a4 4 0 100 8 4 4 0 000-8zM12 3v2M12 19v2M3 12h2M19 12h2M6 6l1.5 1.5M16.5 16.5L18 18', 297),
        ('forestry',          'Miško ūkio technika',                  'M12 3l4 6h-3l3 5h-3l2 4H8l2-4H7l3-5H7l5-6zM12 18v3', None),
        ('camping-houses',    'Turistiniai nameliai',                 'M3 8h11a2 2 0 012 2v6H3zM16 12h3l2 3v1h-5M7 19a2 2 0 100-4 2 2 0 000 4zM6 8v3h5V8', None),
        ('boats',             'Vandens transportas',                  'M4 14h16l-2 4H6l-2-4zM6 14V8l6-3 6 3v6M12 5V3', None),
        ('bicycles',          'El. paspirtukai, riedžiai, dviračiai', 'M5 18a3 3 0 100-6 3 3 0 000 6zM19 18a3 3 0 100-6 3 3 0 000 6zM8 15l3-6h4M10 9h4l2 6M14 9l1-3h2', None),
    ]

    more_items = []
    for _slug, _name, _icon, _sub_id in MORE_ITEMS_SPEC:
        more_items.append({
            'is_sub': _sub_id is not None,
            'slug': _slug,
            'sub_id': _sub_id,
            'name': _name,
            'icon': _icon,
            # car-buying skelbimų neturi ir neturės — rodom, kiek yra
            # paslaugų su tipu „Automobilių supirkimas"
            'count': (_car_buying_count if _slug == 'car-buying'
                      else _sub_counts.get(_sub_id, 0) if _sub_id
                      else _vt_counts.get(_slug, 0)),
        })



    context = {
        'listings': listings_list,
        'brands': brands,
        'moto_brands': moto_brands,
        'wheel_counts': wheel_counts,
        'more_items': more_items,
        **parts_panel_context(request.user),
        **trailers_panel_context(request.user),
        'selected_trailer_equipment': request.GET.getlist('trailer_equipment'),
        'config_panels': {
            slug: panel_config.build_panel(slug, request.user)
            for slug in panel_config.active_categories()
        },
        'config_panels_sub': {
            sub: panel_config.build_panel(
                cfg['vt_slug'], request.user, sub_slug=sub)
            for sub, cfg in panel_config.PANELS_BY_SUB.items()
        },
        'models': models,
        'years': years,
        'fuel_types': fuel_types,
        'transmissions': transmissions,
        'body_type_choices': Listing.BODY_TYPE_CHOICES,
        'selected_body_types': request.GET.getlist('body_type'),
        'search_query': search_query,
        'total_count': listings.count(),
        'categories': categories,
        'selected_category': category_filter,
        'saved_ids': saved_ids,
        'new_listing_ids': new_listing_ids,
        'us_states': Listing.US_STATE_CHOICES,
        'country_choices': Listing.COUNTRY_CHOICES,
        'location_countries': [{'code': c, 'name': n, 'fi_code': c.lower()} for c, n in Listing.COUNTRY_CHOICES],
        'selected_country': country_filter,
        'selected_state': state_filter,
        'tab_featured': tab_featured,
        'tab_newest': tab_newest,
        'tab_popular': tab_popular,
        'tab_expensive': tab_expensive,
        'equipment_by_category': equipment_by_category,
        'selected_equipment': equipment_ids_selected,
    }
    return render(request, 'listings/listing_list.html', context)


# ════════════════════════════════════════════════════════════════════
# BROWSE V2 — autogidas-style sidebar layout (experimental, /v2/)
# Kopija listing_list su nauju template'u + subcategory counts
# ════════════════════════════════════════════════════════════════════

def listing_list_v2(request):
    """Eksperimentinis Browse puslapis su autogidas style sidebar'u.
    Pasiekiamas per /v2/. Logika identiška listing_list, tik template kitas
    + papildomi context'ai (subcategory counts, category icons)."""

    # Naudoja TĄ PAČIĄ listing_list logiką — paprasčiausias būdas
    # išvengti dublikacijos. View'as iškviečia listing_list, gauna response,
    # tada perrenderina su nauju template'u.
    # Bet paprasčiau: tiesiog rekursinis call su override'u.

    # ─── Surenkam tuos pačius duomenis kaip listing_list ───
    listings = _public_listings_qs(request.user).select_related(
        'brand', 'model', 'submodel', 'fuel_type', 'transmission', 'vehicle_type'
    ).order_by('-created_at')

    category_filter = request.GET.get('category', 'cars')
    brand_filter = request.GET.get('brand')

    if category_filter:
        listings = listings.filter(vehicle_type__slug=category_filter)
    if brand_filter:
        listings = listings.filter(brand_id=brand_filter)

    listings_list = list(listings[:60])

    brands = Brand.objects.all().order_by('name')
    fuel_types = FuelType.objects.all().order_by('name')
    current_year = timezone.now().year
    years = list(range(current_year + 1, 1989, -1))

    saved_ids = []
    if request.user.is_authenticated:
        saved_ids = list(SavedListing.objects.filter(
            user=request.user
        ).values_list('listing_id', flat=True))

    # ─── Sidebar kategorijos su counts ───
    visible_vts = _get_visible_vehicle_types(request.user)
    sidebar_categories = []
    for vt in visible_vts:
        count = _public_listings_qs(request.user).filter(vehicle_type=vt).count()
        sidebar_categories.append({
            'slug': vt.slug,
            'name': vt.name,
            'icon': CATEGORY_ICONS.get(vt.slug, '🚗'),
            'count': count,
            'active': category_filter == vt.slug,
        })

    # ─── Subkategorijos selected kategorijai su counts ───
    subcategories = []
    try:
        selected_vt = visible_vts.filter(slug=category_filter).first()
        if selected_vt:
            from .models import SubCategory
            subs = SubCategory.objects.filter(
                vehicle_type=selected_vt,
                parent__isnull=True,
            ).order_by('order', 'name')
            for sub in subs:
                sub_count = _public_listings_qs(request.user).filter(
                    vehicle_type=selected_vt,
                    subcategory=sub,
                ).count()
                subcategories.append({
                    'slug': sub.slug,
                    'name': sub.name,
                    'count': sub_count,
                })
    except Exception as e:
        print(f"[v2] subcategories error: {e}")

    context = {
        'listings': listings_list,
        'brands': brands,
        'years': years,
        'fuel_types': fuel_types,
        'total_count': listings.count(),
        'selected_category': category_filter,
        'sidebar_categories': sidebar_categories,
        'subcategories': subcategories,
        'saved_ids': saved_ids,
    }
    return render(request, 'listings/listing_list_v2.html', context)


def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)

    if listing.is_shadow_banned:
        is_owner = request.user.is_authenticated and listing.seller == request.user
        is_admin = request.user.is_authenticated and request.user.is_superuser
        if not (is_owner or is_admin):
            raise Http404("Listing not found")

    _track_listing_view(request, listing)

    is_owner = request.user.is_authenticated and listing.seller == request.user
    is_saved = request.user.is_authenticated and SavedListing.objects.filter(
        user=request.user, listing=listing
    ).exists()

    # ─── Grouped equipment for autogidas-style display ───
    grouped_equipment = _build_grouped_equipment(listing)

    # ─── Dealer active listings count (jei seller yra dealer) ───
    dealer_active_listings_count = 0
    if hasattr(listing.seller, 'profile') and listing.seller.profile.dealer_subscription_active:
        dealer_active_listings_count = Listing.objects.filter(
            seller=listing.seller,
            status='active',
            is_shadow_banned=False,
        ).count()

    context = {
        'listing': listing,
        'is_owner': is_owner,
        'is_saved': is_saved,
        'grouped_equipment': grouped_equipment,
        'dealer_active_listings_count': dealer_active_listings_count,
        'GOOGLE_MAPS_API_KEY': getattr(settings, 'GOOGLE_MAPS_API_KEY', ''),
    }
    return render(request, 'listings/listing_detail.html', context)


# ═══════════════════════════════════════════════════════════
# CARS DRAFT HELPERS
# ═══════════════════════════════════════════════════════════

def _get_or_create_cars_draft(request, vehicle_type_id=None, subcategory_id=None):
    draft_id = request.session.get(CARS_DRAFT_SESSION_KEY)
    if draft_id:
        try:
            draft = Listing.objects.get(
                pk=draft_id,
                seller=request.user,
                status='draft',
            )
            return draft
        except Listing.DoesNotExist:
            request.session[CARS_DRAFT_SESSION_KEY] = None

    if not vehicle_type_id:
        return None

    try:
        vehicle_type = VehicleType.objects.get(pk=vehicle_type_id)
    except VehicleType.DoesNotExist:
        return None

    draft = Listing.objects.filter(
        seller=request.user,
        vehicle_type=vehicle_type,
        status='draft',
    ).order_by('-updated_at').first()
    if draft is not None:
        request.session[CARS_DRAFT_SESSION_KEY] = draft.pk
        request.session.modified = True
        return draft
    draft = Listing.objects.create(
        seller=request.user,
        vehicle_type=vehicle_type,
        title='Untitled draft',
        year=date.today().year,
        mileage=0,
        price=0,
        country='US',
        city='—',
        status='draft',
    )
    if draft.condition or draft.defects:
        draft.condition = ''
        draft.defects = ''
        draft.save(update_fields=['condition', 'defects'])
    request.session[CARS_DRAFT_SESSION_KEY] = draft.pk
    request.session.modified = True
    return draft


def _draft_to_session_data(draft):
    if not draft:
        return {}

    data = {
        'step1': {
            'vehicle_type': draft.vehicle_type_id,
        },
        'step3_partial': {},
        'step5': {},
        'step6': {},
        'step7': {},
    }

    if draft.brand_id:
        data['step1']['brand'] = draft.brand_id
    if draft.model_id:
        data['step1']['model'] = draft.model_id
    if draft.year:
        data['step1']['year'] = draft.year
    if draft.first_registration:
        data['step1']['first_registration_month'] = draft.first_registration.month
    if draft.vin:
        data['step1']['vin'] = draft.vin

    s3p = data['step3_partial']
    s3p['body_type'] = draft.body_type or ''
    s3p['fuel_type'] = str(draft.fuel_type_id) if draft.fuel_type_id else ''
    s3p['transmission'] = str(draft.transmission_id) if draft.transmission_id else ''
    s3p['doors'] = draft.doors or ''
    s3p['condition'] = draft.condition or ''
    s3p['color'] = draft.color or ''
    s3p['defects'] = draft.defects or ''
    s3p['steering'] = draft.steering or ''
    s3p['mileage'] = str(draft.mileage) if draft.mileage else ''
    s3p['engine_capacity'] = str(draft.engine_capacity) if draft.engine_capacity else ''
    s3p['power'] = str(draft.power) if draft.power else ''
    s3p['drive_type'] = draft.drive_type or ''
    s3p['seats'] = draft.seats or ''
    s3p['rim_size'] = draft.rim_size or ''
    s3p['climate'] = draft.climate or ''
    s3p['curb_weight'] = str(draft.curb_weight) if draft.curb_weight else ''
    s3p['euro_standard'] = draft.euro_standard or ''
    s3p['co2_emission'] = str(draft.co2_emission) if draft.co2_emission else ''
    s3p['fuel_consumption_city'] = str(draft.fuel_consumption_city) if draft.fuel_consumption_city else ''
    s3p['fuel_consumption_highway'] = str(draft.fuel_consumption_highway) if draft.fuel_consumption_highway else ''
    s3p['fuel_consumption_combined'] = str(draft.fuel_consumption_combined) if draft.fuel_consumption_combined else ''
    s3p['origin_country'] = draft.origin_country or ''
    s3p['technical_inspection_month'] = str(draft.technical_inspection_month) if draft.technical_inspection_month else ''
    s3p['technical_inspection_year'] = str(draft.technical_inspection_year) if draft.technical_inspection_year else ''

    if draft.price and draft.price > 0:
        data['step5']['price'] = float(draft.price)
        data['step5']['negotiable'] = draft.negotiable
    if draft.description:
        data['step6']['description'] = draft.description
    if draft.country or draft.city:
        data['step7']['country'] = draft.country or 'US'
        data['step7']['city'] = draft.city if draft.city != '—' else ''
        data['step7']['state'] = draft.state if hasattr(draft, 'state') else ''
        data['step7']['postal_code'] = draft.postal_code or ''
        data['step7']['address'] = draft.address or ''
        data['step7']['hide_exact_address'] = draft.hide_exact_address

    return data


def _draft_completed_steps(draft):
    completed = set()
    if not draft:
        return completed

    if draft.vehicle_type_id:
        completed.add(1)
    if draft.brand_id and draft.model_id and draft.year and draft.first_registration:
        completed.add(2)
    if draft.body_type and draft.fuel_type_id and draft.transmission_id and draft.doors and draft.condition and draft.mileage:
        completed.add(3)
    if 3 in completed:
        completed.add(4)
    if draft.price and draft.price > 0:
        completed.add(5)
    if draft.description:
        completed.add(6)
    return completed


@login_required
@require_POST
def upload_listing_images_ajax(request, pk):
    """AJAX upload for existing listings (used in Edit mode quick form)."""
    try:
        listing = Listing.objects.get(pk=pk, seller=request.user)
    except Listing.DoesNotExist:
        return JsonResponse({'success': False, 'error': str(_('Listing not found'))}, status=404)

    images = request.FILES.getlist('images')
    if not images:
        return JsonResponse({'success': False, 'error': str(_('No images uploaded'))}, status=400)

    try:
        validate_images(images)
    except ImageValidationError as exc:
        return JsonResponse({'success': False, 'error': str(exc)}, status=400)

    existing_count = listing.images.count()
    if existing_count + len(images) > 40:
        available = 40 - existing_count
        images = images[:max(0, available)]
        if not images:
            return JsonResponse({'success': False, 'error': str(_('Maximum 40 photos reached'))}, status=400)

    uploaded = []
    for i, image in enumerate(images):
        try:
            img = ListingImage.objects.create(
                listing=listing,
                image=image,
                is_main=(existing_count == 0 and i == 0),
                order=existing_count + i,
            )
            uploaded.append({
                'id': img.pk,
                'url': img.image.url,
                'is_main': img.is_main,
                'order': img.order,
            })
        except Exception as e:
            print(f"[upload_listing_images] error: {e}")

    return JsonResponse({
        'success': True,
        'uploaded': uploaded,
        'total_count': listing.images.count(),
    })


@login_required
@require_POST
def reorder_listing_images_ajax(request, pk):
    """AJAX reorder for existing listing images (Edit mode drag & drop)."""
    try:
        listing = Listing.objects.get(pk=pk, seller=request.user)
    except Listing.DoesNotExist:
        return JsonResponse({'success': False, 'error': str(_('Listing not found'))}, status=404)

    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

    image_ids = data.get('image_ids', [])
    if not image_ids:
        return JsonResponse({'success': False, 'error': 'No image_ids provided'}, status=400)

    for new_order, img_id in enumerate(image_ids):
        try:
            img = ListingImage.objects.get(pk=img_id, listing=listing)
            img.order = new_order
            img.is_main = (new_order == 0)
            img.save(update_fields=['order', 'is_main'])
        except ListingImage.DoesNotExist:
            continue

    return JsonResponse({'success': True})


@login_required
@require_POST
def rotate_listing_image_ajax(request, pk):
    """AJAX rotate image 90° clockwise (or counter-clockwise)."""
    from PIL import Image as PILImage
    from django.core.files.base import ContentFile
    import io

    try:
        img = ListingImage.objects.get(pk=pk, listing__seller=request.user)
    except ListingImage.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Image not found'}, status=404)

    direction = request.POST.get('direction', 'cw')  # 'cw' or 'ccw'

    try:
        with PILImage.open(img.image.path) as pil_img:
            # PIL rotation: counter-clockwise by default; we use expand=True
            if direction == 'ccw':
                rotated = pil_img.rotate(90, expand=True)
            else:
                rotated = pil_img.rotate(-90, expand=True)

            # Save back as JPEG (or original format)
            fmt = pil_img.format or 'JPEG'
            buffer = io.BytesIO()
            if rotated.mode in ('RGBA', 'LA', 'P') and fmt == 'JPEG':
                rotated = rotated.convert('RGB')
            rotated.save(buffer, format=fmt, quality=92)
            buffer.seek(0)

            # Save back to same file path
            from django.core.files.storage import default_storage
            file_path = img.image.name
            default_storage.delete(file_path)
            default_storage.save(file_path, ContentFile(buffer.read()))

        # Cache busting — append timestamp via update
        img.save(update_fields=['updated_at'] if hasattr(img, 'updated_at') else [])

        return JsonResponse({
            'success': True,
            'url': img.image.url + '?t=' + str(int(timezone.now().timestamp())),
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
@require_POST
def upload_draft_images_ajax(request):
    draft_id = request.session.get(CARS_DRAFT_SESSION_KEY)

    if not draft_id:
        cars_vt = VehicleType.objects.filter(slug='cars').first()
        if cars_vt:
            draft = _get_or_create_cars_draft(request, vehicle_type_id=cars_vt.pk)
        else:
            return JsonResponse({'success': False, 'error': 'No active draft'}, status=400)
    else:
        try:
            draft = Listing.objects.get(
                pk=draft_id,
                seller=request.user,
                status='draft',
            )
        except Listing.DoesNotExist:
            return JsonResponse({'success': False, 'error': str(_('Draft not found'))}, status=400)

    images = request.FILES.getlist('images')
    if not images:
        return JsonResponse({'success': False, 'error': str(_('No images uploaded'))}, status=400)

    try:
        validate_images(images)
    except ImageValidationError as exc:
        return JsonResponse({'success': False, 'error': str(exc)}, status=400)

    existing_count = draft.images.count()
    uploaded = []

    for i, image in enumerate(images[:40]):
        try:
            img = ListingImage.objects.create(
                listing=draft,
                image=image,
                is_main=(existing_count == 0 and i == 0),
                order=existing_count + i,
            )
            uploaded.append({
                'id': img.pk,
                'url': img.image.url,
                'is_main': img.is_main,
                'order': img.order,
            })
        except Exception as e:
            print(f"[upload_draft_images] error: {e}")

    return JsonResponse({
        'success': True,
        'uploaded': uploaded,
        'total_count': draft.images.count(),
    })


@login_required
@require_POST
def delete_draft_image_ajax(request, pk):
    try:
        img = ListingImage.objects.get(pk=pk, listing__seller=request.user, listing__status='draft')
        was_main = img.is_main
        listing = img.listing
        img.delete()

        if was_main:
            first = listing.images.order_by('order').first()
            if first:
                first.is_main = True
                first.save(update_fields=['is_main'])

        return JsonResponse({'success': True, 'remaining_count': listing.images.count()})
    except ListingImage.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Image not found'}, status=404)


@login_required
@require_POST
def reorder_draft_images_ajax(request):
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

    image_ids = data.get('image_ids', [])
    if not image_ids:
        return JsonResponse({'success': False, 'error': 'No image_ids provided'}, status=400)

    draft_id = request.session.get(CARS_DRAFT_SESSION_KEY)
    if not draft_id:
        return JsonResponse({'success': False, 'error': 'No active draft'}, status=400)

    for new_order, img_id in enumerate(image_ids):
        try:
            img = ListingImage.objects.get(
                pk=img_id,
                listing_id=draft_id,
                listing__seller=request.user,
            )
            img.order = new_order
            img.is_main = (new_order == 0)
            img.save(update_fields=['order', 'is_main'])
        except ListingImage.DoesNotExist:
            continue

    return JsonResponse({'success': True})


@login_required
@require_POST
def save_cars_draft_ajax(request):
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

    draft = None
    draft_id = request.session.get(CARS_DRAFT_SESSION_KEY)

    if draft_id:
        try:
            draft = Listing.objects.get(
                pk=draft_id,
                seller=request.user,
                status='draft',
            )
        except Listing.DoesNotExist:
            request.session[CARS_DRAFT_SESSION_KEY] = None
            draft = None

    if not draft:
        vehicle_type_id = _int_or_none(data.get('vehicle_type'))
        if vehicle_type_id:
            draft = _get_or_create_cars_draft(request, vehicle_type_id=vehicle_type_id)
        else:
            cars_vt = VehicleType.objects.filter(slug='cars').first()
            if cars_vt:
                draft = _get_or_create_cars_draft(request, vehicle_type_id=cars_vt.pk)

    if not draft:
        return JsonResponse({'success': False, 'error': 'Cannot create draft (no vehicle type)'}, status=400)

    if 'brand' in data and data['brand']:
        try:
            draft.brand = Brand.objects.get(pk=int(data['brand']))
            draft.model = None
        except (Brand.DoesNotExist, ValueError, TypeError):
            pass

    if 'model' in data and data['model']:
        try:
            draft.model = Model.objects.get(pk=int(data['model']))
        except (Model.DoesNotExist, ValueError, TypeError):
            pass

    if 'year' in data:
        y = _int_or_none(data['year'])
        if y:
            draft.year = y

    month_val = data.get('month') or data.get('first_registration_month')
    if month_val:
        m = _int_or_none(month_val)
        if m and draft.year:
            try:
                draft.first_registration = date(year=draft.year, month=m, day=1)
            except (ValueError, TypeError):
                pass

    if 'vin' in data:
        draft.vin = data['vin'] or ''

    if 'body_type' in data:
        draft.body_type = data['body_type'] or ''
    if 'fuel_type' in data:
        ft_id = _int_or_none(data['fuel_type'])
        if ft_id:
            try:
                draft.fuel_type = FuelType.objects.get(pk=ft_id)
            except FuelType.DoesNotExist:
                pass
        elif data['fuel_type'] == '':
            draft.fuel_type = None
    if 'transmission' in data:
        tr_id = _int_or_none(data['transmission'])
        if tr_id:
            try:
                draft.transmission = Transmission.objects.get(pk=tr_id)
            except Transmission.DoesNotExist:
                pass
        elif data['transmission'] == '':
            draft.transmission = None
    if 'doors' in data:
        draft.doors = data['doors'] or ''
    if 'condition' in data:
        draft.condition = data['condition'] or ''
    if 'color' in data:
        draft.color = data['color'] or ''
    if 'defects' in data:
        draft.defects = data['defects'] or ''
    if 'steering' in data:
        draft.steering = data['steering'] or ''
    if 'mileage' in data:
        m = _int_or_none(data['mileage'])
        if m is not None:
            draft.mileage = m
    if 'engine_capacity' in data:
        draft.engine_capacity = _float_or_none(data['engine_capacity'])
    if 'power' in data:
        draft.power = _int_or_none(data['power'])
    if 'drive_type' in data:
        draft.drive_type = data['drive_type'] or ''
    if 'seats' in data:
        draft.seats = data['seats'] or ''
    if 'rim_size' in data:
        draft.rim_size = data['rim_size'] or ''
    if 'climate' in data:
        draft.climate = data['climate'] or ''
    if 'curb_weight' in data:
        draft.curb_weight = _int_or_none(data['curb_weight'])
    if 'euro_standard' in data:
        draft.euro_standard = data['euro_standard'] or ''
    if 'co2_emission' in data:
        draft.co2_emission = _int_or_none(data['co2_emission'])
    if 'fuel_consumption_city' in data:
        draft.fuel_consumption_city = _float_or_none(data['fuel_consumption_city'])
    if 'fuel_consumption_highway' in data:
        draft.fuel_consumption_highway = _float_or_none(data['fuel_consumption_highway'])
    if 'fuel_consumption_combined' in data:
        draft.fuel_consumption_combined = _float_or_none(data['fuel_consumption_combined'])
    if 'origin_country' in data:
        draft.origin_country = data['origin_country'] or ''
    if 'technical_inspection_month' in data:
        draft.technical_inspection_month = _int_or_none(data['technical_inspection_month'])
    if 'technical_inspection_year' in data:
        draft.technical_inspection_year = _int_or_none(data['technical_inspection_year'])

    if 'price' in data:
        p = _float_or_none(data['price'])
        if p is not None:
            draft.price = p
    if 'negotiable' in data:
        draft.negotiable = data['negotiable'] in (True, 'on', 'true', '1', 1)

    if 'description' in data:
        draft.description = data['description'] or ''
    if 'video_url' in data:
        draft.video_url = data['video_url'] or ''

    equipment_ids = data.get('equipment')
    if isinstance(equipment_ids, list):
        ListingEquipment.objects.filter(listing=draft).delete()
        for eid in equipment_ids:
            try:
                eid_int = int(eid)
                ListingEquipment.objects.create(
                    listing=draft,
                    equipment_id=eid_int,
                )
            except (ValueError, TypeError):
                pass

    if 'country' in data:
        draft.country = data['country'] or 'US'
    if hasattr(draft, 'state') and 'state' in data:
        draft.state = data['state'] or ''
    if 'city' in data:
        if data['city']:
            draft.city = data['city']
    if 'postal_code' in data:
        draft.postal_code = data['postal_code'] or ''
    if 'address' in data:
        draft.address = data['address'] or ''
    if 'hide_exact_address' in data:
        draft.hide_exact_address = data['hide_exact_address'] in (True, 'on', 'true', '1', 1)

    if draft.brand and draft.year:
        title_parts = [draft.brand.name]
        if draft.model:
            title_parts.append(draft.model.name)
        title_parts.append(str(draft.year))
        draft.title = ' '.join(title_parts)

    if draft.country:
        lat, lng = get_coordinates_for_location(draft.city, draft.country)
        draft.latitude = lat
        draft.longitude = lng

    try:
        draft.save()
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({
        'success': True,
        'draft_id': draft.pk,
        'saved_at': timezone.now().isoformat(),
    })


@login_required
def listing_create(request):
    step = int(request.GET.get('step', 1))
    resume_draft_id = _int_or_none(request.GET.get('draft'))

    # ─── 7-step flow pensijoj: gyvas tik Step 1 (kategorijų pikeris). ───
    # cars → quick, moto/trucks/boats turi savo flow. Bet koks 2–7 → atgal į pikerį.
    if step != 1 and not resume_draft_id:
        return redirect('/create/?step=1')

    # ─── BE-JS pasirinkimas ───
    # Pikerio nuorodos yra tikri <a href>, todėl išjungus JS galutinis
    # pasirinkimas ateina GET'u. Maršrutizavimas tas pats kaip POST šakoje.
    if request.method == 'GET' and request.user.is_authenticated:
        pick_sub_id = _int_or_none(request.GET.get('pick_sub'))
        pick_vt_id = _int_or_none(request.GET.get('pick_vt'))
        if pick_sub_id:
            sub = SubCategory.objects.filter(pk=pick_sub_id).first()
            if sub:
                routed = _route_category_pick(
                    request, sub.vehicle_type_id, str(sub.pk), sub.slug
                )
                if routed:
                    return routed
        elif pick_vt_id:
            routed = _route_category_pick(request, pick_vt_id, '', '')
            if routed:
                return routed

    if step == 1 and request.method == 'GET' and not request.GET.get('flow') and not resume_draft_id:
        if CARS_DRAFT_SESSION_KEY in request.session:
            request.session[CARS_DRAFT_SESSION_KEY] = None
        if 'active_moto_draft_id' in request.session:
            del request.session['active_moto_draft_id']
        if 'active_motogear_draft_id' in request.session:
            del request.session['active_motogear_draft_id']
        request.session.modified = True

    if resume_draft_id:
        try:
            existing_draft = Listing.objects.get(
                pk=resume_draft_id,
                seller=request.user,
                status='draft',
            )
            if existing_draft.subcategory and existing_draft.subcategory.slug in MOTO_GEAR_SLUGS:
                request.session['active_motogear_draft_id'] = existing_draft.pk
                request.session.modified = True
                return redirect('motogear_listing_create')
            if existing_draft.vehicle_type and existing_draft.vehicle_type.slug == 'motorcycles':
                request.session['active_moto_draft_id'] = existing_draft.pk
                request.session.modified = True
                return redirect('motorcycle_listing_create')
            if existing_draft.vehicle_type and existing_draft.vehicle_type.slug == 'trucks':
                request.session['active_trucks_draft_id'] = existing_draft.pk
                request.session.modified = True
                return redirect('trucks_listing_create')
            request.session[CARS_DRAFT_SESSION_KEY] = existing_draft.pk
            request.session.modified = True
            if 'step' not in request.GET:
                return redirect('/create/?step=2')
        except Listing.DoesNotExist:
            messages.error(request, 'Draft not found or already published.')
            return redirect('/create/')

    current_draft = None
    draft_id = request.session.get(CARS_DRAFT_SESSION_KEY)
    if draft_id:
        try:
            current_draft = Listing.objects.get(
                pk=draft_id,
                seller=request.user,
                status='draft',
            )
        except Listing.DoesNotExist:
            request.session[CARS_DRAFT_SESSION_KEY] = None
            current_draft = None

    listing_data = _draft_to_session_data(current_draft)

    if request.method == 'POST':
        if step == 1:
            vehicle_type_id = request.POST.get('vehicle_type')
            subcategory_id = request.POST.get('subcategory', '')

            subcategory_slug = ''
            if subcategory_id:
                try:
                    sub = SubCategory.objects.get(id=subcategory_id)
                    subcategory_slug = sub.slug
                except SubCategory.DoesNotExist:
                    pass

            if vehicle_type_id:
                routed = _route_category_pick(
                    request, vehicle_type_id, subcategory_id, subcategory_slug
                )
                if routed:
                    return routed

            form = Step1BasicInfoForm()

        elif step == 2:
            form = Step2MediaForm(request.POST, request.FILES)

            if not current_draft:
                messages.error(request, 'Draft not found, please start over.')
                return redirect('/create/?step=1')

            brand_id = _int_or_none(request.POST.get('brand'))
            model_id = _int_or_none(request.POST.get('model'))
            year = _int_or_none(request.POST.get('year'))
            month = _int_or_none(request.POST.get('month'))

            if brand_id:
                try:
                    current_draft.brand = Brand.objects.get(pk=brand_id)
                except Brand.DoesNotExist:
                    pass
            if model_id:
                try:
                    current_draft.model = Model.objects.get(pk=model_id)
                except Model.DoesNotExist:
                    pass
            if year:
                current_draft.year = year
            if year and month:
                try:
                    current_draft.first_registration = date(year=year, month=month, day=1)
                except (ValueError, TypeError):
                    pass

            current_draft.vin = request.POST.get('vin', '')

            if current_draft.brand and current_draft.year:
                title_parts = [current_draft.brand.name]
                if current_draft.model:
                    title_parts.append(current_draft.model.name)
                title_parts.append(str(current_draft.year))
                current_draft.title = ' '.join(title_parts)

            current_draft.video_url = request.POST.get('video_url', '')

            try:
                current_draft.save()
            except Exception as e:
                messages.error(request, f'Save failed: {e}')

            images, _image_errors = split_valid_images(
                request.FILES.getlist('images')
            )
            for _err in _image_errors:
                messages.error(request, _err)
            existing_count = current_draft.images.count()
            for i, image in enumerate(images[:10]):
                try:
                    ListingImage.objects.create(
                        listing=current_draft,
                        image=image,
                        is_main=(existing_count == 0 and i == 0),
                        order=existing_count + i,
                    )
                except Exception as e:
                    print(f"[create] image upload failed: {e}")

            return redirect('/create/?step=3')

        elif step == 3:
            if not current_draft:
                return redirect('/create/?step=1')

            brand_id = _int_or_none(request.POST.get('step3_brand'))
            model_id = _int_or_none(request.POST.get('step3_model'))
            year = _int_or_none(request.POST.get('step3_year'))
            month = _int_or_none(request.POST.get('step3_month'))

            if brand_id:
                try:
                    current_draft.brand = Brand.objects.get(pk=brand_id)
                except Brand.DoesNotExist:
                    pass
            if model_id:
                try:
                    current_draft.model = Model.objects.get(pk=model_id)
                except Model.DoesNotExist:
                    pass
            if year:
                current_draft.year = year
            if year and month:
                try:
                    current_draft.first_registration = date(year=year, month=month, day=1)
                except (ValueError, TypeError):
                    pass

            current_draft.body_type = request.POST.get('body_type', '')
            ft_id = _int_or_none(request.POST.get('fuel_type'))
            if ft_id:
                try:
                    current_draft.fuel_type = FuelType.objects.get(pk=ft_id)
                except FuelType.DoesNotExist:
                    pass
            tr_id = _int_or_none(request.POST.get('transmission'))
            if tr_id:
                try:
                    current_draft.transmission = Transmission.objects.get(pk=tr_id)
                except Transmission.DoesNotExist:
                    pass
            current_draft.doors = request.POST.get('doors', '')
            current_draft.condition = request.POST.get('condition', '')
            current_draft.color = request.POST.get('color', '')
            current_draft.defects = request.POST.get('defects', '')
            current_draft.steering = request.POST.get('steering', '')
            mileage_val = _int_or_none(request.POST.get('mileage'))
            if mileage_val is not None:
                current_draft.mileage = mileage_val
            current_draft.engine_capacity = _float_or_none(request.POST.get('engine_capacity'))
            current_draft.power = _int_or_none(request.POST.get('power'))
            current_draft.drive_type = request.POST.get('drive_type', '')
            current_draft.seats = request.POST.get('seats', '')
            current_draft.rim_size = request.POST.get('rim_size', '')
            current_draft.climate = request.POST.get('climate', '')
            current_draft.curb_weight = _int_or_none(request.POST.get('curb_weight'))
            current_draft.euro_standard = request.POST.get('euro_standard', '')
            current_draft.co2_emission = _int_or_none(request.POST.get('co2_emission'))
            current_draft.fuel_consumption_city = _float_or_none(request.POST.get('fuel_consumption_city'))
            current_draft.fuel_consumption_highway = _float_or_none(request.POST.get('fuel_consumption_highway'))
            current_draft.fuel_consumption_combined = _float_or_none(request.POST.get('fuel_consumption_combined'))
            current_draft.origin_country = request.POST.get('origin_country', '')
            current_draft.technical_inspection_month = _int_or_none(request.POST.get('technical_inspection_month'))
            current_draft.technical_inspection_year = _int_or_none(request.POST.get('technical_inspection_year'))

            if current_draft.brand and current_draft.year:
                title_parts = [current_draft.brand.name]
                if current_draft.model:
                    title_parts.append(current_draft.model.name)
                title_parts.append(str(current_draft.year))
                current_draft.title = ' '.join(title_parts)

            try:
                current_draft.save()
            except Exception as e:
                messages.error(request, f'Save failed: {e}')

            if request.POST.get('go_back'):
                return redirect('/create/?step=2')

            errors = []
            if not current_draft.brand:
                errors.append('Brand is required')
            if not current_draft.model:
                errors.append('Model is required')
            if not current_draft.year:
                errors.append('Year is required')
            if not current_draft.first_registration:
                errors.append('Month is required')
            if not current_draft.body_type:
                errors.append('Body type is required')
            if not current_draft.fuel_type:
                errors.append('Fuel type is required')
            if not current_draft.transmission:
                errors.append('Transmission is required')
            if not current_draft.doors:
                errors.append('Doors is required')
            if not current_draft.mileage:
                errors.append('Mileage is required')

            if errors:
                form = Step3VehicleDataForm(request.POST)
                listing_data = _draft_to_session_data(current_draft)
            else:
                return redirect('/create/?step=4')

        elif step == 4:
            if not current_draft:
                return redirect('/create/?step=1')

            equipment_ids = request.POST.getlist('equipment')
            ListingEquipment.objects.filter(listing=current_draft).delete()
            for eid in equipment_ids:
                try:
                    ListingEquipment.objects.create(
                        listing=current_draft,
                        equipment_id=int(eid),
                    )
                except (ValueError, Equipment.DoesNotExist):
                    pass

            return redirect('/create/?step=5')

        elif step == 5:
            if not current_draft:
                return redirect('/create/?step=1')

            form = Step5PriceForm(request.POST)
            if form.is_valid():
                current_draft.price = form.cleaned_data['price']
                current_draft.negotiable = form.cleaned_data.get('negotiable', False)
                current_draft.save(update_fields=['price', 'negotiable'])
                return redirect('/create/?step=6')

        elif step == 6:
            if not current_draft:
                return redirect('/create/?step=1')

            form = Step6DescriptionForm(request.POST)
            if form.is_valid():
                current_draft.description = form.cleaned_data.get('description', '')
                current_draft.save(update_fields=['description'])
                return redirect('/create/?step=7')

        elif step == 7:
            if not current_draft:
                return redirect('/create/?step=1')

            form = Step7ContactForm(request.POST)
            phone_val = request.POST.get('phone', '').strip()
            agree_terms_val = request.POST.get('agree_terms')
            extra_errors = []
            if not phone_val:
                extra_errors.append('phone: This field is required.')
            if not agree_terms_val:
                extra_errors.append('agree_terms: You must agree to the terms.')

            if form.is_valid() and not extra_errors:
                if phone_val and hasattr(request.user, 'profile'):
                    request.user.profile.phone_number = phone_val
                    request.user.profile.save(update_fields=['phone_number'])

                current_draft.country = form.cleaned_data['country']
                current_draft.city = form.cleaned_data.get('city', '') or '—'
                if hasattr(current_draft, 'state'):
                    current_draft.state = request.POST.get('state', '') if current_draft.country == 'US' else ''
                current_draft.postal_code = form.cleaned_data.get('postal_code', '')
                current_draft.address = form.cleaned_data.get('address', '')
                current_draft.hide_exact_address = form.cleaned_data.get('hide_exact_address', False)

                lat, lng = get_coordinates_for_location(current_draft.city, current_draft.country)
                current_draft.latitude = lat
                current_draft.longitude = lng

                current_draft.activate(days=Listing.DEFAULT_ACTIVE_DAYS)

                _send_listing_published_email(current_draft, request.user)

                request.session[CARS_DRAFT_SESSION_KEY] = None
                request.session.modified = True

                return redirect(
                    reverse('listing_success', kwargs={'pk': current_draft.pk}) + '?action=published'
                )

    else:
        if step == 1:
            form = Step1BasicInfoForm()
        elif step == 2:
            initial = {}
            if current_draft and current_draft.video_url:
                initial['video_url'] = current_draft.video_url
            form = Step2MediaForm(initial=initial)
        elif step == 3:
            initial_data = {}
            if current_draft:
                initial_data = {
                    'body_type': current_draft.body_type,
                    'fuel_type': current_draft.fuel_type,
                    'transmission': current_draft.transmission,
                    'doors': current_draft.doors,
                    'condition': current_draft.condition,
                    'color': current_draft.color,
                    'defects': current_draft.defects,
                    'steering': current_draft.steering,
                    'mileage': current_draft.mileage,
                    'engine_capacity': current_draft.engine_capacity,
                    'power': current_draft.power,
                    'drive_type': current_draft.drive_type,
                    'seats': current_draft.seats,
                    'rim_size': current_draft.rim_size,
                    'climate': current_draft.climate,
                }
            form = Step3VehicleDataForm(initial=initial_data)
        elif step == 4:
            initial = {}
            if current_draft:
                initial['equipment'] = list(current_draft.equipment_items.values_list('equipment_id', flat=True))
            form = Step4EquipmentForm(initial=initial)
        elif step == 5:
            initial = {}
            if current_draft and current_draft.price > 0:
                initial = {'price': current_draft.price, 'negotiable': current_draft.negotiable}
            form = Step5PriceForm(initial=initial)
        elif step == 6:
            initial = {}
            if current_draft:
                initial = {'description': current_draft.description}
            form = Step6DescriptionForm(initial=initial)
        elif step == 7:
            user_phone = ''
            if hasattr(request.user, 'profile') and request.user.profile.phone_number:
                user_phone = request.user.profile.phone_number

            initial = {}
            if current_draft:
                initial = {
                    'country': current_draft.country or 'US',
                    'city': current_draft.city if current_draft.city != '—' else '',
                    'postal_code': current_draft.postal_code,
                    'address': current_draft.address,
                    'hide_exact_address': current_draft.hide_exact_address,
                    'phone': user_phone,
                    'email': request.user.email,
                    'agree_terms': False,
                }
            form = Step7ContactForm(initial=initial)
        else:
            return redirect('/create/?step=1')

    progress_percent = int((step / 7) * 100)
    brand_name = current_draft.brand.name if (current_draft and current_draft.brand) else ''
    model_name = current_draft.model.name if (current_draft and current_draft.model) else ''
    year_val = current_draft.year if current_draft else ''

    country_choices = list(Listing.COUNTRY_CHOICES)

    completed_steps = _draft_completed_steps(current_draft)
    if step in (1, 2, 3, 4, 5, 6, 7):
        completed_steps.add(step)

    step_labels = [
        (1, 'Basic'), (2, 'Media'), (3, 'Details'), (4, 'Equipment'),
        (5, 'Price'), (6, 'Description'), (7, 'Contact'),
    ]

    context = {
        'form': form,
        'step': step,
        'total_steps': 7,
        'progress_percent': progress_percent,
        'listing_data': listing_data,
        'temp_images_count': current_draft.images.count() if current_draft else 0,
        'vehicle_types': _get_picker_vehicle_types(request.user),
        'picker_tree': _build_picker_tree(request.user),
        'picker_active_vt': request.GET.get('vt', ''),
        'picker_active_sub': request.GET.get('sub', ''),
        'brands': Brand.objects.all().order_by('name'),
        'years': list(range(timezone.now().year + 1, 1949, -1)),
        'step1_brand': brand_name,
        'step1_model': model_name,
        'step1_year': year_val,
        'country_choices': country_choices,
        'us_states': Listing.US_STATE_CHOICES,
        'completed_steps': completed_steps,
        'step_labels': step_labels,
        'current_draft': current_draft,
        'draft_id': current_draft.pk if current_draft else None,
    }
    return render(request, 'listings/listing_create.html', context)


@login_required
def listing_delete(request, pk):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user)

    if request.method == 'POST':
        mark_sold = request.POST.get('mark_sold') == 'yes'
        display_sold = request.POST.get('display_sold') == 'yes'

        if mark_sold:
            SalesRecord.create_from_listing(listing, marked_sold=display_sold)
            _send_listing_sold_confirmation_email(listing, request.user, display_sold)
            _send_saved_listing_sold_emails(listing)

            if display_sold:
                listing.mark_as_sold()
                return redirect('my_listings')
            else:
                listing.delete()
                return redirect('my_listings')
        else:
            listing.delete()
            return redirect('my_listings')

    context = {'listing': listing}
    return render(request, 'listings/listing_delete_confirm.html', context)


@login_required
def listing_boost_all(request):
    if request.method != 'POST':
        return redirect('my_listings')

    now = timezone.now()
    rate_limit_cutoff = now - timedelta(hours=RENEW_RATE_LIMIT_HOURS)
    single_id = request.POST.get('single_listing_id')

    qs = Listing.objects.filter(
        seller=request.user,
        status='active',
        is_shadow_banned=False,
    )

    if single_id:
        qs = qs.filter(pk=single_id)

    eligible = qs.filter(
        Q(last_boosted_at__isnull=True) | Q(last_boosted_at__lt=rate_limit_cutoff)
    )

    eligible_count = eligible.count()
    total_active = qs.count()
    skipped = total_active - eligible_count

    if eligible_count == 0:
        if single_id:
            messages.info(
                request,
                f'Already renewed recently. Wait up to {RENEW_RATE_LIMIT_HOURS} hour before next renew.'
            )
        else:
            messages.info(
                request,
                f'All listings already renewed recently. Wait up to {RENEW_RATE_LIMIT_HOURS} hour.'
            )
        return redirect('my_listings')

    eligible.update(last_boosted_at=now)
    return redirect('my_listings')


@login_required
def saved_listings(request):
    saved = SavedListing.objects.filter(user=request.user).select_related('listing')
    context = {'saved_listings': saved}
    return render(request, 'listings/saved_listings.html', context)


def save_listing(request, pk):
    if not request.user.is_authenticated:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': 'login_required'}, status=401)
        return redirect('accounts:login')

    listing = get_object_or_404(Listing, pk=pk)
    saved, created = SavedListing.objects.get_or_create(
        user=request.user,
        listing=listing
    )
    if not created:
        saved.delete()
        is_saved = False
    else:
        is_saved = True
        if request.user != listing.seller:
            from .models import SavedListingNotification
            _notif, notif_created = SavedListingNotification.objects.get_or_create(
                user=request.user,
                listing=listing,
            )
            if notif_created:
                _send_listing_saved_by_users_email(listing, request.user)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'saved': is_saved})

    next_page = request.META.get('HTTP_REFERER', '/')
    return redirect(next_page)


@login_required
def contact_seller(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if request.method == 'POST':
        sender_email = request.POST.get('sender_email')
        sender_phone = request.POST.get('sender_phone', '')
        message = request.POST.get('message')
        subject = f'Inquiry about: {listing.title}'
        body = f"""Someone is interested in your listing: {listing.title}

From: {sender_email}
Phone: {sender_phone}

Message:
{message}

View listing: http://127.0.0.1:8000{listing.get_absolute_url()}"""
        send_mail(
            subject, body, sender_email, [listing.seller.email],
            fail_silently=True,
        )
    return redirect('listing_detail', pk=listing.pk)


def report_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('reason', '')
        comment = request.POST.get('comment', '')
        reporter_email = request.POST.get('reporter_email', '')
        listing_url = request.build_absolute_uri(f'/listings/{listing.pk}/')
        subject = f'[REPORT] Listing #{listing.pk}: {listing.title}'
        body = f"""A listing has been reported on SellCar.

Listing: {listing.title}
Listing ID: #{listing.pk}
URL: {listing_url}

Reason: {reason}
Comment: {comment}
Reporter email: {reporter_email if reporter_email else 'Not provided'}
Seller: {listing.seller.email}
"""
        send_mail(subject, body, 'noreply@sellcar.com',
                  ['helpautoinfo@gmail.com'], fail_silently=True)
    return redirect('listing_detail', pk=listing.pk)


def search_map(request):
    listings = _public_listings_qs(request.user).select_related('brand', 'model')
    makes = Brand.objects.values_list('name', flat=True).distinct().order_by('name')
    models_list = Model.objects.values_list('name', flat=True).distinct().order_by('name')
    current_year = timezone.now().year
    years = list(range(current_year + 1, 1989, -1))

    make = request.GET.get('make')
    model = request.GET.get('model')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    year_min = request.GET.get('year_min')
    year_max = request.GET.get('year_max')
    fuel_type = request.GET.get('fuel_type')
    transmission = request.GET.get('transmission')

    if make:
        listings = listings.filter(brand__name=make)
    if model:
        listings = listings.filter(model__name=model)
    if price_min:
        listings = listings.filter(price__gte=price_min)
    if price_max:
        listings = listings.filter(price__lte=price_max)
    if year_min:
        listings = listings.filter(year__gte=year_min)
    if year_max:
        listings = listings.filter(year__lte=year_max)
    if fuel_type:
        listings = listings.filter(fuel_type__name__iexact=fuel_type)
    if transmission:
        listings = listings.filter(transmission__name__iexact=transmission)

    listings_all = list(listings[:60])
    _track_listing_impressions(request, listings_all)

    listings_json = []
    for listing in listings_all:
        main_image = None
        first_image = listing.images.first()
        if first_image:
            main_image = first_image.image.url
        if listing.latitude and listing.longitude:
            lat = float(listing.latitude)
            lng = float(listing.longitude)
        else:
            lat, lng = get_coordinates_for_location(listing.city, listing.country)
        listings_json.append({
            'id': listing.pk,
            'title': listing.title,
            'slug': listing.pk,
            'year': listing.year,
            'mileage': listing.mileage,
            'price': float(listing.price),
            'latitude': lat,
            'longitude': lng,
            'main_image': main_image,
            'city': listing.city,
            'country': listing.get_country_display_name() if hasattr(listing, 'get_country_display_name') else listing.country,
        })

    context = {
        'listings': listings_all,
        'listings_json': json.dumps(listings_json),
        'makes': makes,
        'models': models_list,
        'years': years,
        'GOOGLE_MAPS_API_KEY': getattr(settings, 'GOOGLE_MAPS_API_KEY', ''),
    }
    return render(request, 'listings/search_map.html', context)


# ════════════════════════════════════════════════════════════════════
# EDIT VIEWS — visi turi Cars redirect į /create/cars/quick/?edit=<pk>
# ════════════════════════════════════════════════════════════════════

@login_required
def listing_edit(request, pk):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user)

    # ✅ Trucks → atskiras edit puslapis (autoplius 8x4 layout)
    if listing.vehicle_type and listing.vehicle_type.slug == 'trucks':
        return redirect('trucks_listing_edit', pk=pk)

    # ✅ Cars → Quick edit (single-page form, /create/cars/quick/?edit=<pk>)
    if listing.vehicle_type and listing.vehicle_type.slug == 'cars':
        return redirect(f'/create/cars/quick/?edit={pk}')
    if listing.vehicle_type and listing.vehicle_type.slug == 'boats':
        return redirect(f'/create/boats/?edit={pk}')
    if listing.vehicle_type and listing.vehicle_type.slug == 'trailers':
        return redirect(f'/create/trailers/?edit={pk}')
    if listing.vehicle_type and listing.vehicle_type.slug == 'agriculture':
        return redirect(f'/create/agriculture/?edit={pk}')
    if listing.vehicle_type and listing.vehicle_type.slug == 'forestry':
        return redirect(f'/create/forestry/?edit={pk}')
    if listing.vehicle_type and listing.vehicle_type.slug == 'camping-houses':
        return redirect(f'/create/camping-houses/?edit={pk}')
    if listing.vehicle_type and listing.vehicle_type.slug == 'services':
        return redirect(f'/create/services/?edit={pk}')
    if listing.vehicle_type and listing.vehicle_type.slug == 'electronics':
        return redirect(f'/create/electronics/?edit={pk}')
    if listing.vehicle_type and listing.vehicle_type.slug == 'bicycles':
        return redirect(f'/create/bicycles/?edit={pk}')
    if listing.vehicle_type and listing.vehicle_type.slug == 'rental':
        _sub = listing.subcategory.slug if listing.subcategory else ''
        return redirect(
            f'/create/rental/{RENTAL_SUB_TO_FORM.get(_sub, "car")}/?edit={pk}')
    if listing.vehicle_type and listing.vehicle_type.slug == 'loading-equipment':
        return redirect(f'/create/loading-equipment/?edit={pk}')
    if listing.vehicle_type and listing.vehicle_type.slug == 'construction':
        if listing.constr_attach_type or (
                listing.subcategory and listing.subcategory.slug == 'construction-attachments'):
            return redirect(f'/create/construction/attachment/?edit={pk}')
        return redirect(f'/create/construction/?edit={pk}')
    # „Visas X dalimis" turi savo vienpuslapes formas ir TURI būti tikrinamos
    # PRIEŠ bendrą parts šaką — kitaip jos atsidarydavo bendroje dalies
    # formoje, kuri tų laukų nemoka.
    if listing.subcategory and listing.subcategory.slug == 'whole-car-for-parts':
        return redirect('car_for_parts_edit', pk=pk)
    if listing.subcategory and listing.subcategory.slug == 'whole-moto-for-parts':
        return redirect('moto_for_parts_edit', pk=pk)
    if listing.subcategory and listing.subcategory.slug == 'whole-truck-for-parts':
        return redirect('truck_for_parts_edit', pk=pk)
    if listing.vehicle_type and listing.vehicle_type.slug == 'parts':
        return redirect(f'/create/parts/form/?edit={pk}')
    # Moto gear sits under the motorcycles vehicle type — check it first, or
    # gear listings open the motorcycle form.
    if listing.subcategory and listing.subcategory.slug in MOTO_GEAR_SLUGS:
        return redirect(f'/create/motogear/?edit={pk}')
    if listing.vehicle_type and listing.vehicle_type.slug == 'motorcycles':
        return redirect(f'/create/motorcycle/?edit={pk}')

    if request.method == 'POST':
        _old_price = listing.price

        listing.price = request.POST.get('price', listing.price)
        listing.description = request.POST.get('description', listing.description)
        listing.mileage = request.POST.get('mileage', listing.mileage)
        listing.color = request.POST.get('color', listing.color)
        listing.defects = request.POST.get('defects', listing.defects)
        listing.steering = request.POST.get('steering', listing.steering)
        listing.drive_type = request.POST.get('drive_type', listing.drive_type)
        listing.seats = request.POST.get('seats', listing.seats)
        listing.rim_size = request.POST.get('rim_size', listing.rim_size)
        listing.climate = request.POST.get('climate', listing.climate)
        listing.euro_standard = request.POST.get('euro_standard', listing.euro_standard)
        listing.origin_country = request.POST.get('origin_country', listing.origin_country)
        curb_weight = request.POST.get('curb_weight', '')
        listing.curb_weight = int(curb_weight) if curb_weight else None
        co2 = request.POST.get('co2_emission', '')
        listing.co2_emission = int(co2) if co2 else None
        fc_city = request.POST.get('fuel_consumption_city', '')
        listing.fuel_consumption_city = float(fc_city) if fc_city else None
        fc_hw = request.POST.get('fuel_consumption_highway', '')
        listing.fuel_consumption_highway = float(fc_hw) if fc_hw else None
        fc_comb = request.POST.get('fuel_consumption_combined', '')
        listing.fuel_consumption_combined = float(fc_comb) if fc_comb else None
        ti_month = request.POST.get('technical_inspection_month', '')
        listing.technical_inspection_month = int(ti_month) if ti_month else None
        ti_year = request.POST.get('technical_inspection_year', '')
        listing.technical_inspection_year = int(ti_year) if ti_year else None
        listing.negotiable = request.POST.get('negotiable') == 'on'

        listing.vin = request.POST.get('vin', '').strip().upper()

        listing.save()

        try:
            new_price = float(listing.price)
            old_price = float(_old_price) if _old_price else 0
            if new_price != old_price and old_price > 0:
                if new_price < old_price:
                    _send_saved_listing_price_drop_emails(listing, old_price, new_price)
                else:
                    summary = f'Price changed from {listing.currency_symbol}{int(old_price)} to {listing.currency_symbol}{int(new_price)}'
                    _send_saved_listing_updated_emails(listing, summary)
        except (ValueError, TypeError):
            pass

        images, _image_errors = split_valid_images(request.FILES.getlist('images'))
        for _err in _image_errors:
            messages.error(request, _err)
        for i, image in enumerate(images):
            ListingImage.objects.create(
                listing=listing, image=image, is_main=False,
                order=listing.images.count() + i
            )

        return redirect('listing_detail', pk=listing.pk)
    context = {
        'listing': listing,
        'GOOGLE_MAPS_API_KEY': getattr(settings, 'GOOGLE_MAPS_API_KEY', ''),
    }
    return render(request, 'listings/listing_edit.html', context)


@login_required
def image_delete(request, pk):
    image = get_object_or_404(ListingImage, pk=pk, listing__seller=request.user)
    listing_pk = image.listing.pk
    if request.method == 'POST':
        image.delete()
        return redirect('listing_edit_step', pk=listing_pk, step=2)
    return redirect('listing_edit_step', pk=listing_pk, step=2)


@login_required
def image_set_main(request, pk):
    image = get_object_or_404(ListingImage, pk=pk, listing__seller=request.user)
    listing_pk = image.listing.pk

    if request.method == 'POST':
        ListingImage.objects.filter(listing=image.listing).update(is_main=False)
        image.is_main = True
        image.save(update_fields=['is_main'])

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'image_id': image.pk})

    return redirect('listing_edit_step', pk=listing_pk, step=2)


def get_subcategories_ajax(request):
    from .models import SubCategory
    from django.utils.translation import gettext

    vehicle_type_id = request.GET.get('vehicle_type_id')
    vehicle_type_slug = request.GET.get('vehicle_type_slug')
    parent_id = request.GET.get('parent_id')
    parent_slug = request.GET.get('parent_slug')
    top_only = request.GET.get('top_only') in ('1', 'true', 'yes')

    qs = SubCategory.objects.all()

    if vehicle_type_slug:
        qs = qs.filter(vehicle_type__slug=vehicle_type_slug)
    elif vehicle_type_id:
        qs = qs.filter(vehicle_type_id=vehicle_type_id)
    else:
        return JsonResponse([], safe=False)

    if parent_id:
        qs = qs.filter(parent_id=parent_id)
    elif parent_slug:
        qs = qs.filter(parent__slug=parent_slug)
    elif top_only:
        qs = qs.filter(parent__isnull=True)

    qs = qs.order_by('order', 'name')

    # ?picker=1 — tik create pikeriui: apkarpo iki etaloninio medžio ir
    # išrikiuoja PICKER_SUBCATEGORY_SLUGS tvarka. Naršymo/paieškos puslapiai
    # šito parametro nesiunčia ir toliau gauna VISAS subkategorijas.
    if request.GET.get('picker') in ('1', 'true', 'yes') and top_only:
        vt_slug = vehicle_type_slug
        if not vt_slug and vehicle_type_id:
            vt_slug = (
                VehicleType.objects.filter(pk=vehicle_type_id)
                .values_list('slug', flat=True).first()
            )
        allowed = _picker_subcategory_slugs(vt_slug)
        if allowed is not None:
            by_slug = {s.slug: s for s in qs}
            qs = [by_slug[slug] for slug in allowed if slug in by_slug]

    data = [
        {
            'id': s.id,
            'name': gettext(s.name),
            'slug': s.slug,
            'has_children': s.children.exists(),
            'implemented': s.slug not in UNIMPLEMENTED_SUBCATEGORY_SLUGS,
        }
        for s in qs
    ]
    return JsonResponse(data, safe=False)


def get_models_ajax(request):
    brand_id = request.GET.get('brand_id')
    if brand_id:
        from django.db.models.functions import Lower
        models_qs = Model.objects.filter(brand_id=brand_id).order_by(Lower('name'))
        data = []
        for m in models_qs:
            model_count = Listing.objects.filter(
                model=m, status='active', is_shadow_banned=False
            ).count()
            data.append({'id': m.id, 'name': m.name, 'count': model_count,
                        'type': 'model', 'model_id': m.id, 'submodel_id': None})
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)


def get_submodels_ajax(request):
    model_id = request.GET.get('model_id')
    if model_id:
        submodels = SubModel.objects.filter(model_id=model_id).values('id', 'name').order_by('name')
        return JsonResponse(list(submodels), safe=False)
    return JsonResponse([], safe=False)


def get_models_by_brand(request):
    brand_id = request.GET.get('brand_id')
    make = request.GET.get('make')
    if brand_id:
        models = Model.objects.filter(brand_id=brand_id).values('id', 'name').order_by('name')
        return JsonResponse(list(models), safe=False)
    elif make:
        models = Model.objects.filter(brand__name=make).values('id', 'name').order_by('name')
        return JsonResponse({'models': list(models)})
    return JsonResponse({'models': []})


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        send_mail(
            f'[SellCar Contact] {subject}',
            f'From: {name} <{email}>\n\n{message}',
            email, ['helpautoinfo@gmail.com'], fail_silently=True,
        )
        return redirect('contact')
    return render(request, 'listings/contact.html')


def faq(request):
    """Frequently Asked Questions page."""
    return render(request, 'faq.html')


@login_required
def save_search(request):
    if request.method == 'POST':
        from .models import SavedSearch
        params = {k: v for k, v in request.POST.items() if k != 'csrfmiddlewaretoken' and v}

        name = _build_search_name(params)

        saved = SavedSearch.objects.create(user=request.user, name=name, query_params=params)
        return JsonResponse({'success': True, 'id': saved.pk})
    return JsonResponse({'success': False})


def _build_search_name(params):
    """Auto-generate human-readable name from search filters."""
    parts = []

    # Category
    cat = params.get('category')
    if cat and cat != 'cars':
        parts.append(cat.replace('-', ' ').title())

    # Brand + Model
    brand_id = params.get('brand')
    if brand_id:
        try:
            brand = Brand.objects.get(id=brand_id)
            parts.append(brand.name)
        except Brand.DoesNotExist:
            pass

    model_id = params.get('model')
    if model_id:
        try:
            model = Model.objects.get(id=model_id)
            parts.append(model.name)
        except Model.DoesNotExist:
            pass

    # Year range
    year_min = params.get('year_min')
    year_max = params.get('year_max')
    if year_min and year_max:
        parts.append(f"{year_min}-{year_max}")
    elif year_min:
        parts.append(f"from {year_min}")
    elif year_max:
        parts.append(f"till {year_max}")

    # Price range
    price_min = params.get('price_min')
    price_max = params.get('price_max')
    if price_min and price_max:
        parts.append(f"${price_min}-${price_max}")
    elif price_max:
        parts.append(f"up to ${price_max}")
    elif price_min:
        parts.append(f"from ${price_min}")

    # Fuel type
    fuel_id = params.get('fuel_type')
    if fuel_id:
        try:
            ft = FuelType.objects.get(id=fuel_id)
            parts.append(ft.name)
        except FuelType.DoesNotExist:
            pass

    # Transmission
    tr_id = params.get('transmission')
    if tr_id:
        try:
            tr = Transmission.objects.get(id=tr_id)
            parts.append(tr.name)
        except Transmission.DoesNotExist:
            pass

    # Body type
    body = params.get('body_type')
    if body:
        parts.append(body.replace('-', ' ').title())

    # Mileage max
    mileage_max = params.get('mileage_max')
    if mileage_max:
        parts.append(f"max {mileage_max} mi")

    # Location
    state = params.get('state_filter')
    country = params.get('country_filter')
    city = params.get('city')
    if state:
        parts.append(state)
    elif country and country != 'US':
        parts.append(country)
    if city:
        parts.append(city)

    # Free text
    search_q = params.get('search') or params.get('q')
    if search_q:
        parts.append(f'"{search_q}"')

    return ', '.join(parts) if parts else 'All listings'


@login_required
def delete_search(request, pk):
    from .models import SavedSearch
    SavedSearch.objects.filter(pk=pk, user=request.user).delete()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})

    return redirect('saved_searches_list')


def home(request):
    return listing_list(request)


@login_required
def toggle_search_notify(request, pk):
    from .models import SavedSearch
    search = get_object_or_404(SavedSearch, pk=pk, user=request.user)
    search.notify_email = not search.notify_email
    search.save()
    return redirect('saved_searches_list')


@login_required
def mark_search_viewed(request, pk):
    from .models import SavedSearch
    search = get_object_or_404(SavedSearch, pk=pk, user=request.user)
    search.last_viewed_at = timezone.now()
    search.save(update_fields=['last_viewed_at'])
    return JsonResponse({'success': True})


@login_required
def duplicate_search(request, pk):
    from .models import SavedSearch
    search = get_object_or_404(SavedSearch, pk=pk, user=request.user)
    SavedSearch.objects.create(
        user=request.user, name=f"{search.name} (copy)",
        query_params=search.query_params, notify_email=False
    )
    return redirect('saved_searches_list')


@login_required
def save_step3_data(request):
    return save_cars_draft_ajax(request)


@login_required
def saved_searches_list(request):
    from .models import SavedSearch

    searches = SavedSearch.objects.filter(user=request.user)

    searches_with_counts = []
    for search in searches:
        params = search.query_params
        qs = Listing.objects.filter(status='active', is_shadow_banned=False)
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
        if params.get('state_filter'):
            qs = qs.filter(country='US', state=params['state_filter'])
        elif params.get('country_filter'):
            qs = qs.filter(country=params['country_filter'])

        if search.last_viewed_at:
            new_count = qs.filter(created_at__gt=search.last_viewed_at).count()
        else:
            new_count = qs.count()

        search.new_count = new_count
        searches_with_counts.append(search)

    return render(request, 'listings/saved_searches.html', {'searches': searches_with_counts})


def advanced_search_count_ajax(request):
    """AJAX endpoint — grąžina tik count'ą filtruotų listings.
    Naudoja TĄ PAČIĄ filter logiką kaip advanced_search."""
    from django.db.models import Q

    if request.GET.get('category') == 'motorcycles':
        from . import motorcycles_views
        # Motorcycles turi savo count — naudoja kitą lentelę
        try:
            return JsonResponse({'count': motorcycles_views.motorcycles_count_ajax(request).get('count', 0)})
        except Exception:
            return JsonResponse({'count': 0})

    listings = _public_listings_qs(request.user)


    f = request.GET
    category_filter = f.get('category', '')
    if category_filter:
        listings = listings.filter(vehicle_type__slug=category_filter)

    search_query = f.get('search', '')
    if search_query:
        listings = listings.filter(title__icontains=search_query)

    part_query = f.get('part_query', '').strip()
    if part_query:
        listings = listings.filter(
            Q(title__icontains=part_query) | Q(description__icontains=part_query)
        )

    pairs = request.GET.getlist('pair')
    if pairs:
        q = Q()
        for pair in pairs:
            parts = pair.split('|')
            if len(parts) == 4:
                bid, bname, mid, mname = parts
                if mid:
                    q |= Q(brand_id=bid, model_id=mid)
                else:
                    q |= Q(brand_id=bid)
        if q:
            listings = listings.filter(q)
    else:
        brand_filter = f.get('brand', '')
        model_filter = f.get('model', '')
        if brand_filter:
            listings = listings.filter(brand_id=brand_filter)
            if model_filter:
                listings = listings.filter(model_id=model_filter)

    if f.get('price_min'): listings = listings.filter(price__gte=f.get('price_min'))
    if f.get('price_max'): listings = listings.filter(price__lte=f.get('price_max'))
    if f.get('year_min'): listings = listings.filter(year__gte=f.get('year_min'))
    if f.get('year_max'): listings = listings.filter(year__lte=f.get('year_max'))
    if f.get('mileage_min'): listings = listings.filter(mileage__gte=f.get('mileage_min'))
    if f.get('mileage_max'): listings = listings.filter(mileage__lte=f.get('mileage_max'))
    if f.get('fuel_type'): listings = listings.filter(fuel_type_id=f.get('fuel_type'))

    body_type_filter = [v for v in f.getlist('body_type') if v]
    if body_type_filter:
        listings = listings.filter(body_type__in=body_type_filter)

    if f.get('color'): listings = listings.filter(color=f.get('color'))
    if f.get('doors'): listings = listings.filter(doors=f.get('doors'))
    if f.get('condition'): listings = listings.filter(condition=f.get('condition'))
    if f.get('drive_type'): listings = listings.filter(drive_type=f.get('drive_type'))
    if f.get('seats'): listings = listings.filter(seats=f.get('seats'))
    if f.get('euro_standard'): listings = listings.filter(euro_standard=f.get('euro_standard'))
    if f.get('power_min'): listings = listings.filter(power__gte=f.get('power_min'))
    if f.get('power_max'): listings = listings.filter(power__lte=f.get('power_max'))
    if f.get('engine_min'): listings = listings.filter(engine_capacity__gte=f.get('engine_min'))
    if f.get('engine_max'): listings = listings.filter(engine_capacity__lte=f.get('engine_max'))
    if f.get('climate'): listings = listings.filter(climate=f.get('climate'))
    if f.get('steering'): listings = listings.filter(steering=f.get('steering'))
    if f.get('defects'): listings = listings.filter(defects=f.get('defects'))

    state_filter = f.get('state_filter', '')
    country_filter = f.get('country_filter', '')
    if state_filter:
        listings = listings.filter(country='US', state=state_filter)
    elif country_filter:
        listings = listings.filter(country=country_filter)

    city_filter_param = f.get('city_filter', '')
    if city_filter_param:
        listings = listings.filter(city__iexact=city_filter_param)

    equipment_ids = f.getlist('equipment')
    if equipment_ids:
        for eid in equipment_ids:
            listings = listings.filter(equipment_items__equipment_id=eid)

    return JsonResponse({'count': listings.count()})


def advanced_search(request):
    from django.db.models import Q
    from itertools import groupby

    if request.GET.get('category') == 'motorcycles':
        from . import motorcycles_views
        return motorcycles_views.motorcycles_advanced_search(request)

    if request.GET.get('category') == 'moto-gear':
        from . import motogear_views
        return motogear_views.motogear_list(request)

    # ═══ TYRES & WHEELS → atskira WheelListing lentelė ═══
    if request.GET.get('category') in ('tires', 'wheels'):
        wheel_type = 'tyre'
        subcategory_id = request.GET.get('subcategory')
        if subcategory_id:
            try:
                sub = SubCategory.objects.get(id=subcategory_id)
                if 'rim' in sub.slug.lower() or 'ratlank' in sub.name.lower() or 'rim' in sub.name.lower():
                    wheel_type = 'rim'
            except SubCategory.DoesNotExist:
                pass
        return redirect(f'/browse/wheels/?type={wheel_type}')

    # ═══ TYRES & WHEELS → atskira WheelListing lentelė ═══
    if request.GET.get('category') in ('tires', 'wheels'):
        wheel_type = 'tyre'
        subcategory_id = request.GET.get('subcategory')
        if subcategory_id:
            try:
                sub = SubCategory.objects.get(id=subcategory_id)
                if 'rim' in sub.slug.lower() or 'ratlank' in sub.name.lower() or 'rim' in sub.name.lower():
                    wheel_type = 'rim'
            except SubCategory.DoesNotExist:
                pass
        return redirect(f'/browse/wheels/?type={wheel_type}')

    if request.GET.get('category') == 'trucks':
            from . import trucks_views
            return trucks_views.trucks_list(request)

    if request.GET.get('category') in ('tires', 'wheels'):
        return redirect('/search/wheels/advanced/')

    if request.GET.get('category') in ('tires', 'wheels'):
        return redirect('/search/wheels/advanced/')

    listings = _public_listings_qs(request.user).select_related(
        'brand', 'model', 'fuel_type', 'transmission', 'vehicle_type'
    )

    current_year = timezone.now().year
    years = list(range(current_year + 1, 1949, -1))
    fuel_types = FuelType.objects.all().order_by('name')
    transmissions = Transmission.objects.all().order_by('name')
    brands = Brand.objects.all().order_by('name')

    if request.GET.get('brand') and not request.GET.getlist('pair'):
        try:
            brand_obj = Brand.objects.get(id=request.GET.get('brand'))
            model_id = request.GET.get('model', '')
            model_name = ''
            if model_id:
                model_name = Model.objects.get(id=model_id).name
            pair = f"{brand_obj.id}|{brand_obj.name}|{model_id}|{model_name}"
            return redirect(f"/search/advanced/?pair={pair}")
        except:
            pass

    f = request.GET
    category_filter = f.get('category', '')
    brand_filter = f.get('brand', '')
    model_filter = f.get('model', '')
    price_min = f.get('price_min', '')
    price_max = f.get('price_max', '')
    year_min = f.get('year_min', '')
    year_max = f.get('year_max', '')
    mileage_min = f.get('mileage_min', '')
    mileage_max = f.get('mileage_max', '')
    fuel_type_filter = f.get('fuel_type', '')
    transmission_filter = f.get('transmission', '')
    body_type_filter = f.get('body_type', '')
    color_filter = f.get('color', '')
    doors_filter = f.get('doors', '')
    condition_filter = f.get('condition', '')
    drive_type_filter = f.get('drive_type', '')
    seats_filter = f.get('seats', '')
    euro_standard_filter = f.get('euro_standard', '')
    power_min = f.get('power_min', '')
    power_max = f.get('power_max', '')
    engine_min = f.get('engine_min', '')
    engine_max = f.get('engine_max', '')
    climate_filter = f.get('climate', '')
    steering_filter = f.get('steering', '')
    defects_filter = f.get('defects', '')
    state_filter = f.get('state_filter', '')
    country_filter = f.get('country_filter', '')
    search_query = f.get('search', '')
    equipment_ids = f.getlist('equipment')

    if category_filter:
        listings = listings.filter(vehicle_type__slug=category_filter)
    if search_query:
        listings = listings.filter(title__icontains=search_query)

    part_query = request.GET.get('part_query', '').strip()
    if part_query:
        listings = listings.filter(
            Q(title__icontains=part_query) | Q(description__icontains=part_query)
        )

    pairs = request.GET.getlist('pair')
    if pairs:
        q = Q()
        for pair in pairs:
            parts = pair.split('|')
            if len(parts) == 4:
                bid, bname, mid, mname = parts
                if mid:
                    q |= Q(brand_id=bid, model_id=mid)
                else:
                    q |= Q(brand_id=bid)
        if q:
            listings = listings.filter(q)
    elif brand_filter:
        listings = listings.filter(brand_id=brand_filter)
        if model_filter:
            listings = listings.filter(model_id=model_filter)

    if price_min:
        listings = listings.filter(price__gte=price_min)
    if price_max:
        listings = listings.filter(price__lte=price_max)
    if year_min:
        listings = listings.filter(year__gte=year_min)
    if year_max:
        listings = listings.filter(year__lte=year_max)
    if mileage_min:
        listings = listings.filter(mileage__gte=mileage_min)
    if mileage_max:
        listings = listings.filter(mileage__lte=mileage_max)
    if fuel_type_filter:
        listings = listings.filter(fuel_type_id=fuel_type_filter)
    body_type_filter = [v for v in request.GET.getlist('body_type') if v]
    if body_type_filter:
        listings = listings.filter(body_type__in=body_type_filter)
    if color_filter:
        listings = listings.filter(color=color_filter)
    if doors_filter:
        listings = listings.filter(doors=doors_filter)
    if condition_filter:
        listings = listings.filter(condition=condition_filter)
    if drive_type_filter:
        listings = listings.filter(drive_type=drive_type_filter)
    if seats_filter:
        listings = listings.filter(seats=seats_filter)
    if euro_standard_filter:
        listings = listings.filter(euro_standard=euro_standard_filter)
    if power_min:
        listings = listings.filter(power__gte=power_min)
    if power_max:
        listings = listings.filter(power__lte=power_max)
    if engine_min:
        listings = listings.filter(engine_capacity__gte=engine_min)
    if engine_max:
        listings = listings.filter(engine_capacity__lte=engine_max)
    if climate_filter:
        listings = listings.filter(climate=climate_filter)
    if steering_filter:
        listings = listings.filter(steering=steering_filter)
    if defects_filter:
        listings = listings.filter(defects=defects_filter)
    if state_filter:
        listings = listings.filter(country='US', state=state_filter)
    elif country_filter:
        listings = listings.filter(country=country_filter)
    if equipment_ids:
        for eid in equipment_ids:
            listings = listings.filter(equipment_items__equipment_id=eid)

    part_query = f.get('part_query', '').strip()
    if part_query:
        listings = listings.filter(
            Q(title__icontains=part_query) | Q(description__icontains=part_query)
        )

    compat_make = f.get('compat_make', '')
    if compat_make:
        listings = listings.filter(brand_id=compat_make)

    compat_model = f.get('compat_model', '')
    if compat_model:
        listings = listings.filter(model_id=compat_model)

    compat_year_min = f.get('compat_year_min', '')
    if compat_year_min:
        listings = listings.filter(year__gte=compat_year_min)

    compat_year_max = f.get('compat_year_max', '')
    if compat_year_max:
        listings = listings.filter(year__lte=compat_year_max)

    city_filter_param = f.get('city_filter', '')
    if city_filter_param:
        listings = listings.filter(city__iexact=city_filter_param)

    saved_ids = []
    if request.user.is_authenticated:
        saved_ids = list(SavedListing.objects.filter(
            user=request.user
        ).values_list('listing_id', flat=True))

    categories = [
        {'value': vt.slug, 'label': vt.name}
        for vt in _get_visible_vehicle_types(request.user)
    ]

    # ═══ Advanced search Equipment — CARS-ONLY filter ═══
    CARS_CAT_KEYS = [k for k, _ in CARS_EQUIPMENT_CATEGORIES]
    CARS_CAT_LABELS = dict(CARS_EQUIPMENT_CATEGORIES)
    all_equipment = Equipment.objects.filter(
        category__in=CARS_CAT_KEYS
    ).order_by('category', 'name')
    equipment_by_category = [
        (cat_key, CARS_CAT_LABELS.get(cat_key, cat_key), list(items))
        for cat_key, items in groupby(all_equipment, key=lambda x: x.category)
    ]

    from django.db.models import Case, When, IntegerField, Value
    from django.db.models.functions import Greatest, Coalesce
    _now2 = timezone.now()
    _three_days_ago2 = _now2 - timedelta(days=NEW_LISTING_DAYS)

    sorted_listings = listings.annotate(
        effective_date=Greatest(
            'created_at',
            Coalesce('last_boosted_at', 'created_at'),
        ),
    ).annotate(
        sort_priority=Case(
            When(star_level=2, star_expires_at__gt=_now2, then=Value(500)),
            When(star_level=1, star_expires_at__gt=_now2, then=Value(400)),
            When(effective_date__gt=_three_days_ago2, then=Value(200)),
            default=Value(100),
            output_field=IntegerField(),
        )
    ).order_by('-sort_priority', '-effective_date')

    sorted_listings_all = list(sorted_listings[:60])
    _track_listing_impressions(request, sorted_listings_all)

    new_listing_ids = [
        l.id for l in sorted_listings_all
        if l.created_at >= timezone.now() - timedelta(days=NEW_LISTING_DAYS)
    ]

    context = {
        'listings': sorted_listings_all,
        'total_count': listings.count(),
        'brands': brands,
        'years': years,
        'fuel_types': fuel_types,
        'transmissions': transmissions,
        'categories': categories,
        'body_type_choices': Listing.BODY_TYPE_CHOICES,
        'color_choices': Listing.COLOR_CHOICES,
        'door_choices': Listing.DOOR_CHOICES,
        'condition_choices': Listing.CONDITION_CHOICES,
        'drive_type_choices': Listing.DRIVE_TYPE_CHOICES,
        'seats_choices': Listing.SEATS_CHOICES,
        'euro_standard_choices': Listing.EURO_STANDARD_CHOICES,
        'climate_choices': Listing.CLIMATE_CHOICES,
        'steering_choices': Listing.STEERING_CHOICES,
        'defect_choices': Listing.DEFECT_CHOICES,
        'us_states': Listing.US_STATE_CHOICES,
        'saved_ids': saved_ids,
        'new_listing_ids': new_listing_ids,
        'f': request.GET,
        'selected_body_types': request.GET.getlist('body_type'),
        'equipment_by_category': equipment_by_category,
        'selected_equipment': equipment_ids,
    }
    return render(request, 'listings/advanced_search.html', context)


def _build_edit_context(listing, step, form):
    return {
        'form': form, 'listing': listing, 'step': step,
        'is_edit_mode': True, 'edit_listing_id': listing.pk,
        'total_steps': 7,
        'vehicle_types': VehicleType.objects.all().order_by('order'),
        'brands': Brand.objects.all().order_by('name'),
        'years': list(range(timezone.now().year + 1, 1949, -1)),
        'progress_percent': 100,
        'listing_data': {
            'step1': {
                'brand': listing.brand.pk if listing.brand else '',
                'model': listing.model.pk if listing.model else '',
                'year': listing.year,
                'first_registration_month': listing.first_registration.month if listing.first_registration else '',
                'vin': listing.vin,
            },
            'step7': {
                'country': listing.country,
                'state': listing.state if hasattr(listing, 'state') else '',
            },
            'step3_partial': {
                'body_type': listing.body_type,
                'fuel_type': listing.fuel_type.pk if listing.fuel_type else '',
                'transmission': listing.transmission.pk if listing.transmission else '',
                'doors': listing.doors, 'condition': listing.condition,
                'defects': listing.defects, 'steering': listing.steering,
                'mileage': listing.mileage,
                'engine_capacity': float(listing.engine_capacity) if listing.engine_capacity else '',
                'power': listing.power or '',
            },
        },
        'temp_images_count': listing.images.count(),
        'step1_brand': listing.brand.name if listing.brand else '',
        'step1_model': listing.model.name if listing.model else '',
        'step1_year': listing.year,
        'country_choices': list(Listing.COUNTRY_CHOICES),
        'us_states': Listing.US_STATE_CHOICES,
        'completed_steps': {step},
        'step_labels': [
            (2, 'Photos'), (3, 'Details'), (4, 'Equipment'),
            (5, 'Price'), (6, 'Description'), (7, 'Contacts'),
        ],
    }


@login_required
def listing_edit_hub(request, pk):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user)

    # ✅ Trucks → atskiras edit puslapis (autoplius 8x4 layout)
    if listing.vehicle_type and listing.vehicle_type.slug == 'trucks':
        return redirect('trucks_listing_edit', pk=pk)

    # ✅ Cars → Quick edit (single-page form, /create/cars/quick/?edit=<pk>)
    if listing.vehicle_type and listing.vehicle_type.slug == 'cars':
        return redirect(f'/create/cars/quick/?edit={pk}')
    if listing.vehicle_type and listing.vehicle_type.slug == 'boats':
        return redirect(f'/create/boats/?edit={pk}')
    if listing.vehicle_type and listing.vehicle_type.slug == 'trailers':
        return redirect(f'/create/trailers/?edit={pk}')
    if listing.vehicle_type and listing.vehicle_type.slug == 'agriculture':
        return redirect(f'/create/agriculture/?edit={pk}')
    if listing.vehicle_type and listing.vehicle_type.slug == 'forestry':
        return redirect(f'/create/forestry/?edit={pk}')
    if listing.vehicle_type and listing.vehicle_type.slug == 'camping-houses':
        return redirect(f'/create/camping-houses/?edit={pk}')
    if listing.vehicle_type and listing.vehicle_type.slug == 'services':
        return redirect(f'/create/services/?edit={pk}')
    if listing.vehicle_type and listing.vehicle_type.slug == 'electronics':
        return redirect(f'/create/electronics/?edit={pk}')
    if listing.vehicle_type and listing.vehicle_type.slug == 'bicycles':
        return redirect(f'/create/bicycles/?edit={pk}')
    if listing.vehicle_type and listing.vehicle_type.slug == 'rental':
        _sub = listing.subcategory.slug if listing.subcategory else ''
        return redirect(
            f'/create/rental/{RENTAL_SUB_TO_FORM.get(_sub, "car")}/?edit={pk}')
    if listing.vehicle_type and listing.vehicle_type.slug == 'loading-equipment':
        return redirect(f'/create/loading-equipment/?edit={pk}')
    if listing.vehicle_type and listing.vehicle_type.slug == 'construction':
        if listing.constr_attach_type or (
                listing.subcategory and listing.subcategory.slug == 'construction-attachments'):
            return redirect(f'/create/construction/attachment/?edit={pk}')
        return redirect(f'/create/construction/?edit={pk}')
    if listing.subcategory and listing.subcategory.slug == 'whole-car-for-parts':
        return redirect('car_for_parts_edit', pk=pk)
    if listing.subcategory and listing.subcategory.slug == 'whole-moto-for-parts':
        return redirect('moto_for_parts_edit', pk=pk)
    if listing.subcategory and listing.subcategory.slug == 'whole-truck-for-parts':
        return redirect('truck_for_parts_edit', pk=pk)
    if listing.vehicle_type and listing.vehicle_type.slug == 'parts':
        return redirect(f'/create/parts/form/?edit={pk}')
    # Moto gear sits under the motorcycles vehicle type — check it first, or
    # gear listings open the motorcycle form.
    if listing.subcategory and listing.subcategory.slug in MOTO_GEAR_SLUGS:
        return redirect(f'/create/motogear/?edit={pk}')
    if listing.vehicle_type and listing.vehicle_type.slug == 'motorcycles':
        return redirect(f'/create/motorcycle/?edit={pk}')

    # ✅ Whole car for parts → atskiras edit puslapis (vienpuslapė forma)
    if listing.subcategory and listing.subcategory.slug == 'whole-car-for-parts':
        return redirect('car_for_parts_edit', pk=pk)
    if listing.subcategory and listing.subcategory.slug == 'whole-moto-for-parts':
        return redirect('moto_for_parts_edit', pk=pk)

    total_equipment = Equipment.objects.count()
    filled_equipment = listing.equipment_items.count()
    images_count = listing.images.count()
    MAX_IMAGES = 40
    main_image = listing.images.first()

    sections = [
        {'key': 'vehicle', 'icon': '🚗', 'title': 'Vehicle Details',
         'url': reverse('listing_edit_section', kwargs={'pk': listing.pk, 'section': 'vehicle'}),
         'progress': None},
        {'key': 'equipment', 'icon': '🔧', 'title': 'Equipment',
         'url': reverse('listing_edit_section', kwargs={'pk': listing.pk, 'section': 'equipment'}),
         'progress': f'{filled_equipment} / {total_equipment}'},
        {'key': 'price', 'icon': '$', 'title': 'Price',
         'url': reverse('listing_edit_section', kwargs={'pk': listing.pk, 'section': 'price'}),
         'progress': f'{listing.currency_symbol}{int(listing.price)}'},
        {'key': 'description', 'icon': '📝', 'title': 'Description, Technical Condition',
         'url': reverse('listing_edit_section', kwargs={'pk': listing.pk, 'section': 'description'}),
         'progress': None},
        {'key': 'images', 'icon': '📷', 'title': 'Photos, Video',
         'url': reverse('listing_edit_section', kwargs={'pk': listing.pk, 'section': 'images'}),
         'progress': f'{images_count} / {MAX_IMAGES}'},
        {'key': 'contacts', 'icon': '📞', 'title': 'Contacts',
         'url': reverse('listing_edit_section', kwargs={'pk': listing.pk, 'section': 'contacts'}),
         'progress': None},
    ]

    context = {
        'listing': listing,
        'sections': sections,
        'main_image': main_image,
        'is_reserved': listing.status == 'reserved',
        'is_expired': listing.status == 'expired',
        'is_active': listing.status == 'active',
        'listing_fee': listing.listing_fee,
        'payments_enabled': getattr(settings, 'PAYMENTS_ENABLED', False),
    }
    return render(request, 'listings/listing_edit_hub.html', context)


def listing_vin_update(request, pk):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user)
    if request.method == 'POST':
        new_vin = request.POST.get('vin', '').strip().upper()
        listing.vin = new_vin
        listing.save(update_fields=['vin'])
    return redirect('listing_edit_hub', pk=listing.pk)


@login_required
def listing_edit_section(request, pk, section):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user)

    # ✅ Trucks → atskiras edit puslapis (jokios sekcijos navigacijos)
    if listing.vehicle_type and listing.vehicle_type.slug == 'trucks':
        return redirect('trucks_listing_edit', pk=pk)

    # ✅ Cars → Quick edit (single-page form, /create/cars/quick/?edit=<pk>)
    if listing.vehicle_type and listing.vehicle_type.slug == 'cars':
        return redirect(f'/create/cars/quick/?edit={pk}')
    if listing.vehicle_type and listing.vehicle_type.slug == 'boats':
        return redirect(f'/create/boats/?edit={pk}')
    if listing.vehicle_type and listing.vehicle_type.slug == 'trailers':
        return redirect(f'/create/trailers/?edit={pk}')
    if listing.vehicle_type and listing.vehicle_type.slug == 'agriculture':
        return redirect(f'/create/agriculture/?edit={pk}')
    if listing.vehicle_type and listing.vehicle_type.slug == 'forestry':
        return redirect(f'/create/forestry/?edit={pk}')
    if listing.vehicle_type and listing.vehicle_type.slug == 'camping-houses':
        return redirect(f'/create/camping-houses/?edit={pk}')
    if listing.vehicle_type and listing.vehicle_type.slug == 'services':
        return redirect(f'/create/services/?edit={pk}')
    if listing.vehicle_type and listing.vehicle_type.slug == 'electronics':
        return redirect(f'/create/electronics/?edit={pk}')
    if listing.vehicle_type and listing.vehicle_type.slug == 'bicycles':
        return redirect(f'/create/bicycles/?edit={pk}')
    if listing.vehicle_type and listing.vehicle_type.slug == 'rental':
        _sub = listing.subcategory.slug if listing.subcategory else ''
        return redirect(
            f'/create/rental/{RENTAL_SUB_TO_FORM.get(_sub, "car")}/?edit={pk}')
    if listing.vehicle_type and listing.vehicle_type.slug == 'loading-equipment':
        return redirect(f'/create/loading-equipment/?edit={pk}')
    if listing.vehicle_type and listing.vehicle_type.slug == 'construction':
        if listing.constr_attach_type or (
                listing.subcategory and listing.subcategory.slug == 'construction-attachments'):
            return redirect(f'/create/construction/attachment/?edit={pk}')
        return redirect(f'/create/construction/?edit={pk}')
    # „Visas X dalimis" — PRIEŠ bendrą parts šaką, kitaip šie skelbimai
    # atsidaro bendroje dalies formoje, kuri jų laukų nemoka.
    if listing.subcategory and listing.subcategory.slug == 'whole-car-for-parts':
        return redirect('car_for_parts_edit', pk=pk)
    if listing.subcategory and listing.subcategory.slug == 'whole-moto-for-parts':
        return redirect('moto_for_parts_edit', pk=pk)
    if listing.subcategory and listing.subcategory.slug == 'whole-truck-for-parts':
        return redirect('truck_for_parts_edit', pk=pk)
    if listing.vehicle_type and listing.vehicle_type.slug == 'parts':
        return redirect(f'/create/parts/form/?edit={pk}')
    # Moto gear sits under the motorcycles vehicle type — check it first, or
    # gear listings open the motorcycle form.
    if listing.subcategory and listing.subcategory.slug in MOTO_GEAR_SLUGS:
        return redirect(f'/create/motogear/?edit={pk}')
    if listing.vehicle_type and listing.vehicle_type.slug == 'motorcycles':
        return redirect(f'/create/motorcycle/?edit={pk}')


    section_to_step = {
        'vehicle': 3, 'equipment': 4, 'price': 5,
        'description': 6, 'images': 2, 'contacts': 7,
    }
    step = section_to_step.get(section)
    if not step:
        messages.error(request, 'Unknown section.')
        return redirect('listing_edit_hub', pk=listing.pk)
    return redirect('listing_edit_step', pk=listing.pk, step=step)


@login_required
def listing_activation_plans(request, pk):
    from .models import PricingPlan

    listing = get_object_or_404(Listing, pk=pk, seller=request.user)

    if listing.status == 'draft':
        is_moto_gear_draft = (
            listing.subcategory_id
            and listing.subcategory.slug in MOTO_GEAR_SLUGS
        )

        if is_moto_gear_draft:
            is_complete = (
                listing.subcategory_id
                and listing.condition
                and listing.price and listing.price > 0
                and listing.country and listing.city and listing.city != '—'
            )
            if not is_complete:
                request.session['active_motogear_draft_id'] = listing.pk
                request.session.modified = True
                messages.info(request, 'Complete the listing before activating it.')
                return redirect('motogear_listing_create')
        else:
            is_complete = (
                listing.year and listing.first_registration
                and listing.fuel_type_id
                and listing.price and listing.price > 0
                and listing.country and listing.city and listing.city != '—'
            )
            if listing.vehicle_type and listing.vehicle_type.slug == 'cars':
                is_complete = is_complete and (
                    listing.brand_id and listing.body_type
                    and listing.transmission_id
                    and listing.doors and listing.mileage
                )
            elif listing.vehicle_type and listing.vehicle_type.slug == 'trucks':
                is_complete = is_complete and (
                    listing.truck_brand_id and listing.truck_model_text
                    and listing.truck_type
                )

            if not is_complete:
                if listing.vehicle_type and listing.vehicle_type.slug == 'trucks':
                    request.session['active_trucks_draft_id'] = listing.pk
                    request.session.modified = True
                    messages.info(request, 'Complete the listing before activating it.')
                    return redirect('trucks_listing_create')
                if listing.vehicle_type and listing.vehicle_type.slug == 'motorcycles':
                    request.session['active_moto_draft_id'] = listing.pk
                    request.session.modified = True
                    messages.info(request, 'Complete the listing before activating it.')
                    return redirect('motorcycle_listing_create')
                request.session[CARS_DRAFT_SESSION_KEY] = listing.pk
                request.session.modified = True
                messages.info(request, 'Complete the listing before activating it.')
                return redirect('/create/?step=2')

    plans = PricingPlan.objects.filter(
        vehicle_type=listing.vehicle_type,
        is_active=True,
    ).order_by('order', 'duration_days')

    if request.method == 'POST':
        plan_id = request.POST.get('plan_id')

        try:
            plan = PricingPlan.objects.get(
                id=plan_id,
                vehicle_type=listing.vehicle_type,
                is_active=True,
            )
        except (PricingPlan.DoesNotExist, ValueError, TypeError):
            messages.error(request, 'Invalid plan selected.')
            return redirect('listing_activation_plans', pk=listing.pk)

        listing.status = 'active'
        listing.activated_at = timezone.now()
        listing.expires_at = timezone.now() + timedelta(days=plan.duration_days)

        if plan.boost_days:
            listing.last_boosted_at = timezone.now()
        if plan.vip_days:
            listing.star_level = 1
            listing.star_expires_at = timezone.now() + timedelta(days=plan.vip_days)

        listing.save()

        _send_listing_published_email(listing, request.user)

        return redirect(
            reverse('listing_success', kwargs={'pk': listing.pk}) + '?action=published'
        )

    context = {
        'listing': listing,
        'main_image': listing.images.first(),
        'plans': plans,
    }
    return render(request, 'listings/listing_activation_plans.html', context)


@login_required
def listing_activate(request, pk):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user)
    if request.method != 'POST':
        return redirect('listing_edit_hub', pk=listing.pk)

    if listing.status == 'draft':
        if listing.subcategory_id and listing.subcategory.slug in MOTO_GEAR_SLUGS:
            request.session['active_motogear_draft_id'] = listing.pk
            request.session.modified = True
            return redirect('motogear_listing_create')
        if listing.vehicle_type and listing.vehicle_type.slug == 'trucks':
            request.session['active_trucks_draft_id'] = listing.pk
            request.session.modified = True
            return redirect('trucks_listing_create')
        if listing.vehicle_type and listing.vehicle_type.slug == 'motorcycles':
            request.session['active_moto_draft_id'] = listing.pk
            request.session.modified = True
            return redirect('motorcycle_listing_create')
        request.session[CARS_DRAFT_SESSION_KEY] = listing.pk
        request.session.modified = True
        return redirect('/create/?step=2')

    payments_enabled = getattr(settings, 'PAYMENTS_ENABLED', False)
    fee = listing.listing_fee

    if payments_enabled:
        messages.info(request, f'Payment system not yet enabled. Fee: {fee}')
        return redirect('listing_edit_hub', pk=listing.pk)

    previous_status = listing.status
    if previous_status == 'expired':
        action = 'reactivated'
    elif previous_status == 'draft':
        action = 'published'
    else:
        action = 'extended'

    listing.activate(days=Listing.DEFAULT_ACTIVE_DAYS)

    if previous_status == 'draft':
        _send_listing_published_email(listing, request.user)

    return redirect(
        reverse('listing_success', kwargs={'pk': listing.pk}) + f'?action={action}'
    )


@login_required
def listing_reserve_toggle(request, pk):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user)
    if request.method != 'POST':
        return redirect('listing_edit_hub', pk=listing.pk)

    if listing.status == 'reserved':
        listing.unreserve()
    elif listing.status == 'active':
        note = request.POST.get('note', '')
        listing.reserve(note=note)
    else:
        messages.error(request, 'Only active listings can be reserved.')

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': listing.status,
            'is_reserved': listing.status == 'reserved',
        })

    return redirect('listing_edit_hub', pk=listing.pk)


@login_required
def listing_edit_step(request, pk, step):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user)

    # ✅ Trucks → atskiras edit puslapis
    if listing.vehicle_type and listing.vehicle_type.slug == 'trucks':
        return redirect('trucks_listing_edit', pk=pk)

    # ✅ Cars → Quick edit (single-page form, /create/cars/quick/?edit=<pk>)
    if listing.vehicle_type and listing.vehicle_type.slug == 'cars':
        return redirect(f'/create/cars/quick/?edit={pk}')
    if listing.vehicle_type and listing.vehicle_type.slug == 'boats':
        return redirect(f'/create/boats/?edit={pk}')
    if listing.vehicle_type and listing.vehicle_type.slug == 'trailers':
        return redirect(f'/create/trailers/?edit={pk}')
    if listing.vehicle_type and listing.vehicle_type.slug == 'agriculture':
        return redirect(f'/create/agriculture/?edit={pk}')
    if listing.vehicle_type and listing.vehicle_type.slug == 'forestry':
        return redirect(f'/create/forestry/?edit={pk}')
    if listing.vehicle_type and listing.vehicle_type.slug == 'camping-houses':
        return redirect(f'/create/camping-houses/?edit={pk}')
    if listing.vehicle_type and listing.vehicle_type.slug == 'services':
        return redirect(f'/create/services/?edit={pk}')
    if listing.vehicle_type and listing.vehicle_type.slug == 'electronics':
        return redirect(f'/create/electronics/?edit={pk}')
    if listing.vehicle_type and listing.vehicle_type.slug == 'bicycles':
        return redirect(f'/create/bicycles/?edit={pk}')
    if listing.vehicle_type and listing.vehicle_type.slug == 'rental':
        _sub = listing.subcategory.slug if listing.subcategory else ''
        return redirect(
            f'/create/rental/{RENTAL_SUB_TO_FORM.get(_sub, "car")}/?edit={pk}')
    if listing.vehicle_type and listing.vehicle_type.slug == 'loading-equipment':
        return redirect(f'/create/loading-equipment/?edit={pk}')
    if listing.vehicle_type and listing.vehicle_type.slug == 'construction':
        if listing.constr_attach_type or (
                listing.subcategory and listing.subcategory.slug == 'construction-attachments'):
            return redirect(f'/create/construction/attachment/?edit={pk}')
        return redirect(f'/create/construction/?edit={pk}')
    # „Visas X dalimis" — PRIEŠ bendrą parts šaką, kitaip šie skelbimai
    # atsidaro bendroje dalies formoje, kuri jų laukų nemoka.
    if listing.subcategory and listing.subcategory.slug == 'whole-car-for-parts':
        return redirect('car_for_parts_edit', pk=pk)
    if listing.subcategory and listing.subcategory.slug == 'whole-moto-for-parts':
        return redirect('moto_for_parts_edit', pk=pk)
    if listing.subcategory and listing.subcategory.slug == 'whole-truck-for-parts':
        return redirect('truck_for_parts_edit', pk=pk)
    if listing.vehicle_type and listing.vehicle_type.slug == 'parts':
        return redirect(f'/create/parts/form/?edit={pk}')
    # Moto gear sits under the motorcycles vehicle type — check it first, or
    # gear listings open the motorcycle form.
    if listing.subcategory and listing.subcategory.slug in MOTO_GEAR_SLUGS:
        return redirect(f'/create/motogear/?edit={pk}')
    if listing.vehicle_type and listing.vehicle_type.slug == 'motorcycles':
        return redirect(f'/create/motorcycle/?edit={pk}')


    step = int(step)
    if step not in range(1, 8):
        return redirect('listing_edit_hub', pk=listing.pk)
    if request.method == 'POST':
        return _handle_edit_step_post(request, listing, step)
    return _render_edit_step(request, listing, step)


def _render_edit_step(request, listing, step):
    if step == 2:
        form = Step2MediaForm(initial={'video_url': listing.video_url})
    elif step == 3:
        form = Step3VehicleDataForm(initial={
            'body_type': listing.body_type,
            'fuel_type': listing.fuel_type,
            'transmission': listing.transmission,
            'doors': listing.doors, 'condition': listing.condition,
            'color': listing.color, 'defects': listing.defects,
            'steering': listing.steering, 'mileage': listing.mileage,
            'engine_capacity': listing.engine_capacity, 'power': listing.power,
            'drive_type': listing.drive_type, 'seats': listing.seats,
            'rim_size': listing.rim_size, 'climate': listing.climate,
            'curb_weight': listing.curb_weight, 'euro_standard': listing.euro_standard,
            'co2_emission': listing.co2_emission,
            'fuel_consumption_city': listing.fuel_consumption_city,
            'fuel_consumption_highway': listing.fuel_consumption_highway,
            'fuel_consumption_combined': listing.fuel_consumption_combined,
            'origin_country': listing.origin_country,
            'technical_inspection_month': listing.technical_inspection_month,
            'technical_inspection_year': listing.technical_inspection_year,
        })
    elif step == 4:
        selected_equipment_ids = list(listing.equipment_items.values_list('equipment_id', flat=True))
        form = Step4EquipmentForm(initial={'equipment': selected_equipment_ids})
    elif step == 5:
        form = Step5PriceForm(initial={'price': listing.price, 'negotiable': listing.negotiable})
    elif step == 6:
        form = Step6DescriptionForm(initial={'description': listing.description})
    elif step == 7:
        seller_phone = ''
        if hasattr(listing.seller, 'profile') and listing.seller.profile.phone_number:
            seller_phone = listing.seller.profile.phone_number

        form = Step7ContactForm(initial={
            'country': listing.country,
            'city': listing.city,
            'postal_code': listing.postal_code,
            'address': listing.address,
            'hide_exact_address': listing.hide_exact_address,
            'phone': seller_phone,
            'email': listing.seller.email,
            'agree_terms': True,
        })
    else:
        return redirect('listing_edit_hub', pk=listing.pk)

    context = _build_edit_context(listing, step, form)
    return render(request, 'listings/listing_create.html', context)


def _handle_edit_step_post(request, listing, step):
    form = None

    if step == 2:
        form = Step2MediaForm(request.POST, request.FILES)
        if form.is_valid():
            listing.video_url = form.cleaned_data.get('video_url', '')
            new_vin = request.POST.get('vin', '').strip().upper()
            listing.vin = new_vin
            listing.save(update_fields=['video_url', 'vin'])
            images, _image_errors = split_valid_images(
                request.FILES.getlist('images')
            )
            for _err in _image_errors:
                messages.error(request, _err)
            start_order = listing.images.count()
            photos_added = 0
            for i, image in enumerate(images[:40]):
                ListingImage.objects.create(
                    listing=listing, image=image,
                    is_main=(start_order == 0 and i == 0),
                    order=start_order + i
                )
                photos_added += 1

            if photos_added > 0:
                _send_saved_listing_updated_emails(
                    listing,
                    f'{photos_added} new photo{"s" if photos_added > 1 else ""} added'
                )

            return redirect('listing_edit_hub', pk=listing.pk)

    elif step == 3:
        form = Step3VehicleDataForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            def _set_if_provided(attr, val):
                if val not in (None, '', []):
                    setattr(listing, attr, val)

            listing.condition = cd['condition']
            listing.color = cd.get('color', '')
            listing.defects = cd.get('defects', '')
            listing.mileage = cd['mileage']
            listing.drive_type = cd.get('drive_type', '')
            listing.climate = cd.get('climate', '')
            listing.euro_standard = cd.get('euro_standard', '')
            listing.origin_country = cd.get('origin_country', '')

            _set_if_provided('power', cd.get('power'))
            _set_if_provided('seats', cd.get('seats'))
            _set_if_provided('rim_size', cd.get('rim_size'))
            _set_if_provided('curb_weight', cd.get('curb_weight'))
            _set_if_provided('co2_emission', cd.get('co2_emission'))
            _set_if_provided('fuel_consumption_city', cd.get('fuel_consumption_city'))
            _set_if_provided('fuel_consumption_highway', cd.get('fuel_consumption_highway'))
            _set_if_provided('fuel_consumption_combined', cd.get('fuel_consumption_combined'))
            _set_if_provided('technical_inspection_month', cd.get('technical_inspection_month'))
            _set_if_provided('technical_inspection_year', cd.get('technical_inspection_year'))

            listing.vin = request.POST.get('vin', '').strip().upper()

            listing.save()

            _send_saved_listing_updated_emails(listing, 'Vehicle details updated')

            return redirect('listing_edit_hub', pk=listing.pk)

    elif step == 4:
        form = Step4EquipmentForm(request.POST)
        if form.is_valid():
            listing.equipment_items.all().delete()
            for eq in form.cleaned_data.get('equipment', []):
                ListingEquipment.objects.create(listing=listing, equipment=eq)

            _send_saved_listing_updated_emails(listing, 'Equipment updated')

            return redirect('listing_edit_hub', pk=listing.pk)

    elif step == 5:
        form = Step5PriceForm(request.POST)
        if form.is_valid():
            _old_price = float(listing.price) if listing.price else 0

            listing.price = form.cleaned_data['price']
            listing.negotiable = form.cleaned_data.get('negotiable', False)
            listing.save(update_fields=['price', 'negotiable'])

            try:
                new_price = float(listing.price)
                if new_price != _old_price and _old_price > 0:
                    if new_price < _old_price:
                        _send_saved_listing_price_drop_emails(listing, _old_price, new_price)
                    else:
                        summary = (
                            f'Price changed from '
                            f'{listing.currency_symbol}{int(_old_price)} to '
                            f'{listing.currency_symbol}{int(new_price)}'
                        )
                        _send_saved_listing_updated_emails(listing, summary)
            except (ValueError, TypeError):
                pass

            return redirect('listing_edit_hub', pk=listing.pk)

    elif step == 6:
        form = Step6DescriptionForm(request.POST)
        if form.is_valid():
            listing.description = form.cleaned_data.get('description', '')
            listing.save(update_fields=['description'])

            _send_saved_listing_updated_emails(listing, 'Description updated')

            return redirect('listing_edit_hub', pk=listing.pk)

    elif step == 7:
        form = Step7ContactForm(request.POST)
        if form.is_valid():
            listing.country = form.cleaned_data['country']
            listing.city = form.cleaned_data.get('city', '')
            listing.postal_code = form.cleaned_data.get('postal_code', '')
            listing.address = form.cleaned_data.get('address', '')
            listing.hide_exact_address = form.cleaned_data.get('hide_exact_address', False)
            if hasattr(listing, 'state'):
                listing.state = request.POST.get('state', '') if listing.country == 'US' else ''

            lat, lng = get_coordinates_for_location(listing.city, listing.country)
            listing.latitude = lat
            listing.longitude = lng
            listing.save()

            _send_saved_listing_updated_emails(listing, 'Contact info updated')

            return redirect('listing_edit_hub', pk=listing.pk)

    context = _build_edit_context(listing, step, form)
    return render(request, 'listings/listing_create.html', context)


@login_required
def listing_success(request, pk):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user)
    action = request.GET.get('action', 'published')
    if action == 'created':
        action = 'published'
    action_headlines = {
        'published':   'Your listing was successfully published',
        'extended':    'Your listing was successfully extended',
        'reactivated': 'Your listing was successfully reactivated',
    }
    headline = action_headlines.get(action, 'Your listing is active')
    context = {
        'listing': listing, 'action': action, 'headline': headline,
        'main_image': listing.images.first(),
    }
    return render(request, 'listings/listing_success.html', context)


@login_required
def my_listings(request):
    from django.db.models import Case, When, IntegerField, Value

    status_filter = request.GET.get('status', 'all')
    selected_category = request.GET.get('category', '')
    now = timezone.now()
    rate_limit_cutoff = now - timedelta(hours=RENEW_RATE_LIMIT_HOURS)

    base_qs = Listing.objects.filter(seller=request.user).select_related(
        'brand', 'model', 'fuel_type', 'transmission',
        'subcategory', 'motorcycle_brand', 'motorcycle_model',
        'gear_brand', 'vehicle_type',
    ).prefetch_related('images', 'saved_by')

    total_all_count = base_qs.count()

    category_breakdown = _build_category_breakdown(request.user)

    MERGED_VT_SLUGS = {'trucks'}

    if selected_category and ':' in selected_category:
        vt_slug, sub_slug = selected_category.split(':', 1)
        base_qs = base_qs.filter(
            vehicle_type__slug=vt_slug,
            subcategory__slug=sub_slug,
        )
    elif selected_category:
        if selected_category in MERGED_VT_SLUGS:
            base_qs = base_qs.filter(vehicle_type__slug=selected_category)
        else:
            base_qs = base_qs.filter(
                vehicle_type__slug=selected_category,
                subcategory__isnull=True,
            )

    if status_filter == 'active':
        listings = base_qs.filter(status='active')
    elif status_filter == 'inactive':
        listings = base_qs.filter(status__in=['expired', 'draft'])
    elif status_filter == 'reserved':
        listings = base_qs.filter(status='reserved')
    elif status_filter == 'sold':
        listings = base_qs.filter(status='sold')
    elif status_filter == 'draft':
        listings = base_qs.filter(status='draft')
    else:
        listings = base_qs

    listings = listings.annotate(
        status_priority=Case(
            When(status='active', then=Value(1)),
            When(status='reserved', then=Value(2)),
            When(status='sold', then=Value(3)),
            When(status='expired', then=Value(4)),
            When(status='draft', then=Value(5)),
            When(status='archived', then=Value(6)),
            default=Value(99),
            output_field=IntegerField(),
        )
    ).order_by('status_priority', '-created_at')

    all_count = base_qs.count()
    active_count = base_qs.filter(status='active').count()
    inactive_count = base_qs.filter(status__in=['expired', 'draft']).count()
    reserved_count = base_qs.filter(status='reserved').count()
    sold_count = base_qs.filter(status='sold').count()
    draft_count = base_qs.filter(status='draft').count()

    listings_list = []
    for listing in listings:
        listing.saved_count = listing.saved_by.count()
        listing.main_image = listing.images.first()
        listing.is_boosted = (
            listing.last_boosted_at is not None
            and listing.last_boosted_at > rate_limit_cutoff
        )
        if listing.status == 'active' and not listing.is_shadow_banned:
            pos, total = listing.get_position()
            listing.stats_position = pos
            listing.stats_total = total
        else:
            listing.stats_position = None
            listing.stats_total = None
        listings_list.append(listing)

    context = {
        'listings': listings_list,
        'status_filter': status_filter,
        'all_count': all_count,
        'total_all_count': total_all_count,
        'active_count': active_count,
        'inactive_count': inactive_count,
        'reserved_count': reserved_count,
        'sold_count': sold_count,
        'draft_count': draft_count,
        'category_breakdown': category_breakdown,
        'selected_category': selected_category,
    }
    return render(request, 'listings/my_listings.html', context)


@login_required
def listing_stats(request, pk):
    listing = get_object_or_404(Listing, pk=pk)

    if listing.seller != request.user and not request.user.is_superuser:
        raise Http404("Listing not found")

    now = timezone.now()
    start_30d = now - timedelta(days=30)
    start_7d = now - timedelta(days=7)
    start_14d_ago = now - timedelta(days=14)

    views_total = listing.views_count
    impressions_total = listing.impressions_count
    saves_total = listing.saved_by.count()

    ctr = round((views_total / impressions_total) * 100, 1) if impressions_total else 0.0
    save_rate = round((saves_total / views_total) * 100, 1) if views_total else 0.0

    views_this_week = ListingView.objects.filter(
        listing=listing, viewed_at__gte=start_7d
    ).count()
    views_prev_week = ListingView.objects.filter(
        listing=listing, viewed_at__gte=start_14d_ago, viewed_at__lt=start_7d
    ).count()
    views_change_pct = _calc_change_pct(views_this_week, views_prev_week)

    impressions_this_week = ListingImpression.objects.filter(
        listing=listing, shown_at__gte=start_7d
    ).count()
    impressions_prev_week = ListingImpression.objects.filter(
        listing=listing, shown_at__gte=start_14d_ago, shown_at__lt=start_7d
    ).count()
    impressions_change_pct = _calc_change_pct(impressions_this_week, impressions_prev_week)

    position, position_total = listing.get_position()

    views_per_day = _get_daily_counts(
        ListingView.objects.filter(listing=listing, viewed_at__gte=start_30d),
        'viewed_at',
        start_30d.date(),
        now.date(),
    )

    impressions_per_day = _get_daily_counts(
        ListingImpression.objects.filter(listing=listing, shown_at__gte=start_30d),
        'shown_at',
        start_30d.date(),
        now.date(),
    )

    hourly_counts = [0] * 24
    for view in ListingView.objects.filter(listing=listing):
        hourly_counts[view.viewed_at.hour] += 1

    if max(hourly_counts) > 0:
        peak_hour = hourly_counts.index(max(hourly_counts))
        peak_hour_label = f'{peak_hour:02d}:00-{(peak_hour+1) % 24:02d}:00'
    else:
        peak_hour_label = 'No data yet'

    context = {
        'listing': listing,
        'main_image': listing.images.first(),
        'views_total': views_total,
        'impressions_total': impressions_total,
        'saves_total': saves_total,
        'ctr': ctr,
        'save_rate': save_rate,
        'views_change_pct': views_change_pct,
        'impressions_change_pct': impressions_change_pct,
        'position': position,
        'position_total': position_total,
        'chart_labels': json.dumps([d['label'] for d in views_per_day]),
        'chart_views_data': json.dumps([d['count'] for d in views_per_day]),
        'chart_impressions_data': json.dumps([d['count'] for d in impressions_per_day]),
        'chart_hourly_data': json.dumps(hourly_counts),
        'peak_hour_label': peak_hour_label,
    }
    return render(request, 'listings/listing_stats.html', context)


def _get_daily_counts(queryset, date_field, start_date, end_date):
    from collections import defaultdict

    daily = defaultdict(int)
    for obj in queryset:
        d = getattr(obj, date_field).date()
        daily[d] += 1

    result = []
    current = start_date
    while current <= end_date:
        result.append({
            'label': current.strftime('%Y-%m-%d'),
            'count': daily.get(current, 0),
        })
        current += timedelta(days=1)

    return result


def _calc_change_pct(current, previous):
    if previous == 0:
        return 100 if current > 0 else 0
    return round(((current - previous) / previous) * 100, 1)


def _is_superuser(user):
    return user.is_authenticated and user.is_superuser


@user_passes_test(_is_superuser)
def admin_users_list(request):
    search_query = request.GET.get('search', '').strip()

    users_qs = User.objects.annotate(
        total_listings=Count('listings'),
        active_listings=Count('listings', filter=Q(listings__status='active')),
        shadow_banned_listings=Count('listings', filter=Q(listings__is_shadow_banned=True)),
    ).filter(total_listings__gt=0)

    if search_query:
        users_qs = users_qs.filter(
            Q(email__icontains=search_query) |
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )

    users_qs = users_qs.order_by('-total_listings', 'email')

    context = {
        'users': users_qs,
        'search_query': search_query,
        'total_users': users_qs.count(),
    }
    return render(request, 'listings/admin_users_list.html', context)


@user_passes_test(_is_superuser)
def admin_moderate_user(request, user_id):
    target_user = get_object_or_404(User, pk=user_id)

    listings = Listing.objects.filter(seller=target_user).select_related(
        'brand', 'model', 'fuel_type'
    ).prefetch_related('images').order_by('-created_at')

    listings_list = []
    for listing in listings:
        listing.main_image = listing.images.first()
        listings_list.append(listing)

    total_count = listings.count()
    shadow_banned_count = listings.filter(is_shadow_banned=True).count()
    active_count = listings.filter(status='active').count()

    context = {
        'target_user': target_user,
        'listings': listings_list,
        'total_count': total_count,
        'shadow_banned_count': shadow_banned_count,
        'active_count': active_count,
    }
    return render(request, 'listings/admin_moderate_user.html', context)


@user_passes_test(_is_superuser)
def admin_toggle_shadow_ban(request, pk):
    if request.method != 'POST':
        return redirect('admin_users_list')

    listing = get_object_or_404(Listing, pk=pk)
    listing.is_shadow_banned = not listing.is_shadow_banned
    listing.save(update_fields=['is_shadow_banned'])

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'is_shadow_banned': listing.is_shadow_banned,
            'listing_id': listing.pk,
        })

    return redirect('admin_moderate_user', user_id=listing.seller.pk)


@user_passes_test(_is_superuser)
def admin_sales_stats(request):
    from collections import defaultdict

    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_ago = now - timedelta(days=7)
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    start_30d = now - timedelta(days=30)
    start_90d = now - timedelta(days=90)

    total_listings = Listing.objects.count()
    active_listings = Listing.objects.filter(status='active', is_shadow_banned=False).count()
    sold_listings_displayed = Listing.objects.filter(status='sold').count()
    inactive_listings = Listing.objects.filter(status__in=['expired', 'draft']).count()
    shadow_banned = Listing.objects.filter(is_shadow_banned=True).count()

    # ═══ Listings created stats ═══
    listings_today = Listing.objects.filter(created_at__gte=today_start).count()
    listings_week = Listing.objects.filter(created_at__gte=week_ago).count()
    listings_month = Listing.objects.filter(created_at__gte=start_30d).count()

    # By status — only active+sold (real listings, not drafts/expired)
    listings_today_real = Listing.objects.filter(
        created_at__gte=today_start,
        status__in=['active', 'sold']
    ).count()
    listings_week_real = Listing.objects.filter(
        created_at__gte=week_ago,
        status__in=['active', 'sold']
    ).count()
    listings_month_real = Listing.objects.filter(
        created_at__gte=start_30d,
        status__in=['active', 'sold']
    ).count()

    total_sales = SalesRecord.objects.count()
    total_revenue = SalesRecord.objects.aggregate(s=Sum('price'))['s'] or 0
    avg_price = SalesRecord.objects.aggregate(a=Avg('price'))['a'] or 0
    avg_days_active = SalesRecord.objects.aggregate(a=Avg('days_active'))['a'] or 0

    sales_this_month = SalesRecord.objects.filter(sold_at__gte=month_start).count()
    revenue_this_month = SalesRecord.objects.filter(sold_at__gte=month_start).aggregate(
        s=Sum('price')
    )['s'] or 0
    sales_last_30d = SalesRecord.objects.filter(sold_at__gte=start_30d).count()

    top_sellers = SalesRecord.objects.values('seller_email').annotate(
        sales_count=Count('id'),
        total_revenue=Sum('price'),
    ).order_by('-sales_count')[:10]

    top_brands = SalesRecord.objects.filter(brand__isnull=False).values(
        'brand__name'
    ).annotate(
        sales_count=Count('id'),
        avg_price=Avg('price'),
    ).order_by('-sales_count')[:10]

    # ═══ Sales chart (last 30 days) ═══
    daily = defaultdict(int)
    for r in SalesRecord.objects.filter(sold_at__gte=start_30d):
        daily[r.sold_at.date()] += 1

    chart_labels = []
    chart_data = []
    current = start_30d.date()
    end = now.date()
    while current <= end:
        chart_labels.append(current.strftime('%Y-%m-%d'))
        chart_data.append(daily.get(current, 0))
        current += timedelta(days=1)

    # ═══ Listings created chart (last 30 days) ═══
    daily_listings = defaultdict(int)
    for l in Listing.objects.filter(created_at__gte=start_30d).only('created_at'):
        daily_listings[l.created_at.date()] += 1

    listings_chart_labels = []
    listings_chart_data = []
    current = start_30d.date()
    while current <= end:
        listings_chart_labels.append(current.strftime('%Y-%m-%d'))
        listings_chart_data.append(daily_listings.get(current, 0))
        current += timedelta(days=1)

    recent_sales = SalesRecord.objects.select_related('brand', 'model').order_by('-sold_at')[:20]

    # ════════════════════════════════════════════════════
    # ═══ LISTINGS BREAKDOWN ═══
    # ════════════════════════════════════════════════════

    # By category (vehicle_type)
    listings_by_category = list(
        Listing.objects.filter(status__in=['active', 'sold'])
        .values('vehicle_type__name', 'vehicle_type__slug')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    total_real_listings = sum(c['count'] for c in listings_by_category) or 1
    for c in listings_by_category:
        c['percent'] = round(c['count'] * 100.0 / total_real_listings, 1)

    # By country
    listings_by_country = list(
        Listing.objects.filter(status__in=['active', 'sold'])
        .exclude(country__isnull=True).exclude(country='')
        .values('country')
        .annotate(count=Count('id'))
        .order_by('-count')[:10]
    )

    # By US state
    listings_by_state = list(
        Listing.objects.filter(status__in=['active', 'sold'], country='US')
        .exclude(state__isnull=True).exclude(state='')
        .values('state')
        .annotate(count=Count('id'))
        .order_by('-count')[:10]
    )

    # By brand (top 20)
    listings_by_brand = list(
        Listing.objects.filter(status__in=['active', 'sold'], brand__isnull=False)
        .values('brand__name')
        .annotate(count=Count('id'), avg_price=Avg('price'))
        .order_by('-count')[:20]
    )

    # By fuel type
    listings_by_fuel = list(
        Listing.objects.filter(status__in=['active', 'sold'], fuel_type__isnull=False)
        .values('fuel_type__name')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    # By body type
    listings_by_body = list(
        Listing.objects.filter(status__in=['active', 'sold'])
        .exclude(body_type__isnull=True).exclude(body_type='')
        .values('body_type')
        .annotate(count=Count('id'))
        .order_by('-count')[:10]
    )

    # Quality metrics
    real_qs = Listing.objects.filter(status__in=['active', 'sold'])
    real_count = real_qs.count() or 1
    listings_with_vin = real_qs.exclude(vin__isnull=True).exclude(vin='').count()
    listings_with_5plus_photos = real_qs.annotate(
        img_count=Count('images')
    ).filter(img_count__gte=5).count()
    pct_with_vin = round(listings_with_vin * 100.0 / real_count, 1)
    pct_with_5plus = round(listings_with_5plus_photos * 100.0 / real_count, 1)

    # Avg images per listing
    avg_images = ListingImage.objects.filter(
        listing__status__in=['active', 'sold']
    ).count() / real_count if real_count > 0 else 0
    avg_images = round(avg_images, 1)

    # Stale listings (active 90+ days, no recent boost)
    stale_listings_count = Listing.objects.filter(
        status='active',
        created_at__lt=start_90d,
    ).count()

    # Top viewed listings (top 10)
    top_viewed = list(
        Listing.objects.filter(status='active')
        .select_related('brand', 'model')
        .order_by('-views_count')[:10]
    )

    # ════════════════════════════════════════════════════
    # ═══ USERS STATS ═══
    # ════════════════════════════════════════════════════

    total_users = User.objects.count()
    new_users_today = User.objects.filter(date_joined__gte=today_start).count()
    new_users_week = User.objects.filter(date_joined__gte=week_ago).count()
    new_users_month = User.objects.filter(date_joined__gte=start_30d).count()

    # Active sellers (created at least 1 listing in period)
    active_sellers_today = Listing.objects.filter(
        created_at__gte=today_start
    ).values('seller').distinct().count()
    active_sellers_week = Listing.objects.filter(
        created_at__gte=week_ago
    ).values('seller').distinct().count()
    active_sellers_month = Listing.objects.filter(
        created_at__gte=start_30d
    ).values('seller').distinct().count()

    # Top sellers by listings count
    top_sellers_by_listings = list(
        Listing.objects.filter(status__in=['active', 'sold'])
        .values('seller__email', 'seller__id')
        .annotate(
            listings_count=Count('id'),
            active_count=Count('id', filter=Q(status='active')),
            sold_count=Count('id', filter=Q(status='sold')),
        )
        .order_by('-listings_count')[:10]
    )

    # New users chart (last 30 days)
    daily_users = defaultdict(int)
    for u in User.objects.filter(date_joined__gte=start_30d).only('date_joined'):
        daily_users[u.date_joined.date()] += 1

    users_chart_labels = []
    users_chart_data = []
    current = start_30d.date()
    while current <= end:
        users_chart_labels.append(current.strftime('%Y-%m-%d'))
        users_chart_data.append(daily_users.get(current, 0))
        current += timedelta(days=1)

    # ════════════════════════════════════════════════════
    # ═══ ENGAGEMENT STATS ═══
    # ════════════════════════════════════════════════════

    saved_listings_total = SavedListing.objects.count()
    saved_listings_today = SavedListing.objects.filter(
        created_at__gte=today_start
    ).count() if hasattr(SavedListing, 'created_at') else 0

    total_listing_views = ListingView.objects.count()
    views_today = ListingView.objects.filter(
        viewed_at__gte=today_start
    ).count() if hasattr(ListingView, 'viewed_at') else 0
    views_week = ListingView.objects.filter(
        viewed_at__gte=week_ago
    ).count() if hasattr(ListingView, 'viewed_at') else 0

    conversations_total = 0
    messages_total = 0
    saved_searches_total = 0
    try:
        from .models import Conversation
        conversations_total = Conversation.objects.count()
    except (ImportError, Exception):
        pass
    try:
        from .models import Message
        messages_total = Message.objects.count()
    except (ImportError, Exception):
        pass
    try:
        from .models import SavedSearch
        saved_searches_total = SavedSearch.objects.count()
    except (ImportError, Exception):
        pass

    # Listings without views (dead)
    listings_no_views = Listing.objects.filter(
        status='active',
        views_count=0,
    ).count()

    # Listings without saves
    saved_listing_ids = SavedListing.objects.values_list('listing_id', flat=True).distinct()
    listings_no_saves = Listing.objects.filter(
        status='active',
    ).exclude(id__in=saved_listing_ids).count()

    # ════════════════════════════════════════════════════
    # ═══ PRICE INSIGHTS ═══
    # ════════════════════════════════════════════════════

    real_prices = list(real_qs.exclude(price=0).values_list('price', flat=True).order_by('price'))
    median_price = 0
    if real_prices:
        n = len(real_prices)
        if n % 2 == 0:
            median_price = (real_prices[n//2 - 1] + real_prices[n//2]) / 2
        else:
            median_price = real_prices[n//2]
    median_price = round(float(median_price), 0)

    price_buckets = [
        ('< $1k',       0,      1000),
        ('$1k–5k',      1000,   5000),
        ('$5k–10k',     5000,   10000),
        ('$10k–25k',    10000,  25000),
        ('$25k–50k',    25000,  50000),
        ('$50k–100k',   50000,  100000),
        ('$100k+',      100000, 999999999),
    ]
    price_distribution = []
    for label, lo, hi in price_buckets:
        count = real_qs.filter(price__gte=lo, price__lt=hi).count()
        price_distribution.append({'label': label, 'count': count})

    avg_price_by_category = list(
        Listing.objects.filter(status__in=['active', 'sold'])
        .exclude(price=0)
        .values('vehicle_type__name', 'vehicle_type__slug')
        .annotate(avg_price=Avg('price'), count=Count('id'))
        .order_by('-count')
    )

    ttm_buckets = [
        ('< 7 days',    0,      7),
        ('7–14 days',   7,      14),
        ('14–30 days',  14,     30),
        ('30–60 days',  30,     60),
        ('60–90 days',  60,     90),
        ('90+ days',    90,     999999),
    ]
    time_to_sell_distribution = []
    for label, lo, hi in ttm_buckets:
        count = SalesRecord.objects.filter(days_active__gte=lo, days_active__lt=hi).count()
        time_to_sell_distribution.append({'label': label, 'count': count})

    avg_sale_ratio = None
    try:
        ratios = []
        for r in SalesRecord.objects.exclude(asking_price__isnull=True).exclude(asking_price=0)[:200]:
            if r.asking_price and r.asking_price > 0:
                ratios.append(float(r.price) / float(r.asking_price))
        if ratios:
            avg_sale_ratio = round(sum(ratios) / len(ratios) * 100, 1)
    except Exception:
        avg_sale_ratio = None

    # ════════════════════════════════════════════════════
    # ═══ BEST DAY / HOUR TO POST ═══
    # ════════════════════════════════════════════════════

    weekday_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_counts = [0] * 7
    for l in Listing.objects.filter(created_at__gte=start_30d).only('created_at'):
        weekday_counts[l.created_at.weekday()] += 1

    weekday_chart_labels = json.dumps(weekday_names)
    weekday_chart_data = json.dumps(weekday_counts)

    hour_counts = [0] * 24
    for l in Listing.objects.filter(created_at__gte=start_30d).only('created_at'):
        hour_counts[l.created_at.hour] += 1

    hour_chart_labels = json.dumps([f'{h}:00' for h in range(24)])
    hour_chart_data = json.dumps(hour_counts)

    peak_weekday_idx = weekday_counts.index(max(weekday_counts)) if any(weekday_counts) else 0
    peak_weekday_name = weekday_names[peak_weekday_idx]
    peak_weekday_count = max(weekday_counts) if weekday_counts else 0

    peak_hour_idx = hour_counts.index(max(hour_counts)) if any(hour_counts) else 0
    peak_hour_count = max(hour_counts) if hour_counts else 0

    # ════════════════════════════════════════════════════
    # ═══ EMAIL STATS ═══
    # ════════════════════════════════════════════════════

    emails_today = 0
    emails_week = 0
    emails_month = 0
    top_email_scenarios = []
    try:
        from .models import EmailLog
        emails_today = EmailLog.objects.filter(sent_at__gte=today_start).count()
        emails_week = EmailLog.objects.filter(sent_at__gte=week_ago).count()
        emails_month = EmailLog.objects.filter(sent_at__gte=start_30d).count()
        top_email_scenarios = list(
            EmailLog.objects.filter(sent_at__gte=start_30d)
            .values('scenario')
            .annotate(count=Count('id'))
            .order_by('-count')[:10]
        )
    except (ImportError, Exception):
        pass

    if emails_today == 0 and emails_month == 0:
        try:
            from .models import EmailScenarioLog
            emails_today = EmailScenarioLog.objects.filter(sent_at__gte=today_start).count()
            emails_week = EmailScenarioLog.objects.filter(sent_at__gte=week_ago).count()
            emails_month = EmailScenarioLog.objects.filter(sent_at__gte=start_30d).count()
            top_email_scenarios = list(
                EmailScenarioLog.objects.filter(sent_at__gte=start_30d)
                .values('scenario')
                .annotate(count=Count('id'))
                .order_by('-count')[:10]
            )
        except (ImportError, Exception):
            pass

    # ════════════════════════════════════════════════════
    # ═══ WEEK-OVER-WEEK GROWTH ═══
    # ════════════════════════════════════════════════════

    two_weeks_ago = now - timedelta(days=14)

    wow_listings_this = Listing.objects.filter(
        created_at__gte=week_ago
    ).count()
    wow_sales_this = SalesRecord.objects.filter(
        sold_at__gte=week_ago
    ).count()
    wow_users_this = User.objects.filter(
        date_joined__gte=week_ago
    ).count()
    wow_revenue_this = SalesRecord.objects.filter(
        sold_at__gte=week_ago
    ).aggregate(s=Sum('price'))['s'] or 0

    wow_listings_prev = Listing.objects.filter(
        created_at__gte=two_weeks_ago, created_at__lt=week_ago
    ).count()
    wow_sales_prev = SalesRecord.objects.filter(
        sold_at__gte=two_weeks_ago, sold_at__lt=week_ago
    ).count()
    wow_users_prev = User.objects.filter(
        date_joined__gte=two_weeks_ago, date_joined__lt=week_ago
    ).count()
    wow_revenue_prev = SalesRecord.objects.filter(
        sold_at__gte=two_weeks_ago, sold_at__lt=week_ago
    ).aggregate(s=Sum('price'))['s'] or 0

    def _pct_change(curr, prev):
        if prev == 0:
            return None if curr == 0 else 100.0
        return round((curr - prev) * 100.0 / prev, 1)

    wow_listings_change = _pct_change(wow_listings_this, wow_listings_prev)
    wow_sales_change = _pct_change(wow_sales_this, wow_sales_prev)
    wow_users_change = _pct_change(wow_users_this, wow_users_prev)
    wow_revenue_change = _pct_change(float(wow_revenue_this), float(wow_revenue_prev))

    # ════════════════════════════════════════════════════
    # ═══ GEOGRAPHIC INSIGHTS ═══
    # ════════════════════════════════════════════════════

    geo_top_cities = list(
        Listing.objects.filter(status__in=['active', 'sold'])
        .exclude(city__isnull=True).exclude(city='')
        .values('city', 'country')
        .annotate(count=Count('id'))
        .order_by('-count')[:15]
    )

    geo_price_by_country = list(
        Listing.objects.filter(status__in=['active', 'sold'])
        .exclude(country__isnull=True).exclude(country='').exclude(price=0)
        .values('country')
        .annotate(count=Count('id'), avg_price=Avg('price'))
        .order_by('-count')[:10]
    )

    geo_price_by_state = list(
        Listing.objects.filter(status__in=['active', 'sold'], country='US')
        .exclude(state__isnull=True).exclude(state='').exclude(price=0)
        .values('state')
        .annotate(count=Count('id'), avg_price=Avg('price'))
        .order_by('-count')[:10]
    )

    # ════════════════════════════════════════════════════
    # ═══ HOT + DEAD LISTINGS ═══
    # ════════════════════════════════════════════════════

    hot_listings = list(
        Listing.objects.filter(status='active', views_count__gte=50)
        .select_related('brand', 'model')
        .order_by('-views_count')[:10]
    )

    dead_listings = list(
        Listing.objects.filter(
            status='active',
            views_count=0,
            created_at__lt=week_ago,
        )
        .select_related('brand', 'model')
        .order_by('created_at')[:10]
    )

    hot_listings_count = Listing.objects.filter(
        status='active', views_count__gte=50
    ).count()
    dead_listings_count = Listing.objects.filter(
        status='active', views_count=0, created_at__lt=week_ago
    ).count()

    # ════════════════════════════════════════════════════

    # ═══ VISITOR TRAFFIC (analytics_pageview) ═══

    # ════════════════════════════════════════════════════

    from apps.analytics.models import PageView

    from collections import defaultdict as _dd



    _human_qs = PageView.objects.filter(is_bot=False)



    def _unique_ips(start):

        return set(_human_qs.filter(created_at__gte=start).values_list('ip_address', flat=True))



    _ips_today = _unique_ips(today_start)

    _ips_week = _unique_ips(week_ago)

    _ips_month = _unique_ips(start_30d)



    visitors_today = len(_ips_today)

    visitors_week = len(_ips_week)

    visitors_month = len(_ips_month)



    _before_today = set(_human_qs.filter(created_at__lt=today_start).values_list('ip_address', flat=True))

    _before_week = set(_human_qs.filter(created_at__lt=week_ago).values_list('ip_address', flat=True))

    _before_month = set(_human_qs.filter(created_at__lt=start_30d).values_list('ip_address', flat=True))



    returning_visitors_today = len(_ips_today & _before_today)

    returning_visitors_week = len(_ips_week & _before_week)

    returning_visitors_month = len(_ips_month & _before_month)



    new_visitors_today = visitors_today - returning_visitors_today

    new_visitors_week = visitors_week - returning_visitors_week

    new_visitors_month = visitors_month - returning_visitors_month



    _daily_ips = _dd(set)

    for _ip, _ts in _human_qs.filter(created_at__gte=start_30d).values_list('ip_address', 'created_at'):

        _daily_ips[_ts.date()].add(_ip)



    traffic_labels_list = []

    traffic_unique_list = []

    _cur = start_30d.date()

    _end_d = now.date()

    while _cur <= _end_d:

        traffic_labels_list.append(_cur.strftime('%Y-%m-%d'))

        traffic_unique_list.append(len(_daily_ips.get(_cur, ())))

        _cur += timedelta(days=1)



    top_countries_data = list(

        _human_qs.filter(created_at__gte=start_30d)

        .exclude(country='')

        .values('country', 'country_name')

        .annotate(visitors=Count('ip_address', distinct=True))

        .order_by('-visitors')[:10]

    )

    total_country_visitors = (

        _human_qs.filter(created_at__gte=start_30d)

        .exclude(country='')

        .values('ip_address').distinct().count()

    )

    for _c in top_countries_data:

        _c['percent'] = round(_c['visitors'] * 100.0 / total_country_visitors, 1) if total_country_visitors else 0



    context = {

        'visitors_today': visitors_today,

        'visitors_week': visitors_week,

        'visitors_month': visitors_month,

        'new_visitors_today': new_visitors_today,

        'new_visitors_week': new_visitors_week,

        'new_visitors_month': new_visitors_month,

        'returning_visitors_today': returning_visitors_today,

        'returning_visitors_week': returning_visitors_week,

        'returning_visitors_month': returning_visitors_month,

        'traffic_chart_labels': json.dumps(traffic_labels_list),

        'traffic_chart_unique': json.dumps(traffic_unique_list),

        'top_countries_data': top_countries_data,

        'total_country_visitors': total_country_visitors,

        'total_listings': total_listings,
        'active_listings': active_listings,
        'sold_listings_displayed': sold_listings_displayed,
        'inactive_listings': inactive_listings,
        'shadow_banned': shadow_banned,
        'listings_today': listings_today,
        'listings_week': listings_week,
        'listings_month': listings_month,
        'listings_today_real': listings_today_real,
        'listings_week_real': listings_week_real,
        'listings_month_real': listings_month_real,
        'total_sales': total_sales,
        'total_revenue': total_revenue,
        'avg_price': round(float(avg_price), 2),
        'avg_days_active': round(float(avg_days_active), 1),
        'sales_this_month': sales_this_month,
        'revenue_this_month': revenue_this_month,
        'sales_last_30d': sales_last_30d,
        'top_sellers': top_sellers,
        'top_brands': top_brands,
        'recent_sales': recent_sales,
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
        'listings_chart_labels': json.dumps(listings_chart_labels),
        'listings_chart_data': json.dumps(listings_chart_data),
        # Listings Breakdown
        'listings_by_category': listings_by_category,
        'listings_by_country': listings_by_country,
        'listings_by_state': listings_by_state,
        'listings_by_brand': listings_by_brand,
        'listings_by_fuel': listings_by_fuel,
        'listings_by_body': listings_by_body,
        'pct_with_vin': pct_with_vin,
        'pct_with_5plus': pct_with_5plus,
        'avg_images': avg_images,
        'stale_listings_count': stale_listings_count,
        'top_viewed': top_viewed,
        # Users
        'total_users': total_users,
        'new_users_today': new_users_today,
        'new_users_week': new_users_week,
        'new_users_month': new_users_month,
        'active_sellers_today': active_sellers_today,
        'active_sellers_week': active_sellers_week,
        'active_sellers_month': active_sellers_month,
        'top_sellers_by_listings': top_sellers_by_listings,
        'users_chart_labels': json.dumps(users_chart_labels),
        'users_chart_data': json.dumps(users_chart_data),
        # Engagement
        'saved_listings_total': saved_listings_total,
        'saved_listings_today': saved_listings_today,
        'total_listing_views': total_listing_views,
        'views_today': views_today,
        'views_week': views_week,
        'conversations_total': conversations_total,
        'messages_total': messages_total,
        'saved_searches_total': saved_searches_total,
        'listings_no_views': listings_no_views,
        'listings_no_saves': listings_no_saves,
        # Price Insights
        'median_price': median_price,
        'price_distribution': price_distribution,
        'avg_price_by_category': avg_price_by_category,
        'time_to_sell_distribution': time_to_sell_distribution,
        'avg_sale_ratio': avg_sale_ratio,
        # Best Day/Hour
        'weekday_chart_labels': weekday_chart_labels,
        'weekday_chart_data': weekday_chart_data,
        'hour_chart_labels': hour_chart_labels,
        'hour_chart_data': hour_chart_data,
        'peak_weekday_name': peak_weekday_name,
        'peak_weekday_count': peak_weekday_count,
        'peak_hour_idx': peak_hour_idx,
        'peak_hour_count': peak_hour_count,
        # Email stats
        'emails_today': emails_today,
        'emails_week': emails_week,
        'emails_month': emails_month,
        'top_email_scenarios': top_email_scenarios,
        # Week-over-week
        'wow_listings_this': wow_listings_this,
        'wow_listings_prev': wow_listings_prev,
        'wow_listings_change': wow_listings_change,
        'wow_sales_this': wow_sales_this,
        'wow_sales_prev': wow_sales_prev,
        'wow_sales_change': wow_sales_change,
        'wow_users_this': wow_users_this,
        'wow_users_prev': wow_users_prev,
        'wow_users_change': wow_users_change,
        'wow_revenue_this': wow_revenue_this,
        'wow_revenue_prev': wow_revenue_prev,
        'wow_revenue_change': wow_revenue_change,
        # Geographic
        'geo_top_cities': geo_top_cities,
        'geo_price_by_country': geo_price_by_country,
        'geo_price_by_state': geo_price_by_state,
        # Hot + Dead listings
        'hot_listings': hot_listings,
        'dead_listings': dead_listings,
        'hot_listings_count': hot_listings_count,
        'dead_listings_count': dead_listings_count,
    }
    return render(request, 'listings/admin_sales_stats.html', context)


# ════════════════════════════════════════════════════════════════════
# QUICK FORM — CREATE + EDIT (vienas URL su ?edit=<pk> param)
# ════════════════════════════════════════════════════════════════════

@login_required
def listing_create_cars_quick(request):
    """
    Quick mode: visi laukai vienoje formoje.
    Palaiko ABU režimus:
      - CREATE (be ?edit) — sukuria draft, activate'ina į active listing
      - EDIT (?edit=<pk>) — atnaujina esamą listing tiesiogiai

    URL: /create/cars/quick/
    URL EDIT: /create/cars/quick/?edit=<pk>
    """
    cars_vt = VehicleType.objects.filter(slug='cars').first()
    if not cars_vt:
        messages.error(request, 'Cars category not configured.')
        return redirect('listing_list')

    # ═══ EDIT MODE detection ═══
    edit_pk = _int_or_none(request.GET.get('edit')) or _int_or_none(request.POST.get('edit'))
    is_edit_mode = bool(edit_pk)
    listing = None

    if is_edit_mode:
        listing = get_object_or_404(
            Listing,
            pk=edit_pk,
            seller=request.user,
        )
        if not listing.vehicle_type or listing.vehicle_type.slug != 'cars':
            messages.error(request, 'Quick edit is only available for cars.')
            return redirect('listing_edit_hub', pk=edit_pk)

    # ═══ LISTING LIMIT GUARD (CREATE mode only) ═══
    if not is_edit_mode:
        can_create, active_count, limit = can_create_listing(request.user)
        if not can_create:
            messages.error(
                request,
                f'You have reached your active listings limit ({active_count}/{limit}). '
                f'Upgrade your account to create more listings.',
            )
            return redirect('listing_upgrade')

    # ═══ NEW FORM (be ?edit, be ?draft, be ?keep) ═══
    resume_draft_id = _int_or_none(request.GET.get('draft'))
    if not is_edit_mode and request.method == 'GET' and not resume_draft_id and not request.GET.get('keep'):
        if CARS_DRAFT_SESSION_KEY in request.session:
            request.session[CARS_DRAFT_SESSION_KEY] = None
        request.session.modified = True

    # ═══ RESUME draft (only CREATE) ═══
    if not is_edit_mode and resume_draft_id:
        try:
            existing = Listing.objects.get(
                pk=resume_draft_id,
                seller=request.user,
                status='draft',
                vehicle_type=cars_vt,
            )
            request.session[CARS_DRAFT_SESSION_KEY] = existing.pk
            request.session.modified = True
        except Listing.DoesNotExist:
            messages.error(request, 'Draft not found.')
            return redirect('listing_create_cars_quick')

    # ═══ Get current draft from session (CREATE mode) ═══
    current_draft = None
    if not is_edit_mode:
        draft_id = request.session.get(CARS_DRAFT_SESSION_KEY)
        if draft_id:
            try:
                current_draft = Listing.objects.get(
                    pk=draft_id,
                    seller=request.user,
                    status='draft',
                )
            except Listing.DoesNotExist:
                request.session[CARS_DRAFT_SESSION_KEY] = None
                current_draft = None

    listing_data = _draft_to_session_data(listing if is_edit_mode else current_draft)

    # ═══════════════════════════════════════════════════════════════
    # POST: PILNAS SUBMIT
    # ═══════════════════════════════════════════════════════════════
    if request.method == 'POST':
        # CREATE: sukuriam draft jei dar nėra
        if not is_edit_mode and not current_draft:
            current_draft = _get_or_create_cars_draft(
                request,
                vehicle_type_id=cars_vt.pk,
            )
            if not current_draft:
                messages.error(request, 'Could not create draft.')
                return redirect('listing_create_cars_quick')

        # target — listing (EDIT) arba current_draft (CREATE)
        target = listing if is_edit_mode else current_draft
        old_price = float(target.price) if (is_edit_mode and target.price) else 0

        errors = []

        # ─── Section 1: Brand/Model/Year (tik CREATE) ───
        if not is_edit_mode:
            brand_id = _int_or_none(request.POST.get('brand'))
            model_id = _int_or_none(request.POST.get('model'))
            year = _int_or_none(request.POST.get('year'))
            month = _int_or_none(request.POST.get('month'))

            if brand_id:
                try:
                    target.brand = Brand.objects.get(pk=brand_id)
                except Brand.DoesNotExist:
                    errors.append('Brand not found')
            else:
                errors.append('Brand is required')

            if model_id:
                try:
                    target.model = Model.objects.get(pk=model_id)
                except Model.DoesNotExist:
                    errors.append('Model not found')
            else:
                errors.append('Model is required')

            if not year:
                errors.append('Year is required')
            else:
                target.year = year
                if month:
                    try:
                        target.first_registration = date(year=year, month=month, day=1)
                    except (ValueError, TypeError):
                        errors.append('Invalid month/year combination')

        # VIN editable both modes
        target.vin = (request.POST.get('vin', '') or '').strip().upper()

        # ─── Section 3: Technical Details ───
        body_type = request.POST.get('body_type', '')
        if not body_type:
            errors.append('Body Type is required')
        target.body_type = body_type

        ft_id = _int_or_none(request.POST.get('fuel_type'))
        if not ft_id:
            errors.append('Fuel Type is required')
        else:
            try:
                target.fuel_type = FuelType.objects.get(pk=ft_id)
            except FuelType.DoesNotExist:
                errors.append('Fuel Type not found')

        tr_id = _int_or_none(request.POST.get('transmission'))
        if not tr_id:
            errors.append('Transmission is required')
        else:
            try:
                target.transmission = Transmission.objects.get(pk=tr_id)
            except Transmission.DoesNotExist:
                errors.append('Transmission not found')

        doors = request.POST.get('doors', '')
        if not doors:
            errors.append('Doors is required')
        target.doors = doors

        condition = request.POST.get('condition', '')
        if not condition:
            errors.append('Condition is required')
        target.condition = condition

        defects = request.POST.get('defects', '')
        if not defects:
            errors.append('Defects is required')
        target.defects = defects

        mileage = _int_or_none(request.POST.get('mileage'))
        if mileage is None:
            errors.append('Mileage is required')
        else:
            target.mileage = mileage

        # Optional Section 3 fields
        target.color = request.POST.get('color', '')
        target.steering = request.POST.get('steering', '')
        target.engine_capacity = _float_or_none(request.POST.get('engine_capacity'))
        target.power = _int_or_none(request.POST.get('power'))
        target.drive_type = request.POST.get('drive_type', '')
        target.seats = request.POST.get('seats', '')
        target.rim_size = request.POST.get('rim_size', '')
        target.climate = request.POST.get('climate', '')
        target.curb_weight = _int_or_none(request.POST.get('curb_weight'))
        target.euro_standard = request.POST.get('euro_standard', '')
        target.co2_emission = _int_or_none(request.POST.get('co2_emission'))
        target.fuel_consumption_city = _float_or_none(request.POST.get('fuel_consumption_city'))
        target.fuel_consumption_highway = _float_or_none(request.POST.get('fuel_consumption_highway'))
        target.fuel_consumption_combined = _float_or_none(request.POST.get('fuel_consumption_combined'))
        target.origin_country = request.POST.get('origin_country', '')
        target.technical_inspection_month = _int_or_none(request.POST.get('technical_inspection_month'))
        target.technical_inspection_year = _int_or_none(request.POST.get('technical_inspection_year'))

        # ─── Price ───
        price = _float_or_none(request.POST.get('price'))
        if price is None or price <= 0:
            errors.append('Price is required')
        else:
            target.price = price
        target.negotiable = request.POST.get('negotiable') == 'on'

        # ─── Export price + Trade + Taxes ───
        target.export_price = _float_or_none(request.POST.get('export_price'))
        target.open_to_trade = request.POST.get('open_to_trade') == 'on'
        target.taxes_extra = request.POST.get('taxes_extra') == 'on'

        # ─── Special features (sidebar filter fields) ───
        target.has_warranty = request.POST.get('has_warranty') == 'on'
        target.available_on_lease = request.POST.get('available_on_lease') == 'on'
        target.is_sport_ready = request.POST.get('is_sport_ready') == 'on'
        target.disabled_friendly = request.POST.get('disabled_friendly') == 'on'
        target.has_service_book = request.POST.get('has_service_book') == 'on'
        target.imported_from_us = request.POST.get('imported_from_us') == 'on'
        target.multiple_keys = request.POST.get('multiple_keys') == 'on'
        target.power_boosted = request.POST.get('power_boosted') == 'on'
        target.pneumatic_suspension = request.POST.get('pneumatic_suspension') == 'on'
        target.remote_start = request.POST.get('remote_start') == 'on'
        target.spare_wheel = request.POST.get('spare_wheel') == 'on'
        target.valid_inspection = request.POST.get('valid_inspection') == 'on'
        target.is_auction = request.POST.get('is_auction') == 'on'
        target.seller_type = request.POST.get('seller_type', 'private')

        # ─── Description + Video ───
        target.description = request.POST.get('description', '') or ''
        target.video_url = request.POST.get('video_url', '') or ''

        # ─── Location + Contact ───
        country = request.POST.get('country', 'US')
        target.country = country
        if country == 'US':
            state = request.POST.get('state', '')
            if not state:
                errors.append('State is required')
            if hasattr(target, 'state'):
                target.state = state
            target.city = request.POST.get('city', '') or '—'
        else:
            city = request.POST.get('city', '')
            if not city:
                errors.append('City is required')
            target.city = city
            if hasattr(target, 'state'):
                target.state = ''

        target.postal_code = request.POST.get('postal_code', '')
        target.address = request.POST.get('address', '')
        target.hide_exact_address = request.POST.get('hide_exact_address') == 'on'

        # Phone — į user.profile (autoplius style)
        phone_val = (request.POST.get('phone', '') or '').strip()
        if not phone_val:
            errors.append('Phone is required')
        elif hasattr(request.user, 'profile'):
            request.user.profile.phone_number = phone_val
            request.user.profile.save(update_fields=['phone_number'])

        # Terms agreement (tik CREATE)
        if not is_edit_mode and not request.POST.get('agree_terms'):
            errors.append('You must agree to the terms')

        # ─── Equipment ───
        equipment_ids = request.POST.getlist('equipment')

        # ─── Photo upload (failsafe) ───
        new_images = request.FILES.getlist('images')
        try:
            validate_images(new_images)
        except ImageValidationError as exc:
            errors.append(str(exc))

        if errors:
            for e in errors:
                messages.error(request, e)
            try:
                if not is_edit_mode and target.brand and target.year:
                    title_parts = [target.brand.name]
                    if target.model:
                        title_parts.append(target.model.name)
                    title_parts.append(str(target.year))
                    target.title = ' '.join(title_parts)
                target.save()
            except Exception as e:
                print(f"[quick_form] partial save failed: {e}")

            listing_data = _draft_to_session_data(target)
            return _render_quick_form(
                request,
                current_draft if not is_edit_mode else None,
                listing_data,
                listing=listing if is_edit_mode else None,
                is_edit_mode=is_edit_mode,
            )

        # ─── Validation passed — finalize ───

        # Update title (CREATE only)
        if not is_edit_mode and target.brand and target.year:
            title_parts = [target.brand.name]
            if target.model:
                title_parts.append(target.model.name)
            title_parts.append(str(target.year))
            target.title = ' '.join(title_parts)

        # Coordinates
        lat, lng = get_coordinates_for_location(target.city, target.country)
        target.latitude = lat
        target.longitude = lng

        try:
            target.save()
        except Exception as e:
            messages.error(request, f'Save failed: {e}')
            return _render_quick_form(
                request,
                current_draft if not is_edit_mode else None,
                listing_data,
                listing=listing if is_edit_mode else None,
                is_edit_mode=is_edit_mode,
            )

        # Equipment — replace
        ListingEquipment.objects.filter(listing=target).delete()
        for eid in equipment_ids:
            try:
                eid_int = int(eid)
                ListingEquipment.objects.create(
                    listing=target,
                    equipment_id=eid_int,
                )
            except (ValueError, TypeError):
                pass

        # Photo upload (jeigu yra failsafe failai POST)
        existing_count = target.images.count()
        for i, image in enumerate(new_images[:40]):
            try:
                ListingImage.objects.create(
                    listing=target,
                    image=image,
                    is_main=(existing_count == 0 and i == 0),
                    order=existing_count + i,
                )
            except Exception as e:
                print(f"[quick_form] image upload failed: {e}")

        # ═══ EDIT mode: notify + redirect ═══
        if is_edit_mode:
            try:
                new_price = float(target.price)
                if new_price != old_price and old_price > 0:
                    if new_price < old_price:
                        _send_saved_listing_price_drop_emails(target, old_price, new_price)
                    else:
                        summary = (
                            f'Price changed from '
                            f'{target.currency_symbol}{int(old_price)} to '
                            f'{target.currency_symbol}{int(new_price)}'
                        )
                        _send_saved_listing_updated_emails(target, summary)
                else:
                    _send_saved_listing_updated_emails(target, 'Listing updated')
            except (ValueError, TypeError):
                pass

            messages.success(request, 'Listing updated successfully.')
            return redirect('listing_edit_hub', pk=target.pk)

        # ═══ CREATE mode: check free tier vs paid plan ═══
        from .constants import can_create_free_listing, FREE_LISTING_DAYS

        is_free, active_count, free_limit = can_create_free_listing(request.user)

        if is_free:
            # Pirmi 3 skelbimai — auto-publish 30 dienų (nemokami)
            target.activate(days=FREE_LISTING_DAYS)
            _send_listing_published_email(target, request.user)
            request.session[CARS_DRAFT_SESSION_KEY] = None
            request.session.modified = True
            return redirect(
                reverse('listing_success', kwargs={'pk': target.pk}) + '?action=published'
            )
        else:
            # 4-as+ skelbimas — redirect į planų puslapį, NE auto-publish
            request.session[CARS_DRAFT_SESSION_KEY] = None
            request.session.modified = True
            return redirect('listing_select_plan', pk=target.pk)

    # ═══ GET: render template ═══
    return _render_quick_form(
        request,
        current_draft,
        listing_data,
        listing=listing,
        is_edit_mode=is_edit_mode,
    )


def _render_quick_form(request, current_draft, listing_data, listing=None, is_edit_mode=False):
    """Helper: render quick form template with all needed context.

    Args:
        request: HttpRequest
        current_draft: Listing draft (CREATE mode)
        listing_data: dict from _draft_to_session_data
        listing: Listing instance (EDIT mode)
        is_edit_mode: bool — True if editing existing listing
    """
    from itertools import groupby

    # source = listing (EDIT) arba draft (CREATE)
    source = listing if is_edit_mode else current_draft

    initial_step3 = {}
    initial_step5 = {}
    initial_step6 = {}
    initial_step7 = {}

    if source:
        initial_step3 = {
            'body_type': source.body_type,
            'fuel_type': source.fuel_type,
            'transmission': source.transmission,
            'doors': source.doors,
            'condition': source.condition,
            'color': source.color,
            'defects': source.defects,
            'steering': source.steering,
            'mileage': source.mileage,
            'engine_capacity': source.engine_capacity,
            'power': source.power,
            'drive_type': source.drive_type,
            'seats': source.seats,
            'rim_size': source.rim_size,
            'climate': source.climate,
            'curb_weight': source.curb_weight,
            'euro_standard': source.euro_standard,
            'co2_emission': source.co2_emission,
            'fuel_consumption_city': source.fuel_consumption_city,
            'fuel_consumption_highway': source.fuel_consumption_highway,
            'fuel_consumption_combined': source.fuel_consumption_combined,
            'origin_country': source.origin_country,
            'technical_inspection_month': source.technical_inspection_month,
            'technical_inspection_year': source.technical_inspection_year,
        }
        if source.price and source.price > 0:
            initial_step5 = {'price': source.price, 'negotiable': source.negotiable}
        initial_step6 = {'description': source.description}

        # Phone from profile
        user_phone = ''
        if hasattr(request.user, 'profile') and request.user.profile.phone_number:
            user_phone = request.user.profile.phone_number

        initial_step7 = {
            'country': source.country or 'US',
            'city': source.city if source.city != '—' else '',
            'postal_code': source.postal_code,
            'address': source.address,
            'hide_exact_address': source.hide_exact_address,
            'phone': user_phone,
            'email': request.user.email,
        }
    else:
        user_phone = ''
        if hasattr(request.user, 'profile') and request.user.profile.phone_number:
            user_phone = request.user.profile.phone_number
        initial_step7 = {
            'country': 'US',
            'phone': user_phone,
            'email': request.user.email,
        }

    media_form = Step2MediaForm(initial={'video_url': source.video_url if source else ''})
    step3_form = Step3VehicleDataForm(initial=initial_step3)
    step4_form = Step4EquipmentForm(initial={
        'equipment': list(source.equipment_items.values_list('equipment_id', flat=True))
        if source else []
    })
    step5_form = Step5PriceForm(initial=initial_step5)
    step6_form = Step6DescriptionForm(initial=initial_step6)
    step7_form = Step7ContactForm(initial=initial_step7)

    brand_name = source.brand.name if (source and source.brand) else ''
    model_name = source.model.name if (source and source.model) else ''
    year_val = source.year if source else ''

    country_choices = list(Listing.COUNTRY_CHOICES)

    # ═══ Equipment grouped by category — CARS-ONLY filter ═══
    # Excludes truck_*, gear (motorcycles), and any other categories
    CARS_CAT_KEYS = [k for k, _ in CARS_EQUIPMENT_CATEGORIES]

    cars_equipment = Equipment.objects.filter(
        category__in=CARS_CAT_KEYS
    ).order_by('category', 'name')

    items_by_cat = {}
    for item in cars_equipment:
        items_by_cat.setdefault(item.category, []).append(item)

    equipment_by_category = []
    for cat_key, cat_label in CARS_EQUIPMENT_CATEGORIES:
        if cat_key in items_by_cat:
            equipment_by_category.append({
                'key': cat_key,
                'label': cat_label,
                'items': items_by_cat[cat_key],
            })

    # Selected equipment IDs
    selected_equipment_ids = []
    if source:
        selected_equipment_ids = list(source.equipment_items.values_list('equipment_id', flat=True))

    context = {
        'form': _QuickFormProxy(media_form, step3_form, step4_form, step5_form, step6_form, step7_form),
        'is_edit_mode': is_edit_mode,
        'listing': listing,
        'edit_listing_id': listing.pk if listing else None,
        'current_draft': current_draft,
        'listing_data': listing_data,
        'step1_brand': brand_name,
        'step1_model': model_name,
        'step1_year': year_val,
        'brands': Brand.objects.all().order_by('name'),
        'years': list(range(timezone.now().year + 1, 1949, -1)),
        'country_choices': country_choices,
        'us_states': Listing.US_STATE_CHOICES,
        'equipment_by_category': equipment_by_category,
        'selected_equipment_ids': selected_equipment_ids,
    }
    return render(request, 'listings/listing_create_cars_quick.html', context)


class _QuickFormProxy:
    """
    Wrapper, kuris atrodo kaip vienas form'as šablonui, bet po kapotom kreipiasi
    į kelis form'us. Template'as naudoja `{{ form.body_type }}`, `{{ form.price }}`,
    etc. — proxy automatiškai randa, kuriame form'e laukelis yra.
    """
    def __init__(self, media_form, step3_form, step4_form, step5_form, step6_form, step7_form):
        self._forms = [media_form, step3_form, step4_form, step5_form, step6_form, step7_form]

    def __getattr__(self, name):
        for f in self._forms:
            if name in f.fields:
                return f[name]
        raise AttributeError(f"No field '{name}' in any of the wrapped forms")

    @property
    def errors(self):
        all_errors = {}
        for f in self._forms:
            if f.errors:
                all_errors.update(f.errors)
        return all_errors


# ════════════════════════════════════════════════════════════════════
# UPGRADE PAGE — shown when user hits listing limit
# ════════════════════════════════════════════════════════════════════

@login_required
def listing_upgrade(request):
    """Upgrade page shown when user hits their active listings limit."""
    from .constants import (
        PRIVATE_FREE_LIMIT, PRIVATE_SUB_LIMIT, DEALER_LIMIT,
        PER_LISTING_PRICE_USD, PRIVATE_SUB_PRICE_USD, DEALER_SUB_PRICE_EUR,
    )

    can_create, active_count, current_limit = can_create_listing(request.user)
    profile = getattr(request.user, 'profile', None)

    context = {
        'active_count': active_count,
        'current_limit': current_limit,
        'can_create': can_create,
        'private_free_limit': PRIVATE_FREE_LIMIT,
        'private_sub_limit': PRIVATE_SUB_LIMIT,
        'dealer_limit': DEALER_LIMIT,
        'per_listing_price': PER_LISTING_PRICE_USD,
        'private_sub_price': PRIVATE_SUB_PRICE_USD,
        'dealer_sub_price': DEALER_SUB_PRICE_EUR,
        'is_dealer': (
            profile
            and profile.account_type == 'dealer'
            and profile.dealer_status == 'approved'
        ),
        'dealer_status': profile.dealer_status if profile else 'none',
    }
    return render(request, 'listings/listing_upgrade.html', context)


# ════════════════════════════════════════════════════════════════════
# LISTING SELECT PLAN — autogidas-style picker (Premium 90d / Standard 60d / Basic 30d)
# ════════════════════════════════════════════════════════════════════

@login_required
def listing_select_plan(request, pk):
    """Plan picker: 3 paid plans + addons (stars, featured).

    Veikia visiem ne-active statusam (draft / inactive / expired).
    Vienas endpoint'as visiem flow'am (Cars create + Dashboard Activate + Renew).

    DABAR naudoja DB modelius (PricingPlan + PricingSettings + PriceMultiplierTier)
    vietoj constants.py — galima keisti per /admin/listings/pricingplan/
    """
    from .models import PricingPlan, PricingSettings, PriceMultiplierTier
    from decimal import Decimal

    listing = get_object_or_404(Listing, pk=pk, seller=request.user)

    # Jeigu jau active — nukreipk į detail (nereikia mokėti dar kartą)
    if listing.status == 'active':
        return redirect('listing_detail', pk=pk)

    # Completeness guard: incomplete drafts must be filled before activating
    if listing.status == 'draft':
        is_moto_gear = (listing.subcategory_id and listing.subcategory.slug in MOTO_GEAR_SLUGS)
        if is_moto_gear:
            is_complete = bool(
                listing.subcategory_id and listing.condition
                and listing.price and listing.price > 0
                and listing.country and listing.city and listing.city != '—'
            )
        else:
            is_complete = bool(
                listing.year and listing.first_registration and listing.fuel_type_id
                and listing.price and listing.price > 0
                and listing.country and listing.city and listing.city != '—'
            )
            slug = listing.vehicle_type.slug if listing.vehicle_type else ''
            if slug == 'cars':
                is_complete = is_complete and bool(
                    listing.brand_id and listing.body_type
                    and listing.transmission_id and listing.doors and listing.mileage
                )
            elif slug == 'trucks':
                is_complete = is_complete and bool(
                    listing.truck_brand_id and listing.truck_model_text and listing.truck_type
                )
        if not is_complete:
            messages.info(request, 'Complete the listing before activating it.')
            return redirect(listing.get_edit_url())

    # ─── Plan'us paimam iš DB pagal kategoriją ───
    plans_qs = PricingPlan.objects.filter(
        vehicle_type=listing.vehicle_type,
        is_active=True,
    ).order_by('order', '-duration_days')

    # Fallback: jei kategorija nepalaikoma (boats, vans, etc.) — naudoja Cars
    if not plans_qs.exists():
        try:
            cars_vt = VehicleType.objects.get(slug='cars')
            plans_qs = PricingPlan.objects.filter(
                vehicle_type=cars_vt,
                is_active=True,
            ).order_by('order', '-duration_days')
        except VehicleType.DoesNotExist:
            messages.error(request, 'No pricing plans configured. Run: python manage.py seed_pricing')
            return redirect('my_listings')

    # ─── Pricing settings (singleton) ───
    pricing = PricingSettings.get_solo()

    # ─── Apskaičiuojam multiplier (jei įjungtas) ───
    multiplier = Decimal('1.0')
    multiplier_tier_label = None
    if pricing.multiplier_enabled and listing.price:
        active_tier = PriceMultiplierTier.objects.filter(
            is_active=True,
            min_price__lte=listing.price,
            max_price__gt=listing.price,
        ).first()
        if active_tier:
            multiplier = active_tier.multiplier
            multiplier_tier_label = active_tier.label

    # ─── Sukuriam plan'us su preskaičiuotom kainom (template'ui) ───
    plans = []
    for p in plans_qs:
        original_price = p.price
        final_price = (original_price * multiplier).quantize(Decimal('0.01'))
        plans.append({
            'code': p.code or f'plan_{p.duration_days}',
            'label': p.label or p.custom_label or 'Plan',
            'days': p.duration_days,
            'price_usd': original_price,           # Original kaina
            'final_price_usd': final_price,        # Su multiplier (jei įjungtas)
            'has_multiplier': multiplier != Decimal('1.0'),
            'boost_days': p.boost_days,
            'boost_count': p.boost_count,
            'featured_days': p.featured_days,
            'highlight_days': p.highlight_days,
            'is_recommended': p.is_recommended,
            'pk': p.pk,
        })

    profile = getattr(request.user, 'profile', None)
    wallet_balance = profile.wallet_balance if (profile and profile.wallet_balance) else Decimal('0')

    context = {
        'listing': listing,
        'main_image': listing.images.first(),
        'plans': plans,
        'wallet_balance': wallet_balance,
        # Multiplier info (jei įjungtas — rodysim user'iui)
        'multiplier_enabled': pricing.multiplier_enabled,
        'multiplier_value': multiplier,
        'multiplier_tier_label': multiplier_tier_label,
        # Addon dropdown options (iš PricingSettings)
        'renew_count_options': list(range(1, pricing.addon_renew_max_count + 1)),
        'renew_days_options': list(range(1, pricing.addon_renew_max_days + 1)),
        'featured_days_options': list(range(1, pricing.addon_featured_max_days + 1)),
        'renew_price_per_unit': float(pricing.addon_renew_price),
        'featured_price_per_day': float(pricing.addon_featured_price),
    }
    return render(request, 'listings/listing_select_plan.html', context)


@login_required
def listing_pay_plan(request, pk, plan_code):
    """Process plan + addons — deduct wallet, activate listing.

    Veikia visiem ne-active statusam (draft / inactive / expired).
    DABAR naudoja DB modelius (PricingPlan + PricingSettings) vietoj constants.py.
    """
    from .models import PricingPlan, PricingSettings, PriceMultiplierTier
    from decimal import Decimal

    listing = get_object_or_404(Listing, pk=pk, seller=request.user)

    if listing.status == 'active':
        messages.info(request, 'Listing is already active.')
        return redirect('listing_detail', pk=pk)

    # ─── Surask plan'ą DB pagal vehicle_type + code ───
    db_plan = PricingPlan.objects.filter(
        vehicle_type=listing.vehicle_type,
        code=plan_code,
        is_active=True,
    ).first()

    # Fallback į Cars jei kategorija nepalaikoma (boats/vans/etc.)
    if not db_plan:
        try:
            cars_vt = VehicleType.objects.get(slug='cars')
            db_plan = PricingPlan.objects.filter(
                vehicle_type=cars_vt,
                code=plan_code,
                is_active=True,
            ).first()
        except VehicleType.DoesNotExist:
            pass

    if not db_plan:
        messages.error(request, 'Invalid plan selected.')
        return redirect('listing_select_plan', pk=pk)

    # ─── Apskaičiuojam multiplier (jei įjungtas) ───
    pricing = PricingSettings.get_solo()
    multiplier = Decimal('1.0')
    if pricing.multiplier_enabled and listing.price:
        active_tier = PriceMultiplierTier.objects.filter(
            is_active=True,
            min_price__lte=listing.price,
            max_price__gt=listing.price,
        ).first()
        if active_tier:
            multiplier = active_tier.multiplier

    # ─── Plan dict (suderinamas su senu kodu žemiau) ───
    plan = {
        'code': db_plan.code,
        'label': db_plan.label or 'Plan',
        'days': db_plan.duration_days,
        'price_usd': db_plan.price,
        'final_price_usd': (db_plan.price * multiplier).quantize(Decimal('0.01')),
        'boost_days': db_plan.boost_days,
        'boost_count': db_plan.boost_count,
        'featured_days': db_plan.featured_days,
        'highlight_days': db_plan.highlight_days,
    }

    if request.method != 'POST':
        return redirect('listing_select_plan', pk=pk)

    # ─── Calculate total ─ naudojam final_price (su multiplier jei įjungtas) ───
    total_price = Decimal(str(plan['final_price_usd']))

    # Stars addon: count × days × price_per_unit
    renew_count = int(request.POST.get('renew_count', 0) or 0)
    renew_days = int(request.POST.get('renew_days', 0) or 0)
    if renew_count > 0 and renew_days > 0:
        renew_cost = Decimal(str(renew_count * renew_days * float(pricing.addon_renew_price)))
        total_price += renew_cost
    else:
        renew_cost = Decimal('0')

    # Featured addon: days × price_per_day
    featured_days = int(request.POST.get('featured_days', 0) or 0)
    if featured_days > 0:
        featured_cost = Decimal(str(featured_days * float(pricing.addon_featured_price)))
        total_price += featured_cost
    else:
        featured_cost = Decimal('0')

    total_price = total_price.quantize(Decimal('0.01'))

    # ─── Stripe Checkout ─ planai mokami TIK kortele (wallet nedalyvauja) ───
    stripe_secret = getattr(settings, 'STRIPE_SECRET_KEY', '')
    if not stripe_secret:
        messages.error(request, 'Payment system is being set up. Please try again later.')
        return redirect('listing_select_plan', pk=pk)

    addon_parts = []
    if renew_cost > 0:
        addon_parts.append(f"{renew_count}* x {renew_days}d")
    if featured_cost > 0:
        addon_parts.append(f"featured {featured_days}d")

    product_name = f"{listing.title} - {plan['label']} plan ({plan['days']}d)"
    if addon_parts:
        product_name += " + " + ", ".join(addon_parts)

    try:
        import stripe
        stripe.api_key = stripe_secret

        session = stripe.checkout.Session.create(
            mode='payment',
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'product_data': {'name': product_name[:250]},
                    'unit_amount': int(total_price * 100),
                },
                'quantity': 1,
            }],
            customer_email=request.user.email,
            success_url=request.build_absolute_uri(
                reverse('listing_success', kwargs={'pk': listing.pk}) + '?action=published'
            ),
            cancel_url=request.build_absolute_uri(
                reverse('listing_select_plan', kwargs={'pk': listing.pk})
            ),
            metadata={
                'type': 'listing_plan',
                'user_id': str(request.user.id),
                'listing_id': str(listing.pk),
                'plan_code': plan['code'],
                'plan_days': str(plan['days']),
                'plan_boost_days': str(plan.get('boost_days', 0)),
                'plan_boost_count': str(plan.get('boost_count', 0)),
                'plan_featured_days': str(plan.get('featured_days', 0)),
                'plan_highlight_days': str(plan.get('highlight_days', 0)),
                'renew_count': str(renew_count),
                'renew_days': str(renew_days),
                'addon_featured_days': str(featured_days),
                'total_price': str(total_price),
            },
        )
        return redirect(session.url)

    except Exception as e:
        messages.error(request, f'Payment error: {str(e)[:120]}')
        return redirect('listing_select_plan', pk=pk)


# ════════════════════════════════════════════════════════════════════
# PROMO CODE VALIDATION — AJAX endpoint
# ════════════════════════════════════════════════════════════════════

@login_required
@require_POST
def validate_promo_code_ajax(request):
    """Validate promo code and return discount info.

    POST data:
        code: 'MOOD' (case-insensitive)
        listing_pk: 145 (kuriam listing'ui taikom)
        plan_code: 'premium_90' (kuris planas pasirinktas)

    Response (success):
        {
            'success': True,
            'code': 'MOOD',
            'description': 'Įvedus šitą gaus 20%',
            'discount_type': 'percent',
            'discount_value': 20.0,
            'discount_amount': 2.0,      # $ kiek nuolaidos
            'final_price': 8.0,           # plan kaina po nuolaidos
            'message': '-20% off ($2.00 saved)'
        }

    Response (error):
        {
            'success': False,
            'error': str(_('Invalid promo code'))
        }
    """
    from .models import PromoCode, PricingPlan
    from decimal import Decimal
    import json

    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

    code_input = (data.get('code') or '').strip().upper()
    listing_pk = data.get('listing_pk')
    plan_code = data.get('plan_code', '')

    if not code_input:
        return JsonResponse({'success': False, 'error': str(_('Įveskite kodą'))})

    if not listing_pk:
        return JsonResponse({'success': False, 'error': str(_('Listing not found'))})

    # ─── Surask listing ───
    try:
        listing = Listing.objects.get(pk=listing_pk, seller=request.user)
    except Listing.DoesNotExist:
        return JsonResponse({'success': False, 'error': str(_('Listing not found'))})

    # ─── Surask promo kodą (case-insensitive) ───
    promo = PromoCode.objects.filter(code__iexact=code_input).first()
    if not promo:
        return JsonResponse({'success': False, 'error': str(_('Toks kodas neegzistuoja'))})

    # ─── Patikrink ar valid ───
    is_valid, error_msg = promo.is_valid(user=request.user, listing=listing, plan_code=plan_code)
    if not is_valid:
        return JsonResponse({'success': False, 'error': error_msg})

    # ─── Surask plan'ą + apskaičiuok nuolaidą ───
    db_plan = PromoCode.objects.none()
    try:
        db_plan = PricingPlan.objects.filter(
            vehicle_type=listing.vehicle_type,
            code=plan_code,
            is_active=True,
        ).first()

        # Fallback į Cars
        if not db_plan:
            cars_vt = VehicleType.objects.filter(slug='cars').first()
            if cars_vt:
                db_plan = PricingPlan.objects.filter(
                    vehicle_type=cars_vt,
                    code=plan_code,
                    is_active=True,
                ).first()
    except Exception:
        pass

    if not db_plan:
        return JsonResponse({'success': False, 'error': 'Plan not found'})

    plan_price = Decimal(str(db_plan.price))
    discount_amount = promo.calculate_discount(plan_price)
    final_price = max(plan_price - discount_amount, Decimal('0'))

    # ─── Pranešimas user'iui ───
    if promo.discount_type == 'percent':
        message = f'-{promo.discount_value}% off'
    else:
        message = f'-${promo.discount_value} off'

    return JsonResponse({
        'success': True,
        'code': promo.code,
        'description': promo.description or '',
        'discount_type': promo.discount_type,
        'discount_value': float(promo.discount_value),
        'discount_amount': float(discount_amount),
        'final_price': float(final_price),
        'original_price': float(plan_price),
        'message': message,
    })


# ═══════════════════════════════════════════════════════════
# LISTING SERVICES — papildomas žvaigždučių/highlight/featured pirkimas
# AKTYVIAM skelbimui (ne plano dalis, atskiras pirkimas iš wallet)
# Naudoja TĄ PAČIĄ PricingSettings šaltinį kaip Create flow (listing_select_plan)
# ═══════════════════════════════════════════════════════════

@login_required
def listing_services_order(request, pk):
    """Paslaugų užsakymo puslapis aktyviam skelbimui.

    User'is jau aktyvavo skelbimą ir nori PAPILDOMAI nupirkti
    žvaigždučių, highlight'o ar featured'o iš savo wallet.

    UI identiškas Create flow addons sekcijai (listing_activation_plans.html).
    """
    from .models import PricingSettings

    listing = get_object_or_404(Listing, pk=pk, seller=request.user)

    if listing.status != 'active':
        messages.error(request, 'Services can only be purchased for active listings.')
        return redirect('my_listings')

    pricing = PricingSettings.get_solo()
    now = timezone.now()

    # ─── Dabartinis paslaugų statusas (kiek dar liko) ───
    current_stars = listing.star_count if listing.is_star_active() else 0
    current_star_days_left = 0
    if listing.is_star_active() and listing.star_expires_at:
        delta = listing.star_expires_at - now
        current_star_days_left = max(0, delta.days)

    current_highlight_days_left = 0
    if listing.is_highlighted and listing.highlight_until:
        delta = listing.highlight_until - now
        current_highlight_days_left = max(0, delta.days)

    current_featured_days_left = 0
    if listing.is_featured and listing.featured_until:
        delta = listing.featured_until - now
        current_featured_days_left = max(0, delta.days)

    profile = getattr(request.user, 'profile', None)
    wallet_balance = profile.wallet_balance if (profile and profile.wallet_balance) else Decimal('0')

    context = {
        'listing': listing,
        'main_image': listing.images.first(),
        # Current status (kiek dar liko)
        'current_stars': current_stars,
        'current_star_days_left': current_star_days_left,
        'current_highlight_days_left': current_highlight_days_left,
        'current_featured_days_left': current_featured_days_left,
        'wallet_balance': wallet_balance,
        # Dropdown options — IDENTIŠKAI kaip Create flow listing_select_plan
        'renew_count_options': list(range(1, pricing.addon_renew_max_count + 1)),
        'renew_days_options': list(range(1, pricing.addon_renew_max_days + 1)),
        'featured_days_options': list(range(1, pricing.addon_featured_max_days + 1)),
        'highlight_days_options': list(range(1, pricing.addon_featured_max_days + 1)),
        # Kainos — IDENTIŠKAI kaip Create flow
        'renew_price_per_unit': float(pricing.addon_renew_price),
        'featured_price_per_day': float(pricing.addon_featured_price),
        'highlight_price_per_day': float(pricing.addon_featured_price),
    }
    return render(request, 'listings/listing_services_order.html', context)


@login_required
@require_POST
def listing_services_checkout(request, pk):
    """Apdoroja paslaugų pirkimą — nuima iš wallet, prideda paslaugas."""
    from .models import PricingSettings

    listing = get_object_or_404(Listing, pk=pk, seller=request.user)

    if listing.status != 'active':
        messages.error(request, 'Listing is not active.')
        return redirect('my_listings')

    settings_obj = PricingSettings.get_solo()

    def _safe_int(key, max_val):
        try:
            v = int(request.POST.get(key, 0) or 0)
        except (ValueError, TypeError):
            v = 0
        return max(0, min(v, max_val))

    star_count = _safe_int('star_count', settings_obj.addon_renew_max_count)
    star_days = _safe_int('star_days', settings_obj.addon_renew_max_days)
    highlight_days = _safe_int('highlight_days', settings_obj.addon_featured_max_days)
    featured_days = _safe_int('featured_days', settings_obj.addon_featured_max_days)

    total = Decimal('0.00')

    if star_count > 0 and star_days > 0:
        total += settings_obj.addon_renew_price * star_count * star_days
    if highlight_days > 0:
        total += settings_obj.addon_featured_price * highlight_days
    if featured_days > 0:
        total += settings_obj.addon_featured_price * featured_days

    if total == Decimal('0.00'):
        messages.error(request, 'Please select at least one service.')
        return redirect('listing_services_order', pk=listing.pk)

    profile = getattr(request.user, 'profile', None)
    if not profile:
        messages.error(request, 'Profile not found.')
        return redirect('listing_services_order', pk=listing.pk)

    wallet_balance = profile.wallet_balance or Decimal('0')
    if wallet_balance < total:
        messages.error(
            request,
            f'Insufficient wallet balance. Need ${total:.2f}, have ${wallet_balance:.2f}.'
        )
        return redirect('/accounts/wallet/')

    now = timezone.now()

    with transaction.atomic():
        from apps.accounts.models import WalletTransaction
        profile.wallet_balance = wallet_balance - total
        profile.save(update_fields=['wallet_balance'])

        # Description
        parts = []
        if star_count > 0 and star_days > 0:
            parts.append(f'{star_count}★ x {star_days}d')
        if highlight_days > 0:
            parts.append(f'highlight {highlight_days}d')
        if featured_days > 0:
            parts.append(f'featured {featured_days}d')
        desc = f"Extra services for listing #{listing.pk}: " + ", ".join(parts)

        try:
            WalletTransaction.objects.create(
                user=request.user,
                amount=-total,
                transaction_type='service_purchase',
                description=desc,
            )
        except Exception as e:
            print(f"[wallet] transaction log failed: {e}")

        # Stars — sudedam (count + days)
        if star_count > 0 and star_days > 0:
            current_days_left = 0
            if listing.is_star_active() and listing.star_expires_at:
                delta = listing.star_expires_at - now
                current_days_left = max(0, delta.days)
            listing.star_count = (listing.star_count or 0) + star_count
            listing.star_level = max(1, min(listing.star_count, 5))
            listing.star_expires_at = now + timedelta(days=current_days_left + star_days)

        # Highlight — sudedam dienas
        if highlight_days > 0:
            current_days_left = 0
            if listing.is_highlighted and listing.highlight_until:
                delta = listing.highlight_until - now
                current_days_left = max(0, delta.days)
            listing.highlight_until = now + timedelta(days=current_days_left + highlight_days)

        # Featured — sudedam dienas
        if featured_days > 0:
            current_days_left = 0
            if listing.is_featured and listing.featured_until:
                delta = listing.featured_until - now
                current_days_left = max(0, delta.days)
            listing.featured_until = now + timedelta(days=current_days_left + featured_days)

        listing.save(update_fields=[
            'star_count', 'star_level', 'star_expires_at',
            'highlight_until', 'featured_until',
        ])

    messages.success(request, f'Services activated successfully! Charged ${total:.2f} from wallet.')
    return redirect('my_listings')
COUNTRY_FLAGS = {}


# ═══════════════════════════════════════════════════════════
# BENDRA FILTRAVIMO LOGIKA — naudoja listing_list IR search_panel_count
# ═══════════════════════════════════════════════════════════

SEARCH_PANEL_CATEGORIES = {'cars', 'motorcycles', 'trucks', 'parts', 'boats', 'trailers', 'agriculture', 'construction', 'loading-equipment', 'forestry', 'camping-houses', 'rental', 'services', 'electronics', 'bicycles'}

# DALYS subkategorijų count raktai (žr. search_panel.COUNT_KEY_TO_SUB)
PARTS_COUNT_KEYS = COUNT_KEY_TO_SUB


def _subcategory_slug_from(params):
    """?subcategory= (id arba slug) → slug; reikalinga kategorijoms su
    dviem formomis (construction technika vs priedai)."""
    val = params.get('subcategory')
    if not val:
        return params.get('sub') or None
    if str(val).isdigit():
        return (SubCategory.objects.filter(pk=val)
                .values_list('slug', flat=True).first())
    return str(val)


def filter_listings(params, user=None, category=None, base_qs=None):
    """Pritaiko visus GET filtrus ant Listing queryset'o.

    params   — request.GET (QueryDict) arba dict
    base_qs  — jei paduotas, filtruoja jį; kitaip ima _public_listings_qs
    """
    def _getlist(key):
        if hasattr(params, 'getlist'):
            return [v for v in params.getlist(key) if v]
        v = params.get(key)
        return [v] if v else []

    listings = base_qs if base_qs is not None else _public_listings_qs(user)

    category = category or params.get('category')
    if category:
        listings = listings.filter(vehicle_type__slug=category)

    # subcategory — listing_list tai jau darė, count endpoint'as ne
    if params.get('subcategory'):
        # Priima ir id, ir slug — kategorijoms su dviem formomis
        # (construction) subkategorija URL'e patogesnė kaip slug.
        _sub = str(params['subcategory'])
        if _sub.isdigit():
            listings = listings.filter(subcategory_id=_sub)
        else:
            listings = listings.filter(subcategory__slug=_sub)

    # Bendri ?search / ?q taiko TIK pavadinimą. Kai kategorijos tekstinę
    # paiešką valdo deklaratyvus variklis (ieško ir aprašyme), šituos
    # praleidžiam — kitaip susidėję duotų tik title atitikmenis.
    _engine_text = panel_config.owns_text_search(category)
    if params.get('search') and not _engine_text:
        listings = listings.filter(title__icontains=params['search'])
    q = (params.get('q') or '').strip()
    if q and not _engine_text:
        listings = listings.filter(title__icontains=q)

    part_query = (params.get('part_query') or '').strip()
    if part_query:
        listings = listings.filter(
            Q(title__icontains=part_query) | Q(description__icontains=part_query)
        )

    if params.get('brand'):
        listings = listings.filter(brand_id=params['brand'])
    if params.get('model'):
        listings = listings.filter(model_id=params['model'])
    if params.get('submodel'):
        listings = listings.filter(submodel_id=params['submodel'])

    if params.get('price_min'):
        listings = listings.filter(price__gte=params['price_min'])
    if params.get('price_max'):
        listings = listings.filter(price__lte=params['price_max'])
    if params.get('year_min'):
        listings = listings.filter(year__gte=params['year_min'])
    if params.get('year_max'):
        listings = listings.filter(year__lte=params['year_max'])
    if params.get('mileage_min'):
        listings = listings.filter(mileage__gte=params['mileage_min'])
    if params.get('mileage_max'):
        listings = listings.filter(mileage__lte=params['mileage_max'])

    if params.get('fuel_type'):
        listings = listings.filter(fuel_type_id=params['fuel_type'])
    if params.get('transmission'):
        listings = listings.filter(transmission_id=params['transmission'])

    body_types = _getlist('body_type')
    if body_types:
        listings = listings.filter(body_type__in=body_types)

    if params.get('defects'):
        listings = listings.filter(defects=params['defects'])

    city_val = (params.get('city') or '').strip()
    if city_val:
        listings = listings.filter(city__icontains=city_val)

    if params.get('state_filter'):
        listings = listings.filter(country='US', state=params['state_filter'])
    elif params.get('country_filter'):
        listings = listings.filter(country=params['country_filter'])

    posted_within = params.get('posted_within')
    if posted_within:
        try:
            days = int(posted_within)
            if days == 1:
                cutoff = timezone.now() - timedelta(hours=24)
            else:
                cutoff = timezone.now() - timedelta(days=days)
            listings = listings.filter(created_at__gte=cutoff)
        except (ValueError, TypeError):
            pass

    if params.get('has_vin'):
        listings = listings.exclude(vin__isnull=True).exclude(vin='')
    if params.get('valid_inspection'):
        listings = listings.filter(valid_inspection=True)
    if params.get('hide_auctions'):
        listings = listings.filter(is_auction=False)
    if params.get('seller_type'):
        listings = listings.filter(seller_type=params['seller_type'])

    # Special features
    FEATURE_FIELDS = {
        'feat_trade_in': 'open_to_trade',
        'feat_warranty': 'has_warranty',
        'feat_lease': 'available_on_lease',
        'feat_sport': 'is_sport_ready',
        'feat_disabled': 'disabled_friendly',
        'feat_service_book': 'has_service_book',
        'feat_us_import': 'imported_from_us',
        'feat_multi_keys': 'multiple_keys',
        'feat_power_boost': 'power_boosted',
        'feat_pneumatic': 'pneumatic_suspension',
        'feat_remote_start': 'remote_start',
        'feat_spare_wheel': 'spare_wheel',
    }
    for param_key, field in FEATURE_FIELDS.items():
        if params.get(param_key):
            listings = listings.filter(**{field: True})

    # Equipment
    for eid in _getlist('equipment'):
        listings = listings.filter(equipment_items__equipment_id=eid)

    # ═══ PRIEKABOS — išplėstiniai laukai (dar ne konfigūracijoje) ═══
    if category == 'trailers':
        listings = apply_trailer_filters(listings, params)

    # ═══ DEKLARATYVUS SLUOKSNIS ═══
    # Tas pats variklis kaip listing_list — kad skaičiukas ir rezultatai
    # niekada neišsiskirtų (šitos dvi vietos turi atskiras filtrų šakas).
    if category:
        _sub_slug = _subcategory_slug_from(params)
        listings = panel_config.apply_panel_filters(
            listings, category, params, sub_slug=_sub_slug)
        listings = panel_config.apply_panel_filters(
            listings, category, params, source='advanced', sub_slug=_sub_slug)

    return listings


def advanced_search_generic(request, category):
    """Išplėstinė paieška iš konfigūracijos — /paieska/<kategorija>/.

    Renderina isplestine-config.json aprašą; filtravimas eina per tą patį
    filter_listings kelią, todėl rezultatai ir skaičiukas visada sutampa.
    """
    sub_slug = request.GET.get('sub') or None
    adv = panel_config.build_advanced(category, request.user, sub_slug=sub_slug)
    if adv is None:
        raise Http404

    qs = filter_listings(request.GET, user=request.user, category=category)

    # Markės parametras kiekvienoje kategorijoje savas (trailer_brand_text,
    # agri_brand_text, camp_brand_text...) — imam jį iš konfigūracijos, kad
    # perkrovus puslapį pažymėtos markės išliktų visoms kategorijoms.
    brand_param = next(
        (f.get('param') for f in adv['fields']
         if f.get('db_field') in panel_config.TEXT_BRAND_FIELDS
         or f.get('db_field') in panel_config.FK_BRAND_FIELDS),
        'trailer_brand_text',
    )

    return render(request, 'listings/advanced_generic.html', {
        'adv': adv,
        'result_count': qs.count(),
        'selected_equipment': request.GET.getlist('equipment'),
        'selected_brands': request.GET.getlist(brand_param),
    })


def search_panel_count(request, category):
    """AJAX — grąžina tik filtruotų skelbimų skaičių panelės mygtukui."""
    if category in ('tires', 'wheels'):
        try:
            from .models import WheelListing
            qs = WheelListing.objects.filter(status='active')
            wtype = request.GET.get('type')
            if wtype:
                qs = qs.filter(wheel_type=wtype)
            return JsonResponse({'count': qs.count()})
        except Exception:
            return JsonResponse({'count': 0})

    if category == 'motogear':
        qs = _public_listings_qs(request.user).filter(
            subcategory__slug__in=MOTO_GEAR_SLUGS
        )
        if request.GET.get('price_min'):
            qs = qs.filter(price__gte=request.GET['price_min'])
        if request.GET.get('price_max'):
            qs = qs.filter(price__lte=request.GET['price_max'])
        _gq = (request.GET.get('search') or request.GET.get('q') or '').strip()
        if _gq:
            qs = qs.filter(title__icontains=_gq)
        return JsonResponse({'count': qs.count()})

    # DALYS tab'as — trys subkategorijos, kiekviena su savo browse view'u
    if category in PARTS_COUNT_KEYS:
        qs = parts_count_qs(
            PARTS_COUNT_KEYS[category], request.GET, user=request.user
        )
        return JsonResponse({'count': qs.count()})

    if (category not in SEARCH_PANEL_CATEGORIES
            and not panel_config.advanced_is_active(category)):
        raise Http404
    qs = filter_listings(request.GET, user=request.user, category=category)
    return JsonResponse({'count': qs.count()})
