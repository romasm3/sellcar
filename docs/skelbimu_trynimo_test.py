# -*- coding: utf-8 -*-
"""SKELBIMŲ TRYNIMO komandos patikra — manage.py trinti_skelbimus.

Dešimt patikrų, abu režimai:

ID režimas — be atsarginės kopijos netrina; nutraukia, kai rastų kiekis
nesutampa su nurodytu; nutraukia, kai saugomas ID pakliuvo į trinamuosius;
sausas bėgimas nieko nekeičia; tikras trynimas išvalo įrašus ir nuotraukų
failus, bet svetimų failų neliečia.

--visus režimas — nutraukia, kai duotas kartu su ID arba be nieko; sausas
bėgimas nieko nekeičia; tikras išvalo ir Listing, ir WheelListing su visais
failais, o naudotojai, markės ir kategorijos lieka vietoje; ant tuščios DB
praeina švariai.

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
from apps.listings.models import (Listing, ListingImage, VehicleType,
                                  WheelListing, WheelImage)

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

# ── 6-9: --visus režimas ───────────────────────────────────────────
def ratlankis(pk, pav):
    w = WheelListing.objects.create(id=pk, title=pav, seller=u, price=100,
                                    status='active')
    d = os.path.join(MEDIA, 'wheels', '2025', '01')
    os.makedirs(d, exist_ok=True)
    f = os.path.join(d, f'{pk}.jpg'); open(f, 'wb').write(b'x' * 10)
    WheelImage.objects.create(listing=w, image=f'wheels/2025/01/{pk}.jpg')
    return w, f

print('\n== 6. --visus kartu su ID — turi nutraukti ==')
def t6():
    try:
        call_command('trinti_skelbimus', 754, visus=True, kopija=KOPIJA, patvirtinu=True)
    except CommandError as e:
        assert 'Rinkis vieną' in str(e), e
        assert Listing.objects.count() == 1
    else:
        raise AssertionError('nenutraukė')
tikrinu('nutraukia, kai --visus duotas kartu su ID', t6)

print('\n== 7. Nei ID, nei --visus — turi nutraukti ==')
def t7():
    try:
        call_command('trinti_skelbimus', kopija=KOPIJA, patvirtinu=True)
    except CommandError as e:
        assert 'Nurodyk ID arba --visus' in str(e), e
    else:
        raise AssertionError('nenutraukė')
tikrinu('nutraukia, kai nenurodyta nieko', t7)

# prisidedam juodraštį ir ratlankį, kad būtų ką valyti
d, df, dg = skelbimas(760, 'Juodraštis')
Listing.objects.filter(pk=760).update(status='draft')
w, wf = ratlankis(900, 'Nokian 205/55')

print('\n== 8. --visus sausas bėgimas — nieko netrina ==')
def t8():
    call_command('trinti_skelbimus', visus=True, kopija=KOPIJA)
    assert Listing.objects.count() == 2, 'sausas bėgimas trynė Listing!'
    assert WheelListing.objects.count() == 1, 'sausas bėgimas trynė WheelListing!'
    assert os.path.exists(cf) and os.path.exists(wf), 'sausas bėgimas trynė failus!'
tikrinu('--visus sausas bėgimas nieko nekeičia', t8)

print('\n== 9. --visus tikras — viskas 0, bet naudotojai/markės lieka ==')
def t9():
    naudotoju = User.objects.count()
    kategoriju = VehicleType.objects.count()
    call_command('trinti_skelbimus', visus=True, kopija=KOPIJA, patvirtinu=True)
    assert Listing.objects.count() == 0, 'liko Listing'
    assert WheelListing.objects.count() == 0, 'liko WheelListing'
    assert ListingImage.objects.count() == 0, 'liko ListingImage'
    assert WheelImage.objects.count() == 0, 'liko WheelImage'
    for f in (cf, cg, df, dg, wf):
        assert not os.path.exists(f), f'liko failas {f}'
    assert User.objects.count() == naudotoju, 'ištrinti naudotojai!'
    assert VehicleType.objects.count() == kategoriju, 'ištrintos kategorijos!'
tikrinu('--visus išvalo abi lenteles + failus, naudotojų neliečia', t9)

print('\n== 10. --visus ant tuščios DB — nelūžta ==')
def t10():
    call_command('trinti_skelbimus', visus=True, kopija=KOPIJA, patvirtinu=True)
    assert Listing.objects.count() == 0
tikrinu('--visus ant tuščios DB praeina švariai', t10)

print('\nVISI TESTAI PRAĖJO')
