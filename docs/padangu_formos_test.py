# -*- coding: utf-8 -*-
"""
PADANGOS IR RATLANKIAI: FORMA VĖL SIUNČIAMA, SĄRAŠAI PAKANKAMI.

Kas buvo.

1. TYRE-01 / RIM-01 — paskelbti nebuvo įmanoma VISAI. handleTyresSubmit()
   ir handleRimsSubmit() telefono ieškojo per getElementById('id_contact_phone'),
   o tokio id puslapyje nėra: kontaktų blokas name'ą gauna parametru
   (contact_phone), bet id jame visada id_phone. Todėl `phone` visada
   buvo null, klaida įsirašydavo net užpildžius telefoną, ir funkcija
   grąžindavo return — forma niekada nebūdavo išsiųsta.

2. TYRE-02 — klaidų pranešimai rodė ne tą lauką („Būtina nurodyti
   valstiją" vietoj „gamintoją"). Šablono msgid'ai buvo teisingi —
   klydo LIETUVIŠKAS vertimas, penkiose eilutėse.

3. TYRE-03/04 — sąrašai per trumpi: R16C, 315/70 R22.5, motociklų
   pločių 90–130 įvesti buvo neįmanoma.

4. TYRE-10 — paieškos panelė turėjo SAVO sąrašus ir net kitas reikšmes
   („car", „van", „agro", „quad" vietoj passenger/commercial/industrial).
   Toks filtras nerasdavo nieko.

Paleidimas:  python docs/padangu_formos_test.py
"""
import io, os, re, sys, tempfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
for k, v in (('SECRET_KEY', 'x'), ('EMAIL_USER', 'x@x.lt'), ('EMAIL_PASSWORD', 'x')):
    os.environ.setdefault(k, v)

import django
from django.conf import settings

LAIKINA = tempfile.mkdtemp(prefix='padangos-')
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
from django.test.utils import setup_test_environment

setup_test_environment()
call_command('migrate', run_syncdb=True, verbosity=0)

from django.contrib.auth import get_user_model
from django.test import Client

from apps.listings import models as M
from apps.listings.models import WheelListing

gerai = blogai = 0
def tikrink(s, k):
    global gerai, blogai
    if s:
        gerai += 1
    else:
        blogai += 1
        print('  NEPAVYKO: ' + k)
def antraste(t):
    print('\n── ' + t + ' ' + '─' * max(0, 52 - len(t)))


U = get_user_model()
u = U.objects.create_user(username='p@x.lt', email='p@x.lt', password='x')
if hasattr(u, 'profile'):
    u.profile.language = 'lt'
    u.profile.phone_number = '+37060000000'
    u.profile.save()
c = Client()
c.force_login(u)


def parinktys(kunas, vardas):
    m = re.search(r'<select[^>]*name="%s".*?</select>' % vardas, kunas, re.S)
    if not m:
        return []
    return [v for v in re.findall(r'<option value="([^"]*)"', m.group(0)) if v]


# ═══════════════════════════════════════════════════════════════════
antraste('1. Telefonas ieškomas pagal NAME (TYRE-01 / RIM-01)')

for f in ('tyres_create.html', 'rims_create.html', 'wheels_create.html'):
    t = io.open(os.path.join(BASE, 'templates/listings', f), encoding='utf-8').read()
    tikrink("getElementById('id_contact_phone')" not in t,
            '%s: vėl ieško pagal id_contact_phone' % f)
    tikrink('[name="contact_phone"]' in t,
            '%s: neieško pagal name' % f)

# Bendra taisyklė visiems šablonams: nė vienas getElementById('id_…')
# neturi rodyti į id, kurio puslapyje nėra.
TPL = os.path.join(BASE, 'templates')

def su_includais(kelias, matyti=None, gylis=0):
    if matyti is None:
        matyti = set()
    if kelias in matyti or gylis > 6:
        return ''
    matyti.add(kelias)
    try:
        t = io.open(kelias, encoding='utf-8').read()
    except Exception:
        return ''
    dalys = [t]
    for m in re.finditer(r"{%\s*(?:include|extends)\s+['\"]([^'\"]+)", t):
        dalys.append(su_includais(os.path.join(TPL, m.group(1)), matyti, gylis + 1))
    return '\n'.join(dalys)

