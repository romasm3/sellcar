# -*- coding: utf-8 -*-
"""
RATŲ KORTELĖ RODO NUOTRAUKĄ.

Kas buvo (patikrinta gyvai). /wheels/37/ detaliame puslapyje matėsi
keturios nuotraukos, o tituliniame ir kataloge ta pati prekė — tuščias
pilkas langelis. Visos padangos ir ratlankiai; automobiliai gerai.

Priežastis nebuvo trūkstami duomenys. Bendras kortelės partial'as
`partials/_img.html` piešia `<img src="{{ img.url_lg }}">`, o tokią
savybę turėjo tik `ListingImage`. `WheelImage` teturėjo `image`, tad
Django tyliai išvedė tuščią eilutę — `<img src="">`, pilkas langelis.

Detaliame puslapyje bėdos nesimatė, nes ten kreipiamasi tiesiai į
`image.url`, ne per bendrą partial'ą.

Tikrinam TURINIU, ne akimis: kortelės <img src> turi rodyti į failą,
kuris tikrai egzistuoja, ir abiejų tipų kortelės turi elgtis vienodai.

Paleidimas:  python docs/ratu_korteles_nuotrauka_test.py
"""
import io, os, re, sys, tempfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
for k, v in (('SECRET_KEY', 'x'), ('EMAIL_USER', 'x@x.lt'), ('EMAIL_PASSWORD', 'x')):
    os.environ.setdefault(k, v)

import django
from django.conf import settings

LAIKINA = tempfile.mkdtemp(prefix='ratu-kortele-')
import config.settings as pagrindas
n = {k: v for k, v in vars(pagrindas).items() if k.isupper()}
n.update(
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3',
                           'NAME': os.path.join(LAIKINA, 'db.sqlite3')}},
    SECURE_SSL_REDIRECT=False, SESSION_COOKIE_SECURE=False,
    CSRF_COOKIE_SECURE=False, SECURE_HSTS_SECONDS=0,
    MEDIA_ROOT=os.path.join(LAIKINA, 'media'), MEDIA_URL='/media/',
    DEBUG=False, ALLOWED_HOSTS=['*'], PASTAS_FONE=False,
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

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.template.loader import render_to_string
from django.test import Client

from apps.listings.models import (Listing, ListingImage, VehicleType,
                                  WheelImage, WheelListing)

gerai = blogai = 0
def tikrink(pav, ok, papild=''):
    global gerai, blogai
    print((u'  ✓ ' if ok else u'  ✗ ') + pav + (u'   %s' % (papild,) if papild else ''))
    if ok:
        gerai += 1
    else:
        blogai += 1

# Tikras mažas JPEG — kad ImageField turėtų ką įrašyti.
JPEG = bytes.fromhex(
    'ffd8ffe000104a46494600010100000100010000ffdb004300ffffffffffffff'
    'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff'
    'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffc000'
    '0b080001000101011100ffc40014000100000000000000000000000000000009'
    'ffc40014100100000000000000000000000000000000ffda0008010100003f00'
    '54c1ffd9')

U = get_user_model()
u = U.objects.create_user(username='p', email='p@x.lt', password='x')
VT, _ = VehicleType.objects.get_or_create(slug='cars', defaults={'name': 'Automobiliai'})

auto = Listing.objects.create(
    title='BMW 320 2018', seller=u, vehicle_type=VT, price=Decimal(12000),
    year=2018, mileage=1000, city='Vilnius', country='LT', description='x',
    status='active', condition='used', defects='none')
ListingImage.objects.create(listing=auto, image=ContentFile(JPEG, name='auto.jpg'))

ratas = WheelListing.objects.create(
    seller=u, product_type='tyre', title='Pirelli 235/50 R19',
    price=Decimal(400), country='LT', city='Kaunas', status='active',
    diameter='19', tyre_width='235', tyre_profile='50')
for i in range(4):
    WheelImage.objects.create(listing=ratas,
                              image=ContentFile(JPEG, name='ratas%d.jpg' % i))


print(u'\n== 1. Abu nuotraukų modeliai turi tą patį API ==')
# Bendras partial'as `_img.html` kreipiasi būtent į šituos vardus.
BUTINI = ('url_lg', 'url_lg_webp', 'url_sm', 'url_sm_webp')
li = auto.first_image
wi = ratas.first_image
tikrink(u'automobilis turi first_image', li is not None)
tikrink(u'ratas turi first_image', wi is not None)
for savybe in BUTINI:
    tikrink(u'ListingImage.%-14s' % savybe, hasattr(li, savybe))
    tikrink(u'WheelImage.%-16s' % savybe, hasattr(wi, savybe))
tikrink(u'WheelImage.url_lg rodo į failą',
        bool(wi.url_lg) and wi.url_lg.startswith('/media/'), wi.url_lg)
