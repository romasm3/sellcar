# apps/listings/select_views.py
# ═══════════════════════════════════════════════════════════
# DRILL-IN PUSLAPIS — /pasirinkti/
#
# Telefone filtro reikšmė renkama atskirame puslapyje, ne sluoksnyje.
# Taip veikia etalonas (/select/?type=…) ir taip veikia naršyklės
# „atgal" mygtukas. Papildomas laimėjimas: reikšmių sąrašų nebereikia
# antrą kartą renderinti pagrindiniame puslapyje.
#
#     /pasirinkti/?laukas=<param>&kategorija=<slug>&grizti=<path+query>
#
# Lauko tipo parametro nėra — jis paimamas iš konfigūracijos pagal
# lauką ir kategoriją. Kaskadai naudojamas ?zingsnis=1|2.
# ═══════════════════════════════════════════════════════════
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from django.http import Http404
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import gettext as _

from .search_config import panels as panel_config


def _safe_return(request, raw):
    """Grįžimo kelias tik savo svetainėje — kitaip atviras peradresavimas."""
    fallback = '/'
    if not raw:
        return fallback
    if not url_has_allowed_host_and_scheme(raw, allowed_hosts={request.get_host()},
                                           require_https=request.is_secure()):
        return fallback
    return raw


def _find_field(category, param, sub_slug=None):
    """Lauko aprašas iš konfigūracijos — pirma panelė, tada išplėstinė."""
    for builder in (panel_config.build_panel, panel_config.build_advanced):
        cfg = builder(category, None, sub_slug=sub_slug)
        if not cfg:
            continue
        for row in cfg.get('rows') or []:
            for f in row:
                if not f:
                    continue
                if param in (f.get('param'), f.get('param_min'), f.get('param_max')):
                    return f
    return None


def _with_params(path, changes):
    """Grąžina tą patį kelią su pakeistais/pridėtais parametrais."""
    parts = urlparse(path)
    params = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True)
              if k not in changes]
    for key, value in changes.items():
        if value not in ('', None):
            params.append((key, value))
    return urlunparse(parts._replace(query=urlencode(params)))


def select_value(request):
    """Reikšmės pasirinkimo ekranas."""
    param = (request.GET.get('laukas') or '').strip()
    category = (request.GET.get('kategorija') or '').strip()
    sub_slug = (request.GET.get('sub') or '').strip() or None
    back = _safe_return(request, request.GET.get('grizti'))

    field = _find_field(category, param, sub_slug)
    if not field:
        raise Http404('Nežinomas laukas')

    # Pasirinkta reikšmė — grįžtam į tą pačią vietą su pakeistu parametru
    if 'reiksme' in request.GET:
        return redirect(_with_params(back, {param: request.GET['reiksme']}) + '#sp-target')

    current = dict(parse_qsl(urlparse(back).query, keep_blank_values=True)).get(param, '')

    if field.get('widget') == 'brand':
        options = ([(b['value'], b['name'], b['count']) for b in field.get('brands_top', [])]
                   + [(b['value'], b['name'], b['count']) for b in field.get('brands_rest', [])])
    elif field['type'] == 'range':
        source = (field.get('options_min') if param == field.get('param_min')
                  else field.get('options_max')) or []
        options = [(v, l, 0) for v, l in source]
    else:
        options = [(v, l, 0) for v, l in (field.get('options') or [])]

    return render(request, 'listings/select_value.html', {
        'field': field,
        'param': param,
        'category': category,
        'sub_slug': sub_slug,
        'back': back,
        'current': current,
        'options': options,
        'title': field['label'],
        'clear_url': _with_params(back, {param: ''}) + '#sp-target',
    })
