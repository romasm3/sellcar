# apps/listings/equipment_registry.py
# ═══════════════════════════════════════════════════════════
# YPATUMŲ (Equipment) REGISTRAS — vienintelis šaltinis.
#
# Kodėl atskiras modulis, o ne views: šiuos apibrėžimus turi matyti
# TRYS vartotojai —
#   • kategorijos view'as (create formos checkbox'ai),
#   • `seed_equipment` management komanda,
#   • duomenų migracija 0063 (kad naujoje aplinkoje eilutės atsirastų
#     pačios, be jokio rankinio žingsnio).
# Migracijos negali importuoti views (jie traukia modelius importo metu),
# todėl čia laikomi GRYNI duomenys — jokių Django importų.
#
# Kategorijos prefiksas ('trailer_', 'agri_', 'load_') yra privalomas:
# tie patys pavadinimai („Hidraulika", „Kabina") kartojasi tarp
# kategorijų, o paieška juos skiria būtent pagal prefiksą
# (search_config.panels.EQUIPMENT_PREFIX).
#
# Nauja kategorija: pridėk įrašą į CATEGORY_EQUIPMENT, paleisk
# `manage.py seed_equipment` ir įrašyk prefiksą į EQUIPMENT_PREFIX.
# ═══════════════════════════════════════════════════════════

TRAILER_EQUIPMENT_DEFINITION = [
    ('trailer_body', 'Kėbulas ir įranga', [
        'EDSCHA stogas',
        'Su kietu stogu',
        'Atitraukiamas stogas',
        'Su palapine',
        'Atitraukiami šonai',
        'Su tentu',
        'Durys gale',
        'Durys šone',
        'Žaliuzės',
        'Liftas gale',
        'Su hidrauliniu kranu',
        'Su gerve',
        'Hidraulika',
        'Įrankių dėžė',
    ]),
    ('trailer_chassis', 'Važiuoklė', [
        'Pakeliama ašis',
        'Pneumatinė pakaba',
        'Diskiniai stabdžiai',
    ]),
    ('trailer_safety', 'Sauga', [
        'ABS',
        'EBS',
        'Priekabos stabdys',
        'Krovinio diržai',
        'TIR',
        'Termografas',
    ]),
    ('trailer_other', 'Kita', [
        'Garantija',
        'Parduodama lizingu',
    ]),
]


AGRI_EQUIPMENT_DEFINITION = [
    ('agri_drivetrain', 'Pavaros ir važiuoklė', [
        'Lėtintos pavaros',
        'Greičio variatorius',
        'Dvigubi ratai',
        'Vikšrinis',
    ]),
    ('agri_mount', 'Prikabinimas', [
        'Prikabinamas',
        'Pakabinamas',
    ]),
    ('agri_other', 'Kita', [
        'ABS',
        'Hidraulika',
        'Kabina',
    ]),
]


LOAD_EQUIPMENT_DEFINITION = [
    ('load_cabin', 'Kabina ir apsauga', [
        'Kabina',
        'Pusiau kabina',
        'Apšildoma kabina',
        'Apsauginis stogelis',
    ]),
    ('load_hydraulics', 'Hidraulika ir mechanizmai', [
        'Hidraulika',
        'Papildomas hidraulikos vožtuvas',
        'Šoninio poslinkio mechanizmas',
        'Pasukamas griebtuvas',
    ]),
    ('load_platform', 'Platforma ir atramos', [
        'Platforma stumiasi į vieną pusę',
        'Platforma stumiasi į abi puses',
        'Sulankstomos atramos',
        'Lingės',
    ]),
    ('load_surface', 'Važiuoklė ir paviršius', [
        'Skirtas tvirtam paviršiui',
        'Skirtas bet kokiam paviršiui',
        'Žemintos pavaros',
    ]),
]


