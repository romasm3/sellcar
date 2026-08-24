# -*- coding: utf-8 -*-
"""
PERŽIŪRĖTI SKELBIMAI — /perziureti/

Kas kur gyvena:
  • prisijungusiam — PerziuretasSkelbimas įrašai paskyroje (žymimi
    atidarius skelbimo puslapį, views.listing_detail);
  • svečiui — sąrašas naršyklėje (localStorage), o korteles jam
    atiduoda `perziureti_duomenys` pagal atsiųstus id;
  • prisijungus svečio sąrašas perkeliamas į paskyrą
    (`perziureti_sujungti`), tada naršyklės sąrašas išvalomas.

Tas pats šaltinis maitina ir „Žiūrėjote" ženkliuką rezultatų kortelėse
(static/js/perziureti.js).
"""

import json

from django.utils.dateparse import parse_datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from .korteles import kortele
from .models import Listing, PerziuretasSkelbimas


RUSIAVIMAS = {
    'naujausi': ('-perziureta', _('Naujausi')),
    'seniausi': ('perziureta', _('Seniausi')),
    'pigiausi': ('listing__price', _('Pigiausi')),
    'brangiausi': ('-listing__price', _('Brangiausi')),
}


def _matomi(qs):
    """Tik tie skelbimai, kuriuos svečias gali atsidaryti."""
    return qs.filter(
        Q(listing__status='active') | Q(listing__status='sold'),
        listing__is_shadow_banned=False,
    )


def _kategoriju_sarasas(irasai):
    """Kategorijos, kurios realiai yra sąraše — filtrui."""
    matyti = []
    for i in irasai:
        vt = i.listing.vehicle_type if hasattr(i, 'listing') else i.vehicle_type
        if vt and vt.slug not in [k['slug'] for k in matyti]:
            matyti.append({'slug': vt.slug, 'label': vt.name})
    return matyti


def perziureti_skelbimai(request):
    """Puslapis. Prisijungusiam turinys renderinamas iškart, svečiui —
    kortelės užkraunamos iš localStorage (perziureti.js)."""
    sort = request.GET.get('sort') or 'naujausi'
    if sort not in RUSIAVIMAS:
        sort = 'naujausi'
    kategorija = request.GET.get('kategorija') or ''

    korteles, kategorijos, kiek = [], [], 0
    if request.user.is_authenticated:
        qs = _matomi(
            PerziuretasSkelbimas.objects.filter(user=request.user)
            .select_related('listing', 'listing__vehicle_type', 'listing__brand',
                            'listing__model', 'listing__fuel_type',
                            'listing__transmission')
            .prefetch_related('listing__images')
        )
        visi = list(qs)
        kategorijos = _kategoriju_sarasas(visi)
        if kategorija:
            qs = qs.filter(listing__vehicle_type__slug=kategorija)
        korteles = list(qs.order_by(RUSIAVIMAS[sort][0]))
        kiek = len(korteles)

    return render(request, 'listings/perziureti.html', {
        'korteles': [kortele(i.listing, perziureta=i.perziureta) for i in korteles],
        'kiek': kiek,
        'kategorijos': kategorijos,
        'kategorija': kategorija,
        'sort': sort,
        'rusiavimas': [(k, v[1]) for k, v in RUSIAVIMAS.items()],
        'svecias': not request.user.is_authenticated,
    })


