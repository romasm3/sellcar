# -*- coding: utf-8 -*-
"""
VALIUTA — VIENA VISAI SVETAINEI: EUR.

DAUGIAVALIUTĖS KOL KAS NEDAROM. Sąsaja „šalis → valiuta" pašalinta:
`pagal_sali()` bet kuriai šaliai grąžina EUR, tad ir sufiksas formoje,
ir įrašomas `Listing.currency` visada eurai.

Kas buvo. Sąsaja žymę keitė, o SUMOS nekonvertavo: pasirinkus Lenkiją
43 000 € virsdavo „43 000 zł" (≈10 000 €). Taip nukentėjo #789 Dodge RAM,
#791 Lamborghini Urus, #798 Audi S5, #792 ir #799. Kursų svetainė neturi,
tad vienintelis teisingas elgesys — nekeisti nieko.

Žemiau paliktos EURO_ZONA ir KITOS lentelės: jos NIEKUR nebenaudojamos,
bet pravers, kai GBP/USD bus daromi atskirai (tada kartu reikės ir kursų,
ir sumų perskaičiavimo — be jų žymės keisti negalima).

Žemėlapio nebuvo VISAI. Įkėlimo formos valiutą siųsdavo paslėptu lauku
su įrašyta reikšme „USD" (trucks_listing_create.html, cars quick ir
kt.), todėl vokiškas #749 ir kroatiškas #754 rodė „$", nors kaina
įvesta eurais. Lietuviškas #727 rodė „€" tik todėl, kad modelio
numatytoji reikšmė yra EUR.

Rinka — Europa, tad ir numatytoji, ir vienintelė valiuta yra EUR.

Naudojimas:

    from apps.listings import valiutos
    listing.currency = valiutos.NUMATYTA
    simbolis = valiutos.simbolis(listing.currency)

Šablonuose — per `valiutos_tags`:

    {% load valiutos_tags %}
    {% valiutos_simbolis listing.country as sufiksas %}
"""

# Euro zona (2026). Kroatija — nuo 2023, todėl #754 turi būti €.
EURO_ZONA = (
    'AT', 'BE', 'HR', 'CY', 'EE', 'FI', 'FR', 'DE', 'GR', 'IE', 'IT',
    'LV', 'LT', 'LU', 'MT', 'NL', 'PT', 'SK', 'SI', 'ES',
)

# Kitos Europos šalys ir JAV. Ko čia nėra — gauna EUR.
KITOS = {
    'GB': 'GBP', 'PL': 'PLN', 'CZ': 'CZK', 'DK': 'DKK',
    'SE': 'SEK', 'NO': 'NOK', 'CH': 'CHF', 'US': 'USD',
}

NUMATYTA = 'EUR'

SIMBOLIAI = {
    'EUR': '€', 'USD': '$', 'GBP': '£', 'PLN': 'zł',
    'CZK': 'Kč', 'DKK': 'kr', 'SEK': 'kr', 'NOK': 'kr', 'CHF': 'CHF',
}


def pagal_sali(salies_kodas):
    """Bet kuri šalis → EUR.

    Argumentas lieka, kad kviečiantys vaizdai ir šablonų žymos
    nesikeistų, bet reikšmės nebežiūrim: kol nėra kursų, žymės keitimas
    tik meluoja apie kainą.
    """
    return NUMATYTA


def simbolis(valiutos_kodas):
    """Valiutos kodas → simbolis. Nežinomas → €."""
    return SIMBOLIAI.get((valiutos_kodas or '').strip().upper(),
                         SIMBOLIAI[NUMATYTA])


def simbolis_pagal_sali(salies_kodas):
    return simbolis(pagal_sali(salies_kodas))


def zemelapis():
    """Visas žemėlapis {šalis: valiuta} — naršyklei ir patikroms.

    Visoms šalims EUR, todėl static/js/valiuta.js pakeitus šalį sufikso
    nebekeičia.
    """
    return {kodas: NUMATYTA for kodas in tuple(EURO_ZONA) + tuple(KITOS)}