pamesti = []
for saknis, _d, failai in os.walk(TPL):
    for f in failai:
        if not f.endswith('.html'):
            continue
        kelias = os.path.join(saknis, f)
        t = io.open(kelias, encoding='utf-8').read()
        ieskomi = set(re.findall(r"""getElementById\(\s*['"](id_[A-Za-z0-9_]+)['"]""", t))
        if not ieskomi:
            continue
        visas = su_includais(kelias)
        esami = set(re.findall(r"""id=['"](id_[A-Za-z0-9_]+)['"]""", visas))
        truksta = sorted(i for i in ieskomi if i not in esami)
        if truksta:
            pamesti.append('%s: %s' % (os.path.relpath(kelias, BASE), ', '.join(truksta)))
tikrink(not pamesti, 'šablonai ieško nesamų id: %s' % pamesti)


# ═══════════════════════════════════════════════════════════════════
antraste('2. Klaidų pranešimai — apie TĄ lauką (TYRE-02)')

from django.utils import translation
with translation.override('lt'):
    from django.utils.translation import gettext
    LAUKTA = {
        'Manufacturer is required': 'gamintoj',
        'Diameter is required': 'skersmen',
        'Width is required': 'plot',
        'Profile is required': 'profil',
        'Season is required': 'sezoni',
        'Price is required': 'kain',
        'State is required': 'valstij',
        'City is required': 'miest',
    }
    for msgid, saknis in LAUKTA.items():
        verstas = gettext(msgid)
        tikrink(saknis in verstas.lower(),
                '„%s" → „%s" (turi minėti „%s")' % (msgid, verstas, saknis))


# ═══════════════════════════════════════════════════════════════════
antraste('3. Sąrašai pakankami (TYRE-03 / TYRE-04)')

DYDZIAI = {
    'WHEEL_DIAMETER_CHOICES': 57,
    'TYRE_PROFILE_CHOICES': 29,
    'TYRE_TREAD_CHOICES': 27,
    'TYRE_REMAINING_CHOICES': 20,
    'WHEEL_CONDITION_CHOICES': 3,
    'TYRE_SEASON_CHOICES': 4,
    'WHEEL_PURPOSE_CHOICES': 7,
}
for vardas, kiek in DYDZIAI.items():
    sar = getattr(M, vardas)
    tikrink(len(sar) == kiek, '%s: %d, laukta %d' % (vardas, len(sar), kiek))
tikrink(len(M.TYRE_WIDTH_CHOICES) >= 80,
        'TYRE_WIDTH_CHOICES: %d, laukta bent 80' % len(M.TYRE_WIDTH_CHOICES))

# Reikšmės, dėl kurių tikri skelbimai buvo neįvedami
for reiksme in ('16C', '22.5', '15.3', '4', '63'):
    tikrink(any(v == reiksme for v, _l in M.WHEEL_DIAMETER_CHOICES),
            'skersmuo %s neprieinamas' % reiksme)
for reiksme in ('90', '120', '130', '315', '5.50', '1050'):
    tikrink(any(v == reiksme for v, _l in M.TYRE_WIDTH_CHOICES),
            'plotis %s neprieinamas' % reiksme)
tikrink(any(v == 'refurbished' for v, _l in M.WHEEL_CONDITION_CHOICES),
        'nėra būklės „refurbished"')
tikrink(any(v == 'other' for v, _l in M.TYRE_SEASON_CHOICES),
        'nėra sezoniškumo „other"')
tikrink(any(v == 'atv' for v, _l in M.WHEEL_PURPOSE_CHOICES),
        'nėra paskirties „atv"')

# Senos reikšmės NEDINGO
for reiksme in ('10', '16', '24'):
    tikrink(any(v == reiksme for v, _l in M.WHEEL_DIAMETER_CHOICES),
            'dingo senas skersmuo %s' % reiksme)
for reiksme in ('new', 'used'):
    tikrink(any(v == reiksme for v, _l in M.WHEEL_CONDITION_CHOICES),
            'dingo sena būklė %s' % reiksme)

