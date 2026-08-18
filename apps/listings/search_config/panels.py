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

# Kategorijos, kurių paiešką aptarnauja Listing + listing_list.
# tires/wheels sukasi apie WheelListing, o parts/motogear tab'ai turi savo
# browse view'us — jiems šis variklis netinka be daug didesnio refaktoringo.
LISTING_BACKED = {'cars', 'motorcycles', 'trucks', 'boats', 'trailers'}

# 1 ETAPAS: markė→modelis AJAX kaskados variklis dar nepalaiko, todėl
# cars/motorcycles kol kas lieka su savo blokais search_panel.html.
# Įtraukus kaskadą — pridėk juos čia.
ENGINE_ENABLED = {'trucks', 'boats', 'trailers'}

# db_field → iš kur imti reikšmių sąrašą (choices). Etiketės mūsų modelyje
# jau sutampa su etalonu 1:1 (Tipas 2/2, Paskirtis 22/22), todėl JSON
# `options` lieka dokumentacija, o reikšmės imamos iš modelio.
CHOICES_BY_DB_FIELD = {
    'trailer_kind':    'TRAILER_KIND_CHOICES',
    'trailer_purpose': 'TRAILER_PURPOSE_CHOICES',
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
TEXT_BRAND_FIELDS = {'trailer_brand_text'}

TOP_BRANDS = 10

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
for _cat in _RAW['categories']:
    _vt = _cat.get('vt_slug')
    if _vt and _vt not in PANELS:
        PANELS[_vt] = _cat


def is_active(vt_slug):
    """Ar kategorija turi veikiančią deklaratyvią panelę."""
    cat = PANELS.get(vt_slug)
    if not cat or vt_slug not in LISTING_BACKED or vt_slug not in ENGINE_ENABLED:
        return False
    return all(f.get('db_field') for f in cat['fields'])


def active_categories():
    return sorted(s for s in PANELS if is_active(s))


def _price_tiers():
    fmt = lambda v: f'{v:,}'.replace(',', ' ')
    return ([(v, fmt(v)) for v in PRICE_MIN_TIERS],
            [(v, fmt(v)) for v in PRICE_MAX_TIERS])


def _years():
    return list(range(timezone.now().year, 1984, -1)) + YEAR_TAIL


def _brand_rows(vt_slug, db_field, user=None):
    """Markės su skelbimų kiekiais — VIENA agregacija, be N+1."""
    from apps.listings.views import _public_listings_qs
    from apps.listings.trailers_views import TRAILER_BRANDS

    qs = _public_listings_qs(user).filter(vehicle_type__slug=vt_slug)
    counts = {
        r[db_field]: r['c']
        for r in qs.exclude(**{db_field: ''}).values(db_field).annotate(c=Count('id'))
    }
    all_names = TRAILER_BRANDS if db_field == 'trailer_brand_text' else sorted(counts)
    with_ads = sorted((n for n in all_names if counts.get(n)),
                      key=lambda n: (-counts[n], n.lower()))
    top = with_ads[:TOP_BRANDS]
    rest = sorted((n for n in all_names if n not in top), key=lambda n: n.lower())
    return ([{'name': n, 'count': counts.get(n, 0)} for n in top],
            [{'name': n, 'count': counts.get(n, 0)} for n in rest])


def build_panel(vt_slug, user=None):
    """Konfigūracija → šablonui paruoštas panelės aprašas.

    Grąžina None, jei kategorija neaktyvi (tada panelė nerenderinama).
    """
    if not is_active(vt_slug):
        return None

    from apps.listings.models import Listing

    cat = PANELS[vt_slug]
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
            if db == 'year':
                item['options_min'] = [(y, y) for y in years]
                item['options_max'] = [(y, y) for y in years]
            elif db == 'price':
                item['options_min'] = price_min
                item['options_max'] = price_max
            else:
                item['options_min'] = item['options_max'] = None  # laisvas įvedimas

        elif f['type'] in ('select', 'multiselect'):
            if db in TEXT_BRAND_FIELDS:
                item['widget'] = 'brand'
                item['brands_top'], item['brands_rest'] = _brand_rows(vt_slug, db, user)
                item['only_with_ads_toggle'] = bool(f.get('only_with_ads_toggle'))
            else:
                attr = CHOICES_BY_DB_FIELD.get(db)
                item['options'] = list(getattr(Listing, attr)) if attr else []

        fields.append(item)

    return {
        'slug': vt_slug,
        'label': _(cat['name']),
        'fields': fields,
        'card_fields': cat.get('card_fields', []),
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


def apply_panel_filters(listings, vt_slug, params):
    """Pritaiko kategorijos filtrus pagal konfigūraciją.

    Tušti parametrai nieko nesiaurina; kiekvienas laukas — atskiras
    .filter(), todėl keli filtrai veikia kaip IR.
    """
    if not is_active(vt_slug):
        return listings

    for f in PANELS[vt_slug]['fields']:
        if not f.get('active', True):
            continue
        db, ftype = f['db_field'], f['type']

        if ftype == 'range':
            lo, hi = _get(params, f.get('param_min')), _get(params, f.get('param_max'))
            if lo:
                listings = listings.filter(**{f'{db}__gte': lo})
            if hi:
                listings = listings.filter(**{f'{db}__lte': hi})

        elif ftype == 'text':
            q = _get(params, f.get('param'))
            if q:
                listings = listings.filter(
                    Q(title__icontains=q) | Q(description__icontains=q)
                )

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
            val = _get(params, f.get('param'))
            if val:
                listings = listings.filter(**{db: val})

    return listings
