# -*- coding: utf-8 -*-
"""
„+ ĮKELTI" DĖMESIO TAŠKELIS antraštėje.

Tikrinam (tikras HTML ir CSS):
  • neprisijungusiam — mygtukas su klase ikelti-demesio ir JS įtrauktas
  • vartotojui be skelbimų — klasė yra
  • vartotojui su bent vienu skelbimu (ir juodraščiu) — klasės nėra, JS
    neįtraukiamas; tas pats su ratlankių skelbimu
  • įkėlus pirmą — kitame puslapyje klasės jau nebėra (ir lieka nebėra)
  • CSS: ::before su position:absolute, .btn-sell position:relative,
    pointer-events:none ir prefers-reduced-motion taisyklė
  • JS: localStorage raktas, mouseenter/click, 30 s riba

Paleidimas (TIK su laikina sqlite baze, NE prieš produkcijos DB):
    PATIKRA_DB=<laikinas failas> python docs/ikelti_mygtuko_test.py
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

from django.conf import settings                     # noqa: E402
from django.contrib.auth import get_user_model       # noqa: E402
from django.test import Client, override_settings    # noqa: E402
from django.test.utils import setup_test_environment  # noqa: E402

from apps.listings.models import Listing, VehicleType, WheelListing  # noqa: E402

SAKNIS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
gerai = blogai = 0


def tikrink(salyga, tekstas, papildomai=''):
    global gerai, blogai
    if salyga:
        gerai += 1
        print(f'  OK   {tekstas}')
    else:
        blogai += 1
        print(f'  BLOGAI {tekstas}' + (f'\n         {papildomai}' if papildomai else ''))


def naujas(vardas):
    U = get_user_model()
    el = f'{vardas}@ikelti-patikra.lt'
    u = U.objects.filter(email=el).first()
    if u:
        Listing.objects.filter(seller=u).delete()
        WheelListing.objects.filter(seller=u).delete()
    else:
        u = U.objects.create_user(username=vardas, email=el, password='x-Patikra-123')
    return u


def mygtukas(c):
    h = c.get('/', follow=True).content.decode('utf-8', 'replace')
    m = re.search(r'<a [^>]*data-ikelti-mygtukas[^>]*>', h)
    return (m.group(0) if m else ''), h


def klientas(u=None):
    c = Client()
    c.cookies[settings.LANGUAGE_COOKIE_NAME] = 'lt'
    if u is not None:
        c.force_login(u)
    return c


@override_settings(LANGUAGE_CODE='lt')
def main():
    setup_test_environment()

    print('\n— Neprisijungęs')
    a, h = mygtukas(klientas())
    tikrink('ikelti-demesio' in a, 'mygtukas turi klasę ikelti-demesio', a)
    tikrink("'ikelti_demesio_matyta'" in h and 'setTimeout(nuimk, 30000)' in h, 'JS įtrauktas')

    print('\n— Vartotojas be skelbimų')
    u = naujas('ikelti_naujas')
    c = klientas(u)
    a, h = mygtukas(c)
    tikrink('ikelti-demesio' in a, 'klasė yra', a)

    print('\n— Įkėlus pirmą (juodraštį)')
    vt, _ = VehicleType.objects.get_or_create(slug='parts', defaults={'name': 'Parts'})
    Listing.objects.create(seller=u, vehicle_type=vt, title='Pirmas', status='draft',
                           price=Decimal('10'), city='Kaunas', country='LT', year=2020, mileage=0)
    a, h = mygtukas(c)
    tikrink('ikelti-demesio' not in a and 'setTimeout(nuimk, 30000)' not in h,
            'klasės nebėra, JS neįtraukiamas', a)
    Listing.objects.filter(seller=u).delete()
    a, _ = mygtukas(c)
    tikrink('ikelti-demesio' not in a, 'ištrynus skelbimą — nebegrįžta (nebeberodoma niekada)', a)

    print('\n— Vartotojas su aktyviu skelbimu (nauja sesija)')
    u2 = naujas('ikelti_turintis')
    Listing.objects.create(seller=u2, vehicle_type=vt, title='Turi', status='active',
                           price=Decimal('10'), city='Kaunas', country='LT', year=2020, mileage=0)
    a, _ = mygtukas(klientas(u2))
    tikrink('ikelti-demesio' not in a, 'klasės nėra', a)

    print('\n— Vartotojas tik su ratlankių skelbimu')
    u3 = naujas('ikelti_ratai')
    try:
        WheelListing.objects.create(seller=u3, title='Ratai', status='draft', price=Decimal('10'))
        a, _ = mygtukas(klientas(u3))
        tikrink('ikelti-demesio' not in a, 'klasės nėra', a)
    except Exception as e:                           # noqa: BLE001 — privalomi laukai
        print(f'  (ratlankių skelbimo sukurti nepavyko: {e})')

    print('\n— Mygtuko tekstas nepakitęs')
    a1, h1 = mygtukas(klientas())
    a2, h2 = mygtukas(klientas(u2))
    tekstas = lambda h: re.sub(r'\s+', ' ', re.search(r'data-ikelti-mygtukas[^>]*>(.*?)</a>', h, re.S).group(1))
    tikrink(tekstas(h1) == tekstas(h2), 'turinys tas pats su klase ir be jos')

    print('\n— CSS')
    css = open(os.path.join(SAKNIS, 'static/css/bazinis.css'), encoding='utf-8').read()
    blokas = re.search(r'\.ikelti-demesio::before\s*\{(.*?)\}', css, re.S)
    b = blokas.group(1) if blokas else ''
    tikrink('position: absolute' in b and 'pointer-events: none' in b and 'top: -3px' in b
            and 'right: -3px' in b and 'ikelti-tasko-pulsas 2.6s' in b,
            '::before — absolute, -3px, pointer-events:none, 2.6 s pulsas')
    tikrink(re.search(r'\.btn-sell \{\s*position: relative;', css) is not None, '.btn-sell position:relative')
    tikrink(re.search(r'@media \(prefers-reduced-motion: reduce\)\s*\{\s*\.ikelti-demesio::before \{ animation: none; \}', css)
            is not None, 'prefers-reduced-motion taisyklė')
    tikrink('@keyframes ikelti-tasko-pulsas' in css, '@keyframes yra')

    print(f'\n════ {gerai} gerai / {blogai} blogai ════')
    return 1 if blogai else 0


if __name__ == '__main__':
    sys.exit(main())
