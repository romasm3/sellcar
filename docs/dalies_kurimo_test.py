# -*- coding: utf-8 -*-
"""
DALIES KŪRIMAS: POST /create/parts/form/?sub=<slug> NEBEKRENTA SU 500.

Regresija (f7d1ecfd, aktyvavimo srautas): importas
`from .aktyvavimas import aktyvuok` parts_views.py pateko į modulio
docstring'ą, tad išsaugojimo kelias, praėjus validaciją, krisdavo
NameError: name 'aktyvuok' is not defined → 500.

Tikrinam (force_login, tikras POST su multipart):
  • pilnas rinkinys (title, price, condition, brand, model, year_from,
    fuel_type, description, phone, email, country=LT, city,
    hide_exact_address, agree_terms + nuotrauka) → 302 į /<id>/success/,
    skelbimas aktyvus
  • tas pats be nuotraukos → ne 500, o 302 į redagavimą (trūksta
    nuotraukos — aktyvuoti be jos negalima)
  • trūkstami laukai → 200 su klaidomis (ne 500)
  • visi 17 vaizdų, kviečiančių aktyvuok(), jį importuoja MODULIO
    lygyje (ne docstring'e) — kad tokia klaida nepasikartotų kitur

Paleidimas (TIK su laikina sqlite baze, ne produkcijoje):
    PATIKRA_DB=<laikinas failas> python docs/dalies_kurimo_test.py
"""
import os
import sys
import tempfile

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sqlite_settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'patikra'))
BAZE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BAZE)
django.setup()

import ast                                           # noqa: E402
import glob                                          # noqa: E402
import io                                            # noqa: E402
import re                                            # noqa: E402
from urllib.parse import urlparse                    # noqa: E402

from django.core.files.uploadedfile import SimpleUploadedFile  # noqa: E402
from django.test import Client, override_settings    # noqa: E402
from django.test.utils import setup_test_environment  # noqa: E402
from PIL import Image                                # noqa: E402

import formu_seed                                    # noqa: E402
from apps.listings.models import (Brand, FuelType, Listing, Model,  # noqa: E402
                                  PartCategory, SubCategory, VehicleType)

MEDIA = tempfile.mkdtemp(prefix='dalies_kurimo_media_')
LAPAS = 'lighting-front-lights-headlight'

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
    vt, _ = VehicleType.objects.get_or_create(slug='parts', defaults={'name': 'Parts'})
    SubCategory.objects.get_or_create(vehicle_type=vt, slug='single-part-or-kit',
                                      defaults={'name': 'Single part / parts kit'})
    medis = {}
    for slug, vardas, lygis, tevas in (
            ('lighting', 'Lighting', 0, None),
            ('lighting-front-lights', 'Front Lights', 1, 'lighting'),
            (LAPAS, 'Headlight', 2, 'lighting-front-lights')):
        m, _ = PartCategory.objects.update_or_create(slug=slug, defaults=dict(
            name_en=vardas, level=lygis, parent=medis.get(tevas), is_active=True))
        medis[slug] = m
    marke = Brand.objects.filter(name='BMW').first() or Brand.objects.create(
        name='BMW', slug='bmw-kurimas')
    modelis = Model.objects.filter(brand=marke).first() or Model.objects.create(
        brand=marke, name='M3', slug='m3-kurimas')
    kuras = FuelType.objects.first() or FuelType.objects.create(name='Petrol')
    return marke, modelis, kuras


def jpeg():
    b = io.BytesIO()
    Image.new('RGB', (64, 48), 'gray').save(b, 'JPEG')
    return SimpleUploadedFile('dalis.jpg', b.getvalue(), content_type='image/jpeg')


def rinkinys(marke, modelis, kuras, pavadinimas):
    return {
        'sub': LAPAS, 'title': pavadinimas, 'price': '120', 'condition': 'used',
        'brand': str(marke.pk), 'model': str(modelis.pk), 'year_from': '2020',
        'fuel_type': str(kuras.pk), 'description': 'Bandomasis aprašymas.',
        'phone': '+37060000000', 'email': 'patikra@autoleft.lt',
        'country': 'LT', 'city': 'Kaunas', 'hide_exact_address': '', 'agree_terms': 'on',
    }


@override_settings(MOKEJIMAI_IJUNGTI=False, PAYMENTS_ENABLED=False)
def main():
    setup_test_environment()
    marke, modelis, kuras = pasejk()
    c = Client()
    c.force_login(formu_seed.vartotojas())
    url = f'/create/parts/form/?sub={LAPAS}'

    print('\n— Pilnas rinkinys + nuotrauka')
    duom = rinkinys(marke, modelis, kuras, 'Patikra kurimas su nuotrauka')
    duom['images'] = jpeg()
    a = c.post(url, duom)
    vieta = urlparse(a.get('Location', '')).path
    tikrink(a.status_code == 302 and re.fullmatch(r'/\d+/success/', vieta or ''),
            f'302 → /<id>/success/ (gauta {a.status_code} {a.get("Location")})')
    l = Listing.objects.filter(title='Patikra kurimas su nuotrauka').order_by('-pk').first()
    tikrink(l is not None and l.status == 'active', f'skelbimas aktyvus ({l and l.status})')

    print('\n— Tas pats be nuotraukos — ne 500')
    a = c.post(url, rinkinys(marke, modelis, kuras, 'Patikra kurimas be nuotraukos'))
    tikrink(a.status_code == 302 and 'edit' in a.get('Location', ''),
            f'302 → redagavimas (gauta {a.status_code} {a.get("Location")})')

    print('\n— Trūkstami laukai — 200 su klaidomis')
    a = c.post(url, {'sub': LAPAS, 'title': 'x', 'price': '120', 'condition': 'used',
                     'country': 'LT', 'agree_terms': 'on'})
    tikrink(a.status_code == 200, f'200 (gauta {a.status_code})')

    print('\n— aktyvuok() importuojamas modulio lygyje visur, kur kviečiamas')
    blogi = []
    for kelias in glob.glob(os.path.join(BAZE, 'apps', 'listings', '*.py')):
        tekstas = open(kelias, encoding='utf-8').read()
        if 'aktyvuok(' not in tekstas or kelias.endswith('aktyvavimas.py'):
            continue
        medis = ast.parse(tekstas)
        if not any(isinstance(n, ast.ImportFrom) and n.module == 'aktyvavimas'
                   and any(x.name == 'aktyvuok' for x in n.names) for n in medis.body):
            blogi.append(os.path.basename(kelias))
    tikrink(not blogi, 'visuose kvietėjuose importas modulio lygyje', f'trūksta: {blogi}')

    print(f'\n════ {gerai} gerai / {blogai} blogai ════')
    return 1 if blogai else 0


if __name__ == '__main__':
    with override_settings(MEDIA_ROOT=MEDIA):
        kodas = main()
    sys.exit(kodas)
