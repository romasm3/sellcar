# -*- coding: utf-8 -*-
"""
KŪRIMO FORMOS ATSIDARO — visos, ir visi dalių potipiai.

Klaida, dėl kurios šitas testas atsirado: /create/parts/form/?sub=… grąžino
500, ir dalies įkelti buvo neįmanoma IŠVIS. Priežastis — šablone

    val_phone=form_data.phone|default:listing.contact_phone

`listing` kūrimo kelyje konteksto NĖRA, o Django filtro ARGUMENTE
trūkstamo kintamojo nenuryja (ignore_failures taikomas tik pagrindinei
išraiškai, ne filtro argumentams — django/template/base.py:731). Todėl
kiekvienas GET krisdavo su VariableDoesNotExist.

Tikrinam du dalykus:
  1. KIEKVIENAS PartCategory potipis (level=2) atidaro formą su 200 —
     ne tik tie keli, kuriuos kas nors atsitiktinai išbandė;
  2. visos kitos kūrimo formos irgi atsidaro — ta pati klaidos šeima
     (šablonas kreipiasi į kintamąjį, kurio vaizdas neduoda) gali būti
     bet kurioje iš jų.

Paleidimas:
    PATIKRA_DB=<...> python docs/kurimo_formu_test.py
"""
import os
import sys

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sqlite_settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'patikra'))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

from django.test import Client                       # noqa: E402

import formu_seed                                    # noqa: E402
from apps.listings.models import PartCategory        # noqa: E402

# Formos, kurių GET turi grąžinti 200 (arba nukreipimą į 200).
KURIMO_KELIAI = [
    '/create/cars/quick/',
    '/create/motorcycle/',
    '/create/trucks/',
    '/create/boats/',
    '/create/trailers/',
    '/create/agriculture/',
    '/create/construction/',
    '/create/construction/attachment/',
    '/create/loading-equipment/',
    '/create/forestry/',
    '/create/camping-houses/',
    '/create/rental/car/',
    '/create/rental/moto/',
    '/create/rental/minibus/',
    '/create/rental/heavy/',
    '/create/services/',
    '/create/electronics/',
    '/create/bicycles/',
    '/create/wheels/',
    '/create/tyres/',
    '/create/rims/',
    '/create/moto-part/',
    '/create/parts/',
    '/create/motogear/',
    '/create/car-for-parts/',
    '/create/moto-for-parts/',
    '/create/truck-for-parts/',
]

gerai = blogai = 0
nesekmes = []


def tikrink(salyga, tekstas, papildomai=''):
    global gerai, blogai
    if salyga:
        gerai += 1
    else:
        blogai += 1
        nesekmes.append(f'{tekstas} — {papildomai}' if papildomai else tekstas)
    print(('  OK   ' if salyga else '  BLOGAI ') + tekstas
          + ('' if salyga or not papildomai else f'\n         {papildomai}'))


def atidaryk(c, kelias):
    """(kodas, klaidos tekstas). Išimtis irgi laikoma nesėkme."""
    try:
        a = c.get(kelias, follow=True)
        return a.status_code, ''
    except Exception as e:                    # noqa: BLE001
        return 500, f'{type(e).__name__}: {str(e)[:200]}'


def main():
    formu_seed.zinynai()
    u = formu_seed.vartotojas()
    c = Client()
    if not c.login(username=u.username, password=formu_seed.SLAPTAZODIS):
        print('NEPAVYKO PRISIJUNGTI'); return 1

    potipiai = list(PartCategory.objects.filter(
        level=PartCategory.LEVEL_SUBCATEGORY, is_active=True
    ).values_list('slug', flat=True))

    print(f'\n— Dalių potipiai ({len(potipiai)} vnt.)')
    if not potipiai:
        print('  (DB nėra nė vieno PartCategory potipio — patikra neinformatyvi)')
    for slug in potipiai:
        kodas, klaida = atidaryk(c, f'/create/parts/form/?sub={slug}')
        tikrink(kodas == 200, f'/create/parts/form/?sub={slug}',
                klaida or f'HTTP {kodas}')

    print('\n— Kitos kūrimo formos')
    for kelias in KURIMO_KELIAI:
        kodas, klaida = atidaryk(c, kelias)
        tikrink(kodas == 200, kelias, klaida or f'HTTP {kodas}')

    print(f'\n════ {gerai} gerai / {blogai} blogai ════')
    for n in nesekmes:
        print('   ·', n)
    return 1 if blogai else 0


if __name__ == '__main__':
    sys.exit(main())
