# -*- coding: utf-8 -*-
"""
KONTAKTINIS PAŠTAS IŠSISAUGO — IR REDAGUOJANT.

Du sulūžę dalykai, abu tikrinami čia.

1. PAŠTAS NIEKUR NENUGULĖDAVO. `Listing` neturėjo `contact_email`
   stulpelio: kontaktų blokas lauką rodė, žmogus jį keitė, o po
   išsaugojimo vėl matydavo paskyros paštą. Telefonas išlikdavo, nes jį
   vaizdai rašo į profilį. Dabar laukas yra, jį įrašo VISOS formos, o
   pradinę reikšmę ima iš skelbimo — į paskyros paštą krinta tik tada,
   kai skelbimo laukas tuščias.

2. SĖKMĖ KLAIDŲ DĖŽUTĖJE. `_form_errors.html` sėmė VISAS `messages`,
   tad po išsaugojimo rodydavo „Ištaisykite šias klaidas: Listing
   updated successfully." Dabar į tą dėžutę patenka tik klaidos.

Paleidimas:  python docs/kontaktu_pasto_test.py
"""
import io, os, re, sys, tempfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
for k, v in (('SECRET_KEY', 'x'), ('EMAIL_USER', 'x@x.lt'), ('EMAIL_PASSWORD', 'x')):
    os.environ.setdefault(k, v)

import django
from django.conf import settings

LAIKINA = tempfile.mkdtemp(prefix='kontaktai-')
import config.settings as pagrindas
n = {k: v for k, v in vars(pagrindas).items() if k.isupper()}
n.update(
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3',
                           'NAME': os.path.join(LAIKINA, 'db.sqlite3')}},
    SECURE_SSL_REDIRECT=False, SESSION_COOKIE_SECURE=False,
    CSRF_COOKIE_SECURE=False, SECURE_HSTS_SECONDS=0,
    MEDIA_ROOT=LAIKINA, DEBUG=False, ALLOWED_HOSTS=['*'], PASTAS_FONE=False,
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

from django.contrib import messages as dj_messages
from django.contrib.auth import get_user_model
from django.template import Context, Template
from django.test import Client, RequestFactory

from apps.listings import formos_klaidos
from apps.listings.kontaktai import issaugok_pasta, pasto_reiksme
from apps.listings.models import Listing, VehicleType

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
u = U.objects.create_user(username='p@x.lt', email='paskyros@x.lt', password='x')
# Profilio kalba lemia adreso priešdėlį (UserLanguageMiddleware): be jos
# nepriešdėlinis kelias POST'ui neišsisprendžia.
if hasattr(u, 'profile'):
    u.profile.language = 'lt'
    u.profile.save(update_fields=['language'])
VT, _sk = VehicleType.objects.get_or_create(slug='cars', defaults={'name': 'Cars'})


def _butini():
    out = {}
    for f in Listing._meta.concrete_fields:
        if (f.primary_key or f.null or f.blank or f.has_default() or f.auto_created
                or getattr(f, 'auto_now', False) or getattr(f, 'auto_now_add', False)):
            continue
        it = f.get_internal_type()
        if it.endswith('IntegerField'): out[f.name] = 0
        elif it in ('DecimalField', 'FloatField'): out[f.name] = 0
        elif it in ('CharField', 'TextField', 'SlugField', 'EmailField', 'URLField'):
            out[f.name] = ''
        elif it == 'BooleanField': out[f.name] = False
    return out
BUTINI = _butini()


def skelbimas(**extra):
    d = dict(BUTINI)
    d.update(seller=u, vehicle_type=VT, title='T', year=2015, price=100,
             country='LT', city='Vilnius', status='active')
    d.update(extra)
    return Listing.objects.create(**d)


# ═══════════════════════════════════════════════════════════════════
antraste('1. Modelyje yra laukas ir viena taisyklė, ką rodyti')

tikrink(any(f.name == 'contact_email' for f in Listing._meta.concrete_fields),
        'Listing neturi contact_email stulpelio')

l = skelbimas()
tikrink(l.kontaktinis_pastas == 'paskyros@x.lt',
        'tuščias skelbimo paštas turi kristi į paskyros')
l.contact_email = 'skelbimo@x.lt'
tikrink(l.kontaktinis_pastas == 'skelbimo@x.lt',
        'įrašytas skelbimo paštas turi būti svarbesnis už paskyros')

