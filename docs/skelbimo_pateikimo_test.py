# -*- coding: utf-8 -*-
"""
ĮKĖLUS SKELBIMĄ ŽMOGUS PATENKA Į „PAVYKO", O ŽINUTĖ YRA ŽALIA.

Du dalykai, kurie buvo sulūžę:

1. NEIŠLEISDAVO. Nemokamas publikavimas (mokėjimai išjungti) reikalavo
   metų, PIRMOS REGISTRACIJOS ir KURO — iš VISŲ kategorijų. Dalių,
   ratlankių, padangų, elektronikos, paslaugų, dviračių, valčių ir
   nuomos formose tokių laukų nėra visai, tad skelbimas niekada
   nebūdavo „užpildytas": žmogus paspausdavo „Įkelti" ir grįždavo į tą
   pačią formą su prierašu. Dabar reikalaujam tik to, ką kategorijos
   forma iš tikrųjų renka.

2. RAUDONA SĖKMĖ. Šablonai spalvą rinko `message.tags == 'success'`, o
   viską, kas ne tai, dažė RAUDONAI. Django prie ženklo prikabina ir
   papildomus (`extra_tags`), tad sėkmė lengvai atsidurdavo klaidos
   spalvoje. Dabar tikrinam `'success' in message.tags`, o nežinomas
   ženklas yra mėlynas, ne raudonas.

Paleidimas:  python docs/skelbimo_pateikimo_test.py
"""
import io, os, re, sys, tempfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
for k, v in (('SECRET_KEY', 'x'), ('EMAIL_USER', 'x@x.lt'), ('EMAIL_PASSWORD', 'x')):
    os.environ.setdefault(k, v)

import django
from django.conf import settings

LAIKINA = tempfile.mkdtemp(prefix='pateikimas-')
import config.settings as pagrindas
n = {k: v for k, v in vars(pagrindas).items() if k.isupper()}
n.update(
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3',
                           'NAME': os.path.join(LAIKINA, 'db.sqlite3')}},
    SECURE_SSL_REDIRECT=False, SESSION_COOKIE_SECURE=False,
    CSRF_COOKIE_SECURE=False, SECURE_HSTS_SECONDS=0,
    MEDIA_ROOT=LAIKINA, DEBUG=False, ALLOWED_HOSTS=['*'],
    PASTAS_FONE=False,
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
from django.urls import reverse

from apps.listings.models import (Brand, FuelType, Listing, Transmission,
                                  VehicleType)
from apps.listings.views import _skelbimas_uzpildytas

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
SLUGAI = ['cars', 'motorcycles', 'trucks', 'trailers', 'agriculture',
          'construction', 'loading-equipment', 'forestry', 'camping-houses',
          'rental', 'services', 'electronics', 'bicycles', 'boats', 'parts',
          'motogear', 'tires', 'wheels', 'minibuses']
TIPAI = {}
for slug in SLUGAI:
    TIPAI[slug], _ = VehicleType.objects.get_or_create(
        slug=slug, defaults={'name': slug.title()})
MARKE, _ = Brand.objects.get_or_create(name='BMW', defaults={'slug': 'bmw'})
KURAS, _ = FuelType.objects.get_or_create(name='Diesel')
PAVAROS, _ = Transmission.objects.get_or_create(name='Manual')


def _butini():
    """Modelio NOT NULL laukai — kad testinis įrašas apskritai atsirastų."""
    out = {}
    for f in Listing._meta.concrete_fields:
        if (f.primary_key or f.null or f.blank or f.has_default() or f.auto_created
                or getattr(f, 'auto_now', False)
                or getattr(f, 'auto_now_add', False)):
            continue
        it = f.get_internal_type()
        if it.endswith('IntegerField'): out[f.name] = 0
        elif it in ('DecimalField', 'FloatField'): out[f.name] = 0
        elif it in ('CharField', 'TextField', 'SlugField', 'EmailField', 'URLField'):
            out[f.name] = ''
        elif it == 'BooleanField': out[f.name] = False
    return out


BUTINI = _butini()


def skelbimas(slug, **extra):
    # year — NOT NULL modelyje, tad jį deda ir pačios formos
    duom = dict(BUTINI)
    duom.update(seller=u, vehicle_type=TIPAI[slug], title='Testas', year=2015,
                price=100, country='LT', city='Vilnius', status='draft')
    duom.update(extra)
    return Listing.objects.create(**duom)


# ═══════════════════════════════════════════════════════════════════
antraste('1. Užpildytas = tai, ką kategorijos forma renka')

# Kategorijos BE metų/registracijos/kuro laukų — kainos ir vietos gana
for slug in ('parts', 'services', 'electronics', 'bicycles', 'wheels',
             'tires', 'boats', 'rental'):
    l = skelbimas(slug)
    tikrink(_skelbimas_uzpildytas(l),
            '%s: užpildytas skelbimas laikomas neužpildytu' % slug)

# Tuščias skelbimas vis tiek nepraeina — apsauga nedingo
for slug in ('parts', 'cars'):
    tuscias = Listing(seller=u, vehicle_type=TIPAI[slug], title='x', year=2015)
    tuscias.price = None
    tikrink(not _skelbimas_uzpildytas(tuscias),
            '%s: tuščias skelbimas praėjo pro apsaugą' % slug)
