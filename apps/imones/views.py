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
from django.urls import reverse
from django.template.loader import render_to_string

from apps.listings import formatai
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


# „Paros metas" iš paieškos baro „Kada" lango. Reikšmės sutampa su
# tekstais (Rytas 8–12 …) — jei keisis viena, turi keistis ir kita.
PAROS_LANGAI = {
    'rytas': ('08:00', '12:00'),
    'diena': ('12:00', '17:00'),
    'vakaras': ('17:00', '21:00'),
}


# „Kada" lango juostelės. Raktai sutampa su PAROS_LANGAI.
PAROS_PASIRINKIMAI = [
    ('', _('Bet kada')),
    ('rytas', _('Rytas 8–12')),
    ('diena', _('Diena 12–17')),
    ('vakaras', _('Vakaras 17–21')),
]

# „Populiaru" vietos lange. Koordinatės — miestų centrai; „Visa Lietuva"
# jų neturi, nes ji filtrą nuima.
POPULIARIOS_VIETOS = [
    {'vardas': _('Visa Lietuva'), 'apie': '', 'miestas': '', 'lat': '', 'lng': ''},
    {'vardas': _('Vilnius'), 'apie': _('ir 20 km spinduliu'),
     'miestas': 'Vilnius', 'lat': '54.6872', 'lng': '25.2797'},
    {'vardas': _('Kaunas'), 'apie': '', 'miestas': 'Kaunas',
     'lat': '54.8985', 'lng': '23.9036'},
    {'vardas': _('Klaipėda'), 'apie': '', 'miestas': 'Klaipėda',
     'lat': '55.7033', 'lng': '21.1443'},
]


def _data(reiksme):
    """„2026-09-03" -> date arba None (blogą reikšmę tyliai praleidžiam)."""
    from datetime import date
    try:
        m, d, dd = (reiksme or '').split('-')
        return date(int(m), int(d), int(dd))
    except (ValueError, AttributeError):
        return None


def _tinka_datai(imone, data, paros):
    """Ar tą dieną (ir tuo paros metu) įmonė dirba.

    Paros langas tikrinamas persidengimu: „Rytas 8–12" tinka ir tam,
    kas dirba 10–19, ir tam, kas dirba 7–11.
    """
    laikai = imone.laikas(data.weekday())
    if not laikai:
        return False
    langas = PAROS_LANGAI.get(paros)
    if not langas:
        return True
    return laikai[0] < langas[1] and langas[0] < laikai[1]


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
    # „Įmonės | Specialistai" perjungiklis: meistrai rodomi atskirai
    if tipas == 'meistrai':
        qs = qs.filter(tipas=Imone.MEISTRAS)
    elif tipas in dict(Imone.TIPAI):
        qs = qs.filter(tipas=tipas)
    else:
        qs = qs.filter(tipas__in=Imone.IMONIU_TIPAI)
    if veiklos_f:
        qs = qs.filter(veiklos__slug__in=veiklos_f)
    if q:
        qs = qs.filter(Q(pavadinimas__icontains=q) | Q(aprasymas__icontains=q)
                       | Q(veiklos__pavadinimas__icontains=q))
    return qs.distinct()


def _po_laiko(imones, laikas, data=None, paros=''):
    """Darbo laiko filtras — Python'e (laikas guli JSON lauke).

    Du šaltiniai: datų juosta (`laikas`) ir baro „Kada" langas
    (`data` + `paros`). Abu veikia kartu — kas neatitinka, iškrenta.
    """
    if laikas:
        imones = [i for i in imones if _tinka_laikui(i, laikas)]
    if data:
        imones = [i for i in imones if _tinka_datai(i, data, paros)]
    return imones


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


def _be_tipo(request):
    p = request.GET.copy()
    for k in ('tipas', 'lat', 'lng', 'z', 'skrendam'):
        p.pop(k, None)
    return p.urlencode()


