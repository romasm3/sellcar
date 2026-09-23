# -*- coding: utf-8 -*-
"""
NUOTRAUKŲ AUDITO TESTAS.

Tikrinam visas keturias būkles, kurios pasitaiko gyvai:
  1. skelbimas su gera nuotrauka        -> į sąrašą NEPATENKA
  2. skelbimas visai be nuotraukų       -> „be nuotraukų"
  3. DB eilutė yra, failo diske nėra    -> „failai dingę", neatkuriamas
  4. failas guli diske kitu keliu       -> atkuriamas

Ir saugiklius:
  * be --atkurti niekas nekeičiama;
  * be --trinti niekas netrinama;
  * svetimas skelbimas netrinamas net su --trinti;
  * trynimas be pg_dump neįvyksta (sqlite -> RuntimeError).

Paleidimas:  python docs/nuotrauku_audito_test.py
"""
import io, os, sys, tempfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
for k, v in (('SECRET_KEY', 'x'), ('EMAIL_USER', 'x@x.lt'), ('EMAIL_PASSWORD', 'x')):
    os.environ.setdefault(k, v)

import django
from django.conf import settings

LAIKINA = tempfile.mkdtemp(prefix='nuotr-auditas-')
import config.settings as pagrindas
n = {k: v for k, v in vars(pagrindas).items() if k.isupper()}
n.update(
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3',
                           'NAME': os.path.join(LAIKINA, 'db.sqlite3')}},
    SECURE_SSL_REDIRECT=False, SESSION_COOKIE_SECURE=False,
    CSRF_COOKIE_SECURE=False, SECURE_HSTS_SECONDS=0,
    MEDIA_ROOT=os.path.join(LAIKINA, 'media'), DEBUG=False, ALLOWED_HOSTS=['*'],
    PASTAS_FONE=False, MOKEJIMAI_IJUNGTI=False, PAYMENTS_ENABLED=False,
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

from apps.listings.models import Listing, ListingImage, VehicleType
from apps.listings.management.commands import nuotrauku_auditas as A

gerai = blogai = 0
def tikrink(pav, ok, papild=''):
    global gerai, blogai
    print((u'  ✓ ' if ok else u'  ✗ ') + pav + (u'   %s' % (papild,) if papild else ''))
    if ok:
        gerai += 1
    else:
        blogai += 1

JPEG = bytes.fromhex('ffd8ffe000104a46494600010100000100010000ffd9')
U = get_user_model()
mano = U.objects.create_user(username='a', email='romasm3@gmail.com', password='x')
svetimas = U.objects.create_user(username='b', email='kitas@pavyzdys.lt', password='x')
VT, _ = VehicleType.objects.get_or_create(slug='cars', defaults={'name': 'Automobiliai'})


def skelbimas(pavadinimas, seller=None):
    return Listing.objects.create(
        title=pavadinimas, seller=seller or mano, vehicle_type=VT,
        price=Decimal(5000), year=2020, mileage=1000, city='Vilnius',
        country='LT', description='x', status='active',
        condition='used', defects='none')


# 1. Gera nuotrauka
geras = skelbimas('Su nuotrauka')
ListingImage.objects.create(listing=geras, image=ContentFile(JPEG, name='geras.jpg'))

# 2. Visai be nuotraukų
tuscias = skelbimas('Be nuotraukų')

# 3. Eilutė yra, failo nėra
dinges = skelbimas('Failas dingęs')
i3 = ListingImage.objects.create(listing=dinges, image=ContentFile(JPEG, name='dinges.jpg'))
os.remove(i3.image.path)

# 4. Failas guli kitu keliu
kitur = skelbimas('Failas kitur')
i4 = ListingImage.objects.create(listing=kitur, image=ContentFile(JPEG, name='kitur.jpg'))
senas = i4.image.path
naujas_kat = os.path.join(settings.MEDIA_ROOT, 'perkelta')
os.makedirs(naujas_kat, exist_ok=True)
os.rename(senas, os.path.join(naujas_kat, 'kitur.jpg'))