@require_POST
def perziureti_duomenys(request):
    """Svečio kortelės: JSON {ids: [...], laikai: {id: ISO}, kategorija, sort}.

    Grąžina paruoštą HTML — kad kortelė būtų viena ir ta pati kaip
    prisijungusiam (partials/_skelbimo_kortele.html).
    """
    try:
        duom = json.loads(request.body or '{}')
    except ValueError:
        return HttpResponseBadRequest('blogas JSON')

    ids = [int(i) for i in (duom.get('ids') or [])[:PerziuretasSkelbimas.RIBA]
           if str(i).isdigit()]
    laikai = duom.get('laikai') or {}
    sort = duom.get('sort') if duom.get('sort') in RUSIAVIMAS else 'naujausi'
    kategorija = duom.get('kategorija') or ''

    qs = Listing.objects.filter(pk__in=ids, is_shadow_banned=False).filter(
        Q(status='active') | Q(status='sold')
    ).select_related('vehicle_type', 'brand', 'model', 'fuel_type',
                     'transmission').prefetch_related('images')
    pagal_id = {l.pk: l for l in qs}

    irasai = []
    for i in ids:
        l = pagal_id.get(i)
        if not l:
            continue
        if kategorija and (not l.vehicle_type or l.vehicle_type.slug != kategorija):
            continue
        kada = parse_datetime(str(laikai.get(str(i)) or '')) or timezone.now()
        if timezone.is_naive(kada):
            kada = timezone.make_aware(kada)
        irasai.append({'listing': l, 'perziureta': kada})

    if sort == 'seniausi':
        irasai.reverse()
    elif sort == 'pigiausi':
        irasai.sort(key=lambda x: x['listing'].price or 0)
    elif sort == 'brangiausi':
        irasai.sort(key=lambda x: x['listing'].price or 0, reverse=True)

    html = render_to_string(
        'listings/partials/_perziuretu_sarasas.html',
        {'korteles': [kortele(x['listing'], perziureta=x['perziureta']) for x in irasai]},
        request=request)
    kategorijos = _kategoriju_sarasas([pagal_id[i] for i in ids if i in pagal_id])
    return JsonResponse({'html': html, 'kiek': len(irasai),
                         'kategorijos': kategorijos})


@require_POST
@login_required
def perziureti_pasalinti(request, pk):
    """✕ — išima skelbimą iš peržiūrėtų."""
    PerziuretasSkelbimas.objects.filter(user=request.user, listing_id=pk).delete()
    kiek = _matomi(PerziuretasSkelbimas.objects.filter(user=request.user)).count()
    return JsonResponse({'ok': True, 'kiek': kiek})


@require_POST
@login_required
def perziureti_sujungti(request):
    """Svečio sąrašas iš localStorage → paskyra (po prisijungimo).

    Laikai imami iš naršyklės, bet jei skelbimas paskyroje jau yra su
    vėlesniu laiku — paliekamas vėlesnis.
    """
    try:
        duom = json.loads(request.body or '{}')
    except ValueError:
        return HttpResponseBadRequest('blogas JSON')

    laikai = duom.get('laikai') or {}
    ids = [int(i) for i in (duom.get('ids') or [])[:PerziuretasSkelbimas.RIBA]
           if str(i).isdigit()]
    esami = Listing.objects.filter(pk__in=ids).in_bulk()

    for i in ids:
        l = esami.get(i)
        if not l:
            continue
        kada = parse_datetime(str(laikai.get(str(i)) or '')) or timezone.now()
        if timezone.is_naive(kada):
            kada = timezone.make_aware(kada)
        turimas = PerziuretasSkelbimas.objects.filter(
            user=request.user, listing=l).first()
        if turimas and turimas.perziureta >= kada:
            continue
        PerziuretasSkelbimas.zymeti(request.user, l, kada=kada)

    kiek = PerziuretasSkelbimas.objects.filter(user=request.user).count()
    return JsonResponse({'ok': True, 'kiek': kiek})


def perziuretu_id(request):
    """Ženkliukui „Žiūrėjote" — prisijungusio peržiūrėtų skelbimų id."""
    if not request.user.is_authenticated:
        return JsonResponse({'ids': []})
    ids = list(PerziuretasSkelbimas.objects.filter(user=request.user)
               .values_list('listing_id', flat=True)[:PerziuretasSkelbimas.RIBA])
    return JsonResponse({'ids': ids})
