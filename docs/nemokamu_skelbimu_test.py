# -*- coding: utf-8 -*-
"""
VISŲ SKELBIMŲ ĮKĖLIMAS NEMOKAMAS, KOL `MOKEJIMAI_IJUNGTI = False`.

Vienas jungiklis, dvi padėtys, ir abi tikrinamos:

  False → skelbimas aktyvuojamas iš karto, planų puslapio nėra, piniginė
          ir mokami priedai paslėpti;
  True  → grįžta senas srautas: planų puslapis, nurašymas iš piniginės.

Mokėjimo kodas privalo LIKTI: payments programa, modeliai, migracijos,
Stripe servisas ir planų šablonas — patikra 5 dalyje.

Paleidimas:  python docs/nemokamu_skelbimu_test.py
"""
import os, sys, tempfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
for k, v in (('SECRET_KEY', 'x'), ('EMAIL_USER', 'x@x.lt'), ('EMAIL_PASSWORD', 'x')):
    os.environ.setdefault(k, v)

import django
from django.conf import settings

LAIKINA = tempfile.mkdtemp(prefix='nemokami-')
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
from django.test import Client, override_settings
from django.utils import timezone
from apps.listings.constants import can_create_free_listing, mokejimai_ijungti
from apps.listings.models import (Brand, FuelType, Listing, PricingPlan,
                                  PricingSettings, Transmission, VehicleType)

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
u.profile.language = 'lt'
u.profile.save(update_fields=['language'])

VT, _ = VehicleType.objects.get_or_create(slug='cars', defaults={'name': 'Automobiliai'})
MARKE, _ = Brand.objects.get_or_create(name='BMW', defaults={'slug': 'bmw'})
KURAS, _ = FuelType.objects.get_or_create(name='Diesel')
PAVAROS, _ = Transmission.objects.get_or_create(name='Manual')
PricingSettings.get_solo()
PricingPlan.objects.get_or_create(
    vehicle_type=VT, code='plan_30',
    defaults={'label': '30 dienų', 'duration_days': 30, 'price': 10, 'is_active': True})


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


def juodrastis(uzpildytas=True):
    """Juodraštis, kurį planų puslapis laiko paruoštu skelbti."""
    d = _butini(Listing)
    d.update(seller=u, vehicle_type=VT, title='BMW 320d', status='draft',
             country='LT', city='Vilnius')
    if uzpildytas:
        d.update(price=5000, year=2018, first_registration='2018-05-01',
                 fuel_type=KURAS, brand=MARKE, model=None, body_type='sedan',
                 transmission=PAVAROS, doors=4, mileage=120000)
    else:
        # be kainos ir be pirmosios registracijos — nepakankamai skelbti
        d.update(price=0, first_registration=None)
    return Listing.objects.create(**d)


def klientas():
    c = Client()
    c.force_login(u)
    return c


# ═══════════════════════════════════════════════════════════════════
antraste('1. Jungiklis: nustatymai ir pagalbinė')
tikrink(hasattr(pagrindas, 'MOKEJIMAI_IJUNGTI'),
        'settings.MOKEJIMAI_IJUNGTI nėra')
tikrink(pagrindas.MOKEJIMAI_IJUNGTI is False,
        'numatytoji reikšmė turi būti False (viskas nemokama)')
with override_settings(MOKEJIMAI_IJUNGTI=False):
    tikrink(mokejimai_ijungti() is False, 'False → mokejimai_ijungti() False')
with override_settings(MOKEJIMAI_IJUNGTI=True):
    tikrink(mokejimai_ijungti() is True, 'True → mokejimai_ijungti() True')
# Senas vardas rodo į tą patį jungiklį: Stripe raktas vienas neįjungia.
tikrink(pagrindas.PAYMENTS_ENABLED is False,
        'PAYMENTS_ENABLED turi būti False, kol jungiklis išjungtas')


