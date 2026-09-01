# -*- coding: utf-8 -*-
"""
ŠALIES JUOSTA virš greitosios paieškos panelės.

    📍 Lithuania · 4 821 skelbimas            [Keisti šalį ▾]

Kodėl atskiras failas: juosta turi savo pasirinkimo taisykles (adresas →
slapukas → numatytoji) ir savo skaičiukus iš DB. Panelės viduje niekas
nesikeičia — tai atskira eilutė virš jos.

Pasirinkimas:
    1. ?salis=de           — aiškus vartotojo veiksmas, laimi visada
    2. slapukas „salis"    — praeitas pasirinkimas, galioja grįžus
    3. salys.NUMATYTA      — „LT"

Skaičiai — tikri, iš to paties viešų skelbimų queryset'o, kurį rodo
sąrašas. Šalys be skelbimų sąraše nerodomos (išskyrus pasirinktąją, kad
eilutė neliktų tuščia).
"""
from django.core.cache import cache

from . import salys

SLAPUKAS = 'salis'
SLAPUKO_AMZIUS = 60 * 60 * 24 * 365      # metai
KESO_RAKTAS = 'salies_juostos_kiekiai'
KESO_LAIKAS = 300                         # 5 min — skaičiukai, ne pinigai


def _kodas(reiksme):
    """'de' → 'DE'. Nežinomą kodą atmetam, kad ?salis=xx nefiltruotų tuščiai."""
    kodas = str(reiksme or '').strip().upper()
    return kodas if kodas in salys.VARDAI else ''


def pasirinkta(request):
    """Kuri šalis rodoma juostoje. Visada grąžina galiojantį kodą."""
    return (_kodas(request.GET.get('salis'))
            or _kodas(request.COOKIES.get(SLAPUKAS))
            or salys.NUMATYTA)


def aiskiai_pasirinkta(request):
    """Ar žmogus šalį pasirinko pats (adresu arba anksčiau — slapuku)."""
    return bool(_kodas(request.GET.get('salis'))
                or _kodas(request.COOKIES.get(SLAPUKAS)))


def kiekiai(vieso_qs=None):
    """{'LT': 4821, 'DE': 217, …} — tikri skaičiai iš DB.

    Kešuojama 5 min: juosta renderinama kiekviename puslapyje, o
    GROUP BY per visus skelbimus nėra nemokamas.
    """
    esami = cache.get(KESO_RAKTAS)
    if esami is not None:
        return esami

    from django.db.models import Count
    if vieso_qs is None:
        from .views import _public_listings_qs
        vieso_qs = _public_listings_qs(None)
    eilutes = (vieso_qs.exclude(country='')
               .values('country').annotate(kiek=Count('id')))
    surinkta = {e['country']: e['kiek'] for e in eilutes}
    cache.set(KESO_RAKTAS, surinkta, KESO_LAIKAS)
    return surinkta


def _nuoroda(request, kodas):
    """Tas pats puslapis su kita šalimi — visi kiti filtrai lieka.

    Puslapiavimą numetam: pakeitus šalį 7-as puslapis dažniausiai jau
    neegzistuoja.
    """
    params = request.GET.copy()
    params['salis'] = kodas.lower()
    params.pop('page', None)
    return '%s?%s' % (request.path, params.urlencode())


def sarasas(dabartine, vieso_qs=None, request=None):
    """Šalys juostos sąrašui — pagal skelbimų kiekį, ne abėcėlę."""
    skaiciai = kiekiai(vieso_qs)
    eilutes = [
        {'kodas': kodas, 'zemas': kodas.lower(),
         'vardas': salys.vardas_en(kodas), 'kiek': kiek,
         'dabartine': kodas == dabartine,
         'url': _nuoroda(request, kodas) if request else '?salis=' + kodas.lower()}
        for kodas, kiek in skaiciai.items() if kiek and kodas in salys.VARDAI
    ]
    if dabartine and not any(e['dabartine'] for e in eilutes):
        # Pasirinkta šalis rodoma net be skelbimų — kitaip sąraše nebūtų
        # matyti, kas šiuo metu įjungta.
        eilutes.append({
            'kodas': dabartine, 'zemas': dabartine.lower(),
            'vardas': salys.vardas_en(dabartine), 'kiek': 0, 'dabartine': True,
            'url': _nuoroda(request, dabartine) if request else '?salis=' + dabartine.lower()})
    eilutes.sort(key=lambda e: (-e['kiek'], e['vardas']))
    return eilutes


def kontekstas(request, vieso_qs=None):
    """Viskas, ko reikia templates/listings/partials/_salies_juosta.html."""
    dabartine = pasirinkta(request)
    eilutes = sarasas(dabartine, vieso_qs, request)
    return {
        'salies_kodas': dabartine,
        'salies_vardas': salys.vardas_en(dabartine),
        'salies_kiekis': next((e['kiek'] for e in eilutes if e['dabartine']), 0),
        'salies_sarasas': eilutes,
    }


def filtruoti(listings, request):
    """Skelbimai tik iš pasirinktos šalies.

    Numatytoji („LT") filtruoja TIK tada, kai tokių skelbimų iš tikrųjų
    yra: dalis senų įrašų turi country='US' (migracijose 0018–0032 toks
    buvo laukelio numatytasis), ir tyliai pritaikytas LT filtras būtų
    ištuštinęs sąrašą žmogui, kuris nieko nesirinko. Aiškus pasirinkimas
    (adresu ar slapuku) taikomas visada.
    """
    kodas = pasirinkta(request)
    if aiskiai_pasirinkta(request) or kiekiai().get(kodas):
        return listings.filter(country=kodas)
    return listings


def atsiminti(response, request):
    """Įrašo pasirinkimą į slapuką, kai jis atėjo adresu."""
    kodas = _kodas(request.GET.get('salis'))
    if kodas and request.COOKIES.get(SLAPUKAS) != kodas:
        response.set_cookie(SLAPUKAS, kodas, max_age=SLAPUKO_AMZIUS,
                            samesite='Lax')
    return response
