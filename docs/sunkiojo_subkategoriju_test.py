# -*- coding: utf-8 -*-
"""
SUNKUSIS TRANSPORTAS — PENKIOS SUBKATEGORIJOS, PENKI LAUKŲ RINKINIAI.

Iki šiol visos penkios (Sunkvežimiai, Vilkikai, Autotraukiniai/autovežiai,
Autobusai, Komunalinio ūkio transportas) buvo viena bendra forma:
vilkikas prašė „Tipo" iš sunkvežimių antstatų sąrašo (savivartis,
cisterna…), o ašių skaičiaus — kur jis tikrai reikalingas — nebuvo iš
viso.

Tikrinam visus šešis užduoties punktus:

  1. ?subcategory= išlieka skelbime ir matomas puslapyje bei antraštėje;
  2. Vilkikams „Tipas" nerodomas, užtat yra „Ašių skaičius";
  3. Sunkvežimiams „Tipas" ir „Bendroji masė" lieka;
  4. antraštė „MAN 18.510 4x2 2022 m Vilkikas";
  5. dublikato „— Pasirinkite —" nebėra;
  6. backfill komanda perkelia skelbimus ir išvalo „Tipą".

Paleidimas:  python docs/sunkiojo_subkategoriju_test.py
"""
import io, json, os, re, sys, tempfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
for k, v in (('SECRET_KEY', 'x'), ('EMAIL_USER', 'x@x.lt'), ('EMAIL_PASSWORD', 'x')):
    os.environ.setdefault(k, v)

import django
from django.conf import settings

LAIKINA = tempfile.mkdtemp(prefix='sunkusis-')
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
from django.utils import translation
from django.test import Client

from apps.listings import sunkusis
from apps.listings.models import (FuelType, Listing, SubCategory, TruckBrand,
                                  VehicleType)
from apps.listings.trucks_views import sunkiojo_antraste

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
if hasattr(u, 'profile'):
    u.profile.language = 'lt'
    u.profile.phone_number = '+37060000000'
    u.profile.save()

VT, _s = VehicleType.objects.get_or_create(slug='trucks',
                                           defaults={'name': 'Sunkvežimiai'})
SUB = {}
for slug, vardas, eile in (
        ('trucks', 'Sunkvežimiai', 1),
        ('semi-trucks-tractors', 'Vilkikai', 2),
        ('vehicle-transporters', 'Autotraukiniai, autovežiai', 3),
        ('buses', 'Autobusai', 4),
        ('municipal-transport', 'Komunalinio ūkio transportas', 5)):
    SUB[slug], _s = SubCategory.objects.get_or_create(
        vehicle_type=VT, slug=slug, defaults={'name': vardas, 'order': eile})
MARKE, _s = TruckBrand.objects.get_or_create(name='MAN')
KURAS, _s = FuelType.objects.get_or_create(name='Diesel')

c = Client()
c.force_login(u)

BENDRI = {
    'truck_brand': str(MARKE.pk), 'truck_model_text': '18.510',
    'year': '2022', 'first_registration_month': '5',
    'fuel_type': str(KURAS.pk), 'defects': 'none', 'condition': 'used',
    'price': '25000', 'country': 'LT', 'city': 'Vilnius',
    'phone': '+37060000000', 'agree_terms': 'on', 'mileage': '500000',
    'wheel_formula': '4x2',
}


# ═══════════════════════════════════════════════════════════════════
antraste('1. Penkios subkategorijos, penki rinkiniai')

tikrink(len(sunkusis.VISOS) == 5, 'ne penkios subkategorijos: %d'
        % len(sunkusis.VISOS))
for slug in ('trucks', 'semi-trucks-tractors', 'vehicle-transporters',
             'buses', 'municipal-transport'):
    tikrink(slug in sunkusis.VISOS, 'trūksta subkategorijos %s' % slug)
# Slug'ai tie patys, kuriuos naudoja pikeris
vaizdai = io.open(os.path.join(BASE, 'apps/listings/views.py'),
                  encoding='utf-8').read()
for slug in sunkusis.VISOS:
    tikrink("'%s'" % slug in vaizdai,
            'pikeris nepažįsta subkategorijos %s' % slug)
tikrink(sunkusis.normalizuok('nesamone') == 'trucks',
        'nežinomas slug\'as nekrinta į „trucks"')


