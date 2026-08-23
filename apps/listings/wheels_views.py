# apps/listings/wheels_views.py
# ═══════════════════════════════════════════════════════════
# WHEELS (Tyres + Rims) — create / list / advanced search / detail
#
# URLS:
#   path('create/wheels/', wheels_views.wheels_create, name='wheels_create'),
#   path('create/tyres/', wheels_views.tyres_create, name='tyres_create'),
#   path('create/rims/', wheels_views.rims_create, name='rims_create'),
#   path('browse/wheels/', wheels_views.wheels_list, name='wheels_list'),
#   path('search/wheels/advanced/', wheels_views.wheels_advanced_search, name='wheels_advanced_search'),
#   path('ajax/wheels-search-count/', wheels_views.wheels_search_count_ajax, name='wheels_search_count_ajax'),
#   path('wheels/<int:pk>/', wheels_views.wheels_detail, name='wheels_detail'),
# ═══════════════════════════════════════════════════════════

from datetime import timedelta
from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Case, When, IntegerField, Value, Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
# gettext_lazy, o ne gettext: modulio lygio sąrašai (TYRE_FEATURE_FIELDS ir kt.)
# įvertinami importo metu, kai aktyvi numatytoji kalba — su „gettext" jie
# amžiams užšaldavo lietuviškai ir angliškoje versijoje likdavo LT.
from django.utils.translation import gettext_lazy as _

from .image_validation import split_valid_images
from . import wheels_filters
from .models import (
    WheelListing, WheelImage, SavedWheelListing,
    WHEEL_PURPOSE_CHOICES, WHEEL_DIAMETER_CHOICES, WHEEL_CONDITION_CHOICES,
    TYRE_WIDTH_CHOICES, TYRE_PROFILE_CHOICES, TYRE_SEASON_CHOICES,
    TYRE_SPEED_CHOICES, TYRE_TREAD_CHOICES, TYRE_REMAINING_CHOICES,
    TYRE_DOT_YEAR_CHOICES,
    RIM_WIDTH_CHOICES, RIM_PCD_CHOICES, RIM_BOLT_COUNT_CHOICES,
    RIM_MATERIAL_CHOICES,
)
from .search_params import sanitize as sanitize_search_params

NEW_WHEEL_DAYS = 3


def _to_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _to_decimal(value):
    try:
        return Decimal(str(value).replace(',', '.'))
    except (TypeError, ValueError, InvalidOperation):
        return None


TYRE_FEATURE_FIELDS = [
    ('feat_spare_thin', _('Spare tyre (thin)')),
    ('feat_sold_single', _('Sold individually')),
    ('feat_sport', _('Sport tyres')),
    ('feat_suv', _('SUV tyres')),
    ('feat_rain', _('Rain tyres')),
    ('feat_run_flat', _('Run-flat')),
    ('feat_reinforced', _('Reinforced')),
    ('feat_studded', _('Studded (winter)')),
]


def _resolve_brand_name(request):
    """Tyre: select is 'Other' -> free text. Rim/kiti: laisvas tekstas."""
    val = request.POST.get('brand_name', '').strip()
    if val == 'Other':
        other = request.POST.get('brand_name_other', '').strip()
        if other:
            return other[:80]
    return val[:80]