# Migracija — kad serveryje laukas atsirastų
migr = [f for f in os.listdir(os.path.join(BASE, 'apps/listings/migrations'))
        if 'contact_email' in f]
tikrink(migr, 'nėra migracijos su contact_email')


# ═══════════════════════════════════════════════════════════════════
antraste('2. Įrašymas iš POST')

rf = RequestFactory()
l = skelbimas()
issaugok_pasta(l, rf.post('/', {'email': '  naujas@x.lt '}))
tikrink(l.contact_email == 'naujas@x.lt', 'paštas neįrašytas arba su tarpais')

# Tuščias laukas NIEKO netrina — dalis srautų kontaktų bloko nerodo
issaugok_pasta(l, rf.post('/', {}))
tikrink(l.contact_email == 'naujas@x.lt', 'tuščias POST ištrynė įrašytą paštą')

# Pradinė reikšmė formai
tikrink(pasto_reiksme(l, u) == 'naujas@x.lt', 'formai paduodamas ne skelbimo paštas')
tikrink(pasto_reiksme(skelbimas(), u) == 'paskyros@x.lt',
        'naujam skelbimui neparodomas paskyros paštas')


# ═══════════════════════════════════════════════════════════════════
antraste('3. VISOS formos įrašo paštą, ne tik telefoną')

VAIZDAI = ['agriculture_views.py', 'bicycles_views.py', 'boats_views.py',
           'camping_views.py', 'construction_views.py', 'electronics_views.py',
           'forestry_views.py', 'loading_views.py', 'rental_views.py',
           'services_views.py', 'trailers_views.py', 'motogear_views.py',
           'motorcycles_views.py', 'parts_views.py', 'moto_part_views.py',
           'trucks_views.py', 'views.py']
be_pasto = []
for v in VAIZDAI:
    t = io.open(os.path.join(BASE, 'apps/listings', v), encoding='utf-8').read()
    if 'phone_number' not in t:
        continue
    if 'issaugok_pasta' not in t and 'contact_email' not in t:
        be_pasto.append(v)
tikrink(not be_pasto, 'telefoną įrašo, o pašto — ne: %s' % be_pasto)

# „Dalimis" kategorijos eina per bendrą pagalbininką
helpers = io.open(os.path.join(BASE, 'apps/listings/listing_helpers.py'),
                  encoding='utf-8').read()
tikrink('listing.contact_email = common_data' in helpers,
        'apply_common_fields_to_listing neįrašo pašto')

# Ratai/padangos turi savo stulpelį ir savo POST vardą
wheels = io.open(os.path.join(BASE, 'apps/listings/wheels_views.py'),
                 encoding='utf-8').read()
tikrink("contact_email" in wheels, 'wheels_views neįrašo contact_email')


# ═══════════════════════════════════════════════════════════════════
antraste('4. Formos rodo SKELBIMO paštą, ne paskyros')

SABLONAI = [f for f in os.listdir(os.path.join(BASE, 'templates/listings'))
            if 'create' in f and f.endswith('.html')]
blogai_prefill = []
for f in SABLONAI:
    t = io.open(os.path.join(BASE, 'templates/listings', f), encoding='utf-8').read()
    m = re.search(r"contact_block\.html'[^%]*?val_email=([^\s%]+)", t)
    if not m:
        continue
    reiksme = m.group(1)
    # Tinka: skelbimo/juodraščio laukas arba vaizdo paruoštas kintamasis
    if ('contact_email' in reiksme or 'kontaktinis' in reiksme
            or reiksme.startswith('user_email')
            or reiksme.startswith('submitted.email')
            or reiksme.startswith('data.email')
            or reiksme.startswith('listing_data.step7.email')):
        continue
    blogai_prefill.append('%s → %s' % (f, reiksme))
tikrink(not blogai_prefill,
        'formos rodo paskyros paštą: %s' % blogai_prefill[:5])

# Vaizdų paruošti kintamieji irgi turi remtis skelbimu
for v, zyme in (('parts_views.py', 'kontaktinis_pastas'),
                ('moto_part_views.py', 'kontaktinis_pastas'),
                ('motorcycles_views.py', "'email': draft.contact_email"),
                ('motogear_views.py', "'email': draft.contact_email"),
                ('trucks_views.py', "'email': listing.contact_email")):
    t = io.open(os.path.join(BASE, 'apps/listings', v), encoding='utf-8').read()
    tikrink(zyme in t, '%s: pradinė pašto reikšmė ne iš skelbimo' % v)