# ═══════════════════════════════════════════════════════════════════
antraste('2. Vilkikams — be „Tipas", su „Ašių skaičius"')

tikrink(sunkusis.rodyti('semi-trucks-tractors', 'truck_type') is False,
        'vilkikams vis dar rodomas Tipas')
tikrink(sunkusis.rodyti('semi-trucks-tractors', 'axle_count') is True,
        'vilkikams nerodomas Ašių skaičius')
for kita in ('trucks', 'buses', 'vehicle-transporters', 'municipal-transport'):
    tikrink(sunkusis.rodyti(kita, 'truck_type') is True,
            '%s: dingo Tipas' % kita)
    tikrink(sunkusis.rodyti(kita, 'axle_count') is False,
            '%s: atsirado svetimas Ašių skaičius' % kita)

# Laukas modelyje su etalono reikšmėmis
laukas = Listing._meta.get_field('axle_count')
reiksmes = [v for v, _l in laukas.choices]
tikrink(reiksmes == ['1', '2', '3', 'more', 'other'],
        'netinkamos ašių reikšmės: %s' % reiksmes)
migr = [f for f in os.listdir(os.path.join(BASE, 'apps/listings/migrations'))
        if 'axle_count' in f]
tikrink(migr, 'nėra migracijos su axle_count')
tikrink(Listing._meta.get_field('sleeping_seats') is not None,
        'dingo miegamų vietų laukas')

# Forma iš tikrųjų rodo tai, ką sako lentelė
r = c.get('/create/trucks/?subcategory=semi-trucks-tractors', follow=True)
tikrink(r.status_code == 200, 'vilkikų forma neatsidarė (%s)' % r.status_code)
vilkiku_forma = r.content.decode('utf-8')
tikrink('name="truck_type"' not in vilkiku_forma,
        'vilkikų formoje vis dar yra Tipas')
tikrink('name="axle_count"' in vilkiku_forma,
        'vilkikų formoje nėra Ašių skaičiaus')

r = c.get('/create/trucks/?subcategory=trucks', follow=True)
sunkvezimiu_forma = r.content.decode('utf-8')
tikrink('name="truck_type"' in sunkvezimiu_forma,
        'sunkvežimių formoje dingo Tipas')
tikrink('name="axle_count"' not in sunkvezimiu_forma,
        'sunkvežimių formoje atsirado Ašių skaičius')


# ═══════════════════════════════════════════════════════════════════
antraste('3. Sunkvežimiams — Tipas su antstatais ir Bendroji masė')

tikrink('name="gross_weight_kg"' in sunkvezimiu_forma,
        'sunkvežimių formoje nėra Bendrosios masės')
for antstatas in ('tippers', 'refrigerators', 'tankers'):
    tikrink('value="%s"' % antstatas in sunkvezimiu_forma,
            'dingo antstatas %s' % antstatas)


# ═══════════════════════════════════════════════════════════════════
antraste('4. Antraštė „MAN 18.510 4x2 2022 m Vilkikas"')

l = Listing(truck_brand=MARKE, truck_model_text='18.510',
            wheel_formula='4x2', year=2022,
            subcategory=SUB['semi-trucks-tractors'])
tikrink(sunkiojo_antraste(l) == 'MAN 18.510 4x2 2022 m Vilkikas',
        'antraštė: %r' % sunkiojo_antraste(l))

l.subcategory = SUB['trucks']
tikrink(sunkiojo_antraste(l).endswith('Sunkvežimis'),
        'sunkvežimio antraštė: %r' % sunkiojo_antraste(l))

# Trūkstamos dalys tiesiog praleidžiamos — be tuščių vietų
l.wheel_formula = ''
tikrink('  ' not in sunkiojo_antraste(l),
        'antraštėje dviguba tarpų vieta: %r' % sunkiojo_antraste(l))
l.truck_model_text = ''
tikrink(sunkiojo_antraste(l) == 'MAN 2022 m Sunkvežimis',
        'be modelio: %r' % sunkiojo_antraste(l))


# ═══════════════════════════════════════════════════════════════════
antraste('5. Dubliuoto „— Pasirinkite —" nebėra')

