# -*- coding: utf-8 -*-
"""
DALIES PAVADINIMAS REDAGUOJANT — IŠ FORMOS, NE IŠ KATEGORIJOS.

POST į /create/parts/form/?edit=<id> su title="XYZ TESTAS" → /<id>/
rodo „XYZ TESTAS". Tuščias title redaguojant palieka esamą pavadinimą
(anksčiau jį perrašydavo kategorijos vardas).

Forma pateikiama taip, kaip naršyklė: visi laukai iš išvesto HTML
(Forma iš daliu_redagavimo_pavadinimo_test.py), pakeičiamas tik title.

Paleidimas (TIK su laikina sqlite baze, ne produkcijoje):
    PATIKRA_DB=<laikinas failas> python docs/parts_pavadinimo_test.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import daliu_redagavimo_pavadinimo_test as bazinis   # noqa: E402  (django.setup())

from django.conf import settings                     # noqa: E402
from django.test import Client, override_settings    # noqa: E402
from django.test.utils import setup_test_environment  # noqa: E402

import formu_seed                                    # noqa: E402

NAUJAS = 'XYZ TESTAS'

gerai = blogai = 0


def tikrink(salyga, tekstas, papildomai=''):
    global gerai, blogai
    if salyga:
        gerai += 1
        print(f'  OK   {tekstas}')
    else:
        blogai += 1
        print(f'  BLOGAI {tekstas}' + (f'\n         {papildomai}' if papildomai else ''))


def formos_postas(c, url):
    html = c.get(url, follow=True).content.decode('utf-8', 'replace')
    postas = {}
    for k, v in bazinis.forma(html).laukai:
        postas.setdefault(k, []).append(v)
    return postas


@override_settings(LANGUAGE_CODE='lt')
def main():
    setup_test_environment()
    u = formu_seed.vartotojas()
    l = bazinis.pasejk(u)
    c = Client()
    c.cookies[settings.LANGUAGE_COOKIE_NAME] = 'lt'
    c.force_login(u)
    url = f'/create/parts/form/?edit={l.pk}'

    print(f'\n— POST {url} su title="{NAUJAS}"')
    postas = formos_postas(c, url)
    postas['title'] = [NAUJAS]
    a = c.post(url, postas)
    tikrink(a.status_code == 302, f'išsaugota (302, gauta {a.status_code})')
    html = c.get(f'/{l.pk}/', follow=True).content.decode('utf-8', 'replace')
    tikrink(NAUJAS in html, f'GET /{l.pk}/ rodo „{NAUJAS}"')
    tikrink(bazinis.KATEGORIJA_LT not in html.split('<title>')[1].split('</title>')[0]
            if '<title>' in html else True,
            'puslapio antraštėje ne kategorijos vardas')

    print('\n— POST su tuščiu title → lieka esamas')
    postas = formos_postas(c, url)
    postas['title'] = ['']
    c.post(url, postas)
    l.refresh_from_db()
    tikrink(l.title == NAUJAS, f'pavadinimas liko „{NAUJAS}"',
            f'DB: {l.title!r} (kategorija būtų „{bazinis.KATEGORIJA_LT}")')

    # Grąžinam pradinį — kitas testas (daliu_redagavimo_pavadinimo) jo tikisi
    l.title = bazinis.PAVADINIMAS
    l.save(update_fields=['title'])

    print(f'\n════ {gerai} gerai / {blogai} blogai ════')
    return 1 if blogai else 0


if __name__ == '__main__':
    sys.exit(main())
