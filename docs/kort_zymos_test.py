# -*- coding: utf-8 -*-
"""KORTELĖS ŽYMOS — ar „Pasiūlymų" srautas rodo tas pačias žymas kaip sąrašas.

Bendras blokas partials/_kort_zymos.html turi duoti tą patį rezultatą ir
skelbimų sąrašo kortelėje (_skelbimo_kortele.html), ir pagrindinio
puslapio skirtukų kortelėse (listing_list.html home-tab-card).

Tikrinam: „Naujas", laiko žyma, VIN ir žvaigždutė; kad seno kartojimo
nebeliko; kad veikia ne tik lietuviškai.

Paleidimas:  python docs/kort_zymos_test.py
"""
import io, os, re, sys, django
from datetime import timedelta
from django.conf import settings

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
settings.configure(
    DEBUG=True, USE_I18N=True, USE_TZ=True, LANGUAGE_CODE='lt', SECRET_KEY='x',
    ALLOWED_HOSTS=['*'], LOCALE_PATHS=[os.path.join(BASE, 'locale')],
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}},
    DEFAULT_AUTO_FIELD='django.db.models.AutoField',
    INSTALLED_APPS=['django.contrib.contenttypes', 'django.contrib.auth',
                    'django.contrib.humanize', 'apps.listings', 'apps.accounts'],
    TEMPLATES=[{'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [os.path.join(BASE, 'templates')], 'APP_DIRS': True,
                'OPTIONS': {'context_processors': []}}],
)
django.setup()

from django.template.loader import render_to_string
from django.utils import timezone, translation

KLAIDOS = []


def tikrinu(pav, salyga, papild=''):
    if salyga:
        print(u'  ✓ %s' % pav)
    else:
        print(u'  ✗ %s %s' % (pav, papild))
        KLAIDOS.append(pav)


class FakeSkelbimas(object):
    """Tik tie laukai, kuriuos liečia žymų blokas."""
    def __init__(self, vin='', zvaigzdes=0, star_count=0, naujas=True):
        self.vin = vin
        self._zv = zvaigzdes
        self.star_count = star_count
        self.yra_naujas = naujas
        self.paskelbta = timezone.now() - timedelta(hours=5)
        self.title = u'BMW 320d'

    def get_effective_star_level(self):
        return self._zv


def zymos(**kw):
    return render_to_string('listings/partials/_kort_zymos.html',
                            {'listing': FakeSkelbimas(**kw)})


print(u'\n== 1. Bendras blokas rodo visas žymas ==')
h = zymos(vin='WBA123', zvaigzdes=1, star_count=3)
tikrinu(u'„Naujas" žyma', 'card-badge-new' in h, h[:200])
tikrinu(u'laiko žyma', 'card-badge-time' in h and 'data-paskelbta' in h)
tikrinu(u'VIN žyma', 'sk-vin' in h and 'VIN' in h)
tikrinu(u'žvaigždutė su kiekiu', 'mini-1star' in h and '3' in h)

print(u'\n== 2. Ko nėra — to ir nerodo ==')
h = zymos(vin='', zvaigzdes=0, naujas=False)
tikrinu(u'be VIN — nėra sk-vin', 'sk-vin' not in h)
tikrinu(u'be žvaigždučių — nėra mini-1star', 'mini-1star' not in h)
tikrinu(u'nenaujas — nėra card-badge-new', 'card-badge-new' not in h)
tikrinu(u'laikas rodomas visada', 'card-badge-time' in h)
tikrinu(u'tuščias apatinis kampas nepiešiamas', 'card-bottom-left' not in h)

print(u'\n== 3. Sąrašo kortelė naudoja BENDRĄ bloką ==')
kort = io.open(os.path.join(BASE, 'templates/listings/partials/_skelbimo_kortele.html'),
               encoding='utf-8').read()
tikrinu(u'_skelbimo_kortele įtraukia _kort_zymos', '_kort_zymos.html' in kort)
tikrinu(u'nebeturi savos _laiko_zyma kopijos', '_laiko_zyma.html' not in kort)
tikrinu(u'nebeturi savos VIN kopijos', 'sk-vin' not in kort)

