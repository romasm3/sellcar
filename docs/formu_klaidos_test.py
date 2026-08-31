# -*- coding: utf-8 -*-
"""
Vieningas privalomų laukų žymėjimas — serverio pusė.

Tikrinam: klaidos tekstas → laukas → lietuviškas pranešimas; kad visos
28 /create/ formos turi data-validate ir bendrą klaidų partial'ą; kad
dėžutėje kiekviena klaida yra nuoroda <a href="#id_laukas">; kad JSON
blokas, kurį skaito static/js/form_validation.js, turi tuos pačius
laukus.

Paleidimas:  python docs/formu_klaidos_test.py
"""
import os, sys, glob, json, re, django
from django.conf import settings

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
os.environ.setdefault('SECRET_KEY', 'x')
settings.configure(
    DEBUG=True, USE_I18N=True, USE_L10N=True, USE_TZ=True, LANGUAGE_CODE='lt',
    SECRET_KEY='x', ALLOWED_HOSTS=['*'], ROOT_URLCONF='config.urls',
    STRIPE_SECRET_KEY='sk_test_fake',
    LOCALE_PATHS=[os.path.join(BASE, 'locale')],
    INSTALLED_APPS=[
        "django.contrib.admin", "django.contrib.auth", "django.contrib.contenttypes",
        "django.contrib.sessions", "django.contrib.messages", "django.contrib.staticfiles",
        "django.contrib.humanize", "django.contrib.sitemaps",
        "apps.accounts", "apps.listings", "apps.conversations", "apps.broadcasts",
        "apps.payments", "apps.analytics", "apps.imones",
        "crispy_forms", "crispy_bootstrap4", "django_filters", "rosetta",
    ],
    MIDDLEWARE=[],
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}},
    DEFAULT_AUTO_FIELD='django.db.models.BigAutoField',
    STATIC_URL='/static/', MEDIA_URL='/media/', MEDIA_ROOT='/tmp/m',
    TEMPLATES=[{'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [os.path.join(BASE, 'templates')], 'APP_DIRS': True,
                'OPTIONS': {'context_processors': [
                    'django.template.context_processors.request',
                    'django.contrib.messages.context_processors.messages',
                ]}}],
)
django.setup()

from django.template import Template, Context
from django.test import RequestFactory
from apps.listings import formos_klaidos as fk

gerai = blogai = 0
def tikrink(salyga, ka):
    global gerai, blogai
    if salyga: gerai += 1
    else:
        blogai += 1
        print('  NEPAVYKO: ' + ka)

def antraste(t):
    print('\n── ' + t + ' ' + '─' * max(0, 58 - len(t)))


antraste('1. Tekstas → laukas')
for tekstas, laukas in [
    ('You must agree to the terms', 'agree_terms'),
    ('You must agree to terms and conditions.', 'agree_terms'),
    ('Turite sutikti su taisyklėmis', 'agree_terms'),
    ('agree_terms: Turite sutikti su taisyklėmis', 'agree_terms'),
    ('Phone is required', 'phone'),
    ('Telefonas yra privalomas', 'phone'),
    ('phone: Telefonas yra privalomas', 'phone'),
    ('State is required for US listings', 'state'),
    ('Brand is required', 'brand'),
    ('Markė yra privaloma', 'brand'),
    ('Price is required.', 'price'),
    ('Valid price is required.', 'price'),
    ('Kaina yra privaloma', 'price'),
    ('Kėbulo tipas yra privalomas', 'body_type'),
    ('Nežinoma klaida iš niekur', None),
]:
    tikrink(fk.laukas_pagal_teksta(tekstas) == laukas,
            '%r → %r (gauta %r)' % (tekstas, laukas, fk.laukas_pagal_teksta(tekstas)))


antraste('2. kontekstas() — sąrašas, poros, žodynas')
k = fk.kontekstas(['Phone is required', 'You must agree to the terms'])
tikrink(k['error_fields'] == ['phone', 'agree_terms'], 'laukai iš angliškų tekstų: %s' % k['error_fields'])
tikrink(k['error_messages']['agree_terms'] == 'Turite sutikti su taisyklėmis',
        'sutikimo tekstas lietuviškai: %r' % k['error_messages']['agree_terms'])
tikrink(k['error_messages']['phone'] == 'Telefonas yra privalomas',
        'telefono tekstas lietuviškai: %r' % k['error_messages']['phone'])

