# -*- coding: utf-8 -*-
"""
GEOKODAVIMAS — adreso siūlymai ir atvirkštinis geokodavimas.

Tiekėjai (OpenStreetMap duomenys, todėl koordinates saugoti galima —
Google ir Mapbox „temporary" to neleidžia):

  • Photon (photon.komoot.io) — siūlymai rašant (search-as-you-type);
  • Nominatim (nominatim.openstreetmap.org) — atvirkštinis geokodavimas
    ir miestų centrai.

Nominatim taisyklės griežtos (1 užklausa/sek., programiniai srautai
atgrasomi), todėl:
  • atvirkštinis geokodavimas kviečiamas TIK paleidus žymeklį;
  • atsakymai kešuojami serveryje 30 parų;
  • siunčiam User-Agent su domenu ir el. paštu, kaip jie prašo.

Nepavykus užklausai grąžinam tuščią rezultatą — forma turi veikti ir be
siūlymų (žmogus įrašo adresą ranka ir pats pasistato žymeklį).

Tiekėją keičiam vienoje vietoje: GEO_TIEKEJAS.
"""

import hashlib
import json
import logging
import threading
import time
import unicodedata
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

GEO_TIEKEJAS = getattr(settings, 'GEO_TIEKEJAS', 'photon')

PHOTON_URL = 'https://photon.komoot.io/api/'
NOMINATIM_REVERSE = 'https://nominatim.openstreetmap.org/reverse'
NOMINATIM_SEARCH = 'https://nominatim.openstreetmap.org/search'

# Kaip prašo OSM taisyklės: aiškus programos vardas ir kontaktas
USER_AGENT = 'AutoLeft/1.0 (https://autoleft.com; helpautoinfo@gmail.com)'

KESO_TRUKME = 60 * 60 * 24 * 30        # 30 parų
LAUKIMAS = 4                            # sekundės

# Photon moka tik kelias kalbas; kitoms siunčiam „default" (vietiniai
# pavadinimai) — kitaip jis grąžina 400.
PHOTON_KALBOS = {'de', 'en', 'fr', 'it'}


def _raktas(*dalys):
    """Saugus kešo raktas (be tarpų ir dvitaškių)."""
    tekstas = '|'.join(str(d) for d in dalys)
    return 'geo_' + hashlib.md5(tekstas.encode('utf-8')).hexdigest()


def _uzklausa(url, parametrai):
    """GET su mūsų User-Agent; klaida — ne išimtis, o None."""
    adresas = url + '?' + urlencode(parametrai)
    try:
        req = Request(adresas, headers={'User-Agent': USER_AGENT,
                                        'Accept': 'application/json'})
        with urlopen(req, timeout=LAUKIMAS) as atsakymas:
            return json.loads(atsakymas.read().decode('utf-8'))
    except (URLError, HTTPError, ValueError, TimeoutError) as e:
        logger.warning('[geo] nepavyko %s: %s', url, e)
        return None


def _kesas(raktas, gauk):
    reiksme = cache.get(raktas)
    if reiksme is not None:
        return reiksme
    reiksme = gauk()
    if reiksme is not None:
        cache.set(raktas, reiksme, KESO_TRUKME)
    return reiksme


def _photon_irasas(f):
    """Photon GeoJSON -> mūsų žodynas."""
    s = f.get('properties', {})
    koord = (f.get('geometry') or {}).get('coordinates') or [None, None]
    dalys = [s.get('name')]
    if s.get('housenumber') and s.get('street'):
        dalys = ['%s %s' % (s['street'], s['housenumber'])]
    elif s.get('street'):
        dalys = [s['street']]
    vardas = ', '.join(x for x in (dalys[0], s.get('city') or s.get('county'),
                                   s.get('country')) if x)
    return {
        'tekstas': vardas,
        # `vardas` ir `tipas` reikalingi antraštės vietos laukui: miestui
        # Photon dažnai neužpildo `city`, tada `miestas` nukrenta iki
        # savivaldybės („Kauno miesto savivaldybė"), o žmogus rinkosi
        # „Kaunas". Adresui atvirkščiai — reikia būtent miesto.
        'vardas': s.get('name') or '',
        'tipas': s.get('type') or s.get('osm_value') or '',
        'lat': koord[1],
        'lon': koord[0],
        'miestas': s.get('city') or s.get('town') or s.get('village')
                   or s.get('county') or '',
        'salis': s.get('country') or '',
        'salies_kodas': (s.get('countrycode') or '').upper(),
    }


