# -*- coding: utf-8 -*-
"""
VIENA ŠALIS VISAI SVETAINEI.

Šalis nėra atskiras kiekvieno puslapio filtras — tai viena bendra
reikšmė. Šitas testas eina per TIKRUS adresus su tikru Django klientu ir
tikrina, kad pakeitus šalį vienoje vietoje ji pasikeičia visose:

    pakeiti per šoninę juostą  →  atidarai pradžią ir /imones/  →  ta pati

Dar tikrinam:
  * reikšmės sluoksnius: adresas → slapukas → paskyros profilis → lt;
  * kad šalies keitimas neišvalo markės/kainos/metų (tik miestą ir spindulį);
  * kad kode tėra VIENA šalies šablono dalis ir VIENA kiekių funkcija.

Paleidimas:  python docs/viena_salis_test.py
"""
import html as htmlmod
import os, sys, re, shutil, tempfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
os.environ.setdefault('SECRET_KEY', 'x')
os.environ.setdefault('EMAIL_USER', 'x@x.lt')
os.environ.setdefault('EMAIL_PASSWORD', 'x')

import django
from django.conf import settings

# TIKRAS config.settings — tie patys middleware, kontekstiniai procesoriai
# ir adresai kaip produkcijoje; pakeičiam tik duomenų bazę (šitame konteineryje
# psycopg nėra) ir https perjungiklius, kad klientas nešokinėtų per 301.
LAIKINA = tempfile.mkdtemp(prefix='viena-salis-')
import config.settings as pagrindas
nustatymai = {k: v for k, v in vars(pagrindas).items() if k.isupper()}
nustatymai.update(
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3',
                           'NAME': os.path.join(LAIKINA, 'db.sqlite3')}},
    SECURE_SSL_REDIRECT=False, SESSION_COOKIE_SECURE=False,
    CSRF_COOKIE_SECURE=False, SECURE_HSTS_SECONDS=0,
    MEDIA_ROOT=LAIKINA, DEBUG=False, ALLOWED_HOSTS=['*'],
    CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}},
)
settings.configure(**nustatymai)
django.setup()

from django.core.management import call_command
call_command('migrate', run_syncdb=True, verbosity=0)

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client
from django.utils import timezone
from apps.listings import salies_juosta as sj, salys
from apps.listings.models import Brand, Listing, VehicleType

gerai = blogai = 0
def tikrink(s, k):
    global gerai, blogai
    if s: gerai += 1
    else:
        blogai += 1
        print('  NEPAVYKO: ' + k)
def antraste(t):
    print('\n── ' + t + ' ' + '─' * max(0, 56 - len(t)))


# ── Duomenys ────────────────────────────────────────────────────────
U = get_user_model()
u = U.objects.create_user(username='p', email='p@x.lt', password='x')
VT, _ = VehicleType.objects.get_or_create(slug='cars', defaults={'name': 'Automobiliai'})
MARKE, _ = Brand.objects.get_or_create(name='BMW')

def _butini(model):
    out = {}
    for f in model._meta.concrete_fields:
        if (f.primary_key or f.null or f.blank or f.has_default() or f.auto_created
                or getattr(f, 'auto_now', False) or getattr(f, 'auto_now_add', False)):
            continue
        it = f.get_internal_type()
        if it.endswith('IntegerField'): out[f.name] = 0
        elif it in ('DecimalField', 'FloatField'): out[f.name] = 0
        elif it in ('CharField', 'TextField', 'SlugField', 'EmailField', 'URLField'): out[f.name] = ''
        elif it == 'BooleanField': out[f.name] = False
        elif it in ('DateTimeField', 'DateField'): out[f.name] = timezone.now()
    return out

B = _butini(Listing)
KIEK = {'LT': 5, 'DE': 3, 'PL': 2}
sukurti = {}
for kodas, n in KIEK.items():
    for i in range(n):
        d = dict(B)
        d.update(seller=u, vehicle_type=VT, title='%s %d' % (kodas, i),
                 price=5000, year=2018, status='active', country=kodas,
                 brand=MARKE, city='Vilnius' if kodas == 'LT' else 'Berlin')
        sukurti.setdefault(kodas, []).append(Listing.objects.create(**d))

