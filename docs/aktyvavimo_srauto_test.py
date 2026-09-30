# -*- coding: utf-8 -*-
"""
ACT-01: AKTYVAVIMAS PASAKO, KO TRŪKSTA, IR UŽBAIGIAMAS.

Klaida: GET /listings/777/select-plan/ nukreipdavo į redagavimo formą su
„Užpildykite skelbimą prieš jo aktyvavimą", bet formos klaidų JSON būdavo
tuščias ({"laukai": [], "zinutes": {}}) — žmogus nežinojo, ką taisyti, ir
sukosi ratu aktyvuoti → edit → aktyvuoti.

Srautas, kurį tikrinam nuo pradžios iki galo (mokėjimai IŠJUNGTI):
  1. neužpildytas juodraštis (be kainos, miesto, nuotraukų) → select-plan
     → REDAGAVIMAS (/<id>/edit-…/, ne /create/) su KONKREČIAIS laukais
     JSON'e ir klaidų dėžutėje; POST „Aktyvuoti" — tas pats kelias;
  2. užpildom trūkstamus laukus → select-plan → skelbimas aktyvus,
     anoniminis GET /<id>/ → 200;
  3. jokiame žingsnyje — jokio mokėjimo raginimo.

Tikrinam TIKRĄ HTML (su follow=True).

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
from decimal import Decimal                          # noqa: E402

from django.conf import settings                     # noqa: E402
from django.core.files.base import ContentFile       # noqa: E402
from django.test import Client, override_settings    # noqa: E402
from django.test.utils import setup_test_environment  # noqa: E402
from PIL import Image                                # noqa: E402

import formu_seed                                    # noqa: E402
from apps.listings.models import (Listing, ListingImage, SubCategory,  # noqa: E402
                                  VehicleType)

MEDIA = tempfile.mkdtemp(prefix='aktyvavimo_media_')
PAVADINIMAS = 'Patikra aktyvavimo srautas dalimis'
MOKEJIMO_ZODZIAI = ('Stripe', 'Apmokėti', 'Mokėti', 'mokėjim', 'Pasirinkite planą',
                    'checkout', 'Checkout', 'Pay now', 'Choose a plan')

gerai = blogai = 0


def tikrink(salyga, tekstas, papildomai=''):
    global gerai, blogai
    if salyga:
        gerai += 1
        print(f'  OK   {tekstas}')
    else:
        blogai += 1
        print(f'  BLOGAI {tekstas}' + (f'\n         {papildomai}' if papildomai else ''))


def juodrastis(u):
    vt, _ = VehicleType.objects.get_or_create(slug='parts', defaults={'name': 'Parts'})
    sub, _ = SubCategory.objects.get_or_create(
        vehicle_type=vt, slug='whole-car-for-parts', defaults={'name': 'Whole car for parts'})
    l = Listing.objects.filter(seller=u, title=PAVADINIMAS).first() or Listing(
        seller=u, title=PAVADINIMAS)
    l.vehicle_type, l.subcategory, l.status = vt, sub, 'draft'
    l.price, l.city, l.country = Decimal('0'), '—', 'LT'
    l.year, l.mileage = 2015, 180000
    l.save()
    l.images.all().delete()
    return l


def serverio_klaidos(html):
    m = re.search(r'<script type="application/json" id="serverio-klaidos">(.*?)</script>',
                  html, re.S)
    return json.loads(m.group(1)) if m else {}


def be_mokejimo(html, kur):
    rasta = [z for z in MOKEJIMO_ZODZIAI if z in re.sub(r'<script.*?</script>', '', html, flags=re.S)]
    tikrink(not rasta, f'{kur}: jokio mokėjimo raginimo', f'rasta {rasta}')


@override_settings(LANGUAGE_CODE='lt', MOKEJIMAI_IJUNGTI=False, PAYMENTS_ENABLED=False)
def main():
    setup_test_environment()
    u = formu_seed.vartotojas()
    l = juodrastis(u)
    c = Client()
    c.cookies[settings.LANGUAGE_COOKIE_NAME] = 'lt'
    c.force_login(u)

    print(f'\n— 1. Neužpildytas juodraštis #{l.pk} → select-plan')
    a = c.get(f'/listings/{l.pk}/select-plan/', follow=True)
    html = a.content.decode('utf-8', 'replace')
    galas = a.redirect_chain[-1][0] if a.redirect_chain else ''
    tikrink(str(l.pk) in galas and 'edit' in galas and '/create/' not in galas,
            f'nukreipta į REDAGAVIMĄ ({galas})')
    k = serverio_klaidos(html)
    tikrink(bool(k.get('laukai')), f'„laukai" ne tuščias: {k.get("laukai")}')
    for laukas in ('price', 'city', 'images'):
        tikrink(laukas in (k.get('laukai') or []), f'   trūksta „{laukas}"')
    tikrink(bool(k.get('zinutes')) and 'Nurodykite kainą' in (k.get('zinutes') or {}).values(),
            f'„zinutes" užpildytos: {k.get("zinutes")}')
    tikrink('form-error-box' in html and 'Nurodykite kainą' in html
            and 'href="#id_price"' in html,
            'klaidų dėžutėje — konkretūs laukai su nuorodomis')
    be_mokejimo(html, 'redagavimo forma')
    l.refresh_from_db()
    tikrink(l.status == 'draft', 'skelbimas liko juodraštis')

    print('\n— Klaidos parodomos vieną kartą (perkrovus — nebe)')
    html2 = c.get(galas, follow=True).content.decode('utf-8', 'replace')
    tikrink(not serverio_klaidos(html2).get('laukai'), 'antrą kartą sąrašas tuščias')

    print('\n— POST „Aktyvuoti" juodraščiui — tas pats kelias (ne /create/)')
    a = c.post(f'/{l.pk}/activate/', follow=True)
    galas2 = a.redirect_chain[-1][0] if a.redirect_chain else ''
    tikrink(str(l.pk) in galas2 and 'edit' in galas2 and '/create/' not in galas2,
            f'POST activate → redagavimas ({galas2})')
    tikrink(bool(serverio_klaidos(a.content.decode('utf-8', 'replace')).get('laukai')),
            '   su konkrečiais laukais')

    print('\n— 2. Užpildom trūkstamus laukus → select-plan')
    l.price, l.city, l.country = Decimal('1500'), 'Kaunas', 'LT'
    l.save()
    b = io.BytesIO()
    Image.new('RGB', (40, 30), 'gray').save(b, 'JPEG')
    img = ListingImage(listing=l, is_main=True)
    img.image.save('aktyvavimas.jpg', ContentFile(b.getvalue()), save=False)
    img.save()
    a = c.get(f'/listings/{l.pk}/select-plan/', follow=True)
    html = a.content.decode('utf-8', 'replace')
    l.refresh_from_db()
    tikrink(l.status == 'active', f'skelbimas aktyvus (statusas {l.status})')
    be_mokejimo(html, 'po aktyvavimo')
    anonimas = Client()
    r = anonimas.get(f'/{l.pk}/', follow=True)
    tikrink(r.status_code == 200, f'anoniminis GET /{l.pk}/ → 200 (gauta {r.status_code})')

    print(f'\n════ {gerai} gerai / {blogai} blogai ════')
    return 1 if blogai else 0


if __name__ == '__main__':
    with override_settings(MEDIA_ROOT=MEDIA):
        kodas = main()
    sys.exit(kodas)
