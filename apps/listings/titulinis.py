# -*- coding: utf-8 -*-
"""Titulinio puslapio skelbimų srautai — „Pasiūlymai" ir „Dienos pasiūlymai".

KODĖL ATSKIRAS FAILAS. Skelbimai gyvena DVIEJOSE lentelėse: `Listing`
(visos kategorijos, /<id>/) ir `WheelListing` (padangos ir ratlankiai,
/wheels/<id>/). Titulinis rodė tik pirmąją, todėl dvylika padangų ir
ratlankių nepatekdavo niekur — nei į skaitliukus, nei į skirtukus.
Sujungimo taisyklės yra vienos ir tos pačios visiems skirtukams, tad
guli viename faile, o ne išbarstytos po views.py.

Ką duoda:
    ratlankiu_qs()      — vieši ratlankiai/padangos, su šalies filtru
    kategorija()        — vienodas kategorijos raktas abiem modeliams
    pasiulymai()        — po 1–2 iš KIEKVIENOS netuščios kategorijos
    dienos_pasiulymai() — kaina žemiau savo grupės medianos
    naujausi/populiariausi/brangiausi — tas pats pjūvis iš abiejų lentelių
    ratu_kiekiai()      — {'tyre': n, 'rim': n} kategorijų skaitliukams
"""

import datetime
import random
import statistics

from django.db.models import Count, F, Value
from django.db.models.functions import Coalesce

# „Pasiūlymuose" iš vienos kategorijos — ne daugiau tiek kortelių.
PER_KATEGORIJA = 2
# „Dienos pasiūlymuose" metų juostos plotis ir atskaitos taškas, kad
# juostos kristų 2020-2022, 2023-2025... — o ne kur pakliuvo.
METU_JUOSTA = 3
METU_BAZE = 2020
# Mažesnėje grupėje mediana nepatikima — grupė praleidžiama.
MIN_GRUPEJE = 5

# Ratlankių/padangų kategorijų raktai — atitinka juostos punktus
# (views._rail_url: /browse/tyres/, /browse/rims/).
RATU_KATEGORIJOS = {'tyre': 'tyres', 'rim': 'rims'}


# ── Bendri šaltiniai ────────────────────────────────────────────────

def ratlankiu_qs(request=None):
    """Vieši ratlankiai ir padangos, filtruoti pagal šalies juostą.

    Tas pats matomumo filtras kaip views._public_listings_qs: aktyvūs ir
    ne shadow-ban'inti.
    """
    from .models import WheelListing
    qs = (WheelListing.objects
          .filter(status='active', is_shadow_banned=False)
          .prefetch_related('images'))
    if request is not None:
        from . import salies_juosta
        qs = salies_juosta.filtruoti(qs, request)
    return qs


def ratu_kiekiai():
    """{'tyre': n, 'rim': n} — kategorijų skaitliukams.

    Laukas yra `product_type`, ne `wheel_type`: pastarojo modelyje nėra,
    o views.py jį filtre naudojo po `except Exception`, tad skaitliukai
    tyliai virsdavo nuliais („Padangos (0)", „Ratlankiai (0)").
    """
    from .models import WheelListing
    eilutes = (WheelListing.objects
               .filter(status='active', is_shadow_banned=False)
               .values_list('product_type')
               .annotate(n=Count('id')))
    kiekiai = dict(eilutes)
    return {'tyre': kiekiai.get('tyre', 0), 'rim': kiekiai.get('rim', 0)}


def ar_ratlankis(objektas):
    return objektas.__class__.__name__ == 'WheelListing'


def kategorija(objektas):
    """Vienodas kategorijos raktas abiem modeliams."""
    if ar_ratlankis(objektas):
        return RATU_KATEGORIJOS.get(objektas.product_type, 'wheels')
    vt = getattr(objektas, 'vehicle_type', None)
    return getattr(vt, 'slug', '') or 'kita'


