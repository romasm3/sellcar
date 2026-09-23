# -*- coding: utf-8 -*-
"""
„RASTA N SKELBIMŲ" — TAS PATS SKAIČIUS VISOSE TITULINIO SEKCIJOSE.

Kas buvo. Padangos ir ratlankiai gyvena atskiroje `WheelListing`
lentelėje, tad į `filter_listings` nepatenka ir prie šalies juostos
skaičiaus buvo pridedami rankomis — bet TIK `if not params`, t. y. kai
URL'e visai nėra parametrų. `?section=cars` yra parametras, todėl tame
puslapyje iš bendro skaičiaus iškrisdavo VISI ratai:

    /                 Found 47 listings
    /?section=cars    Found 35 listings     <- 12 ratų dingo

Sekcija, puslapis ir rikiavimas paieškos NESIAURINA, tad ratai turi
likti. O tikras filtras (markė, metai, kaina) ratus vis tiek išmeta —
jie tokių laukų neturi, ir juosta žadėtų daugiau, nei parodys sąrašas.

Paleidimas:  python docs/skaitliuko_sekcijos_test.py
"""
import os, sys, tempfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
for k, v in (('SECRET_KEY', 'x'), ('EMAIL_USER', 'x@x.lt'), ('EMAIL_PASSWORD', 'x')):
    os.environ.setdefault(k, v)

import django
from django.conf import settings

LAIKINA = tempfile.mkdtemp(prefix='skaitliukas-')
import config.settings as pagrindas
n = {k: v for k, v in vars(pagrindas).items() if k.isupper()}
n.update(
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3',
                           'NAME': os.path.join(LAIKINA, 'db.sqlite3')}},
    SECURE_SSL_REDIRECT=False, SESSION_COOKIE_SECURE=False,
    CSRF_COOKIE_SECURE=False, SECURE_HSTS_SECONDS=0,
    MEDIA_ROOT=LAIKINA, DEBUG=False, ALLOWED_HOSTS=['*'], PASTAS_FONE=False,
    MOKEJIMAI_IJUNGTI=False, PAYMENTS_ENABLED=False,
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}},
    STORAGES={'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
              'staticfiles': {'BACKEND':
                              'django.contrib.staticfiles.storage.StaticFilesStorage'}},
)
settings.configure(**n)
django.setup()

from django.core.management import call_command
from django.test.utils import setup_test_environment
setup_test_environment()
call_command('migrate', run_syncdb=True, verbosity=0)

import re
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client

from apps.listings import salies_juosta
from apps.listings.models import Listing, VehicleType, WheelListing

gerai = blogai = 0
def tikrink(pav, ok, papild=''):
    global gerai, blogai
    print((u'  ✓ ' if ok else u'  ✗ ') + pav + (u'   %s' % (papild,) if papild else ''))
    if ok:
        gerai += 1
    else:
        blogai += 1

U = get_user_model()
u = U.objects.create_user(username='p', email='p@x.lt', password='x')
SKELBIMU, RATU = 0, 12
for slug, vardas, kiek in (('cars', 'Automobiliai', 20), ('motorcycles', 'Motociklai', 8),
                           ('trucks', 'Sunkvežimiai', 7)):
    vt, _ = VehicleType.objects.get_or_create(slug=slug, defaults={'name': vardas})
    for i in range(kiek):
        Listing.objects.create(
            title='%s %d' % (vardas, i), seller=u, vehicle_type=vt,
            price=Decimal(5000 + i * 100), year=2015 + (i % 8), mileage=1000,
            city='Vilnius', country='LT', description='x', status='active',
            condition='used', defects='none')
        SKELBIMU += 1
for i in range(RATU):
    WheelListing.objects.create(
        seller=u, product_type=('tyre' if i < 10 else 'rim'),
        title='Padanga %d' % i, price=Decimal(60 + i * 20),
        country='LT', city='Kaunas', status='active')

VISO = SKELBIMU + RATU
print('   fikstūra: %d Listing + %d ratai = %d' % (SKELBIMU, RATU, VISO))

c = Client()


def skaicius(adresas):
    cache.clear()
    h = c.get(adresas).content.decode('utf-8')
    m = re.search(r'text-gray-500 text-lg font-medium">[^0-9<]*(\d+)', h)
    return int(m.group(1)) if m else None


print(u'\n== 1. Nefiltruojantys parametrai skaičiaus nekeičia ==')
pagrindas_n = skaicius('/')
tikrink(u'/ rodo visus (%d)' % VISO, pagrindas_n == VISO, pagrindas_n)
for adresas in ('/?section=cars', '/?section=moto', '/?page=2',
                '/?sort=naujausi', '/?section=cars&page=2'):
    n_ = skaicius(adresas)
    tikrink(u'%-26s toks pat' % adresas, n_ == VISO, n_)


print(u'\n== 2. Tikras filtras ratus vis tiek išmeta ==')
# Ratai neturi nei markės, nei metų — su tokiu filtru jų žadėti negalima.
for adresas in ('/?year_min=2018', '/?price_max=6000'):
    n_ = skaicius(adresas)
    tikrink(u'%-22s ratų nebepriduoda' % adresas, n_ is not None and n_ <= SKELBIMU,
            '%s (skelbimų be ratų %d)' % (n_, SKELBIMU))


print(u'\n== 3. _ar_filtruota sprendžia teisingai ==')
from django.http import QueryDict
def qd(s):
    return QueryDict(s, mutable=True)
tikrink(u'tuščia — nefiltruota', salies_juosta._ar_filtruota(qd('')) is False)
for p in ('section=cars', 'page=3', 'sort=naujausi', 'section=cars&page=2'):
    tikrink(u'%-22s nefiltruota' % p, salies_juosta._ar_filtruota(qd(p)) is False)
for p in ('brand=BMW', 'year_min=2018', 'price_max=5000', 'section=cars&brand=BMW'):
    tikrink(u'%-22s FILTRUOTA' % p, salies_juosta._ar_filtruota(qd(p)) is True)
# Tuščia reikšmė nėra filtras: `?brand=` ateina iš neužpildytos formos.
tikrink(u'tuščia reikšmė nefiltruoja',
        salies_juosta._ar_filtruota(qd('brand=&year_min=')) is False)


print(u'\n== 4. Juostos suma sutampa su rodomu skaičiumi ==')
cache.clear()
r = c.get('/?section=cars')
tikrink(u'salies_kiekis = %d' % VISO, int(r.context['salies_kiekis']) == VISO,
        r.context['salies_kiekis'])
cache.clear()
tikrink(u'juostos suma = %d' % VISO,
        sum(salies_juosta.kiekiai(r.wsgi_request).values()) == VISO,
        sum(salies_juosta.kiekiai(r.wsgi_request).values()))

print('\n' + '=' * 60)
print('gerai: %d, nepavyko: %d' % (gerai, blogai))
sys.exit(1 if blogai else 0)
