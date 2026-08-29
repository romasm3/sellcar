# -*- coding: utf-8 -*-
"""
ĮMONIŲ puslapiai: sąrašas su filtrais ir vienos įmonės puslapis.

Rodomos TIK patvirtintos įmonės (`patvirtinta=True`) — servisai
registruosis patys (2 etapas), o kol administratorius nepatvirtino,
puslapyje jų nėra.
"""

from django.conf import settings
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from .models import Imone, VeiklosSritis

PUSLAPYJE = 24
ZEMELAPYJE = 60      # kiek kortelių rodom žemėlapio sąraše


# Trečio juostos lauko reikšmės — filtruojam pagal DARBO LAIKĄ, ne
# rezervaciją: rezervacijų sistemos nėra ir neplanuojam.
LAIKO_PASIRINKIMAI = [
    ('', _('Bet kada')),
    ('dabar', _('Atidaryta dabar')),
    ('siandien', _('Šiandien')),
    ('rytoj', _('Rytoj')),
    ('sestadieni', _('Šeštadienį')),
    ('sekmadieni', _('Sekmadienį')),
]


def _tinka_laikui(imone, laikas):
    from django.utils import timezone

    siandien = timezone.localtime().weekday()
    if laikas == 'dabar':
        return imone.ar_atidaryta()
    if laikas == 'siandien':
        return imone.dirba(siandien)
    if laikas == 'rytoj':
        return imone.dirba((siandien + 1) % 7)
    if laikas == 'sestadieni':
        return imone.dirba(5)
    if laikas == 'sekmadieni':
        return imone.dirba(6)
    return True


def _matomos():
    return Imone.objects.filter(patvirtinta=True)


def _filtruoti(request, qs=None):
    """Filtrai — VIENAS kelias sąrašui ir žemėlapiui.

    Parametrai keliauja tarp /imones/ ir /imones/map/, bet su skelbimų
    puse (/skelbimai/, /map/) nesimaišo: čia savi laukai ir savas
    queryset.
    """
    qs = _matomos() if qs is None else qs
    get = request.GET

    miestas = (get.get('city') or '').strip()
    tipas = (get.get('tipas') or '').strip()
    veiklos_f = [v for v in get.getlist('veikla') if v]
    q = (get.get('q') or '').strip()

    if miestas:
        qs = qs.filter(miestas__icontains=miestas)
    if tipas in dict(Imone.TIPAI):
        qs = qs.filter(tipas=tipas)
    if veiklos_f:
        qs = qs.filter(veiklos__slug__in=veiklos_f)
    if q:
        qs = qs.filter(Q(pavadinimas__icontains=q) | Q(aprasymas__icontains=q)
                       | Q(veiklos__pavadinimas__icontains=q))
    return qs.distinct()


def _po_laiko(imones, laikas):
    """Darbo laiko filtras — Python'e (laikas guli JSON lauke)."""
    if not laikas:
        return imones
    return [i for i in imones if _tinka_laikui(i, laikas)]


def _su_skelbimu_kiekiais(imones):
    kiekiai = {}
    savininkai = [i.savininkas_id for i in imones if i.savininkas_id]
    if savininkai:
        from apps.listings.views import _public_listings_qs
        kiekiai = dict(_public_listings_qs(None).filter(seller_id__in=savininkai)
                       .values_list('seller_id').annotate(n=Count('id')))
    for i in imones:
        i.skelbimu_kiek = kiekiai.get(i.savininkas_id, 0)
    return imones


