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

from .korteles import kortele
from .models import Listing, SavedListing

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

    irasai = list(qs.order_by('-id')[:MAKS_KORTELIU])

    issaugoti = set()
    if request.user.is_authenticated:
        issaugoti = set(SavedListing.objects.filter(
            user=request.user, listing__in=irasai).values_list('listing_id', flat=True))

    html = render_to_string('listings/partials/_zemelapio_sarasas.html', {
        'korteles': [kortele(o, issaugotas=o.pk in issaugoti) for o in irasai],
    }, request=request)

    # values() — be select_related, todėl žymekliams neužklausiam nieko
    # daugiau, negu reikia taškui nupiešti
    zymekliai = [
        {'id': z['id'], 'lat': float(z['latitude']), 'lng': float(z['longitude']),
         'tikslu': z['koordinates_tikslios']}
        for z in qs.values('id', 'latitude', 'longitude',
                           'koordinates_tikslios')[:MAKS_ZYMEKLIU]
    ]

    return JsonResponse({'kiek': kiek, 'html': html, 'zymekliai': zymekliai,
                         'rodoma': len(irasai)})


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
        'papildomi_filtrai': [
            ('vin', _t('Su VIN')),
            ('feat_warranty', _t('Su garantija')),
            ('tik_lietuvoje', _t('Tik Lietuvoje')),
            ('su_nuotraukomis', _t('Su nuotraukomis')),
        ],
        'makes': (Brand.objects.filter(vehicle_type__slug='cars')
                  .values_list('name', flat=True).distinct().order_by('name')),
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
