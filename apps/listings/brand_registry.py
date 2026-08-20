# apps/listings/brand_registry.py
# ═══════════════════════════════════════════════════════════
# MARKIŲ ŠEIMOS — vienas sąrašas visoms tos pačios transporto
# priemonės kategorijoms.
#
# Šis failas SĄMONINGAI neimportuoja Django — jį naudoja ir
# migracijos, ir seed_brands komanda, ir view'ai.
#
# Kodėl būtent taip: autogide (2026-08 patikra per Chrome) dalių
# formos markių sąrašas yra IDENTIŠKAS transporto priemonės
# sąrašui — auto 229/229, moto 515/515, sunkvežimiai 251/251,
# žemės ūkis 729/729 (lyginta turiniu, ne dydžiu). Nuomos
# sekcijos savo sąrašų neturi visai — jos turi lauką „Tipas",
# kuris perjungia į atitinkamos pardavimo kategorijos sąrašą.
# ═══════════════════════════════════════════════════════════

# key, LT pavadinimas, ar turi modelių kaskadą, eiliškumas
SCOPES = [
    ('cars',          'Automobiliai',                   True,  10),
    ('motorcycles',   'Motociklai',                     True,  20),
    ('trucks',        'Sunkusis transportas',           False, 30),
    ('trailers',      'Priekabos, puspriekabės',        False, 40),
    ('agriculture',   'Žemės ūkio technika',            False, 50),
    ('construction',  'Statybinė technika',             False, 60),
    ('loading',       'Krovimo, sandėliavimo technika', False, 70),
    ('forestry',      'Miško ūkio technika',            False, 80),
    ('campers',       'Turistiniai nameliai, kemperiai', False, 90),
    ('gear',          'Moto apranga',                   False, 100),
    ('electronics',   'Video, audio, navigacijos',      False, 110),
    ('bicycles',      'Dviračiai, paspirtukai',         False, 120),
]

# Šeimos sėklos failas (apps/listings/management/commands/).
# Kur turim ir seną lentelę, ir autogidas failą — sėjam abu:
# failas duoda pilnumą, lentelė — susiejimą su esamais skelbimais.
SCOPE_SEED_FILES = {
    'cars':         ['nuomos-auto-markes.txt', 'brands.txt'],
    'motorcycles':  ['nuomos-moto-markes.txt'],
    'trucks':       ['nuomos-sunkiojo-markes.txt'],
    'trailers':     ['priekabu-markes.txt'],
    'agriculture':  ['zemes-ukio-markes.txt'],
    'construction': ['statybines-markes.txt'],
    'loading':      ['krovimo-markes.txt'],
    'forestry':     ['misko-markes.txt'],
    'campers':      ['nameliu-markes.txt'],
    'electronics':  ['elektronikos-markes.txt'],
    'bicycles':     ['paspirtuku-markes.txt'],
    # 'gear' sėjamas iš GearBrand lentelės, failo neturim
}

# Senosios lentelės, iš kurių taip pat traukiam markes ir kurias
# susiejam per Brand.legacy_* (kad forma rodytų Brand, o saugotų
# į seną FK be spėliojimo pagal pavadinimą).
SCOPE_LEGACY_MODEL = {
    'motorcycles': 'MotorcycleBrand',
    'trucks':      'TruckBrand',
    'gear':        'GearBrand',
}

# ── Kategorija → šeima ────────────────────────────────────────
# Raktas: subcategory slug, jei jo nėra — vehicle_type slug.
# Dalys ir nuoma rodo TĄ PATĮ sąrašą kaip transporto priemonė.
SCOPE_BY_VEHICLE_TYPE = {
    'cars':                 'cars',
    'vans':                 'cars',
    'motorcycles':          'motorcycles',
    'trucks':               'trucks',
    'trailers':             'trailers',
    'agriculture':          'agriculture',
    'construction':         'construction',
    'forestry':             'forestry',
    'camping-houses':       'campers',
    'electronics':          'electronics',
    'bicycles':             'bicycles',
}

SCOPE_BY_SUBCATEGORY = {
    # ── Dalys ────────────────────────────────────────────────
    'car-parts':              'cars',
    'single-part-or-kit':     'cars',
    'whole-car-for-parts':    'cars',
    'accessories-tuning':     'cars',
    'moto-parts':             'motorcycles',
    'single-moto-part':       'motorcycles',
    'whole-moto-for-parts':   'motorcycles',
    'truck-parts':            'trucks',
    'single-truck-part':      'trucks',
    'whole-truck-for-parts':  'trucks',
    'agri-special-parts':     'agriculture',
    # ── Moto apranga (atskira šeima — ne motociklų markės) ───
    'moto-gear':              'gear',
    'helmets':                'gear',
    'jackets':                'gear',
    'pants':                  'gear',
    'suits':                  'gear',
    'gloves':                 'gear',
    'boots':                  'gear',
    'protective-gear':        'gear',
    'bags':                   'gear',
    'other-gear':             'gear',
    # ── Miško technika gyvena po žemės ūkiu ──────────────────
    'forestry-machines':      'forestry',
}

# ── Nuomos tipas → šeima ─────────────────────────────────────
# Autogide nuomos forma pati markių neturi: pasirinkus „Tipą"
# užsikrauna atitinkamos pardavimo kategorijos sąrašas.
SCOPE_BY_RENT_TYPE = {
    'passenger_minibus': 'cars',
    'cargo_minibus':     'cars',
    'bus':               'cars',
    'moto_rental':       'motorcycles',
    'truck':             'trucks',
    'tractor_unit':      'trucks',
    'road_train':        'trucks',
    'trailer':           'trailers',
    'agri_constr':       'agriculture',
    'warehouse':         'loading',
    'touring_car':       'campers',
    'towed_house':       'campers',
    # 'water' — laivų neliečiam (sutarta), šeimos neturi
}

def scope_for(vehicle_type_slug=None, subcategory_slug=None, rent_type=None):
    """Grąžina šeimos raktą arba None.

    Tikrinam nuo siauriausio: nuomos tipas → subkategorija → VT.
    """
    if rent_type and rent_type in SCOPE_BY_RENT_TYPE:
        return SCOPE_BY_RENT_TYPE[rent_type]
    if subcategory_slug and subcategory_slug in SCOPE_BY_SUBCATEGORY:
        return SCOPE_BY_SUBCATEGORY[subcategory_slug]
    if vehicle_type_slug and vehicle_type_slug in SCOPE_BY_VEHICLE_TYPE:
        return SCOPE_BY_VEHICLE_TYPE[vehicle_type_slug]
    return None
