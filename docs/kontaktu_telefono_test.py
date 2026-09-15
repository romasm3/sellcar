# -*- coding: utf-8 -*-
"""
TELEFONAS — PRIE SKELBIMO, NE PRIE PASKYROS.

Kas buvo. `Listing` neturėjo telefono lauko VISAI: kiekviena forma rašė
`request.user.profile.phone_number = …`, o skelbimo puslapis rodė
`listing.seller.profile.phone_number`. Vienas laukas visiems žmogaus
skelbimams — pakeitus numerį viename, jis tyliai pasikeisdavo visuose
kituose, įskaitant senus. Penki skelbimai skirtingose šalyse (#821–#825)
ėmė rodyti tą patį paskutinį įrašytą numerį.

Ratlankiai ir padangos (`WheelListing`) savo `contact_phone` turėjo nuo
pradžių ir veikė teisingai — pagal juos sutvarkytos visos kitos
kategorijos.

Dabar:
  · `Listing.contact_phone` — savas kiekvienam skelbimui;
  · paskyros numeris naudojamas tik kaip PRADINĖ reikšmė naujam skelbimui;
  · paskyros numerio keitimas paskelbtų skelbimų neliečia ir atvirkščiai.

Paleidimas:  python docs/kontaktu_telefono_test.py
"""
import io, os, re, sys, tempfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
for k, v in (('SECRET_KEY', 'x'), ('EMAIL_USER', 'helpautoinfo@gmail.com'),
             ('EMAIL_PASSWORD', 'x')):
    os.environ.setdefault(k, v)

import django
from django.conf import settings

LAIKINA = tempfile.mkdtemp(prefix='kontaktai-')
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
    DEFAULT_FROM_EMAIL='helpautoinfo@gmail.com',
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

import json

from django.contrib.auth import get_user_model
from django.test import Client, RequestFactory

from apps.listings.kontaktai import (issaugok_telefona, telefono_reiksme)
from apps.listings.models import Listing, VehicleType, WheelListing

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
u.profile.language = 'lt'
u.profile.phone_number = '+370 601 00000'
u.profile.show_phone = True
u.profile.save()
c = Client()
c.force_login(u)

VT, _s = VehicleType.objects.get_or_create(slug='cars', defaults={'name': 'Automobiliai'})


def skelbimas(miestas, telefonas='', **extra):
    d = dict(seller=u, vehicle_type=VT, title='Auto ' + miestas, year=2018,
             mileage=1000, price=8000, country='LT', city=miestas,
             status='active', condition='used', defects='none',
             contact_phone=telefonas)
    d.update(extra)
    return Listing.objects.create(**d)


# ═══════════════════════════════════════════════════════════════════
antraste('1. Laukas yra prie skelbimo')

tikrink(any(f.name == 'contact_phone' for f in Listing._meta.concrete_fields),
        'Listing neturi contact_phone')
tikrink(hasattr(Listing, 'kontaktinis_telefonas'),
        'nėra kontaktinis_telefonas savybės')

# Nė vienas vaizdas nebeturi rašyti į paskyrą
rasta = []
for f in sorted(os.listdir(os.path.join(BASE, 'apps/listings'))):
    if not f.endswith('.py'):
        continue
    t = io.open(os.path.join(BASE, 'apps/listings', f), encoding='utf-8').read()
    for nr, e in enumerate(t.split('\n'), 1):
        if e.lstrip().startswith('#'):
            continue
        if re.search(r'\.profile\.phone_number\s*=\s*', e):
            rasta.append('%s:%d' % (f, nr))
tikrink(not rasta, 'vaizdai vis dar rašo numerį į paskyrą: %s' % rasta)


# ═══════════════════════════════════════════════════════════════════
antraste('2. Pagalbinės funkcijos')

rf = RequestFactory()
l = skelbimas('Testas')
issaugok_telefona(l, rf.post('/', {'phone': '  +39 111  '}))
tikrink(l.contact_phone == '+39 111', 'neįrašė arba nenukirpo tarpų: %r' % l.contact_phone)