c = Client()
def gauk(kelias):
    cache.clear()
    return c.get(kelias)

def nuoroda(html, kodas):
    """Šalies nuoroda iš HTML. &amp; atgal į & — kitaip klientas gautų
    parametrą „amp;salis" ir pasirinkimas tyliai nesuveiktų."""
    m = re.search(r'href="([^"]*salis=%s[^"]*)"' % kodas, html)
    return htmlmod.unescape(m.group(1)) if m else None


def veliavos_kelias(html, kodas):
    """Ar HTML'e yra tos šalies vėliava. Vardas gali turėti turinio maišą
    (flags/de.e88d88604d65.svg), tad lyginam pagal šabloną."""
    return re.search(r'flags/%s(\.[0-9a-f]{8,12})?\.svg' % kodas, html) is not None

def rodoma_salis(html):
    """Kuri šalis rodoma šablone — iš juostos arba iš šoninės juostos."""
    m = re.search(r'class="salies-vardas">([^<]+)<', html)
    if m:
        return m.group(1).strip()
    # Šoninėje juostoje užrašą valdo Alpine (x-text), tad po klasės gali
    # eiti dar atributų — regexp neturi to laikyti kita struktūra.
    m = re.search(r'class="salis-cur-vardas"[^>]*>([^<]+)<', html)
    return m.group(1).strip() if m else None


antraste('1. Šalies dalis yra tik vienoje vietoje')
saliu_dalys = []
for saknis, _kat, failai in os.walk(os.path.join(BASE, 'templates')):
    for f in failai:
        kelias = os.path.join(saknis, f)
        with open(kelias, encoding='utf-8') as fh:
            t = fh.read()
        # Savas šalių sąrašas šablone atpažįstamas iš ciklo per salies_sarasas
        if '{% for' in t and 'salies_sarasas' in t:
            saliu_dalys.append(os.path.relpath(kelias, BASE))
tikrink(saliu_dalys == ['templates/partials/_salis.html'],
        'sąrašą renderina tik partials/_salis.html, ne %s' % saliu_dalys)

import subprocess
kiekiu_funkcijos = subprocess.run(
    ['grep', '-rn', 'def kiekiai', '--include=*.py', 'apps/'],
    capture_output=True, text=True, cwd=BASE).stdout.split('\n')
kiekiu_funkcijos = [e for e in kiekiu_funkcijos if e.strip()]
tikrink(len(kiekiu_funkcijos) == 1 and 'salies_juosta.py' in kiekiu_funkcijos[0],
        'viena kiekių funkcija: %s' % kiekiu_funkcijos)
procesoriai = [e for e in settings.TEMPLATES[0]['OPTIONS']['context_processors']
               if e.endswith('.salis')]
tikrink(len(procesoriai) == 1, 'vienas kontekstinis procesorius: %s' % procesoriai)


antraste('2. Pakeitus per šoninę juostą — ta pati šalis visur')
# Šoninė juosta rodoma rezultatų režime (?sidebar=1) darbalaukyje;
# pradžios puslapyje jos vietoje — juosta virš paieškos panelės.
REZULTATAI = '/?section=cars&sidebar=1'
sonine = gauk(REZULTATAI)
html = sonine.content.decode()
tikrink(sonine.status_code == 200, 'rezultatai atsidaro (%s)' % sonine.status_code)
tikrink('salis-blk' in html, 'šoninėje juostoje yra šalies blokas')
tikrink(rodoma_salis(html) == 'Lithuania', 'pradžioje — Lithuania (%s)' % rodoma_salis(html))

de_nuoroda = nuoroda(html, 'de')
tikrink(bool(de_nuoroda), 'šoninėje juostoje yra nuoroda į Vokietiją')

# ── PAKEIČIAM per šoninę juostą ──
atsakymas = gauk(de_nuoroda)
tikrink(atsakymas.cookies.get('salis') and atsakymas.cookies['salis'].value == 'DE',
        'paspaudus šoninėje juostoje įrašomas slapukas DE')
tikrink(rodoma_salis(atsakymas.content.decode()) == 'Germany',
        'šoninė juosta rodo Germany')

