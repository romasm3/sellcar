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
    """Žemėlapis naršyklei — kad sufiksas atsinaujintų pakeitus šalį."""
    import json

    from django.utils.safestring import mark_safe
    return mark_safe(json.dumps({
        'salys': valiutos.zemelapis(),
        'numatyta': valiutos.NUMATYTA,
        'simboliai': valiutos.SIMBOLIAI,
    }, ensure_ascii=False))
