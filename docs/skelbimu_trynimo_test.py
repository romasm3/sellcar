# -*- coding: utf-8 -*-
"""SKELBIMŲ TRYNIMO komandos patikra — manage.py trinti_skelbimus.

Tikrinam penkias apsaugas: be atsarginės kopijos netrina, nutraukia kai
rastų kiekis nesutampa su nurodytu, nutraukia kai saugomas ID pakliuvo į
trinamuosius, sausas bėgimas nieko nekeičia, o tikras trynimas išvalo ir
įrašus, ir nuotraukų failus, bet svetimų failų neliečia.

Paleidimas:  python docs/skelbimu_trynimo_test.py
"""
import os, sys, tempfile, django
from django.conf import settings

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
MEDIA = tempfile.mkdtemp(prefix='media_')
os.environ.setdefault('SECRET_KEY', 'x')
settings.configure(
    DEBUG=True, USE_TZ=True, LANGUAGE_CODE='lt', SECRET_KEY='x',
    ALLOWED_HOSTS=['*'], ROOT_URLCONF='config.urls', STRIPE_SECRET_KEY='sk_test_fake',
    MEDIA_ROOT=MEDIA, MEDIA_URL='/media/',
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}},
    DEFAULT_AUTO_FIELD='django.db.models.AutoField',
    INSTALLED_APPS=[
        "django.contrib.admin", "django.contrib.auth", "django.contrib.contenttypes",
        "django.contrib.sessions", "django.contrib.messages", "django.contrib.staticfiles",
        "django.contrib.humanize", "django.contrib.sitemaps",
        "apps.accounts", "apps.listings", "apps.conversations", "apps.broadcasts",
        "apps.imones", "apps.payments", "apps.analytics",
    ],
    TEMPLATES=[{'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [os.path.join(BASE, 'templates')], 'APP_DIRS': True,
                'OPTIONS': {'context_processors': [
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages']}}],
)
django.setup()
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db import connection
from django.contrib.auth.models import User
from apps.listings.models import Listing, ListingImage, VehicleType

call_command('migrate', run_syncdb=True, verbosity=0)

u = User.objects.create_user('t', 't@x.lt', 'x')
vt, _ = VehicleType.objects.get_or_create(slug='cars', defaults={'name': 'Automobiliai'})

def skelbimas(pk, pav):
    l = Listing.objects.create(id=pk, title=pav, seller=u, vehicle_type=vt, price=1000, year=2018,
                             mileage=100000, city='Vilnius', description='x')
    p = os.path.join(MEDIA, 'listings', '2025', '01')
    os.makedirs(p, exist_ok=True)
    f = os.path.join(p, f'{pk}.jpg'); open(f, 'wb').write(b'x' * 10)
    d = os.path.join(MEDIA, 'listings', 'derived', '2025', '01')
    os.makedirs(d, exist_ok=True)
    g = os.path.join(d, f'{pk}_lg.webp'); open(g, 'wb').write(b'x' * 10)
    ListingImage.objects.create(listing=l, image=f'listings/2025/01/{pk}.jpg',
                                image_lg_webp=f'listings/derived/2025/01/{pk}_lg.webp')
    return l, f, g

a, af, ag = skelbimas(748, 'BMW M4')
b, bf, bg = skelbimas(746, 'Audi A6')
c, cf, cg = skelbimas(754, 'Renault T460')   # saugomas

KOPIJA = os.path.join(MEDIA, 'kopija.json')
open(KOPIJA, 'w').write('[' + 'x' * 3000 + ']')

def tikrinu(pavadinimas, f):
    try:
        f(); print(f'  ✓ {pavadinimas}')
    except AssertionError as e:
        print(f'  ✗ {pavadinimas}: {e}'); sys.exit(1)

print('\n== 1. Be kopijos — turi nutraukti ==')
def t1():
    try:
        call_command('trinti_skelbimus', 748, kopija='/nera/tokio.json', patvirtinu=True)
    except CommandError as e:
        assert 'kopijos nėra' in str(e), e
        assert Listing.objects.filter(pk=748).exists(), 'skelbimas dingo!'
    else:
        raise AssertionError('nenutraukė')
tikrinu('nutraukia be kopijos, nieko netrina', t1)

print('\n== 2. Neteisingas kiekis — turi nutraukti ir parodyti nerastus ==')
def t2():
    try:
        call_command('trinti_skelbimus', 748, 746, 999, kopija=KOPIJA, patvirtinu=True)
    except CommandError as e:
        assert '[999]' in str(e), e
        assert Listing.objects.count() == 3, 'kažkas ištrinta!'
    else:
        raise AssertionError('nenutraukė')
tikrinu('nutraukia, kai rasta ≠ nurodyta', t2)

print('\n== 3. Saugomas ID trinamųjų sąraše — turi nutraukti ==')
def t3():
    try:
        call_command('trinti_skelbimus', 748, 754, saugoti=[754], kopija=KOPIJA, patvirtinu=True)
    except CommandError as e:
        assert 'saugomi ID' in str(e), e
        assert Listing.objects.count() == 3
    else:
        raise AssertionError('nenutraukė')
tikrinu('nutraukia, kai saugomas pakliuvo į trinamus', t3)

print('\n== 4. Sausas bėgimas — nieko netrina ==')
def t4():
    call_command('trinti_skelbimus', 748, 746, saugoti=[754], kopija=KOPIJA)
    assert Listing.objects.count() == 3, 'sausas bėgimas trynė!'
    assert os.path.exists(af), 'sausas bėgimas trynė failą!'
tikrinu('sausas bėgimas nieko nekeičia', t4)

print('\n== 5. Tikras trynimas ==')
def t5():
    call_command('trinti_skelbimus', 748, 746, saugoti=[754], kopija=KOPIJA, patvirtinu=True)
    assert not Listing.objects.filter(pk__in=[748, 746]).exists(), 'liko įrašų'
    assert Listing.objects.filter(pk=754).exists(), 'saugomas dingo!'
    assert Listing.objects.count() == 1
    assert ListingImage.objects.count() == 1, 'CASCADE nesuveikė'
    for f in (af, ag, bf, bg):
        assert not os.path.exists(f), f'liko failas {f}'
    for f in (cf, cg):
        assert os.path.exists(f), f'ištrintas svetimas failas {f}!'
tikrinu('ištrina įrašus + failus, saugomo neliečia', t5)

print('\nVISI TESTAI PRAĖJO')