# ─── Turistiniai nameliai ───
# Savi 52 su 'camp_' prefiksu, NE automobilių eilutės: automobilių
# ypatumai suvesti angliškai (Cruise control, Airbags), o šie —
# lietuviškai, tad sutampa tik akronimas „ESP". Be prefikso
# build_advanced() paimtų automobilių ESP eilutę, o nameliai turėtų
# savo — filtras grąžintų 0 rezultatų.
CAMP_EQUIPMENT_DEFINITION = [
    ('camp_electronics', 'Elektronika', [
        '360° vaizdo kamera',
        'Audio grotuvas',
        'Automatinio parkavimo sistema',
        'Kelio ženklų atpažinimo sistema',
        'Kritulių jutiklis',
        'Laisvų rankų įranga',
        'Navigacija / GPS',
        'Nuovargio įspėjimo sistema',
        'Start-Stop sistema',
        'Atstumo jutiklių sistema',
        'Beraktė užvedimo sistema',
        'Galinio vaizdo kamera',
        'Kruizo kontrolė',
    ]),
    ('camp_assist', 'Pagalbos sistemos', [
        'ASR',
        'Borto kompiuteris',
        'Centrinis užraktas',
        'ESP',
        'Vairo stiprintuvas',
    ]),
    ('camp_safety', 'Saugumas ir apsauga', [
        'Aklosios zonos stebėjimo sistema',
        'Atstumo palaikymo sistema',
        'Avarinio stabdymo sistema',
        'Juostos palaikymo sistema',
        'Traukos kontrolės sistema',
        'Oro pagalvės',
        'Signalizacija / Imobilaizeris',
        'Stabilumo kontrolės sistema',
    ]),
    ('camp_interior', 'Salonas', [
        'Autonominis šildymas (webasto)',
        'CD grotuvas',
        'Dujinė viryklė',
        'Dušas',
        'El. langai',
        'El. sėdynės',
        'El. veidrodėliai',
        'Elektroninė klimato kontrolė',
        'Garso aparatūra',
        'Gido mikrofonas',
        'Karštas vanduo',
        'Kavos aparatas',
        'Oro kondicionierius',
        'Šildomas priekinis stiklas',
        'Šildomos sėdynės',
        'Tamsinti stiklai',
        'Tualetas',
        'Video įranga',
    ]),
    ('camp_other', 'Kiti privalumai', [
        'Aukštas',
        'CD keitiklis',
        'Dviračių laikikliai',
        'Geros būklės',
        'Lauko baldai',
        'Skaidraus stiklo priekiniai žibintai',
        'Su prieangiu',
        'Tentas',
    ]),
]


# vehicle_type slug → definicijų sąrašas
# ═══════════════════════════════════════════════════════════
# TRANSPORTO NUOMA — 3 ypatumai, bendri keturioms subkategorijoms
# (motociklų nuoma etalone ypatumų neturi).
#
# Prefiksas 'rent_' privalomas: „Kaina su vairuotoju" ir kiti nuomos
# sąlygų punktai kitose kategorijose neegzistuoja, bet prefiksas laiko
# juos izoliuotus ir ateičiai — žr. panels.EQUIPMENT_PREFIX.
# ═══════════════════════════════════════════════════════════
RENT_EQUIPMENT_DEFINITION = [
    ('rent_terms', 'Nuomos sąlygos', [
        'Kaina su vairuotoju',
        'Nuolaidos ilgesniam laikotarpiui',
        'Nuomojamas tik su vairuotoju',
    ]),
]


# ═══════════════════════════════════════════════════════════
# PASLAUGOS — 18 varnelių iš etalono „Papildomi duomenys" bloko.
#
# Etalono paieškoje jų nėra (sec 18 filtruoja tik tipą, miestą ir tekstą),
# bet skelbime jos rodomos, todėl saugom kaip Equipment eilutes.
# Prefiksas 'svc_' — „Ratų remontas" ir „Kita" pavadinimai lengvai
# susikirstų su kitomis kategorijomis (žr. panels.EQUIPMENT_PREFIX).
# ═══════════════════════════════════════════════════════════
SVC_EQUIPMENT_DEFINITION = [
    ('svc_repair', 'Remontas ir diagnostika', [
        'Bamperių remontas',
        'Dažymo paslaugos',
        'Duslintuvų remontas',
        'Elektronikos diagnostika',
        'Hidraulikos diagnostika',
        'Kėbulo remontas',
        'Pavarų dėžių remontas',
        'Turbinų diagnostika',
        'Ratų remontas',
        'Salono remontas',
        'Starterių, generatorių remontas',
        'Ratų montavimas, balansavimas',
        'Variklių diagnostika',
        'Važiuoklės remontas',
        'Autobusų, sunkvežimių remontas',
        'Motociklų, motorolerių remontas',
    ]),
    ('svc_other', 'Kita', [
        'Vežame į užsienį',
        'Kita',
    ]),
]


