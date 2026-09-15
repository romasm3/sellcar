# -*- coding: utf-8 -*-
"""
„DIENOS PASIŪLYMAI" — ATSITIKTINIAI IR IŠ VISŲ KATEGORIJŲ.

Kas buvo (patikrinta gyvai 2026-09-15).

1. Jokio atsitiktinumo. Du perkrovimai iš eilės duodavo TĄ PAČIĄ eilę:
   825, 824, 823, 822, 821, 820, 819, 818, 817, 816 — paprastas
   rikiavimas pagal ID mažėjančiai. Kaltas buvo
   `order_by('-created_at')` su 7 parų filtru: „pasiūlymai" iš tikrųjų
   buvo „naujausi", o naujumui yra atskiras skirtukas.

2. Padangos ir ratlankiai nepatekdavo VISAI. Jie gyvena kitame modelyje
   (`WheelListing`) ir kitu adresu (/wheels/<id>/), o skirtukas ėmė tik
   iš `Listing`. Visos 63 kortelės buvo /<id>/ tipo, nė vienos
   /wheels/<id>/ — nors ratlankių ir padangų buvo dvylika.

Dabar `_dienos_pasiulymai()` traukia atsitiktinai iš ABIEJŲ modelių,
vietas dalydama pagal kiekį, o kortelė adresą ima iš
`get_absolute_url`.

Paleidimas:  python docs/dienos_pasiulymu_test.py
"""
import io, os, re, sys, tempfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
for k, v in (('SECRET_KEY', 'x'), ('EMAIL_USER', 'x@x.lt'), ('EMAIL_PASSWORD', 'x')):
    os.environ.setdefault(k, v)

import django
from django.conf import settings

LAIKINA = tempfile.mkdtemp(prefix='pasiulymai-')
import config.settings as pagrindas
n = {k: v for k, v in vars(pagrindas).items() if k.isupper()}
n.update(
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3',
                           'NAME': os.path.join(LAIKINA, 'db.sqlite3')}},
    SECURE_SSL_REDIRECT=False, SESSION_COOKIE_SECURE=False,
    CSRF_COOKIE_SECURE=False, SECURE_HSTS_SECONDS=0,
    MEDIA_ROOT=LAIKINA, DEBUG=False, ALLOWED_HOSTS=['*'], PASTAS_FONE=False,
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    MOKEJIMAI_IJUNGTI=False, PAYMENTS_ENABLED=False,
    CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}},
    STORAGES={'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
              'staticfiles': {'BACKEND':
                              'django.contrib.staticfiles.storage.StaticFilesStorage'}},
)
settings.configure(**n)
django.setup()

from django.core.management import call_command
from django.test.utils import CaptureQueriesContext, setup_test_environment

setup_test_environment()
call_command('migrate', run_syncdb=True, verbosity=0)

import time

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.db import connection
from django.test import Client

from apps.listings.models import (Listing, VehicleType, WheelImage,
                                  WheelListing)
from apps.listings.templatetags.listing_filters import spec_eilute

gerai = blogai = 0
def tikrink(s, k):
    global gerai, blogai
    if s:
        gerai += 1
    else:
        blogai += 1
        print('  NEPAVYKO: ' + k)
def antraste(t):
    print('\n── ' + t + ' ' + '─' * max(0, 52 - len(t)))


JPEG = bytes.fromhex('ffd8ffe000104a46494600010100000100010000ffd9')

U = get_user_model()
u = U.objects.create_user(username='p@x.lt', email='p@x.lt', password='x')
u.profile.language = 'lt'
u.profile.save()
VT, _s = VehicleType.objects.get_or_create(slug='cars', defaults={'name': 'Automobiliai'})

# Gyva proporcija: ~63 įprasti + 12 ratų
for i in range(63):
    l = Listing.objects.create(
        seller=u, vehicle_type=VT, title='Auto %d' % i, year=2018, mileage=1000,
        price=5000 + i, country='LT', city='Vilnius', status='active',
        condition='used', defects='none')
for i in range(12):
    w = WheelListing.objects.create(
        seller=u, product_type=('tyre' if i < 10 else 'rim'),
        brand_name='Nokian%d' % i, diameter='16', tyre_width='205',
        tyre_profile='55', tyre_season='summer', rim_width='7', quantity=4,
        price=100 + i, country='LT', city='Vilnius', status='active',
        title='Nokian %d 205/55 R16' % i)
    WheelImage.objects.create(listing=w, image=ContentFile(JPEG, name='r%d.jpg' % i))

c = Client()


def pasiulymai():
    r = c.get('/')
    return r, list(r.context['tab_daily']) if r.context else []


def adresai(sarasas):
    return [o.get_absolute_url() for o in sarasas]


# ═══════════════════════════════════════════════════════════════════
antraste('1. Eilė kaskart kitokia')

eiles = []
for _ in range(5):
    r, sar = pasiulymai()
    tikrink(r.status_code == 200, 'titulinis → %s' % r.status_code)
    eiles.append(tuple(adresai(sar)))

tikrink(len(set(eiles)) >= 3,
        'per 5 perkrovimus skirtingų eilių tik %d' % len(set(eiles)))

# Ne ID mažėjimo tvarka
def maziejantis(e):
    nr = [int(re.search(r'(\d+)', a).group(1)) for a in e]
    return nr == sorted(nr, reverse=True)
tikrink(not all(maziejantis(e) for e in eiles),
        'eilė visada rikiuota pagal ID mažėjančiai — atsitiktinumo nėra')

# Ir turinys, ne tik tvarka, turi kisti
aibes = {frozenset(e) for e in eiles}
tikrink(len(aibes) >= 2,
        'kiekvieną kartą tie patys skelbimai, tik permaišyti')


