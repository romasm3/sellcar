# apps/listings/search_config/panels.py
# ═══════════════════════════════════════════════════════════
# DEKLARATYVUS PAIEŠKOS PANELIŲ SLUOKSNIS
#
# Vienas duomenų šaltinis — paneles-config.json (autogidas etalonas,
# papildytas `db_field` / `param` raktais). Šis modulis jį užkrauna kartą
# importo metu ir praturtina tuo, ko JSON laikyti negali: gettext
# etiketėmis, nuorodomis į modelio choices ir markių užklausa.
#
# Kodėl ne fixture: fixture reikalautų modelio + migracijos, o naujų
# migracijų šioje vertikalėje nekuriame. Python modulis dar ir
# git-diffinasi, ir leidžia lazy vertimus.
#
# ĮJUNGIMO TAISYKLĖ (žr. is_active): kategorija rodo panelę tik jei
#   a) ji remiasi Listing modeliu ir eina per listing_list, IR
#   b) visi jos laukai turi db_field.
# Kitos lieka konfigūracijoje, bet neaktyvios — įsijungs pačios, kai
# atsiras jų laukai. Neaktyvi kategorija panelės <div> visai nerenderina.
# ═══════════════════════════════════════════════════════════

import json
import os

from django.db.models import Count, Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'paneles-config.json')
ADVANCED_PATH = os.path.join(os.path.dirname(__file__), 'isplestine-config.json')

# Kategorijos, kurių paiešką aptarnauja Listing + listing_list.
# tires/wheels sukasi apie WheelListing, o parts/motogear tab'ai turi savo
# browse view'us — jiems šis variklis netinka be daug didesnio refaktoringo.
LISTING_BACKED = {'cars', 'motorcycles', 'trucks', 'boats', 'trailers', 'agriculture', 'construction', 'loading-equipment', 'forestry', 'camping-houses',
                  'rental', 'services'}

# 1 ETAPAS: markė→modelis AJAX kaskados variklis dar nepalaiko, todėl
# cars/motorcycles kol kas lieka su savo blokais search_panel.html.
# Įtraukus kaskadą — pridėk juos čia.
ENGINE_ENABLED = {'trucks', 'boats', 'trailers', 'agriculture', 'construction', 'loading-equipment', 'forestry', 'camping-houses',
                  'rental', 'services'}

# db_field → iš kur imti reikšmių sąrašą (choices). Etiketės mūsų modelyje
# jau sutampa su etalonu 1:1 (Tipas 2/2, Paskirtis 22/22), todėl JSON
# `options` lieka dokumentacija, o reikšmės imamos iš modelio.
CHOICES_BY_DB_FIELD = {
    'trailer_kind':    'TRAILER_KIND_CHOICES',
    'trailer_purpose': 'TRAILER_PURPOSE_CHOICES',
    'trailer_axle_count': 'TRAILER_AXLE_COUNT_CHOICES',
    'agri_type': 'AGRI_TYPE_CHOICES',
    'agri_kind': 'AGRI_KIND_CHOICES',
    'constr_type': 'CONSTR_TYPE_CHOICES',
    'constr_attach_type': 'CONSTR_ATTACH_TYPE_CHOICES',
    'constr_drive_type': 'CONSTR_DRIVE_TYPE_CHOICES',
    'load_type': 'LOAD_TYPE_CHOICES',
    'forest_type': 'FOREST_TYPE_CHOICES',
    'camp_type': 'CAMP_TYPE_CHOICES',
    'rent_type': 'RENT_TYPE_CHOICES',
    'service_type': 'SERVICE_TYPE_CHOICES',
    'doors': 'DOOR_CHOICES',
    'cooling_type': 'COOLING_TYPE_CHOICES',
    'trailer_kind': 'TRAILER_KIND_CHOICES',
    'defects': 'DEFECT_CHOICES',
    'load_energy_source': 'LOAD_ENERGY_CHOICES',
    'wheel_formula': 'WHEEL_FORMULA_CHOICES',
    'color':           'COLOR_CHOICES',
    'truck_type':      'TRUCK_TYPE_CHOICES',
    'boat_type':       'BOAT_TYPE_CHOICES',
    'body_type':       'BODY_TYPE_CHOICES',
    'motorcycle_type': 'MOTORCYCLE_TYPE_CHOICES',
    'euro_standard':   'EURO_STANDARD_CHOICES',
    'condition':       'CONDITION_CHOICES',
}

