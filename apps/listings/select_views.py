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


def _with_params(path, changes, append=False):
    """Tas pats kelias su pakeistais (arba pridėtais) parametrais.

    ``append=True`` palieka esamas to paties vardo reikšmes — taip
    kaupiamos kelios markės, modeliai ar kuro tipai (variklis jas ima per
    getlist). Ta pati reikšmė antrą kartą nepridedama: kitaip du kartus
    pasirinkta „Audi" atsirastų adrese dukart ir žymų būtų dvi.
    """
    parts = urlparse(path)
    existing = parse_qsl(parts.query, keep_blank_values=True)
    params = existing if append else [(k, v) for k, v in existing if k not in changes]
    for key, value in changes.items():
        if value in ('', None):
            continue
        if append and (key, str(value)) in [(k, str(v)) for k, v in params]:
            continue
        params.append((key, value))
    return urlunparse(parts._replace(query=urlencode(params)))


def _model_param(category, sub_slug=None):
    """Kurio lauko vardu saugomas modelis šioje kategorijoje."""
    for builder in (panel_config.build_panel, panel_config.build_advanced):
        cfg = builder(category, None, sub_slug=sub_slug)
        if not cfg:
            continue
        for row in cfg.get('rows') or []:
            for f in row:
                if f and f.get('db_field') == 'model':
                    return f.get('param')
    return None


def _brand_has_models(field):
    """Ar markei rodoma modelių kaskada (kaip autogide — tik ten, kur
    modelių duomenų yra)."""
    from apps.listings import brands as brand_source

    scope = field.get('scope')
    if scope:
        return brand_source.has_models(scope)
    return False


def select_value(request):
    """Reikšmės pasirinkimo ekranas."""
    param = (request.GET.get('laukas') or '').strip()
    category = (request.GET.get('kategorija') or '').strip()
    sub_slug = (request.GET.get('sub') or '').strip() or None
    back = _safe_return(request, request.GET.get('grizti'))

    field = _find_field(category, param, sub_slug)
    if not field:
        raise Http404('Nežinomas laukas')

    cascade = field.get('widget') == 'brand' and _brand_has_models(field)
    step = request.GET.get('zingsnis') or '1'
    chosen_brand = request.GET.get('marke') or ''

    # ── Pasirinkta reikšmė ────────────────────────────────────────────
    if 'reiksme' in request.GET:
        value = request.GET['reiksme']

        # Markė kaskadoje — dar ne pabaiga: einam į modelių žingsnį
        if cascade and step == '1':
            return redirect(_with_params(request.get_full_path(), {
                'zingsnis': '2', 'marke': value, 'reiksme': None,
            }))

        if cascade and step == '2':
            # Pora kaupiama: markė + modelis pridedami prie esamų
            changes = {param: chosen_brand}
            model_param = _model_param(category, sub_slug)
            if model_param and value:
                changes[model_param] = value
            return redirect(_with_params(back, changes, append=True) + '#sp-target')

        # Diapazonas — ekrane abi ribos, tad po „Nuo" LIEKAM čia: kitaip
        # „Iki" nurodyti reikėtų grįžti ir vėl atidaryti tą pačią eilutę.
        # Pasirinkimas įrašomas į grįžimo adresą, o į panelę veda ‹ ir
        # „Gerai".
        if field['type'] == 'range':
            return redirect(_with_params(request.get_full_path(), {
                'grizti': _with_params(back, {param: value}),
                'laukas': field.get('param_min') or param,
                'reiksme': None,
            }))

        # Daugybiniai laukai (kuro tipas, kėbulas, markė be modelių...)
        # kaupia reikšmes — telefone jas rodo atskiros žymos, o „+" šalia
        # jų kviečia būtent šį ekraną. Vienareikšmiai — perrašo.
        daugybinis = field.get('type') == 'multiselect' or field.get('widget') == 'brand'
        return redirect(_with_params(back, {param: value}, append=daugybinis)
                        + '#sp-target')

    # ── Modelių žingsnis ──────────────────────────────────────────────
    if cascade and step == '2' and chosen_brand:
        from apps.listings.models import Brand, Model

        brand = Brand.objects.filter(pk=chosen_brand).first() if str(chosen_brand).isdigit() else None
        models = (Model.objects.filter(brand=brand).order_by('name')
                  if brand else Model.objects.none())
        return render(request, 'listings/select_value.html', {
            'field': field, 'param': param, 'category': category, 'sub_slug': sub_slug,
            'back': back, 'current': '', 'step': '2', 'chosen_brand': chosen_brand,
            'options': [(m.id, m.name, 0) for m in models],
            'rodyti_kiekius': False,
            'title': brand.name if brand else field['label'],
            # „Visi modeliai" — grįžtam tik su marke
            'clear_url': _with_params(back, {param: chosen_brand}, append=True) + '#sp-target',
            'clear_label': _('Visi modeliai'),
            'back_link': _with_params(request.get_full_path(),
                                      {'zingsnis': None, 'marke': None}),
        })

    esami = dict(parse_qsl(urlparse(back).query, keep_blank_values=True))
    current = esami.get(param, '')
    columns = None
    # Skelbimų kiekiai yra tik markių sąraše (brand_api). Kitur jų nėra,
    # o „(0)" prie kiekvienos kainos ar metų atrodė, lyg eilutė būtų
    # neaktyvi — todėl ten kiekių nerodom visai.
    rodyti_kiekius = field.get('widget') == 'brand'

    if field.get('widget') == 'brand':
        # Tas pats šaltinis kaip /ajax/markes/ — sąrašas kešuotas, o į
        # HTML jis nebededamas iš anksto (žr. brand_api.py). Šis puslapis
        # renderinamas serveryje, todėl paiešką filtruoja irgi serveris.
        from apps.listings.brand_api import brand_items
        q = (request.GET.get('q') or '').strip().lower()
        items = brand_items(category, sub_slug) or []
        if q:
            items = [it for it in items if q in it['n'].lower()]
        options = [(it['v'], it['n'], it['c']) for it in items]
    elif field['type'] == 'range':
        # Diapazonas — ABI ribos viename ekrane, kaip etalono
        # „ddvaluedouble" (docs/mobilus-etalonas.md). Iki šiol eilutė vedė
        # tik į „Nuo", tad viršutinės ribos telefone nebuvo kaip nurodyti.
        options = []
        columns = []
        for riba, etikete, source in (
                (field.get('param_min'), _('Nuo'), field.get('options_min')),
                (field.get('param_max'), _('Iki'), field.get('options_max'))):
            if not riba:
                continue
            columns.append({
                'param': riba,
                'label': etikete,
                'current': esami.get(riba, ''),
                'options': [(v, l) for v, l in (source or [])],
                'clear_url': _with_params(back, {riba: ''}) + '#sp-target',
            })
    else:
        options = [(v, l, 0) for v, l in (field.get('options') or [])]

    # „Visi" diapazone valo abi ribas iš karto
    if columns:
        clear_url = _with_params(
            back, {c['param']: '' for c in columns}) + '#sp-target'
    else:
        clear_url = _with_params(back, {param: ''}) + '#sp-target'

    return render(request, 'listings/select_value.html', {
        'field': field,
        'param': param,
        'category': category,
        'sub_slug': sub_slug,
        'back': back,
        'current': current,
        'options': options,
        'columns': columns,
        'rodyti_kiekius': rodyti_kiekius,
        'title': _('Markė, modelis') if cascade else field['label'],
        'step': '1',
        'clear_url': clear_url,
        'clear_label': _('Visi'),
        'back_link': back + '#sp-target',
        'cascade': cascade,
    })