# ═══ TYRE BRANDS — autogidas sarasas (Other paskutinis) ═══
TYRE_BRANDS = [
    'Accelera', 'Achilles', 'Advance', 'Aeolus', 'Agi', 'Agrostar', 'Alliance', 'Altai',
    'Altenzo', 'Altura', 'Amberway', 'American Classic', 'Anlas', 'Antares', 'Aoteli', 'Aplus',
    'Apollo', 'Aptany', 'Arctic', 'Arivo', 'Atlas', 'Atturo', 'Aurora', 'Austone', 'Autogrip',
    'Autoguard', 'Avon', 'Avon Vintage', 'Bandag', 'Barkley', 'Barum', 'Belarus', 'Belshina',
    'BFGoodrich', 'BKT', 'Black-Star', 'Blacklion', 'Blackstar', 'Blockley', 'Boto',
    'Bridgestone', 'Briway', 'Camac', 'Carbon', 'Carbon Series', 'Carlisle', 'Ceat',
    'Champiro', 'Chaoyang', 'Cheng Shin', 'Chengshan', 'Cheyen', 'Claw', 'Coker', 'Comforser',
    'Compass', 'Constancy', 'Continental', 'Contire', 'Cooper', 'Cordiant', 'Courier', 'Cover',
    'Cratos', 'Cultor', 'Dailyway', 'Davanti', 'Dayton', 'Debica', 'Deestone', 'Delfin',
    'Deli Tire', 'Delinte', 'Diplomat', 'DMACK', 'Dneproshina', 'Dongfeng', 'Double coin',
    'Doublestar', 'Dunlop', 'Duraturn', 'Duro', 'Durun', 'Effiplus', 'Encore', 'EP tyres',
    'ESA Tecar', 'Euro-Grip', 'Eurotec', 'Event', 'Evergreen', 'Evermax', 'Excelsior',
    'Falken', 'Faralong', 'Farm King', 'Farroad', 'Fate', 'Federal', 'Fedima', 'Firemax',
    'Firenza', 'Firestone', 'Firststop', 'Fortuna', 'Fortune', 'Fulda', 'Fullrun', 'Fullway',
    'Fuzion', 'G-Force', 'Galaxy', 'General', 'General Tire', 'Gerutti', 'Gislaved', 'Giti',
    'Goalstar', 'Goform', 'Golden Tyre', 'Goldway', 'Goodride', 'Goodyear', 'GreenLander',
    'Greenmax', 'Gremax', 'Gripmax', 'GT radial', 'Haida', 'Hankook', 'Headway', 'Heidenau',
    'Heissrunderneuerung BRW', 'Hercules', 'Hifly', 'High Performer', 'Hilo', 'Horizon',
    'Imperial', 'Import', 'Infinity', 'Insa Turbo', 'Interstate', 'Invovic', 'Ironman',
    'Jintong', 'Jinyu', 'Joyroad', 'Kaltrunderneuerung', 'Kama', 'Kelly', 'Kenda', 'Keter',
    'Kinforest', 'King Meiler', 'Kings Tire', 'Kingstar', 'Kleber', 'Kormoran', 'Kumho',
    'Landsail', 'Lanvigator', 'Lapponia', 'Lassa', 'Laufenn', 'Leao', 'Lexani', 'Linglong',
    'Lucas', 'Luccini', 'Mabor', 'Malatesta', 'Malhotra', 'Maloya', 'Marangoni', 'Marix',
    'Marshal', 'Marshal/Kumho', 'Mastercraft', 'Mastersteel', 'Matador', 'Maxtrek', 'Maxxis',
    'Mazzini', 'McLaren', 'Membat', 'Mentor', 'Meteor', 'Metzeler', 'Michelin',
    'Michelin Collection', 'Michelin Collection Tubes', 'Michelin Remix', 'Mickey Thompson',
    'Milestone', 'Minerva', 'Mitas', 'Momo', 'Motrio', 'MRF', 'Multirac', 'Nankang', 'Nereus',
    'Nexen', 'Next Tread', 'Nitto', 'Nokian', 'Nord frost', 'Nordexx', 'Nordman', 'Nortenha',
    'Novex', 'Omsk', 'Opals', 'Orium', 'Ovation', 'Pace', 'Paxaro', 'Petlas', 'Phoenix',
    'Pirelli', 'Platin', 'Pneu Laurent', 'Pneu Vranik', 'Pneumant', 'Powertrac', 'Premiorri',
    'Primewell', 'Pro Comp', 'Protector', 'Radar', 'Rapid', 'Recip', 'Regal', 'Reifen',
    'Retro', 'Rigdon', 'Riken', 'Roadhog', 'Roadmarch', 'Roadstone', 'Rockstone', 'Rosava',
    'Rotalla', 'Rotex', 'Rovelo', 'Royalblack', 'Royalton', 'Runway', 'Rydanz', 'Saetta',
    'Saferich', 'Saffiro', 'Sagitar', 'Sailun', 'Sava', 'Security', 'Seha', 'Seiberling',
    'Semperit', 'Shikari', 'Sibur', 'Silverstone', 'Solideal', 'Sonar', 'Sonix', 'Sonny',
    'Special Tubes', 'Speedways', 'Sportiva', 'Star', 'Star Performer', 'Starco', 'Starfire',
    'Starmaxx', 'Starway', 'Stomil', 'Sumitomo', 'Sunew', 'Sunfull', 'Sunitrac', 'Sunny',
    'Suntek', 'Sunwide', 'Super King', 'Superia', 'Syron', 'T-Brand', 'Taifa', 'Taurus',
    'Taxat', 'Teamstar', 'Techking', 'Three-A', 'Tianli', 'Tigar', 'Titan', 'Toledo', 'Tomket',
    'Torque', 'Tourador', 'Townhall', 'Toyo', 'Tracmax', 'Trazano', 'Trelleborg', 'Triangle',
    'Tristar', 'TVS', 'Tyfoon', 'Tyrex', 'Unigom', 'Unigrip', 'Uniroyal', 'Unistar', 'V-Netik',
    'VEE-Rubber', 'Veloce', 'Viatti', 'Victorun', 'Viking', 'Voltyre', 'Voyager', 'Vredestein',
    'Wanda', 'Wanli', 'Waymaster', 'Westlake', 'Windforce', 'Windpower', 'Winguard', 'Winrun',
    'Winter Tact', 'Woosung', 'Yokohama', 'Z-Tyre', 'Zeetex', 'Zenises', 'Zeta',
    'Other',
]


# ═══ RIM FEATURES — autogidas Ratlankiai „Ypatumai" ═══
# Visi penki turi laukus WheelListing modelyje (0074 migracija).
# feat_sold_single bendras su padangomis, kiti keturi — tik ratlankiams.
RIM_FEATURE_FIELDS = [
    ('rim_feat_bent', _('Bent rims')),
    ('rim_feat_original', _('Original rims')),
    ('feat_sold_single', _('Sold individually')),
    ('rim_feat_with_tyres', _('With tyres')),
    ('rim_feat_chromed', _('Chromed')),
]


