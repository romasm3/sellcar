# -*- coding: utf-8 -*-
"""
ŠALIES JUOSTA virš greitosios paieškos panelės.

Tikrinam: angliškus (ir NEVERČIAMUS) pavadinimus, tikrus skaičius iš DB,
rikiavimą pagal kiekį, pasirinkimo grandinę (?salis= → slapukas →
numatytoji), filtravimą, ir kad panelės viduje niekas nepasikeitė.

Paleidimas:  python docs/salies_juosta_test.py
"""
import os, sys, django
from django.conf import settings

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
os.environ.setdefault('SECRET_KEY', 'x')
settings.configure(
    DEBUG=True, USE_I18N=True, USE_L10N=True, USE_TZ=True, LANGUAGE_CODE='lt',
    SECRET_KEY='x', ALLOWED_HOSTS=['*'], ROOT_URLCONF='config.urls',
    STRIPE_SECRET_KEY='sk_test_fake', LOCALE_PATHS=[os.path.join(BASE, 'locale')],
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
    CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}},
    TEMPLATES=[{'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [os.path.join(BASE, 'templates')], 'APP_DIRS': True,
                'OPTIONS': {'context_processors': [
                    'django.template.context_processors.request',
                    'django.contrib.messages.context_processors.messages',
                ]}}],
)
django.setup()
from django.core.management import call_command
call_command('migrate', run_syncdb=True, verbosity=0)

import re
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.template import Template, Context
from django.test import RequestFactory
from django.utils import timezone
from apps.listings import salys, salies_juosta as sj
from apps.listings.models import Listing, VehicleType

gerai = blogai = 0
def tikrink(s, k):
    global gerai, blogai
    if s: gerai += 1
    else:
        blogai += 1
        print('  NEPAVYKO: ' + k)
def antraste(t):
    print('\n── ' + t + ' ' + '─' * max(0, 56 - len(t)))

U = get_user_model()
u = U.objects.create_user(username='p', email='p@x.lt', password='x')
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

B = _butini(Listing)
KIEK = {'LT': 7, 'DE': 4, 'PL': 2, 'LV': 1}
for salis, n in KIEK.items():
    for i in range(n):
        d = dict(B); d.update(seller=u, vehicle_type=VT, title=f'{salis} {i}',
                              price=5000, year=2018, status='active',
                              country=salis, city='X')
        Listing.objects.create(**d)
# Juodraštis ir shadow-ban — į skaičiukus neturi patekti
d = dict(B); d.update(seller=u, vehicle_type=VT, title='juodrastis', price=1,
                      year=2018, status='draft', country='DE', city='X')
Listing.objects.create(**d)

rf = RequestFactory()
def uzklausa(kelias='/', **slapukai):
    r = rf.get(kelias)
    r.COOKIES.update(slapukai)
    return r


antraste('1. Angliški pavadinimai — neverčiami')
tikrink(salys.vardas_en('LT') == 'Lithuania', 'LT → Lithuania')
tikrink(salys.vardas_en('DE') == 'Germany', 'DE → Germany')
tikrink(salys.vardas_en('de') == 'Germany', 'mažosiomis irgi veikia')
tikrink(salys.vardas_en('XX') == 'XX', 'nežinomam — pats kodas')
tikrink(len(salys.VARDAI_EN) == len(salys.VARDAI),
        'angliškų vardų tiek pat, kiek šalių (%d vs %d)'
        % (len(salys.VARDAI_EN), len(salys.VARDAI)))
tikrink(set(salys.VARDAI_EN) == set(salys.VARDAI), 'kodai sutampa')
for kodas, vardas in salys.VARDAI_EN.items():
    tikrink(isinstance(vardas, str), '%s: paprasta eilutė, ne gettext' % kodas)
from django.utils import translation
with translation.override('lt'):
    lt_vardas = salys.vardas_en('DE')
with translation.override('en'):
    en_vardas = salys.vardas_en('DE')
tikrink(lt_vardas == en_vardas == 'Germany',
        'pavadinimas nekinta pagal sąsajos kalbą (lt=%r, en=%r)' % (lt_vardas, en_vardas))


antraste('2. Skaičiai — tikri, iš DB')
cache.clear()
k = sj.kiekiai()
tikrink(k == KIEK, 'kiekiai %s (laukta %s)' % (k, KIEK))
tikrink(k.get('DE') == 4, 'juodraštis į skaičiukus nepateko')


antraste('3. Sąrašas')
cache.clear()
eil = sj.sarasas('LT', request=uzklausa('/'))
tikrink([e['kodas'] for e in eil] == ['LT', 'DE', 'PL', 'LV'],
        'rikiuota pagal kiekį, ne abėcėlę: %s' % [e['kodas'] for e in eil])
tikrink(all(e['kiek'] > 0 for e in eil), 'šalys be skelbimų nerodomos')
tikrink(len(eil) == 4, 'sąraše tik tos, kurios turi skelbimų (%d)' % len(eil))
tikrink(eil[0]['dabartine'] and not any(e['dabartine'] for e in eil[1:]),
        'pažymėta tik dabartinė')
tikrink(eil[1]['vardas'] == 'Germany', 'vardas angliškas sąraše')
# pasirinkta be skelbimų — vis tiek rodoma
eil2 = sj.sarasas('JP', request=uzklausa('/'))
tikrink(any(e['kodas'] == 'JP' and e['dabartine'] for e in eil2),
        'pasirinkta šalis rodoma net be skelbimų')


