# -*- coding: utf-8 -*-
"""
PADANGŲ IR RATLANKIŲ SĄRAŠAI ŠABLONAMS — IŠ TO PATIES ŠALTINIO.

Kūrimo formos sąrašus gaudavo iš vaizdo konteksto (wheels_views.py), o
paieškos panelė — `templates/listings/partials/_panel_bodies.html` — turėjo
savo, ranka surašytus. Dėl to filtre buvo R4–R63, o formoje tik R10–R24:
filtruoti buvo galima pagal reikšmes, kurių įvesti neįmanoma.

Blogiau — panelė naudojo ir KITAS reikšmes: „car", „van", „agro", „quad"
vietoj passenger/commercial/industrial/atv. Toks filtras nerasdavo nieko,
nes skelbimuose įrašyta kita reikšmė.

Panelė įtraukiama visuose puslapiuose, tad konteksto kintamųjų jai
paduoti negalim — sąrašus ji pasiima per šias žymas:

    {% load ratu_tags %}
    {% ratu_sarasas 'diameter' as skersmenys %}
    {% for val, label in skersmenys %}…{% endfor %}

Vienintelis sąrašų šaltinis lieka apps/listings/models.py.
"""
from django import template

from apps.listings import models

register = template.Library()

SARASAI = {
    'purpose': 'WHEEL_PURPOSE_CHOICES',
    'diameter': 'WHEEL_DIAMETER_CHOICES',
    'condition': 'WHEEL_CONDITION_CHOICES',
    'tyre_width': 'TYRE_WIDTH_CHOICES',
    'tyre_profile': 'TYRE_PROFILE_CHOICES',
    'tyre_season': 'TYRE_SEASON_CHOICES',
    'tyre_speed': 'TYRE_SPEED_CHOICES',
    'tyre_tread': 'TYRE_TREAD_CHOICES',
    'tyre_remaining': 'TYRE_REMAINING_CHOICES',
    'tyre_dot_year': 'TYRE_DOT_YEAR_CHOICES',
    'rim_width': 'RIM_WIDTH_CHOICES',
    'rim_pcd': 'RIM_PCD_CHOICES',
    'rim_bolt_count': 'RIM_BOLT_COUNT_CHOICES',
    'rim_material': 'RIM_MATERIAL_CHOICES',
}


@register.simple_tag
def ratu_sarasas(vardas):
    """(reikšmė, pavadinimas) poros. Nežinomas vardas — tuščias sąrašas."""
    konstanta = SARASAI.get(vardas)
    if not konstanta:
        return []
    return list(getattr(models, konstanta, []))
