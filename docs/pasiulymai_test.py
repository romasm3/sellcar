# -*- coding: utf-8 -*-
"""
„Pasiūlymai" skirtuko atranka — tikri modeliai, laikina sqlite DB atmintyje.
Produkcinės DB NELIEČIA.

Paleidimas:   python docs/pasiulymai_test.py

Ką tikrina: senoji logika (24 naujausi -> 18 kortelių) su 16 testinių
skelbimų palikdavo matomus tik 2 iš 5 senų — būtent dėl to „nesimatė
mano senų skelbimų". Naujoji parodo visus, bet pasibaigusių (expired)
vis tiek nerodo ir featured palieka viršuje.
"""
import os, sys, django
from datetime import timedelta
from django.conf import settings
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
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
from apps.listings.models import Listing, VehicleType
from apps.listings.views import _public_listings_qs, HOME_OFFERS_MAX


def _butini(model):
    """Užpildo visus NOT NULL laukus be numatytosios reikšmės — kad
    nereikėtų spėlioti, ko modelis reikalauja."""
    from django.db.models import NOT_PROVIDED
    out = {}
    for f in model._meta.concrete_fields:
        if f.primary_key or f.null or f.blank or f.has_default() or f.auto_created:
            continue
        if getattr(f, 'auto_now', False) or getattr(f, 'auto_now_add', False):
            continue
        it = f.get_internal_type()
        if it in ('IntegerField', 'BigIntegerField', 'PositiveIntegerField',
                  'SmallIntegerField', 'PositiveSmallIntegerField'):
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


_VT = None
def _skelbimas(**kw):
    global _VT
    if _VT is None:
        _VT = VehicleType.objects.create(name='Automobiliai', slug='cars')
    d = _butini(Listing)
    d['vehicle_type'] = _VT
    d.update(kw)
    return Listing.objects.create(**d)

U = get_user_model()
senas = U.objects.create(username='senas', email='senas@x.lt')
testas = U.objects.create(username='testai', email='testai@autoleft.local')

now = timezone.now()
# 5 SENI tikri skelbimai (prieš mėnesį)
for i in range(5):
    l = _skelbimas(seller=senas, title='Senas %d' % i, price=1000, year=2010,
                               status='active', description='')
    Listing.objects.filter(pk=l.pk).update(created_at=now - timedelta(days=30 + i))
# 16 TESTINIŲ (vakar) — tiek jų sukuria testiniai_skelbimai
for i in range(16):
    l = _skelbimas(seller=testas, title='TEST %d' % i, price=2000, year=2020,
                               status='active', description='TESTINIS SKELBIMAS')
    Listing.objects.filter(pk=l.pk).update(created_at=now - timedelta(days=1, minutes=i))
# 2 seni, kurie PASIBAIGĖ — jų neturi matytis niekaip
for i in range(2):
    _skelbimas(seller=senas, title='Pasibaiges %d' % i, price=1000, year=2009,
                           status='expired', description='')

base = _public_listings_qs(None)
tab_featured = []          # nei featured, nei žvaigždučių šiame teste

def senoji():
    ids = {l.pk for l in tab_featured}
    return tab_featured + [l for l in base.order_by('-created_at')[:24] if l.pk not in ids][:18 - len(tab_featured)]

def naujoji():
    ids = {l.pk for l in tab_featured}
    return tab_featured + list(base.exclude(pk__in=ids).order_by('-created_at')[:HOME_OFFERS_MAX])

bad = 0
def chk(name, got, want):
    global bad
    ok = got == want
    if not ok: bad += 1
    print(('  ok   ' if ok else '  FAIL ') + name + '  got=%r' % (got,) + ('' if ok else ' want=%r' % (want,)))

sen = senoji(); nauj = naujoji()
sen_seni = sum(1 for l in sen if l.title.startswith('Senas'))
nauj_seni = sum(1 for l in nauj if l.title.startswith('Senas'))

print('\n── PRIEŠ (sena logika: 24 naujausi -> 18 kortelių) ──')
chk('iš viso kortelių', len(sen), 18)
chk('senų skelbimų matosi', sen_seni, 2)          # 18 - 16 testinių = 2

print('\n── PO (visi vieši skelbimai) ──')
chk('iš viso kortelių', len(nauj), 21)            # 5 seni + 16 testinių
chk('VISI seni skelbimai matosi', nauj_seni, 5)
chk('pasibaigę NEmatomi', sum(1 for l in nauj if l.title.startswith('Pasibaiges')), 0)
chk('naujausi eina pirmi', nauj[0].title.startswith('TEST'), True)
chk('be dublikatų', len({l.pk for l in nauj}), len(nauj))

print('\n── featured nedubliuojasi ──')
tab_featured = list(base.order_by('created_at')[:2])   # imam du seniausius kaip „featured"
nauj2 = naujoji()
chk('featured viršuje', [l.pk for l in nauj2[:2]], [l.pk for l in tab_featured])
chk('be dublikatų', len({l.pk for l in nauj2}), len(nauj2))
chk('kiekis nepasikeitė', len(nauj2), 21)

print('\nklaidų:', bad)
sys.exit(1 if bad else 0)
