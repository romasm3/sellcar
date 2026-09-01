# -*- coding: utf-8 -*-
"""
SKAIČIŲ FORMATAS: metai be tarpo, kiekiai su tarpu.

Django lt lokalė tūkstančius skiria TAŠKU (intcomma(48320) → „48.320"),
todėl USE_THOUSAND_SEPARATOR mums netinka: metai virsdavo „2.018", o
formų laukuose atsirasdavo „15.000". Tarpą dedam patys per
apps/listings/formatai.py (|sk, |kaina).

Šitas testas eina per TIKRUS adresus ir tikrina abu galus:
    metai   → „2018"   (jokio skirtuko)
    kiekiai → „1 234"  (nedalomas tarpas)
Jei kuris nors persimaišo — krenta.

Paleidimas:  python docs/skaiciu_formatas_test.py
"""
import html as htmlmod
import os, re, sys, shutil, tempfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
os.environ.setdefault('SECRET_KEY', 'x')
os.environ.setdefault('EMAIL_USER', 'x@x.lt')
os.environ.setdefault('EMAIL_PASSWORD', 'x')

import django
from django.conf import settings

LAIKINA = tempfile.mkdtemp(prefix='skaiciai-')
import config.settings as pagrindas
nustatymai = {k: v for k, v in vars(pagrindas).items() if k.isupper()}
nustatymai.update(
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3',
                           'NAME': os.path.join(LAIKINA, 'db.sqlite3')}},
    SECURE_SSL_REDIRECT=False, SESSION_COOKIE_SECURE=False,
    CSRF_COOKIE_SECURE=False, SECURE_HSTS_SECONDS=0,
    MEDIA_ROOT=LAIKINA, DEBUG=False, ALLOWED_HOSTS=['*'],
    # Skelbimo puslapis paleidžia laiškų scenarijų; be šito testas
    # pakimba bandydamas prisijungti prie SMTP.
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}},
)
settings.configure(**nustatymai)
django.setup()

from django.core.management import call_command
call_command('migrate', run_syncdb=True, verbosity=0)

from django.contrib.auth import get_user_model
from django.test import Client
from django.utils import timezone, translation
from apps.listings.formatai import sk, kaina, NEDALOMAS
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

TARPAS = NEDALOMAS


antraste('1. formatai.py — tarpas, ne taškas')
with translation.override('lt'):
    tikrink(sk(1234) == '1' + TARPAS + '234', 'lt: 1234 → 1 234 (%r)' % sk(1234))
    tikrink(sk(48320) == '48' + TARPAS + '320', 'lt: 48320 → 48 320 (%r)' % sk(48320))
    tikrink('.' not in sk(48320), 'jokio taško (%r)' % sk(48320))
    tikrink(kaina(5000) == '5' + TARPAS + '000' + TARPAS + '€',
            'kaina su tarpu (%r)' % kaina(5000))
with translation.override('en'):
    tikrink(sk(1234) == '1,234', 'en: 1234 → 1,234 (%r)' % sk(1234))

antraste('2. Django lokalė išjungta')
tikrink(settings.USE_THOUSAND_SEPARATOR is False,
        'USE_THOUSAND_SEPARATOR = False')
from django.utils.formats import number_format
with translation.override('lt'):
    tikrink(number_format(2018) == '2018',
            'plikas skaičius nebeskaidomas (%r)' % number_format(2018))


# ── Duomenys ────────────────────────────────────────────────────────
U = get_user_model()
u = U.objects.create_user(username='p', email='p@x.lt', password='x')
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

B = _butini(Listing)
# Metai 2018, rida 168 000, peržiūros 1 234 — visi trys „pavojingi" dydžiai
for i in range(3):
    d = dict(B)
    d.update(seller=u, vehicle_type=VT, title='Auto %d' % i, price=15900,
             year=2018, status='active', country='LT', city='Vilnius',
             mileage=168000, views_count=1234)
    Listing.objects.create(**d)

c = Client()
def puslapis(kelias):
    r = c.get(kelias)
    return r.status_code, r.content.decode()


antraste('3. Metai — BE skirtuko')
for kelias in ('/', '/?section=cars&sidebar=1'):
    kodas, h = puslapis(kelias)
    tikrink(kodas == 200, '%s atsidaro (%s)' % (kelias, kodas))
    tikrink('2018' in h, '%s: metai „2018"' % kelias)
    tikrink('2.018' not in h, '%s: jokio „2.018"' % kelias)
    tikrink('2 018' not in h and ('2' + TARPAS + '018') not in h,
            '%s: jokio „2 018"' % kelias)


antraste('4. Kiekiai ir dydžiai — SU tarpu')
kodas, h = puslapis('/?section=cars&sidebar=1')
tikrink('168' + TARPAS + '000' in h,
        'rida su nedalomu tarpu („168 000")')
tikrink('168000' not in h, 'rida ne plikas „168000"')
tikrink('168.000' not in h, 'rida ne „168.000"')
tikrink('15' + TARPAS + '900' in h, 'kaina su tarpu („15 900")')

# Peržiūros skelbimo puslapyje
pirmas = Listing.objects.first()
with translation.override('lt'):
    adresas = pirmas.get_absolute_url()
kodas, h = puslapis(adresas)
tikrink(kodas == 200, 'skelbimas atsidaro (%s)' % kodas)
# Peržiūros skaitiklis puslapį atidarius pasididina, tad tikrinam ne
# konkretų skaičių, o kad TOKS, koks rodomas, yra su nedalomu tarpu.
rodo = re.search(r'font-medium text-gray-900">([\d\u00a0.,]+)</span>', h)
tikrink(rodo and TARPAS in rodo.group(1),
        'peržiūros su tarpu (rodo %r)' % (rodo.group(1) if rodo else None))
tikrink('1.234' not in h, 'peržiūros ne „1.234"')
# Metai to paties skelbimo puslapyje
tikrink('2.018' not in h, 'skelbime metai be taško')


antraste('5. Šalies sąrašuose — tarpas, ne taškas')
kodas, h = puslapis('/')
# Šalies juostos kiekiai eina per |sk; su trim skelbimais tarpo nesimato,
# todėl tikrinam patį šabloną: |intcomma čia būtų grąžinęs „48.320".
sal = open(os.path.join(BASE, 'templates/partials/_salis.html'),
           encoding='utf-8').read()
tikrink('intcomma' not in sal, 'šalies sąraše nebėra intcomma')
tikrink(sal.count('|sk') == 2, 'abu kiekiai per |sk (%d)' % sal.count('|sk'))


antraste('6. Formų laukuose — plikas skaičius')
# value="15900", ne value="15 900" — kitaip formos nebeišsaugosi
kodas, h = puslapis('/?section=cars&sidebar=1&price_min=15900&year_min=2018')
for bloga in ('value="15 900"', 'value="15' + TARPAS + '900"',
              'value="15.900"', 'value="2.018"'):
    tikrink(bloga not in h, 'formos lauke nėra %s' % bloga)


antraste('7. Visame projekte nebeliko Django lokalės skirtuko')
import subprocess
liko = subprocess.run(['grep', '-rn', 'intcomma', '--include=*.html', 'templates/'],
                      capture_output=True, text=True, cwd=BASE).stdout.strip()
tikrink(not liko, 'jokio |intcomma šablonuose:\n    ' + liko.replace('\n', '\n    '))


shutil.rmtree(LAIKINA, ignore_errors=True)
print('\n' + '═' * 60)
print('gerai: %d, nepavyko: %d' % (gerai, blogai))
sys.exit(1 if blogai else 0)
