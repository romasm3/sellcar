# -*- coding: utf-8 -*-
"""
VIETA BE ŽEMĖLAPIO FORMOJE — KOORDINATES NUSTATO SERVERIS.

Klaida: formų žemėlapis krovė plyteles iš OSM viešo plytelių serverio
(tile.openstreetmap.org), kuris tokį naudojimą blokuoja — kiekvienas
pildantis skelbimą matė „403 Access blocked". Be to, dalis kategorijų
(pvz. dalys) koordinačių nepildė visai, o spėjimas nežinomam miestui
grąžindavo Kauną.

Tikrinam:
  • formos HTML (/create/parts/form/?sub=…) neturi „tile.openstreetmap.org",
    žemėlapio rėmelio ir Leaflet; „Vietos tikslumas" lieka
  • skelbimas su miestu „Kaunas" po išsaugojimo turi latitude/longitude
  • juodraštis koordinates gauna aktyvuojant (activate())
  • pakeitus miestą koordinatės perskaičiuojamos
  • geokodavimui neveikiant (tinklo klaida) skelbimas vis tiek
    išsaugomas — nežinomas miestas lieka be koordinačių, ne Kaune

Paleidimas (TIK su laikina sqlite baze, ne produkcijoje):
    PATIKRA_DB=<laikinas failas> python docs/vietos_geokodavimo_test.py
Kaunas geokoduojamas per Nominatim (kešuojama); be tinklo — iš vietinio
žodyno, tad testas nuo tinklo nepriklauso.
"""
import os
import sys
import tempfile

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sqlite_settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'patikra'))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

import io                                            # noqa: E402
from decimal import Decimal                          # noqa: E402
from unittest import mock                            # noqa: E402

from django.core.cache import cache                  # noqa: E402
from django.core.files.base import ContentFile       # noqa: E402
from django.test import Client, override_settings    # noqa: E402
from django.test.utils import setup_test_environment  # noqa: E402
from PIL import Image                                # noqa: E402

import formu_seed                                    # noqa: E402
from apps.listings import geokodavimas                # noqa: E402
from apps.listings.models import (Listing, ListingImage, PartCategory,  # noqa: E402
                                  SubCategory, VehicleType)

LAPAS = 'lighting-front-lights-headlight'
MEDIA = tempfile.mkdtemp(prefix='vietos_media_')

gerai = blogai = 0


def tikrink(salyga, tekstas, papildomai=''):
    global gerai, blogai
    if salyga:
        gerai += 1
        print(f'  OK   {tekstas}')
    else:
        blogai += 1
        print(f'  BLOGAI {tekstas}' + (f'\n         {papildomai}' if papildomai else ''))


def pagrindai():
    vt, _ = VehicleType.objects.get_or_create(slug='parts', defaults={'name': 'Parts'})
    sub, _ = SubCategory.objects.get_or_create(
        vehicle_type=vt, slug='single-part-or-kit', defaults={'name': 'Atskira dalis'})
    medis = {}
    for slug, vardas, lygis, tevas in (
            ('lighting', 'Lighting', 0, None),
            ('lighting-front-lights', 'Front Lights', 1, 'lighting'),
            (LAPAS, 'Headlight', 2, 'lighting-front-lights')):
        m, _ = PartCategory.objects.update_or_create(slug=slug, defaults=dict(
            name_en=vardas, level=lygis, parent=medis.get(tevas), is_active=True))
        medis[slug] = m
    return vt, sub, medis[LAPAS]


def skelbimas(u, vt, sub, pav, miestas, statusas):
    l = Listing.objects.filter(seller=u, title=pav).first() or Listing(seller=u, title=pav)
    l.vehicle_type, l.subcategory, l.status = vt, sub, statusas
    l.city, l.country, l.address = miestas, 'LT', ''
    l.latitude = l.longitude = None
    l.price, l.year, l.mileage, l.condition = Decimal('100'), 2020, 0, 'used'
    l.save()
    return l


def main():
    setup_test_environment()
    cache.clear()
    u = formu_seed.vartotojas()
    vt, sub, _lapas = pagrindai()
    c = Client()
    c.force_login(u)

    print('\n— Formos HTML be OSM plytelių ir žemėlapio')
    for url in (f'/create/parts/form/?sub={LAPAS}',):
        html = c.get(url, follow=True).content.decode('utf-8', 'replace')
        tikrink('tile.openstreetmap.org' not in html, f'{url}: nėra „tile.openstreetmap.org"')
        tikrink('vt-zemelapis' not in html and 'leaflet' not in html.lower(),
                f'{url}: nėra žemėlapio rėmelio ir Leaflet')
        tikrink('vietos_zemelapis.js' not in html, f'{url}: nėra vietos_zemelapis.js')
        tikrink('Vietos tikslumas' in html and 'name="hide_exact_address"' in html,
                f'{url}: „Vietos tikslumas" lieka')

    print('\n— Aktyvus skelbimas su miestu „Kaunas"')
    l = skelbimas(u, vt, sub, 'Patikra vieta Kaunas', 'Kaunas', 'active')
    l.refresh_from_db()
    tikrink(l.latitude is not None and l.longitude is not None,
            f'latitude/longitude užpildyti ({l.latitude}, {l.longitude})')
    tikrink(l.latitude is not None and 54.7 < float(l.latitude) < 55.1
            and 23.7 < float(l.longitude) < 24.2, '   ir jos — Kaune')

    print('\n— Miestas pakeičiamas → koordinatės perskaičiuojamos')
    l.city = 'Vilnius'
    l.save()
    l.refresh_from_db()
    tikrink(l.latitude is not None and 54.5 < float(l.latitude) < 54.9
            and 25.0 < float(l.longitude) < 25.5,
            f'Vilnius ({l.latitude}, {l.longitude})')

    print('\n— Juodraštis → activate()')
    d = skelbimas(u, vt, sub, 'Patikra vieta juodraštis', 'Kaunas', 'draft')
    d.refresh_from_db()
    tikrink(d.latitude is None, 'juodraščio įrašymas tinklo nekviečia (koordinačių dar nėra)')
    if not d.images.exists():
        b = io.BytesIO()
        Image.new('RGB', (40, 30), 'green').save(b, 'JPEG')
        img = ListingImage(listing=d, is_main=True)
        img.image.save('vieta_patikra.jpg', ContentFile(b.getvalue()), save=False)
        img.save()
    tikrink(d.activate() is True, 'aktyvuota')
    d.refresh_from_db()
    tikrink(d.latitude is not None and d.longitude is not None,
            f'po activate() koordinatės yra ({d.latitude}, {d.longitude})')

    print('\n— Geokodavimas neveikia (tinklo klaida)')
    with mock.patch.object(geokodavimas, '_uzklausa', return_value=None):
        x = skelbimas(u, vt, sub, 'Patikra vieta be tinklo', 'Nesamasmiestasxyz', 'active')
    x.refresh_from_db()
    tikrink(x.pk is not None, 'skelbimas vis tiek išsaugotas')
    tikrink(x.latitude is None and x.longitude is None,
            'nežinomas miestas — be koordinačių (ne Kaune)', f'({x.latitude}, {x.longitude})')

    print(f'\n════ {gerai} gerai / {blogai} blogai ════')
    return 1 if blogai else 0


if __name__ == '__main__':
    with override_settings(MEDIA_ROOT=MEDIA):
        kodas = main()
    sys.exit(kodas)
