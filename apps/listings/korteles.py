# -*- coding: utf-8 -*-
"""
Kortelės duomenys — vienas pavidalas visiems sąrašams.

Skelbimai gyvena dviejuose modeliuose (`Listing` ir `WheelListing`), o
kortelė turi atrodyti vienodai. Todėl vaizdai paverčia įrašus į vieną
žodyną, o šablonas (`partials/_skelbimo_kortele.html`) nebeturi šakų
„jei ratlankis…".

    korteles = [kortele(o) for o in objektai]
"""

from django.urls import reverse
from django.utils.translation import gettext

from .templatetags.listing_filters import spec_eilute, vietovardis


def _nuotrauka(objektas):
    nuotraukos = list(getattr(objektas, 'images').all()) if hasattr(objektas, 'images') else []
    return nuotraukos[0] if nuotraukos else None


def _ratlankio_spec(w):
    """„205/55 R16 · Vasarinės · 4 vnt." — ratlankių ir padangų eilutė."""
    dalys = []
    if w.product_type == 'tyre':
        matmuo = '/'.join(x for x in (w.tyre_width, w.tyre_profile) if x)
        if matmuo or w.diameter:
            dalys.append(' '.join(x for x in (matmuo, w.diameter) if x))
        if w.tyre_season:
            dalys.append(w.get_tyre_season_display())
    else:
        if w.diameter or w.rim_width:
            dalys.append(' '.join(x for x in (w.diameter, w.rim_width) if x))
        if w.rim_pcd:
            dalys.append(w.rim_pcd)
    if w.quantity:
        dalys.append('%s %s' % (w.quantity, gettext('vnt.')))
    return ' · '.join(d for d in dalys if d)


def kortele(objektas, perziureta=None, issaugotas=False):
    """Vienas įrašas -> kortelės žodynas."""
    ar_ratlankis = objektas.__class__.__name__ == 'WheelListing'

    if ar_ratlankis:
        url = objektas.get_absolute_url()
        spec = _ratlankio_spec(objektas)
        miestas = vietovardis(getattr(objektas, 'city', ''))
    else:
        url = reverse('listing_detail', args=[objektas.pk])
        spec = spec_eilute(objektas)
        miestas = vietovardis(objektas.city) if objektas.city and objektas.city != '—' else ''

    return {
        'obj': objektas,
        'pk': objektas.pk,
        'url': url,
        'img': _nuotrauka(objektas),
        'spec': spec,
        'miestas': miestas,
        'vin': getattr(objektas, 'vin', '') or '',
        'perziureta': perziureta,
        'issaugotas': issaugotas,
        'ratlankis': ar_ratlankis,
    }
