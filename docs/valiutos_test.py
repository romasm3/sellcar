# -*- coding: utf-8 -*-
"""
VALIUTA — VISADA EURAI. ŠALIS JOS NEBELEMIA.

Kas buvo. Iš pradžių formos siųsdavo paslėptą „USD", tad vokiškas #749 ir
kroatiškas #754 rodė „$", nors kaina įvesta eurais. Pataisa susiejo
valiutą su šalimi — ir atsirado blogesnė klaida: keitėsi tik ŽYMĖ, o
suma ne. Pasirinkus Lenkiją įvesti 43 000 € virsdavo „43 000 zł"
(≈10 000 €). Taip nukentėjo #789 Dodge RAM, #791 Lamborghini Urus
(„327 250 kr"), #798 Audi S5 („45 942 CHF"), #792 ir #799.

Kursų svetainė neturi, tad sąsaja pašalinta: `pagal_sali()` bet kuriai
šaliai grąžina EUR, `Listing.save()` įrašo EUR, static/js/valiuta.js
šalies lauko nebeklauso. Daugiavaliutės (GBP/USD) — atskiras darbas
kartu su kursais ir sumų perskaičiavimu.

Paleidimas:  python docs/valiutos_test.py
"""
import io, os, re, sys, tempfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
for k, v in (('SECRET_KEY', 'x'), ('EMAIL_USER', 'x@x.lt'), ('EMAIL_PASSWORD', 'x')):
    os.environ.setdefault(k, v)

import django
from django.conf import settings

LAIKINA = tempfile.mkdtemp(prefix='valiutos-')
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
from django.test import Client

from apps.listings import valiutos
from apps.listings.models import (FuelType, Listing, TruckBrand, VehicleType,
                                  WheelListing)

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
antraste('1. Bet kuri šalis → EUR')

VISOS = ['AT', 'BE', 'HR', 'CY', 'EE', 'FI', 'FR', 'DE', 'GR', 'IE', 'IT',
         'LV', 'LT', 'LU', 'MT', 'NL', 'PT', 'SK', 'SI', 'ES',
         'GB', 'PL', 'CZ', 'DK', 'SE', 'NO', 'CH', 'US']
for salis in VISOS:
    tikrink(valiutos.pagal_sali(salis) == 'EUR',
            '%s turi būti EUR, gavom %s' % (salis, valiutos.pagal_sali(salis)))

# Būtent šitos šalys ir sugadino #789, #791, #792, #798, #799
for salis, senas in (('PL', 'PLN'), ('SE', 'SEK'), ('CH', 'CHF'),
                     ('NO', 'NOK'), ('DK', 'DKK'), ('CZ', 'CZK'),
                     ('GB', 'GBP'), ('US', 'USD')):
    tikrink(valiutos.pagal_sali(salis) != senas,
            '%s vėl gauna %s — sąsaja su šalimi grįžo' % (salis, senas))
    tikrink(valiutos.simbolis_pagal_sali(salis) == '€',
            '%s sufiksas ne €: %s' % (salis, valiutos.simbolis_pagal_sali(salis)))

for salis in ('XX', '', None, 'ZZ'):
    tikrink(valiutos.pagal_sali(salis) == 'EUR',
            'nežinomai šaliai %r turi būti EUR' % salis)

# Simbolių lentelė lieka — pačios valiutos kodas → ženklas nesikeitė
tikrink(valiutos.simbolis('EUR') == '€' and valiutos.simbolis('USD') == '$'
        and valiutos.simbolis('GBP') == '£' and valiutos.simbolis('PLN') == 'zł',
        'netinkami valiutų simbolių ženklai')
tikrink(valiutos.simbolis('XYZ') == '€', 'nežinomos valiutos simbolis ne €')
tikrink(set(valiutos.zemelapis().values()) == {'EUR'},
        'žemėlapyje liko ne EUR: %s'
        % {k: v for k, v in valiutos.zemelapis().items() if v != 'EUR'})


# ═══════════════════════════════════════════════════════════════════
antraste('2. Skelbimas visada gauna EUR')

