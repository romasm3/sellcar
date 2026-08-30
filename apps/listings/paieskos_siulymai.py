# -*- coding: utf-8 -*-
"""
PAGRINDINĖS PAIEŠKOS SIŪLYMAI — /ajax/paieska/

Vienas galas, grąžinantis sugrupuotus rezultatus juostai pradžios
puslapyje: markės ir modeliai, skelbimai, įmonės, vietos.

Šaltiniai — tie patys, kuriuos naudoja visa svetainė:
  markės/modeliai  brand_api (Brand + scopes iš panelių konfigūracijos)
  skelbimai        views._public_listings_qs
  įmonės           apps.imones.models.Imone (tik patvirtintos)
  vietos           miestai iš tų pačių skelbimų

Nuorodos veda ten, kur parametrus supranta atrankos variklis: markė ir
modelis — į rezultatų puslapį su `brand`/`model` (ne `make=`, kurio
filter_listings neskaito), vieta — į žemėlapio paiešką su `city`.
"""

from django.db.models import Count, Q
from django.http import JsonResponse
from django.utils.translation import gettext as _
from django.views.decorators.http import require_GET

EILUCIU = 4          # kiek eilučių viename bloke
MARKIU_RIBA = 6      # populiariausios markės, kai dar nieko neįvesta


def _markes(q, kiek=EILUCIU):
    from apps.listings.brand_api import visos_markes

    q = q.lower()
    rasta = [m for m in visos_markes() if q in m['n'].lower()]
    # Pirma tos, kurios turi skelbimų, tada pagal vardą
    rasta.sort(key=lambda m: (-m['c'], m['n'].lower()))
    return [{
        'tipas': 'marke',
        'vardas': m['n'],
        'kiek': m['c'],
        'url': '/?category=%s&%s=%s&sidebar=1' % (m['k'], m.get('p') or 'brand', m['v']),
    } for m in rasta[:kiek]]


def _modeliai(q, kiek=EILUCIU):
    """„BMW 320d" — modelis kartu su markės vardu."""
    from apps.listings.models import Listing, Model

    if len(q) < 2:
        return []
    eilutes = (Model.objects.filter(name__icontains=q)
               .select_related('brand')[:kiek * 3])
    kiekiai = dict(Listing.objects.filter(model__in=eilutes)
                   .values_list('model_id').annotate(n=Count('id')))
    isvestis = []
    for m in eilutes:
        isvestis.append({
            'tipas': 'modelis',
            'vardas': ('%s %s' % (m.brand.name if m.brand_id else '', m.name)).strip(),
            'kiek': kiekiai.get(m.pk, 0),
            'url': '/?category=cars&brand=%s&model=%s&sidebar=1' % (m.brand_id, m.pk),
        })
    isvestis.sort(key=lambda x: -x['kiek'])
    return isvestis[:kiek]


def _skelbimai(q, user, kiek=EILUCIU):
    from apps.listings import formatai
    from apps.listings.templatetags.listing_filters import vietovardis
    from apps.listings.views import _public_listings_qs

    SIMB = {'EUR': '€', 'USD': '$', 'GBP': '£'}
    eilutes = (_public_listings_qs(user).filter(title__icontains=q)
               .prefetch_related('images')[:kiek])
    isvestis = []
    for l in eilutes:
        nuotrauka = l.first_image
        isvestis.append({
            'tipas': 'skelbimas',
            'vardas': l.title,
            'kaina': formatai.kaina(l.price, SIMB.get(l.currency, '€')) if l.price else '',
            'vieta': vietovardis(l.city) if l.city and l.city != '—' else '',
            'img': nuotrauka.image.url if nuotrauka and nuotrauka.image else '',
            'url': '/%s/' % l.pk,
        })
    return isvestis


def _imones_nuotrauka(i):
    """Logotipas, o jei jo nėra — pirma įmonės nuotrauka."""
    if i.logotipas:
        return i.logotipas.url
    pirma = i.nuotraukos.first()
    return pirma.failas.url if pirma and pirma.failas else ''


