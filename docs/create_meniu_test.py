# -*- coding: utf-8 -*-
"""
/create/ KATEGORIJŲ RINKIMAS — kaip autogidas.lt/v2/naujas-skelbimas
(CREATE-01, CREATE-02).

  • punktai su pomeniu — <button type="button"> (URL renkantis
    nesikeičia), ne <a href="?step=1&vt=…">;
  • lapai — nuorodos /create/?pick_vt=<id> ir /create/?pick_sub=<id>,
    be step;
  • ?step= nebenaudojamas: /create/?step=1 → 302 /create/, o
    /create/?step=1&pick_sub=<id> → /create/?pick_sub=<id> (senos
    nuorodos nelūžta).

Tikrinam TIKRĄ HTML ir nukreipimus. ID sqlite ir produkcijoje skiriasi,
todėl randam juos pagal slug'ą (produkcijoje: pick_sub=288 — „Atskira
dalis / komplektas", pick_vt=46 — automobiliai).

Paleidimas (TIK su laikina sqlite baze, ne produkcijoje):
    PATIKRA_DB=<laikinas failas> python docs/create_meniu_test.py
"""
import os
import sys

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sqlite_settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'patikra'))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

import re                                            # noqa: E402
from urllib.parse import urlparse                    # noqa: E402

from django.test import Client                       # noqa: E402
from django.test.utils import setup_test_environment  # noqa: E402

import formu_seed                                    # noqa: E402
from apps.listings.models import SubCategory, VehicleType  # noqa: E402

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
    cars, _ = VehicleType.objects.get_or_create(slug='cars', defaults={'name': 'Cars'})
    parts, _ = VehicleType.objects.get_or_create(slug='parts', defaults={'name': 'Parts'})
    dalis, _ = SubCategory.objects.get_or_create(
        vehicle_type=parts, slug='single-part-or-kit',
        defaults={'name': 'Single part / parts kit'})
    return cars, dalis


def kelias(atsakymas):
    return urlparse(atsakymas.get('Location', '')).path


def main():
    setup_test_environment()
    cars, dalis = pasejk()
    c = Client()
    c.force_login(formu_seed.vartotojas())

    print('\n— GET /create/ (tikras HTML)')
    a = c.get('/create/')
    html = a.content.decode('utf-8', 'replace')
    tikrink(a.status_code == 200, f'200 (gauta {a.status_code})')
    nuorodos = re.findall(r'<a\b[^>]*\bhref="([^"]*)"', html)
    blogos = [h for h in nuorodos
              if re.search(r'[?&;](vt|sub)=', h.replace('&amp;', '&'))]
    tikrink(not blogos, 'nė vieno <a> su „vt=" / „sub=" be „pick_"', f'rasta {blogos[:6]}')
    tikrink(not [h for h in nuorodos if 'step=' in h and '/create' in h or h.startswith('?step=')],
            'nėra /create/?step= nuorodų')

    pomeniu = re.findall(r'<(\w+)\b([^>]*\bdata-open="(?:vt|sub)-[^"]*"[^>]*)>', html)
    tikrink(bool(pomeniu), f'yra punktų su pomeniu ({len(pomeniu)})')
    ne_mygtukai = [f'<{t} …>' for t, attrs in pomeniu
                   if t != 'button' or 'type="button"' not in attrs]
    tikrink(not ne_mygtukai, 'visi punktai su pomeniu — <button type="button">',
            f'ne mygtukai: {ne_mygtukai[:5]}')
    tikrink(f'href="/create/?pick_vt={cars.pk}"' in html,
            f'lapas — nuoroda /create/?pick_vt={cars.pk} (be step)')
    lapai = [h for h in nuorodos if 'pick_sub=' in h]
    tikrink(bool(lapai) and all(re.fullmatch(r'/create/\?pick_sub=\d+', h) for h in lapai),
            f'lapai — nuorodos /create/?pick_sub=<id> be step ({len(lapai)})', f'{lapai[:5]}')

    print('\n— Nukreipimai')
    a = c.get(f'/create/?pick_sub={dalis.pk}')
    tikrink(a.status_code == 302 and kelias(a) == '/create/parts/',
            f'/create/?pick_sub={dalis.pk} → 302 /create/parts/', f'{a.status_code} {a.get("Location")}')
    a = c.get(f'/create/?pick_vt={cars.pk}')
    tikrink(a.status_code == 302 and kelias(a) == '/create/cars/quick/',
            f'/create/?pick_vt={cars.pk} → 302 /create/cars/quick/', f'{a.status_code} {a.get("Location")}')
    a = c.get('/create/?step=1')
    tikrink(a.status_code == 302 and a.get('Location') == '/create/',
            '/create/?step=1 → 302 /create/', f'{a.status_code} {a.get("Location")}')
    a = c.get(f'/create/?step=1&pick_sub={dalis.pk}')
    tikrink(a.status_code == 302 and a.get('Location') == f'/create/?pick_sub={dalis.pk}',
            f'sena nuoroda ?step=1&pick_sub={dalis.pk} → /create/?pick_sub={dalis.pk}',
            f'{a.status_code} {a.get("Location")}')
    a = c.get('/create/?step=3')
    tikrink(a.status_code == 302 and a.get('Location') == '/create/',
            '/create/?step=3 → 302 /create/', f'{a.status_code} {a.get("Location")}')

    print(f'\n════ {gerai} gerai / {blogai} blogai ════')
    return 1 if blogai else 0


if __name__ == '__main__':
    sys.exit(main())
