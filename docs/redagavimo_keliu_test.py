# -*- coding: utf-8 -*-
"""
KIEKVIENOS KATEGORIJOS REDAGAVIMO KELIAS NEBAIGIASI 500.

Kas buvo. /create/motorcycle/?edit=<id> ir /create/motogear/?edit=<id>
grąžindavo 500 kiekvieną kartą, nesvarbu, kas formoje — krisdavo net
užpildžius visus laukus. Priežastis abiejuose ta pati:

    issaugok_pasta(listing, request)      # ← `listing`
    ...
    listing = _save_draft_fields(...)     # ← atsiranda TIK ČIA

Redagavimo objektas tuose vaizduose vadinasi `edit_listing`, o `listing`
sukuriamas tik kuriant naują skelbimą ir tik žemiau. Redaguojant jis
nesukuriamas niekada, tad kelias visada baigdavosi UnboundLocalError.
Automobiliuose (views.py) to nebuvo, nes ten yra vienas bendras
`target = listing if is_edit_mode else current_draft`.

Šis testas atidaro KIEKVIENOS kategorijos redagavimo formą ir pateikia
ją nieko nekeitus. Laukiama bet ko, tik ne 500 ir ne išimties: 302
(išsaugota) arba 200 (forma su klaidų žinutėmis) abu tinka — tikrinam,
kad kelias apskritai nebelūžta.

Antra dalis: nepavykęs pateikimas neturi palikti juodraščio. „Visas
automobilis / motociklas / sunkvežimis dalimis" formos juodraščio eilutę
kurdavo POST'o pradžioje, dar prieš patikrą, tad kiekvienas nepavykęs
bandymas palikdavo DB tuščią „Untitled draft".

Paleidimas:  python docs/redagavimo_keliu_test.py
"""
import os, re, sys, tempfile, traceback

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
for k, v in (('SECRET_KEY', 'x'), ('EMAIL_USER', 'x@x.lt'), ('EMAIL_PASSWORD', 'x')):
    os.environ.setdefault(k, v)

import django
from django.conf import settings

LAIKINA = tempfile.mkdtemp(prefix='redagavimas-')
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
call_command('migrate', run_syncdb=True, verbosity=0)

from django.contrib.auth import get_user_model
from django.test import Client

from apps.listings.models import (Listing, SubCategory, VehicleType,
                                  WheelListing)

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


U = get_user_model()
u = U.objects.create_user(username='p@x.lt', email='p@x.lt', password='x')
if hasattr(u, 'profile'):
    u.profile.language = 'lt'
    u.profile.phone_number = '+37060000000'
    u.profile.save()


def vt(slug):
    o, _ = VehicleType.objects.get_or_create(slug=slug, defaults={'name': slug})
    return o


def sc(vt_slug, slug):
    o, _ = SubCategory.objects.get_or_create(
        vehicle_type=vt(vt_slug), slug=slug, defaults={'name': slug})
    return o


def skelbimas(vt_slug, sub_slug=None, **extra):
    kw = dict(seller=u, vehicle_type=vt(vt_slug), title='Testas %s' % vt_slug,
              year=2018, mileage=1000, price=1000, currency='EUR',
              country='LT', city='Vilnius', status='active',
              condition='used', defects='none')
    kw.update(extra)
    if sub_slug:
        kw['subcategory'] = sc(vt_slug, sub_slug)
    return Listing.objects.create(**kw)


def laukai_is_formos(h):
    """Ką naršyklė pateiktų nieko nekeitus — įrašytos reikšmės iš HTML."""
    d = {}
    for m in re.finditer(r'<input[^>]*>', h):
        t = m.group(0)
        vardas = re.search(r'name="([^"]+)"', t)
        if not vardas or 'type="file"' in t:
            continue
        if 'type="checkbox"' in t or 'type="radio"' in t:
            if 'checked' in t:
                v = re.search(r'value="([^"]*)"', t)
                d.setdefault(vardas.group(1), v.group(1) if v else 'on')
            continue
        v = re.search(r'value="([^"]*)"', t)
        d[vardas.group(1)] = v.group(1) if v else ''
    for m in re.finditer(r'<select[^>]*name="([^"]+)".*?</select>', h, re.S):
        pasirinkta = re.search(r'<option value="([^"]*)"[^>]*selected', m.group())
        d[m.group(1)] = pasirinkta.group(1) if pasirinkta else ''
    for m in re.finditer(r'<textarea[^>]*name="([^"]+)"[^>]*>(.*?)</textarea>', h, re.S):
        d[m.group(1)] = m.group(2)
    d.pop('equipment', None)          # Alpine šablonas, ne tikra reikšmė
    return d


