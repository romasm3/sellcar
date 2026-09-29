# -*- coding: utf-8 -*-
"""
DALIES REDAGAVIMAS NEPERRAŠO PAVADINIMO KATEGORIJA.

Klaida: /create/parts/form/?edit=<id> title laukas buvo užpildomas
sub_name (kategorijos vardu) ir readonly. Išsaugojus redagavimą nieko
nekeitus „BMW M3 G80 galinis bamperis" virsdavo „Galinis bamperis" (po
vertimo — lietuviška kategorija, prieš tai — angliška „Rear Bumper").

Tikrinam TIKRĄ HTML ir DB:
  • ?edit=<id> title value = esamas pavadinimas, ne kategorija
  • laukas NĖRA readonly
  • forma pateikiama nieko nekeitus (visi laukai iš išvesto HTML, kaip
    naršyklė) → išsaugoma, pavadinimas DB nepasikeičia
  • pakeistas pavadinimas išsaugomas (laukas tikrai taisomas)
  • kuriant naują (?sub=) — kategorija kaip pradinė reikšmė, readonly

Paleidimas (TIK su laikina sqlite baze, ne produkcijoje):
    PATIKRA_DB=<laikinas failas> python docs/daliu_redagavimo_pavadinimo_test.py
"""
import os
import sys

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sqlite_settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'patikra'))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

from decimal import Decimal                          # noqa: E402
from html.parser import HTMLParser                   # noqa: E402

from django.conf import settings                     # noqa: E402
from django.test import Client, override_settings    # noqa: E402
from django.test.utils import setup_test_environment  # noqa: E402

import formu_seed                                    # noqa: E402
from apps.listings.models import (Listing, PartCategory,  # noqa: E402
                                  SubCategory, VehicleType)

PAVADINIMAS = 'BMW M3 G80 galinis bamperis'
LAPAS = 'rear-exterior-parts-rear-body-rear-bumper'
KATEGORIJA_LT = 'Galinis bamperis'

gerai = blogai = 0


def tikrink(salyga, tekstas, papildomai=''):
    global gerai, blogai
    if salyga:
        gerai += 1
        print(f'  OK   {tekstas}')
    else:
        blogai += 1
        print(f'  BLOGAI {tekstas}' + (f'\n         {papildomai}' if papildomai else ''))


class Forma(HTMLParser):
    """Surenka #partsForm laukus taip, kaip juos pateiktų naršyklė."""

    def __init__(self):
        super().__init__()
        self.formoje = False
        self.laukai = []          # (vardas, reikšmė)
        self.title_attrs = None
        self._select = None
        self._pasirinkta = None
        self._pirmas = None
        self._textarea = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'form' and a.get('id') == 'partsForm':
            self.formoje = True
        if not self.formoje:
            return
        if tag == 'input' and a.get('name'):
            tipas = (a.get('type') or 'text').lower()
            if a['name'] == 'title':
                self.title_attrs = a
            if tipas in ('file', 'submit', 'button'):
                return
            if tipas in ('checkbox', 'radio') and 'checked' not in a:
                return
            self.laukai.append((a['name'], a.get('value', 'on' if tipas == 'checkbox' else '')))
        elif tag == 'select' and a.get('name'):
            self._select, self._pasirinkta, self._pirmas = a['name'], None, None
        elif tag == 'option' and self._select:
            v = a.get('value', '')
            if self._pirmas is None:
                self._pirmas = v
            if 'selected' in a:
                self._pasirinkta = v
        elif tag == 'textarea' and a.get('name'):
            self._textarea = [a['name'], '']

    def handle_endtag(self, tag):
        if tag == 'form' and self.formoje:
            self.formoje = False
        elif tag == 'select' and self._select:
            v = self._pasirinkta if self._pasirinkta is not None else (self._pirmas or '')
            self.laukai.append((self._select, v))
            self._select = None
        elif tag == 'textarea' and self._textarea:
            self.laukai.append(tuple(self._textarea))
            self._textarea = None

    def handle_data(self, data):
        if self._textarea is not None:
            self._textarea[1] += data


