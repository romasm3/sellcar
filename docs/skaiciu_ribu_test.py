# -*- coding: utf-8 -*-
"""
PER DIDELIS SKAIČIUS DUODA ŽINUTĘ, O NE 500.

Kas buvo. `engine_capacity` yra DecimalField(max_digits=5,
decimal_places=1) — telpa iki 9999,9. Sunkvežimių forma prašo LITRŲ
(„pvz., 12,0"), o žmogus įrašo kubinius centimetrus: 10837. Postgres
tokio skaičiaus nepriima, Django to negaudo, ir vietoj klaidos žmogus
gauna 500 — o kartu pakibusį juodraštį su jau įkeltomis nuotraukomis.

Modelio validatoriai vieni nepadeda: vaizdai objektą užpildo ir kviečia
`save()`, o `full_clean()` — ne. Todėl ribas tikrinam patys, prieš
įrašymą (apps/listings/skaiciai.py).

Paleidimas:  python docs/skaiciu_ribu_test.py
"""
import io, os, sys, tempfile
from decimal import Decimal

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
for k, v in (('SECRET_KEY', 'x'), ('EMAIL_USER', 'x@x.lt'), ('EMAIL_PASSWORD', 'x')):
    os.environ.setdefault(k, v)

import django
from django.conf import settings

LAIKINA = tempfile.mkdtemp(prefix='ribos-')
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

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models as dj_models

from apps.listings import skaiciai
from apps.listings.models import Listing, WheelListing

gerai = blogai = 0
def tikrink(s, k):
    global gerai, blogai
    if s: gerai += 1
    else:
        blogai += 1
        print('  NEPAVYKO: ' + k)
def antraste(t):
    print('\n── ' + t + ' ' + '─' * max(0, 52 - len(t)))


# ═══════════════════════════════════════════════════════════════════
antraste('1. Ribos imamos iš paties modelio')

RIBOS = {
    'engine_capacity': Decimal('9999.9'),
    'fuel_consumption_city': Decimal('999.9'),
    'fuel_consumption_highway': Decimal('999.9'),
    'fuel_consumption_combined': Decimal('999.9'),
    'price': Decimal('99999999.99'),
    'export_price': Decimal('99999999.99'),
    'truck_volume_m3': Decimal('9999.99'),
    'power': 9999,
    'mileage': 9999999,
    'curb_weight': 99999,
    'gross_weight_kg': 999999,
    'payload_kg': 999999,
    'co2_emission': 9999,
    'engine_hours': 999999,
}
for laukas, virsus in RIBOS.items():
    f = Listing._meta.get_field(laukas)
    _, gauta = skaiciai.ribos(f)
    tikrink(gauta is not None and Decimal(str(gauta)) == Decimal(str(virsus)),
            '%s: riba %s, tikėtasi %s' % (laukas, gauta, virsus))

# Nė vienas skaitinis laukas nelieka be ribos — naujas laukas
# apsaugotas savaime
be_ribu = []
for M in (Listing, WheelListing):
    for f in M._meta.concrete_fields:
        if not isinstance(f, (dj_models.IntegerField, dj_models.DecimalField,
                              dj_models.FloatField)) or f.primary_key:
            continue
        _, virsus = skaiciai.ribos(f)
        if virsus is None:
            be_ribu.append('%s.%s' % (M.__name__, f.name))
tikrink(not be_ribu, 'skaitiniai laukai be ribos: %s' % be_ribu[:5])


# ═══════════════════════════════════════════════════════════════════
antraste('2. Modelyje surašyti validatoriai (admin ir formos)')

BUTINI = ['engine_capacity', 'fuel_consumption_city', 'fuel_consumption_highway',
          'fuel_consumption_combined', 'price', 'export_price', 'truck_volume_m3',
          'power', 'mileage', 'curb_weight', 'gross_weight_kg', 'payload_kg',
          'co2_emission', 'engine_hours']
for laukas in BUTINI:
    f = Listing._meta.get_field(laukas)
    turi_max = any(isinstance(v, MaxValueValidator) for v in f.validators)
    turi_min = any(isinstance(v, MinValueValidator) for v in f.validators)
    tikrink(turi_max and turi_min, '%s: trūksta Min/MaxValueValidator' % laukas)


# ═══════════════════════════════════════════════════════════════════
antraste('3. Reikšmė netelpa — randama tiek objekte, tiek POST\'e')

l = Listing(engine_capacity=Decimal('10837'))
klaidos = skaiciai.patikra(l)
tikrink('engine_capacity' in klaidos, '10837 l nepagauta objekte')
tikrink('9999,9' in klaidos.get('engine_capacity', ''),
        'žinutėje nėra ribos: %r' % klaidos.get('engine_capacity'))
tikrink('Variklio' in klaidos.get('engine_capacity', ''),
        'žinutėje nėra lauko pavadinimo: %r' % klaidos.get('engine_capacity'))