# ═══ RIM BRANDS — autogidas Ratlankiai sarasas (Other paskutinis) ═══
RIM_BRANDS = [
    '100', '5 Zigen', '57 Motorsport', 'A.M.G.', 'AB-Eintz', 'ABTsportsline',
    'AC Schnitzer', 'Ace', 'ACE Alloy', 'ACK', 'Acura', 'ADR',
    'ADVAN Racing', 'Advanti Racing', 'AEZ', 'AG Forged', 'Akita Racing', 'Akuza',
    'Alba', 'Alessio', 'Alfa Romeo', 'Alpina', 'ALT', 'ALUTEC',
    'American Eagle', 'American Racing', 'AMG', 'Anella', 'Antera', 'Apex',
    'APP', 'Arceo', 'Arelli', 'Armano', 'Artec', 'ASA',
    'Asanti', 'ASC', 'ATS', 'Audi', 'Autec', 'Autowheels',
    'Avenue', 'AWC', 'Axis', 'AZA Forged', 'Azev', 'Azzur',
    'B2Boyz', 'Baccarat', 'Bazo', 'BBS', 'Bentley', 'Binno',
    'Black Racing', 'Blades', 'Blingz', 'BMW', 'Borbet', 'Boss',
    'Boyd-Coddington', 'Boze', 'Brabus', 'Branzach', 'Breyton', 'Brock',
    'BSA', 'Budnik', 'BWA Racing', 'BZO', 'Cabo', 'Cadillac',
    'CAM', 'Carlsson', 'CEC', 'Centerline', 'Chevrolet', 'Chopper',
    'Chrysler', 'Citroen', 'CMS', 'Concept One', 'Cragar', 'Cromodora',
    'Cupra', 'D Forged', 'DAAT', 'Dacia', 'Daewoo', 'Daihatsu',
    'Damani', 'Datho', 'Davin', 'Dayton', 'Dayton Wire', 'DeCorsa',
    'Defy Wheels', 'DeModa', 'Detata', 'Devino', 'Dezent', 'Diablo',
    'Diamo', 'Dip', 'Dodge', 'Dolce', 'Donz', 'Dotz',
    'Drag', 'Drag wheels', 'Driv', 'DUB', 'DV', 'Dvinci',
    'DVS', 'E Forged', 'Echelon', 'Eco', 'Edge', 'Egoist',
    'Elite', 'EMO', 'Enkei', 'Enzo', 'Epic', 'Everhart',
    'FAB', 'Fahrzeug-Technik', 'Feracci', 'Ferretti', 'Fiat', 'Focal',
    'Fondmetal', 'Foose', 'Ford', 'ForgedMetal', 'Forzza', 'Foxx',
    'Fundo', 'G-Racing', 'Gazario', 'Genx', 'GFG', 'Gianelle',
    'Gino', 'Giovanna', 'Giovanna GG', 'Giovanna Racing', 'Gitano', 'GZC Wheels',
    'HAGEN', 'Hamann', 'Hartge', 'HAXER Wheels', 'Helo', 'Hero',
    'Hijoin wheels', 'Hipnotic', 'Honda', 'HRE', 'Hummer', 'Hyundai',
    'ICE', 'ICW Racing', 'ILAN', 'Image', 'Imola', 'Infiniti',
    'Intro Wheels', 'ION', 'Isuzu', 'Jaguar', 'Japan Racing', 'Jeep',
    'JesseJames', 'K2 Racing', 'Kaizer', 'Kaotik', 'Katana Racing', 'Keskin',
    'Keskin Tuning', 'KIA', 'KMC', 'Konig', 'Kormetal', 'Kosei',
    'Kruz', 'Kyowa Racing', 'LA Wire', 'Laced', 'Land Rover', 'League',
    'Lenso', 'Lenzo', 'Lexani', 'Lexus', 'Limited', 'Lionhart',
    'Lorenzo', 'Lorinser', 'Lowenhart', 'Luxe', 'Luxor Wire', 'MAE',
    'Maido', 'MAK', 'MAM', 'Marqi', 'Maserati', 'MAYA',
    'Mazda', 'Mazzi', 'MC Motorsports', 'Mega', 'Mercedes-Benz', 'MHT',
    'Milano', 'MINI', 'Mitsubishi', 'Mizati', 'MKW', 'Mob Empire',
    'Modello', 'Mogul', 'MOMO', 'Monaco', 'Monet', 'Monza',
    'Mossa', 'Motegi Racing', 'Moto Metal', 'Moven', 'MOZ', 'MSR',
    'MVR', 'Nano', 'NCwheels', 'Neeper', 'Niche', 'Nismo',
    'Nissan', 'Oasis', 'OC Motorsport', 'OEM', 'Oettinger', 'Omega',
    'Opel', 'Oxigin', 'OZ Racing', 'OZI', 'P Miller', 'Pacer',
    'Panther', 'Paragon', 'Paragon Wire', 'PCW', 'PDW', 'Peugeot',
    'Pinnacle', 'Pinnacle Racing', 'Platinum', 'Player', 'Player Wire', 'Polo',
    'Porsche', 'Power Tech', 'Predator', 'Primax', 'ProLine', 'Quantum',
    'Quantum44', 'R1 Racing', 'Raceline', 'Racing', 'RacingHart', 'Radius',
    'Raju', 'Raze', 'Razor', 'RC Design', 'RCD', 'Rebel',
    'Remotec', 'Renault', 'Replica', 'RH Evolution', 'Rial', 'Roadster Wire',
    'Ronal', 'Rondell', 'Rota', 'Rover', 'Rozzi', 'SA Forged',
    'Saab', 'Sacchi', 'Saint', 'Savini Forged', 'Schmidt', 'Seat',
    'Sinister', 'Skoda', 'Smart', 'Smiths', 'Sparco', 'Spectrum',
    'Speedline', 'Spintek', 'Spinweel', 'Sport Dynamics', 'Sport Technic', 'Sportec',
    'Sportiva', 'Sportrux', 'Sporza', 'SR Racing', 'SRW', 'SsangYong',
    'SSR', 'Stilauto', 'Strada', 'Subaru', 'Suzuki', 'Swift',
    'Symbolic', 'Team Dynamics', 'TechArt', 'Teckademics', 'Tenzo Racing', 'Tezzen',
    'TG Racing', 'TIS', 'Tomason', 'Toora', 'Toyota', 'Traxx',
    'TRK', 'TSW', 'TTE', 'UltraU', 'UWC', 'V.I.P',
    'Varance', 'VCT', 'Veloche', 'Velocity', 'Velox', 'Verde',
    'VIPER', 'Volk Racing', 'Volkswagen', 'Volt Racing', 'Volvo', 'Vossen',
    'Voxx', 'VSMPO', 'Weld Evo', 'Wolfrace', 'WORK', 'X Power',
    'X2O', 'Xenex', 'XTC', 'XXL', 'XXR', 'Yokawa',
    'Yokawa Racing', 'YOTO', 'ZE Forged', 'Zenetti', 'ZEO', 'Zinik',
    'Zora', 'Zyoxx', 'Other',
]