antraste('4. Pasirinkimo grandinė: ?salis= → slapukas → numatytoji')
tikrink(sj.pasirinkta(uzklausa('/')) == 'LT', 'be nieko — numatytoji LT')
tikrink(sj.pasirinkta(uzklausa('/?salis=de')) == 'DE', '?salis=de → DE')
tikrink(sj.pasirinkta(uzklausa('/?salis=DE')) == 'DE', 'didžiosiomis irgi')
tikrink(sj.pasirinkta(uzklausa('/', salis='PL')) == 'PL', 'slapukas → PL')
tikrink(sj.pasirinkta(uzklausa('/?salis=de', salis='PL')) == 'DE',
        'adresas nugali slapuką')
tikrink(sj.pasirinkta(uzklausa('/?salis=xx')) == 'LT', 'nežinomas kodas → numatytoji')
tikrink(sj.pasirinkta(uzklausa('/', salis='zz')) == 'LT', 'šiukšlė slapuke → numatytoji')
tikrink(not sj.aiskiai_pasirinkta(uzklausa('/')), 'be nieko — nepasirinkta')
tikrink(sj.aiskiai_pasirinkta(uzklausa('/?salis=de')), 'adresu — pasirinkta')
tikrink(sj.aiskiai_pasirinkta(uzklausa('/', salis='DE')), 'slapuku — pasirinkta')


antraste('5. Filtravimas')
cache.clear()
visi = Listing.objects.filter(status='active')
tikrink(sj.filtruoti(visi, uzklausa('/?salis=de')).count() == 4, 'DE → 4')
tikrink(sj.filtruoti(visi, uzklausa('/?salis=pl')).count() == 2, 'PL → 2')
tikrink(sj.filtruoti(visi, uzklausa('/')).count() == 7, 'be pasirinkimo → LT 7')
tikrink(sj.filtruoti(visi, uzklausa('/', salis='LV')).count() == 1, 'slapukas LV → 1')
# Numatytoji netuština sąrašo, jei tokių skelbimų nėra
Listing.objects.filter(country='LT').update(country='US')
cache.clear()
tikrink(sj.filtruoti(visi, uzklausa('/')).count() == visi.count(),
        'jei numatytoje šalyje skelbimų nėra — filtras netaikomas')
tikrink(sj.filtruoti(visi, uzklausa('/?salis=lt')).count() == 0,
        'aiškiai pasirinkta tuščia šalis — filtruojama vis tiek')
Listing.objects.filter(country='US').update(country='LT')
cache.clear()


antraste('6. Slapukas')
from django.http import HttpResponse
atsakymas = sj.atsiminti(HttpResponse(), uzklausa('/?salis=de'))
tikrink(atsakymas.cookies.get('salis') and atsakymas.cookies['salis'].value == 'DE',
        'įrašomas slapukas DE')
tikrink(atsakymas.cookies['salis']['max-age'] == sj.SLAPUKO_AMZIUS, 'galioja metus')
tuscias = sj.atsiminti(HttpResponse(), uzklausa('/'))
tikrink('salis' not in tuscias.cookies, 'be ?salis= slapukas nerašomas')


antraste('7. Nuorodos neša esamus filtrus')
eil = sj.sarasas('LT', request=uzklausa('/?section=cars&price_min=5000&page=3'))
de = next(e for e in eil if e['kodas'] == 'DE')
tikrink('section=cars' in de['url'] and 'price_min=5000' in de['url'],
        'filtrai lieka: %s' % de['url'])
tikrink('salis=de' in de['url'], 'nurodoma nauja šalis')
tikrink('page=' not in de['url'], 'puslapiavimas numetamas: %s' % de['url'])


antraste('8. Šablonas')
cache.clear()
r = uzklausa('/')
html = Template("{% include 'listings/partials/_salies_juosta.html' %}").render(
    Context({'request': r, **sj.kontekstas(r)}))
tikrink('Lithuania' in html, 'rodoma dabartinė šalis angliškai')
tikrink('salies-juosta' in html and 'salies-eilute' in html, 'yra juostos struktūra')
tikrink(html.count('salies-punktas') >= 4, 'sąraše visos 4 šalys')
tikrink('Germany' in html and 'Poland' in html, 'kitos šalys angliškai')
tikrink('Lietuva' not in html and 'Vokietija' not in html,
        'lietuviškų pavadinimų juostoje nėra')
tikrink('salies-varnele' in html, 'dabartinė su varnele')
tikrink('escape.window' in html, 'Escape uždaro')
tikrink('salies-uzdanga' in html, 'paspaudus šalia uždaro')
tikrink('Ieškoti šalies' in html, 'yra paieškos laukelis')


antraste('9. Panelės vidus nepaliestas')
import subprocess
pakeisti = subprocess.run(['git', 'diff', '--name-only', 'origin/master', '--'],
                          capture_output=True, text=True, cwd=BASE).stdout.split()
PANELES = ('templates/listings/partials/search_panel.html',
           'templates/listings/partials/_panel_bodies.html',
           'templates/listings/partials/panel_generic.html',
           'templates/listings/partials/_sp_field_styles.html',
           'templates/listings/partials/search_rail.html')
for failas in PANELES:
    tikrink(failas not in pakeisti, 'nepaliestas %s' % failas)
# listing_list.html — tik pridėta
diff = subprocess.run(['git', 'diff', '--numstat', 'origin/master', '--',
                       'templates/listings/listing_list.html'],
                      capture_output=True, text=True, cwd=BASE).stdout.strip()
if diff:
    prideta, pasalinta = diff.split()[0], diff.split()[1]
    tikrink(pasalinta == '0',
            'listing_list.html tik papildytas (+%s / -%s)' % (prideta, pasalinta))


print('\n' + '═' * 60)
print('gerai: %d, nepavyko: %d' % (gerai, blogai))
sys.exit(1 if blogai else 0)