tikrink('engine_capacity' in skaiciai.patikra_posto(
    Listing, {'engine_capacity': '10837'}), '10837 nepagauta POST\'e')
# Kablelis (lietuviška klaviatūra) — ne klaida
tikrink(not skaiciai.patikra_posto(Listing, {'engine_capacity': '12,0'}),
        '„12,0" palaikyta netinkama')
tikrink(not skaiciai.patikra(Listing(engine_capacity=Decimal('12.0'))),
        'teisinga reikšmė palaikyta netinkama')
# Neigiama
tikrink('price' in skaiciai.patikra_posto(Listing, {'price': '-5'}),
        'neigiama kaina praėjo')
# Ne skaičius netikrinamas čia (tai formos bėda)
tikrink(not skaiciai.patikra_posto(Listing, {'price': 'labas'}),
        'tekstas palaikytas per dideliu skaičiumi')


# ═══════════════════════════════════════════════════════════════════
antraste('4. Sunkvežimių forma: 10837 → žinutė, ne 500')

from django.contrib.auth import get_user_model
from django.test import Client
from apps.listings.models import TruckBrand, VehicleType, FuelType, SubCategory

U = get_user_model()
u = U.objects.create_user(username='p@x.lt', email='p@x.lt', password='x')
if hasattr(u, 'profile'):
    u.profile.language = 'lt'
    u.profile.phone_number = '+37060000000'
    u.profile.save()
VehicleType.objects.get_or_create(slug='trucks', defaults={'name': 'Trucks'})
marke, _sk = TruckBrand.objects.get_or_create(name='Renault')
kuras, _sk = FuelType.objects.get_or_create(name='Diesel')

c = Client()
c.force_login(u)

BENDRI = {
    'truck_type': 'tractor', 'truck_brand': str(marke.pk),
    'truck_model_text': 'T460', 'year': '2018',
    'first_registration_month': '5', 'fuel_type': str(kuras.pk),
    'defects': 'none', 'condition': 'used', 'price': '25000',
    'country': 'LT', 'city': 'Vilnius', 'phone': '+37060000000',
    'agree_terms': 'on', 'mileage': '500000',
}

def pateik(**papildomai):
    duom = dict(BENDRI)
    duom.update(papildomai)
    return c.post('/create/trucks/', duom, follow=True)

# a) litrai + 10837 → žinutė, ne 500, ir skelbimas nepaskelbtas
r = pateik(engine_capacity='10837', engine_capacity_unit='L')
tikrink(r.status_code == 200, 'per didelis tūris davė %s' % r.status_code)
kunas = r.content.decode('utf-8')
tikrink('negali viršyti' in kunas, 'nerodoma žinutė apie per didelę reikšmę')
tikrink('cm³' in kunas, 'žinutė nesiūlo cm³')
tikrink(not Listing.objects.filter(status='active').exists(),
        'skelbimas paskelbtas nepaisant netinkamos reikšmės')

# b) TA PATI reikšmė su cm³ — priimama ir virsta 10,8 l
r = pateik(engine_capacity='10837', engine_capacity_unit='cm3')
tikrink(r.status_code == 200, 'cm³ reikšmė davė %s' % r.status_code)
paskelbtas = Listing.objects.filter(status='active').first()
tikrink(paskelbtas is not None, 'cm³ reikšmė nepriimta')
if paskelbtas:
    tikrink(str(paskelbtas.engine_capacity) == '10.8',
            'cm³ neperskaičiuoti į litrus: %s' % paskelbtas.engine_capacity)
    paskelbtas.delete()

# c) teisingi litrai
r = pateik(engine_capacity='12.0', engine_capacity_unit='L')
tikrink(r.status_code == 200, 'teisingas tūris davė %s' % r.status_code)
paskelbtas = Listing.objects.filter(status='active').first()
tikrink(paskelbtas is not None, 'teisingas skelbimas nepaskelbtas')
if paskelbtas:
    tikrink(str(paskelbtas.engine_capacity) == '12.0',
            'tūris išsaugotas neteisingai: %s' % paskelbtas.engine_capacity)
    paskelbtas.delete()

# d) be jokio vieneto (senas klientas) — elgiamės kaip su saugojimo vienetu
r = pateik(engine_capacity='10837')
tikrink(r.status_code == 200, 'be vieneto davė %s' % r.status_code)
tikrink(not Listing.objects.filter(status='active').exists(),
        'be vieneto per didelė reikšmė praėjo')


# ═══════════════════════════════════════════════════════════════════
antraste('5. Patikra prijungta VISOSE formose')

VAIZDAI = ['agriculture_views.py', 'bicycles_views.py', 'boats_views.py',
           'camping_views.py', 'construction_views.py', 'electronics_views.py',
           'forestry_views.py', 'loading_views.py', 'rental_views.py',
           'services_views.py', 'trailers_views.py', 'motogear_views.py',
           'motorcycles_views.py', 'parts_views.py', 'moto_part_views.py',
           'trucks_views.py', 'wheels_views.py', 'views.py',
           'listing_helpers.py']
