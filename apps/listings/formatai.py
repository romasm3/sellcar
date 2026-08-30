# -*- coding: utf-8 -*-
"""
Skaičių ir kainų formatas — VIENA vieta visam projektui.

Lietuviškai tūkstančiai skiriami tarpu, o valiutos simbolis rašomas
gale: „5 000 €", „15 000 km". Tarpai nedalomi ( ), kad skaičius
nelūžtų per dvi eilutes.

Šablonuose tas pats per filtrus: {{ listing.price|kaina:listing.currency_symbol }}
ir {{ listing.mileage|sk }} (apps/listings/templatetags/listing_filters.py).
Python kode (laiškai, pranešimai) — kaina(...) / sk(...) tiesiogiai.
"""

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from django.utils.translation import get_language

NEDALOMAS = '\u00a0'

# Kalbos formatas: (tūkstančių skirtukas, ar simbolis prieš skaičių).
# Django lt lokalė tūkstančius skirtų tašku („5.000") — mums reikia nedalomo
# tarpo, todėl skirtuką nurodom patys, o ne imam iš formats.py.
FORMATAI = {
    'en': (',', True),        # €5,000
}
NUMATYTAS = (NEDALOMAS, False)   # lt: 5 000 €


def _formatas():
    return FORMATAI.get((get_language() or 'lt')[:2], NUMATYTAS)


def sveikas(reiksme):
    """Reikšmė -> suapvalintas sveikas skaičius arba None."""
    if reiksme is None or reiksme == '':
        return None
    try:
        return int(Decimal(str(reiksme)).quantize(Decimal('1'), rounding=ROUND_HALF_UP))
    except (InvalidOperation, ValueError, TypeError):
        return None


def sk(reiksme):
    """15000 -> lt „15 000", en „15,000". Neatpažintą reikšmę grąžina nepakeistą."""
    n = sveikas(reiksme)
    if n is None:
        return reiksme if reiksme is not None else ''
    return '{:,}'.format(n).replace(',', _formatas()[0])


def kaina(reiksme, simbolis='€'):
    """5000 -> lt „5 000 €" (simbolis gale), en „€5,000" (simbolis priekyje)."""
    n = sveikas(reiksme)
    if n is None:
        return ''
    simbolis = simbolis or '€'
    priekyje = _formatas()[1]
    return '%s%s' % (simbolis, sk(n)) if priekyje else '%s%s%s' % (sk(n), NEDALOMAS, simbolis)
