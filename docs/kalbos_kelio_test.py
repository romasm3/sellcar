# -*- coding: utf-8 -*-
"""
NĖ VIENAS PAGRINDINIS KELIAS NEGALI GRĄŽINTI 404 DĖL KALBOS.

`i18n_patterns(prefix_default_language=False)`: lietuviški adresai be
priešdėlio, kiti su. Kai aktyvi kalba ne lietuvių, o kelyje priešdėlio
nėra, maršruto NĖRA — ir puslapis grąžina 404. Taip 2026-09 prisijungę
žmonės su rusišku profiliu į svetainę nebepateko visai.

Tikrinam kiekvienai kalbai (lt, ru, en) ir kiekvienam pagrindiniam keliui:
atsakymas 200 arba 302 į TEISINGĄ adresą, niekada 404.

Paleidimas:  python docs/kalbos_kelio_test.py
"""
import os, sys, tempfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
for k, v in (('SECRET_KEY', 'x'), ('EMAIL_USER', 'x@x.lt'), ('EMAIL_PASSWORD', 'x')):
    os.environ.setdefault(k, v)

import django
from django.conf import settings

LAIKINA = tempfile.mkdtemp(prefix='kalbos-kelias-')
import config.settings as pagrindas
nustatymai = {k: v for k, v in vars(pagrindas).items() if k.isupper()}
nustatymai.update(
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3',
                           'NAME': os.path.join(LAIKINA, 'db.sqlite3')}},
    SECURE_SSL_REDIRECT=False, SESSION_COOKIE_SECURE=False,
    CSRF_COOKIE_SECURE=False, SECURE_HSTS_SECONDS=0,
    MEDIA_ROOT=LAIKINA, DEBUG=False, ALLOWED_HOSTS=['*'],
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}},
    STORAGES={'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
              'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'}},
)
settings.configure(**nustatymai)
django.setup()

from django.core.management import call_command
call_command('migrate', run_syncdb=True, verbosity=0)

from django.contrib.auth import get_user_model
from django.test import Client
from django.utils import timezone
from apps.listings.models import Brand, Listing, VehicleType

gerai = blogai = 0
def tikrink(s, k):
    global gerai, blogai
    if s: gerai += 1
    else:
        blogai += 1
        print('  NEPAVYKO: ' + k)
def antraste(t):
    print('\n── ' + t + ' ' + '─' * max(0, 52 - len(t)))


U = get_user_model()
u = U.objects.create_user(username='p@x.lt', email='p@x.lt', password='x')
VT, _ = VehicleType.objects.get_or_create(slug='cars', defaults={'name': 'Automobiliai'})
MARKE, _ = Brand.objects.get_or_create(name='BMW', defaults={'slug': 'bmw'})

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

d = _butini(Listing)
d.update(seller=u, vehicle_type=VT, title='BMW 320d', price=5000, year=2018,
         status='active', country='LT', city='Vilnius', brand=MARKE)
SKELBIMAS = Listing.objects.create(**d)

KELIAI = [
    ('pradžia',            '/'),
    ('skelbimų sąrašas',   '/skelbimai/'),
    ('įmonės',             '/imones/'),
    ('išplėstinė paieška', '/paieska/cars/'),
    ('žemėlapis',          '/map/'),
    ('skelbimo puslapis',  '/%s/' % SKELBIMAS.pk),
]
UZ_I18N = [('admin', '/admin/'), ('robots.txt', '/robots.txt')]
UZKLAUSA = '?section=cars&price_min=5000&salis=lt'


def bandyk(kelias, kalba, prisijunges):
    """(status, Location) su nurodyta profilio/slapuko kalba."""
    if prisijunges:
        p = u.profile
        p.language = kalba
        p.save(update_fields=['language'])
        c = Client()
        c.force_login(u)
    else:
        c = Client()
        c.cookies['django_language'] = kalba
    r = c.get(kelias + UZKLAUSA)
    return r.status_code, r.get('Location', '')


for prisijunges in (True, False):
    antraste('%s vartotojas' % ('Prisijungęs' if prisijunges else 'Anoniminis'))
    for kalba in ('lt', 'ru', 'en'):
        for vardas, kelias in KELIAI:
            kodas, vieta = bandyk(kelias, kalba, prisijunges)
            tikrink(kodas != 404, '%s · %s · %s → 404' % (kalba, vardas, kelias))
            if kalba == 'lt':
                tikrink(kodas == 200, '%s · %s → %s (turi būti 200)' % (kalba, vardas, kodas))
            else:
                tikrink(kodas in (200, 302),
                        '%s · %s → %s' % (kalba, vardas, kodas))
                if kodas == 302:
                    laukta = '/%s%s%s' % (kalba, kelias, UZKLAUSA)
                    tikrink(vieta == laukta,
                            '%s · %s → %r (laukta %r)' % (kalba, vardas, vieta, laukta))
        print('  %s: %d keliai patikrinti' % (kalba, len(KELIAI)))


antraste('Nukreipimas nuveda į veikiantį puslapį')
p = u.profile; p.language = 'ru'; p.save(update_fields=['language'])
c = Client(); c.force_login(u)
for vardas, kelias in KELIAI:
    r = c.get(kelias)
    if r.status_code == 302:
        r2 = c.get(r['Location'])
        tikrink(r2.status_code == 200,
                '%s: nukreipus %s → %s' % (vardas, r['Location'], r2.status_code))


antraste('Keliai UŽ i18n_patterns ribų nepaliesti')
for kalba in ('ru', 'en'):
    p = u.profile; p.language = kalba; p.save(update_fields=['language'])
    c = Client(); c.force_login(u)
    for vardas, kelias in UZ_I18N:
        r = c.get(kelias)
        tikrink(r.status_code != 404, '%s · %s → 404' % (kalba, vardas))
        tikrink(not r.get('Location', '').startswith('/%s/' % kalba),
                '%s · %s nukreiptas į kalbos priešdėlį (%s)'
                % (kalba, vardas, r.get('Location')))


antraste('Tikras 404 lieka 404, be ciklo')
p = u.profile; p.language = 'ru'; p.save(update_fields=['language'])
c = Client(); c.force_login(u)
r = c.get('/tokio-kelio-tikrai-nera/')
tikrink(r.status_code == 404, 'nesamas kelias grąžino %s' % r.status_code)
tikrink(not r.get('Location'), 'nesamas kelias nukreipiamas — būtų ciklas')


antraste('POST nenukreipiamas (302 nuneštų kūną)')
p = u.profile; p.language = 'ru'; p.save(update_fields=['language'])
c = Client(); c.force_login(u)
r = c.post('/', {'x': '1'})
tikrink(r.status_code != 302 or not r.get('Location', '').startswith('/ru/'),
        'POST nukreiptas į /ru/ — dingtų forma')


print('\n' + '═' * 60)
print('gerai: %d, nepavyko: %d' % (gerai, blogai))
sys.exit(1 if blogai else 0)
