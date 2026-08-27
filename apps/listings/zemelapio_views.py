# -*- coding: utf-8 -*-
"""
ŽEMĖLAPIO PAIEŠKA — /map/ ir jos duomenų galas.

Maketas kaip Fresha: kairėje rezultatai dviem stulpeliais, dešinėje
prilipęs žemėlapis. Sąrašas persirenka pagal MATOMĄ žemėlapio plotą,
todėl duomenys imami per atskirą galą (/map/duomenys/): jam paduodam
kraštines (šiaurė/pietūs/rytai/vakarai), o jis grąžina korteles ir jų
skaičių.

Kortelė ta pati kaip rezultatų puslapyje (partials/_skelbimo_kortele.html
per korteles.py) — atskiros kopijos nėra.
"""

import json

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from . import formatai
from .korteles import kortele
from .models import Listing, SavedListing

SIMBOLIAI = {'EUR': '€', 'USD': '$', 'GBP': '£'}

MAKS_KORTELIU = 60          # kiek kortelių rodom sąraše vienu metu
MAKS_ZYMEKLIU = 2000        # kiek taškų siunčiam žemėlapiui


def _filtruoti(request, qs=None):
    """Filtrai — TAS PATS kelias kaip rezultatų puslapyje ir detalioje
    paieškoje: search_params.sanitize + views.filter_listings. Ketvirtos
    kopijos nėra, todėl „Benzinas" čia ir ten reiškia tą patį."""
    from .views import filter_listings
    from .search_params import sanitize as sanitize_search_params
    parametrai = sanitize_search_params(request.GET)
    return filter_listings(parametrai, user=request.user,
                           category=parametrai.get('category') or None,
                           base_qs=qs if qs is not None else _su_koordinatemis(request.user))


def _su_koordinatemis(user):
    from .views import _public_listings_qs
    return _public_listings_qs(user).exclude(latitude=None).exclude(longitude=None)


def _riba(reiksme):
    try:
        return float(reiksme)
    except (TypeError, ValueError):
        return None


def zemelapio_rezultatai(request):
    """JSON: kortelės ir žymekliai matomame plote."""
    qs = _filtruoti(request, _su_koordinatemis(request.user).select_related(
        'brand', 'model', 'fuel_type', 'transmission', 'vehicle_type'
    ).prefetch_related('images'))
    s, n = _riba(request.GET.get('s')), _riba(request.GET.get('n'))
    v, r = _riba(request.GET.get('v')), _riba(request.GET.get('r'))
    if None not in (s, n, v, r):
        qs = qs.filter(latitude__gte=s, latitude__lte=n)
        # Jei plotas kerta 180-ąjį dienovidinį, ilguma „apsisuka"
        qs = qs.filter(longitude__gte=v, longitude__lte=r) if v <= r else \
             qs.filter(Q(longitude__gte=v) | Q(longitude__lte=r))

    kiek = qs.count()

    # Filtrų langui užtenka skaičiaus — jis skaičiuojamas SU tomis pačiomis
    # kraštinėmis, todėl mygtuke matomas tas pats skaičius, kurį žmogus
    # pamatys sąraše pritaikęs filtrus.
    if request.GET.get('tik_skaicius'):
        return JsonResponse({'kiek': kiek})

    # Rikiavimas — ta pati funkcija kaip rezultatų puslapyje; be jos
    # filtrų lango „Rūšiuoti pagal" nieko nedarydavo.
    irasai = list(_rikiuoti_zemelapiui(qs, request)[:MAKS_KORTELIU])

    issaugoti = set()
    if request.user.is_authenticated:
        issaugoti = set(SavedListing.objects.filter(
            user=request.user, listing__in=irasai).values_list('listing_id', flat=True))

    html = render_to_string('listings/partials/_zemelapio_sarasas.html', {
        'korteles': [kortele(o, issaugotas=o.pk in issaugoti) for o in irasai],
    }, request=request)

    zymekliai = _zymekliai(qs, request)

    return JsonResponse({'kiek': kiek, 'html': html, 'zymekliai': zymekliai,
                         'rodoma': len(irasai)})


