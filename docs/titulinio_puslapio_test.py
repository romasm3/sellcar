# -*- coding: utf-8 -*-
"""Titulinis nuo galo iki galo — tikras view, tikras šablonas, sqlite.

Papildo docs/titulinio_srautu_test.py: tas tikrina atrankos taisykles,
o šitas — kad titulinis su jomis atsidaro ir rodo tai, ką turi.

Tikrinama tai, kas 2026-09-22 buvo sugedę gyvai:
padangos ir ratlankiai (WheelListing, /wheels/<id>/) nesimatė nei
skaitliukuose, nei skirtukuose; „Pasiūlymai" buvo vien automobiliai;
„Dienos pasiūlymai" tušti; skirtukų pavadinimai vienaskaitoje.

Paleidimas:
    PYTHONPATH=docs/patikra python docs/titulinio_puslapio_test.py

Vertimams reikia sukompiliuoto locale/lt/.../django.mo. Jo repo nėra
(gamina deploy'as), tad be jo pavadinimų patikros praleidžiamos.
"""
import os, re, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
sys.path.insert(0, os.path.join(BASE, 'docs', 'patikra'))

# config.settings šitų reikalauja be numatytųjų — patikrai užtenka tuščių.
for kintamasis, reiksme in (('SECRET_KEY', 'patikra'), ('DEBUG', 'True'),
                            ('ALLOWED_HOSTS', '*'), ('EMAIL_USER', 'x'),
                            ('EMAIL_PASSWORD', 'x'),
                            ('STRIPE_SECRET_KEY', 'sk_test_x'),
                            ('STRIPE_PUBLISHABLE_KEY', 'pk_test_x'),
                            ('STRIPE_WEBHOOK_SECRET', 'whsec_x')):
    os.environ.setdefault(kintamasis, reiksme)