def _filtru_kontekstas(request):
    """Bendras kontekstas abiem puslapiams (filtrai, sąrašai, žymos)."""
    get = request.GET
    veiklos_f = [v for v in get.getlist('veikla') if v]
    miestas = (get.get('city') or '').strip()
    tipas = (get.get('tipas') or '').strip()
    q = (get.get('q') or '').strip()
    laikas = (get.get('laikas') or '').strip()
    data = (get.get('data') or '').strip()
    paros = (get.get('paros') or '').strip()
    return {
        'miestai': (_matomos().exclude(miestas='')
                    .values_list('miestas', flat=True).distinct().order_by('miestas')),
        'veiklos': (VeiklosSritis.objects.filter(imones__patvirtinta=True)
                    .annotate(kiek=Count('imones', distinct=True))
                    .order_by('tvarka', 'pavadinimas').distinct()),
        'tipai': Imone.TIPAI,
        'f_miestas': miestas, 'f_tipas': tipas, 'f_veiklos': veiklos_f,
        'f_q': q, 'f_laikas': laikas, 'f_data': data, 'f_paros': paros,
        'f_lat': (get.get('vlat') or '').strip(), 'f_lng': (get.get('vlng') or '').strip(),
        'laiko_pasirinkimai': LAIKO_PASIRINKIMAI,
        'paros_pasirinkimai': PAROS_PASIRINKIMAI,
        'populiarios_vietos': POPULIARIOS_VIETOS,
        'aktyviu_filtru': (len([x for x in (miestas, q, laikas, data, paros) if x])
                           + len(veiklos_f)),
        # Perjungiklio nuorodos — visi filtrai be `tipas`
        'be_tipo': _be_tipo(request),
        'GOOGLE_MAPS_API_KEY': getattr(settings, 'GOOGLE_MAPS_API_KEY', ''),
        'GOOGLE_MAPS_ID': getattr(settings, 'GOOGLE_MAPS_ID', 'DEMO_MAP_ID'),
    }


def _js_tekstai():
    """Tekstai, kuriuos piešia naršyklė (kortelė, burbulas, datų juosta).

    JS'e eilučių nelaikom — jos verčiamos čia ir keliauja per json_script,
    kad vertimą pagautų makemessages, o ne liktų anglų/lietuvių mišinys.
    """
    # vietinis „_" — kad msgid'us pagautų makemessages (jis ieško _(...))
    from django.utils.translation import gettext as _
    return {
        'imoniu': [_('įmonė'), _('įmonės'), _('įmonių')],
        'betKada': _('Bet kada'),
        'siandien': _('Šiandien'),
        'rytoj': _('Rytoj'),
        'atsiliepimai': _('atsiliepimai'),
        'ziureti': _('Žiūrėti'),
        # Vietos lango pranešimai — tylėti negalima nė vienu atveju
        'vietosIeskom': _('Ieškom jūsų vietos…'),
        'vietosNeleido': _('Vietos leidimas atmestas — įrašykite miestą ranka.'),
        'vietosKlaida': _('Vietos nustatyti nepavyko — įrašykite miestą ranka.'),
        'vietaCia': _('Dabartinė vieta'),
        # „Kada" segmento užrašui — tekstų iš DOM neskaitom
        'paros': {r: str(v) for r, v in PAROS_PASIRINKIMAI if r},
        'dienos': [_('Sk'), _('Pr'), _('An'), _('Tr'), _('Kt'), _('Pn'), _('Št')],
    }


def imoniu_sarasas(request):
    """/imones/ — kortelių tinklelis su filtrais (paieška, vieta, kada)."""
    qs = _filtruoti(request).prefetch_related('veiklos', 'nuotraukos')
    visos = _po_laiko(list(qs), (request.GET.get('laikas') or '').strip(),
                      _data(request.GET.get('data')),
                      (request.GET.get('paros') or '').strip())
    imones = _su_skelbimu_kiekiais(visos[:PUSLAPYJE])

    kontekstas = _filtru_kontekstas(request)
    kontekstas.update({
        'imones': imones, 'rasta': len(visos),
        # Kortelės ir žymekliai piešiami naršyklėje iš /imones/duomenys/,
        # todėl čia užtenka pradinės žemėlapio padėties.
        'tekstai': _js_tekstai(),
        # Pasirinkta vieta (vlat/vlng) tampa pradine žemėlapio padėtimi,
        # jei adrese dar nėra tikslesnio lat/lng.
        'pradine': {'lat': float(request.GET.get('lat') or request.GET.get('vlat') or 54.6872),
                    'lng': float(request.GET.get('lng') or request.GET.get('vlng') or 25.2797),
                    'z': int(request.GET.get('z') or 12)},
    })
    return render(request, 'imones/sarasas.html', kontekstas)


