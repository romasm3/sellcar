# -*- coding: utf-8 -*-
"""
DALIŲ FORMA IR KATEGORIJŲ MEDIS — LIETUVIŠKAI.

Klaida: su LT kalba /create/parts/ rodė visas 19 kategorijų ir 294 lapus
angliškai, o forma buvo pusiau išversta („Part Name", „Condition",
„Brand" šalia „Modelis", „Telefonas").

Vertimai eina per .po (locale/lt/LC_MESSAGES/django.po):
  • medis — PartCategory.pavadinimas → pgettext('dalių kategorija', name_en)
  • forma — {% trans %} parts_listing_create.html
Slug'ai (URL raktai) NEKEIČIAMI.

Tikrinam:
  • /create/parts/ ir /create/parts/form/?sub=lighting-front-lights-headlight
    išvestame HTML nėra „Part Name", „Condition", „Brand", „Gearbox",
    „Body Type", „Photos", „Lighting", „Brakes", „Headlight"
  • yra lietuviški atitikmenys
  • AJAX medis ir paieška grąžina LT pavadinimus, slug'ai tie patys
  • VISI 347 medžio pavadinimai (19 + 35 + 294) turi LT vertimą kataloge

Reikia sukompiliuoto .mo:  python manage.py compilemessages -l lt

Paleidimas (TIK su laikina sqlite baze, ne produkcijoje):
    PATIKRA_DB=<laikinas failas> python docs/daliu_vertimu_test.py
"""
import os
import sys

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sqlite_settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'patikra'))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

import re                                            # noqa: E402

from django.conf import settings                     # noqa: E402
from django.test import Client, override_settings    # noqa: E402
from django.test.utils import setup_test_environment  # noqa: E402
from django.utils import translation                 # noqa: E402

import formu_seed                                    # noqa: E402
from apps.listings.models import PartCategory, VehicleType  # noqa: E402

LAPAS = 'lighting-front-lights-headlight'
# (slug, name_en, lygis, tėvo slug, order)
MEDIS = [
    ('lighting', 'Lighting', 0, None, 0),
    ('lighting-front-lights', 'Front Lights', 1, 'lighting', 1),
    (LAPAS, 'Headlight', 2, 'lighting-front-lights', 0),
    ('brakes', 'Brakes', 0, None, 2),
    ('brakes-brake-parts', 'Brake Parts', 1, 'brakes', 0),
    ('brakes-brake-parts-brake-disc', 'Brake Disc', 2, 'brakes-brake-parts', 0),
]
DRAUDZIAMI = ['Part Name', 'Condition', 'Brand', 'Gearbox', 'Body Type',
              'Photos', 'Lighting', 'Brakes', 'Headlight']

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
    VehicleType.objects.get_or_create(slug='parts', defaults={'name': 'Parts'})
    mazgai = {}
    for slug, vardas, lygis, tevas, eile in MEDIS:
        m, _ = PartCategory.objects.update_or_create(slug=slug, defaults=dict(
            name_en=vardas, level=lygis, parent=mazgai.get(tevas),
            order=eile, is_active=True))
        mazgai[slug] = m


def angliski(html):
    """Draudžiami žodžiai išvestame HTML — su kontekstu, kad būtų aišku kur."""
    rasta = []
    for zodis in DRAUDZIAMI:
        for m in re.finditer(rf'\b{re.escape(zodis)}\b', html):
            rasta.append(f'„{zodis}": …{html[max(0, m.start() - 50):m.end() + 30]!r}…')
    return rasta