# db_field, kurių reikšmės — laisvas tekstas iš skelbimų (ne choices).
# Rodomos su skelbimų kiekiais, Top N + likusios abėcėle.
TEXT_BRAND_FIELDS = {'trailer_brand_text', 'agri_brand_text', 'constr_brand_text', 'load_brand_text', 'forest_brand_text',
                     'camp_brand_text', 'rent_brand_text'}

# FK markės — reikšmė yra id, etiketė iš susieto modelio.
# db_field → (modelio vardas apps.listings.models, susiejimo laukas)
FK_BRAND_FIELDS = {'truck_brand': 'TruckBrand'}

# Laukai, kurių reikšmės — laisvas tekstas iš skelbimų (Miestas).
DISTINCT_VALUE_FIELDS = {'city'}

# FK laukai, kurių reikšmių sąrašas — atskira lentelė (ne choices).
# Reikšmė filtre yra id, todėl bendra .filter(<laukas>=id) logika tinka
# be pakeitimų; čia tik pasiimam etiketes. Etalono `options` lietuviški,
# o lentelėse vardai angliški — sutapdinam per gettext (vertimai jau yra,
# žr. translatable_db.FUEL_AND_TRANSMISSION_NAMES), kad kategorija rodytų
# būtent etalono poaibį (pvz. motociklų nuomai — tik Benzinas / Elektra).
FK_CHOICE_FIELDS = {'fuel_type': 'FuelType', 'transmission': 'Transmission'}


def _fk_options(db_field, config_options=None):
    from apps.listings import models as m
    from django.utils.translation import gettext
    model = getattr(m, FK_CHOICE_FIELDS[db_field])
    rows = [(o.pk, gettext(o.name)) for o in model.objects.all()]
    if config_options:
        wanted = {str(o).strip() for o in config_options}
        subset = [r for r in rows if r[1] in wanted]
        if subset:
            rows = subset
    return sorted(rows, key=lambda r: r[1])

TOP_BRANDS = 10

# Ypatumų Equipment kategorijų prefiksas pagal kategoriją. Reikalingas, nes
# tie patys pavadinimai (ABS, Hidraulika) egzistuoja kelioms kategorijoms —
# ieškant vien pagal name būtų paimta svetima eilutė.
EQUIPMENT_PREFIX = {'trailers': 'trailer_', 'agriculture': 'agri_',
                    'loading-equipment': 'load_', 'camping-houses': 'camp_',
                    'rental': 'rent_', 'services': 'svc_'}

# Kainos pakopos — tos pačios, kurias naudoja automobilių panelė.
PRICE_MIN_TIERS = [500, 1000, 2000, 3000, 5000, 7500, 10000, 15000, 20000, 30000]
PRICE_MAX_TIERS = [1000, 2000, 3000, 5000, 7500, 10000, 15000, 20000, 30000, 50000]

# Metai: kas metus iki 1985, toliau retėjant (autogidas).
YEAR_TAIL = [1980, 1975, 1970, 1965, 1960, 1950, 1940, 1930, 1927, 1925]


def _load():
    with open(CONFIG_PATH, encoding='utf-8') as fh:
        return json.load(fh)


_RAW = _load()