# ═══════════════════════════════════════════════════════════════════
antraste('2. IŠJUNGTA: viskas nemokama, be planų puslapio')
with override_settings(MOKEJIMAI_IJUNGTI=False):
    # Visų kategorijų formos sprendžia per šią vieną funkciją.
    for n in (0, 3, 50):
        Listing.objects.filter(seller=u).delete()
        for i in range(n):
            d = _butini(Listing)
            d.update(seller=u, vehicle_type=VT, title='x%d' % i, price=1,
                     status='active', country='LT', city='Vilnius')
            Listing.objects.create(**d)
        is_free = can_create_free_listing(u)[0]
        tikrink(is_free, 'turint %d aktyvių įkėlimas privalo būti nemokamas' % n)
    Listing.objects.filter(seller=u).delete()

    # Planų puslapis → iškart aktyvus, jokio „apmokėti"
    l = juodrastis()
    r = klientas().get('/listings/%d/select-plan/' % l.pk)
    l.refresh_from_db()
    tikrink(r.status_code == 302, 'select-plan turi nukreipti, grąžino %s' % r.status_code)
    tikrink('/success' in r['Location'] or 'action=published' in r['Location'],
            'nukreipta ne į „pavyko": %s' % r.get('Location'))
    tikrink(l.status == 'active', 'skelbimas turi būti aktyvus, yra „%s"' % l.status)
    tikrink(l.expires_at is not None, 'neuždėtas galiojimas')

    # Skydelio „Aktyvuoti" nebeklausia mokėjimo
    l2 = juodrastis()
    l2.status = 'expired'
    l2.save(update_fields=['status'])
    r = klientas().post('/%d/activate/' % l2.pk)
    l2.refresh_from_db()
    tikrink(l2.status == 'active', 'neaktyvus → activate turi duoti active, yra „%s"' % l2.status)
    tikrink('select-plan' not in r.get('Location', ''),
            'activate vis dar veda į planų puslapį')

    # Nurašymo kelias irgi nemokamas, o ne 404/500
    l3 = juodrastis()
    r = klientas().post('/listings/%d/pay-plan/plan_30/' % l3.pk)
    l3.refresh_from_db()
    tikrink(r.status_code == 302, 'pay/plan grąžino %s' % r.status_code)
    tikrink(l3.status == 'active', 'pay/plan turi aktyvuoti nemokamai, yra „%s"' % l3.status)
    tikrink(u.profile.wallet_balance in (None, 0) or u.profile.wallet_balance >= 0,
            'piniginė nuėjo į minusą')

    # Pusiau tuščias juodraštis į svetainę NEPAKLIŪVA
    tuscias = juodrastis(uzpildytas=False)
    r = klientas().get('/listings/%d/select-plan/' % tuscias.pk)
    tuscias.refresh_from_db()
    tikrink(tuscias.status == 'draft',
            'neužpildytas juodraštis neturi būti paskelbtas, yra „%s"' % tuscias.status)

    # Mokami priedai ir piniginė — uždaryti
    for kelias in ('/%d/services/' % l.pk, '/accounts/wallet/'):
        r = klientas().get(kelias)
        tikrink(r.status_code == 302, '%s turi nukreipti, grąžino %s' % (kelias, r.status_code))
        tikrink('select-plan' not in r.get('Location', ''),
                '%s nukreipia į planų puslapį' % kelias)

    # Šablonų jungiklis ir paslėpti mygtukai
    r = klientas().get('/dashboard/announcements/')
    kunas = r.content.decode('utf-8')
    tikrink(r.status_code == 200, 'skelbimų skydelis grąžino %s' % r.status_code)
    tikrink('/services/' not in kunas, 'skydelis vis dar rodo mokamus priedus')
    r = klientas().get('/')
    kunas = r.content.decode('utf-8')
    tikrink('accounts/wallet' not in kunas, 'antraštėje vis dar piniginė')
    tikrink('become-dealer' not in kunas, 'antraštėje vis dar prekiautojo prenumerata')