print(u'\n== 4. Pagrindinio puslapio skirtukai naudoja TĄ PATĮ bloką ==')
hp = io.open(os.path.join(BASE, 'templates/listings/listing_list.html'),
             encoding='utf-8').read()
kiek = hp.count("_kort_zymos.html' with listing=listing")
tikrinu(u'penki skirtukai + rezultatų kortelė = 6 įtraukimai',
        kiek == 6, u'rasta %d' % kiek)
tikrinu(u'kiekvienas home-tab-img turi žymas',
        hp.count('home-tab-img">') == 5 and kiek >= 5)
tikrinu(u'sena rezultatų kortelės kopija pašalinta',
        "_laiko_zyma.html' with listing=listing" not in hp)
tikrinu(u'mini-1star stilius nebedubliuojamas', '.mini-1star {' not in hp)

print(u'\n== 5. Stiliai — viena vieta, abiejuose puslapiuose ==')
st = io.open(os.path.join(BASE, 'templates/listings/partials/_kort_zymos_stiliai.html'),
             encoding='utf-8').read()
tikrinu(u'VIN spalva nepakeista', 'rgba(6,118,71,.9)' in st)
tikrinu(u'žvaigždutės spalva nepakeista', 'rgba(0,0,0,0.35)' in st)
tikrinu(u'VIN dydis iš dizaino sistemos', 'var(--fs-xs)' in st)
kd = io.open(os.path.join(BASE, 'templates/listings/partials/_kortele_stiliai.html'),
             encoding='utf-8').read()
tikrinu(u'sąrašo puslapis įtraukia bendrus stilius', '_kort_zymos_stiliai' in kd)
tikrinu(u'pagrindinis puslapis įtraukia bendrus stilius', '_kort_zymos_stiliai' in hp)
tikrinu(u'.sk-vin apibrėžtas tik bendrame faile', '.sk-vin {' not in kd)

print(u'\n== 6. Kalbos — msgid verčiami, ne įrašyti kietai ==')
for kalba in ('en', 'ru', 'de'):
    with translation.override(kalba):
        h = zymos(vin='WBA1', zvaigzdes=1)
    tikrinu(u'%s: blokas atsipiešia' % kalba,
            'card-badge-time' in h and 'sk-vin' in h)
tikrinu(u'„Naujas" eina per {% trans %}',
        '{% trans "Naujas" %}' in io.open(
            os.path.join(BASE, 'templates/listings/partials/_laiko_zyma.html'),
            encoding='utf-8').read())
tikrinu(u'VIN eina per {% trans %}',
        '{% trans "VIN" %}' in io.open(
            os.path.join(BASE, 'templates/listings/partials/_kort_zymos.html'),
            encoding='utf-8').read())

print(u'\n== 7. Ratlankis — be VIN ir be get_effective_star_level ==')


class FakeRatlankis(object):
    """WheelListing neturi nei vin, nei get_effective_star_level —
    bendras blokas privalo nesugriūti (kortelė ta pati abiem modeliams,
    žr. apps/listings/korteles.py)."""
    def __init__(self):
        self.yra_naujas = True
        self.paskelbta = timezone.now() - timedelta(days=1)
        self.title = u'Nokian 205/55 R16'


h = render_to_string('listings/partials/_kort_zymos.html',
                     {'listing': FakeRatlankis()})
tikrinu(u'atsipiešia be klaidos', 'card-badge-time' in h)
tikrinu(u'„Naujas" rodoma', 'card-badge-new' in h)
tikrinu(u'nėra VIN', 'sk-vin' not in h)
tikrinu(u'nėra žvaigždutės', 'mini-1star' not in h)
tikrinu(u'nėra tuščio apatinio kampo', 'card-bottom-left' not in h)

print('')
if KLAIDOS:
    print(u'NEPRAĖJO: %d' % len(KLAIDOS))
    sys.exit(1)
print(u'VISI TESTAI PRAĖJO')