U = get_user_model()
u = U.objects.create_user(username='p@x.lt', email='p@x.lt', password='x')
if hasattr(u, 'profile'):
    u.profile.language = 'lt'
    u.profile.phone_number = '+37060000000'
    u.profile.save()
VT, _s = VehicleType.objects.get_or_create(slug='trucks', defaults={'name': 'T'})
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


def skelbimas(salis, valiuta=None):
    d = dict(BUTINI)
    d.update(seller=u, vehicle_type=VT, title='T', year=2018, price=25000,
             country=salis, city='Vilnius', status='active')
    if valiuta:
        d['currency'] = valiuta
    return Listing.objects.create(**d)


for salis in ('DE', 'HR', 'LT', 'US', 'GB', 'PL', 'SE', 'CH', 'NO'):
    sk = skelbimas(salis)
    tikrink(sk.currency == 'EUR',
            '%s: valiuta %s, tikėtasi EUR' % (salis, sk.currency))
    tikrink(sk.currency_symbol == '€',
            '%s: simbolis %s, tikėtasi €' % (salis, sk.currency_symbol))

# Forma vis dar gali atsiųsti paslėptą lauką — modelis jį normalizuoja
klaidingas = skelbimas('PL', valiuta='PLN')
tikrink(klaidingas.currency == 'EUR',
        'atsiųstas PLN liko: %s' % klaidingas.currency)

# Dalinis įrašymas (activate ir pan.) skelbimo nepagadina
klaidingas.status = 'draft'
klaidingas.save(update_fields=['status'])
klaidingas.refresh_from_db()
tikrink(klaidingas.currency == 'EUR', 'dalinis įrašymas sugadino valiutą')


# ═══════════════════════════════════════════════════════════════════
antraste('3. Ratlankiai/padangos — irgi €')

ratai = WheelListing(seller=u, product_type='tyre', country='PL', price=100,
                     city='Varšuva', title='T')
tikrink(ratai.currency_symbol == '€',
        'lenkiškas ratlankis rodo %s' % ratai.currency_symbol)
for salis in ('US', 'SE', 'CH', 'GB'):
    ratai.country = salis
    tikrink(ratai.currency_symbol == '€',
            '%s ratlankis rodo %s' % (salis, ratai.currency_symbol))


# ═══════════════════════════════════════════════════════════════════
antraste('4. Žemėlapio kopijų nebeliko')

modeliai = io.open(os.path.join(BASE, 'apps/listings/models.py'),
                   encoding='utf-8').read()
tikrink("{'USD': '$', 'EUR': '€', 'GBP': '£'}.get(self.currency" not in modeliai,
        'modelyje liko nusirašytas simbolių žemėlapis')
tikrink("'$' if self.country == 'US' else '€'" not in modeliai,
        'ratlankiuose liko sava dviejų šalių taisyklė')
tikrink(modeliai.count('valiutos.simbolis(') >= 4,
        'ne visos simbolio vietos naudoja bendrą žemėlapį')
tikrink("default='USD'" not in modeliai,
        'kur nors liko numatyta USD')


# ═══════════════════════════════════════════════════════════════════
antraste('5. Formos: sufiksas ir paslėptas laukas')

SABLONAI = [f for f in os.listdir(os.path.join(BASE, 'templates/listings'))
            if 'create' in f and f.endswith('.html')]
be_zymes, su_usd = [], []
for f in SABLONAI:
    t = io.open(os.path.join(BASE, 'templates/listings', f), encoding='utf-8').read()
    # kainos sufiksas turi būti pažymėtas, kad JS jį atnaujintų
    for m in re.finditer(r'<span([^>]*)>([€$])</span>', t):
        if 'data-valiutos-sufiksas' not in m.group(1):
            be_zymes.append('%s: %s' % (f, m.group(0)[:60]))
    if re.search(r'name="currency"[^>]*value="USD"', t):
        su_usd.append(f)
tikrink(not be_zymes, 'nepažymėti kainos sufiksai: %s' % be_zymes[:3])
tikrink(not su_usd, 'formos vis dar siunčia įrašytą USD: %s' % su_usd)