def siulymai(uzklausa, kalba='lt', kiek=6, salis=''):
    """Adresų siūlymai rašant. Tuščias sąrašas = tyliai be siūlymų.

    `salis` (pvz. „LT") palieka tik tos šalies rezultatus. Photon šalies
    filtro neturi, todėl imam su atsarga ir atsijojam čia.
    """
    uzklausa = (uzklausa or '').strip()
    if len(uzklausa) < 3:
        return []
    salis = (salis or '').upper()
    raktas = _raktas('siul', GEO_TIEKEJAS, kalba, salis, kiek, uzklausa.lower())

    def gauk():
        if GEO_TIEKEJAS != 'photon':
            return []
        photon_kalba = kalba if kalba in PHOTON_KALBOS else 'default'
        duom = _uzklausa(PHOTON_URL, {'q': uzklausa,
                                      'limit': kiek * 3 if salis else kiek,
                                      'lang': photon_kalba})
        if not duom:
            return []
        eil = [_photon_irasas(f) for f in duom.get('features', [])]
        if salis:
            eil = [e for e in eil if e.get('salies_kodas') == salis]
        return eil[:kiek]

    return _kesas(raktas, gauk) or []


def atvirkstinis(lat, lon, kalba='lt'):
    """Koordinatės -> adresas (kviečiama TIK paleidus žymeklį)."""
    try:
        lat, lon = round(float(lat), 5), round(float(lon), 5)
    except (TypeError, ValueError):
        return None
    raktas = _raktas('atv', lat, lon, kalba)

    def gauk():
        duom = _uzklausa(NOMINATIM_REVERSE, {
            'lat': lat, 'lon': lon, 'format': 'jsonv2',
            'accept-language': kalba, 'zoom': 18,
        })
        if not duom or 'address' not in duom:
            return None
        a = duom['address']
        gatve = a.get('road') or a.get('pedestrian') or ''
        numeris = a.get('house_number') or ''
        miestas = (a.get('city') or a.get('town') or a.get('village')
                   or a.get('municipality') or '')
        return {
            'tekstas': duom.get('display_name', ''),
            'gatve': (' '.join(x for x in (gatve, numeris) if x)).strip(),
            'miestas': miestas,
            'salis': a.get('country', ''),
            'salies_kodas': (a.get('country_code') or '').upper(),
            'pasto_kodas': a.get('postcode', ''),
        }

    return _kesas(raktas, gauk)


def miesto_centras(miestas, salis=''):
    """Miesto centro koordinatės — seniems skelbimams, kurie turi tik miestą.

    Vienas miestas geokoduojamas vieną kartą (kešas 30 parų), todėl net
    ir su tūkstančiais skelbimų užklausų būna vienetai.
    """
    miestas = (miestas or '').strip()
    if not miestas:
        return None
    raktas = _raktas('centras', miestas.lower(), (salis or '').lower())

    def gauk():
        duom = _uzklausa(NOMINATIM_SEARCH, {
            'q': ', '.join(x for x in (miestas, salis) if x),
            'format': 'jsonv2', 'limit': 1,
        })
        if not duom:
            return None
        p = duom[0]
        return {'lat': float(p['lat']), 'lon': float(p['lon'])}

    return _kesas(raktas, gauk)


# ═══════════════════════════════════════════════════════════════════
# AJAX GALAI — naršyklė į OSM tiesiogiai nesikreipia
#
# Taip mes valdom User-Agent, kešą ir dažnį (OSM to ir prašo), o raktų
# ar tiekėjo vardo puslapyje nėra: prireikus keičiam GEO_TIEKEJAS ir
# priekinė dalis nieko nežino.
# ═══════════════════════════════════════════════════════════════════

def _kalba(request):
    from django.utils.translation import get_language
    return (get_language() or 'lt').split('-')[0]


def ajax_siulymai(request):
    """/ajax/adresai/?q=… — adresų siūlymai rašant."""
    from django.http import JsonResponse
    try:
        kiek = min(int(request.GET.get('kiek') or 6), 10)
    except ValueError:
        kiek = 6
    return JsonResponse({'siulymai': siulymai(request.GET.get('q', ''),
                                              _kalba(request), kiek,
                                              request.GET.get('salis', ''))})


def ajax_adresas_pagal_taska(request):
    """/ajax/vieta/?lat=&lon= — adresas paleidus žymeklį."""
    from django.http import JsonResponse
    duom = atvirkstinis(request.GET.get('lat'), request.GET.get('lon'),
                        _kalba(request))
    return JsonResponse({'vieta': duom or {}})


