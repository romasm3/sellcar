# -*- coding: utf-8 -*-
"""
DALIŲ PAIEŠKA PAGAL DETALĖS NUMERĮ IR TEKSTĄ.

Klaida: /?section=parts&q=51128075031 grąžindavo „Rasta 0", nors
skelbimas egzistuoja. Ir /?section=parts&q=bamperis irgi — t. y. dalių
tekstinė paieška neveikė visai. Dvi priežastys:

  1. `?section=` nebuvo laikomas kategorija, tad tuščia kategorija
     krisdavo į „cars" ir ieškodavo automobiliuose;
  2. `q` ieškojo tik pavadinime — nei aprašyme, nei `oem_code`.

Tikrinam (skelbimas su oem_code „210181001000 / 51128075031 / …"):
  • pilnas kodas                      51128075031
  • kodas su tarpais                  5112 807 5031
  • kodas su brūkšneliu ir tašku       51128-075.031
  • NE pirmas kodas sąraše            51128085093
  • žodis iš pavadinimo               bamperis
  • žodis iš aprašymo                 originalus
  • svetimas kodas NERANDA            99999999999
  • skelbimo puslapyje matosi visi trys kodai atskirai

Paleidimas:
    PATIKRA_DB=<...> python docs/daliu_paieskos_test.py
"""
import os
import sys

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sqlite_settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'patikra'))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

from decimal import Decimal                          # noqa: E402

from django.test import Client                       # noqa: E402
from django.test.utils import setup_test_environment  # noqa: E402

import formu_seed                                    # noqa: E402
from apps.listings.models import (Listing, SubCategory,  # noqa: E402
                                  VehicleType)

KODAI = '210181001000 / 51128075031 / 51128085093'
PAVADINIMAS = 'BMW M3 G80 galinis bamperis'
APRASYMAS = 'Visiškai originalus, be defektų.'

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
    l = Listing.objects.filter(seller=u, title=PAVADINIMAS).first() or Listing(
        seller=u, title=PAVADINIMAS)
    l.vehicle_type, l.subcategory = vt, sub
    l.year, l.mileage, l.price = 2021, 1000, Decimal('450')
    l.city, l.country, l.status = 'Vilnius', 'LT', 'active'
    l.oem_code = KODAI
    l.description = APRASYMAS
    l.save()
    return l


def rasta(c, q):
    """Ar paieška grąžina mūsų skelbimą (per tikrą puslapį, ne ORM)."""
    a = c.get(f'/?section=parts&q={q}', follow=True)
    if a.status_code != 200:
        return None
    return a.context['listings'] if a.context and 'listings' in a.context else None


def main():
    setup_test_environment()
    l = pasejk()
    c = Client()

    print('\n— Paieška pagal detalės numerį')
    for q, pav in (('51128075031', 'pilnas kodas'),
                   ('5112 807 5031', 'kodas su tarpais'),
                   ('51128-075.031', 'kodas su brūkšneliu ir tašku'),
                   ('51128085093', 'trečias kodas sąraše'),
                   ('210181001000', 'pirmas kodas sąraše')):
        sarasas = rasta(c, q)
        tikrink(sarasas is not None and l.pk in [x.pk for x in sarasas],
                f'{pav}: „{q}" randa #{l.pk}',
                f'rasta {0 if sarasas is None else len(sarasas)}')

    print('\n— Paieška pagal tekstą')
    for q, pav in (('bamperis', 'žodis iš pavadinimo'),
                   ('originalus', 'žodis iš aprašymo')):
        sarasas = rasta(c, q)
        tikrink(sarasas is not None and l.pk in [x.pk for x in sarasas],
                f'{pav}: „{q}" randa #{l.pk}',
                f'rasta {0 if sarasas is None else len(sarasas)}')

    print('\n— Svetimo nerandam')
    sarasas = rasta(c, '99999999999')
    tikrink(sarasas is not None and l.pk not in [x.pk for x in sarasas],
            'nesamas kodas skelbimo NEranda',
            f'rasta {0 if sarasas is None else len(sarasas)}')

    print('\n— Skelbimo puslapis')
    a = c.get(f'/{l.pk}/', follow=True)
    turinys = a.content.decode('utf-8', 'replace')
    tikrink('Detalės numeris' in turinys, 'rodoma eilutė „Detalės numeris"')
    for kodas in ('210181001000', '51128075031', '51128085093'):
        tikrink(f'>{kodas}<' in turinys.replace('\n', '').replace(' ', ''),
                f'kodas {kodas} rodomas atskirai')

    print(f'\n════ {gerai} gerai / {blogai} blogai ════')
    return 1 if blogai else 0


if __name__ == '__main__':
    sys.exit(main())