# ═══════════════════════════════════════════════════════════
# VIDEO, AUDIO, NAVIGACIJOS — 16 ypatumų (etalonas sec 15).
#
# Prefiksas 'elec_'. Automobilių ypatumų kategorija vadinasi
# 'electronics' — be pabraukimo prefikse ji irgi pakliūtų į
# startswith() filtrą, todėl pabraukimas čia būtinas.
# ═══════════════════════════════════════════════════════════
ELEC_EQUIPMENT_DEFINITION = [
    ('elec_features', 'Ypatumai', [
        '“Subwoofer” valdymas',
        'AUX jungtis',
        'Ekvalaizeris',
        'Galinė dalis',
        'Korteliu skaitytuvas',
        'LCD ekranas',
        'Liečiamas ekranas',
        'Linijiniai išėjimai',
        'Multifunkcinis valdymas nuo vairo',
        'Neveikiantis',
        'Nuotolinio valdymo pultas',
        'Priekinis skydelis',
        'Spalvotas ekranas',
        'USB jungtis',
        'Valdymas ratuku',
        'Vidinė atmintis',
    ]),
]


# ═══════════════════════════════════════════════════════════
# EL. PASPIRTUKAI, RIEDŽIAI, DVIRAČIAI — 12 ypatumų (etalonas sec 09).
# Prefiksas 'bike_'.
# ═══════════════════════════════════════════════════════════
BIKE_EQUIPMENT_DEFINITION = [
    ('bike_features', 'Ypatumai', [
        'Amortizatoriai',
        'Diskiniai stabdžiai',
        'Galimybė prijungti papildomą bateriją',
        'Garantija',
        'Greičio palaikymo sistema',
        'Integruotas ekranas',
        'Parkavimo kojelė',
        'Pritaikytas bekelei',
        'Savęs balansavimas',
        'Sėdynė',
        'Sulankstomas rėmas',
        'Žibintai',
    ]),
]


# ═══════════════════════════════════════════════════════════
# SENOSIOS KATEGORIJOS (automobiliai, motociklai, moto apranga,
# sunkvežimiai, sunkiojo transporto dalys).
#
# Šios eilutės DB egzistavo tik todėl, kad kažkas kadaise atidarė jų
# create formą — jos kuriamos tingiai per get_or_create. Atkūrus DB iš
# švarios migracijų būsenos formos rodytų 0 varnelių, o filtrai būtų
# tušti (SKILL.md, SPĄSTAS 1). Turinys perkeltas iš produkcijos DB
# tokia pačia tvarka (order_by('id')).
#
# Automobilių raktai istoriškai be prefikso ('interior', 'safety',
# 'electronics'...). Nekeičiam — jie surišti su 133 esamomis eilutėmis
# ir jų ListingEquipment nuorodomis.
# ═══════════════════════════════════════════════════════════


