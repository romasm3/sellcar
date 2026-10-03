# -*- coding: utf-8 -*-
"""
„+ ĮKELTI" TAŠKELIS antraštėje — mirksi VISIEMS ir VISADA (2026-10-03).

Be JS, be localStorage, be sąlygų. Vienintelė išimtis —
prefers-reduced-motion (be animacijos).

Tikrinam (tikras HTML ir CSS):
  • „+ Įkelti" mygtukas (a.btn-sell[data-ikelti-mygtukas]) yra ir
    neprisijungusiam, ir vartotojui be skelbimų, ir su skelbimais — HTML
    vienodas visiems (jokių sąlyginių klasių)
  • nėra jokio taškelio JS / localStorage / ankstesnės klasės ikelti-demesio
  • CSS: ::before su position:absolute, -3px, 9px, #ff4d2d, 2.6 s pulsas,
    pointer-events:none; .btn-sell position:relative
  • prefers-reduced-motion taisyklė
  • taškelis tik „+ Įkelti", ne „Registruotis" (tą pačią .btn-sell klasę)

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

from apps.listings.models import Listing, VehicleType  # noqa: E402

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


def naudotojas(vardas, su_skelbimu):
    U = get_user_model()
    el = f'{vardas}@ikelti-patikra.lt'
    u = U.objects.filter(email=el).first() or U.objects.create_user(
        username=vardas, email=el, password='x-Patikra-123')
    Listing.objects.filter(seller=u).delete()
    if su_skelbimu:
        vt, _ = VehicleType.objects.get_or_create(slug='parts', defaults={'name': 'Parts'})
        Listing.objects.create(seller=u, vehicle_type=vt, title='Turi', status='active',
                               price=Decimal('10'), city='Kaunas', country='LT', year=2020, mileage=0)
    return u


def puslapis(u=None):
    c = Client()
    c.cookies[settings.LANGUAGE_COOKIE_NAME] = 'lt'
    if u is not None:
        c.force_login(u)
    h = c.get('/', follow=True).content.decode('utf-8', 'replace')
    m = re.search(r'<a [^>]*data-ikelti-mygtukas[^>]*>', h)
    return (m.group(0) if m else ''), h


@override_settings(LANGUAGE_CODE='lt')
def main():
    setup_test_environment()

    print('\n— Mygtukas visiems vienodas')
    variantai = {
        'neprisijungęs': puslapis(),
        'be skelbimų': puslapis(naudotojas('ikelti_be', False)),
        'su skelbimu': puslapis(naudotojas('ikelti_su', True)),
    }
    for kas, (a, h) in variantai.items():
        tikrink('class="btn-sell shrink-0"' in a, f'{kas}: a.btn-sell[data-ikelti-mygtukas] yra', a)
        tikrink('ikelti-demesio' not in h and 'ikelti_demesio_matyta' not in h
                and 'ikelti-matyta' not in h,
                f'{kas}: jokio taškelio JS / localStorage / sąlyginės klasės')

    print('\n— CSS')
    css = open(os.path.join(SAKNIS, 'static/css/bazinis.css'), encoding='utf-8').read()
    blokas = re.search(r'\.btn-sell\[data-ikelti-mygtukas\]::before\s*\{(.*?)\}', css, re.S)
    b = blokas.group(1) if blokas else ''
    for dalis in ('content: ""', 'position: absolute', 'top: -3px', 'right: -3px', 'width: 9px',
                  'height: 9px', 'border-radius: 50%', 'background: #ff4d2d',
                  'animation: ikelti-tasko-pulsas 2.6s ease-in-out infinite', 'pointer-events: none'):
        tikrink(dalis in b, f'::before — {dalis}')
    tikrink(re.search(r'\.btn-sell \{\s*position: relative;', css) is not None, '.btn-sell position:relative')
    tikrink(re.search(r'@keyframes ikelti-tasko-pulsas\s*\{\s*0%, 100% \{ opacity: 1;\s+transform: scale\(1\); \}'
                      r'\s*50%\s+\{ opacity: \.35; transform: scale\(\.8\); \}', css) is not None,
            '@keyframes: 1 → .35 / scale .8')
    tikrink(re.search(r'@media \(prefers-reduced-motion: reduce\)\s*\{\s*'
                      r'\.btn-sell\[data-ikelti-mygtukas\]::before \{ animation: none; \}', css) is not None,
            'prefers-reduced-motion taisyklė')
    tikrink(not re.search(r'\.btn-sell::before', css),
            'taškelis ne visiems .btn-sell (ir „Registruotis") — tik [data-ikelti-mygtukas]')
    _a, h = variantai['neprisijungęs']
    reg = re.search(r'<a [^>]*accounts/register[^>]*btn-sell[^>]*>', h)
    tikrink(reg is None or 'data-ikelti-mygtukas' not in reg.group(0),
            '„Registruotis" mygtukas be data-ikelti-mygtukas')

    print(f'\n════ {gerai} gerai / {blogai} blogai ════')
    return 1 if blogai else 0


if __name__ == '__main__':
    sys.exit(main())