# Stulpeliai talpina ilgiausias reikšmes
LAUKAI = {'diameter': M.WHEEL_DIAMETER_CHOICES, 'tyre_width': M.TYRE_WIDTH_CHOICES,
          'tyre_profile': M.TYRE_PROFILE_CHOICES, 'tyre_tread_mm': M.TYRE_TREAD_CHOICES,
          'condition': M.WHEEL_CONDITION_CHOICES, 'purpose': M.WHEEL_PURPOSE_CHOICES,
          'tyre_season': M.TYRE_SEASON_CHOICES}
for vardas, sar in LAUKAI.items():
    laukas = WheelListing._meta.get_field(vardas)
    ilgiausia = max(len(v) for v, _l in sar)
    tikrink(laukas.max_length >= ilgiausia,
            '%s: max_length %d < ilgiausios reikšmės %d'
            % (vardas, laukas.max_length, ilgiausia))


# ═══════════════════════════════════════════════════════════════════
antraste('4. Forma ir filtras — iš to paties šaltinio (TYRE-10)')

panele = io.open(os.path.join(BASE,
                 'templates/listings/partials/_panel_bodies.html'),
                 encoding='utf-8').read()
tikrink('ratu_sarasas' in panele, 'panelė neima bendrų sąrašų')
for senas in ('value="car"', 'value="van"', 'value="agro"', 'value="quad"'):
    tikrink(senas not in panele,
            'panelėje liko sena paskirties reikšmė %s' % senas)

from apps.listings.templatetags.ratu_tags import ratu_sarasas
for vardas, konstanta in (('diameter', M.WHEEL_DIAMETER_CHOICES),
                          ('tyre_width', M.TYRE_WIDTH_CHOICES),
                          ('purpose', M.WHEEL_PURPOSE_CHOICES)):
    tikrink(ratu_sarasas(vardas) == list(konstanta),
            'žyma %s grąžina ne tą sąrašą' % vardas)
tikrink(ratu_sarasas('nesamas') == [], 'nežinomas sąrašas nemeta klaidos')


# ═══════════════════════════════════════════════════════════════════
antraste('5. Tikras skelbimas paskelbiamas (TYRE-01 patikra)')

forma = c.get('/create/tyres/').content.decode()
tikrink('16C' in parinktys(forma, 'diameter'), 'formoje nėra R16C')
tikrink('120' in parinktys(forma, 'tyre_width'), 'formoje nėra pločio 120')
tikrink(bool(re.search(r'name="agree_terms"[^>]*required', forma)),
        'agree_terms be required (TYRE-13)')
tikrink('Vieneto kaina' in forma, 'kainos etiketė ne „Vieneto kaina" (TYRE-16)')
tikrink('komplekto-kaina' in forma, 'nėra komplekto kainos eilutės (TYRE-16)')
tikrink(re.search(r'(20|nuotrauk).{0,80}(MB|JPG)', forma, re.S | re.I) is not None,
        'nėra nuotraukų ribų aprašo (TYRE-16)')

BENDRA = dict(product_type='tyre', contact_phone='+37060000000',
              contact_email='p@x.lt', country='LT', agree_terms='on')

r = c.post('/create/tyres/', dict(
    BENDRA, brand_name='Bridgestone', model_name='Duravis',
    purpose='commercial', diameter='16C', tyre_width='205', tyre_profile='65',
    tyre_season='summer', condition='used', quantity='2', price='50',
    tyre_remaining_pct='100', tyre_tread_mm='10', tyre_dot_year='2024',
    city='Marijampolė'))
tikrink(r.status_code == 302, 'Bridgestone: POST → %s (turi būti 302)' % r.status_code)
tikrink('/wheels/' in r.get('Location', ''),
        'Bridgestone: nenukreipė į skelbimą (%s)' % r.get('Location', ''))
bridge = WheelListing.objects.filter(brand_name='Bridgestone').first()
tikrink(bridge is not None, 'Bridgestone skelbimas nesukurtas')

r = c.post('/create/tyres/', dict(
    BENDRA, brand_name='Michelin', model_name='Pilot Power 3',
    purpose='moto', diameter='17', tyre_width='120', tyre_profile='70',
    tyre_season='summer', condition='used', quantity='1', price='130',
    city='Vilnius'))
