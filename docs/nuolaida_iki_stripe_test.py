# -*- coding: utf-8 -*-
"""
Nuolaidos kodas iki pat Stripe — tikras listing_pay_plan view'as, tikri
modeliai, laikina sqlite DB atmintyje. Produkcinės DB NELIEČIA ir į Stripe
nieko nesiunčia: Session.create perimamas ir tik pasižiūrima, kokią sumą
view'as būtų padavęs.

Paleidimas:  python docs/nuolaida_iki_stripe_test.py

Kodėl: nuolaida buvo skaičiuojama tik naršyklėje. Vartotojas matydavo
sumažintą sumą, o Stripe gaudavo pilną kainą.
"""
import os, sys, django
from decimal import Decimal
from django.conf import settings
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('SECRET_KEY', 'x')
settings.configure(
    DEBUG=True, USE_I18N=True, USE_L10N=True, USE_TZ=True, LANGUAGE_CODE='lt',
    SECRET_KEY='x', ALLOWED_HOSTS=['*'], ROOT_URLCONF='config.urls',
    STRIPE_SECRET_KEY='sk_test_fake',
    INSTALLED_APPS=[
        "django.contrib.admin", "django.contrib.auth", "django.contrib.contenttypes",
        "django.contrib.sessions", "django.contrib.messages", "django.contrib.staticfiles",
        "django.contrib.humanize", "django.contrib.sitemaps",
        "apps.accounts", "apps.listings", "apps.conversations", "apps.broadcasts",
        "apps.payments", "apps.analytics",
        "crispy_forms", "crispy_bootstrap4", "django_filters", "rosetta",
    ],
    MIDDLEWARE=[
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
    ],
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}},
    DEFAULT_AUTO_FIELD='django.db.models.BigAutoField',
    STATIC_URL='/static/', MEDIA_URL='/media/', MEDIA_ROOT='/tmp/m',
    TEMPLATES=[{'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates')], 'APP_DIRS': True,
                'OPTIONS': {'context_processors': [
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ]}}],
)
django.setup()
from django.core.management import call_command
call_command('migrate', run_syncdb=True, verbosity=0)
print('DB paruošta')

from django.contrib.auth import get_user_model
from django.test import RequestFactory
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.utils import timezone
from apps.listings.models import (Listing, VehicleType, PromoCode, PricingPlan,
                                  PricingSettings)
from apps.listings import views as lviews

U = get_user_model()
user = U.objects.create_user(username='p', email='p@x.lt', password='x')
VT = VehicleType.objects.create(name='Automobiliai', slug='cars')

def _butini(model):
    out = {}
    for f in model._meta.concrete_fields:
        if (f.primary_key or f.null or f.blank or f.has_default() or f.auto_created
                or getattr(f, 'auto_now', False) or getattr(f, 'auto_now_add', False)):
            continue
        it = f.get_internal_type()
        if it.endswith('IntegerField'): out[f.name] = 0
        elif it in ('DecimalField', 'FloatField'): out[f.name] = 0
        elif it in ('CharField','TextField','SlugField','EmailField','URLField'): out[f.name] = ''
        elif it == 'BooleanField': out[f.name] = False
        elif it in ('DateTimeField', 'DateField'): out[f.name] = timezone.now()
    return out

d = _butini(Listing); d.update(dict(seller=user, vehicle_type=VT, title='BMW M3',
                                     price=5000, year=2018, status='draft'))
listing = Listing.objects.create(**d)

pd = _butini(PricingPlan)
pd.update(dict(vehicle_type=VT, code='premium_90', label='Recommended plan',
               duration_days=90, price=Decimal('20.00'), boost_days=10, boost_count=3,
               featured_days=1, highlight_days=14, is_active=True, is_recommended=True))
PricingPlan.objects.create(**pd)
PricingSettings.get_solo()

PromoCode.objects.create(code='MOOD', discount_type='percent',
                         discount_value=Decimal('20'), is_active=True)

# ── Perimam Stripe: nieko nesiunčiam, tik pasižiūrim kokią sumą paduoda ──
gauta = {}
import stripe
class FakeSession:
    @staticmethod
    def create(**kw):
        gauta.update(kw)
        return type('S', (), {'url': '/fake-stripe/'})()
stripe.checkout.Session = FakeSession

rf = RequestFactory()

def paleisk(post):
    req = rf.post('/x/', post)
    req.user = user
    SessionMiddleware(lambda r: None).process_request(req)
    req.session.save()
    req._messages = FallbackStorage(req)
    gauta.clear()
    resp = lviews.listing_pay_plan(req, listing.pk, 'premium_90')
    suma = gauta.get('line_items', [{}])[0].get('price_data', {}).get('unit_amount')
    return resp, suma, gauta.get('metadata', {})

bad = 0
def chk(n, got, want):
    global bad
    ok = str(got) == str(want)
    if not ok: bad += 1
    print(('  ok   ' if ok else '  FAIL ') + n + '  got=%r' % (got,) + ('' if ok else ' want=%r' % (want,)))

print('\n── Be nuolaidos ──')
_, suma, _md = paleisk({'renew_count': '0', 'renew_days': '0', 'featured_days': '0'})
chk('Stripe suma centais', suma, 2000)

print('\n── Su MOOD (-20 %) ──')
_, suma, md = paleisk({'renew_count': '0', 'renew_days': '0', 'featured_days': '0',
                       'applied_promo_code': 'MOOD'})
chk('Stripe suma centais', suma, 1600)
chk('metadata promo_code', md.get('promo_code'), 'MOOD')
chk('metadata promo_discount', md.get('promo_discount'), '4.00')

print('\n── MOOD + priedai (nuolaida tik planui) ──')
_, suma, md = paleisk({'renew_count': '2', 'renew_days': '3', 'featured_days': '0',
                       'applied_promo_code': 'MOOD'})
ps = PricingSettings.get_solo()
laukiama = int((Decimal('20') + Decimal('2') * 3 * ps.addon_renew_price - Decimal('4')) * 100)
chk('Stripe suma centais', suma, laukiama)

print('\n── Kodas mažosiomis raidėmis ──')
_, suma, _md = paleisk({'renew_count': '0', 'renew_days': '0', 'featured_days': '0',
                        'applied_promo_code': 'mood'})
chk('Stripe suma centais', suma, 1600)

print('\n── Melagingas applied_discount_amount ignoruojamas ──')
_, suma, _md = paleisk({'renew_count': '0', 'renew_days': '0', 'featured_days': '0',
                        'applied_promo_code': 'MOOD', 'applied_discount_amount': '20.00'})
chk('vis tiek 16.00, ne 0', suma, 1600)

print('\nklaidų:', bad)
sys.exit(1 if bad else 0)