CARS_EQUIPMENT_DEFINITION = [
    ('interior', 'Interior', [
        'Air conditioning',
        'Climate control',
        'Heated seats',
        'Leather seats',
        'Electric seats',
        'Sunroof',
        'Keyless entry',
        'Navigation',
        'Auto heater',
        'Leather interior',
        'Cargo cover',
        'Memory seats',
        'Tinted windows',
        'Multi-function steering',
        'Sport seats',
        'Velour interior',
        'Electric windows',
        'Massage seats',
        'Heated steering wheel',
        'Ventilated seats',
    ]),
    ('exterior', 'Exterior', [
        'Alloy wheels',
        'LED headlights',
        'Xenon headlights',
        'Fog lights',
        'Roof rails',
        'Tow hook',
        'Auto-folding mirrors',
        'LED lights',
        'Headlight washer',
        'Summer tire set',
        'Soft-close doors',
        'Xenon lights',
        'Tow hitch',
        'Matrix lights',
        'Sunroof',
        'Winter tire set',
        'LED daytime lights',
        'Panoramic roof',
    ]),
    ('electronics', 'Electronics', [
        'Parking sensors',
        'Adjustable steering',
        'Touchscreen',
        'Digital dashboard',
        'Auto lights',
        'Heated windshield',
        'Navigation / GPS',
        'Start-Stop system',
        'Cruise control',
        'Electric trunk',
        'Paddle shifters',
        'Heated mirrors',
        'Keyless entry',
        'Rain sensor',
        'Auto-dimming mirror',
        'LCD screen',
        'Head-up display (HUD)',
        'Virtual mirrors',
        'Wireless phone charging',
        'Electric mirrors',
    ]),
    ('safety', 'Safety & Security', [
        'ABS',
        'ESP',
        'Airbag (driver)',
        'Airbag (passenger)',
        'Side airbags',
        'Parking sensors',
        'Rear camera',
        'Blind spot monitor',
        'Lane assist',
        'Adaptive cruise control',
        '360° camera',
        'ESP (Stability Control)',
        'Night vision assistant',
        'Front camera',
        'Blind-spot monitoring',
        'Fatigue alert',
        'Alarm / Immobilizer',
        'Hill-hold assist',
        'Airbags',
        'Collision prevention',
        'Auto parking',
        'ISOFIX (child seats)',
        'Tire pressure monitoring',
        'Long-range light assist',
        'Emergency brake (ABS)',
        'Lane keeping assist',
        'Emergency call (eCall)',
        'Traction control system',
        'Dynamic cornering lights',
        'Traffic sign recognition',
        'Follow assist',
    ]),
    ('audio_video', 'Audio, Video & Connectivity', [
        'Bluetooth',
        'Apple CarPlay',
        'Android Auto',
        'USB',
        'Premium sound system',
        'Touchscreen',
        'Apple CarPlay / Android Auto',
        'CD player',
        'Hands-free system',
        'USB port',
        'Audio player',
        'CD changer',
        'MP3 player',
        'USB Type-C port',
        'AUX port',
        'DVD player',
        'Premium audio system',
        'Subwoofer',
        'HiFi audio system',
        'TV screen',
    ]),
    ('electric', 'Electric vehicle features', [
        'APVA grant unused',
        'Bidirectional charging',
        'Heat pump',
        'Three-phase charging',
        'Battery warranty',
        'Fast charging',
    ]),
    ('other', 'Other', [
        'Cruise control',
        'Start/Stop',
        '4x4',
        'AWD',
        'Paddle shifters',
        'Spare tire',
        'Not used as taxi',
        'For sale on leasing',
        'Disabled access',
        'From USA',
        'Remote start',
        'Sport-prepared',
        'Service book',
        'Warranty',
        'Increased engine power',
        'Air suspension',
        'Listing with VIN',
        'Extra key set',
    ]),
]


MOTO_EQUIPMENT_DEFINITION = [
    ('moto_engine', 'Variklis', [
        'Crankshaft',
        'Mufflers',
        'Carburetor',
        'Pistons',
        'Cylinders',
        'Intake manifold',
        'Camshafts',
        'Engine',
        'Cylinder head',
        'Exhaust manifold',
        'Gearbox',
    ]),
    ('moto_chassis', 'Važiuoklė', [
        'Shock absorber',
        'Axles',
        'Brake discs',
        'Forks',
        'Swingarm',
        'Levers',
        'Brake calipers',
        'Handlebar',
        'Chains',
        'Final drive',
        'Hubs',
        'Sprockets',
        'Driveshaft',
        'Frame',
    ]),
    ('moto_electrical', 'Elektra', [
        'Wiring / Electrical',
        'ECU / Computer',
        'Dashboard',
        'Lights',
        'Generator',
        'Turn signals',
        'Starter',
    ]),
    ('moto_cooling', 'Aušinimas', [
        'Radiator',
        'Thermostat',
        'Water radiator',
        'Fan',
        'Oil cooler',
        'Water pump',
    ]),
    ('moto_trim', 'Apdaila', [
        'Trim strips',
        'Seats / Backrests',
        'Fenders',
        'Spoilers',
    ]),
]