tikrink(r.status_code == 302, 'Michelin: POST → %s' % r.status_code)
moto = WheelListing.objects.filter(brand_name='Michelin').first()
tikrink(moto is not None, 'Michelin skelbimas nesukurtas')

# Ratlankiai — ta pati telefono klaida
r = c.post('/create/rims/', dict(
    product_type='rim', brand_name='BBS', diameter='18', rim_width='8',
    rim_pcd='5x112', rim_bolt_count='5', rim_material='alloy', quantity='4',
    price='400', condition='used', contact_phone='+37060000000',
    contact_email='p@x.lt', country='LT', city='Kaunas', agree_terms='on'))
tikrink(r.status_code == 302, 'BBS ratlankiai: POST → %s' % r.status_code)


# ═══════════════════════════════════════════════════════════════════
antraste('6. Skelbimo puslapis (TYRE-05 / 06 / 12)')

if bridge:
    tikrink(bridge.title == 'Bridgestone 205/65 R16C',
            'pavadinimas be „R": %s' % bridge.title)
    b = c.get('/wheels/%d/' % bridge.pk).content.decode()
    tikrink('>summer<' not in b, 'rodoma žalia reikšmė „summer" (TYRE-05)')
    tikrink('Vasarin' in b, 'sezoniškumas neišverstas')
    for lt, en in (('Specifikacijos', 'Specifications'),
                   ('Likutis', 'Remaining'),
                   ('Pagaminimo metai', 'Production year')):
        tikrink(lt in b and ('>%s<' % en) not in b,
                'lentelėje liko angliškas „%s" (TYRE-06)' % en)

# Visi sezoniškumai, įskaitant naują
with translation.override('lt'):
    for reiksme in ('summer', 'winter', 'all_season', 'other'):
        w = WheelListing(product_type='tyre', tyre_season=reiksme)
        tikrink(w.get_tyre_season_display() != reiksme,
                'sezoniškumas „%s" neturi vertimo' % reiksme)


# ═══════════════════════════════════════════════════════════════════
antraste('7. Katalogas (TYRE-07 / 08 / 09 / 17)')

with translation.override('lt'):
    b = c.get('/browse/tyres/').content.decode()
    tikrink('Naršyti padangas' in b, 'ne tas <title> (TYRE-07)')
    tikrink('Naršyti sunkvežimius' not in b, 'liko sunkvežimių antraštė (TYRE-07)')
    tikrink('Rasta skelbimų:' in b, 'nerodoma „Rasta skelbimų" (TYRE-08)')
    tikrink('Nerasta jokių skelbimų' not in b.split('Rasta skelbimų')[0],
            '„Nerasta" rodoma, nors rezultatų yra (TYRE-08)')
    tikrink('Redaguoti profilį' not in b, 'kortelėje „Redaguoti profilį" (TYRE-09)')
    tikrink('>Naujas<' not in b, 'įkėlimo žyma vis dar „Naujas" (TYRE-17)')

    tuscia = c.get('/browse/tyres/?city=NeraTokioMiesto').content.decode()
    tikrink('Nerasta jokių skelbimų' in tuscia,
            'tuščiam rezultatui nerodoma „Nerasta" (TYRE-08)')
    tikrink('Rasta skelbimų:' not in tuscia,
            'tuščiam rezultatui rodoma „Rasta skelbimų" (TYRE-08)')

    r = c.get('/browse/rims/')
    tikrink('Naršyti ratlankius' in r.content.decode(), 'ratlankių <title> ne tas')

# Senos filtro nuorodos vis dar veikia
for senas, nauja in (('van', 'commercial'), ('car', 'passenger'),
                     ('agro', 'industrial'), ('quad', 'atv')):
    a = c.get('/browse/tyres/?purpose=' + senas).context['total_count']
    n2 = c.get('/browse/tyres/?purpose=' + nauja).context['total_count']
    tikrink(a == n2, 'sena nuoroda purpose=%s duoda %s, nauja %s duoda %s'
            % (senas, a, nauja, n2))


print('\n' + '═' * 60)
print('gerai: %d, nepavyko: %d' % (gerai, blogai))
sys.exit(1 if blogai else 0)