def _apply_wheel_post(listing, request):
    """Užpildo WheelListing laukus iš POST. Bendra create ir edit srautams.

    product_type keičiamas tik kuriant — jau paskelbtam skelbimui tipo
    perjungimas paliktų svetimos šakos laukus užpildytus.
    """
    if not listing.pk:
        product_type = request.POST.get('product_type', 'tyre')
        if product_type not in ('tyre', 'rim'):
            product_type = 'tyre'
        listing.product_type = product_type

    # ─── bendri ───
    listing.brand_name = _resolve_brand_name(request)
    listing.model_name = request.POST.get('model_name', '').strip()[:80]
    listing.purpose = request.POST.get('purpose', '')
    listing.diameter = request.POST.get('diameter', '')
    listing.condition = request.POST.get('condition', 'used')
    listing.quantity = _to_int(request.POST.get('quantity')) or 4
    listing.price = _to_decimal(request.POST.get('price')) or Decimal('0')
    listing.negotiable = request.POST.get('negotiable') == 'on'
    listing.description = request.POST.get('description', '').strip()

    # ─── lokacija / kontaktai ───
    listing.country = request.POST.get('country', 'LT')
    listing.state = request.POST.get('state', '').strip()[:64]
    listing.city = request.POST.get('city', '').strip()[:100]
    listing.postal_code = request.POST.get('postal_code', '').strip()[:20]
    listing.contact_phone = request.POST.get('contact_phone', '').strip()[:30]
    listing.contact_email = request.POST.get('contact_email', '').strip()

    if listing.product_type == 'tyre':
        listing.tyre_width = request.POST.get('tyre_width', '')
        listing.tyre_profile = request.POST.get('tyre_profile', '')
        listing.tyre_season = request.POST.get('tyre_season', '')
        listing.tyre_speed_index = request.POST.get('tyre_speed_index', '')
        listing.tyre_load_index = request.POST.get('tyre_load_index', '').strip()[:6]
        listing.tyre_tread_mm = request.POST.get('tyre_tread_mm', '')
        listing.tyre_remaining_pct = request.POST.get('tyre_remaining_pct', '')
        listing.tyre_dot_year = request.POST.get('tyre_dot_year', '')
        for field, _label in TYRE_FEATURE_FIELDS:
            setattr(listing, field, request.POST.get(field) == 'on')
    else:
        listing.rim_width = request.POST.get('rim_width', '')
        listing.rim_pcd = request.POST.get('rim_pcd', '')
        listing.rim_bolt_count = request.POST.get('rim_bolt_count', '')
        listing.rim_et = _to_int(request.POST.get('rim_et'))
        listing.rim_dia = _to_decimal(request.POST.get('rim_dia'))
        listing.rim_material = request.POST.get('rim_material', '')
        listing.fits_brands = request.POST.get('fits_brands', '').strip()[:200]
        for field, _label in RIM_FEATURE_FIELDS:
            setattr(listing, field, request.POST.get(field) == 'on')
    return listing


def _save_wheel_photos(listing, request):
    """Naujos nuotraukos pridedamos prie esamų (redaguojant senų netrinam).

    Netinkamų failų neįrašom, bet skelbimo neprarandam — apie atmestas
    nuotraukas pranešam per messages.
    """
    existing = listing.images.count()
    photos, photo_errors = split_valid_images(
        request.FILES.getlist('photos')[:20]
    )
    for err in photo_errors:
        messages.error(request, err)
    for i, photo in enumerate(photos):
        WheelImage.objects.create(
            listing=listing,
            image=photo,
            is_main=(existing == 0 and i == 0),
            order=existing + i,
        )


@login_required
def wheels_create(request):
    """Create form — Tyres arba Rims (?type=tyre / ?type=rim).

    GET renderina dedikuotą template'ą pagal URL name:
        tyres_create -> tyres_create.html
        rims_create  -> rims_create.html
        wheels_create -> wheels_create.html (bendras su toggle)
    POST logika bendra — skaito product_type iš hidden input.
    """

    if request.method == 'POST':
        listing = _apply_wheel_post(WheelListing(seller=request.user), request)
        listing.title = listing.build_title()
        listing.save()
        _save_wheel_photos(listing, request)
        listing.activate()
        return redirect('wheels_detail', pk=listing.pk)

    # ─── GET ───
    return render(request, *_wheel_form(request, None))