def _filtru_kontekstas(request):
    """Bendras kontekstas abiem puslapiams (filtrai, sąrašai, žymos)."""
    get = request.GET
    veiklos_f = [v for v in get.getlist('veikla') if v]
    miestas = (get.get('city') or '').strip()
    tipas = (get.get('tipas') or '').strip()
    q = (get.get('q') or '').strip()
    laikas = (get.get('laikas') or '').strip()
    return {
        'miestai': (_matomos().exclude(miestas='')
                    .values_list('miestas', flat=True).distinct().order_by('miestas')),
        'veiklos': (VeiklosSritis.objects.filter(imones__patvirtinta=True)
                    .annotate(kiek=Count('imones', distinct=True))
                    .order_by('tvarka', 'pavadinimas').distinct()),
        'tipai': Imone.TIPAI,
        'f_miestas': miestas, 'f_tipas': tipas, 'f_veiklos': veiklos_f,
        'f_q': q, 'f_laikas': laikas,
        'laiko_pasirinkimai': LAIKO_PASIRINKIMAI,
        'aktyviu_filtru': len([x for x in (miestas, tipas, q, laikas) if x]) + len(veiklos_f),
        'GOOGLE_MAPS_API_KEY': getattr(settings, 'GOOGLE_MAPS_API_KEY', ''),
    }


def imoniu_sarasas(request):
    """/imones/ — kortelių tinklelis su filtrais (paieška, vieta, kada)."""
    qs = _filtruoti(request).prefetch_related('veiklos', 'nuotraukos')
    visos = _po_laiko(list(qs), (request.GET.get('laikas') or '').strip())
    imones = _su_skelbimu_kiekiais(visos[:PUSLAPYJE])

    kontekstas = _filtru_kontekstas(request)
    kontekstas.update({'imones': imones, 'rasta': len(visos)})
    return render(request, 'imones/sarasas.html', kontekstas)


def imoniu_zemelapis(request):
    """/imones/map/ — įmonių žemėlapis: kortelės kairėje, žemėlapis dešinėje.

    Atskiras puslapis nuo skelbimų /map/: savi duomenys, savi filtrai,
    sava navigacija. Bendras tik karkasas — kortelė ir žymeklio piešinys.
    """
    kontekstas = _filtru_kontekstas(request)
    kontekstas.update({
        'pradine_busena': {
            'lat': float(request.GET.get('lat') or 55.17),
            'lng': float(request.GET.get('lng') or 23.88),
            'z': int(request.GET.get('z') or 7),
            'is_url': bool(request.GET.get('lat')),
        },
    })
    return render(request, 'imones/zemelapis.html', kontekstas)



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
    """JSON įmonių žemėlapiui: kortelės, žymekliai ir skaičius plote.

    Tas pats pavidalas kaip skelbimų žemėlapyje ({kiek, html, imones}),
    bet duomenys — tik įmonės.
    """
    qs = _filtruoti(request).exclude(latitude=None).exclude(longitude=None)

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

    visos = _po_laiko(list(qs.prefetch_related('veiklos', 'nuotraukos')),
                      (request.GET.get('laikas') or '').strip())
    imones = _su_skelbimu_kiekiais(visos[:ZEMELAPYJE])

    html = render_to_string('imones/_zemelapio_sarasas.html',
                            {'imones': imones}, request=request)
    return JsonResponse({
        'kiek': len(visos),
        'html': html,
        'imones': [{
            'id': i.pk,
            'vardas': i.pavadinimas,
            'lat': float(i.latitude),
            'lng': float(i.longitude),
            'logo': i.logotipas.url if i.logotipas else '',
            'kiek': i.skelbimu_kiek,
            'url': i.get_absolute_url(),
            'tipas': i.tipas,
        } for i in imones],
    })


def zemelapio_kortele(request, pk):
    """Burbulas paspaudus įmonės žymeklį."""
    imone = get_object_or_404(_matomos().prefetch_related('veiklos', 'nuotraukos'),
                              pk=pk)
    _su_skelbimu_kiekiais([imone])
    return JsonResponse({
        'html': render_to_string('imones/_burbulas.html', {'i': imone},
                                 request=request),
        'url': imone.get_absolute_url(),
        'lat': float(imone.latitude) if imone.latitude else None,
        'lng': float(imone.longitude) if imone.longitude else None,
    })