# 5. Svetimas, be nuotraukų
kito = skelbimas('Svetimas be nuotraukų', seller=svetimas)


print(u'\n== 1. Sąrašas ==')
r = {x['id']: x for x in A.surink()}
tikrink(u'geras skelbimas nepatenka', geras.pk not in r, sorted(r))
tikrink(u'be nuotraukų — patenka', tuscias.pk in r)
tikrink(u'be nuotraukų — būklė', r[tuscias.pk]['bukle'] == u'be nuotraukų',
        r[tuscias.pk]['bukle'])
tikrink(u'dingęs failas — patenka', dinges.pk in r)
tikrink(u'dingęs failas — būklė', r[dinges.pk]['bukle'] == u'failai dingę',
        r[dinges.pk]['bukle'])
tikrink(u'dingęs failas — neatkuriamas', r[dinges.pk]['atkuriamu'] == 0,
        r[dinges.pk]['atkuriamu'])
tikrink(u'failas kitur — atkuriamas', r[kitur.pk]['atkuriamu'] == 1,
        r[kitur.pk]['atkuriamu'])
tikrink(u'sąraše yra visi laukai',
        all(k in r[tuscias.pk] for k in
            ('id', 'pavadinimas', 'kategorija', 'savininkas', 'sukurta')))
tikrink(u'savininkas teisingas', r[tuscias.pk]['savininkas'] == 'romasm3@gmail.com',
        r[tuscias.pk]['savininkas'])

print(u'\n== 2. Peržiūra nieko nekeičia ==')
pries = ListingImage.objects.get(pk=i4.pk).image.name
call_command('nuotrauku_auditas', verbosity=0)
tikrink(u'kelias nepakeistas',
        ListingImage.objects.get(pk=i4.pk).image.name == pries)
tikrink(u'niekas neištrinta', Listing.objects.filter(status='active').count() == 5,
        Listing.objects.filter(status='active').count())

print(u'\n== 3. --atkurti prisega rastą failą ==')
call_command('nuotrauku_auditas', atkurti=True, verbosity=0)
i4.refresh_from_db()
tikrink(u'kelias atnaujintas', i4.image.name.endswith('perkelta/kitur.jpg'),
        i4.image.name)
tikrink(u'failas dabar randamas', A._failas_yra(i4))
liko = {x['id'] for x in A.surink()}
tikrink(u'atkurtas iškrenta iš sąrašo', kitur.pk not in liko, sorted(liko))
tikrink(u'niekas neištrinta be --trinti',
        Listing.objects.filter(status='active').count() == 5)

print(u'\n== 4. Trynimas be pg_dump neįvyksta ==')
klaida = None
try:
    call_command('nuotrauku_auditas', atkurti=True, trinti=True, verbosity=0)
except Exception as e:
    klaida = e
tikrink(u'sqlite atveju atsisakoma trinti', isinstance(klaida, RuntimeError),
        type(klaida).__name__ if klaida else 'klaidos nebuvo')
tikrink(u'klaida paaiškina kodėl', klaida and 'pg_dump' in str(klaida),
        str(klaida)[:60] if klaida else '')
tikrink(u'po nepavykusio trynimo viskas vietoje',
        Listing.objects.filter(status='active').count() == 5)

print(u'\n== 5. Svetimi skelbimai neliečiami ==')
sav = {'romasm3@gmail.com', 'romasm333@gmail.com'}
radiniai = A.surink()
svetimi = [x for x in radiniai if x['savininkas'].lower() not in sav]
tikrink(u'svetimas atpažintas', [x['id'] for x in svetimi] == [kito.pk],
        [x['id'] for x in svetimi])
tikrink(u'svetimas vis dar aktyvus',
        Listing.objects.filter(pk=kito.pk, status='active').exists())

print('\n' + '=' * 60)
print('gerai: %d, nepavyko: %d' % (gerai, blogai))
sys.exit(1 if blogai else 0)