def _wheel_form(request, listing):
    """(template, context) create ir edit srautams.

    Ypatumų sąrašai atiduodami kaip trejetai (laukas, etiketė, pažymėta),
    kad šablonui nereikėtų kviesti atributo pagal kintamą vardą.
    """
    if listing is not None:
        initial_type = listing.product_type
    else:
        initial_type = request.GET.get('type', 'tyre')
        if initial_type not in ('tyre', 'rim'):
            initial_type = 'tyre'

    url_name = request.resolver_match.url_name if request.resolver_match else ''

    def feats(fields):
        return [(f, lbl, bool(getattr(listing, f, False))) for f, lbl in fields]

    context = {
        'listing': listing,
        'is_edit_mode': listing is not None,
        'initial_type': initial_type,
        # Redaguojant tipas visada užrakintas: perjungimas paliktų
        # svetimos šakos laukus užpildytus.
        'type_locked': listing is not None or url_name in ('tyres_create', 'rims_create'),
        # bendri
        'purpose_choices': WHEEL_PURPOSE_CHOICES,
        'diameter_choices': WHEEL_DIAMETER_CHOICES,
        'condition_choices': WHEEL_CONDITION_CHOICES,
        'country_choices': WheelListing.COUNTRY_CHOICES,
        'us_states': WheelListing.US_STATE_CHOICES,
        # tyres
        'tyre_width_choices': TYRE_WIDTH_CHOICES,
        'tyre_profile_choices': TYRE_PROFILE_CHOICES,
        'tyre_season_choices': TYRE_SEASON_CHOICES,
        'tyre_speed_choices': TYRE_SPEED_CHOICES,
        'tyre_tread_choices': TYRE_TREAD_CHOICES,
        'tyre_remaining_choices': TYRE_REMAINING_CHOICES,
        'tyre_dot_year_choices': TYRE_DOT_YEAR_CHOICES,
        'tyre_feature_fields': feats(TYRE_FEATURE_FIELDS),
        'tyre_brands': TYRE_BRANDS,
        # rims
        'rim_width_choices': RIM_WIDTH_CHOICES,
        'rim_pcd_choices': RIM_PCD_CHOICES,
        'rim_bolt_count_choices': RIM_BOLT_COUNT_CHOICES,
        'rim_material_choices': RIM_MATERIAL_CHOICES,
        'rim_feature_fields': feats(RIM_FEATURE_FIELDS),
        'rim_brands': RIM_BRANDS,
    }

    if initial_type == 'tyre' and (listing is not None or url_name == 'tyres_create'):
        template = 'listings/tyres_create.html'
    elif initial_type == 'rim' and (listing is not None or url_name == 'rims_create'):
        template = 'listings/rims_create.html'
    else:
        template = 'listings/wheels_create.html'

    return template, context


@login_required
def wheels_edit(request, pk):
    """Padangų / ratlankių redagavimas — iki šiol jo nebuvo visai.

    Skelbimą sukūrus vienintelis būdas ištaisyti raidę buvo ištrinti ir
    kurti iš naujo. Naudoja tuos pačius šablonus kaip create.
    """
    listing = get_object_or_404(WheelListing, pk=pk, seller=request.user)

    if request.method == 'POST':
        _apply_wheel_post(listing, request)
        listing.title = listing.build_title()
        listing.save()
        _save_wheel_photos(listing, request)
        messages.success(request, _('Skelbimas atnaujintas.'))
        return redirect('wheels_detail', pk=listing.pk)

    return render(request, *_wheel_form(request, listing))


@login_required
def tyres_create(request):
    """Atskiras Tyres create puslapis — tipas užrakintas."""
    request.GET = request.GET.copy()
    request.GET['type'] = 'tyre'
    return wheels_create(request)


@login_required
def rims_create(request):
    """Atskiras Rims create puslapis — tipas užrakintas."""
    request.GET = request.GET.copy()
    request.GET['type'] = 'rim'
    return wheels_create(request)


# ═══════════════════════════════════════════════════════════
# SHARED FILTER LOGIC — wheels_list + advanced search + count AJAX
# Vienas šaltinis, kad count'as VISADA sutaptų su rezultatais.
# ═══════════════════════════════════════════════════════════

# Filtrai, kuriuos palaikom per GET (naudojami ir 'f' contexte)
WHEELS_FILTER_KEYS = [
    'purpose', 'diameter', 'condition', 'brand', 'q', 'city',
    'country_filter', 'state_filter',
    'price_from', 'price_to', 'quantity_min',
    # tyre
    'tyre_width', 'tyre_profile', 'tyre_season',
    'tyre_speed_index', 'tyre_tread_mm', 'tyre_dot_year',
    # rim
    'rim_width', 'rim_pcd', 'rim_bolt_count', 'rim_material',
    'rim_et_from', 'rim_et_to',
    # etalono papildymas (docs/autogidas-ratlankiai-padangos.md)
    'rim_pcd_mm', 'rim_dia', 'fits_brand', 'quantity', 'manufacturer',
    'tread_from', 'tread_to', 'age', 'seller_type',
]


