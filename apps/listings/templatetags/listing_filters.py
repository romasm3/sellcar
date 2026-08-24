"""
Custom template filters for listings app.

Usage in templates:
    {% load listing_filters %}
    {% for y in "2024 2025 2026"|split:" " %}
        {{ y }}
    {% endfor %}
"""
from django import template

register = template.Library()


@register.filter(name='split')
def split_filter(value, delimiter=' '):
    """Split a string by delimiter. Default delimiter is space.

    Example:
        {{ "a,b,c"|split:"," }}  -> ['a', 'b', 'c']
        {{ "a b c"|split }}      -> ['a', 'b', 'c']
    """
    if value is None:
        return []
    return str(value).split(delimiter)


@register.filter(name='get_item')
def get_item(dictionary, key):
    """Get an item from a dict by key.

    Example:
        {{ my_dict|get_item:"somekey" }}
    """
    if dictionary is None:
        return None
    return dictionary.get(key) if hasattr(dictionary, 'get') else None


@register.filter(name='star_badge')
def star_badge(listing):
    """Return star emoji based on effective star level.

    Example:
        {{ listing|star_badge }}
    """
    if not hasattr(listing, 'get_effective_star_level'):
        return ''
    level = listing.get_effective_star_level()
    if level == 2:
        return '⭐⭐'
    if level == 1:
        return '⭐'
    return ''

# ═══════════════════════════════════════════════════════════════════
# SKAIČIŲ IR KAINŲ FORMATAS — logika viena, apps/listings/formatai.py
# ═══════════════════════════════════════════════════════════════════

from apps.listings import formatai

register.filter(name='sk')(formatai.sk)
register.filter(name='kaina')(formatai.kaina)


# ═══════════════════════════════════════════════════════════════════
# KORTELĖS SPECIFIKACIJŲ EILUTĖ
#
# Tušti laukai praleidžiami, skyriklis „ · ", todėl eilutė niekada
# neprasideda skyrikliu ir nelieka „, , sedanas". DB reikšmės (kuro
# tipas) verčiamos per katalogą — tas pats šaltinis kaip |tdb.
# ═══════════════════════════════════════════════════════════════════

from django.utils.translation import gettext


@register.simple_tag(name='spec_eilute')
def spec_eilute(listing):
    """„2.0 L · Benzinas / dujos · Sedanas"."""
    dalys = []

    if getattr(listing, 'is_truck', False) and getattr(listing, 'truck_type', ''):
        dalys.append(listing.get_truck_type_display())
    elif getattr(listing, 'engine_capacity', None):
        dalys.append('%s L' % listing.engine_capacity)

    kuras = getattr(listing, 'fuel_type', None)
    if kuras and getattr(kuras, 'name', ''):
        dalys.append(gettext(str(kuras.name)))

    if getattr(listing, 'body_type', ''):
        dalys.append(listing.get_body_type_display())

    return ' · '.join(d for d in dalys if d)


# ═══════════════════════════════════════════════════════════════════
# KATEGORIJŲ IKONOS — vienas žemėlapis visoms vietoms
#
# Šoninė juosta, kategorijų modalas, „…" sąrašai, pikeris (ir mobilus),
# tuščios būsenos vaizdas — visi ima ikoną iš čia. Nauja kategorija =
# viena eilutė šiame žodyne.
#
# Font Awesome 6.4 (įkeltas base.html). Spalvą paveldi iš tėvo, todėl
# akcentą valdo CSS, ne šis failas.
# ═══════════════════════════════════════════════════════════════════

from django.utils.html import format_html
from django.utils.safestring import mark_safe

KATEGORIJU_IKONOS = {
    'cars':                     'fa-car-side',
    'vans':                     'fa-van-shuttle',
    'motorcycles':              'fa-motorcycle',
    'motogear':                 'fa-shirt',
    'trucks':                   'fa-truck-moving',
    'truck-tractors':           'fa-truck-fast',
    'truck-carriers':           'fa-truck-ramp-box',
    'buses':                    'fa-bus',
    'municipal':                'fa-snowplow',
    'parts':                    'fa-screwdriver-wrench',
    'car-parts':                'fa-car-battery',
    'moto-parts':               'fa-oil-can',
    'truck-parts':              'fa-wrench',
    'agri-parts':               'fa-wheat-awn',
    'accessories':              'fa-gauge-high',
    'tuning':                   'fa-gauge-high',
    'boats':                    'fa-ship',
    'water-rental':             'fa-sailboat',
    'trailers':                 'fa-trailer',
    'construction':             'fa-person-digging',
    'construction-attachments': 'fa-toolbox',
    'agriculture':              'fa-tractor',
    'forestry':                 'fa-tree',
    'loading-equipment':        'fa-truck-ramp-box',
    'camping-houses':           'fa-caravan',
    'bicycles':                 'fa-person-biking',
    'services':                 'fa-handshake-angle',
    'rental':                   'fa-key',
    'car-rental':               'fa-key',
    'limo-rental':              'fa-champagne-glasses',
    'moto-rental':              'fa-helmet-safety',
    'truck-rental':             'fa-truck-ramp-box',
    'car-buying':               'fa-hand-holding-dollar',
    'electronics':              'fa-microchip',
    'planes':                   'fa-jet-fighter',
    'planes-parts':             'fa-plane-circle-check',
    'tractor-units':            'fa-truck-fast',
    'car-carriers':             'fa-truck-ramp-box',
    'robots':                   'fa-robot',
    'robots-parts':             'fa-robot',
    'drones':                   'fa-helicopter',
    'drones-parts':             'fa-microchip',
}