# ═══════════════════════════════════════════════════════════════════
antraste('5. Pilnas ratas per HTTP: pakeista reikšmė išlieka')

c = Client()
c.force_login(u)
l = skelbimas(status='active', brand=None)
adresas = '/create/cars/quick/?edit=%d' % l.pk
# follow=True — LocaleMiddleware pirma permeta į kalbos priešdėlį
r = c.get(adresas, follow=True)
tikrink(r.status_code == 200, 'redagavimo forma neatsidarė (%s)' % r.status_code)
tikrink('paskyros@x.lt' in r.content.decode('utf-8'),
        'naujam skelbimui nerodomas paskyros paštas')

l.contact_email = 'kitas@x.lt'
l.save(update_fields=['contact_email'])
r = c.get(adresas, follow=True)
kunas = r.content.decode('utf-8')
tikrink('kitas@x.lt' in kunas, 'įrašytas paštas formoje nerodomas')
tikrink(re.search(r'name=[\'"]email[\'"][^>]*value=[\'"]paskyros@x\.lt', kunas) is None,
        'paskyros paštas perrašo įrašytą reikšmę')

# TIKRA reprodukcija: pateikiam redagavimo formą su kitu paštu
duomenys = {
    'edit': str(l.pk), 'year': '2015', 'price': '100',
    'country': 'LT', 'city': 'Vilnius', 'phone': '+37060000000',
    'email': 'pakeistas@x.lt', 'description': 'x',
}
r = c.post('/create/cars/quick/?edit=%d' % l.pk, duomenys, follow=True)
l.refresh_from_db()
tikrink(l.contact_email == 'pakeistas@x.lt',
        'po išsaugojimo paštas liko %r' % l.contact_email)
tikrink(u.email == 'paskyros@x.lt',
        'skelbimo paštas per klaidą perrašė PASKYROS paštą')

r = c.get(adresas, follow=True)
tikrink('pakeistas@x.lt' in r.content.decode('utf-8'),
        'po perkrovimo formoje vėl ne ta reikšmė')

# TELEFONAS — atvirkštinio atvejo patikra: jis gyvena profilyje ir
# redaguojant privalo išlikti lygiai taip pat
u.profile.refresh_from_db()
tikrink(u.profile.phone_number == '+37060000000',
        'telefonas redaguojant neišsisaugojo (%r)' % u.profile.phone_number)
r = c.get(adresas, follow=True)
tikrink('+37060000000' in r.content.decode('utf-8'),
        'po perkrovimo formoje nerodomas išsaugotas telefonas')

# Ir kodo lygmeniu: kur įrašomas telefonas, ten įrašomas ir paštas
VIETOS = []
for v in VAIZDAI + ['listing_helpers.py']:
    t = io.open(os.path.join(BASE, 'apps/listings', v), encoding='utf-8').read()
    tel = t.count('profile.phone_number = ')
    pastas = t.count('issaugok_pasta(') + t.count('listing.contact_email =')
    if tel and pastas < 1:
        VIETOS.append('%s (telefonas %d, paštas %d)' % (v, tel, pastas))
tikrink(not VIETOS, 'telefoną įrašo, o pašto — ne: %s' % VIETOS)


# ═══════════════════════════════════════════════════════════════════
antraste('6. Pirkėjo laiškas eina skelbimo paštu')

vaizdai = io.open(os.path.join(BASE, 'apps/listings/views.py'),
                  encoding='utf-8').read()
tikrink('[listing.kontaktinis_pastas]' in vaizdai,
        'contact_seller vis dar rašo paskyros paštu')
# Paskyros pranešimai (peržiūros, įsiminimai) lieka paskyros pašte
tikrink(vaizdai.count('to_email=seller.email') >= 3,
        'paskyros pranešimai per klaidą perkelti į skelbimo paštą')


# ═══════════════════════════════════════════════════════════════════
antraste('7. Sėkmės žinutė nebekrenta į klaidų dėžutę')