def _apply_wheels_filters(request, product_type=None):
    """Grąžina (qs, product_type, f_dict) pagal request.GET.

    Naudoja rims_list / tyres_list, wheels_advanced_search ir
    wheels_search_count_ajax — filter logika VIENOJE vietoje.
    Naršymo puslapiai kategoriją perduoda argumentu (atskiri URL), senoji
    išplėstinė paieška — per ?type=.
    """

    def getval(name):
        v = request.GET.get(name, '')
        return v.strip() if v else ''

    if product_type not in ('tyre', 'rim'):
        product_type = getval('type')
    if product_type not in ('tyre', 'rim'):
        product_type = 'tyre'

    qs = WheelListing.objects.filter(
        status='active',
        is_shadow_banned=False,
        product_type=product_type,
    )

    # ─── bendri filtrai ───
    if getval('purpose'):
        qs = qs.filter(purpose=getval('purpose'))
    if getval('diameter'):
        qs = qs.filter(diameter=getval('diameter'))
    if getval('condition'):
        qs = qs.filter(condition=getval('condition'))
    # Gamintojas: `brand` sanitize'e laikomas FK id (automobilių markė), todėl
    # ratų gamintojo vardas keliauja per `manufacturer`; `brand` paliktas dėl
    # senų nuorodų.
    gamintojas = getval('manufacturer') or getval('brand')
    if gamintojas:
        qs = qs.filter(brand_name__icontains=gamintojas)

    # Tekstinė paieška — title + description + brand + model
    if getval('q'):
        q_val = getval('q')
        qs = qs.filter(
            Q(title__icontains=q_val)
            | Q(description__icontains=q_val)
            | Q(brand_name__icontains=q_val)
            | Q(model_name__icontains=q_val)
        )

    if getval('city'):
        qs = qs.filter(city__icontains=getval('city'))

    # Lokacija — kaip cars: state (US) > country
    if getval('state_filter'):
        qs = qs.filter(country='US', state=getval('state_filter'))
    elif getval('country_filter'):
        qs = qs.filter(country=getval('country_filter'))

    price_from = _to_decimal(getval('price_from'))
    price_to = _to_decimal(getval('price_to'))
    if price_from is not None and getval('price_from'):
        qs = qs.filter(price__gte=price_from)
    if price_to is not None and getval('price_to'):
        qs = qs.filter(price__lte=price_to)

    qty_min = _to_int(getval('quantity_min'))
    if qty_min:
        qs = qs.filter(quantity__gte=qty_min)

    # ─── tyre filtrai ───
    if product_type == 'tyre':
        if getval('tyre_width'):
            qs = qs.filter(tyre_width=getval('tyre_width'))
        if getval('tyre_profile'):
            qs = qs.filter(tyre_profile=getval('tyre_profile'))
        if getval('tyre_season'):
            qs = qs.filter(tyre_season=getval('tyre_season'))
        if getval('tyre_speed_index'):
            qs = qs.filter(tyre_speed_index=getval('tyre_speed_index'))
        if getval('tyre_tread_mm'):
            qs = qs.filter(tyre_tread_mm=getval('tyre_tread_mm'))
        if getval('tyre_dot_year'):
            qs = qs.filter(tyre_dot_year=getval('tyre_dot_year'))
    # ─── rim filtrai ───
    else:
        if getval('rim_width') and getval('rim_width') != wheels_filters.RIM_WIDTH_OVER:
            qs = qs.filter(rim_width=getval('rim_width'))
        if getval('rim_pcd'):
            qs = qs.filter(rim_pcd=getval('rim_pcd'))
        if getval('rim_bolt_count'):
            qs = qs.filter(rim_bolt_count=getval('rim_bolt_count'))
        if getval('rim_material'):
            qs = qs.filter(rim_material=getval('rim_material'))
        et_from = _to_int(getval('rim_et_from'))
        et_to = _to_int(getval('rim_et_to'))
        if et_from is not None and getval('rim_et_from'):
            qs = qs.filter(rim_et__gte=et_from)
        if et_to is not None and getval('rim_et_to'):
            qs = qs.filter(rim_et__lte=et_to)

    # ─── etalono filtrai (abiem kategorijom) ───
    if getval('quantity'):
        if getval('quantity') == '5plus':
            qs = qs.filter(quantity__gte=5)
        else:
            qty = _to_int(getval('quantity'))
            if qty:
                qs = qs.filter(quantity=qty)

    amzius = getval('age')
    if amzius in wheels_filters.AGE_DAYS:
        riba = timezone.now() - timedelta(days=wheels_filters.AGE_DAYS[amzius])
        qs = qs.filter(created_at__gte=riba)
        if amzius == '1d_new':
            # „tik nauji" — ne pakelti į viršų, o realiai nauji skelbimai
            qs = qs.filter(last_boosted_at__isnull=True)

    if getval('seller_type') in ('private', 'dealer'):
        qs = qs.filter(seller__profile__account_type=getval('seller_type'))

    # ─── etalono filtrai pagal kategoriją ───
    if product_type == 'tyre':
        gylis = [
            v for v in wheels_filters.TREAD_DEPTHS
            if (not getval('tread_from') or float(v) >= float(getval('tread_from')))
            and (not getval('tread_to') or float(v) <= float(getval('tread_to')))
        ]
        if getval('tread_from') or getval('tread_to'):
            qs = qs.filter(tyre_tread_mm__in=gylis)
    else:
        # PCD mm: DB saugo „5x112" pavidalu, etalonas — 112.00
        if getval('rim_pcd_mm'):
            mm = getval('rim_pcd_mm').rstrip('0').rstrip('.')
            qs = qs.filter(rim_pcd__endswith='x' + mm)
        if getval('rim_dia'):
            dia = _to_decimal(getval('rim_dia'))
            if dia is not None:
                qs = qs.filter(rim_dia=dia)
        if getval('rim_width') == wheels_filters.RIM_WIDTH_OVER:
            platesni = [v for v, _lbl in RIM_WIDTH_CHOICES
                        if _to_decimal(v) is not None and float(v) > 11]
            qs = qs.filter(rim_width__in=platesni)
        if getval('fits_brand'):
            qs = qs.filter(fits_brands__icontains=getval('fits_brand'))

    # Žymimieji langeliai (etalonas: juostos apačia)
    zymes = (wheels_filters.RIM_FEATURES if product_type == 'rim'
             else wheels_filters.TYRE_FEATURES)
    for laukas, _label in zymes:
        if request.GET.get(laukas):
            qs = qs.filter(**{laukas: True})

    f = {k: getval(k) for k in WHEELS_FILTER_KEYS}
    f['type'] = product_type
    return qs, product_type, f


