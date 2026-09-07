# -*- coding: utf-8 -*-
"""
VALIUTA SEKA ŠALĮ — VIENAS ŽEMĖLAPIS VISAI SVETAINEI.

Kas buvo. Šalis→valiuta žemėlapio NEBUVO VISAI: įkėlimo formos siųsdavo
paslėptą „USD", tad vokiškas #749 ir kroatiškas #754 rodė „$", nors
kaina įvesta eurais. Lietuviškas #727 rodė „€" tik todėl, kad modelio
numatytoji reikšmė yra EUR. Simbolių žemėlapis dar buvo nusirašytas
keturis kartus modelyje ir penktą — ratlankiuose („$ jei US, kitaip €").

Dabar viskas iš apps/listings/valiutos.py: euro zona → EUR, GB→GBP,
PL→PLN, CZ→CZK, DK→DKK, SE→SEK, NO→NOK, CH→CHF, US→USD, nežinoma → EUR
(rinka — Europa).

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
antraste('1. Žemėlapis — visa euro zona ir kaimynai')

EURO = ['AT', 'BE', 'HR', 'CY', 'EE', 'FI', 'FR', 'DE', 'GR', 'IE', 'IT',
        'LV', 'LT', 'LU', 'MT', 'NL', 'PT', 'SK', 'SI', 'ES']
for salis in EURO:
    tikrink(valiutos.pagal_sali(salis) == 'EUR',
            '%s turi būti EUR, gavom %s' % (salis, valiutos.pagal_sali(salis)))

KITOS = {'GB': 'GBP', 'PL': 'PLN', 'CZ': 'CZK', 'DK': 'DKK',
         'SE': 'SEK', 'NO': 'NOK', 'CH': 'CHF', 'US': 'USD'}
for salis, valiuta in KITOS.items():
    tikrink(valiutos.pagal_sali(salis) == valiuta,
            '%s turi būti %s, gavom %s' % (salis, valiuta,
                                           valiutos.pagal_sali(salis)))

# Nežinoma šalis — EUR, ne USD: rinka yra Europa
for salis in ('XX', '', None, 'ZZ'):
    tikrink(valiutos.pagal_sali(salis) == 'EUR',
            'nežinomai šaliai %r turi būti EUR' % salis)

tikrink(valiutos.simbolis('EUR') == '€' and valiutos.simbolis('USD') == '$'
        and valiutos.simbolis('GBP') == '£' and valiutos.simbolis('PLN') == 'zł',
        'netinkami valiutų simboliai')
tikrink(valiutos.simbolis('XYZ') == '€', 'nežinomos valiutos simbolis ne €')
tikrink(len(valiutos.zemelapis()) == len(EURO) + len(KITOS),
        'žemėlapio dydis %d' % len(valiutos.zemelapis()))


# ═══════════════════════════════════════════════════════════════════
antraste('2. Skelbimas gauna valiutą pagal šalį')

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


for salis, zenklas in (('DE', '€'), ('HR', '€'), ('LT', '€'),
                       ('US', '$'), ('GB', '£'), ('PL', 'zł')):
    sk = skelbimas(salis)
    tikrink(sk.currency_symbol == zenklas,
            '%s: simbolis %s, tikėtasi %s' % (salis, sk.currency_symbol, zenklas))

# Net jei kas nors bandytų įrašyti kitą valiutą — šalis svarbesnė
klaidingas = skelbimas('DE', valiuta='USD')
tikrink(klaidingas.currency == 'EUR',
        'įrašytas USD vokiškam skelbimui liko: %s' % klaidingas.currency)

# Dalinis įrašymas (activate ir pan.) skelbimo nepagadina
klaidingas.status = 'draft'
klaidingas.save(update_fields=['status'])
klaidingas.refresh_from_db()
tikrink(klaidingas.currency == 'EUR', 'dalinis įrašymas sugadino valiutą')


# ═══════════════════════════════════════════════════════════════════
antraste('3. Ratlankiai/padangos — tas pats žemėlapis')

ratai = WheelListing(seller=u, product_type='tyre', country='PL', price=100,
                     city='Varšuva', title='T')
tikrink(ratai.currency_symbol == 'zł',
        'ratlankiams sava taisyklė: %s' % ratai.currency_symbol)
ratai.country = 'US'
tikrink(ratai.currency_symbol == '$', 'US ratlankiams ne $')


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
tikrink('data-valiutos-sufiksas' in js and 'id_country' in js,
        'valiuta.js neseka šalies lauko')
b = io.open(os.path.join(BASE, 'templates/base.html'), encoding='utf-8').read()
tikrink('valiutu_zemelapis_json' in b and 'valiuta.js' in b,
        'žemėlapis nepasiekia naršyklės')


# ═══════════════════════════════════════════════════════════════════
antraste('6. Pilnas ratas: vokiškas skelbimas gauna €')

c = Client()
c.force_login(u)
duom = {
    'truck_type': 'tractor', 'truck_brand': str(MARKE.pk),
    'truck_model_text': 'T460', 'year': '2018',
    'first_registration_month': '5', 'fuel_type': str(KURAS.pk),
    'defects': 'none', 'condition': 'used', 'price': '25000',
    'country': 'DE', 'city': 'Berlynas', 'phone': '+37060000000',
    'agree_terms': 'on', 'mileage': '500000', 'currency': 'USD',
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

# Kroatija — nuo 2023 euro zonoje (#754)
duom.update(country='HR', city='Zagrebas')
c.post('/create/trucks/', duom, follow=True)
kroatiskas = Listing.objects.filter(city='Zagrebas').order_by('-pk').first()
tikrink(kroatiskas is not None and kroatiskas.currency == 'EUR',
        'kroatiškas skelbimas gavo %s'
        % (kroatiskas.currency if kroatiskas else '—'))


# ═══════════════════════════════════════════════════════════════════
antraste('7. Migracija sutvarko jau esamus skelbimus')

migracijos = [f for f in os.listdir(os.path.join(BASE, 'apps/listings/migrations'))
              if 'valiuta' in f]
tikrink(migracijos, 'nėra migracijos esamiems skelbimams')

# Ta pati logika, kaip migracijoje
sugadintas = skelbimas('DE')
Listing.objects.filter(pk=sugadintas.pk).update(currency='USD')
for salis in Listing.objects.values_list('country', flat=True).distinct():
    Listing.objects.filter(country=salis).exclude(
        currency=valiutos.pagal_sali(salis)).update(
        currency=valiutos.pagal_sali(salis))
sugadintas.refresh_from_db()
tikrink(sugadintas.currency == 'EUR', 'migracija nepataisė vokiško skelbimo')


print('\n' + '═' * 60)
print('gerai: %d, nepavyko: %d' % (gerai, blogai))
sys.exit(1 if blogai else 0)
