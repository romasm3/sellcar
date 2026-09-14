# -*- coding: utf-8 -*-
"""Valiutos simbolis šablonams — žr. apps/listings/valiutos.py."""
from django import template

from apps.listings import valiutos

register = template.Library()


@register.simple_tag
def valiutos_simbolis(salies_kodas):
    """Šalies kodas → valiutos simbolis („LT" → „€").

    Naudojam formose, kur kainos sufiksas turi atitikti pasirinktą šalį.
    Pačiuose skelbimuose imam `listing.currency_symbol` — ten valiuta jau
    įrašyta.
    """
    return valiutos.simbolis_pagal_sali(salies_kodas)


@register.simple_tag
def valiutos_kodas(salies_kodas):
    return valiutos.pagal_sali(salies_kodas)


@register.simple_tag
def valiutu_zemelapis_json():
    """Ką naršyklei reikia žinoti apie valiutą — žr. static/js/valiuta.js.

    Anksčiau čia keliavo visas {šalis: valiuta} žemėlapis ir visų valiutų
    simboliai, nes JS sufiksą keitė pagal pasirinktą šalį. Sąsaja
    pašalinta (valiuta visada EUR), tad nebesiunčiam ir sąrašo — kitaip
    „zł", „kr", „CHF" gulėtų kiekvieno puslapio kode be jokio tikslo.
    """
    import json

    from django.utils.safestring import mark_safe
    return mark_safe(json.dumps({
        'numatyta': valiutos.NUMATYTA,
        'simboliai': {valiutos.NUMATYTA: valiutos.simbolis(valiutos.NUMATYTA)},
    }, ensure_ascii=False))
