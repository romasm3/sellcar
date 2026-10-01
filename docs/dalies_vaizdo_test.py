# -*- coding: utf-8 -*-
"""
DALIES VAIZDAS — skelbimo puslapis ir kortelė (PARTS-13, 19, 20, 21, 22, 23).

Sukuriama dalis BE spalvos ir kėbulo (bet su kuro tipu — tai automobilio,
kuriam dalis tinka, požymis) ir su 2 nuotraukomis. Tikrinam TIKRĄ HTML:

/<id>/:
  • nėra „Rida" (PARTS-13)
  • nėra „Transporto priemonės duomenys", yra „Detalės duomenys" (PARTS-20)
  • nėra tuščių „—" eilučių (PARTS-21)
  • naršymo kelias — „Dalys" → /skelbimai/?kategorija=parts (PARTS-22)
  • yra įkėlimo data (PARTS-23)
/skelbimai/?kategorija=parts kortelė (PARTS-19):
  • detalės numeris, metai, nuotraukų skaičius; kuro tipo nėra

Paleidimas (TIK su laikina sqlite baze, ne produkcijoje):
    PATIKRA_DB=<laikinas failas> python docs/dalies_vaizdo_test.py
Nuotraukos rašomos į laikiną MEDIA_ROOT.
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
import re                                            # noqa: E402
from decimal import Decimal                          # noqa: E402

from django.conf import settings                     # noqa: E402
from django.core.files.base import ContentFile       # noqa: E402
from django.test import Client, override_settings    # noqa: E402
from django.test.utils import setup_test_environment  # noqa: E402
from django.utils import timezone                    # noqa: E402
from PIL import Image                                # noqa: E402

import formu_seed                                    # noqa: E402
from apps.listings.models import (FuelType, Listing, ListingImage,  # noqa: E402
                                  PartCategory, SubCategory, VehicleType)

PAVADINIMAS = 'Patikra dalies vaizdas priekinis žibintas'
KODAS = '63117214533'
MEDIA = tempfile.mkdtemp(prefix='dalies_vaizdo_media_')

gerai = blogai = 0


def tikrink(salyga, tekstas, papildomai=''):
    global gerai, blogai
    if salyga:
        gerai += 1
        print(f'  OK   {tekstas}')
    else:
        blogai += 1
        print(f'  BLOGAI {tekstas}' + (f'\n         {papildomai}' if papildomai else ''))


def pasejk(u):
    vt, _ = VehicleType.objects.get_or_create(slug='parts', defaults={'name': 'Parts'})
    sub, _ = SubCategory.objects.get_or_create(
        vehicle_type=vt, slug='single-part-or-kit', defaults={'name': 'Atskira dalis'})
    medis = {}
    for slug, vardas, lygis, tevas in (
            ('lighting', 'Lighting', 0, None),
            ('lighting-front-lights', 'Front Lights', 1, 'lighting'),
            ('lighting-front-lights-headlight', 'Headlight', 2, 'lighting-front-lights')):
        m, _ = PartCategory.objects.update_or_create(slug=slug, defaults=dict(
            name_en=vardas, level=lygis, parent=medis.get(tevas), is_active=True))
        medis[slug] = m
    kuras = FuelType.objects.first() or FuelType.objects.create(name='Petrol')
    l = Listing.objects.filter(seller=u, title=PAVADINIMAS).first() or Listing(
        seller=u, title=PAVADINIMAS)
    l.vehicle_type, l.subcategory = vt, sub
    l.part_category = medis['lighting-front-lights-headlight']
    l.oem_code = f'{KODAS} / 63117214534'
    l.fuel_type = kuras
    l.color, l.body_type, l.doors, l.address, l.state = '', '', '', '', ''
    l.year, l.mileage, l.price, l.condition = 2019, 0, Decimal('240'), 'used'
    l.city, l.country, l.status = 'Kaunas', 'LT', 'active'
    l.expires_at = timezone.now() + timezone.timedelta(days=30)
    l.description = 'Bandomoji dalis.'
    l.save()
    if l.images.count() != 2:
        l.images.all().delete()
        for i, spalva in enumerate(('red', 'blue')):
            b = io.BytesIO()
            Image.new('RGB', (48, 32), spalva).save(b, 'JPEG')
            img = ListingImage(listing=l, is_main=(i == 0), order=i)
            img.image.save(f'dalies_vaizdas_{i}.jpg', ContentFile(b.getvalue()), save=False)
            img.save()
    # Bendroje laikinoje DB kiti testai kuria daug dalių — sėkla turi būti
    # naujausia, kad būtų pirmame /skelbimai/ puslapyje.
    Listing.objects.filter(pk=l.pk).update(created_at=timezone.now(), activated_at=timezone.now(),
                                           updated_at=timezone.now())
    l.refresh_from_db()
    return l, kuras


def be_skriptu(html):
    return re.sub(r'<script.*?</script>|<style.*?</style>|<!--.*?-->', '', html, flags=re.S)


@override_settings(LANGUAGE_CODE='lt')
def main():
    setup_test_environment()
    u = formu_seed.vartotojas()
    l, kuras = pasejk(u)
    c = Client()
    c.cookies[settings.LANGUAGE_COOKIE_NAME] = 'lt'

    print(f'\n— /{l.pk}/ (tikras HTML)')
    a = c.get(f'/{l.pk}/', follow=True)
    html = a.content.decode('utf-8', 'replace')
    tekstas = be_skriptu(html)
    tikrink(a.status_code == 200, f'200 (gauta {a.status_code})')
    tikrink('Rida' not in tekstas, 'nėra „Rida"',
            ' | '.join(re.sub(r'\s+', ' ', tekstas[m.start() - 80:m.end() + 60])
                       for m in re.finditer('Rida', tekstas))[:300])
    tikrink('Transporto priemonės duomenys' not in tekstas, 'nėra „Transporto priemonės duomenys"')
    tikrink('Detalės duomenys' in tekstas, 'yra „Detalės duomenys"')
    bruksniai = [re.sub(r'\s+', ' ', re.sub('<[^>]+>', ' ', tekstas[m.start() - 200:m.end()]))[-90:]
                 for m in re.finditer(r'>\s*—\s*<', tekstas)]
    tikrink(not bruksniai, 'nėra tuščių „—" eilučių', ' | '.join(bruksniai))
    tikrink(re.search(r'data-ikelta>\d{4}-\d{2}-\d{2}<', html) is not None
            and 'Įkelta' in tekstas, f'yra įkėlimo data ({l.created_at:%Y-%m-%d})')
    kelias = re.search(r'<nav class="mb-6">(.*?)</nav>', html, re.S)
    kelias = kelias.group(1) if kelias else ''
    tikrink('?kategorija=parts' in kelias and '>Dalys<' in kelias
            and 'Naršyti automobilius' not in kelias,
            'naršymo kelias „Dalys" → /skelbimai/?kategorija=parts',
            re.sub(r'\s+', ' ', re.sub('<[^>]+>', ' ', kelias)).strip())
    tikrink(KODAS in tekstas, f'detalės numeris {KODAS} matosi')

    print('\n— /skelbimai/?kategorija=parts kortelė')
    a = c.get('/skelbimai/?kategorija=parts', follow=True)
    html = a.content.decode('utf-8', 'replace')
    m = re.search(rf'<div class="sk-kort" data-skelbimas="{l.pk}">(.*?)<div class="sk-veiksmai">',
                  html, re.S)
    kortele = m.group(1) if m else ''
    tikrink(bool(kortele), f'kortelė #{l.pk} yra sąraše')
    spec = re.search(r'<div class="sk-spec">(.*?)</div>', kortele, re.S)
    spec = spec.group(1).strip() if spec else ''
    tikrink(KODAS in spec, f'kortelėje detalės numeris („{spec}")')
    tikrink('2019' in spec, 'kortelėje metai')
    tikrink('2 nuotr.' in spec, 'kortelėje nuotraukų skaičius')
    tikrink(kuras.name not in spec, f'kortelėje NĖRA kuro tipo („{kuras.name}")')

    print(f'\n════ {gerai} gerai / {blogai} blogai ════')
    return 1 if blogai else 0


if __name__ == '__main__':
    with override_settings(MEDIA_ROOT=MEDIA):
        kodas = main()
    sys.exit(kodas)
