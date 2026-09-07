# -*- coding: utf-8 -*-
"""
VISOS ĮKĖLIMO FORMOS ELGIASI VIENODAI SU NUOTRAUKOMIS.

Iki šiol kiekvienas iš 28 create šablonų turėjo savo nusirašytą
nuotraukų kodą: ◀ ▶ mygtukai buvo tik automobiliuose, o pusėje formų
nebuvo kaip pakeisti pagrindinės nuotraukos. Dabar elgsena gyvena
vienoje vietoje (static/js/nuotrauku_valdymas.js +
templates/listings/partials/_nuotrauku_valdymas.html), ir šis testas
saugo, kad nė viena forma neliktų nuošalyje.

Tikrinam KIEKVIENĄ create adresą:
  * puslapis atsidaro (200) — visomis 13 kalbų;
  * bendra dalis prijungta (jos nėra = forma vėl liko su savo kodu);
  * bendras JS pasiekiamas;
  * nuotraukų keliai (įkėlimas, pertvarkymas, trynimas, pagrindinė,
    juodraštis) grąžina ne 404.

Paleidimas:  python docs/create_formu_nuotraukos_test.py
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

LAIKINA = tempfile.mkdtemp(prefix='create-formos-')
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
from django.test import Client

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

# Be kategorijų įrašų formos nusimeta į skelbimų sąrašą („kategorija
# nesukonfigūruota"), ir patikra tikrintų ne tą puslapį.
from apps.listings.models import VehicleType
SLUGAI = ['cars', 'motorcycles', 'trucks', 'trailers', 'agriculture',
          'construction', 'loading-equipment', 'forestry', 'camping-houses',
          'rental', 'services', 'electronics', 'bicycles', 'boats', 'parts',
          'motogear', 'tires', 'wheels', 'minibuses']
for i, slug in enumerate(SLUGAI):
    VehicleType.objects.get_or_create(slug=slug, defaults={'name': slug.title()})

# Visi create adresai iš urls.py — sąrašo rankomis nelaikom, kad nauja
# kategorija į patikrą pakliūtų savaime.
from django.urls import get_resolver

def create_keliai():
    """Visi „create/…" adresai — surenkami iš maršrutų medžio.

    Sąrašo rankomis nelaikom: nauja kategorija į patikrą turi pakliūti
    savaime, kitaip po pusmečio testas tikrins pasenusį rinkinį.
    """
    rasta = []

    def eik(sarasas, priesd):
        for m in sarasas:
            kelias = priesd + str(getattr(m, 'pattern', ''))
            vidus = getattr(m, 'url_patterns', None)
            if vidus is not None:
                eik(vidus, kelias)
            elif kelias.startswith('create/') and '<' not in kelias:
                rasta.append('/' + kelias)

    eik(get_resolver().url_patterns, '')
    return sorted(set(rasta))


KELIAI = create_keliai()
SABLONAI = sorted(f for f in os.listdir(os.path.join(BASE, 'templates', 'listings'))
                  if 'create' in f and f.endswith('.html'))

BENDRA = "_nuotrauku_valdymas.html"


def klientas(kalba='lt'):
    p = u.profile
    p.language = kalba
    p.save(update_fields=['language'])
    c = Client()
    c.force_login(u)
    c.cookies['django_language'] = kalba
    return c


antraste('Bendra dalis prijungta VISUOSE create šablonuose')
print('  create šablonų: %d' % len(SABLONAI))
for f in SABLONAI:
    kelias = os.path.join(BASE, 'templates', 'listings', f)
    turinys = io.open(kelias, encoding='utf-8').read()
    tikrink(BENDRA in turinys,
            '%s neprijungė bendros nuotraukų dalies' % f)


antraste('Bendras JS ir dalis egzistuoja')
for f in ('static/js/nuotrauku_valdymas.js',
          'templates/listings/partials/_nuotrauku_valdymas.html'):
    tikrink(os.path.exists(os.path.join(BASE, f)), 'nėra %s' % f)

js = io.open(os.path.join(BASE, 'static/js/nuotrauku_valdymas.js'),
             encoding='utf-8').read()
for dalis, kam in (('foto-perstumti', '◀ ▶ perstūmimas'),
                   ('foto-zyme', 'PAGRINDINĖ ženklas'),
                   ('issaugokTvarka', 'tvarkos išsaugojimas'),
                   ('siuskPoViena', 'įkėlimas po vieną'),
                   ('beforeunload', 'išėjimo sargas'),
                   ('sessionStorage', 'laukai išlieka keičiant kalbą')):
    tikrink(dalis in js, 'bendrame JS nėra: %s' % kam)


antraste('Kiekviena forma atsidaro (visomis 13 kalbų)')
KALBOS = [k for k, _v in settings.LANGUAGES]
print('  adresų: %d, kalbų: %d' % (len(KELIAI), len(KALBOS)))
neatsidare = []
for kelias in KELIAI:
    for kalba in KALBOS:
        c = klientas(kalba)
        priesd = '' if kalba == settings.LANGUAGE_CODE else '/' + kalba
        r = c.get(priesd + kelias, follow=True)
        if r.status_code != 200:
            neatsidare.append('%s %s → %s' % (kalba, kelias, r.status_code))
tikrink(not neatsidare,
        'neatsidarė: %s' % neatsidare[:5])
print('  patikrinta derinių: %d' % (len(KELIAI) * len(KALBOS)))


antraste('Bendra dalis pasiekia atiduotą puslapį')
c = klientas('lt')
be_dalies, nukreipia, rinkikliai = [], [], []
for kelias in KELIAI:
    r = c.get(kelias, follow=True)
    if r.status_code != 200:
        continue
    # Nukreipimas reiškia, kad forma neatsidarė (trūksta kategorijos ar
    # panašiai) — tada bendros dalies joje ir negali būti.
    if r.redirect_chain and not r.redirect_chain[-1][0].rstrip('/').endswith(
            kelias.rstrip('/')):
        nukreipia.append('%s → %s' % (kelias, r.redirect_chain[-1][0]))
        continue
    kunas = r.content.decode('utf-8')
    # Kategorijų rinkikliai („/create/parts/", „/create/minibuses/")
    # nuotraukų neturi visai — jiems bendros dalies ir nereikia.
    if 'id="imageInput"' not in kunas and 'id="existing-photos"' not in kunas:
        rinkikliai.append(kelias)
        continue
    if 'js/nuotrauku_valdymas.js' not in kunas:
        be_dalies.append(kelias)
print('  formų atsidarė: %d, nukreipė: %d, kategorijų rinkiklių: %d'
      % (len(KELIAI) - len(nukreipia), len(nukreipia), len(rinkikliai)))
for x in rinkikliai:
    print('    be nuotraukų (rinkiklis): %s' % x)
for x in nukreipia:
    print('    nukreipia: %s' % x)
tikrink(not be_dalies, 'puslapiuose nėra bendro JS: %s' % be_dalies[:5])
tikrink(len(nukreipia) <= 6,
        'per daug formų nusimeta į kitą puslapį: %d' % len(nukreipia))


antraste('Nuotraukų keliai — ne 404 visomis kalbomis')
KELIAI_API = [
    ('POST', '/ajax/upload-listing-images/1/'),
    ('POST', '/ajax/reorder-listing-images/1/'),
    ('POST', '/ajax/upload-draft-images/'),
    ('POST', '/ajax/reorder-draft-images/'),
    ('POST', '/ajax/delete-draft-image/1/'),
    ('POST', '/ajax/save-cars-draft/'),
    ('POST', '/image/1/delete/'),
    ('POST', '/image/1/set-main/'),
]
# Tikrinam MARŠRUTĄ, ne objektą: skelbimo su pk=1 čia nėra, tad HTTP
# 404 reikštų ir „nėra kelio", ir „nėra skelbimo". Sprendžiam adresą su
# aktyvia kalba — būtent tai ir lūždavo (LocalePrefixPattern atpažįsta
# tik aktyvios kalbos priešdėlį).
from django.urls import Resolver404, resolve
from django.utils import translation

for kalba in KALBOS:
    with translation.override(kalba):
        for metodas, kelias in KELIAI_API:
            try:
                resolve(kelias)
                rado = True
            except Resolver404:
                rado = False
            tikrink(rado, '%s: %s neišsisprendžia (404)' % (kalba, kelias))

print('\n' + '═' * 60)
print('gerai: %d, nepavyko: %d' % (gerai, blogai))
sys.exit(1 if blogai else 0)