k = fk.kontekstas([('phone', 'nesvarbu'), ('city', 'nesvarbu')])
tikrink(k['error_fields'] == ['phone', 'city'], 'poros: %s' % k['error_fields'])

k = fk.kontekstas({'truck_brand': 'x', 'condition': 'y'})
tikrink(set(k['error_fields']) == {'truck_brand', 'condition'}, 'žodynas: %s' % k['error_fields'])

k = fk.kontekstas(['Phone is required', 'Telefonas yra privalomas'])
tikrink(k['error_fields'] == ['phone'], 'tas pats laukas du kartus — viena eilutė')

k = fk.kontekstas(['Nežinoma klaida'])
tikrink(k['error_fields'] == [] and k['form_errors'][0]['tekstas'] == 'Nežinoma klaida',
        'nežinoma klaida lieka dėžutėje be lauko')

tikrink(fk.kontekstas([])['form_errors'] == [], 'tuščias sąrašas — tuščia')
tikrink(fk.kontekstas(None)['form_errors'] == [], 'None — tuščia')


antraste('3. Partial: dėžutė su nuorodomis + JSON')
rf = RequestFactory()
SAB = Template("{% include 'listings/partials/_form_errors.html' %}")
html = SAB.render(Context({
    'request': rf.get('/create/'),
    **fk.kontekstas(['Phone is required', 'You must agree to the terms']),
}))
tikrink('<a href="#id_phone">Telefonas yra privalomas</a>' in html,
        'telefono klaida — nuoroda į lauką')
tikrink('<a href="#id_agree_terms">Turite sutikti su taisyklėmis</a>' in html,
        'sutikimo klaida — nuoroda į lauką')
blokas = re.search(r'id="serverio-klaidos">(.*?)</script>', html, re.S)
tikrink(blokas is not None, 'yra JSON blokas skriptui')
if blokas:
    d = json.loads(blokas.group(1))
    tikrink(d['laukai'] == ['phone', 'agree_terms'], 'JSON laukai: %s' % d['laukai'])
    tikrink(d['zinutes']['phone'] == 'Telefonas yra privalomas', 'JSON žinutė')
    tikrink(d['tekstai']['taisykles'] == 'Turite sutikti su taisyklėmis', 'JSON tekstai')

# be klaidų — dėžutės nėra, bet JSON blokas yra (skriptui reikia tekstų)
tuscia = SAB.render(Context({'request': rf.get('/create/')}))
tikrink('form-error-box' not in tuscia, 'be klaidų dėžutės nėra')
tikrink('serverio-klaidos' in tuscia, 'be klaidų JSON blokas vis tiek yra')


antraste('4. Atsarginis kelias — klaidos iš messages')
class FakeMsg:
    def __init__(self, t): self.t = t
    def __str__(self): return self.t
html = SAB.render(Context({
    'request': rf.get('/create/'),
    'messages': [FakeMsg('Phone is required'), FakeMsg('City is required')],
}))
tikrink('<a href="#id_phone">' in html and '<a href="#id_city">' in html,
        'view be error_fields — klaidos atpažįstamos iš messages')


antraste('5. Visos /create/ formos prijungtos')
sablonai = sorted(glob.glob(os.path.join(BASE, 'templates/listings/*create*.html')))
tikrink(len(sablonai) >= 28, 'rasta %d create šablonų' % len(sablonai))
for kelias in sablonai:
    vardas = os.path.basename(kelias)
    t = open(kelias, encoding='utf-8').read()
    tikrink('data-validate' in t, '%s: forma turi data-validate' % vardas)
    tikrink("_form_errors.html" in t, '%s: įtrauktas bendras klaidų partial\'as' % vardas)
    tikrink('{% if messages %}' not in t,
            '%s: senas messages blokas pašalintas (kitaip klaidos dubliuotųsi)' % vardas)


antraste('6. CSS ir JS įjungti visur (base.html)')
baze = open(os.path.join(BASE, 'templates/base.html'), encoding='utf-8').read()
tikrink("css/form_validation.css" in baze, 'base.html įtraukia CSS')
tikrink("js/form_validation.js" in baze, 'base.html įtraukia JS')
css = open(os.path.join(BASE, 'static/css/form_validation.css'), encoding='utf-8').read()
for reiksme in ('#dc2626', '#fef2f2', 'scroll-margin-top: 90px',
                '.field-invalid', '.label-invalid', '.field-error-msg'):
    tikrink(reiksme in css, 'CSS turi %s' % reiksme)
