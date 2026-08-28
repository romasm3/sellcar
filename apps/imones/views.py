# -*- coding: utf-8 -*-
"""
ĮMONIŲ puslapiai: sąrašas su filtrais ir vienos įmonės puslapis.

Rodomos TIK patvirtintos įmonės (`patvirtinta=True`) — servisai
registruosis patys (2 etapas), o kol administratorius nepatvirtino,
puslapyje jų nėra.
"""

from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from .models import Imone, VeiklosSritis

PUSLAPYJE = 24


def _matomos():
    return Imone.objects.filter(patvirtinta=True)


def imoniu_sarasas(request):
    """/imones/ — kortelių tinklelis su filtrais (miestas, tipas, veikla)."""
    qs = _matomos().prefetch_related('veiklos', 'nuotraukos')

    miestas = (request.GET.get('city') or '').strip()
    tipas = (request.GET.get('tipas') or '').strip()
    # Veiklos sritys — žymos, galima rinktis kelias (?veikla=a&veikla=b).
    # Kelios reiškia „bet kuri iš jų": servisas dažnai daro ir remontą,
    # ir padangas, todėl susiaurinti iki „visos kartu" būtų per griežta.
    veiklos_f = [v for v in request.GET.getlist('veikla') if v]
    q = (request.GET.get('q') or '').strip()

    if miestas:
        qs = qs.filter(miestas__icontains=miestas)
    if tipas in dict(Imone.TIPAI):
        qs = qs.filter(tipas=tipas)
    if veiklos_f:
        qs = qs.filter(veiklos__slug__in=veiklos_f)
    if q:
        qs = qs.filter(Q(pavadinimas__icontains=q) | Q(aprasymas__icontains=q))

    imones = list(qs.distinct()[:PUSLAPYJE])

    # Skelbimų skaičius prekiautojų kortelėms — viena užklausa
    kiekiai = {}
    savininkai = [i.savininkas_id for i in imones if i.savininkas_id]
    if savininkai:
        from apps.listings.views import _public_listings_qs
        kiekiai = dict(_public_listings_qs(None).filter(seller_id__in=savininkai)
                       .values_list('seller_id').annotate(n=Count('id')))
    for i in imones:
        i.skelbimu_kiek = kiekiai.get(i.savininkas_id, 0)

    return render(request, 'imones/sarasas.html', {
        'imones': imones,
        'rasta': qs.distinct().count(),
        'miestai': (_matomos().exclude(miestas='')
                    .values_list('miestas', flat=True).distinct().order_by('miestas')),
        # Filtre rodom tik tas sritis, kurios turi bent vieną įmonę
        'veiklos': (VeiklosSritis.objects.filter(imones__patvirtinta=True)
                    .annotate(kiek=Count('imones', distinct=True))
                    .order_by('tvarka', 'pavadinimas').distinct()),
        'tipai': Imone.TIPAI,
        'f_miestas': miestas, 'f_tipas': tipas, 'f_veiklos': veiklos_f, 'f_q': q,
    })


def imone(request, slug):
    """/imone/<slug>/ — vienos įmonės puslapis."""
    obj = get_object_or_404(
        _matomos().prefetch_related('veiklos', 'nuotraukos', 'paslaugos'), slug=slug)

    skelbimai, skelbimu_kiek, zinutes_url = [], 0, ''
    if obj.tipas == Imone.PREKIAUTOJAS:
        qs = obj.skelbimai()
        skelbimu_kiek = qs.count()
        skelbimai = list(qs.order_by('-id')[:8])
        # „Rašyti žinutę" pokalbis rišamas prie skelbimo — imam naujausią.
        # Jei skelbimų nėra, mygtuko nerodom (žr. šabloną).
        if skelbimai:
            from django.urls import reverse
            zinutes_url = reverse('conversations:start', args=[skelbimai[0].pk])

    from django.urls import reverse
    from django.utils.translation import gettext as _t
    trupiniai = [{'label': _t('Įmonės'), 'url': reverse('imones:sarasas')}]
    if obj.miestas:
        trupiniai.append({'label': obj.miestas,
                          'url': reverse('imones:sarasas') + '?city=' + obj.miestas})

    return render(request, 'imones/imone.html', {
        'imone': obj,
        'trupiniai': trupiniai,
        'nuotraukos': list(obj.nuotraukos.all()[:5]),
        'nuotrauku_kiek': obj.nuotraukos.count(),
        'paslaugos': list(obj.paslaugos.all()) if obj.tipas == Imone.SERVISAS else [],
        'skelbimai': skelbimai,
        'skelbimu_kiek': skelbimu_kiek,
        'zinutes_url': zinutes_url,
        'laikai': obj.savaites_laikai(),
    })


def zemelapio_imones(request):
    """JSON žemėlapio paieškai: įmonės matomame plote.

    Grąžinam tą patį pavidalą, kurį žemėlapis jau moka piešti, plius
    logotipo adresą — žymeklis su logotipu.
    """
    qs = _matomos().exclude(latitude=None).exclude(longitude=None)

    def _riba(v):
        try:
            return float(v)
        except (TypeError, ValueError):
            return None

    s, n = _riba(request.GET.get('s')), _riba(request.GET.get('n'))
    v, r = _riba(request.GET.get('v')), _riba(request.GET.get('r'))
    if None not in (s, n, v, r):
        qs = qs.filter(latitude__gte=s, latitude__lte=n)
        qs = (qs.filter(longitude__gte=v, longitude__lte=r) if v <= r
              else qs.filter(Q(longitude__gte=v) | Q(longitude__lte=r)))

    tipas = (request.GET.get('imoniu_tipas') or '').strip()
    if tipas in dict(Imone.TIPAI):
        qs = qs.filter(tipas=tipas)

    imones = list(qs[:300])
    kiekiai = {}
    savininkai = [i.savininkas_id for i in imones if i.savininkas_id]
    if savininkai:
        from apps.listings.views import _public_listings_qs
        kiekiai = dict(_public_listings_qs(None).filter(seller_id__in=savininkai)
                       .values_list('seller_id').annotate(n=Count('id')))

    return JsonResponse({'imones': [{
        'id': i.pk,
        'vardas': i.pavadinimas,
        'lat': float(i.latitude),
        'lng': float(i.longitude),
        'logo': i.logotipas.url if i.logotipas else '',
        'kiek': kiekiai.get(i.savininkas_id, 0),
        'url': i.get_absolute_url(),
        'tipas': i.tipas,
    } for i in imones]})