# Slapukas jau kliente — einam į kitus puslapius NIEKO nenurodydami adrese.
pradzia = gauk('/')
tikrink(rodoma_salis(pradzia.content.decode()) == 'Germany',
        'PRADŽIA rodo Germany (%s)' % rodoma_salis(pradzia.content.decode()))

imones = gauk('/imones/')
tikrink(imones.status_code == 200, '/imones/ atsidaro (%s)' % imones.status_code)
tikrink(rodoma_salis(imones.content.decode()) == 'Germany',
        '/imones/ rodo Germany (%s)' % rodoma_salis(imones.content.decode()))

paieska = gauk('/imones/paieska/')
tikrink(rodoma_salis(paieska.content.decode()) == 'Germany',
        '/imones/paieska/ rodo Germany (%s)' % rodoma_salis(paieska.content.decode()))


antraste('3. Pakeitus per juostą virš panelės — ta pati šalis šoninėje')
c2 = Client()
def gauk2(kelias):
    cache.clear()
    return c2.get(kelias)

pr = gauk2('/')
html = pr.content.decode()
tikrink('salies-juosta' in html, 'pradžioje yra juosta virš panelės')
tikrink(rodoma_salis(html) == 'Lithuania', 'juosta rodo Lithuania')
pl = nuoroda(html, 'pl')
tikrink(bool(pl), 'juostoje yra nuoroda į Lenkiją')
gauk2(pl)
tikrink(rodoma_salis(gauk2(REZULTATAI).content.decode()) == 'Poland',
        'ŠONINĖ JUOSTA rodo Poland')
tikrink(rodoma_salis(gauk2('/imones/').content.decode()) == 'Poland',
        '/imones/ rodo Poland')
tikrink(rodoma_salis(gauk2('/').content.decode()) == 'Poland',
        'pradžia rodo Poland')


antraste('4. Adresas visada laimi slapuką')
su_adresu = gauk2('/?salis=de')
tikrink(rodoma_salis(su_adresu.content.decode()) == 'Germany',
        '?salis=de nugali slapuką PL')


antraste('5. Skelbimų sąrašas tikrai filtruojamas')
c3 = Client()
cache.clear()
r = c3.get('/?section=cars&sidebar=1&salis=de')
turinys = r.content.decode()
tikrink(all(('DE %d' % i) in turinys for i in range(KIEK['DE'])),
        'rodomi visi vokiški skelbimai')
tikrink('LT 0' not in turinys, 'lietuviškų sąraše nėra')
# Pradžios skirtukai („Naujausi", „Populiariausi") — ta pati šalis.
cache.clear()
pr = c3.get('/?salis=lt').content.decode()
tikrink('home-tab-title">LT 0<' in pr, 'skirtukuose yra lietuviškas skelbimas')
tikrink('home-tab-title">DE 0<' not in pr, 'skirtukuose vokiškų nėra')


antraste('6. Šalies keitimas neišvalo kitų filtrų')
cache.clear()
r = c3.get('/?section=cars&sidebar=1&salis=lt&brand=%d&price_min=1000'
           '&year_min=2015&city=Vilnius&spindulys=50' % MARKE.id)
h = r.content.decode()
de = nuoroda(h, 'de')
tikrink(bool(de), 'su filtrais nuoroda į Vokietiją vis tiek yra')
for lieka in ('brand=%d' % MARKE.id, 'price_min=1000', 'year_min=2015'):
    tikrink(lieka in de, '%s lieka: %s' % (lieka, de))
for isvaloma in ('city=', 'spindulys='):
    tikrink(isvaloma not in de, '%s išvaloma: %s' % (isvaloma, de))


antraste('7. Skelbimo šalis — TIK iš kontaktų bloko')
vokiskas = sukurti['DE'][0]
c4 = Client()
cache.clear()
c4.cookies['salis'] = 'LT'          # svetainėje pasirinkta Lietuva
det = c4.get(vokiskas.get_absolute_url())
h = det.content.decode()
tikrink(det.status_code == 200, 'vokiškas skelbimas atsidaro (%s)' % det.status_code)
tikrink(veliavos_kelias(h, 'de'), 'kontaktų bloke — VOKIŠKA vėliava')
tikrink('pard-kita-salis' in h, 'yra tyli eilutė „Šis skelbimas yra …"')
tikrink('Vokietijoje' in h, 'eilutėje vietininkas „Vokietijoje"')
tikrink('salis=de' in h, 'nuoroda „Rodyti visus Vokietijos skelbimus"')

