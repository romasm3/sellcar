"""Ratlankių ir padangų naršymo filtrai.

Etalonas — docs/autogidas-ratlankiai-padangos.md (autogidas.lt). Ratlankiai
ir padangos yra DVI ATSKIROS kategorijos, todėl ir laukų rinkiniai atskiri:
bendro „Tipas: ratlankiai / padangos" perjungiklio nėra.

Čia gyvena TIK reikšmių sąrašai ir laukų aprašai; filtravimas —
wheels_views._apply_wheels_filters, atvaizdavimas — wheels_list.html.
Create forma šių sąrašų nenaudoja ir nesikeičia.
"""

from django.utils.translation import gettext

# ═══════════════════════════════════════════════════════════
# REIKŠMIŲ SĄRAŠAI (etalono tvarka ir užrašai)
# ═══════════════════════════════════════════════════════════

# Ratlankių skersmuo R4–R42 (etalonas). DB `diameter` saugo skaičių be „R".
RIM_DIAMETERS = [
    '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15',
    '16', '16.5', '17', '17.5', '18', '19', '19.5', '20', '21', '22',
    '22.5', '23', '24', '24.5', '26', '26.5', '28', '29', '30', '32',
    '34', '38', '42',
]

# Padangų skersmuo su C variantais (etalonas).
TYRE_DIAMETERS = [
    '4', '5', '6', '8', '9', '10', '11', '12',
    '13', '13C', '14', '14C', '15', '15C', '16', '16C', '17', '17C',
    '17.5', '18', '19', '19.5', '20', '21', '22', '22.5', '23', '24',
    '24.5', '25', '26', '28', '30', '32', '34', '38', '42', '44', '46',
    '49', '51', '54', '57', '63',
]

RIM_BOLT_COUNTS = ['1', '3', '4', '5', '6', '8', '10', '12']

# Tarpai tarp skylių (mm) — standartinės PCD reikšmės.
RIM_PCD_MM = [
    '92.25', '95.25', '98.00', '100.00', '105.00', '108.00', '110.00',
    '112.00', '114.30', '115.00', '118.00', '120.00', '120.65', '125.00',
    '127.00', '130.00', '135.00', '139.70', '150.00', '160.00', '161.00',
    '165.10', '170.00', '180.00', '190.50', '200.00', '205.00', '208.00',
    '210.00', '220.00', '222.25',
]

# Centrinės skylės diametras (mm).
RIM_CENTRE_BORES = [
    '43.0', '54.1', '56.1', '56.5', '56.6', '57.1', '58.1', '58.6',
    '60.1', '63.3', '63.4', '64.1', '65.1', '66.1', '66.5', '66.6',
    '67.1', '70.0', '70.1', '71.5', '71.6', '72.5', '72.6', '73.1',
    '74.1', '78.1', '82.0', '84.1', '87.1', '89.1', '92.5', '93.1',
    '95.3', '98.5', '100.0', '106.0', '108.0', '110.1', '116.0',
    '120.0', '130.0', '143.0', '161.0',
]

# Plotis coliais; paskutinė reikšmė — „daugiau nei 11".
RIM_WIDTHS = ['5', '5.5', '6', '6.5', '7', '7.5', '8', '8.5', '9',
              '9.5', '10', '11']
RIM_WIDTH_OVER = 'gt11'

# Padangų plotis ir profilis (etalonas; papildoma DB reikšmėmis).
TYRE_WIDTHS = ['135', '145', '155', '165', '175', '185', '195', '205',
               '215', '225', '235', '245', '255', '265', '275', '285',
               '295', '305', '315', '325', '335', '345', '355']
TYRE_PROFILES = ['25', '30', '35', '40', '45', '50', '55', '60', '65',
                 '70', '75', '80', '85', '90']

# Protektoriaus gylis (mm).
TREAD_DEPTHS = ['1', '1.5', '2', '2.5', '3', '3.5', '4', '4.5', '5',
                '5.5', '6', '6.5', '7', '7.5', '8', '9', '10', '12',
                '14', '16', '18', '20', '25', '30', '35', '40']

RIM_PRICES = ['5', '10', '15', '20', '25', '30', '35', '40', '50', '60',
              '70', '80', '90', '100', '125', '150', '175', '200', '300',
              '400', '500', '600', '700', '800', '900', '1000']
