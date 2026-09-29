# -*- coding: utf-8 -*-
"""
DALIŲ FILTRAS „DETALĖS NUMERIS" (?oem=) ŠONINĖJE JUOSTOJE.

Klaida: /?category=parts&sidebar=1 formoje buvo 22 laukai ir nė vieno
detalės numeriui — pirkėjas negalėjo filtruoti pagal kodą kartu su
marke ar kaina.

Sėjam dvi dalis su skirtingais kodais (ir skirtingomis markėmis) ir
tikrinam TIKRĄ puslapio HTML (nuorodas į /<pk>/), ne kontekstą:
  • oem=<pilnas kodas>           → tik viena dalis
  • oem su tarpais / brūkšneliu  → ta pati dalis
  • ne pirmas kodas „A / B" lauke → ta pati dalis
  • nesamas kodas                → 0
  • oem + markė                  → IR (tinkama markė 1, kita — 0)
  • skaitliukas /paieska/count/  → sutampa su sąrašu
  • laukas name="oem" yra dalių juostoje su įvesta reikšme,
    automobilių juostoje jo nėra
  • ?oem= patenka į išsaugomos paieškos parametrus

Paleidimas (TIK su laikina sqlite baze, ne produkcijoje):
    PATIKRA_DB=<laikinas failas> python docs/daliu_oem_filtro_test.py
"""
import os
import sys

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sqlite_settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'patikra'))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

import re                                            # noqa: E402
from decimal import Decimal                          # noqa: E402
from urllib.parse import urlencode                   # noqa: E402

from django.test import Client, RequestFactory       # noqa: E402
from django.test.utils import setup_test_environment  # noqa: E402

import formu_seed                                    # noqa: E402
from apps.listings.models import (Brand, Listing, SubCategory,  # noqa: E402
                                  VehicleType)

DALYS = [
    # (pavadinimas, markė, oem_code)
    ('Patikra oem galinis bamperis', 'BMW', '77120075031 / 77120085093'),
    ('Patikra oem priekinis žibintas', 'Audi', '8W0941099'),
]

gerai = blogai = 0


def tikrink(salyga, tekstas, papildomai=''):
    global gerai, blogai
    if salyga:
        gerai += 1
        print(f'  OK   {tekstas}')
    else:
        blogai += 1
        print(f'  BLOGAI {tekstas}' + (f'\n         {papildomai}' if papildomai else ''))


def pasejk():
    u = formu_seed.vartotojas()
    vt, _ = VehicleType.objects.get_or_create(slug='parts',
                                              defaults={'name': 'Parts'})
    sub, _ = SubCategory.objects.get_or_create(
        vehicle_type=vt, slug='single-part-or-kit',
        defaults={'name': 'Atskira dalis'})
    rezultatas = []
    for pav, marke, kodas in DALYS:
        b = Brand.objects.filter(name=marke).first() or Brand.objects.create(
            name=marke, slug=marke.lower() + '-patikra')
        l = Listing.objects.filter(seller=u, title=pav).first() or Listing(
            seller=u, title=pav)
        l.vehicle_type, l.subcategory, l.brand = vt, sub, b
        l.year, l.mileage, l.price = 2021, 1000, Decimal('150')
        l.city, l.country, l.status = 'Vilnius', 'LT', 'active'
        l.oem_code = kodas
        l.description = 'Bandomoji dalis.'
        l.save()
        rezultatas.append(l)
    return rezultatas


def puslapis(c, **params):
    a = c.get('/?' + urlencode(dict({'category': 'parts', 'sidebar': '1'}, **params)),
              follow=True)
    return a.status_code, a.content.decode('utf-8', 'replace')


def rasti(html, dalys):
    """Kurios iš MŪSŲ dalių turi kortelę išvestame HTML (data-skelbimas)."""
    return {l.pk for l in dalys if re.search(rf'data-skelbimas="{l.pk}"', html)}