# ═══════════════════════════════════════════════════════════════════
antraste('3. ĮJUNGTA: grįžta mokėjimo žingsnis')
with override_settings(MOKEJIMAI_IJUNGTI=True):
    Listing.objects.filter(seller=u).delete()
    tikrink(can_create_free_listing(u)[0] is True,
            'pirmi trys skelbimai vis dar nemokami')
    for i in range(3):
        d = _butini(Listing)
        d.update(seller=u, vehicle_type=VT, title='y%d' % i, price=1,
                 status='active', country='LT', city='Vilnius')
        Listing.objects.create(**d)
    tikrink(can_create_free_listing(u)[0] is False,
            'ketvirtas skelbimas turi būti mokamas')

    # Planų puslapis vėl rodomas, o ne apeinamas
    l = juodrastis()
    r = klientas().get('/listings/%d/select-plan/' % l.pk)
    l.refresh_from_db()
    tikrink(r.status_code == 200, 'select-plan turi rodyti planus, grąžino %s' % r.status_code)
    tikrink(l.status == 'draft', 'įjungus mokėjimus skelbimas neturi pats aktyvuotis')
    kunas = r.content.decode('utf-8')
    tikrink('30' in kunas, 'planų puslapyje nėra plano trukmės')

    # Skydelio „Aktyvuoti" vėl veda į planus
    l2 = juodrastis()
    l2.status = 'expired'
    l2.save(update_fields=['status'])
    r = klientas().post('/%d/activate/' % l2.pk)
    l2.refresh_from_db()
    tikrink('select-plan' in r.get('Location', ''),
            'activate turi vesti į planų puslapį, veda į %s' % r.get('Location'))
    tikrink(l2.status == 'expired', 'skelbimas aktyvavosi be apmokėjimo')

    # Piniginė ir prekiautojas vėl atsidaro
    r = klientas().get('/accounts/wallet/')
    tikrink(r.status_code == 200, 'piniginė turi atsidaryti, grąžino %s' % r.status_code)
    r = klientas().get('/')
    kunas = r.content.decode('utf-8')
    tikrink('accounts/wallet' in kunas, 'antraštėje nėra piniginės')
    tikrink('become-dealer' in kunas, 'antraštėje nėra prekiautojo')


# ═══════════════════════════════════════════════════════════════════
antraste('4. Įstrigusių skelbimų aktyvavimas')
with override_settings(MOKEJIMAI_IJUNGTI=False):
    Listing.objects.filter(seller=u).delete()
    uzpildyti = [juodrastis() for _ in range(3)]
    tusti = [juodrastis(uzpildytas=False) for _ in range(2)]

    call_command('aktyvuok_istrigusius', bandymas=True, verbosity=0)
    tikrink(all(Listing.objects.get(pk=l.pk).status == 'draft' for l in uzpildyti),
            '--bandymas neturi nieko keisti')

    call_command('aktyvuok_istrigusius', verbosity=0)
    tikrink(all(Listing.objects.get(pk=l.pk).status == 'active' for l in uzpildyti),
            'užpildyti juodraščiai turi būti aktyvuoti')
    tikrink(all(Listing.objects.get(pk=l.pk).status == 'draft' for l in tusti),
            'neužpildyti juodraščiai turi likti juodraščiais')
    tikrink(all(Listing.objects.get(pk=l.pk).expires_at for l in uzpildyti),
            'aktyvuotiems neuždėtas galiojimas')


# ═══════════════════════════════════════════════════════════════════
antraste('5. Mokėjimo kodas NEIŠTRINTAS')
for kelias in ('apps/payments/__init__.py', 'apps/payments/models.py',
               'apps/payments/views.py', 'apps/payments/urls.py',
               'apps/payments/stripe_service.py',
               'apps/payments/migrations/0001_initial.py',
               'templates/listings/listing_select_plan.html',
               'templates/accounts/wallet.html'):
    tikrink(os.path.exists(os.path.join(BASE, kelias)), 'ištrintas %s' % kelias)
tikrink('payments' in ' '.join(settings.INSTALLED_APPS),
        'payments programa iškrito iš INSTALLED_APPS')
from apps.payments.models import StripeCheckoutSession, StripeEvent   # noqa: F401
tikrink(True, 'payments modeliai importuojasi')

# Jungiklis dokumentuotas, o ne paslėptas kode
ns = open(os.path.join(BASE, 'config', 'settings.py'), encoding='utf-8').read()
tikrink('MOKEJIMAI_IJUNGTI' in ns and 'apeina' in ns.lower(),
        'settings.py neaiškina, ką jungiklis daro')

print('\n' + '═' * 60)
print('gerai: %d, nepavyko: %d' % (gerai, blogai))
sys.exit(1 if blogai else 0)