def redaguok(zyme, pk, tiesiogine_nuoroda=None):
    """GET /<pk>/edit/ → forma → POST nieko nekeitus. Tikimasi: ne 500."""
    c = Client(raise_request_exception=True)
    c.force_login(u)
    nuoroda = tiesiogine_nuoroda
    try:
        if nuoroda is None:
            r = c.get('/%d/edit/' % pk)
            tikrink(r.status_code == 302,
                    '%s: /%d/edit/ turi nukreipti į savo formą (gauta %s)'
                    % (zyme, pk, r.status_code))
            if r.status_code != 302:
                return
            nuoroda = r['Location']
        g = c.get(nuoroda, follow=True)
        tikrink(g.status_code == 200,
                '%s: %s neatsidaro (%s)' % (zyme, nuoroda, g.status_code))
        if g.status_code != 200:
            return
        p = c.post(nuoroda, laukai_is_formos(g.content.decode()), follow=False)
        tikrink(p.status_code != 500,
                '%s: pateikus nieko nekeitus gautas 500' % zyme)
        tikrink(p.status_code in (200, 302),
                '%s: netikėta būsena %s' % (zyme, p.status_code))
    except Exception:
        blogai_eilutes = traceback.format_exc().strip().split('\n')[-1]
        tikrink(False, '%s: išimtis — %s' % (zyme, blogai_eilutes))


antraste('1. Kiekvienos kategorijos redagavimo kelias')

KATEGORIJOS = [
    ('cars',                 'cars',              None,                          {}),
    ('trucks',               'trucks',            None,                          {}),
    ('motorcycles',          'motorcycles',       None,                          {}),
    ('motogear',             'motorcycles',       'helmets',                     {}),
    ('agriculture',          'agriculture',       None,                          {}),
    ('boats',                'boats',             None,                          {}),
    ('trailers',             'trailers',          None,                          {}),
    ('construction',         'construction',      'other-construction',          {}),
    ('construction/attach',  'construction',      'construction-attachments',
                                                  {'constr_attach_type': 'bucket'}),
    ('forestry',             'forestry',          None,                          {}),
    ('loading-equipment',    'loading-equipment', None,                          {}),
    ('camping-houses',       'camping-houses',    None,                          {}),
    ('bicycles',             'bicycles',          None,                          {}),
    ('electronics',          'electronics',       None,                          {}),
    ('services',             'services',          None,                          {}),
    ('rental/car',           'rental',            'car-rental',                  {}),
    ('rental/moto',          'rental',            'motorcycle-rental',           {}),
    ('rental/minibus',       'rental',            'minibus-touring-water-rental',{}),
    ('rental/heavy',         'rental',            'heavy-trailer-rental',        {}),
    ('car-for-parts',        'parts',             'whole-car-for-parts',         {}),
    ('moto-for-parts',       'parts',             'whole-moto-for-parts',        {}),
    ('truck-for-parts',      'parts',             'whole-truck-for-parts',       {}),
    ('moto-part',            'parts',             'single-moto-part',            {}),
]

for zyme, v, s, papildomai in KATEGORIJOS:
    l = skelbimas(v, s, **papildomai)
    if zyme == 'moto-part':
        # Bendras /<pk>/edit/ moto dalį vestų į bendrą dalių formą.
        redaguok(zyme, l.pk, '/create/moto-part/?edit=%d' % l.pk)
    else:
        redaguok(zyme, l.pk)

# Padangos ir ratlankiai gyvena atskiroje lentelėje, tad ir atskiru adresu.
for zyme, tipas in (('tyres', 'tyre'), ('rims', 'rim')):
    w = WheelListing.objects.create(seller=u, product_type=tipas, price=100,
                                    country='LT', city='Vilnius', status='active')
    redaguok(zyme, w.pk, '/wheels/%d/edit/' % w.pk)


antraste('2. Nepavykęs pateikimas nepalieka juodraščio')

for zyme, nuoroda in (('car-for-parts',   '/create/car-for-parts/'),
                      ('moto-for-parts',  '/create/moto-for-parts/'),
                      ('truck-for-parts', '/create/truck-for-parts/')):
    c = Client()
    c.force_login(u)
    pries = Listing.objects.filter(seller=u, status='draft').count()
    c.get(nuoroda)
    tikrink(Listing.objects.filter(seller=u, status='draft').count() == pries,
            '%s: vien atidarius formą atsirado juodraštis' % zyme)
    # Tyčia nepilna forma — markės nėra, tad patikra nepraeis.
    c.post(nuoroda, {'price': '33'})
    c.post(nuoroda, {'price': '0'})
    tikrink(Listing.objects.filter(seller=u, status='draft').count() == pries,
            '%s: nepavykęs pateikimas paliko juodraštį' % zyme)


antraste('3. Juodraščiai svetimiems nematomi')

juodrastis = skelbimas('cars', None, status='draft', title='Untitled draft')
svetimas = U.objects.create_user(username='k@x.lt', email='k@x.lt', password='x')
if hasattr(svetimas, 'profile'):
    svetimas.profile.language = 'lt'
    svetimas.profile.save()

c = Client()
tikrink(c.get('/%d/' % juodrastis.pk).status_code == 404,
        'juodraštį mato neprisijungęs lankytojas')
c.force_login(svetimas)
tikrink(c.get('/%d/' % juodrastis.pk).status_code == 404,
        'juodraštį mato kitas naudotojas')

from apps.listings.views import _public_listings_qs
tikrink(not _public_listings_qs().filter(pk=juodrastis.pk).exists(),
        'juodraštis patenka į viešą sąrašą')


print('\n' + '═' * 60)
print('gerai: %d, nepavyko: %d' % (gerai, blogai))
sys.exit(1 if blogai else 0)
