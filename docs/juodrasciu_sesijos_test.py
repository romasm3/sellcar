# -*- coding: utf-8 -*-
"""
JUODRAŠČIO NUOTRAUKOS NEPRILIMPA PRIE KITO SKELBIMO.

Kas buvo. Įkėlimo forma juodraštį laiko sesijoje, o nuotraukos AJAX'u
gula tiesiai į jį. Nulūžus pateikimui (per didelis skaičius → 500)
sesijos raktas likdavo, ir kitas bandymas pildė TĄ PATĮ juodraštį:
skelbimas #754 gavo 40 nuotraukų vietoj 20 — renault-t460_*.jpg iš
pirmo bandymo ir rt460_*.jpg iš antro.

Taisyklė: šviežias formos atidarymas pradeda švariai. Tuščias senas
juodraštis ištrinamas, turintis turinio — atrišamas ir pasiūlomas
tęsti (?tesk=<id>), o POST'as (perkrovimas su klaidomis) juodraščio
neliečia.

Paleidimas:  python docs/juodrasciu_sesijos_test.py
"""
import io, os, sys, tempfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
for k, v in (('SECRET_KEY', 'x'), ('EMAIL_USER', 'x@x.lt'), ('EMAIL_PASSWORD', 'x')):
    os.environ.setdefault(k, v)

import django
from django.conf import settings

LAIKINA = tempfile.mkdtemp(prefix='juodrasciai-')
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
from django.core.files.base import ContentFile
from django.test import Client

from apps.listings import juodrasciai
from apps.listings.models import (FuelType, Listing, ListingImage, TruckBrand,
                                  VehicleType)

gerai = blogai = 0
def tikrink(s, k):
    global gerai, blogai
    if s: gerai += 1
    else:
        blogai += 1
        print('  NEPAVYKO: ' + k)
def antraste(t):
    print('\n── ' + t + ' ' + '─' * max(0, 52 - len(t)))


# 1×1 px JPEG — tikras failas, ne tuščias baitas
JPEG = bytes.fromhex(
    'ffd8ffe000104a46494600010100000100010000ffdb004300ffffffffffffffffff'
    'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff'
    'ffffffffffffffffffffffffffffffffffffffffffffffffffffc2000b0801000100'
    '0101011100ffc40014000100000000000000000000000000000009ffda0008010100'
    '00013f10')

U = get_user_model()
u = U.objects.create_user(username='p@x.lt', email='p@x.lt', password='x')
if hasattr(u, 'profile'):
    u.profile.language = 'lt'
    u.profile.phone_number = '+37060000000'
    u.profile.save()
VT, _s = VehicleType.objects.get_or_create(slug='trucks', defaults={'name': 'Trucks'})
MARKE, _s = TruckBrand.objects.get_or_create(name='Renault')
KURAS, _s = FuelType.objects.get_or_create(name='Diesel')


def _butini():
    out = {}
    for f in Listing._meta.concrete_fields:
        if (f.primary_key or f.null or f.blank or f.has_default() or f.auto_created
                or getattr(f, 'auto_now', False) or getattr(f, 'auto_now_add', False)):
            continue
        it = f.get_internal_type()
        if it.endswith('IntegerField'): out[f.name] = 0
        elif it in ('DecimalField', 'FloatField'): out[f.name] = 0
        elif it in ('CharField', 'TextField', 'SlugField', 'EmailField', 'URLField'):
            out[f.name] = ''
        elif it == 'BooleanField': out[f.name] = False
    return out
BUTINI = _butini()


def juodrastis(**extra):
    d = dict(BUTINI)
    d.update(seller=u, vehicle_type=VT, title='', year=2018, price=0,
             country='LT', city='Vilnius', status='draft')
    d.update(extra)
    return Listing.objects.create(**d)


def nuotrauka(sk, vardas):
    return ListingImage.objects.create(
        listing=sk, image=ContentFile(JPEG, name=vardas), order=0)


c = Client()
c.force_login(u)
SESIJOS_RAKTAS = 'active_trucks_draft_id'


def prisek(sk):
    s = c.session
    s[SESIJOS_RAKTAS] = sk.pk
    s.save()


# ═══════════════════════════════════════════════════════════════════
antraste('1. Šviežias atidarymas nepaveldi senų nuotraukų')