def skaitliukas(c, **params):
    a = c.get('/paieska/count/parts/?' + urlencode(dict({'advanced': '1'}, **params)),
              HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    try:
        return a.json().get('count')
    except Exception:
        return None


def main():
    setup_test_environment()
    bamperis, zibintas = dalys = pasejk()
    c = Client()

    print('\n— Laukas juostoje')
    kodas, html = puslapis(c, oem='77120075031')
    tikrink(kodas == 200, f'dalių rezultatų puslapis 200 (gauta {kodas})')
    laukas = re.search(r'<input[^>]*name="oem"[^>]*>', html)
    tikrink(laukas is not None, 'dalių juostoje yra <input name="oem">')
    tikrink(laukas is not None and 'value="77120075031"' in laukas.group(0),
            'laukas išlaiko įvestą reikšmę (nuoroda persiunčiama)')
    tikrink('Detalės numeris' in html, 'užrašas „Detalės numeris"')
    _k, auto = c.get('/?category=cars&sidebar=1', follow=True).status_code, \
        c.get('/?category=cars&sidebar=1', follow=True).content.decode('utf-8', 'replace')
    tikrink('name="oem"' not in auto, 'automobilių juostoje lauko NĖRA')
    for kelias, turi in (('/paieska/parts/', True), ('/paieska/cars/', False)):
        html_d = c.get(kelias, follow=True).content.decode('utf-8', 'replace')
        yra = re.search(r'<input[^>]*name="oem"', html_d) is not None
        tikrink(yra == turi, f'„Daugiau filtrų" {kelias}: laukas '
                f'{"yra" if turi else "NĖRA"}')

    print('\n— Filtras pagal kodą (tikras HTML)')
    for q, laukta, pav in (
            ('77120075031', {bamperis.pk}, 'pilnas kodas'),
            ('7712 007 5031', {bamperis.pk}, 'kodas su tarpais'),
            ('77120-075031', {bamperis.pk}, 'kodas su brūkšneliu'),
            ('7712.0075.031', {bamperis.pk}, 'kodas su taškais'),
            ('77120085093', {bamperis.pk}, 'antras kodas „A / B" lauke'),
            ('8w0-941-099', {zibintas.pk}, 'kita dalis, mažosios raidės'),
            ('99999999999', set(), 'nesamas kodas'),
            ('7712007503177120085093', set(), 'suklijuoti du kodai NErandami')):
        _k, html = puslapis(c, oem=q)
        gauta = rasti(html, dalys)
        tikrink(gauta == laukta, f'{pav}: oem="{q}" → {sorted(laukta) or "0"}',
                f'gauta {sorted(gauta)}')
        sk = skaitliukas(c, oem=q)
        # Skaitliukas skaičiuoja VISAS dalis; mūsų sėklos kodai unikalūs (ne #880 —
        # daliu_paieskos_test sėja jo kodus į tą pačią DB),
        # tad jis turi sutapti su mūsų rastų skaičiumi.
        tikrink(sk == len(laukta), f'   skaitliukas = {len(laukta)}', f'gauta {sk}')

    print('\n— oem kartu su marke (IR)')
    bmw, audi = bamperis.brand_id, zibintas.brand_id
    for marke, laukta, pav in ((bmw, {bamperis.pk}, 'tinkama markė'),
                               (audi, set(), 'kita markė')):
        _k, html = puslapis(c, oem='7712 007 5031', brand=marke)
        gauta = rasti(html, dalys)
        tikrink(gauta == laukta, f'oem + {pav} → {sorted(laukta) or "0"}',
                f'gauta {sorted(gauta)}')
        sk = skaitliukas(c, oem='7712 007 5031', brand=marke)
        tikrink(sk == len(laukta), f'   skaitliukas = {len(laukta)}', f'gauta {sk}')

    print('\n— oem kartu su kaina (IR)')
    _k, html = puslapis(c, oem='77120075031', price_max='100')
    tikrink(rasti(html, dalys) == set(), 'oem + kaina iki 100 (dalis 150) → 0')

    print('\n— Išsaugoma paieška')
    from apps.listings.views import _paieskos_params
    params = _paieskos_params(RequestFactory().get(
        '/?category=parts&sidebar=1&oem=77120075031'))
    tikrink(params.get('oem') == '77120075031', 'oem patenka į SavedSearch parametrus',
            f'gauta {params}')

    print(f'\n════ {gerai} gerai / {blogai} blogai ════')
    return 1 if blogai else 0


if __name__ == '__main__':
    sys.exit(main())