def imoniu_zemelapis(request):
    """Senas /imones/map/ — žemėlapis dabar yra pačiame /imones/ puslapyje."""
    from django.shortcuts import redirect
    adresas = reverse('imones:sarasas')
    if request.GET:
        adresas += '?' + request.GET.urlencode()
    return redirect(adresas)



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
    # vietinis „_" — kad msgid'us pagautų makemessages (jis ieško _(...))
    from django.utils.translation import gettext as _
    trupiniai = [{'label': _('Įmonės'), 'url': reverse('imones:sarasas')}]
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
                      (request.GET.get('laikas') or '').strip(),
                      _data(request.GET.get('data')),
                      (request.GET.get('paros') or '').strip())
    imones = _su_skelbimu_kiekiais(visos[:ZEMELAPYJE])

    html = render_to_string('imones/_zemelapio_sarasas.html',
                            {'imones': imones}, request=request)
    return JsonResponse({'kiek': len(visos), 'imones': [_zemelapiui(i) for i in imones]})


def _zemelapiui(i):
    """Vienos įmonės duomenys kortelei, žymekliui ir burbului.

    Vienas pavidalas visiems trims — kortelė sąraše, piliulė žemėlapyje
    ir burbulas piešiami iš to paties įrašo.
    """
    p = i.pirma_paslauga()
    nuotrauka = i.nuotraukos.first()
    if i.tipas == Imone.PREKIAUTOJAS:
        # Prekiautojui vietoj paslaugos — aikštelė ir kainos pradžia
        paslauga = ('%s %s' % (i.skelbimu_kiek, _('automobiliai aikštelėje'))
                    if i.skelbimu_kiek else str(_('Automobilių prekyba')))
        kaina = _pigiausia(i)
        trukme = ('%s %s' % (_('Atidaryta iki'), i.uzsidaro()) if i.ar_atidaryta()
                  else (('%s · %s %s' % (_('Uždaryta'), _('atidaro'), i.atidaro()))
                        if i.atidaro() else ''))
        cipsai = [{'tekstas': str(_('Žiūrėti skelbimus')), 'ghost': True,
                   'url': i.get_absolute_url() + '#skelbimai'}]
    else:
        paslauga = p.pavadinimas if p else ''
        # Kainos formatas — iš formatai.kaina (lt „30 €", en „€30"), ne ranka.
        kaina = formatai.kaina(p.kaina) if p and p.kaina else ''
        trukme = (_('apie %(min)s min.') % {'min': p.trukme_min}) if p and p.trukme_min else ''
        # Laisvų laikų sistemos nėra, todėl čia — tikras darbo laikas
        # ir kelias į paslaugas, o ne išgalvoti laikai.
        cipsai = []
        if i.ar_atidaryta():
            cipsai.append({'tekstas': '%s %s–%s' % (_('Šiandien'),
                                                    i.laikas(_siandien())[0],
                                                    i.uzsidaro()),
                           'ghost': False,
                           'url': i.get_absolute_url() + '#paslaugos'})
        elif i.atidaro():
            cipsai.append({'tekstas': '%s %s' % (_('Atidaro'), i.atidaro()),
                           'ghost': False,
                           'url': i.get_absolute_url() + '#paslaugos'})
        cipsai.append({'tekstas': str(_('Žiūrėti paslaugas')), 'ghost': True,
                       'url': i.get_absolute_url() + '#paslaugos'})

    return {
        'id': i.pk,
        'vardas': i.rodomas_vardas(),
        'tipas': i.rodomas_tipas(),
        'vietove': i.vietove(),
        'meistras': i.tipas == Imone.MEISTRAS,
        'reitingas': float(i.reitingas) if i.reitingas else None,
        'atsiliepimai': i.atsiliepimu_kiekis,
        'img': nuotrauka.nuotrauka.url if nuotrauka else '',
        'lat': float(i.latitude) if i.latitude else None,
        'lng': float(i.longitude) if i.longitude else None,
        'url': i.get_absolute_url(),
        'paslauga': paslauga,
        'kaina': kaina,
        'trukme': trukme,
        'cipsai': cipsai,
    }


def _siandien():
    from django.utils import timezone
    return timezone.localtime().weekday()


def _pigiausia(imone):
    """„nuo 4 900 €" — pigiausias prekiautojo skelbimas."""
    from apps.listings.views import _public_listings_qs
    if not imone.savininkas_id:
        return ''
    eil = (_public_listings_qs(None).filter(seller_id=imone.savininkas_id)
           .exclude(price=None).order_by('price').values_list('price', flat=True).first())
    return (_('nuo %(kaina)s') % {'kaina': formatai.kaina(eil)}) if eil else ''


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
