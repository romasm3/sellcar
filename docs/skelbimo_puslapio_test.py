# -*- coding: utf-8 -*-
"""
SKELBIMO PUSLAPIS: Google Maps krovimas (MAP-03) ir „Atnaujinta" (PARTS-23b).

MAP-03: maps.googleapis.com/maps/api/js buvo sinchroninis ir stabdė
puslapį (/917/ ekrano kadras krisdavo „script injection timed out").
Dabar — tik skelbimams su koordinatėmis ir ASINCHRONIŠKAI
(<script async … &loading=async&callback=…>).

PARTS-23b: dalies bloke „Detalės duomenys" — „Įkelta" visiems,
„Atnaujinta" tik savininkui ir administratoriui ir tik kai data
skiriasi nuo įkėlimo.

Tikrinam TIKRĄ HTML:
  • be koordinačių — nėra „maps.googleapis.com"
  • su koordinatėmis — yra, su loading=async ir async atributu
  • redaguotas: savininkas mato „Atnaujinta", anonimas — ne
  • neredaguotas: tik „Įkelta"

Paleidimas (TIK su laikina sqlite baze, ne produkcijoje):
    PATIKRA_DB=<laikinas failas> python docs/skelbimo_puslapio_test.py
"""
import os
import sys

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sqlite_settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'patikra'))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

import re                                            # noqa: E402
from datetime import timedelta                       # noqa: E402
from decimal import Decimal                          # noqa: E402

from django.conf import settings                     # noqa: E402
from django.test import Client, override_settings    # noqa: E402
from django.test.utils import setup_test_environment  # noqa: E402
from django.utils import timezone                    # noqa: E402

import formu_seed                                    # noqa: E402
from apps.listings.models import Listing, SubCategory, VehicleType  # noqa: E402

gerai = blogai = 0


def tikrink(salyga, tekstas, papildomai=''):
    global gerai, blogai
    if salyga:
        gerai += 1
        print(f'  OK   {tekstas}')
    else:
        blogai += 1
        print(f'  BLOGAI {tekstas}' + (f'\n         {papildomai}' if papildomai else ''))


def dalis(u, pav, koordinates, redaguota):
    vt, _ = VehicleType.objects.get_or_create(slug='parts', defaults={'name': 'Parts'})
    sub, _ = SubCategory.objects.get_or_create(
        vehicle_type=vt, slug='single-part-or-kit', defaults={'name': 'Atskira dalis'})
    l = Listing.objects.filter(seller=u, title=pav).first() or Listing(seller=u, title=pav)
    l.vehicle_type, l.subcategory, l.status = vt, sub, 'active'
    l.city, l.country, l.oem_code = 'Kaunas', 'LT', '11111111111'
    l.price, l.year, l.mileage, l.condition = Decimal('50'), 2020, 0, 'used'
    l.expires_at = timezone.now() + timedelta(days=30)
    l.save()
    # save() pats geokoduoja miestą — būseną nustatom tiesiai DB
    atnaujinta = timezone.now()
    Listing.objects.filter(pk=l.pk).update(
        latitude=Decimal('54.898214') if koordinates else None,
        longitude=Decimal('23.904482') if koordinates else None,
        created_at=atnaujinta - timedelta(days=3) if redaguota else atnaujinta,
        updated_at=atnaujinta)
    l.refresh_from_db()
    return l


def html(c, l):
    return c.get(f'/{l.pk}/', follow=True).content.decode('utf-8', 'replace')


@override_settings(LANGUAGE_CODE='lt')
def main():
    setup_test_environment()
    u = formu_seed.vartotojas()
    be = dalis(u, 'Patikra puslapis be koordinačių', koordinates=False, redaguota=False)
    su = dalis(u, 'Patikra puslapis su koordinatėmis', koordinates=True, redaguota=True)

    anonimas = Client()
    anonimas.cookies[settings.LANGUAGE_COOKIE_NAME] = 'lt'
    savininkas = Client()
    savininkas.cookies[settings.LANGUAGE_COOKIE_NAME] = 'lt'
    savininkas.force_login(u)

    print(f'\n— MAP-03: be koordinačių (#{be.pk})')
    h = html(anonimas, be)
    tikrink('maps.googleapis.com' not in h, 'nėra maps.googleapis.com')

    print(f'\n— MAP-03: su koordinatėmis (#{su.pk})')
    h = html(anonimas, su)
    zyma = re.search(r'<script\b[^>]*maps\.googleapis\.com/maps/api/js[^>]*>', h)
    zyma = zyma.group(0) if zyma else ''
    tikrink(bool(zyma), 'yra maps.googleapis.com')
    tikrink('loading=async' in zyma, 'su loading=async', zyma)
    tikrink(re.search(r'<script\s+async\b', zyma) is not None, 'su async atributu', zyma)
    tikrink('callback=alSkelbimoZemelapis' in zyma and 'window.alSkelbimoZemelapis' in h,
            'callback apibrėžtas')
    tikrink(h.index('window.alSkelbimoZemelapis') < h.index(zyma) if zyma else False,
            'callback apibrėžtas PRIEŠ skripto žymą')

    print(f'\n— PARTS-23b: redaguotas (#{su.pk})')
    tikrink('Atnaujinta' in html(savininkas, su), 'savininkas mato „Atnaujinta"')
    h = html(anonimas, su)
    tikrink('Atnaujinta' not in h, 'anonimas „Atnaujinta" nemato')
    tikrink('data-ikelta' in h and 'Įkelta' in h, 'anonimas mato „Įkelta"')

    print(f'\n— PARTS-23b: neredaguotas (#{be.pk})')
    h = html(savininkas, be)
    tikrink('Įkelta' in h and 'Atnaujinta' not in h, 'tik „Įkelta" (net savininkui)')

    print(f'\n════ {gerai} gerai / {blogai} blogai ════')
    return 1 if blogai else 0


if __name__ == '__main__':
    sys.exit(main())