lietuviskas = sukurti['LT'][0]
cache.clear()
h2 = c4.get(lietuviskas.get_absolute_url()).content.decode()
tikrink('pard-kita-salis' not in h2,
        'ta pati šalis — tylios eilutės nėra')
tikrink(veliavos_kelias(h2, 'lt'), 'lietuviška vėliava')


antraste('8. Vėliava — PO pavadinimo')
def po_pavadinimo(html, vardo_klase):
    """Ar <img class="veliava"> eina PO pavadinimo, o ne prieš jį."""
    m = re.search(r'class="%s"[^>]*>[^<]*</span>\s*<img[^>]*class="veliava'
                  % vardo_klase, html)
    return bool(m)

h = gauk(REZULTATAI).content.decode()
tikrink(po_pavadinimo(h, 'salis-cur-vardas'), 'šoninė juosta: vardas → vėliava')
tikrink(po_pavadinimo(h, 'salis-eil-vardas'), 'šoninės juostos eilutė: vardas → vėliava')
h = gauk('/').content.decode()
tikrink(po_pavadinimo(h, 'salies-vardas'), 'juosta virš panelės: vardas → vėliava')
tikrink(po_pavadinimo(h, 'salies-punkto-vardas'), 'juostos eilutė: vardas → vėliava')
tikrink(not re.search(r'<img[^>]*class="veliava[^"]*"[^>]*>\s*<span class="salies-vardas"', h),
        'niekur nėra vėliavos PRIEŠ pavadinimą')


antraste('9. Angliška sąsaja')
cache.clear()
c5 = Client()
h = c5.get('/en/?salis=de').content.decode()
tikrink('All countries' in h, '„Visos šalys" išversta')
tikrink('Visos šalys' not in h, 'lietuviško varianto nebeliko')
tikrink('Change country' in h, '„Keisti šalį" išversta')
cache.clear()
c6 = Client()
c6.cookies['salis'] = 'LT'          # svetainėje Lietuva, skelbimas vokiškas
# get_absolute_url() priklauso nuo AKTYVIOS kalbos (i18n_patterns), o ji
# lieka nuo praeitos užklausos — todėl adresą sudarom aiškiai angliškai.
from django.utils import translation
with translation.override('en'):
    en_adresas = vokiskas.get_absolute_url()
h = c6.get(en_adresas).content.decode()
tikrink('This listing is in Germany' in h,
        'tyli eilutė angliškai, be vietininko')
tikrink('Vokietijoje' not in h, 'lietuviško vietininko angliškame puslapyje nėra')


antraste('10. Profilis — trečias sluoksnis')
from django.test import RequestFactory
rf = RequestFactory()
r = rf.get('/')
r.user = u
if hasattr(u, 'profile'):
    u.profile.country = 'Germany'
    u.profile.save()
    tikrink(sj.pasirinkta(r) == 'DE', 'profilio šalis („Germany") → DE')
    r2 = rf.get('/?salis=pl'); r2.user = u
    tikrink(sj.pasirinkta(r2) == 'PL', 'adresas nugali profilį')
    r3 = rf.get('/'); r3.user = u; r3.COOKIES['salis'] = 'LV'
    tikrink(sj.pasirinkta(r3) == 'LV', 'slapukas nugali profilį')
    u.profile.country = ''
    u.profile.save()
    tikrink(sj.pasirinkta(r) == salys.NUMATYTA, 'tuščias profilis → numatytoji')
else:
    print('  (profilio modelio nėra — praleista)')


shutil.rmtree(LAIKINA, ignore_errors=True)
print('\n' + '═' * 60)
print('gerai: %d, nepavyko: %d' % (gerai, blogai))
sys.exit(1 if blogai else 0)