def _markes_zemelapyje(user):
    """[{v, n}] — markės, kurių skelbimai turi koordinates.

    Vardai imami iš DB nekeičiant: jei ten „Škoda", taip ir rodom.
    Sąrašas trumpas ir tikras — anksčiau juostoje gulėjo visos
    automobilių markės, įskaitant tas, kurių žemėlapyje nė vienos.
    """
    eilutes = (_su_koordinatemis(user).exclude(brand=None)
               .values('brand_id', 'brand__name').distinct()
               .order_by('brand__name'))
    return [{'v': e['brand_id'], 'n': e['brand__name']} for e in eilutes]


def _rikiuoti_zemelapiui(qs, request):
    """Rikiavimas žemėlapyje: bendra views.rikiuoti + „Arčiausiai".

    „Arčiausiai" prasmę turi tik čia, todėl ir gyvena čia. Atskaitos
    taškas — vartotojo vieta (mlat/mlng), o jei jos nėra, žemėlapio
    centras. Atstumas skaičiuojamas apytiksliai (plokščias, ilgumos
    skirtumas pataisytas pagal platumą) — rikiavimui to užtenka ir
    nereikia PostGIS.
    """
    from .views import rikiuoti

    if (request.GET.get('sort') or '') != 'arciausiai':
        return rikiuoti(qs, request.GET.get('sort'))

    from django.db.models import F, FloatField, ExpressionWrapper, Value
    import math

    lat = _riba(request.GET.get('mlat')) or _riba(request.GET.get('lat'))
    lng = _riba(request.GET.get('mlng')) or _riba(request.GET.get('lng'))
    if lat is None or lng is None:
        return rikiuoti(qs, 'newest')

    k = math.cos(math.radians(lat)) ** 2
    atstumas = ExpressionWrapper(
        (F('latitude') - Value(lat)) * (F('latitude') - Value(lat))
        + (F('longitude') - Value(lng)) * (F('longitude') - Value(lng)) * Value(k),
        output_field=FloatField())
    return qs.annotate(_atstumas=atstumas).order_by('_atstumas')


def zemelapio_paieska(request):
    """Puslapis. Pradinis turinys — Lietuva; toliau viską tvarko žemėlapis."""
    from django.conf import settings
    from .models import Brand, Model as ModelasModelis
    from django.utils import timezone

    qs = _filtruoti(request)
    metai = timezone.now().year

    from .models import FuelType
    from django.utils.translation import gettext as _t

    return render(request, 'listings/search_map.html', {
        'is_viso': qs.count(),
        # Filtrų lango turinys — tie patys raktai, kaip visose paieškose
        'rusiavimo_kortos': [
            ('newest', _t('Naujausi'), 'fa-clock'),
            ('arciausiai', _t('Arčiausiai'), 'fa-location-crosshairs'),
            ('price_asc', _t('Pigiausi'), 'fa-arrow-down-short-wide'),
            ('price_desc', _t('Brangiausi'), 'fa-arrow-up-wide-short'),
        ],
        'filtru_kategorijos': [
            {'slug': 'cars', 'label': _t('Automobiliai')},
            {'slug': 'motorcycles', 'label': _t('Motociklai')},
            {'slug': 'trucks', 'label': _t('Sunkusis transportas')},
            {'slug': 'trailers', 'label': _t('Priekabos')},
            {'slug': 'agriculture', 'label': _t('Žemės ūkio')},
            {'slug': 'construction', 'label': _t('Statybinė')},
            {'slug': 'parts', 'label': _t('Dalys')},
            {'slug': 'rental', 'label': _t('Nuoma')},
        ],
        'kuro_tipai': FuelType.objects.all().order_by('name'),
        # Raktai — TIKRI filter_listings parametrai, ne savi vardai.
        # „vin"/„tik_lietuvoje" niekur nebuvo skaitomi, todėl tos žymos
        # tik piešdavosi ir nieko nefiltruodavo.
        'papildomi_filtrai': [
            ('has_vin', '1', _t('Su VIN')),
            ('feat_warranty', 'on', _t('Su garantija')),
            ('country_filter', 'LT', _t('Tik Lietuvoje')),
            ('su_nuotraukomis', '1', _t('Su nuotraukomis')),
        ],
        # Markės — id ir vardas, o ne vardas kaip tekstas: filtruojam
        # `brand=<id>`, nes būtent jį supranta filter_listings. Rodom tik
        # tas markes, kurių skelbimai žemėlapyje realiai yra, ir vardus
        # tokius, kokie įrašyti DB („Škoda", ne „Skoda").
        'makes': _markes_zemelapyje(request.user),
        'models': ModelasModelis.objects.values_list('name', flat=True)
                  .distinct().order_by('name'),
        'years': list(range(metai + 1, 1989, -1)),
        'GOOGLE_MAPS_API_KEY': getattr(settings, 'GOOGLE_MAPS_API_KEY', ''),
        'pradine_busena': ({
            'lat': _riba(request.GET.get('lat')) or 55.17,
            'lng': _riba(request.GET.get('lng')) or 23.88,
            'z': int(request.GET.get('z') or 7),
            'is_url': bool(request.GET.get('lat')),
        }),
    })