def _wheels_distinct(product_type, field):
    """DB reikšmės, kurių nėra etalono sąraše (spec. technikos dydžiai)."""
    return list(
        WheelListing.objects.filter(status='active', product_type=product_type)
        .exclude(**{field: ''})
        .values_list(field, flat=True).distinct()
    )


def _wheels_cities(product_type):
    return sorted(
        c for c in WheelListing.objects.filter(
            status='active', product_type=product_type
        ).exclude(city='').values_list('city', flat=True).distinct() if c
    )


def _wheels_vehicle_brands():
    """Tr. priem. markės — automobilių markių sąrašas (`fits_brands` tekste)."""
    from .models import Brand
    return list(Brand.objects.order_by('name').values_list('name', flat=True))


def _wheels_choices_context():
    """Bendri choices — list + advanced search template'ams."""
    return {
        'purpose_choices': WHEEL_PURPOSE_CHOICES,
        'diameter_choices': WHEEL_DIAMETER_CHOICES,
        'condition_choices': WHEEL_CONDITION_CHOICES,
        'tyre_width_choices': TYRE_WIDTH_CHOICES,
        'tyre_profile_choices': TYRE_PROFILE_CHOICES,
        'tyre_season_choices': TYRE_SEASON_CHOICES,
        'tyre_speed_choices': TYRE_SPEED_CHOICES,
        'tyre_tread_choices': TYRE_TREAD_CHOICES,
        'tyre_dot_year_choices': TYRE_DOT_YEAR_CHOICES,
        'rim_width_choices': RIM_WIDTH_CHOICES,
        'rim_pcd_choices': RIM_PCD_CHOICES,
        'rim_bolt_count_choices': RIM_BOLT_COUNT_CHOICES,
        'rim_material_choices': RIM_MATERIAL_CHOICES,
        'tyre_brands': TYRE_BRANDS,
        'rim_brands': RIM_BRANDS,
        'country_choices': WheelListing.COUNTRY_CHOICES,
        'us_states': WheelListing.US_STATE_CHOICES,
    }


# ═══════════════════════════════════════════════════════════
# WHEELS LIST / SEARCH — cars-style sidebar layout
# ═══════════════════════════════════════════════════════════

def wheels_list(request):
    """Senoji bendra nuoroda — 301 į atskiras kategorijas.

    Etalone (docs/autogidas-ratlankiai-padangos.md) ratlankiai ir padangos
    yra dvi atskiros kategorijos, todėl bendro puslapio su „Tipas"
    perjungikliu nebėra. Parametrai keliauja kartu, kad išsaugotos nuorodos
    neprarastų filtrų.
    """
    from django.http import HttpResponsePermanentRedirect
    params = request.GET.copy()
    tipas = (params.pop('type', [''])[0] or '').strip()
    tikslas = reverse('tyres_list') if tipas == 'tyre' else reverse('rims_list')
    likutis = params.urlencode()
    return HttpResponsePermanentRedirect(tikslas + (f'?{likutis}' if likutis else ''))


def rims_list(request):
    """Ratlankiai — atskira kategorija (etalonas: autogidas „Ratlankiai")."""
    return _wheels_browse(request, 'rim')


def tyres_list(request):
    """Padangos — atskira kategorija (etalonas: autogidas „Padangos")."""
    return _wheels_browse(request, 'tyre')