os.environ.setdefault('PATIKRA_DB', os.path.join(BASE, '.patikra_titulinis.sqlite3'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'sqlite_settings'

import django
django.setup()

from decimal import Decimal
from django.core.management import call_command
from django.test import Client
from django.contrib.auth.models import User
from apps.listings.models import Listing, VehicleType, WheelListing

call_command('migrate', verbosity=0, run_syncdb=True)

KLAIDOS = []
NARSYKLE = 'Mozilla/5.0 (X11; Linux x86_64)'


def tikrinu(pav, ok, papild=''):
    print((u'  ✓ ' if ok else u'  ✗ ') + pav + (u'   %s' % (papild,) if papild else ''))
    if not ok:
        KLAIDOS.append(pav)


# ── Duomenys: kaip gyvai — daug automobilių, 10 padangų, 2 ratlankiai ──
u, _ = User.objects.get_or_create(username='patikra', defaults={'email': 'p@x.lt'})
Listing.objects.all().delete()
WheelListing.objects.all().delete()

TIPAI = {}
for slug, vardas in (('cars', 'Automobiliai'), ('motorcycles', 'Motociklai'),
                     ('trucks', 'Sunkvežimiai'), ('trailers', 'Priekabos'),
                     ('agriculture', 'Žemės ūkio technika')):
    TIPAI[slug], _ = VehicleType.objects.get_or_create(
        slug=slug, defaults={'name': vardas})

for slug, kainos in (('cars', [5000, 7000, 9000, 11000, 13000, 15000, 17000, 19000]),
                     ('motorcycles', [3000, 4000, 4500, 5000, 5500]),
                     ('trucks', [30000]), ('trailers', [8000]),
                     ('agriculture', [50000])):
    for k in kainos:
        Listing.objects.create(
            title='%s %s' % (slug, k), seller=u, vehicle_type=TIPAI[slug],
            price=Decimal(k), year=2021, mileage=1000, city='Vilnius',
            country='LT', description='x', status='active')
for k in (100, 120, 140, 160, 180, 200, 220, 240, 260, 280):
    WheelListing.objects.create(seller=u, product_type='tyre',
                                title='Padanga %s' % k, price=Decimal(k),
                                country='LT', city='Kaunas', status='active')
for k in (300, 400):
    WheelListing.objects.create(seller=u, product_type='rim',
                                title='Ratlankis %s' % k, price=Decimal(k),
                                country='LT', city='Kaunas', status='active')

VISO = Listing.objects.filter(status='active').count() + WheelListing.objects.count()

c = Client()
r = c.get('/', HTTP_USER_AGENT=NARSYKLE)
tikrinu(u'titulinis atsidaro', r.status_code == 200, r.status_code)
if r.status_code != 200:
    sys.exit(1)
h = r.content.decode('utf-8')


def skirtukas(vardas):
    m = re.search(r'x-show="tab === \'%s\'"' % vardas, h)
    if not m:
        return ''
    seg = h[m.start():]
    kitas = re.search(r'x-show="tab === \'', seg[10:])
    return seg[:kitas.start() + 10] if kitas else seg


print(u'\n== 1. Padangos ir ratlankiai matomi ==')
def skaitliukas(zodis):
    m = re.search(re.escape(zodis) + r'</span>\s*<span[^>]*>\((\d+)\)</span>', h)
    return int(m.group(1)) if m else None


tikrinu(u'meniu rodo „Padangos (10)"', skaitliukas('Padangos') == 10,
        skaitliukas('Padangos'))
tikrinu(u'meniu rodo „Ratlankiai (2)"', skaitliukas('Ratlankiai') == 2,
        skaitliukas('Ratlankiai'))
m = re.search(r'text-gray-500 text-lg font-medium">[^0-9<]*(\d+)', h)
rasta = int(m.group(1)) if m else None
tikrinu(u'bendras skaičius apima ir ratlankius (16 + 12 = %d)' % VISO,
        rasta == VISO, rasta)

print(u'\n== 2. Skirtukų turinys ==')
for vardas in ('offers', 'daily', 'newest', 'expensive'):
    seg = skirtukas(vardas)
    print(u'      %-10s %2d kortelės, %d ratlankių'
          % (vardas, seg.count('home-tab-card'),
             len(re.findall(r'href="/wheels/\d+/"', seg))))

seg = skirtukas('offers')
tikrinu(u'„Pasiūlymai" turi /wheels/<id>/ nuorodų',
        len(re.findall(r'href="/wheels/\d+/"', seg)) > 0)
tikrinu(u'„Pasiūlymai" rodo bent 4 korteles', seg.count('home-tab-card') >= 4,
        seg.count('home-tab-card'))
tikrinu(u'„Pasiūlymai" nebe vien automobiliai',
        seg.count('home-tab-card') > len(re.findall(r'href="/wheels/\d+/"', seg)))

seg = skirtukas('daily')
tikrinu(u'„Dienos pasiūlymai" nėra tuščias', seg.count('home-tab-card') > 0,
        seg.count('home-tab-card'))
nuolaidos = re.findall(r'(\d+)% žemiau vidurkio', seg)
tikrinu(u'rodo, kiek pigiau', len(nuolaidos) > 0, nuolaidos[:3])
tikrinu(u'didžiausia nuolaida pirma',
        [int(x) for x in nuolaidos] == sorted([int(x) for x in nuolaidos], reverse=True),
        nuolaidos[:5])

print(u'\n== 3. Tvarka stabili per sesiją ==')
def eile():
    hh = c.get('/', HTTP_USER_AGENT=NARSYKLE).content.decode('utf-8')
    m = re.search(r'x-show="tab === \'offers\'"', hh)
    seg = hh[m.start():]
    k = re.search(r'x-show="tab === \'', seg[10:])
    return re.findall(r'data-skelbimas="(\d+)"', seg[:k.start() + 10] if k else seg)


a, b = eile(), eile()
tikrinu(u'perkrovus tvarka nesikeičia', a == b and len(a) > 0,
        u'%s vs %s' % (a[:4], b[:4]))

print(u'\n== 4. Skirtukų pavadinimai ==')
mygtukai = [x.strip() for x in
            re.findall(r'class="home-tab-btn[^"]*"[^>]*>\s*([^<]+)', h)]
print(u'      %s' % mygtukai)
if 'Newest' in mygtukai:
    print(u'  –  vertimai nesukompiliuoti (.mo nėra) — pavadinimų patikra praleista')
else:
    tikrinu(u'„Naujausi" daugiskaita', 'Naujausi' in mygtukai)
    tikrinu(u'„Brangiausi" daugiskaita', 'Brangiausi' in mygtukai)
    tikrinu(u'vienaskaitos nebeliko',
            'Naujausias' not in mygtukai and 'Brangiausias' not in mygtukai)

print(u'\n== 5. „Populiariausi" ==')
tikrinu(u'be peržiūrų ir įsimintų — skirtukas paslėptas',
        not any('opulia' in x for x in mygtukai), mygtukai)
pirmas = Listing.objects.filter(status='active').order_by('pk').first()
Listing.objects.filter(pk=pirmas.pk).update(views_count=5)
from django.core.cache import cache
cache.clear()
h2 = c.get('/', HTTP_USER_AGENT=NARSYKLE).content.decode('utf-8')
mygtukai2 = [x.strip() for x in
             re.findall(r'class="home-tab-btn[^"]*"[^>]*>\s*([^<]+)', h2)]
tikrinu(u'atsiradus peržiūroms — skirtukas grįžta',
        any('opulia' in x or 'popular' in x.lower() for x in mygtukai2), mygtukai2)

print('')
if KLAIDOS:
    print(u'NEPRAĖJO: %d' % len(KLAIDOS))
    sys.exit(1)
print(u'VISOS PATIKROS PRAĖJO')
