# -*- coding: utf-8 -*-
"""
LAIŠKAI NELAIKO LANKYTOJO.

Skelbimo puslapis siųsdavo laišką TIESIOG UŽKLAUSOJE: `_track_listing_view`
peržengus 10, 100, 500 ar 1000 peržiūrų kviečia send_scenario, o tas
sinchroniškai jungiasi prie smtp.gmail.com. Kol vyksta TLS ir siuntimas,
laukia ir gunicorn darbininkas, ir eilinis lankytojas, neturintis su tuo
laišku nieko bendra. Be EMAIL_TIMEOUT — laukiama be galo.

Testas pakiša LĖTĄ pašto backend'ą (2 s vienam laiškui) ir tikrina, kad
puslapis vis tiek atiduodamas greitai, o laiškas išsiunčiamas fone.

Paleidimas:  python docs/pasto_fone_test.py
"""
import os, sys, shutil, tempfile, threading, time

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
os.environ.setdefault('SECRET_KEY', 'x')
os.environ.setdefault('EMAIL_USER', 'x@x.lt')
os.environ.setdefault('EMAIL_PASSWORD', 'x')

import django
from django.conf import settings

LAIKINA = tempfile.mkdtemp(prefix='pastas-')
import config.settings as pagrindas
nustatymai = {k: v for k, v in vars(pagrindas).items() if k.isupper()}
nustatymai.update(
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3',
                           'NAME': os.path.join(LAIKINA, 'db.sqlite3')}},
    SECURE_SSL_REDIRECT=False, SESSION_COOKIE_SECURE=False,
    CSRF_COOKIE_SECURE=False, SECURE_HSTS_SECONDS=0,
    MEDIA_ROOT=LAIKINA, DEBUG=False, ALLOWED_HOSTS=['*'],
    EMAIL_BACKEND='docs.pasto_letas_backend.LetasBackend',
    CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}},
)
settings.configure(**nustatymai)
django.setup()

from docs.pasto_letas_backend import DELSA, issiusta

from django.core.management import call_command
call_command('migrate', run_syncdb=True, verbosity=0)

from django.contrib.auth import get_user_model
from django.test import Client
from django.utils import timezone, translation
from apps.listings.models import Listing, VehicleType

gerai = blogai = 0
def tikrink(s, k):
    global gerai, blogai
    if s: gerai += 1
    else:
        blogai += 1
        print('  NEPAVYKO: ' + k)
def antraste(t):
    print('\n── ' + t + ' ' + '─' * max(0, 56 - len(t)))


antraste('1. Saugikliai nustatymuose')
tikrink(getattr(settings, 'EMAIL_TIMEOUT', None) == 10,
        'EMAIL_TIMEOUT = 10 (yra %r)' % getattr(settings, 'EMAIL_TIMEOUT', None))
tikrink(getattr(settings, 'PASTAS_FONE', None) is True,
        'PASTAS_FONE = True (yra %r)' % getattr(settings, 'PASTAS_FONE', None))


antraste('2. Fono siuntimas grąžina tuoj pat')
from apps.listings.emails import fone
pr = time.monotonic()
fone.fone(time.sleep, DELSA)
truko = time.monotonic() - pr
tikrink(truko < 0.5, 'fone() negrįžta po %.1f s (truko %.2f s)' % (DELSA, truko))

# Išjungus — sinchroniška, kaip komandoms ir testams reikia
settings.PASTAS_FONE = False
pr = time.monotonic()
fone.fone(time.sleep, 0.3)
truko = time.monotonic() - pr
tikrink(truko >= 0.29, 'PASTAS_FONE=False → sinchroniška (%.2f s)' % truko)
settings.PASTAS_FONE = True


# ── Duomenys ────────────────────────────────────────────────────────
U = get_user_model()
pardavejas = U.objects.create_user(username='p', email='p@pardavejas.lt', password='x')
VT, _ = VehicleType.objects.get_or_create(slug='cars', defaults={'name': 'Automobiliai'})