# ═══════════════════════════════════════════════════════════════════
# SKELBIMO VIETA → KOORDINATĖS (serverio pusėje, po išsaugojimo)
#
# Formose žemėlapio nebėra (OSM viešos plytelės blokuojamos), tad
# koordinates nustatom patys iš to, ką žmogus įvedė: adresas + miestas +
# šalis. Kviečia Listing.save()/activate() — viena vieta visoms
# kategorijoms, nes dalis formų koordinačių nepildė visai (dalys, #875–883).
#
# Nominatim taisyklės serveriui: ≤1 užklausa/s, aiškus User-Agent,
# rezultatų kešas. Laikomės visų trijų; nesėkmė irgi kešuojama (parai),
# kad nežinomas miestas nekviestų tinklo kiekvieno įrašymo metu.
# ═══════════════════════════════════════════════════════════════════

_NOMINATIM_TARPAS = 1.1          # sekundės tarp užklausų (taisyklė: ≤1/s)
_uzrakas = threading.Lock()
_paskutine = [0.0]
_NERASTA = '__nerasta__'
NESEKMES_KESAS = 60 * 60 * 24    # 1 para


def _nominatim_paieska(q, salis=''):
    """Viena Nominatim paieška su tempo ribojimu. None — nerasta/klaida."""
    with _uzrakas:
        laukti = _NOMINATIM_TARPAS - (time.monotonic() - _paskutine[0])
        if laukti > 0:
            time.sleep(laukti)
        parametrai = {'q': q, 'format': 'jsonv2', 'limit': 1}
        if salis and len(salis) == 2:
            parametrai['countrycodes'] = salis.lower()
        duom = _uzklausa(NOMINATIM_SEARCH, parametrai)
        _paskutine[0] = time.monotonic()
    if not duom:
        return None
    try:
        return float(duom[0]['lat']), float(duom[0]['lon'])
    except (KeyError, IndexError, TypeError, ValueError):
        return None


def _be_diakritiku(tekstas):
    return ''.join(c for c in unicodedata.normalize('NFKD', tekstas)
                   if not unicodedata.combining(c)).lower().strip()


def _is_zodyno(miestas):
    """Atsarga be tinklo: keli dideli miestai iš views.CITY_COORDINATES."""
    from apps.listings.views import CITY_COORDINATES
    return CITY_COORDINATES.get(_be_diakritiku(miestas))


def vietos_koordinates(miestas, adresas='', salis=''):
    """(lat, lon, tikslios) arba None.

    1. adresas + miestas  → tiksli vieta (tikslios=True);
    2. vien miestas       → miesto centras (tikslios=False);
    3. tinklas neveikia   → miesto centras iš vietinio žodyno.
    Tuščias ar „—" miestas → None (nieko nespėliojam; anksčiau čia
    grįždavo Kauno koordinatės bet kokiam nežinomam miestui).
    """
    miestas = (miestas or '').strip()
    adresas = (adresas or '').strip()
    salis = (salis or '').strip().upper()
    if not miestas or miestas in ('—', '-'):
        return None

    raktas = _raktas('vieta', miestas.lower(), adresas.lower(), salis)
    kesuota = cache.get(raktas)
    if kesuota == _NERASTA:
        return None
    if kesuota is not None:
        return tuple(kesuota)

    rezultatas = None
    if adresas:
        taskas = _nominatim_paieska(f'{adresas}, {miestas}', salis)
        if taskas:
            rezultatas = (taskas[0], taskas[1], True)
    if rezultatas is None:
        centras = cache.get(_raktas('vieta', miestas.lower(), '', salis))
        if centras and centras != _NERASTA:
            rezultatas = (centras[0], centras[1], False)
        else:
            taskas = _nominatim_paieska(miestas, salis)
            if taskas:
                rezultatas = (taskas[0], taskas[1], False)
                cache.set(_raktas('vieta', miestas.lower(), '', salis),
                          list(rezultatas), KESO_TRUKME)
    if rezultatas is None:
        is_zodyno = _is_zodyno(miestas)
        if is_zodyno:
            # Tinklo klaidos kešuojam trumpai — kitą kartą bandysim tikslesnį
            return (is_zodyno[0], is_zodyno[1], False)
        cache.set(raktas, _NERASTA, NESEKMES_KESAS)
        return None

    cache.set(raktas, list(rezultatas), KESO_TRUKME)
    return rezultatas