@override_settings(LANGUAGE_CODE='lt')
def main():
    setup_test_environment()
    pasejk()
    c = Client()
    c.cookies[settings.LANGUAGE_COOKIE_NAME] = 'lt'
    c.force_login(formu_seed.vartotojas())

    print('\n— /create/parts/')
    a = c.get('/create/parts/', follow=True, HTTP_ACCEPT_LANGUAGE='lt')
    html = a.content.decode('utf-8', 'replace')
    tikrink(a.status_code == 200, f'200 (gauta {a.status_code})')
    blogi = angliski(html)
    tikrink(not blogi, 'angliškų užrašų nėra', '\n         '.join(blogi[:8]))
    for lt in ('Apšvietimas', 'Stabdžiai'):
        tikrink(lt in html, f'yra „{lt}"')
    for slug in ('lighting', 'brakes'):
        tikrink(re.search(rf'["\'=]{slug}["\'&]', html) is not None,
                f'slug\'as „{slug}" nepasikeitęs')

    print('\n— /create/parts/form/?sub=' + LAPAS)
    a = c.get(f'/create/parts/form/?sub={LAPAS}', follow=True, HTTP_ACCEPT_LANGUAGE='lt')
    html = a.content.decode('utf-8', 'replace')
    tikrink(a.status_code == 200, f'200 (gauta {a.status_code})')
    blogi = angliski(html)
    tikrink(not blogi, 'angliškų užrašų nėra', '\n         '.join(blogi[:8]))
    for lt in ('Dalies pavadinimas', 'Detalės numeris', 'Būklė', 'Markė',
               'Pavarų dėžė', 'Kėbulo tipas', 'Nuotraukos', 'Varantieji ratai',
               'Priekinis žibintas', 'Apšvietimas', 'Priekiniai žibintai',
               '>Nauja<', '>Su defektais<', 'pvz. 63217160797'):
        tikrink(lt in html, f'yra „{lt}"')
    tikrink(f'name="sub" value="{LAPAS}"' in html,
            f'formoje slug\'as „{LAPAS}" nepasikeitęs')

    print('\n— AJAX medis ir paieška')
    from django.urls import reverse
    j = c.get(reverse('parts_subtree_ajax'), {'category_slug': 'lighting'})
    d = j.json() if j.status_code == 200 else {}
    vaikai = [v for g in d.get('groups', []) for v in g['children']]
    tikrink(d.get('category_name') == 'Apšvietimas',
            f'kategorija „Apšvietimas" (gauta {d.get("category_name")!r})')
    tikrink({'name': 'Priekinis žibintas', 'slug': LAPAS} in vaikai,
            'lapas „Priekinis žibintas" su tuo pačiu slug\'u', f'gauta {vaikai}')

    for q in ('žibintas', 'Headlight'):
        r = c.get(reverse('parts_search_ajax'), {'q': q}).json().get('results', [])
        tikrink(any(x['slug'] == LAPAS and x['name'] == 'Priekinis žibintas' for x in r),
                f'paieška „{q}" randa „Priekinis žibintas"', f'gauta {r}')

    print('\n— Visi medžio pavadinimai kataloge')
    import ast
    from apps.listings.translatable_db import PART_CATEGORY_NAMES
    # msgid'ai tiesiai iš šaltinio — lazy objektas jų neatskleidžia
    medis = ast.parse(open(os.path.join(settings.BASE_DIR, 'apps', 'listings',
                                        'translatable_db.py'), encoding='utf-8').read())
    msgid = [n.args[1].value for n in ast.walk(medis)
             if isinstance(n, ast.Call) and getattr(n.func, 'id', '') == 'pgettext_lazy'
             and n.args[0].value == 'dalių kategorija']
    with translation.override('lt'):
        neisversti = [m for m in msgid
                      if translation.pgettext('dalių kategorija', m) == m]
    tikrink(len(PART_CATEGORY_NAMES) == 347, f'347 pavadinimai (yra {len(PART_CATEGORY_NAMES)})')
    tikrink(not neisversti, 'visi išversti į LT', f'neišversti: {neisversti[:15]}')

    print(f'\n════ {gerai} gerai / {blogai} blogai ════')
    return 1 if blogai else 0


if __name__ == '__main__':
    sys.exit(main())