TYRE_PRICES = RIM_PRICES + ['1250', '1500', '2000', '2500', '3000']

# Padangų paskirtis — etalono užrašai mūsų reikšmėms. Modelio
# WHEEL_PURPOSE_CHOICES nekeičiam: jį naudoja create forma.
TYRE_PURPOSE_LABELS = [
    ('passenger', 'Lengviesiems'),
    ('moto', 'Motociklams'),
    ('commercial', 'Mikroautobusams'),
    ('truck', 'Sunkvežimiams ir autobusams'),
    ('industrial', 'Traktoriams ir spec technikai'),
    ('suv', 'Visureigiams'),
]

TYRE_SEASON_LABELS = [
    ('summer', 'Vasarinės'),
    ('all_season', 'Universalios'),
    ('winter', 'Žieminės'),
]

RIM_TYPE_LABELS = [
    ('accessory', 'Priedai'),
    ('alloy', 'Lengvojo lydinio'),
    ('steel', 'Plieniniai štampuoti'),
    ('forged', 'Kalti'),
    ('spare', 'Atsarginis ratas'),
    ('hubcap', 'Ratų gaubtai'),
    ('centercap', 'Ratlankių dangteliai'),
]

CONDITION_RIM_LABELS = [('used', 'Naudoti'), ('new', 'Nauji')]
CONDITION_TYRE_LABELS = [('used', 'Naudotos'), ('new', 'Naujos')]

AGE_CHOICES = [
    ('1d', 'Vienos dienos'),
    ('1d_new', 'Vienos dienos (tik nauji)'),
    ('3d', 'Trijų dienų'),
    ('7d', 'Savaitės'),
    ('14d', 'Dviejų savaičių'),
]
AGE_DAYS = {'1d': 1, '1d_new': 1, '3d': 3, '7d': 7, '14d': 14}

SELLER_TYPE_CHOICES = [('private', 'Privatus'), ('dealer', 'Verslas')]

RIM_FEATURES = [
    ('feat_sold_single', 'Parduodu po vieną'),
    ('rim_feat_with_tyres', 'Su padangom'),
    ('rim_feat_original', 'Originalūs ratlankiai'),
    ('rim_feat_chromed', 'Chromuoti'),
    ('rim_feat_bent', 'Aplankstyti ratlankiai'),
]

TYRE_FEATURES = [
    ('feat_suv', 'Visureigių padangos'),
    ('feat_sport', 'Sportinės padangos'),
    ('feat_reinforced', 'Sustiprintos'),
    ('feat_sold_single', 'Parduodamos po vieną'),
    ('feat_run_flat', 'Run on flat'),
    ('feat_spare_thin', 'Atsarginė padanga „plona“'),
    ('feat_rain', 'Lietaus padangos'),
    ('feat_studded', 'Žieminės dygliuotos'),
]

# Greitos nuorodos virš rezultatų (tik ratlankiams) — etalono tvarka.
RIM_QUICK_LINKS = [
    ('alloy', 'Lengvojo lydinio'),
    ('steel', 'Plieniniai štampuoti'),
    ('spare', 'Atsarginis ratas'),
    ('hubcap', 'Ratų gaubtai'),
    ('centercap', 'Ratlankių dangteliai'),
    ('forged', 'Kalti'),
    ('accessory', 'Priedai'),
]


def quick_links():
    """Greitos nuorodos virš rezultatų (ratlankiams) — su vertimais."""
    return [(v, gettext(l)) for v, l in RIM_QUICK_LINKS]


def _sk(v):
    """Rūšiavimo raktas skaitinei reikšmei su galimu „C" (13C) priedu."""
    try:
        return (float(str(v).rstrip('Cc')), str(v))
    except ValueError:
        return (0.0, str(v))


def _su_db(bazinis, db_reiksmes):
    """Etalono sąrašas + tai, kas realiai yra DB (spec. technikos dydžiai)."""
    visi = list(bazinis) + [v for v in db_reiksmes if v and v not in bazinis]
    return sorted(set(visi), key=_sk)


# ═══════════════════════════════════════════════════════════
# LAUKŲ APRAŠAI ŠABLONUI
# ═══════════════════════════════════════════════════════════