be_vietos = Listing(seller=u, vehicle_type=TIPAI['parts'], title='x',
                    year=2015, price=10)
tikrink(not _skelbimas_uzpildytas(be_vietos),
        'skelbimas be vietos praėjo pro apsaugą')

# Automobiliams reikalavimai lieka griežti
maza = skelbimas('cars')
tikrink(not _skelbimas_uzpildytas(maza),
        'automobiliui be markės/kėbulo/pavarų nebereikia nieko')
pilna = skelbimas('cars', brand=MARKE, body_type='suv',
                  transmission=PAVAROS, doors='4/5', mileage=1000)
tikrink(_skelbimas_uzpildytas(pilna),
        'užpildytas automobilis laikomas neužpildytu')


# ═══════════════════════════════════════════════════════════════════
antraste('2. Pateikus skelbimą — „pavyko" puslapis, ne ta pati forma')

c = Client()
c.force_login(u)
for slug in ('parts', 'services', 'electronics', 'bicycles'):
    l = skelbimas(slug)
    r = c.get(reverse('listing_select_plan', kwargs={'pk': l.pk}), follow=True)
    galutinis = r.redirect_chain[-1][0] if r.redirect_chain else ''
    l.refresh_from_db()
    tikrink('/success/' in galutinis,
            '%s: po pateikimo nepateko į „pavyko" (%s)' % (slug, galutinis))
    tikrink(l.status == 'active',
            '%s: skelbimas liko %s' % (slug, l.status))
    tikrink(r.status_code == 200, '%s: „pavyko" puslapis neatsidarė' % slug)

# Nepilnas skelbimas ir toliau grąžinamas pildyti — bet tai NE sėkmė
nepilnas = skelbimas('cars')
r = c.get(reverse('listing_select_plan', kwargs={'pk': nepilnas.pk}), follow=True)
nepilnas.refresh_from_db()
tikrink(nepilnas.status == 'draft', 'nepilnas skelbimas buvo paskelbtas')
zinutes = list(r.context['messages']) if r.context and 'messages' in r.context else []
tikrink(all('success' not in z.tags for z in zinutes),
        'nepilnam skelbimui parodyta sėkmės žinutė')


# ═══════════════════════════════════════════════════════════════════
antraste('3. „Pavyko" puslapyje — nuoroda į patį skelbimą')

l = skelbimas('parts')
r = c.get(reverse('listing_select_plan', kwargs={'pk': l.pk}), follow=True)
kunas = r.content.decode('utf-8')
tikrink('/%d/' % l.pk in kunas, '„pavyko" puslapyje nėra nuorodos į skelbimą')


# ═══════════════════════════════════════════════════════════════════
antraste('4. Sėkmės žinutė — ŽALIA, nežinoma — ne raudona')

# Ciklas nebekopijuojamas: spalva gyvena vienoje dalyje
BENDRA = 'templates/partials/_zinutes.html'
tikrink(os.path.exists(os.path.join(BASE, BENDRA)), 'nėra %s' % BENDRA)
t = io.open(os.path.join(BASE, BENDRA), encoding='utf-8').read()
# Lyginimas „== 'success'" lūžta, kai Django prideda extra_tags
tikrink("message.tags == 'success'" not in t,
        '%s: spalvą renka tiksliu lyginimu (extra_tags viską sugriauna)' % BENDRA)
tikrink("'success' in message.tags" in t,
        '%s: sėkmės žinutė neturi savo (žalios) spalvos' % BENDRA)
# Raudona — tik klaidai. Jei „else" yra raudonas, sėkmė virsta klaida.
raudona_else = re.search(r"\{%\s*else\s*%\}[^{]*bg-red", t)
tikrink(not raudona_else, '%s: nežinomas ženklas dažomas raudonai' % BENDRA)

for kelias in ('templates/base.html',
               'templates/listings/my_listings.html',
               'templates/listings/listing_services_order.html',
               'templates/listings/wheels_detail.html'):
    t = io.open(os.path.join(BASE, kelias), encoding='utf-8').read()
    tikrink('partials/_zinutes.html' in t,
            '%s: žinutes piešia savo kodu, ne bendra dalimi' % kelias)


# ═══════════════════════════════════════════════════════════════════
antraste('5. Galerijos braukymas — skelbimo puslapyje')

det = io.open(os.path.join(BASE, 'templates/listings/listing_detail.html'),
              encoding='utf-8').read()
for dalis, kam in (('pirstasZemyn', 'piršto nuleidimas'),
                   ('pirstasAukstyn', 'piršto pakėlimas'),
                   ('Math.abs(dx) <= Math.abs(dy)', 'vertikalaus judesio atmetimas'),
                   ('touch-action: pan-y', 'puslapio slinkimas lieka puslapiui'),
                   ('atidaryk(', 'peržiūra neatsidaro po braukymo')):
    tikrink(dalis in det, 'galerijoje nėra: %s' % kam)
# Rodyklės darbalaukyje niekur nedingo
tikrink(det.count('fa-chevron-left') >= 1 and det.count('fa-chevron-right') >= 1,
        'dingo galerijos rodyklės')


print('\n' + '═' * 60)
print('gerai: %d, nepavyko: %d' % (gerai, blogai))
sys.exit(1 if blogai else 0)