# Tuščias laukas NIEKO netrina
issaugok_telefona(l, rf.post('/', {}))
tikrink(l.contact_phone == '+39 111', 'tuščias POST ištrynė numerį')
issaugok_telefona(l, rf.post('/', {'phone': '   '}))
tikrink(l.contact_phone == '+39 111', 'tarpai ištrynė numerį')

# Paskyra NEPALIEČIAMA
u.profile.refresh_from_db()
tikrink(u.profile.phone_number == '+370 601 00000',
        'issaugok_telefona pakeitė paskyros numerį')

# Pradinė reikšmė
tuscias = skelbimas('Tuscias')
tikrink(telefono_reiksme(tuscias, u) == '+370 601 00000',
        'naujam skelbimui nepasiūlomas paskyros numeris')
tikrink(telefono_reiksme(l, u) == '+39 111',
        'skelbimo numeris nenugali paskyros')
tikrink(telefono_reiksme(None, u) == '+370 601 00000',
        'be skelbimo negrąžina paskyros numerio')
tikrink(issaugok_telefona(None, rf.post('/', {'phone': 'x'})) == '',
        'None objektas meta klaidą')


# ═══════════════════════════════════════════════════════════════════
antraste('3. Du skelbimai — du numeriai (atkūrimas #821–#825)')

a = skelbimas('Biella', '+39 000 000001')
b = skelbimas('Madridas', '+34 000 000002')

def puslapio_numeris(pk):
    r = c.get('/%d/telefonas/' % pk)
    if r.status_code != 200:
        return 'NĖRA(%s)' % r.status_code
    return json.loads(r.content.decode()).get('telefonas')

tikrink(puslapio_numeris(a.pk) == '+39 000 000001',
        '#1 puslapis rodo %s' % puslapio_numeris(a.pk))
tikrink(puslapio_numeris(b.pk) == '+34 000 000002',
        '#2 puslapis rodo %s' % puslapio_numeris(b.pk))

# Redagavimo forma siūlo ŠIO skelbimo numerį
h = c.get('/create/cars/quick/?edit=%d' % a.pk).content.decode()
m = re.search(r'<input[^>]*name="phone"[^>]*>', h)
v = re.search(r'value="([^"]*)"', m.group(0)) if m else None
tikrink(v and v.group(1) == '+39 000 000001',
        'forma siūlo %s, ne šio skelbimo numerį' % (v.group(1) if v else '—'))

# Keičiam pirmą — antras nejuda
c.post('/create/cars/quick/?edit=%d' % a.pk, {'phone': '+33 000 000003'})
a.refresh_from_db(); b.refresh_from_db(); u.profile.refresh_from_db()
tikrink(a.contact_phone == '+33 000 000003',
        'pirmo skelbimo numeris neįrašytas: %s' % a.contact_phone)
tikrink(b.contact_phone == '+34 000 000002',
        'ANTRO skelbimo numeris pasikeitė: %s' % b.contact_phone)
tikrink(u.profile.phone_number == '+370 601 00000',
        'PASKYROS numeris pasikeitė: %s' % u.profile.phone_number)
tikrink(puslapio_numeris(b.pk) == '+34 000 000002',
        'antro skelbimo puslapis rodo %s' % puslapio_numeris(b.pk))

# Ir atvirkščiai: paskyros keitimas skelbimų neliečia
u.profile.phone_number = '+370 699 99999'
u.profile.save()
a.refresh_from_db(); b.refresh_from_db()
tikrink(a.contact_phone == '+33 000 000003' and b.contact_phone == '+34 000 000002',
        'paskyros keitimas perrašė skelbimus')
tikrink(puslapio_numeris(a.pk) == '+33 000 000003',
        'po paskyros keitimo skelbimas rodo %s' % puslapio_numeris(a.pk))


# ═══════════════════════════════════════════════════════════════════
antraste('4. Senas skelbimas be savo numerio — atsargine lieka paskyra')

senas = skelbimas('Senas', '')
tikrink(senas.kontaktinis_telefonas == '+370 699 99999',
        'be savo numerio negrąžina paskyros: %r' % senas.kontaktinis_telefonas)
tikrink(puslapio_numeris(senas.pk) == '+370 699 99999',
        'senas skelbimas puslapyje be numerio')


# ═══════════════════════════════════════════════════════════════════
antraste('5. El. paštas — ta pati tvarka, be portalo adreso')