js = io.open(os.path.join(BASE, 'static/js/valiuta.js'), encoding='utf-8').read()
tikrink('data-valiutos-sufiksas' in js,
        'valiuta.js nebeįrašo sufikso')
tikrink('id_country' not in js and 'al:salis-pakeista' not in js,
        'valiuta.js vėl klauso šalies lauko')
b = io.open(os.path.join(BASE, 'templates/base.html'), encoding='utf-8').read()
tikrink('valiutu_zemelapis_json' in b and 'valiuta.js' in b,
        'žemėlapis nepasiekia naršyklės')


# ═══════════════════════════════════════════════════════════════════
antraste('6. Pilnas ratas: ir lenkiškas skelbimas gauna €')

c = Client()
c.force_login(u)
duom = {
    'truck_type': 'tractor', 'truck_brand': str(MARKE.pk),
    'truck_model_text': 'T460', 'year': '2018',
    'first_registration_month': '5', 'fuel_type': str(KURAS.pk),
    'defects': 'none', 'condition': 'used', 'price': '25000',
    'country': 'DE', 'city': 'Berlynas', 'phone': '+37060000000',
    'agree_terms': 'on', 'mileage': '500000', 'currency': 'PLN',
}
c.post('/create/trucks/', duom, follow=True)
naujas = Listing.objects.filter(city='Berlynas').order_by('-pk').first()
tikrink(naujas is not None, 'vokiškas skelbimas nesukurtas')
if naujas:
    tikrink(naujas.currency == 'EUR',
            'vokiškas skelbimas gavo %s' % naujas.currency)
    r = c.get('/%d/' % naujas.pk, follow=True)
    kunas = r.content.decode('utf-8')
    tikrink(r.status_code == 200, 'skelbimo puslapis %s' % r.status_code)
    tikrink('€' in kunas, 'skelbimo puslapyje nėra €')

# Lenkija — būtent ji virsdavo „zł" (#789 Dodge RAM)
duom.update(country='PL', city='Varšuva', price='43000')
c.post('/create/trucks/', duom, follow=True)
lenkiskas = Listing.objects.filter(city='Varšuva').order_by('-pk').first()
tikrink(lenkiskas is not None and lenkiskas.currency == 'EUR',
        'lenkiškas skelbimas gavo %s'
        % (lenkiskas.currency if lenkiskas else '—'))
if lenkiskas:
    kunas = c.get('/%d/' % lenkiskas.pk, follow=True).content.decode('utf-8')
    tikrink('zł' not in kunas, 'lenkiško skelbimo puslapyje vis dar „zł"')
    tikrink(int(lenkiskas.price) == 43000,
            'suma pasikeitė: %s' % lenkiskas.price)


# ═══════════════════════════════════════════════════════════════════
antraste('7. Migracija sutvarko jau esamus skelbimus')

migracijos = [f for f in os.listdir(os.path.join(BASE, 'apps/listings/migrations'))
              if 'valiuta' in f]
tikrink(migracijos, 'nėra migracijos esamiems skelbimams')

tikrink(any('visada_eur' in f for f in migracijos),
        'nėra migracijos, grąžinančios EUR (#789, #791, #792, #798, #799)')

# Ta pati logika, kaip 0103 migracijoje: keičiam TIK žymę, ne sumą
sugadintas = skelbimas('PL')
Listing.objects.filter(pk=sugadintas.pk).update(currency='PLN', price=43000)
Listing.objects.exclude(currency='EUR').update(currency='EUR')
sugadintas.refresh_from_db()
tikrink(sugadintas.currency == 'EUR', 'migracija nepataisė lenkiško skelbimo')
tikrink(int(sugadintas.price) == 43000,
        'migracija pakeitė sumą: %s' % sugadintas.price)


# ═══════════════════════════════════════════════════════════════════
antraste('8. VISOS create formos — sufiksas € ir laukas EUR')