# vt_slug → kategorijos konfigūracija. Kelios autogidas sekcijos gali
# rodyti į tą patį VT (pvz. Vilkikai ir Autobusai → trucks); imame pirmą,
# t. y. pagrindinę sekciją.
PANELS = {}
# Subkategorijų konfigūracijos: vienam VT gali būti kelios sekcijos
# (construction: technika sec 24 + priedai sec 16). Raktas — subcategory slug.
PANELS_BY_SUB = {}
for _cat in _RAW['categories']:
    _vt = _cat.get('vt_slug')
    if not _vt:
        continue
    _sub = _cat.get('subcategory_slug')
    if _sub:
        PANELS_BY_SUB[_sub] = _cat
    elif _vt not in PANELS:
        PANELS[_vt] = _cat

with open(ADVANCED_PATH, encoding='utf-8') as _fh:
    _RAW_ADV = json.load(_fh)

# Išplėstinė paieška — tas pats mechanizmas, tik platesnis laukų rinkinys.
ADVANCED = {}
ADVANCED_BY_SUB = {}
for _cat in _RAW_ADV['categories']:
    _vt = _cat.get('vt_slug')
    if not _vt:
        continue
    _sub = _cat.get('subcategory_slug')
    if _sub:
        ADVANCED_BY_SUB[_sub] = _cat
    elif _vt not in ADVANCED:
        ADVANCED[_vt] = _cat

# Kategorijos, kurių išplėstinė paieška įjungta (kaip ENGINE_ENABLED panelėms)
ADVANCED_ENABLED = {'trailers', 'agriculture', 'construction', 'loading-equipment', 'forestry', 'camping-houses',
                    'rental', 'services'}

SORT_OPTIONS = [
    ('newest',     _('Nauji ir atnaujinti viršuje')),
    ('price_asc',  _('Pigiausi viršuje')),
    ('price_desc', _('Brangiausi viršuje')),
]


def advanced_is_active(vt_slug):
    return vt_slug in ADVANCED_ENABLED and vt_slug in ADVANCED


def advanced_categories():
    return sorted(s for s in ADVANCED if advanced_is_active(s))


def _panel_cfg(vt_slug, sub_slug=None):
    """Konfigūracija VT arba jo subkategorijai.

    Vienam VT gali būti kelios etalono sekcijos: construction turi
    technikos (sec 24) ir priedų (sec 16) formas su skirtingais laukais.
    Priedų sekcija pažymėta `subcategory_slug`.
    """
    if sub_slug and sub_slug in PANELS_BY_SUB:
        return PANELS_BY_SUB[sub_slug]
    return PANELS.get(vt_slug)


def _advanced_cfg(vt_slug, sub_slug=None):
    if sub_slug and sub_slug in ADVANCED_BY_SUB:
        return ADVANCED_BY_SUB[sub_slug]
    return ADVANCED.get(vt_slug)


def is_active(vt_slug):
    """Ar kategorija turi veikiančią deklaratyvią panelę."""
    cat = PANELS.get(vt_slug)
    if not cat or vt_slug not in LISTING_BACKED or vt_slug not in ENGINE_ENABLED:
        return False
    return all(f.get('db_field') for f in cat['fields'] if f.get('active', True))


def active_categories():
    return sorted(s for s in PANELS if is_active(s))


def _price_tiers():
    fmt = lambda v: f'{v:,}'.replace(',', ' ')
    return ([(v, fmt(v)) for v in PRICE_MIN_TIERS],
            [(v, fmt(v)) for v in PRICE_MAX_TIERS])


def _years():
    return list(range(timezone.now().year, 1984, -1)) + YEAR_TAIL


