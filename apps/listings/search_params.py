# apps/listings/search_params.py
# ═══════════════════════════════════════════════════════════
# NETINKAMOS PAIEŠKOS REIKŠMĖS — tylus ignoravimas.
#
# `?year_min=abc` ar `?brand=Volkswagen` anksčiau griaudavo puslapį
# (ValueError: Field 'id' expected a number). Užtekdavo boto, seno
# bookmark'o ar ranka pataisyto URL.
#
# Sprendžiam vienoje vietoje: prieš filtruojant iš GET išmetam tas
# reikšmes, kurių atitinkamas DB stulpelis priimti negali. Laukų
# sąrašas NERAŠOMAS ranka — jis išvedamas iš modelių laukų tipų ir iš
# paieškos konfigūracijų, todėl naujas skaitinis laukas apsaugą gauna
# automatiškai.
# ═══════════════════════════════════════════════════════════
from django.db import models

_NUMERIC_FIELD_TYPES = (
    models.ForeignKey, models.OneToOneField,
    models.IntegerField, models.BigIntegerField, models.SmallIntegerField,
    models.PositiveIntegerField, models.PositiveSmallIntegerField,
    models.PositiveBigIntegerField, models.AutoField, models.BigAutoField,
    models.DecimalField, models.FloatField,
)

# Diapazonų galūnės — jos visada skaitinės, nesvarbu koks stulpelis.
_RANGE_SUFFIXES = ('_min', '_max', '_from', '_to')

# Rankomis darytų panelių parametrai, kurių konfigūracijoje nėra.
_EXTRA_INT_PARAMS = {
    'brand', 'model', 'fuel_type', 'transmission', 'truck_brand',
    'motorcycle_brand', 'motorcycle_model', 'gear_brand', 'equipment',
    'part_types', 'part_category', 'page', 'seller',
}

_CACHE = {}


def _numeric_model_fields():
    """Listing ir WheelListing stulpeliai, kurie priima tik skaičius."""
    from apps.listings.models import Listing, WheelListing

    names = set()
    for model in (Listing, WheelListing):
        for field in model._meta.get_fields():
            if isinstance(field, _NUMERIC_FIELD_TYPES):
                names.add(field.name)
                if getattr(field, 'is_relation', False):
                    names.add(f'{field.name}_id')
    return names


def numeric_params():
    """Visi GET parametrai, kurių reikšmė privalo būti skaičius."""
    if 'params' in _CACHE:
        return _CACHE['params']

    from apps.listings.search_config import panels as P

    numeric_fields = _numeric_model_fields()
    params = set(_EXTRA_INT_PARAMS)

    configs = []
    configs.extend(P.PANELS.values())
    configs.extend(P.PANELS_BY_SUB.values())
    configs.extend(P.ADVANCED.values())
    configs.extend(P.ADVANCED_BY_SUB.values())

    for cfg in configs:
        for f in cfg.get('fields', []):
            if f.get('type') == 'range':
                for key in ('param_min', 'param_max'):
                    if f.get(key):
                        params.add(f[key])
                continue
            param, db = f.get('param'), f.get('db_field')
            if param and db and db in numeric_fields:
                params.add(param)

    _CACHE['params'] = params
    return params


def _is_number(value):
    try:
        float(str(value).replace(',', '.'))
    except (TypeError, ValueError):
        return False
    return True


def is_numeric_param(name):
    return name.endswith(_RANGE_SUFFIXES) or name in numeric_params()


def sanitize(get_params):
    """GET kopija be reikšmių, kurių DB priimti negali.

    Tušti ir tvarkingi parametrai lieka nepaliesti; sugadinti tyliai
    dingsta, tarsi jų nebūtų — puslapis atsidaro, filtras tiesiog
    nepritaikomas.
    """
    bad = [
        (key, value)
        for key in get_params
        if is_numeric_param(key)
        for value in get_params.getlist(key)
        if value not in ('', None) and not _is_number(value)
    ]
    if not bad:
        return get_params

    cleaned = get_params.copy()
    for key, _value in bad:
        good = [v for v in cleaned.getlist(key) if v == '' or _is_number(v)]
        if good:
            cleaned.setlist(key, good)
        else:
            del cleaned[key]
    cleaned._mutable = False
    return cleaned