def forma(html):
    p = Forma()
    p.feed(html)
    return p


def pasejk(u):
    vt, _ = VehicleType.objects.get_or_create(slug='parts', defaults={'name': 'Parts'})
    sub, _ = SubCategory.objects.get_or_create(
        vehicle_type=vt, slug='single-part-or-kit', defaults={'name': 'Atskira dalis'})
    medis = {}
    for slug, vardas, lygis, tevas in (
            ('rear-exterior-parts', 'Rear Exterior Parts', 0, None),
            ('rear-exterior-parts-rear-body', 'Rear Body', 1, 'rear-exterior-parts'),
            (LAPAS, 'Rear Bumper', 2, 'rear-exterior-parts-rear-body')):
        m, _ = PartCategory.objects.update_or_create(slug=slug, defaults=dict(
            name_en=vardas, level=lygis, parent=medis.get(tevas), is_active=True))
        medis[slug] = m
    l = Listing.objects.filter(seller=u, oem_code='51128075031-PAV').first() or Listing(seller=u)
    l.title = PAVADINIMAS
    l.vehicle_type, l.subcategory, l.part_category = vt, sub, medis[LAPAS]
    l.condition, l.price, l.year, l.mileage = 'used', Decimal('150'), 2022, 0
    l.city, l.country, l.status = 'Vilnius', 'LT', 'active'
    l.contact_phone = '+37060000000'
    l.oem_code = '51128075031-PAV'
    l.description = 'Originali BMW M dalis.'
    l.save()
    return l


@override_settings(LANGUAGE_CODE='lt')
def main():
    setup_test_environment()
    u = formu_seed.vartotojas()
    l = pasejk(u)
    c = Client()
    c.cookies[settings.LANGUAGE_COOKIE_NAME] = 'lt'
    c.force_login(u)
    url = f'/create/parts/form/?edit={l.pk}'

    print(f'\n— {url} (tikras HTML)')
    a = c.get(url, follow=True)
    html = a.content.decode('utf-8', 'replace')
    tikrink(a.status_code == 200, f'200 (gauta {a.status_code})')
    f = forma(html)
    t = f.title_attrs or {}
    tikrink(t.get('value') == PAVADINIMAS, f'title value = „{PAVADINIMAS}"',
            f'gauta {t.get("value")!r}')
    tikrink(t.get('value') != KATEGORIJA_LT, 'title NE kategorijos vardas')
    tikrink(t and 'readonly' not in t, 'title laukas NĖRA readonly', f'atributai {t}')

    print('\n— Pateikiam nieko nekeitę')
    postas = dict()
    for k, v in f.laukai:
        postas.setdefault(k, []).append(v)
    a = c.post(url, postas)
    tikrink(a.status_code == 302, f'išsaugota (302, gauta {a.status_code})',
            'forma grįžo su klaidomis — išsaugojimas neįvyko' if a.status_code == 200 else '')
    l.refresh_from_db()
    tikrink(l.title == PAVADINIMAS, 'pavadinimas DB nepasikeitė', f'DB: {l.title!r}')

    print('\n— Pavadinimą galima taisyti')
    postas['title'] = [PAVADINIMAS + ' (originalus)']
    c.post(url, postas)
    l.refresh_from_db()
    tikrink(l.title == PAVADINIMAS + ' (originalus)', 'pakeistas pavadinimas išsaugotas',
            f'DB: {l.title!r}')
    l.title = PAVADINIMAS
    l.save(update_fields=['title'])

    print(f'\n— Naujas skelbimas (?sub={LAPAS})')
    html = c.get(f'/create/parts/form/?sub={LAPAS}', follow=True).content.decode('utf-8', 'replace')
    t = forma(html).title_attrs or {}
    tikrink(t.get('value') == KATEGORIJA_LT, f'pradinė reikšmė — kategorija „{KATEGORIJA_LT}"',
            f'gauta {t.get("value")!r}')
    tikrink('readonly' in t, 'kuriant laukas lieka readonly')

    print(f'\n════ {gerai} gerai / {blogai} blogai ════')
    return 1 if blogai else 0


if __name__ == '__main__':
    sys.exit(main())