def _sekla(request):
    """Data + sesija: atranka atsitiktinė, bet per sesiją nešokinėja.

    Perkrovus puslapį tą pačią dieną su ta pačia sesija tvarka lieka ta
    pati; rytoj arba kitam lankytojui ji bus kita.
    """
    diena = datetime.date.today().isoformat()
    raktas = ''
    if request is not None:
        sesija = getattr(request, 'session', None)
        raktas = (getattr(sesija, 'session_key', None)
                  or request.COOKIES.get('sessionid', '')
                  or '')
    return '%s|%s' % (diena, raktas)


def _paimti(listing_qs, ratai_qs, listing_ids, ratu_ids):
    """Objektai pagal ID — po vieną užklausą modeliui, tvarka nesvarbi."""
    rasta = {}
    if listing_ids:
        for o in listing_qs.filter(pk__in=listing_ids):
            rasta[('L', o.pk)] = o
    if ratu_ids:
        for o in ratai_qs.filter(pk__in=ratu_ids):
            rasta[('R', o.pk)] = o
    return rasta


# ── „Pasiūlymai" — po 1–2 iš kiekvienos kategorijos ─────────────────

def pasiulymai(listing_qs, request, per_kategorija=PER_KATEGORIJA):
    """Po kelis skelbimus iš KIEKVIENOS kategorijos, kurioje jų yra.

    Anksčiau čia buvo naujausi pagal ID, todėl iš dvylikos kortelių
    vienuolika būdavo automobiliai — likusios kategorijos nesimatė visai.

    Kategorijos be aktyvių skelbimų praleidžiamos savaime: jų tiesiog
    nėra sugrupuotame sąraše.
    """
    ratai_qs = ratlankiu_qs(request)

    # Viena užklausa modeliui: (pk, kategorijos raktas)
    poros = [('L', pk, slug or 'kita') for pk, slug
             in listing_qs.values_list('pk', 'vehicle_type__slug')]
    poros += [('R', pk, RATU_KATEGORIJOS.get(tipas, 'wheels')) for pk, tipas
              in ratai_qs.values_list('pk', 'product_type')]
    if not poros:
        return []

    grupes = {}
    for zyme, pk, slug in poros:
        grupes.setdefault(slug, []).append((zyme, pk))

    r = random.Random(_sekla(request))
    eile = sorted(grupes)                 # stabilus pagrindas
    r.shuffle(eile)                       # ...ir stabilus maišymas

    pasirinkti = []
    for slug in eile:
        nariai = sorted(grupes[slug])     # kad sample būtų atkartojamas
        kiek = min(per_kategorija, len(nariai))
        pasirinkti += r.sample(nariai, kiek)

    rasta = _paimti(listing_qs, ratai_qs,
                    [pk for z, pk in pasirinkti if z == 'L'],
                    [pk for z, pk in pasirinkti if z == 'R'])
    return [rasta[(z, pk)] for z, pk in pasirinkti if (z, pk) in rasta]


# ── „Dienos pasiūlymai" — kaina žemiau grupės medianos ──────────────

def _metu_juosta(metai):
    """Metų juostos numeris: 2020-2022 -> 0, 2023-2025 -> 1, 2017-2019 -> -1."""
    if not metai:
        return None
    return (int(metai) - METU_BAZE) // METU_JUOSTA


