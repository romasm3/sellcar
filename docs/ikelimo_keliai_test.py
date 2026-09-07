# -*- coding: utf-8 -*-
"""
AJAX KELIAI PRIVALO VEIKTI VISOMIS KALBOMIS.

Frontend'as nuotraukų įkėlimą siunčia į KIETAI užrašytą adresą be kalbos
priešdėlio:

    xhr.open('POST', '/ajax/upload-listing-images/' + listingId + '/')

O `config/urls.py` visus `apps.listings.urls` maršrutus laiko
`i18n_patterns(prefix_default_language=False)` viduje. Vadinasi, jie
gyvena ties „/ajax/…" TIK kai aktyvi kalba lietuvių; bet kuriai kitai
`LocalePrefixPattern` reikalauja „/ru/ajax/…", ir POST'as be priešdėlio
gauna 404 — „Upload failed (404)" su 100 % progreso juosta.

GET'ą tokiu atveju išgelbsti KalbosKelioMiddleware (302 į priešdėlį),
bet POST'o jis sąmoningai neliečia: 302 nuneštų failo kūną.

Tikrinam KIEKVIENĄ kalbą ir abu pavidalus — su priešdėliu ir be jo.

Paleidimas:  python docs/ikelimo_keliai_test.py
"""
import io
import json
import os
import sys
import tempfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
for k, v in (('SECRET_KEY', 'x'), ('EMAIL_USER', 'x@x.lt'), ('EMAIL_PASSWORD', 'x')):
    os.environ.setdefault(k, v)

import django
from django.conf import settings

LAIKINA = tempfile.mkdtemp(prefix='ikelimas-')
import config.settings as pagrindas
n = {k: v for k, v in vars(pagrindas).items() if k.isupper()}
n.update(
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3',
                           'NAME': os.path.join(LAIKINA, 'db.sqlite3')}},
    SECURE_SSL_REDIRECT=False, SESSION_COOKIE_SECURE=False,
    CSRF_COOKIE_SECURE=False, SECURE_HSTS_SECONDS=0,
    MEDIA_ROOT=LAIKINA, DEBUG=False, ALLOWED_HOSTS=['*'],
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
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
from django.core.files.uploadedfile import SimpleUploadedFile
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


def tikras_jpg():
    """Tikras JPEG, ne baitų šiukšlės — vaizdų tikrintuvas jį atpažįsta."""
    from PIL import Image
    b = io.BytesIO()
    Image.new('RGB', (60, 40), (200, 60, 30)).save(b, format='JPEG')
    return b.getvalue()


JPG = tikras_jpg()

U = get_user_model()
u = U.objects.create_user(username='p@x.lt', email='p@x.lt', password='x')
VT, _ = VehicleType.objects.get_or_create(slug='cars', defaults={'name': 'Automobiliai'})
MARKE, _ = Brand.objects.get_or_create(name='BMW', defaults={'slug': 'bmw'})


def _butini(model):
    from django.db import models as dm
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
d.update(seller=u, vehicle_type=VT, brand=MARKE, title='BMW 320d', price=5000,
         year=2018, status='draft', country='LT', city='Vilnius')
SKELBIMAS = Listing.objects.create(**d)

KALBOS = [k for k, _v in settings.LANGUAGES]


def klientas(kalba):
    p = u.profile
    p.language = kalba
    p.save(update_fields=['language'])
    c = Client()
    c.force_login(u)
    c.cookies['django_language'] = kalba
    return c


def ikelk(c, kelias):
    return c.post(kelias, {
        'images': SimpleUploadedFile('nuotrauka.jpg', JPG, content_type='image/jpeg'),
    })


# ═══════════════════════════════════════════════════════════════════
antraste('Nuotraukos įkėlimas — kelias BE priešdėlio')
KELIAS = '/ajax/upload-listing-images/%d/' % SKELBIMAS.pk
for kalba in KALBOS:
    prade = SKELBIMAS.images.count()
    r = ikelk(klientas(kalba), KELIAS)
    tikrink(r.status_code != 404,
            '%s: POST %s grąžino 404 — maršruto nėra' % (kalba, KELIAS))
    tikrink(r.status_code == 200,
            '%s: grąžino %s, laukta 200' % (kalba, r.status_code))
    if r.status_code == 200:
        tikrink(SKELBIMAS.images.count() == prade + 1,
                '%s: atsakymas 200, bet nuotrauka neįrašyta' % kalba)
print('  patikrinta kalbų: %d' % len(KALBOS))