GEAR_EQUIPMENT_DEFINITION = [
    ('gear', 'Gear', [
        'Nesibraižantis stiklas',
        'Nerasojantis stiklas',
        'Šildomas stiklas',
        'Ultravioletinių spindulių apsauga',
        'Vidinis saulės skydelis',
        'Pritaikytas Pinlock',
        'Greito atsegimo dirželis',
        'Micrometric užsegimas',
        'Double D-ring užsegimas',
        'Pritaikytas nešiojantiems akinius',
        'Pritaikytas Bluetooth',
        'Nuimami skruostų pagalvėliai',
        'CE armor — shoulders',
        'CE armor — elbows',
        'CE armor — back',
        'CE armor — chest',
        'CE armor — knees',
        'CE armor — hips',
        'Waterproof',
        'Windproof',
        'Thermal liner',
        'Removable liner',
        'Ventilation zippers',
        'Reflective elements',
        'Reinforced impact zones',
        'Connection zipper (jacket↔pants)',
        'Hump (aerodynamic)',
        'Kvėpuojantis pamušalas',
        'Antialerginis pamušalas',
        'Išsegamas ir skalbiamas pamušalas',
        'Drėgmę sugerianti vidinė danga',
        'Touchscreen-compatible',
        'Knuckle protector',
        'Palm slider',
        'Long cuff',
        'Short cuff',
        'Ankle protection',
        'Shin protection',
        'Toe slider',
        'Heel protection',
        'Reinforced sole',
        'Magnetic mount',
        'Strap mount',
        'Rain cover',
        'Expandable',
        'Laptop compartment',
        'Keičiama',
    ]),
]


TRUCK_EQUIPMENT_DEFINITION = [
    ('truck_body', 'Body', [
        'Aluminum floor',
        'Aluminum side panels',
        'Hydraulics',
        'Rear doors',
        'Side doors',
        'Air suspension',
        'Central lubrication',
        'Two-way tipper',
        'Three-way tipper',
        'Lift axle',
        'For bulk cargo',
        'Spare wheel',
        'Additional fuel tank',
        'Refrigeration unit',
        'Alarm',
        'Tail lift',
        'Springs',
        'Hook / winch',
        'Crane / manipulator',
        'Bucket / grapple',
    ]),
    ('truck_cabin', 'Cabin', [
        'Sunroof',
        'Heated seat',
        'Air conditioning',
        'Double cabin',
        'Mini kitchen',
        'Tilt cabin',
        'Personal lighting',
        'Low cabin',
        'Personal ventilation',
        'Power steering',
    ]),
    ('truck_electronics', 'Electronics', [
        'Cruise control',
        'Electric mirrors',
        'Navigation / GPS',
        'Auxiliary heater',
        'Tachograph',
        'Electric steering adjustment',
        'Electric windows',
        'Onboard computer',
        'Climate control',
    ]),
    ('truck_safety', 'Safety', [
        'ABS',
        'ADR (hazmat)',
        'Cargo straps',
        'Airbags',
        'EBS',
        'Engine brake / retarder',
        'Locking differential',
        'ESP',
        'Trailer brake',
        'Hill-start assist',
    ]),
    ('truck_audio_video', 'Audio/Video', [
        'Audio system',
        'Video system',
    ]),
    ('truck_other', 'Other', [
        'Metallic paint',
        'Trailer hitch',
        'Not used in Lithuania',
        'Open to trade',
        'For sale on lease',
        'Service book',
    ]),
]


TRUCK_PARTS_EQUIPMENT_DEFINITION = [
    ('truck_part_engine', 'Variklio detalės', [
        'Crankshaft',
        'Intake manifold',
        'Injection system',
        'Exhaust manifold',
        'Carburetor',
        'Pistons',
        'Engine block',
        'Cylinder head',
        'Engine',
        'Engine bracket',
    ]),
    ('truck_part_body', 'Kėbulo detalės', [
        'Trim parts',
        'Trim strips',
        'Bumpers',
        'Bumper reinforcements',
        'Hood',
        'Doors',
        'Frame rails',
        'Radiator grille',
        'Sills',
        'Fenders',
        'Fender flares',
        'Spoilers',
        'Glass',
        'Roof',
        'Mirrors',
        'Lights',
    ]),
    ('truck_part_chassis', 'Važiuoklės detalės', [
        'Shock absorber',
        'Rear axle beam',
        'Driveshaft',
        'Gearbox',
        'Half-shafts',
        'Reducer / differential',
        'Brake discs',
        'Brake calipers',
        'Hubs',
        'Forks',
        'Engine cradle',
    ]),
    ('truck_part_cooling', 'Aušinimo detalės', [
        'A/C radiator',
        'Radiator',
        'Cabin heater',
        'Oil cooler',
        'Viscous fan coupling',
        'Water pump',
        'Water radiator',
        'Fan',
    ]),
    ('truck_part_electrical', 'Elektros detalės', [
        'Wiring',
        'Alternator',
        'Computer',
        'Starter',
    ]),
    ('truck_part_interior', 'Salono detalės', [
        'Trim parts',
        'Door panels',
        'Dashboard',
        'Instrument cluster',
        'Seats',
        'SRS airbags',
        'Headliner',
    ]),
    ('truck_part_superstructure', 'Antstato detalės', [
        'Car carrier body',
        'Concrete mixer body',
        'Flatbed platform',
        'Tank',
        'Livestock carrier body',
        'Insulated body',
        'Hard-side body',
        'Container carrier',
        'Crane',
        'Timber carrier body',
        'Platform body',
        'Tipper body',
        'Refrigerator body',
        'Tarpaulins',
    ]),
]