def _brand_rows(vt_slug, db_field, user=None, sub_slug=None):
    """Markės su skelbimų kiekiais — VIENA agregacija, be N+1.

    Grąžina (top, rest); kiekvienas įrašas: {'value', 'name', 'count'}.
    Tekstinėms markėms value == name, FK markėms value == id.
    """
    from apps.listings.views import _public_listings_qs

    qs = _public_listings_qs(user).filter(vehicle_type__slug=vt_slug)
    if sub_slug:
        qs = qs.filter(subcategory__slug=sub_slug)

    if db_field in FK_BRAND_FIELDS:
        from apps.listings import models as m
        model = getattr(m, FK_BRAND_FIELDS[db_field])
        counts = {
            r[f'{db_field}_id']: r['c']
            for r in qs.exclude(**{f'{db_field}__isnull': True})
                       .values(f'{db_field}_id').annotate(c=Count('id'))
        }
        rows = [{'value': o.pk, 'name': o.name, 'count': counts.get(o.pk, 0)}
                for o in model.objects.all()]
    else:
        if db_field == 'agri_brand_text':
            from apps.listings.agriculture_views import AGRI_BRANDS as ALL_NAMES
        elif db_field == 'constr_brand_text':
            from apps.listings.construction_views import CONSTR_BRANDS as ALL_NAMES
        elif db_field == 'load_brand_text':
            from apps.listings.loading_views import LOAD_BRANDS as ALL_NAMES
        elif db_field == 'forest_brand_text':
            from apps.listings.forestry_views import FOREST_BRANDS as ALL_NAMES
        elif db_field == 'camp_brand_text':
            from apps.listings.camping_views import CAMP_BRANDS as ALL_NAMES
        elif db_field == 'rent_brand_text':
            # Nuomoje markių sąrašas skiriasi pagal subkategoriją
            # (automobiliai 229, motociklai 514, sunkusis 251...).
            from apps.listings.rental_views import SUB_TO_FORM, brands_for
            ALL_NAMES = brands_for(SUB_TO_FORM.get(sub_slug, 'car'))
        else:
            from apps.listings.trailers_views import TRAILER_BRANDS as ALL_NAMES
        counts = {
            r[db_field]: r['c']
            for r in qs.exclude(**{db_field: ''}).values(db_field).annotate(c=Count('id'))
        }
        names = ALL_NAMES or sorted(counts)
        rows = [{'value': n, 'name': n, 'count': counts.get(n, 0)} for n in names]

    with_ads = sorted((r for r in rows if r['count']),
                      key=lambda r: (-r['count'], r['name'].lower()))
    top = with_ads[:TOP_BRANDS]
    top_vals = {r['value'] for r in top}
    rest = sorted((r for r in rows if r['value'] not in top_vals),
                  key=lambda r: r['name'].lower())
    return top, rest


def _distinct_options(vt_slug, db_field, user=None):
    """Reikšmės, realiai esančios skelbimuose (Miestas) — viena agregacija."""
    from apps.listings.views import _public_listings_qs
    qs = _public_listings_qs(user).filter(vehicle_type__slug=vt_slug)
    rows = (qs.exclude(**{db_field: ''}).exclude(**{db_field: '—'})
              .values(db_field).annotate(c=Count('id')).order_by('-c', db_field))
    return [(r[db_field], f"{r[db_field]} ({r['c']})") for r in rows]