# Padangoms ir ratlankiams Font Awesome tinkamų formų neturi (fa-tire yra
# tik Pro rinkinyje), todėl jiems liko savos SVG formos.
_PADANGA = ('<svg class="{cls}" width="{d}" height="{d}" viewBox="0 0 24 24" fill="none" '
            'stroke="currentColor" stroke-width="4.2" aria-hidden="true">'
            '<circle cx="12" cy="12" r="8"/></svg>')
_RATLANKIS = ('<svg class="{cls}" width="{d}" height="{d}" viewBox="0 0 24 24" fill="none" '
              'stroke="currentColor" stroke-width="1.7" aria-hidden="true">'
              '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="2.6"/>'
              '<path stroke-linecap="round" d="M12 3v6.4M12 14.6V21M3 12h6.4M14.6 12H21'
              'M5.6 5.6l4.5 4.5M13.9 13.9l4.5 4.5M18.4 5.6l-4.5 4.5M10.1 13.9l-4.5 4.5"/></svg>')

SAVOS_FORMOS = {
    'tires': _PADANGA, 'tyres': _PADANGA, 'moto-tyres': _PADANGA, 'quad-tyres': _PADANGA,
    'rims': _RATLANKIS, 'wheels': _RATLANKIS,
}


# Kai kelios eilutės dalijasi tuo pačiu slug'u (pvz. „Autobusai" ir
# „Sunkvežimiai" abu yra `trucks`, skiriasi tik subkategorija), ikona
# parenkama pagal pavadinimą.
IKONOS_PAGAL_PAVADINIMA = {
    'Autobusai':                                    'fa-bus',
    'Komunalinio ūkio transportas':                 'fa-snowplow',
    'Vilkikai':                                     'fa-truck-fast',
    'Autotraukiniai, autovežiai':                   'fa-truck-ramp-box',
    'Automobilių nuoma':                            'fa-key',
    'Limuzinų, vestuvių transporto nuoma':          'fa-champagne-glasses',
    'Motociklų nuoma':                              'fa-helmet-safety',
    'Mikroautobusų, turistinio, vandens tr. nuoma': 'fa-sailboat',
    'Sunkiojo transporto, priekabų nuoma':          'fa-truck-ramp-box',
    'Statybinės technikos priedai':                 'fa-toolbox',
    'Automobilių supirkimas':                       'fa-hand-holding-dollar',
    'Video, audio, navigacijos':                    'fa-microchip',
    'Krovimo ir sandėliavimo technika':             'fa-truck-ramp-box',
    'Miško ūkio technika':                          'fa-tree',
    'Turistiniai nameliai':                         'fa-caravan',
    'Automobilių, mikroautobusų dalys':             'fa-car-battery',
    'Motociklų dalys':                              'fa-oil-can',
    'Sunkiojo transporto dalys':                    'fa-wrench',
    'Žemės ūkio, spec. dalys':                      'fa-wheat-awn',
    'Aksesuarai, Tuning':                           'fa-gauge-high',
    'Apranga, šalmai, aksesuarai':                  'fa-shirt',
}


@register.simple_tag(name='kategorijos_ikona')
def kategorijos_ikona(slug, dydis=22, cls='', pav=''):
    """<i class="fa-solid fa-car-side …"> arba SVG ratams.

    `pav` — kategorijos pavadinimas; naudojamas tik ten, kur to paties
    slug'o eilutės skiriasi (Sunkvežimiai / Autobusai / Vilkikai…).
    """
    raktas = (slug or '').strip()
    pagal_varda = IKONOS_PAGAL_PAVADINIMA.get((pav or '').strip())
    try:
        dydis = int(dydis)
    except (TypeError, ValueError):
        dydis = 22

    if raktas in SAVOS_FORMOS:
        return mark_safe(SAVOS_FORMOS[raktas].format(cls=cls, d=dydis))

    ikona = pagal_varda or KATEGORIJU_IKONOS.get(raktas, 'fa-car-side')
    return format_html(
        '<i class="fa-solid {} {}" style="font-size:{}px" aria-hidden="true"></i>',
        ikona, cls, dydis)