senas = juodrastis(truck_brand=MARKE, truck_model_text='T460')
nuotrauka(senas, 'renault-t460_1.jpg')
nuotrauka(senas, 'renault-t460_2.jpg')
prisek(senas)

r = c.get('/create/trucks/', follow=True)
tikrink(r.status_code == 200, 'forma neatsidarė (%s)' % r.status_code)
tikrink(c.session.get(SESIJOS_RAKTAS) in (None, ''),
        'sesija vis dar rodo į seną juodraštį')
senas.refresh_from_db()
tikrink(senas.images.count() == 2, 'senos nuotraukos dingo — jų prarasti negalima')
kunas = r.content.decode('utf-8')
tikrink('renault-t460_1' not in kunas,
        'naujoje formoje matomos senojo juodraščio nuotraukos')
tikrink('tesk=%d' % senas.pk in kunas,
        'nepasiūlyta tęsti nebaigto skelbimo')


# ═══════════════════════════════════════════════════════════════════
antraste('2. Tuščias juodraštis ištrinamas, o ne kaupiasi')

tuscias_j = juodrastis()
prisek(tuscias_j)
c.get('/create/trucks/', follow=True)
tikrink(not Listing.objects.filter(pk=tuscias_j.pk).exists(),
        'tuščias juodraštis liko gulėti')


# ═══════════════════════════════════════════════════════════════════
antraste('3. ?tesk= tęsia tą patį juodraštį')

prisek(senas)
c.get('/create/trucks/', follow=True)          # atriša
r = c.get('/create/trucks/?tesk=%d' % senas.pk, follow=True)
tikrink(c.session.get(SESIJOS_RAKTAS) == senas.pk,
        'aiškiai paprašius tęsti juodraštis neprisirišo')
tikrink('renault-t460_1' in r.content.decode('utf-8'),
        'tęsiant nerodomos senos nuotraukos')


# ═══════════════════════════════════════════════════════════════════
antraste('4. Nepavykęs pateikimas juodraščio NEatriša')

BENDRI = {
    'truck_type': 'tractor', 'truck_brand': str(MARKE.pk),
    'truck_model_text': 'T460', 'year': '2018',
    'first_registration_month': '5', 'fuel_type': str(KURAS.pk),
    'defects': 'none', 'condition': 'used', 'price': '25000',
    'country': 'LT', 'city': 'Vilnius', 'phone': '+37060000000',
    'agree_terms': 'on', 'mileage': '500000',
}
prisek(senas)
duom = dict(BENDRI)
duom['engine_capacity'] = '10837'       # per didelė — pateikimas krenta
duom['engine_capacity_unit'] = 'L'
r = c.post('/create/trucks/', duom, follow=True)
tikrink(r.status_code == 200, 'nepavykęs pateikimas davė %s' % r.status_code)
tikrink(c.session.get(SESIJOS_RAKTAS) == senas.pk,
        'po klaidos juodraštis atrištas — įvesti duomenys ir nuotraukos dingtų')
senas.refresh_from_db()
tikrink(senas.status == 'draft', 'nepavykęs pateikimas paskelbė skelbimą')


# ═══════════════════════════════════════════════════════════════════
antraste('5. Antras bandymas negauna pirmojo nuotraukų')

# Žmogus po klaidos atsidaro formą iš naujo (be ?tesk=)
c.get('/create/trucks/', follow=True)
tikrink(c.session.get(SESIJOS_RAKTAS) in (None, ''), 'sesija liko prikabinta')

# ...ir įkelia KITAS nuotraukas į naują juodraštį
naujas = juodrastis(truck_brand=MARKE, truck_model_text='T460')
nuotrauka(naujas, 'rt460_1.jpg')
prisek(naujas)
duom = dict(BENDRI)
duom['engine_capacity'] = '12.0'
duom['engine_capacity_unit'] = 'L'
c.post('/create/trucks/', duom, follow=True)
naujas.refresh_from_db()
tikrink(naujas.status == 'active', 'antras bandymas nepaskelbtas (%s)' % naujas.status)
vardai = [i.image.name.rsplit('/', 1)[-1] for i in naujas.images.all()]
tikrink(all('renault-t460_' not in v for v in vardai),
        'į naują skelbimą pateko pirmojo bandymo nuotraukos: %s' % vardai)
