# -*- coding: utf-8 -*-
"""
Paieškos diapazonų (nuo–iki) susiejimas su matavimo vienetų perjungikliais.

Deklaratyvioje paieškos konfigūracijoje laukai vadinasi `mileage_min`,
`gross_weight_max` ir pan., o static/js/unit_toggle.js specifikacijos
sudėtos pagal MODELIO lauko vardą. Šis filtras juos sujungia, kad
_range.html galėtų vienoje vietoje pažymėti visus kategorijų laukus.

Ko čia SĄMONINGAI nėra: `battery` (Ah), `charge` (val.), `engine_hours`,
`incline` (°), `power_w` (W), `price`, `seats`, `wheel` (coliai jau yra
pramonės standartas) ir `year` — jiems imperinio atitikmens nėra arba
jis beprasmis.
"""
from django import template

register = template.Library()

# diapazono parametro šaknis -> unit_toggle.js SPECS raktas
RANGE_UNIT_SPECS = {
    'mileage':      'mileage',
    'power':        'power',
    'engine':       'engine_capacity',
    'engine_cc':    'engine_capacity_cc',
    'curb_weight':  'curb_weight',
    'weight':       'curb_weight',
    'gross_weight': 'gross_weight_kg',
    'payload':      'payload_kg',
    'length_m':     'length_m',
    'width_m':      'width_m',
    'height_m':     'height_m',
    'lift_height':  'lift_height_m',
    'range':        'range_km',
    'speed':        'max_speed_kmh',
    'length':       'truck_length_mm',   # etalone „Ilgis (mm)" priekaboms
}


@register.filter
def unit_spec(param):
    """'mileage_min' -> 'mileage'; nežinomam laukui — tuščia eilutė."""
    if not param:
        return ''
    name = str(param)
    for suffix in ('_min', '_max'):
        if name.endswith(suffix):
            name = name[:-len(suffix)]
            break
    return RANGE_UNIT_SPECS.get(name, '')
