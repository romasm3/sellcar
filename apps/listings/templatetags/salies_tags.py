# -*- coding: utf-8 -*-
"""
ŠALIES ŽYMĖS šablonams — vardas ir vėliavos buvimas.

Vardas VIETOS eilutėje („Vilnius, Lietuva") yra pilnas ir IŠVERSTAS —
tai tekstas žmogui, skaitančiam puslapį savo kalba. Nepainioti su šalies
juosta virš paieškos panelės: ten sąrašas tarptautinis, todėl vardai
angliški ir neverčiami (salys.VARDAI_EN).
"""
import os

from django import template

from apps.listings import salys

register = template.Library()

# Kelias skaičiuojamas nuo paties failo, ne nuo settings.BASE_DIR:
# testai konfigūruoja Django be jo, o šablonų kompiliavimas krito.
_VELIAVU_KATALOGAS = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))))),
    'static', 'flags')
_TURIMOS = None


@register.filter
def salies_vardas(kodas):
    """'LT' → „Lietuva" (išversta). Nežinomam kodui — pats kodas."""
    return salys.vardas(str(kodas or '').upper())


@register.filter
def salies_vardas_en(kodas):
    """'LT' → „Lithuania" — angliškas ir NEVERČIAMAS.

    Kortelės vietos eilutėje ir šalies sąrašuose vardas visur vienodas,
    nepriklausomai nuo sąsajos kalbos: sąrašas tarptautinis, jį skaito ir
    tas, kuris svetainės kalbos nemoka.
    """
    return salys.vardas_en(kodas)


@register.filter
def veliava_yra(zemas_kodas):
    """Ar turim tokį SVG. Sąrašas nuskaitomas kartą, ne po failą kaskart."""
    global _TURIMOS
    if _TURIMOS is None:
        try:
            _TURIMOS = {f[:-4].lower() for f in os.listdir(_VELIAVU_KATALOGAS)
                        if f.endswith('.svg')}
        except OSError:
            _TURIMOS = set()
    return str(zemas_kodas or '').lower() in _TURIMOS