def _select(label, param, options, placeholder='Visi'):
    return {
        'type': 'select',
        'label': gettext(label),
        'param': param,
        'placeholder': gettext(placeholder),
        'options': [(v, gettext(str(l)) if isinstance(l, str) else l)
                    for v, l in options],
    }


def _range(label, param_min, param_max, values, unit=''):
    opts = [(v, v) for v in values]
    return {
        'type': 'range',
        'label': gettext(label) + (f' ({unit})' if unit else ''),
        'param_min': param_min,
        'param_max': param_max,
        'options_min': opts,
        'options_max': opts,
    }


def sidebar_fields(product_type, brand_names, cities, tyre_widths_db=(),
                   tyre_profiles_db=(), vehicle_brands=()):
    """Šoninės juostos laukai vienai kategorijai (etalono eilės tvarka)."""
    from .models import WheelListing

    bendri_pabaiga = [
        _select('Šalis', 'country_filter',
                [(c, n) for c, n in WheelListing.COUNTRY_CHOICES],
                placeholder='Visos šalys'),
        _select('Miestas', 'city', [(c, c) for c in cities],
                placeholder='Visi miestai'),
        _select('Rodyti ne senesnius nei', 'age', AGE_CHOICES),
        _select('Pardavėjo tipas', 'seller_type', SELLER_TYPE_CHOICES),
        {'type': 'text', 'label': gettext('Tekstinė paieška'), 'param': 'q',
         'placeholder': gettext('Ieškoti...')},
    ]

    if product_type == 'rim':
        laukai = [
            _select('Tipas', 'rim_material', RIM_TYPE_LABELS),
            _select('Skersmuo', 'diameter',
                    [(d, f'R{d}') for d in RIM_DIAMETERS]),
            _select('Tvirtinimo taškai', 'rim_bolt_count',
                    [(b, b) for b in RIM_BOLT_COUNTS]),
            _select('Tarpai tarp skylių (mm)', 'rim_pcd_mm',
                    [(p, p) for p in RIM_PCD_MM]),
            _select('Centr. skylės diametras', 'rim_dia',
                    [(d, d) for d in RIM_CENTRE_BORES]),
            _select('Plotis (coliais)', 'rim_width',
                    [(w, w) for w in RIM_WIDTHS] + [(RIM_WIDTH_OVER, '>11')]),
            _select('Gamintojas', 'manufacturer', [(b, b) for b in brand_names],
                    placeholder='Visi gamintojai'),
            _select('Tr. priem. markė', 'fits_brand',
                    [(b, b) for b in vehicle_brands],
                    placeholder='Visos markės'),
            _range('Kaina', 'price_from', 'price_to', RIM_PRICES),
            _select('Kiekis', 'quantity',
                    [(str(n), str(n)) for n in range(1, 10)]),
            _select('Naudoti/Nauji', 'condition', CONDITION_RIM_LABELS),
        ] + bendri_pabaiga
        features = RIM_FEATURES
    else:
        laukai = [
            _select('Paskirtis', 'purpose', TYRE_PURPOSE_LABELS),
            _select('Sezoniškumas', 'tyre_season', TYRE_SEASON_LABELS),
            _select('Naudotas/Naujas', 'condition', CONDITION_TYRE_LABELS),
            _select('Skersmuo', 'diameter',
                    [(d, f'R{d}') for d in TYRE_DIAMETERS]),
            _select('Plotis', 'tyre_width',
                    [(w, w) for w in _su_db(TYRE_WIDTHS, tyre_widths_db)]),
            _select('Aukštis (profilis)', 'tyre_profile',
                    [(p, p) for p in _su_db(TYRE_PROFILES, tyre_profiles_db)]),
            _range('Kaina', 'price_from', 'price_to', TYRE_PRICES),
            _select('Gamintojas', 'manufacturer', [(b, b) for b in brand_names],
                    placeholder='Visi gamintojai'),
            _range('Protektoriaus gylis', 'tread_from', 'tread_to',
                   TREAD_DEPTHS, unit='mm'),
            _select('Kiekis', 'quantity',
                    [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
                     ('5plus', gettext('5 ir daugiau'))]),
        ] + bendri_pabaiga
        features = TYRE_FEATURES

    return laukai, [(p, gettext(l)) for p, l in features]
