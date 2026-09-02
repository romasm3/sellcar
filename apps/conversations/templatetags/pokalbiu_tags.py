# -*- coding: utf-8 -*-
"""
Pokalbių sąsajos pagalbininkai.

VIENA VIETA, KUR SPRENDŽIAMA, KOKS VARDAS RODOMAS ŽMOGUI.

El. paštas pokalbiuose nerodomas niekada. Registruojantis
`user.username` prilyginamas el. paštui (accounts/forms.py:33), todėl
`Profile.display_name` atsarginis kelias (`get_full_name() or username`)
grąžina būtent adresą — jį atpažįstam iš „@" ir atmetam.
"""
from django import template
from django.utils.translation import gettext as _

register = template.Library()


def _svarus(reiksme):
    """Vardas be el. pašto. Tuščia, jei tai adresas."""
    v = str(reiksme or '').strip()
    return '' if (not v or '@' in v) else v


@register.filter
def vardas(user):
    """Kaip vadinti žmogų pokalbyje. NIEKADA ne el. paštas.

    Eilės tvarka: Profile.display_name (įmonė arba vardas ir pavardė) →
    vardas ir pavardė → „Naudotojas #42".
    """
    if not user or not getattr(user, 'pk', None):
        return _('Naudotojas')
    profilis = getattr(user, 'profile', None)
    v = _svarus(getattr(profilis, 'display_name', '')) if profilis else ''
    if not v:
        v = _svarus(user.get_full_name())
    return v or '%s #%s' % (_('Naudotojas'), user.pk)


@register.filter
def vardo_raide(user):
    """Avataro raidė — iš to paties vardo, ne iš el. pašto."""
    v = vardas(user)
    return (v[:1] or '?').upper()


@register.filter
def dienos_zyma(data):
    """Datos skirtukas žinučių sraute: „Šiandien", „Vakar", „rugsėjo 2"."""
    if not data:
        return ''
    from django.utils import timezone
    from django.utils.formats import date_format
    vietine = timezone.localtime(data) if timezone.is_aware(data) else data
    siandien = timezone.localdate()
    diena = vietine.date()
    if diena == siandien:
        return _('Šiandien')
    if (siandien - diena).days == 1:
        return _('Vakar')
    return date_format(vietine, 'j E')
