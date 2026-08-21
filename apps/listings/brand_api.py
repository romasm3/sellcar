"""Markių sąrašų galinis taškas — /ajax/markes/.

KODĖL: iki 2026-08-21 visų 18 kategorijų markių sąrašai buvo įdedami į
pagrindinio puslapio HTML iš karto — 11 295 `sp-dd-item` eilutės, 3,4 MB
iš 4,2 MB viso puslapio, 11 554 Alpine elementai ir 6,4 s trunkanti viena
JS užduotis. Sąrašas realiai reikalingas tik tada, kai vartotojas
atidaro iškrentantį lauką, todėl jis kraunamas tada.

VIENAS ŠALTINIS: tą patį atsakymą naudoja greitoji panelė, detali paieška,
rezultatų šoninė juosta ir mobilus /pasirinkti/ puslapis. Antro sąrašo
niekur nekuriame — jei markių logika keičiasi, keičiasi čia.

PAIEŠKA: `q` filtruoja serveryje (reikia /pasirinkti/ puslapiui, kuris
renderinamas be JS), bet iškrentantis laukas jos nenaudoja — jis vieną
kartą parsisiunčia visą kategorijos sąrašą ir filtruoja naršyklėje.
Ilgiausias sąrašas (žemės ūkis, 700 markių) suspaustas sveria ~6 KB,
todėl antras tinklo lakstymas kiekvienam raidės paspaudimui nieko
neduotų.

KEŠAS: serveryje `cache` 10 min (markės keičiasi retai — jas prideda
administratorius per BrandSuggestion patvirtinimą), naršyklėje
`Cache-Control: public, max-age=600` + ETag, kad pakartotinis atidarymas
neitų iki serverio.
"""

import hashlib
import json

from django.core.cache import cache
from django.http import JsonResponse, HttpResponseNotFound
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET

CACHE_SECONDS = 600
MAX_ITEMS = 2000


def _cache_key(vt_slug, sub_slug):
    return f'brandlist:v1:{vt_slug}:{sub_slug or "-"}'


def brand_items(vt_slug, sub_slug=None):
    """[{v, n, c}] — reikšmė, pavadinimas, skelbimų skaičius. Kešuojama.

    Skaičiai imami iš viešo skelbimų srauto (be prisijungusio vartotojo),
    nes kešas bendras visiems. Skaičius yra dekoracija — filtravimas per
    jį neina, todėl superadmino šešėliniai skelbimai jo neiškreipia
    kritiškai.
    """
    key = _cache_key(vt_slug, sub_slug)
    cached = cache.get(key)
    if cached is not None:
        return cached

    from apps.listings.search_config.panels import _brand_rows, _panel_cfg

    cfg = _panel_cfg(vt_slug, sub_slug)
    if not cfg:
        return None

    db_field = None
    for f in cfg.get('fields', []):
        from apps.listings.search_config.panels import (
            FK_BRAND_FIELDS, TEXT_BRAND_FIELDS)
        if f.get('db_field') in FK_BRAND_FIELDS or f.get('db_field') in TEXT_BRAND_FIELDS:
            db_field = f['db_field']
            break
    if not db_field:
        return None

    top, rest = _brand_rows(vt_slug, db_field, None, sub_slug)
    items = [{'v': str(r['value']), 'n': r['name'], 'c': r['count']}
             for r in (list(top) + list(rest))[:MAX_ITEMS]]
    cache.set(key, items, CACHE_SECONDS)
    return items


def brand_name(vt_slug, value, sub_slug=None):
    """Pasirinktos markės pavadinimas — kad laukas rodytų jį be JS."""
    if not value:
        return None
    items = brand_items(vt_slug, sub_slug) or []
    for it in items:
        if it['v'] == str(value):
            return it['n']
    return str(value)


@require_GET
@cache_control(public=True, max_age=CACHE_SECONDS)
def brand_options(request):
    """GET /ajax/markes/?kategorija=<slug>&subkategorija=<slug>&q=<tekstas>"""
    vt_slug = request.GET.get('kategorija') or ''
    sub_slug = request.GET.get('subkategorija') or None
    q = (request.GET.get('q') or '').strip().lower()

    items = brand_items(vt_slug, sub_slug)
    if items is None:
        return HttpResponseNotFound(json.dumps({'error': 'nežinoma kategorija'}),
                                    content_type='application/json')
    if q:
        items = [it for it in items if q in it['n'].lower()]

    payload = {'kategorija': vt_slug, 'markes': items, 'viso': len(items)}
    body = json.dumps(payload, ensure_ascii=False)
    etag = '"%s"' % hashlib.md5(body.encode('utf-8')).hexdigest()[:16]
    if request.headers.get('If-None-Match') == etag:
        from django.http import HttpResponseNotModified
        r = HttpResponseNotModified()
        r['ETag'] = etag
        return r

    resp = JsonResponse(payload, json_dumps_params={'ensure_ascii': False})
    resp['ETag'] = etag
    return resp


# ── Modeliai ────────────────────────────────────────────────────────
# Ta pati logika kaip markėms: sąrašas HTML'e negulėjo ir negulės, o
# darbalaukyje jis iki 2026-08-21 apskritai neatsirasdavo — modelio
# laukas likdavo tuščias („Visi"). Telefone kaskada jau veikė per
# /pasirinkti/?zingsnis=2; dabar abu paviršiai ima iš vieno šaltinio.

MODEL_SOURCES = {
    'cars': ('Model', 'brand'),
    'motorcycles': ('MotorcycleModel', 'brand'),
}


def model_items(vt_slug, brand_id):
    """[{v, n, c}] modeliai pagal markę. Kešuojama 10 min."""
    src = MODEL_SOURCES.get(vt_slug)
    if not src or not str(brand_id).isdigit():
        return None

    key = f'modellist:v1:{vt_slug}:{brand_id}'
    hit = cache.get(key)
    if hit is not None:
        return hit

    from django.db.models import Count
    from django.db.models.functions import Lower
    from apps.listings import models as m
    from apps.listings.views import _public_listings_qs

    model_cls = getattr(m, src[0])
    rows = model_cls.objects.filter(**{src[1] + '_id': brand_id}).order_by(Lower('name'))

    field = 'model' if vt_slug == 'cars' else 'motorcycle_model'
    counts = {
        r[f'{field}_id']: r['c']
        for r in _public_listings_qs(None)
        .filter(vehicle_type__slug=vt_slug)
        .exclude(**{f'{field}__isnull': True})
        .values(f'{field}_id').annotate(c=Count('id'))
    }
    items = [{'v': str(o.pk), 'n': o.name, 'c': counts.get(o.pk, 0)} for o in rows]
    cache.set(key, items, CACHE_SECONDS)
    return items


@require_GET
@cache_control(public=True, max_age=CACHE_SECONDS)
def model_options(request):
    """GET /ajax/modeliai/?kategorija=<slug>&marke=<id>&q=<tekstas>"""
    vt_slug = request.GET.get('kategorija') or ''
    brand_id = request.GET.get('marke') or ''
    q = (request.GET.get('q') or '').strip().lower()

    items = model_items(vt_slug, brand_id)
    if items is None:
        return JsonResponse({'kategorija': vt_slug, 'modeliai': [], 'viso': 0})
    if q:
        items = [it for it in items if q in it['n'].lower()]
    return JsonResponse({'kategorija': vt_slug, 'marke': brand_id,
                         'modeliai': items, 'viso': len(items)},
                        json_dumps_params={'ensure_ascii': False})
