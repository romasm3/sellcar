# -*- coding: utf-8 -*-
"""
Apmokėto plano pritaikymas ir nuolaidos kodas — tikri modeliai, laikina
sqlite DB atmintyje. Produkcinės DB NELIEČIA.

Paleidimas:  python docs/planas_nuolaida_test.py

Kodėl: nuolaidos kodas buvo skaičiuojamas tik naršyklėje — vartotojas
matydavo €0.00, o Stripe imdavo pilną kainą. Serveris jo neskaitė iš viso.
Be to, 100 % nuolaidos atveju Stripe sesijos sukurti neįmanoma, tad
skelbimas liktų neaktyvuotas.
"""
import os, sys, django
from datetime import timedelta
from decimal import Decimal
from django.conf import settings

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
settings.configure(
    DEBUG=True, USE_I18N=True, USE_TZ=True, LANGUAGE_CODE='lt', SECRET_KEY='x',
    INSTALLED_APPS=['django.contrib.contenttypes', 'django.contrib.auth',
                    'django.contrib.sites', 'apps.listings', 'apps.accounts'],
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}},
    DEFAULT_AUTO_FIELD='django.db.models.BigAutoField', AUTH_USER_MODEL='auth.User',
)
django.setup()
from django.core.management import call_command
call_command('migrate', run_syncdb=True, verbosity=0)

from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.listings.models import Listing, VehicleType, PromoCode, PromoCodeUsage
from apps.listings.listing_helpers import pritaikyti_apmoketa_plana

U = get_user_model()
pardavejas = U.objects.create(username='p', email='p@x.lt')
VT = VehicleType.objects.create(name='Automobiliai', slug='cars')


def _butini(model):
    out = {}
    for f in model._meta.concrete_fields:
        if (f.primary_key or f.null or f.blank or f.has_default() or f.auto_created
                or getattr(f, 'auto_now', False) or getattr(f, 'auto_now_add', False)):
            continue
        it = f.get_internal_type()
        if it.endswith('IntegerField'):
            out[f.name] = 0
        elif it in ('DecimalField', 'FloatField'):
            out[f.name] = 0
        elif it in ('CharField', 'TextField', 'SlugField', 'EmailField', 'URLField'):
            out[f.name] = ''
        elif it == 'BooleanField':
            out[f.name] = False
        elif it in ('DateTimeField', 'DateField'):
            out[f.name] = timezone.now()
    return out


def naujas_skelbimas(**kw):
    d = _butini(Listing)
    d.update(dict(seller=pardavejas, vehicle_type=VT, title='BMW M3',
                  price=5000, year=2018, status='draft'))
    d.update(kw)
    return Listing.objects.create(**d)


bad = 0
def chk(name, got, want):
    global bad
    ok = str(got) == str(want)
    if not ok:
        bad += 1
    print(('  ok   ' if ok else '  FAIL ') + name + '  got=%r' % (got,)
          + ('' if ok else ' want=%r' % (want,)))


print('\n── 1. Plano pritaikymas aktyvuoja ir uždeda paslaugas ──')
l = naujas_skelbimas()
rez = pritaikyti_apmoketa_plana(l, plan_days=90, plan_boost_days=10, plan_boost_count=3,
                                plan_featured_days=1, plan_highlight_days=14,
                                send_email=False)
l.refresh_from_db()
chk('grąžino True', rez, True)
chk('statusas', l.status, 'active')
chk('galioja ~90 d.', (l.expires_at - timezone.now()).days, 89)
chk('žvaigždučių', l.star_count, 3)
chk('žvaigždutės ~10 d.', (l.star_expires_at - timezone.now()).days, 9)
chk('reklama ~1 d.', (l.featured_until - timezone.now()).days, 0)
chk('paryškinimas ~14 d.', (l.highlight_until - timezone.now()).days, 13)

