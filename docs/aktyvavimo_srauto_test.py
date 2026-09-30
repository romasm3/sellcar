# -*- coding: utf-8 -*-
"""
AKTYVAVIMO SRAUTAS — galutinai (ACT-01, ACT-02, PARTS-12, POST).

    neaktyvus skelbimas → EDIT (ne /create/) → užpildai, ko trūksta →
    „Aktyvuoti skelbimą" (POST) → aktyvus.
Jokio mokėjimo, plano, trukmės ar paslaugų pasirinkimo.

Tikrinam TIKRĄ HTML ir DB:
  1. neužpildytas: aktyvavimas (GET ir POST /listings/<id>/aktyvuoti/)
     → redagavimas su KONKREČIAIS laukais (ne tuščias "laukai": [])
  2. skelbimas be nuotraukų, net jei DB „active" (kaip #869):
     anoniminis GET /<id>/ → 404; savininkas mato „Juodraštis – trūksta"
  3. GET /listings/<id>/select-plan/, GET /aktyvuoti/ ir senas POST
     /<id>/activation-plans/ BŪSENOS NEKEIČIA (aktyvaus nepratęsia)
  4. užpildžius ir POST „Aktyvuoti" → aktyvus, anoniminis GET → 200
  5. jokiame žingsnyje nėra „Mokėjimas", „Paslaugų pasirinkimas",
     „Skelbimo trukmė"; mygtukas — „Aktyvuoti skelbimą"
  6. ištrynus paskutinę aktyvaus skelbimo nuotrauką — nebeviešas

Paleidimas (TIK su laikina sqlite baze, ne produkcijoje):
    PATIKRA_DB=<laikinas failas> python docs/aktyvavimo_srauto_test.py
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
import json                                          # noqa: E402
import re                                            # noqa: E402
from datetime import timedelta                       # noqa: E402
from decimal import Decimal                          # noqa: E402

from django.conf import settings                     # noqa: E402
from django.core.files.base import ContentFile       # noqa: E402
from django.test import Client, override_settings    # noqa: E402
from django.test.utils import setup_test_environment  # noqa: E402
from django.utils import timezone                    # noqa: E402
from PIL import Image                                # noqa: E402

import formu_seed                                    # noqa: E402
from apps.listings.models import (Listing, ListingImage, PartCategory,  # noqa: E402
                                  SubCategory, VehicleType)

MEDIA = tempfile.mkdtemp(prefix='aktyvavimo_media_')
DRAUDZIAMI = ('Mokėjimas', 'Paslaugų pasirinkimas', 'Skelbimo trukmė',
              'Continue to Plan Selection', 'Stripe', 'Apmokėti')

gerai = blogai = 0


def tikrink(salyga, tekstas, papildomai=''):
    global gerai, blogai
    if salyga:
        gerai += 1
        print(f'  OK   {tekstas}')
    else:
        blogai += 1
        print(f'  BLOGAI {tekstas}' + (f'\n         {papildomai}' if papildomai else ''))


def nuotrauka(l, vardas):
    b = io.BytesIO()
    Image.new('RGB', (40, 30), 'gray').save(b, 'JPEG')
    img = ListingImage(listing=l, is_main=True)
    img.image.save(vardas, ContentFile(b.getvalue()), save=False)
    img.save()
    return img


def skelbimas(u, pav, statusas='draft', kaina='0', miestas='—'):
    vt, _ = VehicleType.objects.get_or_create(slug='parts', defaults={'name': 'Parts'})
    sub, _ = SubCategory.objects.get_or_create(
        vehicle_type=vt, slug='whole-car-for-parts', defaults={'name': 'Whole car for parts'})
    l = Listing.objects.filter(seller=u, title=pav).first() or Listing(seller=u, title=pav)
    l.vehicle_type, l.subcategory = vt, sub
    l.price, l.city, l.country = Decimal(kaina), miestas, 'LT'
    l.year, l.mileage, l.status = 2015, 180000, 'draft'
    l.save()
    l.images.all().delete()
    # Būsena tiesiai DB — kaip senas įrašas (#869 buvo „active" be nuotraukų)
    Listing.objects.filter(pk=l.pk).update(
        status=statusas, expires_at=timezone.now() + timedelta(days=30))
    l.refresh_from_db()
    return l


def klaidos(html):
    m = re.search(r'<script type="application/json" id="serverio-klaidos">(.*?)</script>',
                  html, re.S)
    return json.loads(m.group(1)) if m else {}


def be_mokejimo(html, kur):
    tekstas = re.sub(r'<script.*?</script>|<!--.*?-->', '', html, flags=re.S)
    rasta = [z for z in DRAUDZIAMI if z in tekstas]
    tikrink(not rasta, f'{kur}: nėra mokėjimo / plano / trukmės', f'rasta {rasta}')


def html(a):
    return a.content.decode('utf-8', 'replace')


@override_settings(LANGUAGE_CODE='lt', MOKEJIMAI_IJUNGTI=False, PAYMENTS_ENABLED=False)
def main():
    setup_test_environment()
    u = formu_seed.vartotojas()
    c = Client()
    c.cookies[settings.LANGUAGE_COOKIE_NAME] = 'lt'
    c.force_login(u)
    anonimas = Client()

    print('\n— 1. Neužpildytas → aktyvavimas pasako, ko trūksta')
    l = skelbimas(u, 'Patikra aktyvavimo srautas dalimis')
    for metodas in ('get', 'post'):
        a = getattr(c, metodas)(f'/listings/{l.pk}/aktyvuoti/', follow=True)
        galas = a.redirect_chain[-1][0] if a.redirect_chain else ''
        k = klaidos(html(a))
        tikrink(str(l.pk) in galas and 'edit' in galas and '/create/' not in galas,
                f'{metodas.upper()} aktyvuoti → redagavimas ({galas})')
        tikrink(set(k.get('laukai') or []) >= {'price', 'city', 'images'},
                f'   konkretūs laukai: {k.get("laukai")}')
        be_mokejimo(html(a), f'   {metodas.upper()} redagavimo forma')
    l.refresh_from_db()
    tikrink(l.status == 'draft', 'liko juodraštis')

    print('\n— 2. „Aktyvus" DB, bet be nuotraukų (kaip #869)')
    x = skelbimas(u, 'Patikra aktyvus be nuotrauku', statusas='active',
                  kaina='900', miestas='Kaunas')
    tikrink(x.status == 'active' and not x.images.exists(), 'DB: active, 0 nuotraukų')
    r = anonimas.get(f'/{x.pk}/')
    tikrink(r.status_code == 404, f'anoniminis GET /{x.pk}/ → 404 (gauta {r.status_code})')
    h = html(c.get(f'/{x.pk}/'))
    tikrink('Juodraštis' in h and 'trūksta' in h and 'nuotraukos' in h,
            'savininkas mato „Juodraštis – trūksta: nuotraukos"')

    print('\n— 3. GET būsenos nekeičia')
    pilnas = skelbimas(u, 'Patikra pilnas juodrastis', kaina='1200', miestas='Kaunas')
    nuotrauka(pilnas, 'pilnas.jpg')
    for kelias in (f'/listings/{pilnas.pk}/select-plan/', f'/listings/{pilnas.pk}/aktyvuoti/'):
        a = c.get(kelias, follow=True)
        pilnas.refresh_from_db()
        tikrink(pilnas.status == 'draft', f'GET {kelias} → liko juodraštis')
    a = c.get(f'/listings/{pilnas.pk}/aktyvuoti/')
    tikrink(a.status_code == 200 and 'method="post"' in html(a)
            and 'Aktyvuoti skelbimą' in html(a),
            'GET aktyvuoti — puslapis su POST mygtuku „Aktyvuoti skelbimą"')
    be_mokejimo(html(a), '   aktyvavimo puslapis')
    c.post(f'/{pilnas.pk}/activation-plans/', {'plan_id': '1'})
    pilnas.refresh_from_db()
    tikrink(pilnas.status == 'draft', 'senas POST /activation-plans/ nebeaktyvuoja')

    aktyvus = skelbimas(u, 'Patikra jau aktyvus', statusas='active', kaina='800', miestas='Kaunas')
    nuotrauka(aktyvus, 'aktyvus.jpg')
    Listing.objects.filter(pk=aktyvus.pk).update(status='active')
    aktyvus.refresh_from_db()
    pries = aktyvus.expires_at
    c.get(f'/listings/{aktyvus.pk}/select-plan/', follow=True)
    c.get(f'/listings/{aktyvus.pk}/select-plan/', follow=True)
    aktyvus.refresh_from_db()
    tikrink(aktyvus.expires_at == pries, 'GET select-plan aktyvaus NEPRATĘSIA',
            f'{pries} → {aktyvus.expires_at}')

    print('\n— 4. Užpildom → POST „Aktyvuoti" → aktyvus')
    l.price, l.city = Decimal('1500'), 'Kaunas'
    l.save()
    nuotrauka(l, 'aktyvavimas.jpg')
    a = c.post(f'/listings/{l.pk}/aktyvuoti/', follow=True)
    l.refresh_from_db()
    tikrink(l.status == 'active', f'aktyvus (statusas {l.status})')
    be_mokejimo(html(a), '   „pavyko" puslapis')
    r = anonimas.get(f'/{l.pk}/')
    tikrink(r.status_code == 200, f'anoniminis GET /{l.pk}/ → 200 (gauta {r.status_code})')

    print('\n— 5. Kūrimo žingsniai be mokėjimo')
    PartCategory.objects.update_or_create(slug='lighting', defaults=dict(
        name_en='Lighting', level=0, is_active=True))
    be_mokejimo(html(c.get('/create/parts/', follow=True)), '/create/parts/')
    leaf = PartCategory.objects.filter(level=2).first()
    if leaf:
        h = html(c.get(f'/create/parts/form/?sub={leaf.slug}', follow=True))
        tikrink('Aktyvuoti skelbimą' in h, 'dalies formos mygtukas „Aktyvuoti skelbimą"')
        be_mokejimo(h, '   dalies forma')

    print('\n— 6. Ištrynus paskutinę nuotrauką — nebeviešas')
    l.images.all().delete()
    l.refresh_from_db()
    tikrink(l.status == 'draft', f'statusas → draft (yra {l.status})')
    tikrink(anonimas.get(f'/{l.pk}/').status_code == 404, 'anonimui 404')

    print(f'\n════ {gerai} gerai / {blogai} blogai ════')
    return 1 if blogai else 0


if __name__ == '__main__':
    with override_settings(MEDIA_ROOT=MEDIA):
        kodas = main()
    sys.exit(kodas)