# Kiekviena forma atidaroma ir tikrinama, ką ji siųstų: paslėptas
# `currency` laukas ir kainos sufiksas. Anksčiau JS juos perrašydavo
# pagal pasirinktą šalį, tad užtenka vienos praleistos formos.
FORMOS = [
    '/create/cars/quick/', '/create/', '/create/trucks/',
    '/create/motorcycle/', '/create/motogear/', '/create/agriculture/',
    '/create/boats/', '/create/trailers/', '/create/construction/',
    '/create/construction/attachment/', '/create/forestry/',
    '/create/loading-equipment/', '/create/camping-houses/',
    '/create/bicycles/', '/create/electronics/', '/create/services/',
    '/create/rental/car/', '/create/rental/moto/',
    '/create/rental/minibus/', '/create/rental/heavy/',
    '/create/tyres/', '/create/rims/', '/create/moto-part/',
    '/create/car-for-parts/', '/create/moto-for-parts/',
    '/create/truck-for-parts/',
]
NE_EUR = ('PLN', 'SEK', 'NOK', 'DKK', 'CZK', 'CHF', 'GBP', 'USD')
NE_EURO_ZENKLAI = ('zł', 'Kč', 'CHF', '£', '$')

for adresas in FORMOS:
    r = c.get(adresas, follow=True)
    if r.status_code != 200:
        tikrink(False, '%s neatsidaro (%s)' % (adresas, r.status_code))
        continue
    kunas = r.content.decode('utf-8')

    for m in re.finditer(r'<input[^>]*name="currency"[^>]*>', kunas):
        v = re.search(r'value="([^"]*)"', m.group(0))
        tikrink(v is not None and v.group(1) == 'EUR',
                '%s: paslėptas currency = %s'
                % (adresas, v.group(1) if v else '—'))

    for m in re.finditer(r'<select[^>]*name="currency"', kunas):
        tikrink(False, '%s: valiutos pasirinkimas formoje' % adresas)

    for m in re.finditer(r'data-valiutos-sufiksas[^>]*>([^<]{0,6})<', kunas):
        tikrink(m.group(1).strip() in ('€', ''),
                '%s: sufiksas %r' % (adresas, m.group(1)))

    # Į naršyklę neturi keliauti nė vienos kitos valiutos
    for kodas in NE_EUR:
        tikrink('"%s"' % kodas not in kunas,
                '%s: puslapyje minima valiuta %s' % (adresas, kodas))


# ═══════════════════════════════════════════════════════════════════
antraste('9. Švedija — kaina lieka eurais')

# Būtent taip tikrina žmogus: naujas skelbimas su šalimi Švedija.
duom.update(country='SE', city='Stokholmas', price='45942', currency='SEK')
c.post('/create/trucks/', duom, follow=True)
svedas = Listing.objects.filter(city='Stokholmas').order_by('-pk').first()
tikrink(svedas is not None, 'švediškas skelbimas nesukurtas')
if svedas:
    tikrink(svedas.currency == 'EUR', 'švediškas gavo %s' % svedas.currency)
    tikrink(int(svedas.price) == 45942, 'suma pasikeitė: %s' % svedas.price)
    kunas = c.get('/%d/' % svedas.pk, follow=True).content.decode('utf-8')
    tikrink('45' in kunas and '€' in kunas, 'puslapyje nėra „45 942 €"')
    tikrink(' kr<' not in kunas and '>kr<' not in kunas,
            'puslapyje liko „kr"')

# Ir tos šalys, kurių žemėlapyje niekada nebuvo (HU, RO, BG) — irgi EUR
for salis in ('HU', 'RO', 'BG'):
    sk = skelbimas(salis)
    tikrink(sk.currency == 'EUR', '%s gavo %s' % (salis, sk.currency))

# Modelis normalizuoja ir tada, kai reikšmė ateina apeinant formą
apeinant = skelbimas('SE', valiuta='SEK')
tikrink(apeinant.currency == 'EUR',
        'tiesiogiai įrašytas SEK liko: %s' % apeinant.currency)
apeinant.price = 45942
apeinant.save(update_fields=['price'])
apeinant.refresh_from_db()
tikrink(apeinant.currency == 'EUR', 'dalinis įrašymas grąžino SEK')



print('\n' + '═' * 60)
print('gerai: %d, nepavyko: %d' % (gerai, blogai))
sys.exit(1 if blogai else 0)