print('\n── 2. Antras kvietimas nieko nekartoja (webhook gali ateiti du kartus) ──')
zvaigzdes_pries = l.star_count
rez2 = pritaikyti_apmoketa_plana(l, plan_days=90, plan_boost_count=3, send_email=False)
l.refresh_from_db()
chk('grąžino False', rez2, False)
chk('žvaigždučių nepadaugėjo', l.star_count, zvaigzdes_pries)

print('\n── 3. Priedai sudedami su planu ──')
l3 = naujas_skelbimas()
pritaikyti_apmoketa_plana(l3, plan_days=30, plan_boost_count=1, plan_boost_days=5,
                          renew_count=2, renew_days=10, plan_featured_days=1,
                          addon_featured_days=3, send_email=False)
l3.refresh_from_db()
chk('žvaigždutės: planas 1 + priedas 2', l3.star_count, 3)
chk('trukmė — ilgesnioji (10, ne 5)', (l3.star_expires_at - timezone.now()).days, 9)
chk('reklama 1 + 3 = 4 d.', (l3.featured_until - timezone.now()).days, 3)

print('\n── 4. Nuolaidos skaičiavimas (kaip serveryje) ──')
proc100 = PromoCode.objects.create(code='BANDOM', discount_type='percent',
                                   discount_value=Decimal('100'), is_active=True)
proc20 = PromoCode.objects.create(code='DVIDESIMT', discount_type='percent',
                                  discount_value=Decimal('20'), is_active=True)
fiksuota = PromoCode.objects.create(code='PENKI', discount_type='fixed',
                                    discount_value=Decimal('5'), is_active=True)

def galutine(promo, plano_kaina, priedai):
    """Ta pati eiga kaip listing_pay_plan."""
    viso = Decimal(str(plano_kaina)) + Decimal(str(priedai))
    nuolaida = promo.calculate_discount(Decimal(str(plano_kaina)))
    if nuolaida > viso:
        nuolaida = viso
    return (viso - nuolaida).quantize(Decimal('0.01')), nuolaida

chk('-100 % nuo 20, be priedų', galutine(proc100, 20, 0)[0], Decimal('0.00'))
chk('-100 % nuo 20, priedai 3 -> lieka priedai', galutine(proc100, 20, 3)[0], Decimal('3.00'))
chk('-20 % nuo 20', galutine(proc20, 20, 0)[0], Decimal('16.00'))
chk('-20 % taikoma tik planui, ne priedams', galutine(proc20, 20, 10)[0], Decimal('26.00'))
chk('fiksuota -5 nuo 20', galutine(fiksuota, 20, 0)[0], Decimal('15.00'))
chk('fiksuota didesnė nei suma neneigiama', galutine(fiksuota, 3, 0)[0], Decimal('0.00'))

print('\n── 5. Negaliojantis kodas atmetamas ──')
neaktyvus = PromoCode.objects.create(code='SENAS', discount_type='percent',
                                     discount_value=Decimal('50'), is_active=False)
l5 = naujas_skelbimas()
chk('neaktyvus', neaktyvus.is_valid(user=pardavejas, listing=l5)[0], False)
pasibaiges = PromoCode.objects.create(code='BAIGESI', discount_type='percent',
                                      discount_value=Decimal('50'), is_active=True,
                                      valid_until=timezone.now() - timedelta(days=1))
chk('pasibaigęs', pasibaiges.is_valid(user=pardavejas, listing=l5)[0], False)
chk('galiojantis', proc20.is_valid(user=pardavejas, listing=l5)[0], True)

print('\n── 6. Kartotinio naudojimo riba ──')
vienkartinis = PromoCode.objects.create(code='VIENA', discount_type='percent',
                                        discount_value=Decimal('50'), is_active=True,
                                        once_per_user=True)
chk('pirmą kartą galima', vienkartinis.is_valid(user=pardavejas, listing=l5)[0], True)
PromoCodeUsage.objects.create(promo_code=vienkartinis, user=pardavejas,
                              listing=l5, discount_amount=Decimal('10'))
chk('antrą kartą nebe', vienkartinis.is_valid(user=pardavejas, listing=l5)[0], False)

print('\nklaidų:', bad)
sys.exit(1 if bad else 0)
