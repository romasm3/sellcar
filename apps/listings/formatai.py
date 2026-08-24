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

NEDALOMAS = ' '


def sveikas(reiksme):
    """Reikšmė -> suapvalintas sveikas skaičius arba None."""
    if reiksme is None or reiksme == '':
        return None
    try:
        return int(Decimal(str(reiksme)).quantize(Decimal('1'), rounding=ROUND_HALF_UP))
    except (InvalidOperation, ValueError, TypeError):
        return None


def sk(reiksme):
    """15000 -> „15 000". Neatpažintą reikšmę grąžina nepakeistą."""
    n = sveikas(reiksme)
    if n is None:
        return reiksme if reiksme is not None else ''
    return '{:,}'.format(n).replace(',', NEDALOMAS)


def kaina(reiksme, simbolis='€'):
    """5000 -> „5 000 €" (simbolis gale, tarpas prieš jį)."""
    n = sveikas(reiksme)
    if n is None:
        return ''
    return '%s%s%s' % (sk(n), NEDALOMAS, simbolis or '€')