tikrink('font-size: 13px' in css, 'CSS žinutė 13px')
tikrink('border: 2px solid #dc2626' in css, 'CSS rėmelis 2px')


antraste('7. View\'uose nebeliko angliškų validacijos tekstų')
ANGLIŠKI = re.compile(
    r"errors(?:\.append\(|\[['\"][a-z_]+['\"]\]\s*=\s*)\s*f?['\"]"
    r"(?:[A-Z][a-z]+ (?:is|not|must) |You must|Save failed)")
for kelias in sorted(glob.glob(os.path.join(BASE, 'apps/listings/*_views.py'))) + \
              [os.path.join(BASE, 'apps/listings/views.py'),
               os.path.join(BASE, 'apps/listings/listing_helpers.py')]:
    t = open(kelias, encoding='utf-8').read()
    rasta = ANGLIŠKI.findall(t)
    tikrink(not rasta, '%s: %d angliškų validacijos tekstų' %
            (os.path.basename(kelias), len(rasta)))

# ir visi jie susieti su laukais
from apps.listings.listing_helpers import validate_common_fields
bendri = validate_common_fields(
    {'condition': '', 'year': None, 'price': 0, 'phone': '', 'city': '',
     'country': 'US', 'state': '', 'agree_terms': False}, require_terms=True)
k = fk.kontekstas(bendri)
tikrink(set(k['error_fields']) == {'agree_terms', 'condition', 'year', 'price', 'phone', 'city', 'state'},
        'validate_common_fields klaidos visos susietos su laukais: %s' % k['error_fields'])
tikrink(len(k['form_errors']) == len(k['error_fields']),
        'nė viena bendra klaida nelieka be lauko')


antraste('8. error_fields šablone (kontekstinis procesorius)')
from django.contrib.messages.storage.base import Message
from django.contrib.messages import constants
from apps.listings.context_processors import form_error_fields

class FakeStorage(list):
    pass

req = rf.post('/create/cars/')
req._messages = FakeStorage([Message(constants.ERROR, 'Phone is required'),
                             Message(constants.ERROR, 'You must agree to the terms')])
ctx = form_error_fields(req)
tikrink(list(ctx['error_fields']) == ['phone', 'agree_terms'],
        'procesorius atpažįsta laukus: %s' % list(ctx['error_fields']))
tikrink(dict(ctx['error_messages'])['phone'] == 'Telefonas yra privalomas',
        'procesorius paduoda lietuvišką tekstą')

SAB2 = Template("{% if 'agree_terms' in error_fields %}field-invalid{% endif %}")
tikrink(SAB2.render(Context(ctx)).strip() == 'field-invalid',
        "šablone veikia {% if 'agree_terms' in error_fields %}")
SAB3 = Template("{% if 'brand' in error_fields %}field-invalid{% endif %}")
tikrink(SAB3.render(Context(ctx)).strip() == '',
        'nepaminėtas laukas nepažymimas')

# Tingumas: kol šablonas neprašo, messages neliečiamos (kitaip dingtų
# sėkmės pranešimai puslapiuose, kurie klaidų visai nerodo)
req2 = rf.get('/')
req2._messages = FakeStorage([Message(constants.SUCCESS, 'Skelbimas paskelbtas')])
ctx2 = form_error_fields(req2)
tikrink(Template('{{ 1 }}').render(Context(ctx2)) == '1',
        'šablonas be error_fields atsivaizduoja')
tikrink(list(ctx2['error_fields']) == [],
        'sėkmės pranešimas nevirsta klaida')

# View'as, padavęs savo laukus, laimi prieš messages
html = SAB.render(Context({
    'request': rf.get('/create/'),
    'messages': [FakeMsg('Phone is required')],
    **fk.kontekstas([('brand', '')]),
}))
tikrink('#id_brand' in html and '#id_phone' not in html,
        'view\'o paduoti error_fields turi pirmenybę prieš messages')


print('\n' + '═' * 62)
print('gerai: %d, nepavyko: %d' % (gerai, blogai))
sys.exit(1 if blogai else 0)
