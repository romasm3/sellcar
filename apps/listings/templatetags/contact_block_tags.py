# apps/listings/templatetags/contact_block_tags.py
# ═══════════════════════════════════════════════════════════
# Choice lists for the shared contact block.
#
# Views used to build these themselves, and the copies had drifted —
# car-for-parts and truck-for-parts offered only the United States, and
# motorcycles offered the full list or only the US depending on a branch.
# The contact block reads them from here instead, so no view can narrow
# the list by accident.
# ═══════════════════════════════════════════════════════════

from django import template

from .. import salys
from ..models import Listing

register = template.Library()


@register.simple_tag
def contact_country_choices():
    """Visos salys plokscia eile - is apps/listings/salys.py."""
    return salys.plokscias()


@register.simple_tag
def contact_country_groups():
    """Tos pacios salys grupemis - <optgroup> skirtukams."""
    return [{'vardas': g, 'poros': p} for g, p in salys.GRUPES]


@register.simple_tag
def contact_state_groups():
    """Valstijos, sugrupuotos pagal salj."""
    return [{'vardas': g, 'poros': p} for g, p in salys.visos_valstijos()]


@register.simple_tag
def contact_numatyta_salis():
    """Numatytoji salis - Lietuva (svetaine lietuviska)."""
    return salys.NUMATYTA


@register.simple_tag
def contact_state_choices(salis=None):
    """Valstijos. Be salies - visos, sugrupuotos pagal salj.

    Laukas "Valstija" prasmingas tik toms salims, kurios jas turi
    (salys.VALSTIJOS). Kitoms jis slepiamas, ne paliekamas tuscias.
    """
    if salis:
        return salys.valstijos(salis)
    return salys.visos_valstijos()


@register.simple_tag
def contact_valstiju_salys():
    """Saliu kodai, kuriems rodomas laukas "Valstija" - juos skaito JS."""
    return ','.join(salys.valstiju_salys())
