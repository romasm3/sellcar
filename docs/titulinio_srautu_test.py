# -*- coding: utf-8 -*-
"""Titulinio skelbimų srautai — padangos, „Pasiūlymai", „Dienos pasiūlymai".

Tikrina tai, ką rodė gyva klaida 2026-09-22: padangos ir ratlankiai
(WheelListing, /wheels/<id>/) nepatekdavo nei į skaitliukus, nei į
skirtukus, „Pasiūlymai" buvo vien automobiliai, o „Dienos pasiūlymai"
reiškė „šiandien įkelta" ir tyliomis dienomis likdavo tušti.

Paleidimas:  python docs/titulinio_srautu_test.py
"""
import io, os, sys, django
from decimal import Decimal
from django.conf import settings

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
settings.configure(
    DEBUG=True, USE_I18N=True, USE_TZ=True, LANGUAGE_CODE='lt', SECRET_KEY='x',
    ALLOWED_HOSTS=['*'], ROOT_URLCONF='config.urls', STRIPE_SECRET_KEY='sk_test_x',
    LOCALE_PATHS=[os.path.join(BASE, 'locale')],
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}},
    DEFAULT_AUTO_FIELD='django.db.models.AutoField',
    CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}},
    INSTALLED_APPS=['django.contrib.admin', 'django.contrib.auth',
                    'django.contrib.contenttypes', 'django.contrib.sessions',
                    'django.contrib.messages', 'django.contrib.staticfiles',
                    'django.contrib.humanize', 'django.contrib.sitemaps',
                    'apps.accounts', 'apps.listings', 'apps.imones',
                    'apps.conversations', 'apps.broadcasts', 'apps.payments',
                    'apps.analytics', 'crispy_forms', 'crispy_bootstrap4',
                    'django_filters', 'rosetta'],
    STATIC_URL='/static/', STATIC_ROOT=os.path.join(BASE, 'staticfiles'),
    TEMPLATES=[{'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [os.path.join(BASE, 'templates')], 'APP_DIRS': True,
                'OPTIONS': {'context_processors': [
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages']}}],
)
django.setup()

from django.core.management import call_command
from django.contrib.auth.models import User
from apps.listings.models import Listing, VehicleType, WheelListing
from apps.listings import titulinis

call_command('migrate', run_syncdb=True, verbosity=0)

KLAIDOS = []


def tikrinu(pav, salyga, papild=''):
    if salyga:
        print(u'  ✓ %s' % pav)
    else:
        print(u'  ✗ %s   %s' % (pav, papild))
        KLAIDOS.append(pav)


# ── Duomenys ────────────────────────────────────────────────────────
u = User.objects.create_user('t', 't@x.lt', 'x')
TIPAI = {}
for slug, vardas in (('cars', 'Automobiliai'), ('motorcycles', 'Motociklai'),
                     ('trucks', 'Sunkvežimiai'), ('trailers', 'Priekabos'),
                     ('agriculture', 'Žemės ūkio technika')):
    TIPAI[slug] = VehicleType.objects.create(slug=slug, name=vardas)


def skelbimas(slug, kaina, metai=2021, miestas='Vilnius'):
    return Listing.objects.create(
        title='%s %s' % (slug, kaina), seller=u, vehicle_type=TIPAI[slug],
        price=Decimal(kaina), year=metai, mileage=10000, city=miestas,
        country='LT', description='x', status='active')


def ratas(tipas, kaina):
    return WheelListing.objects.create(
        seller=u, product_type=tipas, title='%s %s' % (tipas, kaina),
        price=Decimal(kaina), country='LT', city='Kaunas', status='active')


# Automobiliai — dauguma, kaip gyvai. Kainos taip, kad mediana būtų aiški.
for k in (5000, 7000, 9000, 11000, 13000, 15000, 17000, 19000):
    skelbimas('cars', k)
for k in (3000, 4000):
    skelbimas('motorcycles', k)
skelbimas('trucks', 30000)
skelbimas('trailers', 8000)
skelbimas('agriculture', 50000)
# Padangos (10) ir ratlankiai (2) — kaip gyvai
for k in (100, 120, 140, 160, 180, 200, 220, 240, 260, 280):
    ratas('tyre', k)
for k in (300, 400):
    ratas('rim', k)

VISI = Listing.objects.filter(status='active')


class FakeSesija(object):
    session_key = 'abc123'


class FakeRequest(object):
    """salies_juosta.filtruoti tikrina tik GET, COOKIES ir user."""
    def __init__(self):
        from django.http import QueryDict
        self.GET = QueryDict('')
        self.COOKIES = {}
        self.session = FakeSesija()
        self.user = u
        self.path = '/'


R = FakeRequest()

print(u'\n== 1. Padangos ir ratlankiai matomi ==')
kiekiai = titulinis.ratu_kiekiai()
tikrinu(u'Padangos = 10', kiekiai['tyre'] == 10, kiekiai)
tikrinu(u'Ratlankiai = 2', kiekiai['rim'] == 2, kiekiai)
tikrinu(u'WheelListing modelyje nėra lauko wheel_type',
        not any(f.name == 'wheel_type' for f in WheelListing._meta.get_fields()
                if hasattr(f, 'name')),
        u'jei atsirado — senas filtras būtų veikęs')
tikrinu(u'ratlankiu_qs grąžina visus 12', titulinis.ratlankiu_qs(R).count() == 12)

print(u'\n== 2. „Pasiūlymai" — po 1–2 iš kiekvienos kategorijos ==')
p = titulinis.pasiulymai(VISI, R)
kategorijos = [titulinis.kategorija(o) for o in p]
tikrinu(u'bent 4 skirtingos kategorijos', len(set(kategorijos)) >= 4, set(kategorijos))
tikrinu(u'yra padangų arba ratlankių',
        'tyres' in kategorijos or 'rims' in kategorijos, set(kategorijos))
tikrinu(u'iš vienos kategorijos ne daugiau kaip 2',
        all(kategorijos.count(k) <= titulinis.PER_KATEGORIJA for k in set(kategorijos)),
        {k: kategorijos.count(k) for k in set(kategorijos)})
tikrinu(u'automobiliai nebedominuoja (buvo 11 iš 12)',
        kategorijos.count('cars') <= 2, kategorijos.count('cars'))
tikrinu(u'visos 7 netuščios kategorijos atstovaujamos',
        len(set(kategorijos)) == 7, set(kategorijos))
tuscia = VehicleType.objects.create(slug='boats', name='Katerai')
p2 = titulinis.pasiulymai(VISI, R)
tikrinu(u'tuščia kategorija praleidžiama',
        'boats' not in [titulinis.kategorija(o) for o in p2])
tuscia.delete()

print(u'\n== 2b. Tvarka stabili per sesiją ==')
a = [(o.__class__.__name__, o.pk) for o in titulinis.pasiulymai(VISI, R)]
b = [(o.__class__.__name__, o.pk) for o in titulinis.pasiulymai(VISI, R)]
tikrinu(u'perkrovus tas pats sąrašas ta pačia tvarka', a == b)


class KitaSesija(FakeRequest):
    def __init__(self):
        FakeRequest.__init__(self)
        self.session = type('S', (), {'session_key': 'kita999'})()


c = [(o.__class__.__name__, o.pk) for o in titulinis.pasiulymai(VISI, KitaSesija())]
tikrinu(u'kitai sesijai — kita tvarka', a != c, u'gali sutapti atsitiktinai')

print(u'\n== 3. „Dienos pasiūlymai" — žemiau medianos ==')
d = titulinis.dienos_pasiulymai(VISI, R, kiek=12)
tikrinu(u'nėra tuščias', len(d) > 0, len(d))
tikrinu(u'visi turi nuolaidos procentą',
        all(hasattr(o, 'nuolaida_proc') for o in d))
tikrinu(u'didžiausia nuolaida pirma',
        [o.nuolaida_proc for o in d] == sorted([o.nuolaida_proc for o in d], reverse=True),
        [o.nuolaida_proc for o in d])
# cars mediana = 12000; pigiausias 5000 -> ~58 %
pigiausias = [o for o in d if titulinis.kategorija(o) == 'cars']
tikrinu(u'automobilių pigiausias turi ~58% nuolaidą',
        pigiausias and pigiausias[0].nuolaida_proc == 58,
        pigiausias[0].nuolaida_proc if pigiausias else None)
tikrinu(u'brangesnių už medianą nėra',
        all(float(o.price) <= 12000 for o in d if titulinis.kategorija(o) == 'cars'))
tikrinu(u'mažos grupės praleistos (sunkvežimiai, priekabos, ž. ū. — po 1)',
        not any(titulinis.kategorija(o) in ('trucks', 'trailers', 'agriculture')
                for o in d),
        [titulinis.kategorija(o) for o in d])
tikrinu(u'motociklai (2 skelbimai) praleisti',
        'motorcycles' not in [titulinis.kategorija(o) for o in d])
tikrinu(u'padangos (10 skelbimų) įtrauktos',
        'tyres' in [titulinis.kategorija(o) for o in d],
        [titulinis.kategorija(o) for o in d])

print(u'\n== 3b. Metų juostos ==')
tikrinu(u'2020, 2021, 2022 — ta pati juosta',
        titulinis._metu_juosta(2020) == titulinis._metu_juosta(2021)
        == titulinis._metu_juosta(2022))
tikrinu(u'2023-2025 — kita juosta',
        titulinis._metu_juosta(2022) != titulinis._metu_juosta(2023)
        and titulinis._metu_juosta(2023) == titulinis._metu_juosta(2025))
tikrinu(u'senesni metai irgi grupuojami po tris',
        titulinis._metu_juosta(2017) == titulinis._metu_juosta(2019)
        != titulinis._metu_juosta(2016))
tikrinu(u'be metų — juostos nėra', titulinis._metu_juosta(None) is None)

print(u'\n== 4. Kiti skirtukai apima abu modelius ==')
br = titulinis.brangiausi(VISI, R, kiek=6)
tikrinu(u'brangiausi rikiuoti mažėjančiai',
        [float(o.price) for o in br] == sorted([float(o.price) for o in br], reverse=True))
nj = titulinis.naujausi(VISI, R, kiek=6)
tikrinu(u'naujausiuose yra ratlankių (jie sukurti paskutiniai)',
        any(titulinis.ar_ratlankis(o) for o in nj),
        [titulinis.kategorija(o) for o in nj])

print(u'\n== 5. „Populiariausi" — peržiūros + įsiminimai ==')
pop = titulinis.populiariausi(VISI, R, kiek=6)
tikrinu(u'be duomenų skirtukas slepiamas',
        titulinis.turi_populiarumo(pop) is False)
vienas = VISI.order_by('pk').first()
Listing.objects.filter(pk=vienas.pk).update(views_count=7)
pop = titulinis.populiariausi(VISI, R, kiek=6)
tikrinu(u'atsiradus peržiūroms — rodomas', titulinis.turi_populiarumo(pop) is True)
tikrinu(u'peržiūrėtas skelbimas pirmas', pop[0].pk == vienas.pk)
from apps.listings.models import SavedListing
kitas = VISI.exclude(pk=vienas.pk).order_by('pk').first()
for i in range(9):
    SavedListing.objects.create(user=User.objects.create_user('u%d' % i), listing=kitas)
pop = titulinis.populiariausi(VISI, R, kiek=6)
tikrinu(u'devyni įsiminimai aplenkia septynias peržiūras', pop[0].pk == kitas.pk,
        [(o.pk, o._populiarumas) for o in pop[:3]])

print(u'\n== 6. Nuorodos ir šablonas ==')
r1 = WheelListing.objects.first()
tikrinu(u'ratlankio nuoroda veda į /wheels/<id>/',
        r1.get_absolute_url() == '/wheels/%d/' % r1.pk, r1.get_absolute_url())
l1 = VISI.first()
tikrinu(u'skelbimo nuoroda veda į /<id>/',
        l1.get_absolute_url() == '/%d/' % l1.pk, l1.get_absolute_url())
sab = io.open(os.path.join(BASE, 'templates/listings/listing_list.html'),
              encoding='utf-8').read()
_skirtukai = sab[sab.index('HOME TABS'):]
tikrinu(u'skirtukų kortelės naudoja get_absolute_url',
        "{% url 'listing_detail' listing.pk %}\"" not in _skirtukai
        and _skirtukai.count('{{ listing.get_absolute_url }}') == 5,
        _skirtukai.count('{{ listing.get_absolute_url }}'))
tikrinu(u'„Populiariausi" mygtukas po sąlyga',
        sab.count('{% if tab_popular_rodyti %}') == 2, sab.count('{% if tab_popular_rodyti %}'))
tikrinu(u'„Dienos pasiūlymai" rodo nuolaidą', 'nuolaida_proc' in sab)

print(u'\n== 7. Vertimai ==')
po = io.open(os.path.join(BASE, 'locale/lt/LC_MESSAGES/django.po'), encoding='utf-8').read()
tikrinu(u'Newest → „Naujausi"', u'msgid "Newest"\nmsgstr "Naujausi"' in po)
tikrinu(u'Most expensive → „Brangiausi"',
        u'msgid "Most expensive"\nmsgstr "Brangiausi"' in po)
tikrinu(u'vienaskaitos nebeliko',
        u'msgstr "Naujausias"' not in po and u'msgstr "Brangiausias"' not in po)
truksta = []
for kalba in sorted(os.listdir(os.path.join(BASE, 'locale'))):
    kelias = os.path.join(BASE, 'locale', kalba, 'LC_MESSAGES', 'django.po')
    if not os.path.exists(kelias):
        continue
    t = io.open(kelias, encoding='utf-8').read()
    for msgid in (u'žemiau vidurkio', u'Kol kas nėra pakankamai skelbimų kainoms palyginti.'):
        if u'msgid "%s"' % msgid not in t:
            truksta.append('%s: %s' % (kalba, msgid))
tikrinu(u'nauji msgid yra visose 13 kalbų', not truksta, truksta)

print('')
if KLAIDOS:
    print(u'NEPRAĖJO: %d' % len(KLAIDOS))
    sys.exit(1)
print(u'VISI TESTAI PRAĖJO')
