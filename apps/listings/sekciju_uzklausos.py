# -*- coding: utf-8 -*-
"""
VIENA UŽKLAUSA SEKCIJAI — sąrašui, skaitliukui ir meniu.

Klaida, dėl kurios šitas modulis atsirado: panelės mygtuko skaičių ir
tikrąjį /browse/<sekcija>/ sąrašą skaičiavo DVI skirtingos užklausos.
Kol jos sutapdavo, niekas nepastebėdavo; išsiskyrus — mygtukas rodydavo
0, o sąrašas tą patį skelbimą rasdavo:

  /?section=motogear     → „Skelbimai 0"
  /browse/motogear/      → „Rastas 1 skelbimas"

O „Padangos motociklams" ir „Padangos keturračiams" skaitliuko išvis
neturėjo: /paieska/count/moto-tyres/ grąžindavo 404, naršyklė klaidą
nurydavo (`catch`), ir mygtuke likdavo 0.

Nuo šiol kiekviena sekcija turi vieną funkciją, kuri grąžina TĄ PATĮ
queryset'ą, kurį rodo naršymo puslapis. Ja remiasi:

  • `views.search_panel_count`  — panelės mygtukas,
  • `meniu_kiekiai.kiekiai()`   — visi meniu skaičiai,
  • `manage.py tikrinti_meniu`  — patikra.

Naršymo puslapiai kviečia tas pačias filtrų funkcijas
(`filter_listings`, `_apply_wheels_filters`, `parts_count_qs`,
`motogear_views.taikyk_filtrus`), todėl kelias tikrai vienas, o ne du
panašūs.
"""


class _Uzklausa:
    """Minimalus `request` pakaitalas: wheels filtrai laukia objekto su
    `.GET` ir `.user`, o mes turim tik parametrus."""

    def __init__(self, params, user):
        self.GET = params
        self.user = user


def _tuscia(params):
    from django.http import QueryDict
    return params if params is not None else QueryDict('')


# Sekcijos, kurios gyvena WheelListing lentelėje: (product_type, purpose).
# `atv`, ne `quad` — taip vadinasi reikšmė modelyje
# (models.WHEEL_PURPOSE_CHOICES). Dėl „quad" skaitliukai ir juostos
# nuorodos rodė 0, nors keturračių padangų yra.
RATU_SEKCIJOS = {
    'tires':      ('tyre', None),
    'tyres':      ('tyre', None),
    'wheels':     ('tyre', None),
    'rims':       ('rim', None),
    'moto-tyres': ('tyre', 'moto'),
    'quad-tyres': ('tyre', 'atv'),
}


def uzklausa(sekcija, params=None, user=None):
    """Queryset, kurį sekcijai rodo jos naršymo puslapis.

    Nežinoma sekcija → None (kvietėjas nusprendžia, ar tai 404).
    """
    from django.http import QueryDict

    params = _tuscia(params)

    # ─── Ratai (atskira lentelė) ───
    if sekcija in RATU_SEKCIJOS:
        from . import wheels_views
        tipas, paskirtis = RATU_SEKCIJOS[sekcija]
        if hasattr(params, 'copy'):
            p = params.copy()
        else:
            p = QueryDict('', mutable=True)
            p.update(params or {})
        if paskirtis:
            p['purpose'] = paskirtis          # sekcija nusako paskirtį
        if tipas == 'rim' or p.get('type') == 'rim':
            tipas = 'rim'
        qs, _t, _f = wheels_views._apply_wheels_filters(_Uzklausa(p, user), tipas)
        return qs

    # ─── Moto apranga ───
    if sekcija == 'motogear':
        from . import motogear_views
        return motogear_views.taikyk_filtrus(
            motogear_views._moto_gear_public_qs(user), params)

    # ─── Dalys: penkios subkategorijos ───
    from .search_panel import COUNT_KEY_TO_SUB, parts_count_qs
    if sekcija in COUNT_KEY_TO_SUB and not params.get('advanced'):
        return parts_count_qs(COUNT_KEY_TO_SUB[sekcija], params, user=user)

    # ─── Visa kita — bendras Listing filtras ───
    from .views import (MOTO_GEAR_SLUGS, SEARCH_PANEL_CATEGORIES,
                        filter_listings, panel_config)
    if sekcija in SEARCH_PANEL_CATEGORIES or panel_config.advanced_is_active(sekcija):
        qs = filter_listings(params, user=user, category=sekcija)
        if sekcija == 'motorcycles' and not params.get('subcategory'):
            # Apranga gyvena po „motorcycles" tipu, bet visur yra atskira
            # kategorija: savo punktas meniu, sava panelė, savas
            # /browse/motogear/. Palikta motociklų sąraše ji būtų
            # suskaičiuota dukart, o „Motociklai" rodytų šalmus.
            qs = qs.exclude(subcategory__slug__in=list(MOTO_GEAR_SLUGS))
        return qs

    return None


def kiek(sekcija, params=None, user=None):
    """Kiek skelbimų sekcijoje. Nežinoma sekcija → 0."""
    qs = uzklausa(sekcija, params, user)
    return qs.count() if qs is not None else 0