be_patikros = []
for v in VAIZDAI:
    t = io.open(os.path.join(BASE, 'apps/listings', v), encoding='utf-8').read()
    if 'skaiciai' not in t:
        be_patikros.append(v)
tikrink(not be_patikros, 'be skaičių patikros: %s' % be_patikros)


# ═══════════════════════════════════════════════════════════════════
antraste('6. Kliento pusės perspėjimas dėl L / cm³')

js = io.open(os.path.join(BASE, 'static/js/unit_toggle.js'), encoding='utf-8').read()
tikrink('PERSPEJIMAI' in js, 'unit_toggle.js neturi perspėjimų')
tikrink('engine_capacity: { virs: 100 }' in js.replace('  ', ' ')
        or 'engine_capacity: { virs: 100 }' in js,
        'nėra perspėjimo ties 100 l')
tikrink('perskaitykKitaisVienetais' in js,
        'nėra būdo perskaityti reikšmę kitais vienetais')
b = io.open(os.path.join(BASE, 'templates/base.html'), encoding='utf-8').read()
tikrink('UNIT_WARN_TEXT' in b, 'perspėjimo tekstas neverčiamas (nėra base.html)')



# ═══════════════════════════════════════════════════════════════════
antraste('7. Vienetai keliauja kartu su reikšme')

from django.test import RequestFactory
from apps.listings import units
from apps.listings.units import VienetuMiddleware

rf = RequestFactory()
mw = VienetuMiddleware(lambda r: r)

r = rf.post('/', {'engine_capacity': '10837', 'engine_capacity_unit': 'cm3'})
mw(r)
tikrink(r.POST['engine_capacity'] == '10.8',
        'cm³ neperskaičiuoti: %s' % r.POST['engine_capacity'])
tikrink(r.POST['engine_capacity_unit'] == 'L',
        'po normalizavimo vienetas turi būti saugojimo')

r = rf.post('/', {'mileage': '100', 'mileage_unit': 'mi'})
mw(r)
tikrink(r.POST['mileage'] == '161', 'mylios neperskaičiuotos: %s' % r.POST['mileage'])
tikrink('.' not in r.POST['mileage'], 'sveikam laukui liko trupmena')

r = rf.post('/', {'curb_weight': '3000', 'curb_weight_unit': 'lb'})
mw(r)
tikrink(r.POST['curb_weight'] == '1361', 'svarai neperskaičiuoti')

# Kanoninė reikšmė NEKEIČIAMA — dvigubo vertimo negali būti
r = rf.post('/', {'engine_capacity': '12.0', 'engine_capacity_unit': 'L'})
mw(r)
tikrink(r.POST['engine_capacity'] == '12.0', 'kanoninė reikšmė pakeista')
r = rf.post('/', {'engine_capacity': '12.0'})
mw(r)
tikrink(r.POST['engine_capacity'] == '12.0', 'reikšmė be vieneto pakeista')

# Žinutė įvardija vienetą ir siūlo kitą
zinute = units.per_didele('engine_capacity', 10837, 'L')
tikrink('30' in zinute and '10' in zinute and 'cm³' in zinute,
        'žinutėje trūksta ribos, įvestos reikšmės arba pasiūlymo: %r' % zinute)
tikrink(units.per_didele('engine_capacity', Decimal('10.8'), 'cm3') is None,
        '10,8 l palaikyta per didele')

# Jungikliai NIEKUR nedingo — jie yra sąmoninga funkcija
js = io.open(os.path.join(BASE, 'static/js/unit_toggle.js'), encoding='utf-8').read()
for zenklas in ("engine_capacity:", "mileage:", "curb_weight:",
                "canonical: 'L'", "alt: 'cm³'", "alt: 'mi'", "alt: 'lbs'"):
    tikrink(zenklas in js, 'unit_toggle.js dingo jungiklis: %s' % zenklas)
tikrink("_unit'" in js or '_unit"' in js or "'_unit'" in js
        or "f.origName + '_unit'" in js,
        'naršyklė nesiunčia vieneto kartu su reikšme')
tikrink('VienetuMiddleware' in io.open(
    os.path.join(BASE, 'config/settings.py'), encoding='utf-8').read(),
    'normalizavimas neprijungtas prie užklausų')

# Pasirinkimas išlieka perkrovus formą (klaidos, ?edit=) — jungiklio
# būsena laikoma localStorage'e pagal šeimą
tikrink('savePref' in js and 'loadPrefs' in js and 'localStorage' in js,
        'jungiklio pasirinkimas neišsaugomas tarp perkrovimų')
tikrink('STORAGE_KEY' in js, 'nėra vietos, kur laikomas pasirinkimas')


print('\n' + '═' * 60)
print('gerai: %d, nepavyko: %d' % (gerai, blogai))
sys.exit(1 if blogai else 0)