def _butini(model):
    out = {}
    for f in model._meta.concrete_fields:
        if (f.primary_key or f.null or f.blank or f.has_default() or f.auto_created
                or getattr(f, 'auto_now', False) or getattr(f, 'auto_now_add', False)):
            continue
        it = f.get_internal_type()
        if it.endswith('IntegerField'): out[f.name] = 0
        elif it in ('DecimalField', 'FloatField'): out[f.name] = 0
        elif it in ('CharField', 'TextField', 'SlugField', 'EmailField', 'URLField'): out[f.name] = ''
        elif it == 'BooleanField': out[f.name] = False
        elif it in ('DateTimeField', 'DateField'): out[f.name] = timezone.now()
    return out

d = dict(_butini(Listing))
d.update(seller=pardavejas, vehicle_type=VT, title='Auto', price=5000, year=2018,
         status='active', country='LT', city='Vilnius',
         # 9 peržiūros: kitas atidarymas peržengs 10 ir paleis laišką
         views_count=9)
skelbimas = Listing.objects.create(**d)
with translation.override('lt'):
    ADRESAS = skelbimas.get_absolute_url()


antraste('3. Skelbimo puslapis nelaukia pašto')
c = Client(REMOTE_ADDR='203.0.113.7')
pr = time.monotonic()
r = c.get(ADRESAS)
truko = time.monotonic() - pr
tikrink(r.status_code == 200, 'puslapis atsidaro (%s)' % r.status_code)
tikrink(truko < DELSA,
        'atiduotas per %.2f s, greičiau nei paštas (%.1f s)' % (truko, DELSA))

skelbimas.refresh_from_db()
tikrink(skelbimas.views_count == 10,
        'peržiūra suskaičiuota (%s)' % skelbimas.views_count)
tikrink(skelbimas.first_views_notified_at is not None,
        'slenkstis pažymėtas — laiškas paleistas')

antraste('4. Laiškas vis tiek išsiunčiamas')
pabaiga = time.monotonic() + DELSA * 3
while not issiusta and time.monotonic() < pabaiga:
    time.sleep(0.1)
tikrink(bool(issiusta), 'fone išsiųstas (%s)' % issiusta)


antraste('5. Užklausoje nebeliko sinchroninių siuntimų')
import re
v = open(os.path.join(BASE, 'apps/listings/views.py'), encoding='utf-8').read()
# Pagalbinės _send_* funkcijos (iki „saved_listings_list") — visos per foną
virsus = v[:v.index('def email_saved_listings')]
tikrink('from apps.listings.emails.sender import send_scenario' not in virsus,
        'pranešimų pagalbinės nebeimporuoja sinchroninio siuntėjo')
tikrink(virsus.count('emails.fone import') == 8,
        'visos aštuonios pranešimų pagalbinės per foną (%d)'
        % virsus.count('emails.fone import'))
for kelias, ka in (('apps/conversations/views.py', 'žinutės pranešimas'),
                   ('apps/accounts/views.py', 'pasisveikinimas')):
    t = open(os.path.join(BASE, kelias), encoding='utf-8').read()
    tikrink('emails.fone import' in t, '%s per foną' % ka)
# Vartotojo inicijuotas „atsiųsk sąrašą" LIEKA sinchroninis — puslapis
# rodo, ar pavyko, tad rezultato reikia iš tikrųjų.
apacia = v[v.index('def email_saved_listings'):]
tikrink('from apps.listings.emails.sender import send_scenario' in apacia,
        '„atsiųsk sąrašą" lieka sinchroninis — puslapis rodo rezultatą')


shutil.rmtree(LAIKINA, ignore_errors=True)
print('\n' + '═' * 60)
print('gerai: %d, nepavyko: %d' % (gerai, blogai))
sys.exit(1 if blogai else 0)