for kunas, vardas in ((sunkvezimiu_forma, 'sunkvežimiai'),
                      (vilkiku_forma, 'vilkikai')):
    tuscios = re.findall(r'<option value=""[^>]*>([^<]*)</option>', kunas)
    for laukas_html in re.findall(
            r'<select name="(truck_type|axle_count)".*?</select>', kunas, re.S):
        pass
    for m in re.finditer(r'<select name="(truck_type|axle_count)"(.*?)</select>',
                         kunas, re.S):
        kiek = len(re.findall(r'<option value=""', m.group(2)))
        tikrink(kiek <= 1,
                '%s/%s: %d tuščios eilutės' % (vardas, m.group(1), kiek))

# Ir šaltinyje: sąrašas be tuščios, tuščią deda šablonas
from apps.listings.trucks_views import _truck_type_choices
tikrink(all(v for v, _l in _truck_type_choices()),
        '_truck_type_choices vis dar grąžina tuščią reikšmę')


# ═══════════════════════════════════════════════════════════════════
antraste('6. ?subcategory= išlieka nuo formos iki skelbimo')

def pateik(subkategorija, **papildomai):
    duom = dict(BENDRI)
    duom['subcategory'] = subkategorija
    duom.update(papildomai)
    return c.post('/create/trucks/?subcategory=%s' % subkategorija,
                  duom, follow=True)

r = pateik('semi-trucks-tractors', axle_count='2')
tikrink(r.status_code == 200, 'vilkiko pateikimas davė %s' % r.status_code)
vilkikas = Listing.objects.filter(
    subcategory=SUB['semi-trucks-tractors']).order_by('-pk').first()
tikrink(vilkikas is not None, 'vilkikas nepateko į savo subkategoriją')
if vilkikas:
    tikrink(vilkikas.axle_count == '2',
            'ašių skaičius neišsaugotas: %r' % vilkikas.axle_count)
    tikrink(vilkikas.title == 'MAN 18.510 4x2 2022 m Vilkikas',
            'antraštė: %r' % vilkikas.title)
    tikrink(not vilkikas.truck_type,
            'vilkikui prilipo Tipas: %r' % vilkikas.truck_type)
    # Skelbimo puslapyje matoma ir subkategorija, ir ašys
    r = c.get('/%d/' % vilkikas.pk, follow=True)
    puslapis = r.content.decode('utf-8')
    tikrink(r.status_code == 200, 'skelbimo puslapis %s' % r.status_code)
    tikrink('Vilkikai' in puslapis, 'puslapyje nematyti subkategorijos')
    tikrink('MAN 18.510 4x2 2022 m Vilkikas' in puslapis,
            'puslapyje nematyti naujos antraštės')
    # Antraštė nepriklauso nuo to, kokia kalba pildyta forma: ji
    # įrašoma vieną kartą ir rodoma visiems.
    for kalba in ('de', 'ru', 'en'):
        with translation.override(kalba):
            tikrink(sunkiojo_antraste(vilkikas)
                    == 'MAN 18.510 4x2 2022 m Vilkikas',
                    'antraštė %s kalba pasikeitė: %r'
                    % (kalba, sunkiojo_antraste(vilkikas)))
    # Kortelėje sąraše — irgi subkategorija, nes „Tipo" vilkikas neturi
    # ir žymė iš kortelės buvo dingusi visai
    r = c.get('/search/advanced/?category=trucks', follow=True)
    sarasas = r.content.decode('utf-8')
    tikrink('Vilkikai' in sarasas, 'kortelėje nematyti subkategorijos')
    # Redaguojant rodomi tie patys laukai — subkategorija paimama iš
    # paties skelbimo, o ne iš adreso
    r = c.get('/%d/edit-trucks/' % vilkikas.pk, follow=True)
    forma = r.content.decode('utf-8')
    tikrink('name="truck_type"' not in forma, 'redaguojant vilkikui rodomas Tipas')
    tikrink('name="axle_count"' in forma, 'redaguojant nėra ašių skaičiaus')
    tikrink('name="subcategory" value="semi-trucks-tractors"' in forma,
            'redaguojant subkategorija nekeliauja su forma')

# Sunkvežimis su Tipu — savo subkategorijoje
r = pateik('trucks', truck_type='tippers')
sunkvezimis = Listing.objects.filter(
    subcategory=SUB['trucks'], status='active').order_by('-pk').first()