# ═══════════════════════════════════════════════════════════════════
# ŽYMEKLIAI
#
# Žemėlapyje rodoma KAINA, ne taškas. Prekiautojų skelbimai suklijuojami
# į vieną aikštelės žymeklį. Apytikslėms vietoms koordinatės apvalinamos
# ČIA — tikslios į naršyklę neiškeliauja.
# ═══════════════════════════════════════════════════════════════════

APVALINIMAS = 3          # 3 skaitmenys ≈ 110 m tikslumas


def _apytiksliai(reiksme):
    return round(float(reiksme), APVALINIMAS)


def _zymekliai(qs, request):
    laukai = ('id', 'latitude', 'longitude', 'koordinates_tikslios',
              'hide_exact_address', 'price', 'currency', 'city',
              'seller_id', 'seller__profile__dealer_subscription_active',
              'seller__profile__dealer_company_name', 'seller__username')
    eilutes = list(qs.values(*laukai)[:MAKS_ZYMEKLIU])

    # Prekiautojų skelbimai — vienas žymeklis aikštelei
    prekiautoju = {}
    for e in eilutes:
        if e['seller__profile__dealer_subscription_active']:
            prekiautoju.setdefault(e['seller_id'], []).append(e)

    zymekliai = []
    for e in eilutes:
        if e['seller_id'] in prekiautoju:
            continue
        neaisku = e['hide_exact_address'] or not e['koordinates_tikslios']
        zymekliai.append({
            'id': e['id'],
            'lat': _apytiksliai(e['latitude']) if neaisku else float(e['latitude']),
            'lng': _apytiksliai(e['longitude']) if neaisku else float(e['longitude']),
            'kaina': formatai.kaina(e['price'], SIMBOLIAI.get(e['currency'], '€')),
            'apytiksliai': bool(e['hide_exact_address']),
            'spetas': not e['koordinates_tikslios'],
        })

    for seller_id, jo in prekiautoju.items():
        pirmas = jo[0]
        zymekliai.append({
            'tipas': 'pardavejas',
            'pardavejas': seller_id,
            'lat': float(pirmas['latitude']),
            'lng': float(pirmas['longitude']),
            'vardas': (pirmas['seller__profile__dealer_company_name']
                       or pirmas['seller__username']),
            'kiek': len(jo),
        })
    return zymekliai


def zemelapio_kortele(request, pk):
    """Burbulo turinys paspaudus žymeklį."""
    from django.shortcuts import get_object_or_404
    from .models import Listing as L
    l = get_object_or_404(_su_koordinatemis(request.user), pk=pk)
    neaisku = l.hide_exact_address or not l.koordinates_tikslios
    return JsonResponse({
        'html': render_to_string('listings/partials/_zemelapio_burbulas.html',
                                 {'l': l, 'neaisku': neaisku}, request=request),
        # Navigacijai — apvalintos, jei vieta apytikslė
        'lat': _apytiksliai(l.latitude) if neaisku else float(l.latitude),
        'lng': _apytiksliai(l.longitude) if neaisku else float(l.longitude),
    })


def zemelapio_pardavejas(request, pk):
    """Prekiautojo aikštelė — visi jo skelbimai sąraše."""
    qs = _filtruoti(request).filter(seller_id=pk)
    irasai = list(qs.order_by('-id')[:50])
    return JsonResponse({
        'kiek': qs.count(),
        'html': render_to_string('listings/partials/_zemelapio_aikstele.html',
                                 {'korteles': [kortele(o) for o in irasai]},
                                 request=request),
    })