def _wheels_browse(request, product_type):
    """Bendras naršymo puslapis: struktūra ta pati, laukai — pagal kategoriją."""
    request.GET = sanitize_search_params(request.GET)

    qs, product_type, f = _apply_wheels_filters(request, product_type)
    qs = qs.prefetch_related('images')

    # ─── rikiavimas: stars > boost > new > kiti (kaip Listing) ───
    now = timezone.now()
    boost_cutoff = now - timedelta(hours=24)
    three_days_ago = now - timedelta(days=NEW_WHEEL_DAYS)

    qs = qs.annotate(
        sort_priority=Case(
            When(star_level=2, star_expires_at__gt=now, then=Value(500)),
            When(star_level=1, star_expires_at__gt=now, then=Value(400)),
            When(last_boosted_at__gt=boost_cutoff, then=Value(300)),
            When(created_at__gt=three_days_ago, then=Value(200)),
            default=Value(100),
            output_field=IntegerField(),
        )
    )

    sort = request.GET.get('sort', '').strip()
    if sort == 'price_asc':
        qs = qs.order_by('price', '-created_at')
    elif sort == 'price_desc':
        qs = qs.order_by('-price', '-created_at')
    elif sort == 'newest':
        qs = qs.order_by('-created_at')
    else:
        sort = ''
        qs = qs.order_by('-sort_priority', '-created_at')

    paginator = Paginator(qs, 24)
    page_obj = paginator.get_page(request.GET.get('page'))

    # querystring be page (paginacijos linkams)
    params = request.GET.copy()
    params.pop('page', None)
    querystring = params.urlencode()

    saved_ids = set()
    if request.user.is_authenticated:
        saved_ids = set(
            SavedWheelListing.objects.filter(
                user=request.user,
                listing__in=page_obj.object_list,
            ).values_list('listing_id', flat=True)
        )

    # ─── badge helpers (template'ui — datetime lygint negalim) ───
    new_ids = [
        l.pk for l in page_obj.object_list
        if l.created_at and l.created_at > three_days_ago
    ]
    starred = {
        l.pk: l.star_count or 1
        for l in page_obj.object_list
        if l.star_level and l.star_expires_at and l.star_expires_at > now
    }

    laukai, features = wheels_filters.sidebar_fields(
        product_type,
        brand_names=(RIM_BRANDS if product_type == 'rim' else TYRE_BRANDS),
        cities=_wheels_cities(product_type),
        tyre_widths_db=_wheels_distinct(product_type, 'tyre_width'),
        tyre_profiles_db=_wheels_distinct(product_type, 'tyre_profile'),
        vehicle_brands=_wheels_vehicle_brands(),
    )

    context = {
        'product_type': product_type,
        'sidebar_fields': laukai,
        'feature_fields': [
            (param, label, bool(request.GET.get(param))) for param, label in features
        ],
        'quick_links': wheels_filters.quick_links() if product_type == 'rim' else [],
        'page_obj': page_obj,
        'total_count': paginator.count,
        'querystring': querystring,
        'sort': sort,
        'saved_ids': saved_ids,
        'new_ids': new_ids,
        'starred': starred,
        'f': f,
    }
    context.update(_wheels_choices_context())
    return render(request, 'listings/wheels_list.html', context)


# ═══════════════════════════════════════════════════════════
# WHEELS ADVANCED SEARCH — autogidas-style 3-col grid + live count
# ═══════════════════════════════════════════════════════════

def wheels_advanced_search(request):
    """Advanced search puslapis Tyres/Rims. Form submit'ina į /browse/wheels/."""
    request.GET = sanitize_search_params(request.GET)
    qs, product_type, f = _apply_wheels_filters(request)

    context = {
        'product_type': product_type,
        'f': f,
        'total_count': qs.count(),
    }
    context.update(_wheels_choices_context())
    return render(request, 'listings/wheels_advanced_search.html', context)


def wheels_search_count_ajax(request):
    """AJAX live count — grąžina filtruotų wheels skaičių.
    Naudoja TĄ PAČIĄ _apply_wheels_filters logiką kaip wheels_list."""
    request.GET = sanitize_search_params(request.GET)
    try:
        qs, _pt, _f = _apply_wheels_filters(request)
        return JsonResponse({'count': qs.count()})
    except Exception:
        return JsonResponse({'count': 0})


def wheels_save_toggle(request, pk):
    """AJAX heart toggle — SavedWheelListing (kaip cars save_listing)."""
    if not request.user.is_authenticated:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': 'login_required'}, status=401)
        return redirect('accounts:login')

    listing = get_object_or_404(WheelListing, pk=pk)
    saved, created = SavedWheelListing.objects.get_or_create(
        user=request.user,
        listing=listing,
    )
    if not created:
        saved.delete()
        is_saved = False
    else:
        is_saved = True

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'saved': is_saved})

    return redirect(request.META.get('HTTP_REFERER', '/'))


def wheels_detail(request, pk):
    """Wheels (tyre/rim) skelbimo detail puslapis."""
    listing = get_object_or_404(WheelListing, pk=pk)

    if listing.status != 'active' and listing.seller_id != request.user.id:
        from django.http import Http404
        raise Http404

    # views count (paprastas — be dedupe kol kas)
    if listing.seller_id != request.user.id:
        WheelListing.objects.filter(pk=pk).update(views_count=listing.views_count + 1)

    context = {
        'listing': listing,
        'images': listing.images.all(),
        'is_owner': listing.seller_id == request.user.id,
    }
    return render(request, 'listings/wheels_detail.html', context)


# ═══════════════════════════════════════════════════════════
# MY LISTINGS actions — delete / activate
# ═══════════════════════════════════════════════════════════

@login_required
def wheels_delete(request, pk):
    """Ištrina wheels skelbimą (my_listings modal POST'ina čia)."""
    listing = get_object_or_404(WheelListing, pk=pk, seller=request.user)
    if request.method == 'POST':
        listing.delete()
    return redirect('my_listings')


@login_required
def wheels_activate(request, pk):
    """Aktyvuoja neaktyvų wheels skelbimą (my_listings Activate mygtukas)."""
    listing = get_object_or_404(WheelListing, pk=pk, seller=request.user)
    if request.method == 'POST' and listing.status != 'active':
        listing.activate()
    return redirect('my_listings')