def build_panel(vt_slug, user=None, sub_slug=None):
    """Konfigūracija → šablonui paruoštas panelės aprašas.

    Grąžina None, jei kategorija neaktyvi (tada panelė nerenderinama).
    """
    if not is_active(vt_slug):
        return None

    from apps.listings.models import Listing

    cat = _panel_cfg(vt_slug, sub_slug) or PANELS[vt_slug]
    # ui_order leidžia išlaikyti dabartinę laukų tvarką ten, kur ji
    # skiriasi nuo etalono (trucks/boats: Metai prieš Kainą).
    cat_fields = sorted(cat['fields'], key=lambda f: f.get('ui_order', 0))
    price_min, price_max = _price_tiers()
    years = _years()
    fields = []

    for f in cat_fields:
        if not f.get('active', True):
            continue          # etalone yra, bet mūsų panelėje kol kas nerodom
        db = f['db_field']
        item = {
            'label': _(f['label']),
            'type': f['type'],
            'db_field': db,
            'param': f.get('param'),
            'param_min': f.get('param_min'),
            'param_max': f.get('param_max'),
            'placeholder': _(f['placeholder']) if f.get('placeholder') else '',
        }

        if f['type'] == 'range':
            # own_options: kategorija turi savas pakopas ir bendrosios
            # netinka — nuomos kaina parai prasideda nuo 5, o pardavimo
            # pakopos nuo 500, todėl visas sąrašas būtų bevertis.
            _own_src = f.get('options') or f.get('options_from') or []
            own = [(o, o) for o in _own_src] if f.get('own_options') else None
            if own:
                item['options_min'] = item['options_max'] = own
                item['free_input'] = True
            elif db == 'year':
                item['options_min'] = [(y, y) for y in years]
                item['options_max'] = [(y, y) for y in years]
            elif db == 'price':
                item['options_min'] = price_min
                item['options_max'] = price_max
            else:
                item['options_min'] = item['options_max'] = None  # laisvas įvedimas

        elif f['type'] in ('select', 'multiselect'):
            if db in DISTINCT_VALUE_FIELDS:
                item['options'] = _distinct_options(vt_slug, db, user)
            elif db == 'boat_material':
                from apps.listings.boats_views import BOAT_MATERIAL_CHOICES
                item['options'] = [(v, l) for v, l in BOAT_MATERIAL_CHOICES if v]
            elif db in TEXT_BRAND_FIELDS or db in FK_BRAND_FIELDS:
                item['widget'] = 'brand'
                item['brands_top'], item['brands_rest'] = _brand_rows(
                    vt_slug, db, user, sub_slug)
                item['only_with_ads_toggle'] = bool(f.get('only_with_ads_toggle'))
            elif db in FK_CHOICE_FIELDS:
                item['options'] = _fk_options(db, f.get('options'))
            else:
                attr = CHOICES_BY_DB_FIELD.get(db)
                item['options'] = list(getattr(Listing, attr)) if attr else []
                # Viena kategorija gali rodyti tik dalį bendrų choices —
                # nuomos „Tipas" sec 33 turi 7 reikšmes, sec 34 kitas 6,
                # o modelyje jos laikomos viename sąraše.
                if f.get('limit_to_options') and f.get('options'):
                    _want = {str(o).strip() for o in f['options']}
                    item['options'] = [(v, l) for v, l in item['options']
                                       if str(l) in _want]

        fields.append(item)

    return {
        'slug': vt_slug,
        'label': _(cat['name']),
        'fields': fields,
        'card_fields': cat.get('card_fields', []),
        'has_advanced': advanced_is_active(vt_slug),
    }