# ═══════════════════════════════════════════════════════════════════
antraste('2. Padangos ir ratlankiai patenka')

su_ratais = 0
for _ in range(5):
    _r, sar = pasiulymai()
    if any(a.startswith('/wheels/') for a in adresai(sar)):
        su_ratais += 1
tikrink(su_ratais == 5,
        'ratlankių pasitaikė tik %d kartus iš 5' % su_ratais)

# Ir įprasti skelbimai neišstumiami
_r, sar = pasiulymai()
adr = adresai(sar)
tikrink(any(not a.startswith('/wheels/') for a in adr),
        'liko vien ratlankiai')
tikrink(len(adr) == 12, 'kortelių %d, laukta 12' % len(adr))

# Dalybos proporcija: 12 ratų iš 75 → apie 2 vietos iš 12
ratu = sum(1 for a in adr if a.startswith('/wheels/'))
tikrink(1 <= ratu <= 5, 'ratlankių vietų %d — neproporcinga' % ratu)


# ═══════════════════════════════════════════════════════════════════
antraste('3. Kortelė veda teisingai ir rodo turinį')

r = c.get('/')
kunas = r.content.decode('utf-8')
wheel_kortele = re.search(
    r'<a data-skelbimas="\d+" href="(/wheels/\d+/)"[^>]*class="home-tab-card.*?</a>',
    kunas, re.S)
bandymai = 0
while not wheel_kortele and bandymai < 15:
    bandymai += 1
    kunas = c.get('/').content.decode('utf-8')
    wheel_kortele = re.search(
        r'<a data-skelbimas="\d+" href="(/wheels/\d+/)"[^>]*class="home-tab-card.*?</a>',
        kunas, re.S)

tikrink(wheel_kortele is not None, 'HTML nėra nė vienos /wheels/ kortelės')
if wheel_kortele:
    k = wheel_kortele.group(0)
    adresas = wheel_kortele.group(1)
    tikrink(c.get(adresas).status_code == 200,
            'kortelės adresas %s neatsidaro' % adresas)
    tikrink('<img' in k and 'home-tab-no-img' not in k,
            'kortelėje nėra nuotraukos')
    kaina = re.search(r'home-tab-price">([^<]*)<', k)
    tikrink(kaina and re.search(r'\d', kaina.group(1)),
            'kortelėje nėra kainos: %s' % (kaina.group(1) if kaina else '—'))
    tikrink(kaina and '€' in kaina.group(1),
            'kainoje nėra € ženklo')
    spec = re.search(r'home-tab-spec">\s*([^<]*)', k)
    tikrink(spec and spec.group(1).strip(),
            'kortelėje nėra specifikacijos eilutės')

# Skersmuo su „R", kaip ir pavadinime
w = WheelListing.objects.filter(product_type='tyre').first()
tikrink('R16' in spec_eilute(w),
        'kortelės eilutėje skersmuo be „R": %r' % spec_eilute(w))

# Modelis moka tą patį, ką Listing
for savybe in ('first_image', 'is_highlighted', 'get_effective_star_level',
               'get_absolute_url', 'currency_symbol'):
    tikrink(hasattr(w, savybe), 'WheelListing neturi %s' % savybe)
tikrink(w.first_image is not None, 'first_image negrąžina nuotraukos')

sablonas = io.open(os.path.join(BASE, 'templates/listings/listing_list.html'),
                   encoding='utf-8').read()
# Kortelė „home-tab-card" su įrašytu listing_detail adresu — būtent dėl jos
# ratlankiai vestų į neegzistuojantį puslapį.
blogos = re.findall(
    r"href=\"{% url 'listing_detail' listing\.pk %}\"[^>]*class=\"home-tab-card",
    sablonas)
tikrink(not blogos,
        'kortelėje vėl įrašytas listing_detail adresas (%d vt.)' % len(blogos))
tikrink('href="{{ listing.get_absolute_url }}" class="home-tab-card' in sablonas,
        'kortelė neima adreso iš get_absolute_url')


# ═══════════════════════════════════════════════════════════════════
antraste('4. Puslapis nesulėtėjo')

c.get('/')                                  # apšilimas
uzklausu, laikai = [], []
for _ in range(3):
    with CaptureQueriesContext(connection) as uzk:
        t0 = time.time()
        c.get('/')
        laikai.append(time.time() - t0)
    uzklausu.append(len(uzk))

vid = sum(uzklausu) / len(uzklausu)
print('   SQL užklausų: %s | laikas vid. %.3f s' % (uzklausu, sum(laikai) / len(laikai)))

# Svarbiausia: užklausų kiekis NEAUGA su kortelių skaičiumi (nėra N+1).
tikrink(max(uzklausu) - min(uzklausu) <= 2,
        'užklausų skaičius svyruoja: %s' % uzklausu)
tikrink(vid < 120, 'per daug užklausų: %.0f' % vid)

# Nuotraukos imamos per prefetch: kai sąrašas jau paimtas, `first_image`
# kiekvienai kortelei NEBETURI kelti naujos užklausos. Būtent tai ir yra
# N+1 riba — 12 kortelių neturi duoti 12 užklausų.
_r, sar = pasiulymai()
with CaptureQueriesContext(connection) as uzk:
    for o in sar:
        _ = o.first_image
tikrink(len(uzk) == 0,
        'first_image kelia %d papildomų užklausų — N+1' % len(uzk))


print('\n' + '═' * 60)
print('gerai: %d, nepavyko: %d' % (gerai, blogai))
sys.exit(1 if blogai else 0)