tikrink(len(vardai) == 1, 'nuotraukų kiekis %d, tikėtasi 1' % len(vardai))


# ═══════════════════════════════════════════════════════════════════
antraste('6. Ta pati taisyklė VISOSE kategorijose')

VAIZDAI = ['trucks_views.py', 'views.py', 'motogear_views.py',
           'motorcycles_views.py', 'car_for_parts_views.py',
           'moto_for_parts_views.py', 'truck_for_parts_views.py']
be_taisykles = []
for v in VAIZDAI:
    t = io.open(os.path.join(BASE, 'apps/listings', v), encoding='utf-8').read()
    if 'juodrasciai' not in t:
        be_taisykles.append(v)
tikrink(not be_taisykles, 'kategorijos be švaraus atidarymo: %s' % be_taisykles)

# POST niekada nėra šviežias atidarymas
from django.test import RequestFactory
rf = RequestFactory()
tikrink(not juodrasciai.sviezias_atidarymas(rf.post('/create/trucks/')),
        'POST palaikytas šviežiu atidarymu')
tikrink(juodrasciai.sviezias_atidarymas(rf.get('/create/trucks/')),
        'paprastas GET nelaikomas šviežiu atidarymu')
tikrink(not juodrasciai.sviezias_atidarymas(rf.get('/create/trucks/?tesk=5')),
        '?tesk= palaikytas šviežiu atidarymu')
tikrink(not juodrasciai.sviezias_atidarymas(rf.get('/create/trucks/?edit=5')),
        '?edit= palaikytas šviežiu atidarymu')


# ═══════════════════════════════════════════════════════════════════
antraste('7. Valymo komandos')

komandos = os.path.join(BASE, 'apps/listings/management/commands')
tikrink(os.path.exists(os.path.join(komandos, 'valyti_juodrascius.py')),
        'nėra valyti_juodrascius komandos')
tikrink(os.path.exists(os.path.join(komandos, 'valyti_dubliuotas_nuotraukas.py')),
        'nėra valyti_dubliuotas_nuotraukas komandos')
tekstas = io.open(os.path.join(komandos, 'valyti_juodrascius.py'),
                  encoding='utf-8').read()
tikrink('expire_listings' in tekstas, 'komandos apraše nėra cron eilutės')

# Sena, nebetęsiama eilutė išvaloma
from django.utils import timezone
from datetime import timedelta
sena = juodrastis()
Listing.objects.filter(pk=sena.pk).update(
    updated_at=timezone.now() - timedelta(days=40))
call_command('valyti_juodrascius', verbosity=0)
tikrink(not Listing.objects.filter(pk=sena.pk).exists(),
        'senas tuščias juodraštis neištrintas')

# O turintis turinio — lieka (jį žmogus mato „Mano skelbimuose")
su_turiniu = juodrastis(description='Renault T460, geros būklės')
Listing.objects.filter(pk=su_turiniu.pk).update(
    updated_at=timezone.now() - timedelta(days=40))
call_command('valyti_juodrascius', verbosity=0)
tikrink(Listing.objects.filter(pk=su_turiniu.pk).exists(),
        'ištrintas juodraštis su turiniu')

# Dubliuotų nuotraukų valymas — kaip #754 atveju
dublis = juodrastis(status='active', title='Renault T460')
for v in ('renault-t460_1.jpg', 'renault-t460_2.jpg', 'rt460_1.jpg', 'rt460_2.jpg'):
    nuotrauka(dublis, v)
call_command('valyti_dubliuotas_nuotraukas', skelbimas=dublis.pk,
             trinti='renault-t460_', verbosity=0)
liko = [i.image.name.rsplit('/', 1)[-1] for i in dublis.images.order_by('order')]
tikrink(len(liko) == 2 and all('rt460_' in v for v in liko),
        'dublikatai neišvalyti: %s' % liko)
tikrink(dublis.images.filter(is_main=True).count() == 1,
        'po valymo nėra vienos pagrindinės nuotraukos')


print('\n' + '═' * 60)
print('gerai: %d, nepavyko: %d' % (gerai, blogai))
sys.exit(1 if blogai else 0)