def build_advanced(vt_slug, user=None, sub_slug=None):
    """Išplėstinės paieškos aprašas šablonui (arba None, jei neaktyvi)."""
    if not advanced_is_active(vt_slug):
        return None

    from apps.listings.models import Listing

    cat = _advanced_cfg(vt_slug, sub_slug) or ADVANCED[vt_slug]
    price_min, price_max = _price_tiers()
    years = _years()
    fields, equipment, eq_section = [], [], ''

    for f in cat['fields']:
        if not f.get('active', True):
            continue
        db = f['db_field']

        # Ypatumai — atskira suskleidžiama sekcija su skaitikliu
        if db == '__equipment__':
            eq_section = f.get('section') or ''
            equipment.append(f['label'])
            continue

        item = {
            'label': _(f['label']),
            'type': f['type'],
            'db_field': db,
            'param': f.get('param'),
            'param_min': f.get('param_min'),
            'param_max': f.get('param_max'),
            'unit': f.get('unit') or '',
            'free_input': bool(f.get('free_input')),
            'multi': bool(f.get('multi')),
        }

        if f['type'] == 'range':
            _own_src = f.get('options') or f.get('options_from') or []
            own = [(o, o) for o in _own_src] if f.get('own_options') else None
            if own:
                item['options_min'] = item['options_max'] = own
                item['free_input'] = True
            elif db == 'year':
                item['options_min'] = item['options_max'] = [(y, y) for y in years]
            elif db == 'price':
                item['options_min'], item['options_max'] = price_min, price_max
            else:
                opts = [(o, o) for o in (f.get('options') or [])]
                item['options_min'] = item['options_max'] = opts
                item['free_input'] = True     # kg/mm diapazonai — leidžiam bet kokį skaičių
        elif f['type'] in ('select', 'multiselect'):
            if db in TEXT_BRAND_FIELDS or db in FK_BRAND_FIELDS:
                item['widget'] = 'brand'
                item['brands_top'], item['brands_rest'] = _brand_rows(
                    vt_slug, db, user, sub_slug)
                item['only_with_ads_toggle'] = True
            elif db in FK_CHOICE_FIELDS:
                item['options'] = _fk_options(db, f.get('options'))
            elif db in DISTINCT_VALUE_FIELDS:
                item['options'] = _distinct_options(vt_slug, db, user)
            elif db == 'country':
                item['options'] = list(Listing.COUNTRY_CHOICES)
            elif db == 'created_at':
                item['options'] = [(1, _('Vienos dienos')), (3, _('Trijų dienų')),
                                   (7, _('Savaitės')), (14, _('Dviejų savaičių'))]
            elif db == 'seller_type':
                item['options'] = [('private', _('Privatus')), ('business', _('Verslas'))]
            elif db == 'condition':
                item['options'] = [(v, l) for v, l in Listing.CONDITION_CHOICES
                                   if v in ('used', 'new')]
            else:
                attr = CHOICES_BY_DB_FIELD.get(db)
                item['options'] = list(getattr(Listing, attr)) if attr else []
                # Viena kategorija gali rodyti tik dalį bendrų choices —
                # nuomos „Tipas" sec 33 turi 7 reikšmes, sec 34 kitas 6,
                # o modelyje jos laikomos viename sąraše.
                if f.get('limit_to_options') and f.get('options'):
                    _want = {str(o).strip() for o in f['options']}
                    item['options'] = [(v, l) for v, l in item['options']
                                       if str(l) in _want]

        fields.append(item)

    # Ypatumų Equipment eilutės — viena užklausa, be N+1
    from apps.listings.models import Equipment
    eq_qs = Equipment.objects.filter(name__in=equipment)
    prefix = EQUIPMENT_PREFIX.get(vt_slug)
    if prefix:
        eq_qs = eq_qs.filter(category__startswith=prefix)
    eq_rows = {e.name: e for e in eq_qs}
    eq_items = [{'id': eq_rows[n].id, 'name': n} for n in equipment if n in eq_rows]

    return {
        'slug': vt_slug,
        'label': _(cat['name']),
        'fields': fields,
        'equipment': eq_items,
        'equipment_label': eq_section,
        'equipment_total': len(eq_items),
        'sort_options': SORT_OPTIONS,
    }


# ═══════════════════════════════════════════════════════════
# FILTRAVIMAS — vienas variklis, kviečiamas ir listing_list (rezultatai),
# ir filter_listings (AJAX skaičiukas). Projekte tai dvi atskiros filtrų
# šakos; be bendro variklio mygtuko skaičius nesutaptų su sąrašu.
# ═══════════════════════════════════════════════════════════

def _get(params, key):
    if not key:
        return None
    v = params.get(key)
    return v.strip() if isinstance(v, str) else v


def _getlist(params, key):
    if not key:
        return []
    if hasattr(params, 'getlist'):
        return [v for v in params.getlist(key) if v]
    v = params.get(key)
    return [v] if v else []


def owns_text_search(vt_slug):
    """Ar tekstinę paiešką šiai kategorijai tvarko variklis.

    Bendri ?q / ?search filtrai taiko tik pavadinimą; variklis ieško ir
    aprašyme. Susidėję jie duotų tik title atitikmenis, todėl kai variklis
    valdo — bendri praleidžiami (žr. views.filter_listings / listing_list).
    """
    panel = PANELS.get(vt_slug)
    if not is_active(vt_slug) or not panel:
        return False
    return any(f['db_field'] == '__text__' and f.get('active', True)
               for f in panel['fields'])