def _piesk(lygis, tekstas):
    """Atvaizduoja _form_errors.html su viena žinute.

    Tikrinam ABU kelius: šablono žymę (`messages` kontekste) ir
    kontekstinį procesorių (`form_errors`) — pirmoji pataisa lietė tik
    žymę, o naršyklėje laimėdavo procesorius, tad klaida liko.
    """
    uzklausa = rf.get('/')
    zinute = dj_messages.storage.base.Message(lygis, tekstas)
    sablonas = Template("{% include 'listings/partials/_form_errors.html' %}")
    pro_zyme = sablonas.render(Context({'messages': [zinute],
                                        'request': uzklausa}))
    is_procesoriaus = formos_klaidos.kontekstas(
        formos_klaidos.tik_klaidu_tekstai([zinute]))
    pro_procesoriu = sablonas.render(Context({
        'request': uzklausa,
        'error_fields': is_procesoriaus['error_fields'],
        'error_messages': is_procesoriaus['error_messages'],
        'form_errors': is_procesoriaus['form_errors'],
    }))
    return pro_zyme + pro_procesoriu

# Dėžutę atpažįstam iš žymės (form-error-box), ne iš išversto teksto:
# aktyvi kalba priklauso nuo ankstesnių šio testo užklausų.
sekme = _piesk(dj_messages.SUCCESS, 'Listing updated successfully.')
tikrink('form-error-box' not in sekme and 'successfully' not in sekme,
        'sėkmės žinutė vis dar rodoma klaidų dėžutėje')

info = _piesk(dj_messages.INFO, 'Užpildykite skelbimą prieš jo aktyvavimą.')
tikrink('form-error-box' not in info, 'informacinė žinutė rodoma kaip klaida')

klaida = _piesk(dj_messages.ERROR, 'Telefonas yra privalomas')
tikrink('form-error-box' in klaida, 'tikra klaida nebeparodoma')

# Papildomi ženklai (extra_tags) sėkmės nepaverčia klaida
su_zenklu = dj_messages.storage.base.Message(
    dj_messages.SUCCESS, 'Listing updated successfully.', extra_tags='sticky')
tikrink('success' in su_zenklu.tags and su_zenklu.tags != 'success',
        'extra_tags nebeprikabinami — patikra nebeprasminga')


# ═══════════════════════════════════════════════════════════════════
antraste('8. Žinučių blokas — vienas visai svetainei')

tikrink(os.path.exists(os.path.join(BASE, 'templates/partials/_zinutes.html')),
        'nėra bendros žinučių dalies')
kopijos = []
for saknis, _d, failai in os.walk(os.path.join(BASE, 'templates')):
    for f in failai:
        if not f.endswith('.html'):
            continue
        kelias = os.path.join(saknis, f)
        t = io.open(kelias, encoding='utf-8').read()
        if 'for message in messages' in t and not kelias.endswith('_zinutes.html'):
            kopijos.append(os.path.relpath(kelias, BASE))
# Prisijungimo ir slaptažodžio puslapiai turi savo apipavidalinimą
kopijos = [k for k in kopijos if 'accounts/' not in k]
tikrink(not kopijos, 'žinučių ciklas vis dar nukopijuotas: %s' % kopijos)

zin = io.open(os.path.join(BASE, 'templates/partials/_zinutes.html'),
              encoding='utf-8').read()
for zenklas, spalva in (('success', 'green'), ('error', 'red'),
                        ('warning', 'yellow')):
    tikrink("'%s' in message.tags" % zenklas in zin and spalva in zin,
            'bendroje dalyje nėra %s → %s' % (zenklas, spalva))
tikrink('{% if message.tags ==' not in zin,
        'spalva renkama tiksliu lyginimu — extra_tags viską sugriauna')

# Klaidas atrenka VIENA taisyklė, kurią naudoja ir šablono žymė, ir
# kontekstinis procesorius
cp = io.open(os.path.join(BASE, 'apps/listings/context_processors.py'),
             encoding='utf-8').read()
tikrink('tik_klaidu_tekstai' in cp,
        'kontekstinis procesorius vis dar semia visas žinutes')
zym = io.open(os.path.join(BASE,
              'apps/listings/templatetags/formos_klaidos_tags.py'),
              encoding='utf-8').read()
tikrink('tik_klaidu_tekstai' in zym, 'šablono žymė nenaudoja bendros taisyklės')
tikrink(formos_klaidos.yra_klaida(
    dj_messages.storage.base.Message(dj_messages.ERROR, 'x')),
    'klaida neatpažįstama')
tikrink(not formos_klaidos.yra_klaida(
    dj_messages.storage.base.Message(dj_messages.SUCCESS, 'x',
                                     extra_tags='sticky')),
    'sėkmė su extra_tags vis dar laikoma klaida')


print('\n' + '═' * 60)
print('gerai: %d, nepavyko: %d' % (gerai, blogai))
sys.exit(1 if blogai else 0)
