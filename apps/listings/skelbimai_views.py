# -*- coding: utf-8 -*-
"""
VISI SKELBIMAI — /skelbimai/

Vienas sąrašas iš visų kategorijų. Skelbimai gyvena dviejuose modeliuose:
`Listing` (automobiliai, motociklai, dalys, apranga…) ir `WheelListing`
(ratlankiai, padangos), todėl abu sujungiami į vieną sąrašą ir rikiuojami
kartu — kortelės pavidalą suvienodina apps/listings/korteles.py.

Kategorijų žymų juosta filtruoja tame pačiame puslapyje (?kategorija=),
rūšiavimas — ?rusiuoti=. Skaičius „Rasta skelbimų" skaičiuojamas iš tų
pačių užklausų, todėl visada sutampa su sąrašu.
"""

from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render
from django.utils.translation import gettext, gettext_lazy as _

from .korteles import kortele
from .models import Listing, SavedListing, VehicleType, WheelListing

# Rūšiavimo raktas -> (etiketė, Listing laukas, WheelListing laukas)
RUSIAVIMAS = {
    'naujausi':   (_('Naujausi'),      '-paskelbta_db', '-paskelbta_db'),
    'populiarus': (_('Populiariausi'), '-views_count',  '-views_count'),
    'brangiausi': (_('Brangiausi'),    '-price',        '-price'),
    'pigiausi':   (_('Pigiausi'),      'price',         'price'),
}

# Ratlankiai ir padangos yra atskiras modelis, todėl juostoje turi savo žymas
RATU_ZYMOS = {
    'padangos':   (_('Padangos'),   'tyre'),
    'ratlankiai': (_('Ratlankiai'), 'rim'),
}

PUSLAPYJE = 20


def _listing_qs():
    return Listing.objects.filter(
        status='active', is_shadow_banned=False,
    ).select_related('vehicle_type', 'brand', 'model', 'fuel_type', 'transmission') \
     .prefetch_related('images')


def _wheels_qs():
    return WheelListing.objects.filter(status='active').prefetch_related('images')


def _paskelbta(qs):
    from django.db.models.functions import Coalesce
    return qs.annotate(paskelbta_db=Coalesce('activated_at', 'created_at'))


def _zymos(listing_qs, wheels_qs, aktyvi):
    """Kategorijų juosta: tik tos kategorijos, kuriose skelbimų YRA."""
    kiekiai = {
        e['vehicle_type__slug']: e['n']
        for e in listing_qs.values('vehicle_type__slug').annotate(n=Count('id'))
    }

    zymos = [{'slug': '', 'label': _('Visi skelbimai'), 'kiek': None,
              'aktyvi': not aktyvi}]
    for vt in VehicleType.objects.all().order_by('name'):
        if kiekiai.get(vt.slug):
            # VehicleType.name DB'e angliškas — rodom per katalogą (kaip |tdb)
            zymos.append({'slug': vt.slug, 'label': gettext(vt.name),
                          'kiek': kiekiai[vt.slug], 'aktyvi': aktyvi == vt.slug})
    for slug, (label, tipas) in RATU_ZYMOS.items():
        kiek = wheels_qs.filter(product_type=tipas).count()
        if kiek:
            zymos.append({'slug': slug, 'label': label, 'kiek': kiek,
                          'aktyvi': aktyvi == slug})
    return zymos


def visi_skelbimai(request):
    rusiuoti = request.GET.get('rusiuoti') or 'naujausi'
    if rusiuoti not in RUSIAVIMAS:
        rusiuoti = 'naujausi'
    kategorija = (request.GET.get('kategorija') or '').strip()

    l_qs = _paskelbta(_listing_qs())
    w_qs = _paskelbta(_wheels_qs())

    zymos = _zymos(_listing_qs(), _wheels_qs(), kategorija)
    # Bendras skaičius — VISI aktyvūs skelbimai abiejuose modeliuose
    is_viso = _listing_qs().count() + _wheels_qs().count()

    if kategorija in RATU_ZYMOS:
        l_qs = l_qs.none()
        w_qs = w_qs.filter(product_type=RATU_ZYMOS[kategorija][1])
    elif kategorija:
        l_qs = l_qs.filter(vehicle_type__slug=kategorija)
        w_qs = w_qs.none()

    _e, l_laukas, w_laukas = RUSIAVIMAS[rusiuoti]
    irasai = list(l_qs.order_by(l_laukas)) + list(w_qs.order_by(w_laukas))

    # Sujungus du modelius rikiuojam Python'e — kitaip antrojo įrašai
    # nugultų sąrašo gale.
    if rusiuoti == 'naujausi':
        irasai.sort(key=lambda o: o.paskelbta, reverse=True)
    elif rusiuoti == 'populiarus':
        irasai.sort(key=lambda o: getattr(o, 'views_count', 0) or 0, reverse=True)
    else:
        irasai.sort(key=lambda o: o.price or 0, reverse=(rusiuoti == 'brangiausi'))

    rasta = len(irasai)
    puslapiai = Paginator(irasai, PUSLAPYJE)
    puslapis = puslapiai.get_page(request.GET.get('page'))

    issaugoti = set()
    if request.user.is_authenticated:
        issaugoti = set(SavedListing.objects.filter(
            user=request.user,
            listing__in=[o for o in puslapis if not isinstance(o, WheelListing)],
        ).values_list('listing_id', flat=True))

    korteles = [kortele(o, issaugotas=(o.pk in issaugoti and not isinstance(o, WheelListing)))
                for o in puslapis]

    params = request.GET.copy()
    params.pop('page', None)

    return render(request, 'listings/skelbimai.html', {
        'korteles': korteles,
        'puslapis': puslapis,
        'rasta': rasta,
        'is_viso': is_viso,
        'zymos': zymos,
        'kategorija': kategorija,
        'rusiuoti': rusiuoti,
        'rusiavimas': [(k, v[0]) for k, v in RUSIAVIMAS.items()],
        'params': params.urlencode(),
    })