def dienos_pasiulymai(listing_qs, request, kiek=12):
    """Skelbimai, kurių kaina žemiau savo grupės medianos.

    Grupė = kategorija + pagaminimo metų juosta (po METU_JUOSTA metus).
    Ratlankiams ir padangoms metų nėra, tad jų grupė — tik kategorija.

    Skaičiuojama iš aktyvių skelbimų su kaina > 0. Grupė, kurioje mažiau
    nei MIN_GRUPEJE skelbimų, praleidžiama — iš trijų kainų mediana
    nieko nereiškia.

    Anksčiau šis skirtukas reiškė „šiandien įkelta", tad tyliomis
    dienomis būdavo tuščias ir dubliuodavo „Naujausius".
    """
    ratai_qs = ratlankiu_qs(request)

    irasai = [('L', pk, (slug or 'kita', _metu_juosta(metai)), float(kaina))
              for pk, slug, metai, kaina
              in listing_qs.filter(price__gt=0)
                           .values_list('pk', 'vehicle_type__slug', 'year', 'price')
              if kaina is not None]
    irasai += [('R', pk, (RATU_KATEGORIJOS.get(tipas, 'wheels'), None), float(kaina))
               for pk, tipas, kaina
               in ratai_qs.filter(price__gt=0)
                          .values_list('pk', 'product_type', 'price')
               if kaina is not None]
    if not irasai:
        return []

    grupes = {}
    for zyme, pk, raktas, kaina in irasai:
        grupes.setdefault(raktas, []).append((zyme, pk, kaina))

    radiniai = []
    for nariai in grupes.values():
        if len(nariai) < MIN_GRUPEJE:
            continue
        mediana = statistics.median([k for _, _, k in nariai])
        if mediana <= 0:
            continue
        for zyme, pk, kaina in nariai:
            if kaina <= mediana:
                radiniai.append((zyme, pk, (mediana - kaina) / mediana))

    if not radiniai:
        return []

    # Didžiausia nuolaida pirma; ties lygiosiomis — stabili tvarka.
    radiniai.sort(key=lambda t: (-t[2], t[0], t[1]))
    radiniai = radiniai[:kiek]

    rasta = _paimti(listing_qs, ratai_qs,
                    [pk for z, pk, _ in radiniai if z == 'L'],
                    [pk for z, pk, _ in radiniai if z == 'R'])
    isvada = []
    for zyme, pk, nuolaida in radiniai:
        o = rasta.get((zyme, pk))
        if o is None:
            continue
        # Kortelė gali parodyti, KIEK pigiau (sveikais procentais).
        o.nuolaida_proc = int(round(nuolaida * 100))
        isvada.append(o)
    return isvada


# ── Likę skirtukai — tas pats pjūvis iš abiejų lentelių ─────────────

def _sujungti(listing_qs, ratai_qs, raktas, kiek, atvirkscias=True):
    """Po `kiek` iš kiekvieno modelio, sujungta ir perrikiuota.

    Iš kiekvienos lentelės užtenka paimti `kiek` — daugiau į galutinį
    sąrašą vis tiek nepatektų.
    """
    nariai = list(listing_qs[:kiek]) + list(ratai_qs[:kiek])
    nariai.sort(key=raktas, reverse=atvirkscias)
    return nariai[:kiek]


def naujausi(listing_qs, request, kiek=6):
    from django.db.models.functions import Coalesce as _C
    kiti = listing_qs.annotate(
        paskelbta_db=_C('activated_at', 'created_at')).order_by('-paskelbta_db')
    ratai = ratlankiu_qs(request).annotate(
        paskelbta_db=_C('activated_at', 'created_at')).order_by('-paskelbta_db')
    return _sujungti(kiti, ratai, lambda o: o.paskelbta_db, kiek)


def _populiarumas(qs):
    """Peržiūros + įsiminimai.

    Vien peržiūrų neužtenka: nauji skelbimai visi turi 0, tad tvarka
    būdavo atsitiktinė. Įsiminimas yra stipresnis ženklas nei peržiūra,
    bet čia sudedami lygiaverčiai — kol duomenų mažai, svoriai būtų
    apsimetinėjimas tikslumu.
    """
    return qs.annotate(
        _populiarumas=Coalesce(F('views_count'), Value(0)) +
                      Count('saved_by', distinct=True)
    ).order_by('-_populiarumas')


def populiariausi(listing_qs, request, kiek=6):
    """Abu modeliai turi ir views_count, ir saved_by — formulė ta pati."""
    return _sujungti(_populiarumas(listing_qs),
                     _populiarumas(ratlankiu_qs(request)),
                     lambda o: o._populiarumas, kiek)


def turi_populiarumo(nariai):
    """Ar skirtuką apskritai verta rodyti — ar yra bent vienas ženklas."""
    return any(getattr(o, '_populiarumas', 0) for o in nariai)


def brangiausi(listing_qs, request, kiek=6):
    kiti = listing_qs.filter(price__gt=0).order_by('-price')
    ratai = ratlankiu_qs(request).filter(price__gt=0).order_by('-price')
    return _sujungti(kiti, ratai, lambda o: o.price, kiek)
