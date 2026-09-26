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


def daliu_keliai():
    """Adresai, kuriuos forma TIKRAI atpažįsta, + kiek kurio tipo.

    `parts_listing_create` ieško PartCategory pagal TIKSLŲ `slug`
    (level=2). Svetainės nuorodos statomos iš trijų dalių kelio
    „sekcija-kategorija-lapas" (lighting-rear-lights-rear-light). Jei
    patikra imtų vien lapo trumpą slug'ą (`rear-light`), gautų 302 į
    /create/parts/ — būtent taip anksčiau išėjo „blogų: 294" visiškai
    sveikoje svetainėje.

    Todėl kelią statom iš protėvių, o jei DB tokios eilutės nėra (lapo
    slug'as jau ir yra pilnas kelias), imam patį slug'ą. Abi formos
    suskaičiuojamos atskirai, kad ataskaitoje matytųsi, kaip duomenys
    sutvarkyti.
    """
    keliai, pilnu, savu = [], 0, 0
    lapai = (PartCategory.objects
             .filter(level=PartCategory.LEVEL_SUBCATEGORY, is_active=True)
             .select_related('parent', 'parent__parent'))
    for lapas in lapai:
        dalys = [lapas.slug]
        if lapas.parent:
            dalys.insert(0, lapas.parent.slug)
            if lapas.parent.parent:
                dalys.insert(0, lapas.parent.parent.slug)
        pilnas = '-'.join(dalys)
        if pilnas != lapas.slug and PartCategory.objects.filter(
                slug=pilnas, level=PartCategory.LEVEL_SUBCATEGORY).exists():
            keliai.append(pilnas); pilnu += 1
        else:
            keliai.append(lapas.slug); savu += 1
    return sorted(keliai), pilnu, savu


def atidaryk(c, kelias, turi_likti=None):
    """(kodas, klaidos tekstas). Išimtis irgi laikoma nesėkme.

    `follow=True` reikalingas dėl kalbos priešdėlio (i18n_patterns) — be
    jo KIEKVIENAS atsakymas būtų 302. Bet jis ir pavojingas: nukreipimas
    į /create/parts/ irgi baigiasi 200, tad sulaužytas adresas atrodytų
    geras. Todėl `turi_likti` tikrina, kad galiausiai vis dar esam toje
    pačioje formoje, o ne kategorijų rinkiklyje.
    """
    try:
        a = c.get(kelias, follow=True)
    except Exception as e:                    # noqa: BLE001
        return 500, f'{type(e).__name__}: {str(e)[:200]}'
    if a.status_code != 200:
        return a.status_code, ''
    if turi_likti:
        galutinis = a.redirect_chain[-1][0] if a.redirect_chain else kelias
        if turi_likti not in galutinis:
            return 302, f'nukreipė į {galutinis} (adresas neatpažintas)'
    return 200, ''


def main():
    formu_seed.zinynai()
    u = formu_seed.vartotojas()
    c = Client()
    if not c.login(username=u.username, password=formu_seed.SLAPTAZODIS):
        print('NEPAVYKO PRISIJUNGTI'); return 1

    keliai, pilnu, savu = daliu_keliai()

    print(f'\n— Dalių potipiai ({len(keliai)} vnt.; '
          f'pilnu keliu {pilnu}, savo slug\'u {savu})')
    if not keliai:
        print('  (DB nėra nė vieno PartCategory potipio — patikra neinformatyvi)')
    for sub in keliai:
        kodas, klaida = atidaryk(c, f'/create/parts/form/?sub={sub}',
                                 turi_likti='/create/parts/form/')
        tikrink(kodas == 200, f'/create/parts/form/?sub={sub}',
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