tikrink(hasattr(Listing, 'kontaktinis_pastas'), 'nėra kontaktinis_pastas')
sav = skelbimas('Pastas', '+370 1')
tikrink(sav.kontaktinis_pastas == 'p@x.lt',
        'be savo pašto negrąžina paskyros: %s' % sav.kontaktinis_pastas)
sav.contact_email = 'kitas@x.lt'
sav.save()
tikrink(sav.kontaktinis_pastas == 'kitas@x.lt', 'skelbimo paštas nenugali paskyros')

# Portalo adresas skelbime — niekada
PORTALAS = settings.DEFAULT_FROM_EMAIL
tikrink(Listing.objects.filter(contact_email__iexact=PORTALAS).count() == 0,
        'skelbimuose yra portalo palaikymo adresas')

mig = io.open(os.path.join(BASE,
              'apps/listings/migrations/0106_kontaktai_i_skelbima.py'),
              encoding='utf-8').read()
tikrink('DEFAULT_FROM_EMAIL' in mig,
        'migracija nevalo portalo adreso iš skelbimų')
tikrink('contact_phone' in mig, 'migracija neužpildo telefono')


# ═══════════════════════════════════════════════════════════════════
antraste('6. Visos kategorijos — kontaktas prie skelbimo')

# Kiekvienas kūrimo šablonas turi imti numerį iš skelbimo, ne tik iš paskyros
TPL = os.path.join(BASE, 'templates/listings')
blogi = []
for f in sorted(os.listdir(TPL)):
    if not f.endswith('.html'):
        continue
    t = io.open(os.path.join(TPL, f), encoding='utf-8').read()
    for m in re.finditer(r'val_phone=(\S+)', t):
        reiksme = m.group(1)
        # `submitted.phone` ir `step7.phone` vaizde užpildomi iš skelbimo
        # (telefono_reiksme), tad jie irgi tinka — žemiau tai patikrinta
        # ir elgsena, ne tik tekstu.
        if ('contact_phone' in reiksme or 'step7.phone' in reiksme
                or 'submitted.phone' in reiksme):
            continue
        blogi.append('%s: %s' % (f, reiksme))
tikrink(not blogi, 'šablonai ima numerį tik iš paskyros: %s' % blogi)

# Motociklai ir moto apranga numerį paduoda per `submitted` — patikrinam,
# kad ten atsiranda būtent ŠIO skelbimo reikšmė, o ne paskyros.
MOTO_VT, _s = VehicleType.objects.get_or_create(
    slug='motorcycles', defaults={'name': 'Motociklai'})
moto = Listing.objects.create(
    seller=u, vehicle_type=MOTO_VT, title='Moto', year=2018, mileage=1,
    price=1000, country='LT', city='Vilnius', status='active',
    condition='used', defects='none', contact_phone='+370 700 00007')
h = c.get('/create/motorcycle/?edit=%d' % moto.pk).content.decode('utf-8')
m = re.search(r'<input[^>]*name="phone"[^>]*>', h)
v = re.search(r'value="([^"]*)"', m.group(0)) if m else None
tikrink(v and v.group(1) == '+370 700 00007',
        'motociklų forma siūlo %s, ne šio skelbimo numerį'
        % (v.group(1) if v else '—'))

# Skelbimo puslapis — irgi iš skelbimo
det = io.open(os.path.join(BASE, 'templates/listings/listing_detail.html'),
              encoding='utf-8').read()
tikrink('seller.profile.phone_number' not in det,
        'skelbimo puslapis vis dar rodo paskyros numerį')
tikrink(det.count('listing.kontaktinis_telefonas') >= 2,
        'skelbimo puslapis neima numerio iš skelbimo')

# Ratlankiai/padangos — buvo teisingi, tokie ir lieka
w = WheelListing.objects.create(seller=u, product_type='tyre', price=100,
                                country='LT', city='Vilnius', status='active',
                                contact_phone='+370 5 111111')
tikrink(w.contact_phone == '+370 5 111111', 'ratlankių numeris sugadintas')


print('\n' + '═' * 60)
print('gerai: %d, nepavyko: %d' % (gerai, blogai))
sys.exit(1 if blogai else 0)