def _imones_eilute(i):
    """Viena įmonės/meistro eilutė: nuotrauka, vardas, vieta, reitingas."""
    return {
        'tipas': 'meistras' if i.tipas == i.MEISTRAS else 'imone',
        'vardas': i.rodomas_vardas(),
        'apie': i.rodomas_tipas(),
        'vieta': i.vietove(),
        'img': _imones_nuotrauka(i),
        'reitingas': float(i.reitingas) if i.reitingas else 0,
        'url': i.get_absolute_url(),
    }


def _imones(q, kiek=EILUCIU):
    try:
        from apps.imones.models import Imone
    except Exception:
        return []
    eilutes = Imone.objects.filter(patvirtinta=True, tipas__in=Imone.IMONIU_TIPAI)
    if q:
        eilutes = eilutes.filter(Q(pavadinimas__icontains=q) | Q(miestas__icontains=q))
    return [_imones_eilute(i) for i in eilutes[:kiek]]


def _meistrai(q, kiek=EILUCIU):
    """Meistrai — atskira grupė, kaip etalone."""
    try:
        from apps.imones.models import Imone
    except Exception:
        return []
    eilutes = Imone.objects.filter(patvirtinta=True, tipas=Imone.MEISTRAS)
    if q:
        eilutes = eilutes.filter(Q(meistras_vardas__icontains=q)
                                 | Q(pavadinimas__icontains=q)
                                 | Q(specializacija__icontains=q)
                                 | Q(miestas__icontains=q))
    return [_imones_eilute(i) for i in eilutes[:kiek]]


def _vietos(q, user, kiek=EILUCIU):
    from apps.listings.templatetags.listing_filters import vietovardis
    from apps.listings.views import _public_listings_qs

    eilutes = (_public_listings_qs(user).filter(city__icontains=q)
               .exclude(city='').exclude(city='—')
               .values('city').annotate(n=Count('id')).order_by('-n')[:kiek])
    return [{
        'tipas': 'vieta',
        'vardas': vietovardis(e['city']),
        'kiek': e['n'],
        'url': '/map/?city=%s' % e['city'],
    } for e in eilutes]


def _populiarios(user, kiek=MARKIU_RIBA):
    """Kai dar nieko neįvesta — markės, kurios turi daugiausia skelbimų."""
    from apps.listings.brand_api import visos_markes

    turincios = [m for m in visos_markes() if m['c']]
    turincios.sort(key=lambda m: -m['c'])
    return [{
        'tipas': 'marke',
        'vardas': m['n'],
        'kiek': m['c'],
        'url': '/?category=%s&%s=%s&sidebar=1' % (m['k'], m.get('p') or 'brand', m['v']),
    } for m in turincios[:kiek]]


def _paslaugos(q, kiek=EILUCIU):
    """Veiklos sritys su įmonių skaičiumi — įmonių puslapio siūlymai."""
    try:
        from apps.imones.models import VeiklosSritis
    except Exception:
        return []
    eilutes = (VeiklosSritis.objects.filter(imones__patvirtinta=True)
               .annotate(kiek=Count('imones', distinct=True)))
    if q:
        eilutes = eilutes.filter(pavadinimas__icontains=q)
    eilutes = eilutes.order_by('-kiek', 'tvarka')[:kiek]
    # DB laikom trumpą vardą („fa-car-side"), o naršyklei duodam pilną
    # klasę — Font Awesome 6 be stiliaus klasės ženkliuko nepiešia.
    def klase(ikona):
        ikona = ikona or 'fa-screwdriver-wrench'
        return ikona if ikona.startswith('fa-solid') else 'fa-solid ' + ikona

    return [{
        'tipas': 'paslauga',
        'ikona': klase(v.ikona),
        'vardas': v.pavadinimas,
        'kiek_imoniu': v.kiek,
        'url': '/imones/?veikla=%s' % v.slug,
    } for v in eilutes]


