# apps/listings/templatetags/i18n_db.py
# ═══════════════════════════════════════════════════════════
# DB reikšmių (VehicleType.name, SubCategory.name) vertimas.
#
# Pavadinimai gyvena DB, tad {% trans %} jų nepasiekia. Msgid'ai
# surenkami per translatable_db.py, o čia jie išverčiami rodymo metu.
#
#   {{ vt.name|tdb }}
# ═══════════════════════════════════════════════════════════

from django import template
from django.utils.translation import gettext

register = template.Library()


@register.filter(name='tdb')
def translate_db_value(value):
    """Išverčia DB tekstą, jei toks msgid yra kataloge; kitaip grąžina originalą."""
    if not value:
        return value
    return gettext(str(value))