tikrink(sunkvezimis is not None, 'sunkvežimis nepateko į savo subkategoriją')
if sunkvezimis:
    tikrink(sunkvezimis.truck_type == 'tippers',
            'Tipas neišsaugotas: %r' % sunkvezimis.truck_type)
    tikrink(sunkvezimis.title.endswith('Sunkvežimis'),
            'antraštė: %r' % sunkvezimis.title)

# Subkategorija turi atkeliauti ir į juodraštį — jį sukuria autosave,
# o ne formos atidarymas (šviežias atidarymas juodraščių nebekuria ir
# senų nebetęsia, žr. apps/listings/juodrasciai.py). Būtent čia
# pasirinkimas ir dingdavo: autosave'as apie jį nieko nežinojo ir
# naujas juodraštis guldavo į „Sunkvežimius".
c.get('/create/trucks/?subcategory=buses', follow=True)
c.post('/ajax/save-trucks-draft/',
       data=json.dumps({'subcategory': 'buses', 'truck_model_text': 'Tourismo'}),
       content_type='application/json')
juodrastis = Listing.objects.filter(seller=u, status='draft').order_by('-pk').first()
tikrink(juodrastis is not None and juodrastis.subcategory_id == SUB['buses'].pk,
        'autosave juodraštį įdėjo ne ten: %s'
        % (juodrastis.subcategory.slug if juodrastis
           and juodrastis.subcategory_id else '—'))

# Persigalvojus — tęsiant tą patį juodraštį (?tesk=) su kita
# subkategorija — įrašas turi persikelti, o ne likti senoje.
if juodrastis:
    c.get('/create/trucks/?tesk=%d&subcategory=municipal-transport' % juodrastis.pk,
          follow=True)
    juodrastis.refresh_from_db()
    tikrink(juodrastis.subcategory_id == SUB['municipal-transport'].pk,
            'persigalvojus subkategorija neatnaujinta: %s'
            % (juodrastis.subcategory.slug if juodrastis.subcategory_id else '—'))


# ═══════════════════════════════════════════════════════════════════
antraste('7. Backfill komanda')

kelias = os.path.join(BASE, 'apps/listings/management/commands',
                      'sunkiojo_subkategorijos.py')
tikrink(os.path.exists(kelias), 'nėra sunkiojo_subkategorijos komandos')

blogai_priskirtas = Listing.objects.filter(subcategory=SUB['trucks']).first()
if blogai_priskirtas:
    blogai_priskirtas.truck_type = 'tippers'
    blogai_priskirtas.save(update_fields=['truck_type'])
    # sausas bėgimas nieko nekeičia
    call_command('sunkiojo_subkategorijos', skelbimai=[blogai_priskirtas.pk],
                 subkategorija='semi-trucks-tractors', isvalyti_tipa=True,
                 verbosity=0)
    blogai_priskirtas.refresh_from_db()
    tikrink(blogai_priskirtas.subcategory_id == SUB['trucks'].pk,
            'sausas bėgimas jau perkėlė skelbimą')

    call_command('sunkiojo_subkategorijos', skelbimai=[blogai_priskirtas.pk],
                 subkategorija='semi-trucks-tractors', isvalyti_tipa=True,
                 patvirtinu=True, verbosity=0)
    blogai_priskirtas.refresh_from_db()
    tikrink(blogai_priskirtas.subcategory_id == SUB['semi-trucks-tractors'].pk,
            'skelbimas neperkeltas į Vilkikus')
    tikrink(not blogai_priskirtas.truck_type,
            'Tipas neišvalytas: %r' % blogai_priskirtas.truck_type)
    tikrink(blogai_priskirtas.title.endswith('Vilkikas'),
            'antraštė neperrašyta: %r' % blogai_priskirtas.title)

# Nežinoma subkategorija — komanda sustoja, o ne tyliai perkelia
from django.core.management.base import CommandError
try:
    call_command('sunkiojo_subkategorijos', skelbimai=[1],
                 subkategorija='nesamone', verbosity=0)
    tikrink(False, 'nežinoma subkategorija praėjo')
except CommandError:
    tikrink(True, '')


print('\n' + '═' * 60)
print('gerai: %d, nepavyko: %d' % (gerai, blogai))
sys.exit(1 if blogai else 0)