def _imoniu_cipsai(q):
    """Juostelės su kiekiais: Visi · Paslaugos · Įmonės · Meistrai."""
    try:
        from apps.imones.models import Imone, VeiklosSritis
    except Exception:
        return []
    paslaugu = VeiklosSritis.objects.filter(imones__patvirtinta=True)
    imoniu = Imone.objects.filter(patvirtinta=True, tipas__in=Imone.IMONIU_TIPAI)
    meistru = Imone.objects.filter(patvirtinta=True, tipas=Imone.MEISTRAS)
    if q:
        paslaugu = paslaugu.filter(pavadinimas__icontains=q)
        imoniu = imoniu.filter(Q(pavadinimas__icontains=q) | Q(miestas__icontains=q))
        meistru = meistru.filter(Q(meistras_vardas__icontains=q)
                                 | Q(specializacija__icontains=q)
                                 | Q(miestas__icontains=q))
    return [
        {'raktas': 'visi', 'vardas': str(_('Visi'))},
        {'raktas': 'paslaugos', 'vardas': str(_('Paslaugos')),
         'kiek': paslaugu.distinct().count()},
        {'raktas': 'imones', 'vardas': str(_('Įmonės')), 'kiek': imoniu.count()},
        {'raktas': 'meistrai', 'vardas': str(_('Meistrai')), 'kiek': meistru.count()},
    ]


def _imoniu_siulymai(request, q, sritis='imoniu_puslapis'):
    """Įmonių puslapio sąrašas: paslaugos, įmonės ir meistrai — be markių.

    `tipas` — pasirinkta juostelė lango viršuje; „visi" rodo visas grupes.
    """
    tipas = (request.GET.get('tipas') or 'visi').strip()
    grupes = []

    def prideti(vardas, eilutes):
        if eilutes:
            grupes.append({'vardas': vardas, 'eilutes': eilutes})

    if sritis in ('imoniu_puslapis', 'paslaugos') and tipas in ('visi', 'paslaugos'):
        prideti(str(_('Paslaugos')), _paslaugos(q))
    if sritis in ('imoniu_puslapis', 'imones') and tipas in ('visi', 'imones'):
        prideti(str(_('Įmonės')), _imones(q))
    if sritis == 'imoniu_puslapis' and tipas in ('visi', 'meistrai'):
        prideti(str(_('Meistrai')), _meistrai(q))

    return JsonResponse({'q': q, 'paskutines': [],
                         'cipsai': _imoniu_cipsai(q), 'grupes': grupes})


@require_GET
def ajax_paieskos_siulymai(request):
    """GET /ajax/paieska/?q=<tekstas>&sritis=visi|markes|skelbimai|imones"""
    q = (request.GET.get('q') or '').strip()
    sritis = (request.GET.get('sritis') or 'visi').strip()

    # Įmonių puslapyje siūlom TIK paslaugas ir įmones — markių, modelių
    # ir skelbimų ten nėra ir nebus.
    if sritis in ('imoniu_puslapis', 'paslaugos', 'imones'):
        return _imoniu_siulymai(request, q, sritis)

    if len(q) < 2:
        # Tuščias laukas: paskutinės paieškos (sesija — veikia ir svečiui)
        # ir populiariausios markės.
        from apps.listings import search_history
        return JsonResponse({
            'q': q,
            'paskutines': [{
                'vardas': i.get('pavadinimas') or '',
                'url': '/?%s&sidebar=1' % i.get('params', ''),
            } for i in search_history.sarasas(request)[:4]],
            'grupes': [{'vardas': str(_('Populiariausios markės')),
                        'eilutes': _populiarios(request.user)}]
                      if _populiarios(request.user) else [],
        })

    grupes = []

    def prideti(vardas, eilutes):
        if eilutes:
            grupes.append({'vardas': vardas, 'eilutes': eilutes})

    if sritis in ('visi', 'markes'):
        prideti(str(_('Markės ir modeliai')),
                (_markes(q) + _modeliai(q))[:EILUCIU])
    if sritis in ('visi', 'skelbimai'):
        prideti(str(_('Skelbimai')), _skelbimai(q, request.user))
    if sritis in ('visi', 'imones'):
        prideti(str(_('Įmonės')), _imones(q))
    if sritis == 'visi':
        prideti(str(_('Vietos')), _vietos(q, request.user))

    return JsonResponse({'q': q, 'paskutines': [], 'grupes': grupes})
