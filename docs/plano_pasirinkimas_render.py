# -*- coding: utf-8 -*-
"""
Atrenderina listing_select_plan.html tikru Django varikliu.

base.html pakeičiamas tuščiu karkasu, kad nereikėtų viso projekto
konteksto — mums rūpi tik pats plano puslapis ir jo inline JS.
Rezultatas: <tmp>/plan_rendered.html, kurį tikrina
docs/plano_pasirinkimas_test.js.

Paleidimas:  python docs/plano_pasirinkimas_render.py
"""
import os, sys, io, django
from django.conf import settings
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import tempfile
SP = tempfile.gettempdir()
os.makedirs(os.path.join(SP, 'stub'), exist_ok=True)
io.open(os.path.join(SP, 'stub', 'base.html'), 'w', encoding='utf-8').write(
    '<!doctype html><html><head><title>{% block title %}{% endblock %}</title></head>'
    '<body>{% block content %}{% endblock %}{% block extra_js %}{% endblock %}</body></html>')
settings.configure(
    DEBUG=True, USE_I18N=True, USE_L10N=True, USE_TZ=True, LANGUAGE_CODE='lt', SECRET_KEY='x',
    INSTALLED_APPS=['django.contrib.contenttypes', 'django.contrib.auth', 'apps.listings'],
    DATABASES={}, STATIC_URL='/static/',
    TEMPLATES=[{'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [os.path.join(SP, 'stub'), os.path.join(ROOT, 'templates')],
                'APP_DIRS': True, 'OPTIONS': {'context_processors': []}}],
)
django.setup()
from django.template.loader import render_to_string

class Obj(dict):
    __getattr__ = dict.get

plans = [
    dict(code='p130', label='130', days=130, price_usd='39.99', final_price_usd='39.99',
         has_multiplier=False, boost_days=35, boost_count=3, featured_days=1,
         highlight_days=14, is_recommended=True, pk=1),
    dict(code='p65', label='65', days=65, price_usd='35.99', final_price_usd='35.99',
         has_multiplier=False, boost_days=0, boost_count=0, featured_days=0,
         highlight_days=7, is_recommended=False, pk=2),
    dict(code='p40', label='40', days=40, price_usd='29.99', final_price_usd='29.99',
         has_multiplier=False, boost_days=0, boost_count=0, featured_days=0,
         highlight_days=0, is_recommended=False, pk=3),
]
ctx = {
    'listing': Obj(pk=7, title='Ac Aceca 2022 m Hečbekas', price=33333, year=2022,
                   mileage=3333, city='Kaunas', country='Lietuva', engine_capacity='13.0'),
    'main_image': None, 'plans': plans, 'wallet_balance': 0,
    'multiplier_enabled': False, 'multiplier_value': 1, 'multiplier_tier_label': '',
    'renew_count_options': [1, 2, 3], 'renew_days_options': [1, 2, 3],
    'featured_days_options': [1, 2, 3],
    'renew_price_per_unit': 1.0, 'featured_price_per_day': 3.0,
}
html = render_to_string('listings/listing_select_plan.html', ctx)
out = os.path.join(SP, 'plan_rendered.html')
io.open(out, 'w', encoding='utf-8').write(html)
print('atrenderinta:', out, '| simbolių:', len(html))