# Etalono sec 04 ypatumai, kurių mūsų sąraše nebuvo — be jų išplėstinė
# paieška rodė 5 iš 16 (2026-08-20 auditas).
TRUCK_ADVANCED_EQUIPMENT = [
    ('truck_advanced', 'Papildoma įranga', [
        '„Webasto“',
        'ADR',
        'Autopilotas',
        'Blokuojamas diferencialas',
        'CB radio įranga',
        'Kalnų stabdis',
        'Liftas',
        'Šaldymo įranga',
        'Su priekaba',
        'Tachografas',
        'Galiojanti techninė apžiūra (TA)',
    ]),
]

# Etalono sec 02 ypatumai (motociklai)
MOTO_ADVANCED_EQUIPMENT = [
    ('moto_advanced', 'Papildoma įranga', [
        '4x4 varantys ratai',
        'Audio aparatūra',
        'Automatinė pavarų dėžė',
        'Dempferis',
        'El. starteris',
        'Keleivio atlošas',
        'LED dienos žibintai',
        'Lietuvoje neeksploatuotas',
        'Lopšys',
        'Platus galinis ratas',
        'Priekinis stiklas',
        'Su dokumentais',
        'Kelioniniai krepsiai',
        'Šildomos rankenos',
        'Galiojanti techninė apžiūra (TA)',
    ]),
]

# Etalono sec 05 ypatumai (vandens transportas)
BOAT_EQUIPMENT_DEFINITION = [
    ('boat_features', 'Ypatumai', [
        'Elektrinis starteris',
        'Kuro žarna',
        'Papildomas kuro bakas',
        'Rankinis užvedimas',
        'Sraigtas',
        'Su auto priekaba',
        'Variklio defektas',
    ]),
]


CATEGORY_EQUIPMENT = {
    'trailers': TRAILER_EQUIPMENT_DEFINITION,
    'agriculture': AGRI_EQUIPMENT_DEFINITION,
    'loading-equipment': LOAD_EQUIPMENT_DEFINITION,
    'camping-houses': CAMP_EQUIPMENT_DEFINITION,
    'rental': RENT_EQUIPMENT_DEFINITION,
    'services': SVC_EQUIPMENT_DEFINITION,
    'electronics': ELEC_EQUIPMENT_DEFINITION,
    'bicycles': BIKE_EQUIPMENT_DEFINITION,
    # ─── senosios kategorijos (turinys perkeltas iš DB) ───
    'cars': CARS_EQUIPMENT_DEFINITION,
    'motorcycles': MOTO_EQUIPMENT_DEFINITION + MOTO_ADVANCED_EQUIPMENT,
    'motogear': GEAR_EQUIPMENT_DEFINITION,
    'trucks': TRUCK_EQUIPMENT_DEFINITION + TRUCK_ADVANCED_EQUIPMENT,
    'truck-parts': TRUCK_PARTS_EQUIPMENT_DEFINITION,
    'boats': BOAT_EQUIPMENT_DEFINITION,
}


def iter_equipment():
    """(category_key, name) poros visoms kategorijoms."""
    for definition in CATEGORY_EQUIPMENT.values():
        for cat_key, _label, names in definition:
            for name in names:
                yield cat_key, name


def seed(equipment_model):
    """Idempotentiškai sukuria trūkstamas eilutes. Grąžina (sukurta, viso).

    Priima modelio klasę, kad tiktų ir migracijai (apps.get_model), ir
    management komandai (tiesioginis importas).
    """
    created = 0
    total = 0
    for cat_key, name in iter_equipment():
        total += 1
        _obj, was_created = equipment_model.objects.get_or_create(
            category=cat_key, name=name,
        )
        if was_created:
            created += 1
    return created, total
