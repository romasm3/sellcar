# -*- coding: utf-8 -*-
"""
ŠALIS → VALIUTA. VIENA VIETA VISAI SVETAINEI.

Žemėlapio nebuvo VISAI. Įkėlimo formos valiutą siųsdavo paslėptu lauku
su įrašyta reikšme „USD" (trucks_listing_create.html, cars quick ir
kt.), todėl vokiškas #749 ir kroatiškas #754 rodė „$", nors kaina
įvesta eurais. Lietuviškas #727 rodė „€" tik todėl, kad modelio
numatytoji reikšmė yra EUR.

Rinka — Europa, tad nežinomai šaliai atsarginė valiuta irgi EUR, ne USD.

Naudojimas:

    from apps.listings import valiutos
    listing.currency = valiutos.pagal_sali(listing.country)
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
    """Šalies kodas (LT, DE, HR…) → valiutos kodas. Nežinoma → EUR."""
    kodas = (salies_kodas or '').strip().upper()
    if kodas in EURO_ZONA:
        return 'EUR'
    return KITOS.get(kodas, NUMATYTA)


def simbolis(valiutos_kodas):
    """Valiutos kodas → simbolis. Nežinomas → €."""
    return SIMBOLIAI.get((valiutos_kodas or '').strip().upper(),
                         SIMBOLIAI[NUMATYTA])


def simbolis_pagal_sali(salies_kodas):
    return simbolis(pagal_sali(salies_kodas))


def zemelapis():
    """Visas žemėlapis {šalis: valiuta} — patikroms ir ataskaitoms."""
    visos = {kodas: 'EUR' for kodas in EURO_ZONA}
    visos.update(KITOS)
    return visos