tikrink(u'automobilio url_lg rodo į failą',
        bool(li.url_lg) and li.url_lg.startswith('/media/'), li.url_lg)


print(u'\n== 2. Bendras partial\'as išveda <img src> abiem ==')
for vardas, img in ((u'automobilis', li), (u'ratas', wi)):
    html = render_to_string('listings/partials/_img.html',
                            {'img': img, 'alt': vardas})
    m = re.search(r'<img[^>]*src="([^"]*)"', html)
    tikrink(u'%-12s <img> yra' % vardas, m is not None)
    if m:
        tikrink(u'%-12s src NETUŠČIAS' % vardas, m.group(1).strip() != '',
                repr(m.group(1)))
        kelias = os.path.join(settings.MEDIA_ROOT,
                              m.group(1).replace('/media/', '', 1))
        tikrink(u'%-12s failas yra diske' % vardas, os.path.exists(kelias),
                m.group(1))


print(u'\n== 3. Titulinio kortelė — ratas rodomas kaip automobilis ==')
c = Client()
h = c.get('/').content.decode('utf-8')

def kortele(adreso_pradzia):
    m = re.search(r'<a data-skelbimas="\d+" href="(%s[^"]*)"[^>]*'
                  r'class="home-tab-card.*?</a>' % adreso_pradzia, h, re.S)
    return m.group(0) if m else None

k_ratas = kortele('/wheels/')
k_auto = kortele('/\\d+/')
tikrink(u'tituliniame yra ratų kortelė', k_ratas is not None)
tikrink(u'tituliniame yra automobilio kortelė', k_auto is not None)
for vardas, k in ((u'ratas', k_ratas), (u'automobilis', k_auto)):
    if not k:
        continue
    m = re.search(r'<img[^>]*src="([^"]*)"', k)
    tikrink(u'%-12s kortelėje yra <img>' % vardas, m is not None,
            u'tuščias langelis' if 'home-tab-no-img' in k else '')
    if m:
        tikrink(u'%-12s kortelės src netuščias' % vardas,
                m.group(1).strip() != '', repr(m.group(1)))
        tikrink(u'%-12s kortelės failas yra' % vardas,
                os.path.exists(os.path.join(
                    settings.MEDIA_ROOT, m.group(1).replace('/media/', '', 1))),
                m.group(1))
    tikrink(u'%-12s be „nėra nuotraukos" ženklo' % vardas,
            'home-tab-no-img' not in k)

print(u'\n== 4. Bendra sąrašų kortelė (_skelbimo_kortele.html) ==')
# Ta pati kortelė piešia /skelbimai/ ir /perziureti/ abiem modeliams;
# duomenis paruošia apps/listings/korteles.py.
from apps.listings import korteles
for vardas, obj in ((u'automobilis', auto), (u'ratas', ratas)):
    i = korteles.kortele(obj)
    tikrink(u'%-12s korteles.kortele() randa nuotrauką' % vardas,
            i['img'] is not None)
    html = render_to_string('listings/partials/_skelbimo_kortele.html', {'i': i})
    m = re.search(r'<img[^>]*src="([^"]*)"', html)
    tikrink(u'%-12s sąrašo kortelėje yra <img>' % vardas, m is not None,
            u'rodomas „be nuotraukos" ženklas' if 'sk-be-nuotraukos' in html else '')
    if m:
        tikrink(u'%-12s sąrašo src netuščias' % vardas,
                m.group(1).strip() != '', repr(m.group(1)))
        tikrink(u'%-12s sąrašo failas yra' % vardas,
                os.path.exists(os.path.join(
                    settings.MEDIA_ROOT, m.group(1).replace('/media/', '', 1))),
                m.group(1))
    tikrink(u'%-12s be „be nuotraukos" ženklo' % vardas,
            'sk-be-nuotraukos' not in html)
    tikrink(u'%-12s kortelės adresas teisingas' % vardas,
            i['url'] in html, i['url'])

print(u'\n== 5. VISI trys nuotraukų modeliai turi tą patį API ==')
# Sargyba nuo pasikartojimo: ratams šitos neatitikties nepagavo joks
# testas — pastebėta akimis, gyvai. TruckImage šiandien pro _img.html
# neina, bet perkėlus sunkvežimius į bendrą kortelę lūžtų taip pat.
from apps.listings.models import TruckImage
for modelis in (ListingImage, TruckImage, WheelImage):
    truksta = [s for s in BUTINI if not hasattr(modelis, s)]
    tikrink(u'%-14s turi visas 4 savybes' % modelis.__name__,
            not truksta, u'trūksta: %s' % truksta if truksta else '')

print('\n' + '=' * 60)
print('gerai: %d, nepavyko: %d' % (gerai, blogai))
sys.exit(1 if blogai else 0)