antraste('Tas pats kelias SU kalbos priešdėliu (senos nuorodos)')
for kalba in KALBOS:
    if kalba == settings.LANGUAGE_CODE:
        continue
    kelias = '/%s/ajax/upload-listing-images/%d/' % (kalba, SKELBIMAS.pk)
    r = ikelk(klientas(kalba), kelias)
    tikrink(r.status_code == 200,
            '%s: %s grąžino %s' % (kalba, kelias, r.status_code))


antraste('Kiti įkėlimo ir juodraščio keliai — irgi ne 404')
KITI = [
    '/ajax/save-cars-draft/',
    '/ajax/upload-draft-images/',
    '/ajax/reorder-listing-images/%d/' % SKELBIMAS.pk,
    '/ajax/get-models/',
    '/ajax/markes/',
]
for kalba in ('lt', 'ru', 'de'):
    c = klientas(kalba)
    for kelias in KITI:
        r = c.post(kelias, {}) if 'get-models' not in kelias and 'markes' not in kelias \
            else c.get(kelias)
        tikrink(r.status_code != 404,
                '%s: %s grąžino 404' % (kalba, kelias))


antraste('Trynimas, pertvarkymas ir juodraštis — visomis kalbomis')
# Nuotraukų valdymas formoje remiasi šiais trimis keliais. Jei bent
# vienas kuria nors kalba grąžina 404, mygtukai atrodo „neveikiantys".
for kalba in KALBOS:
    c = klientas(kalba)

    # Įkeliam dvi, kad būtų ką pertvarkyti ir ištrinti
    ikelk(c, KELIAS); ikelk(c, KELIAS)
    ids = list(SKELBIMAS.images.order_by('order').values_list('pk', flat=True))
    tikrink(len(ids) >= 2, '%s: per mažai nuotraukų pertvarkymui' % kalba)
    if len(ids) < 2:
        continue

    # Pertvarkymas: apsukam pirmas dvi
    nauja = [ids[1], ids[0]] + list(ids[2:])
    r = c.post('/ajax/reorder-listing-images/%d/' % SKELBIMAS.pk,
               data=json.dumps({'image_ids': nauja}),
               content_type='application/json')
    tikrink(r.status_code == 200,
            '%s: pertvarkymas grąžino %s' % (kalba, r.status_code))
    po = list(SKELBIMAS.images.order_by('order').values_list('pk', flat=True))
    tikrink(po[:2] == nauja[:2],
            '%s: tvarka neišsaugota: %s vs %s' % (kalba, po[:2], nauja[:2]))
    pirma = SKELBIMAS.images.order_by('order').first()
    tikrink(pirma.pk == nauja[0],
            '%s: pirmoji nuotrauka ne ta, kurią uždėjom' % kalba)

    # Juodraščio išsaugojimas (grįžus „atgal" darbas neturi dingti)
    r = c.post('/ajax/save-cars-draft/',
               data=json.dumps({'price': '5500'}),
               content_type='application/json')
    tikrink(r.status_code == 200,
            '%s: save-cars-draft grąžino %s' % (kalba, r.status_code))

    # Trynimas
    kiek = SKELBIMAS.images.count()
    r = c.post('/image/%d/delete/' % nauja[-1])
    tikrink(r.status_code in (200, 302),
            '%s: trynimas grąžino %s (404 = kelio nėra)' % (kalba, r.status_code))
    tikrink(SKELBIMAS.images.count() == kiek - 1,
            '%s: nuotrauka neištrinta' % kalba)

    # „Padaryti pagrindine" — 18 šablonų kvietė /listings/image/…/,
    # kurio NIEKADA nebuvo (404 net lietuviškai).
    likusios = list(SKELBIMAS.images.order_by('order').values_list('pk', flat=True))
    if len(likusios) >= 2:
        r = c.post('/image/%d/set-main/' % likusios[-1])
        tikrink(r.status_code in (200, 302),
                '%s: set-main grąžino %s' % (kalba, r.status_code))
        SKELBIMAS.refresh_from_db()
        tikrink(SKELBIMAS.images.get(pk=likusios[-1]).is_main,
                '%s: pagrindinė nuotrauka nepasikeitė' % kalba)
    SKELBIMAS.images.all().delete()


antraste('Nuotrauka tikrai JPEG (ne šiukšlės)')
tikrink(JPG[:2] == b'\xff\xd8', 'testo failas nėra JPEG')
tikrink(len(JPG) > 200, 'testo JPEG per mažas')

print('\n' + '═' * 60)
print('gerai: %d, nepavyko: %d' % (gerai, blogai))
sys.exit(1 if blogai else 0)