def apply_panel_filters(listings, vt_slug, params, source='advanced_or_panel', sub_slug=None):
    source = 'panel' if source == 'advanced_or_panel' else source
    """Pritaiko kategorijos filtrus pagal konfigūraciją.

    source='panel'    — greitoji panelė (paneles-config.json)
    source='advanced' — išplėstinė paieška (isplestine-config.json)

    Tušti parametrai nieko nesiaurina; kiekvienas laukas — atskiras
    .filter(), todėl keli filtrai veikia kaip IR.
    """
    if source == 'advanced':
        if not advanced_is_active(vt_slug):
            return listings
        cfg_fields = (_advanced_cfg(vt_slug, sub_slug) or ADVANCED[vt_slug])['fields']
    else:
        if not is_active(vt_slug):
            return listings
        cfg_fields = (_panel_cfg(vt_slug, sub_slug) or PANELS[vt_slug])['fields']

    for f in cfg_fields:
        if not f.get('active', True):
            continue
        db, ftype = f['db_field'], f['type']

        # Ypatumus ir bendrus laukus (šalis/miestas/senumas/pardavėjas)
        # jau tvarko filter_listings — čia jų nekartojam, kad nedubliuotume.
        if db in ('__equipment__', 'country', 'city', 'created_at', 'seller_type'):
            continue

        # Kelios markės vienu metu — reikšmės masyvas
        if f.get('multi'):
            vals = _getlist(params, f.get('param'))
            if vals:
                listings = listings.filter(**{f'{db}__in': vals})
            continue

        if ftype == 'range':
            lo, hi = _get(params, f.get('param_min')), _get(params, f.get('param_max'))
            if lo:
                listings = listings.filter(**{f'{db}__gte': lo})
            if hi:
                listings = listings.filter(**{f'{db}__lte': hi})

        elif ftype == 'text':
            if db == '__text__':
                # ?q, o jei tuščias — legacy ?search, kad senos nuorodos veiktų
                q = _get(params, f.get('param')) or _get(params, 'search')
                if q:
                    listings = listings.filter(
                        Q(title__icontains=q) | Q(description__icontains=q)
                    )
            else:
                # Tekstinis laukas su savo stulpeliu (pvz. Modelis) —
                # icontains TAME lauke, ne bendra paieška pavadinime.
                val = _get(params, f.get('param'))
                if val:
                    listings = listings.filter(**{f'{db}__icontains': val})

        elif ftype == 'multiselect':
            vals = _getlist(params, f.get('param'))
            if vals:
                listings = listings.filter(**{f'{db}__in': vals})

        elif ftype == 'checkbox':
            if _get(params, f.get('param')):
                if db == 'vin':
                    listings = listings.exclude(vin__isnull=True).exclude(vin='')
                elif db == 'country':
                    listings = listings.filter(country='LT')
                else:
                    listings = listings.filter(**{db: True})

        else:  # select
            # Kelios to paties lauko reikšmės (pvz. kelios markės iš
            # išplėstinės paieškos) — OR lauko viduje, kad greitosios
            # panelės vienos reikšmės filtras jų nesusiaurintų iki vienos.
            vals = _getlist(params, f.get('param'))
            if len(vals) > 1:
                listings = listings.filter(**{f'{db}__in': vals})
                continue
            val = _get(params, f.get('param'))
            if val:
                # Miestui — icontains, kaip daro bendrasis filtras; kitaip
                # senos dalinės nuorodos (?city=vil) nustotų veikti.
                lookup = f'{db}__icontains' if db in DISTINCT_VALUE_FIELDS else db
                listings = listings.filter(**{lookup: val})

    return listings
