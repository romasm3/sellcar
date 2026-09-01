# -*- coding: utf-8 -*-
"""
TELEFONO FILTRŲ PASIRINKIMO EKRANAS — grįžimas į panelę, ne į rezultatus.

Klaida, kurią gaudom: paieškos panelėje telefone pasirinkus bet kurią
reikšmę (pvz. „Kaina nuo 5 000") puslapis nušokdavo tiesiai į skelbimų
sąrašą. Priežastis buvo panel_generic.html: grįžimo adresas
`/?category=<slug>`, o listing_list, pamatęs `category`, peradresuoja į
rezultatus su `?sidebar=1`. Paieška turi startuoti TIK nuo „Skelbimai".

Tikrinam visas kategorijas ir visus jų drill-in laukus.

Paleidimas:  python docs/mob_filtro_pasirinkimas_test.py
Produkcinės DB neliečia — laikina sqlite atmintyje.
"""
import os, sys, django
from django.conf import settings

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
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
        "apps.payments", "apps.analytics", "apps.imones",
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
                'DIRS': [os.path.join(BASE, 'templates')], 'APP_DIRS': True,
                'OPTIONS': {'context_processors': [
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                    'apps.listings.context_processors.search_panel_tab',
                    'apps.listings.context_processors.device_kind',
                ]}}],
)
django.setup()
from django.core.management import call_command
call_command('migrate', run_syncdb=True, verbosity=0)

from urllib.parse import urlparse, parse_qsl, quote
from django.test import RequestFactory
from django.template import Template, Context
from apps.listings.context_processors import search_panel_tab, PANEL_SLUGS, SECTIONS
from apps.listings.search_config import panels as panel_config
from apps.listings import select_views

rf = RequestFactory()
gerai = nesekmes = 0


def tikrink(salyga, ka):
    global gerai, nesekmes
    if salyga:
        gerai += 1
    else:
        nesekmes += 1
        print('  NEPAVYKO: ' + ka)


def antraste(t):
    print('\n── ' + t + ' ' + '─' * max(0, 60 - len(t)))


# ═══ 1. sp_back veda į panelę, ne į rezultatus ═══════════════════════
antraste('1. sp_back adresas')

for adresas, laukiama in [
    ('/', '/?section=cars'),
    ('/?section=cars', '/?section=cars'),
    ('/?section=boats', '/?section=boats'),
    # kategorija adrese (rezultatų puslapis) — grįžimas vis tiek į panelę
    ('/?category=cars&sidebar=1', '/?section=cars'),
    # sekcija kategorijos viduje išlieka
    ('/?section=trucks&sekcija=buses', '/?section=trucks&sekcija=buses'),
    ('/?section=parts&sekcija=moto', '/?section=parts&sekcija=moto'),
    ('/?section=wheels&sekcija=rim', '/?section=wheels&sekcija=rim'),
]:
    ctx = search_panel_tab(rf.get(adresas))
    tikrink(ctx['sp_back'] == laukiama,
            '%s → %s (laukta %s)' % (adresas, ctx['sp_back'], laukiama))

# jau pasirinkti filtrai keliauja kartu — kitaip antras pasirinkimas
# ištrintų pirmą
ctx = search_panel_tab(rf.get('/?section=cars&price_min=5000&brand=7'))
por = dict(parse_qsl(urlparse(ctx['sp_back']).query))
tikrink(por.get('price_min') == '5000' and por.get('brand') == '7',
        'esami filtrai lieka sp_back adrese: ' + ctx['sp_back'])

# puslapiavimas, rikiavimas ir vidiniai jungikliai — nekeliauja
ctx = search_panel_tab(rf.get('/?section=cars&page=3&sort=price&sidebar=1&issaugoti=1'))
tikrink(ctx['sp_back'] == '/?section=cars', 'šiukšlės išvalytos: ' + ctx['sp_back'])

# sp_back NIEKADA neturi „category" — dėl jo listing_list eina į rezultatus
for adresas in ('/', '/?category=cars', '/?category=trucks&subcategory=buses',
                '/?section=motorcycles', '/?category=parts&sidebar=1'):
    back = search_panel_tab(rf.get(adresas))['sp_back']
    tikrink('category=' not in back and 'sidebar=' not in back,
            'sp_back be category/sidebar: %s → %s' % (adresas, back))


# ═══ 2. panel_generic.html nuorodos ══════════════════════════════════
antraste('2. Drill-in nuoroda šablone')

sablonas = Template("{% include 'listings/partials/panel_generic.html' %}")
panele = panel_config.build_panel('cars')
req = rf.get('/?section=cars')
html = sablonas.render(Context({
    'request': req, 'panel': panele, 'count_key': 'cars',
    'adv_url': '/paieska/cars/', **search_panel_tab(req),
}))
# Django |urlencode filtras „/" palieka neužkoduotą
tikrink('grizti=' + quote('/?section=cars', safe='/') in html,
        'nuorodoje grizti=/?section=cars')
tikrink('category' not in html.split('grizti=')[1].split('"')[0],
        'grįžimo adrese nebėra category (buvo /?category=cars)')


# ═══ 3. Kiekvienas laukas kiekvienoje kategorijoje ═══════════════════
antraste('3. Visi laukai, visos kategorijos')


def diapazono_params(cfg):
    """Diapazono laukų parametrai — jie elgiasi kitaip nei vienareikšmiai."""
    out = set()
    for row in cfg.get('rows') or []:
        for f in row or []:
            if f and f.get('type') == 'range':
                out |= {p for p in (f.get('param_min'), f.get('param_max')) if p}
    return out


def drill_laukai(cfg):
    """Laukai, kuriuos telefone renderina _mobile_rows.html."""
    out = []
    for row in cfg.get('rows') or []:
        for f in row or []:
            if not f:
                continue
            if f.get('type') in ('text', 'checkbox') or f.get('db_field') == 'model':
                continue
            if f.get('type') == 'range':
                out += [p for p in (f.get('param_min'), f.get('param_max')) if p]
            elif f.get('param'):
                out.append(f['param'])
    return out


tikrinta = 0
for slug in sorted(panel_config.active_categories()):
    cfg = panel_config.build_panel(slug)
    if not cfg:
        continue
    back = search_panel_tab(rf.get('/?section=' + slug))['sp_back']
    diapazonai = diapazono_params(cfg)
    for param in drill_laukai(cfg):
        atsakymas = select_views.select_value(rf.get(
            '/pasirinkti/', {'laukas': param, 'kategorija': slug,
                             'grizti': back, 'reiksme': '5000'}))
        vieta = atsakymas.get('Location', '')
        tikrink(atsakymas.status_code == 302, '%s/%s: 302' % (slug, param))
        tikrink('category=' not in vieta,
                '%s/%s: grąžina be category= (%s)' % (slug, param, vieta))
        tikrink('sidebar=' not in vieta,
                '%s/%s: grąžina be sidebar= (%s)' % (slug, param, vieta))
        if param in diapazonai:
            # Diapazonas lieka pasirinkimo ekrane (abi ribos vienu ekranu),
            # o reikšmė įrašoma į grįžimo adresą.
            tikrink(vieta.startswith('/pasirinkti/'),
                    '%s/%s: lieka pasirinkimo ekrane (%s)' % (slug, param, vieta))
            grizti = dict(parse_qsl(urlparse(vieta).query)).get('grizti', '')
            tikrink(grizti.startswith('/?section=' + slug),
                    '%s/%s: grįžimas veda į panelę (%s)' % (slug, param, grizti))
            tikrink(param + '=5000' in grizti,
                    '%s/%s: reikšmė grįžimo adrese (%s)' % (slug, param, grizti))
        else:
            tikrink(vieta.startswith('/?section=' + slug),
                    '%s/%s: grįžta į panelę (%s)' % (slug, param, vieta))
            tikrink(param + '=5000' in vieta,
                    '%s/%s: reikšmė adrese (%s)' % (slug, param, vieta))
        tikrinta += 1
print('  patikrinta laukų: %d' % tikrinta)


# ═══ 4. Sekcijos (sunkusis, dalys, ratai, nuoma, statyba) ════════════
antraste('4. Sekcijos kategorijos viduje')

for slug, sekcijos in sorted(SECTIONS.items()):
    for sek in sekcijos:
        adresas = '/?section=%s&sekcija=%s' % (slug, sek)
        back = search_panel_tab(rf.get(adresas))['sp_back']
        cfg = (panel_config.build_panel(slug, sub_slug=sek)
               if sek in panel_config.PANELS_BY_SUB else panel_config.build_panel(slug))
        if not cfg:
            continue
        laukai = drill_laukai(cfg)
        if not laukai:
            continue
        # Kiekvienas sekcijos laukas: constr_attach_type, rent_type ir
        # motorcycle_type pagrindinės kategorijos konfigūracijoje neegzistuoja.
        for param in laukai:
            sub = cfg.get('sub_slug') or ''
            uzklausa = {'laukas': param, 'kategorija': slug,
                        'grizti': back, 'reiksme': '2020'}
            if sub:
                uzklausa['sub'] = sub
            atsakymas = select_views.select_value(rf.get('/pasirinkti/', uzklausa))
            vieta = atsakymas.get('Location', '')
            # Diapazonas lieka pasirinkimo ekrane — panelės adresas guli
            # ?grizti parametre.
            panele = (dict(parse_qsl(urlparse(vieta).query)).get('grizti', '')
                      if vieta.startswith('/pasirinkti/') else vieta)
            tikrink('sekcija=' + sek in panele,
                    '%s/%s/%s: sekcija išlieka (%s)' % (slug, sek, param, panele))
            tikrink('category=' not in panele,
                    '%s/%s/%s: be category= (%s)' % (slug, sek, param, panele))


# ═══ 5. Kaupimas ir perrašymas ═══════════════════════════════════════
antraste('5. Daugybiniai laukai kaupiami, vienareikšmiai perrašomi')

# kaina — vienareikšmė: antras pasirinkimas perrašo
v1 = select_views.select_value(rf.get('/pasirinkti/', {
    'laukas': 'price_min', 'kategorija': 'cars',
    'grizti': '/?section=cars&price_min=1000', 'reiksme': '5000'})).get('Location')
g1 = dict(parse_qsl(urlparse(v1).query)).get('grizti', '')
tikrink(parse_qsl(urlparse(g1).query).count(('price_min', '1000')) == 0
        and ('price_min', '5000') in parse_qsl(urlparse(g1).query),
        'kaina perrašoma: ' + str(g1))

# kuro tipas — daugybinis: antras pasirinkimas pridedamas
cfg = panel_config.build_panel('cars')
daug = None
for row in cfg['rows']:
    for f in row or []:
        if f and f.get('type') == 'multiselect':
            daug = f['param']
            break
    if daug:
        break
if daug:
    v2 = select_views.select_value(rf.get('/pasirinkti/', {
        'laukas': daug, 'kategorija': 'cars',
        'grizti': '/?section=cars&%s=1' % daug, 'reiksme': '2'})).get('Location')
    poros = parse_qsl(urlparse(v2).query)
    tikrink((daug, '1') in poros and (daug, '2') in poros,
            'daugybinis laukas kaupiamas: ' + str(v2))
    # ta pati reikšmė antrą kartą nesidubliuoja
    v3 = select_views.select_value(rf.get('/pasirinkti/', {
        'laukas': daug, 'kategorija': 'cars',
        'grizti': '/?section=cars&%s=1' % daug, 'reiksme': '1'})).get('Location')
    tikrink(parse_qsl(urlparse(v3).query).count((daug, '1')) == 1,
            'ta pati reikšmė nesidubliuoja: ' + str(v3))
else:
    print('  (multiselect lauko cars panelėje nerasta — praleista)')


# ═══ 6. Kelios reikšmės pasiekia „Skelbimai" mygtuką ═════════════════
antraste('6. Kelios to paties lauko reikšmės keliauja su forma')

req = rf.get('/?section=cars&brand=7&brand=9')
html = Template("{% include 'listings/partials/panel_generic.html' %}").render(Context({
    'request': req, 'panel': panel_config.build_panel('cars'),
    'count_key': 'cars', **search_panel_tab(req),
}))
tikrink('<input type="hidden" name="brand" value="7">' in html,
        'ankstesnė markė lieka paslėptu įvedimu')

req = rf.get('/?section=cars&brand=7')
html = Template("{% include 'listings/partials/panel_generic.html' %}").render(Context({
    'request': req, 'panel': panel_config.build_panel('cars'),
    'count_key': 'cars', **search_panel_tab(req),
}))
tikrink('<input type="hidden" name="brand" value="7">' not in html,
        'viena reikšmė papildomų įvedimų nekuria')


# ═══ 7. Sekcijos nuorodoje keliauja ?sub= ════════════════════════════
antraste('7. Sekcijos laukas turi ?sub= nuorodoje')

req = rf.get('/?section=construction&sekcija=construction-attachments')
html = Template("{% include 'listings/partials/panel_generic.html' %}").render(Context({
    'request': req,
    'panel': panel_config.build_panel('construction', sub_slug='construction-attachments'),
    'count_key': 'construction', **search_panel_tab(req),
}))
tikrink('sub=construction-attachments' in html,
        'priedų panelės nuorodose yra ?sub=')


# ═══ 8. Tikras puslapis: panelė atsako 200, rezultatai — 302 ═════════
antraste('8. listing_list: ?section= lieka panelėje, ?category= eina į rezultatus')

from django.test import Client
klientas = Client()

atsakymas = klientas.get('/', {'category': 'cars'})
tikrink(atsakymas.status_code == 302 and 'sidebar=1' in atsakymas.get('Location', ''),
        '?category=cars → rezultatai su sidebar=1 (darbalaukio elgsena nepakito)')

atsakymas = klientas.get('/', {'section': 'cars', 'price_min': '5000'})
tikrink(atsakymas.status_code == 200,
        '?section=cars&price_min=5000 → 200, ne peradresavimas (buvo šuolis į rezultatus)')


# ═══ 9. Diapazonas: eilutė rodo reikšmę, ekrane abi ribos ════════════
antraste('9. Diapazonai (kaina, metai) — etalono „ddvaluedouble"')

import re as _re

def panele_html(qs):
    r = rf.get(qs)
    return Template("{% include 'listings/partials/panel_generic.html' %}").render(Context({
        'request': r, 'panel': panel_config.build_panel('cars'),
        'count_key': 'cars', **search_panel_tab(r)}))


def mob_eilutes(html):
    dalis = html.split('<div class="sp-mlist')[1].split('sp-mfoot-search')[0]
    return [' '.join(_re.sub(r'<[^>]+>', ' ', m).split())
            for m in _re.findall(r'<a class="sp-mrow"[\s\S]*?</a>', dalis)]


# Klaida, dėl kurios viskas prasidėjo: pasirinkus kainą eilutė nerodė nieko
eil = mob_eilutes(panele_html('/?section=cars&price_min=5000'))
tikrink(any('5 000' in e for e in eil), 'eilutė rodo pasirinktą kainą: %s' % eil)
eil = mob_eilutes(panele_html('/?section=cars&price_min=5000&price_max=20000'))
tikrink(any('5 000' in e and '20 000' in e for e in eil),
        'eilutė rodo abi ribas: %s' % eil)
# neformatuotas adreso skaičius eilutėje virsta „5 000", kaip ekrane
tikrink(not any('5000' in e for e in eil), 'skaičius suformatuotas: %s' % eil)
eil = mob_eilutes(panele_html('/?section=cars'))
tikrink(not any(_re.search(r'\d', e) for e in eil),
        'be filtrų eilutėse skaičių nėra: %s' % eil)

# Pasirinkimo ekranas: du stulpeliai, kiekvienas su savo parametru
puslapis = klientas.get('/pasirinkti/', {
    'laukas': 'price_min', 'kategorija': 'cars', 'grizti': '/?section=cars'}).content.decode()
# Ribojam iki pačių stulpelių: toliau puslapyje yra kalbų perjungiklis,
# kurio „next" laukas neša dabartinį adresą (su ?laukas=price_min), ir
# atviras pjūvis iki dokumento galo pagautų būtent jį.
_stulp = puslapis.split('<div class="sp-sheet-cols">')[1].split('sp-sheet-foot')[0]
stulpeliai = _stulp.split('<div class="sp-sheet-col">')[1:]
tikrink(len(stulpeliai) == 2, 'du stulpeliai (rasta %d)' % len(stulpeliai))
if len(stulpeliai) == 2:
    for laukiama, stulpelis in zip(('price_min', 'price_max'), stulpeliai):
        rasta = set(_re.findall(r'laukas=([a-z_]+)', stulpelis))
        tikrink(rasta == {laukiama}, 'stulpelio laukas %s (rasta %s)' % (laukiama, rasta))

# „Nuo" pasirinkimas palieka ekrane, kad „Iki" nereikėtų atidaryti iš naujo
zingsnis = klientas.get('/pasirinkti/', {
    'laukas': 'price_min', 'kategorija': 'cars',
    'grizti': '/?section=cars', 'reiksme': '5000'})
tikrink(zingsnis.status_code == 302 and zingsnis['Location'].startswith('/pasirinkti/'),
        'po „Nuo" liekam ekrane: %s' % zingsnis.get('Location'))

toliau = klientas.get(zingsnis['Location'].replace('laukas=price_min', 'laukas=price_max')
                      + '&reiksme=20000')
galutinis = klientas.get(toliau['Location']).content.decode()
pazymeta = _re.findall(r'is-sel"[\s\S]{0,220}?<span>([^<]*)</span>', galutinis)
tikrink(pazymeta == ['5 000', '20 000'],
        'abi ribos pažymėtos ekrane: %s' % pazymeta)
baigti = _re.search(r'sp-sheet-done" href="([^"]+)"', galutinis)
tikrink(baigti is not None, '„Gerai" mygtukas yra')
if baigti:
    adresas = baigti.group(1).replace('&amp;', '&').split('#')[0]
    tikrink('price_min=5000' in adresas and 'price_max=20000' in adresas,
            '„Gerai" veda į panelę su abiem ribom: %s' % adresas)
    tikrink(klientas.get(adresas).status_code == 200, '„Gerai" adresas atsidaro')

# Skelbimų kiekiai — tik markių sąraše; „(0)" prie kiekvienos kainos
# atrodė, lyg eilutė būtų neaktyvi
for laukas in ('price_min', 'fuel_type'):
    p = klientas.get('/pasirinkti/', {'laukas': laukas, 'kategorija': 'cars',
                                      'grizti': '/?section=cars'}).content.decode()
    tikrink('class="cnt"' not in p, '%s: sąraše nebėra „(0)"' % laukas)


# ═══ 10. Detali paieška telefone — su reikšmių ekranais ══════════════
antraste('10. „Detali paieška" veda į puslapį su drill-in eilutėmis')

# Senasis /search/advanced/ telefone yra darbalaukio tinklelis: paspaudus
# „Kaina" nieko neatsidarydavo. Migruotos kategorijos siunčiamos į
# /paieska/<kategorija>/, kur laukai yra spaudžiamos eilutės.
# Kurios kategorijos turi savo /paieska/ puslapį — imam iš to paties
# šaltinio, kurį naudoja pati nuoroda, kad testas nesentų migruojant
# naujoms kategorijoms.
migruotos = set(panel_config.advanced_categories())
for kat in ('cars', 'trucks', 'boats', 'parts', 'electronics', 'moto-gear'):
    b = klientas.get('/', {'category': kat, 'sidebar': '1'}).content.decode()
    m = _re.search(r'<a href="([^"]*)"\s*\n?\s*class="inline-flex[^"]*"[^>]*>\s*'
                   r'<i class="fas fa-sliders-h"', b)
    nuoroda = m.group(1) if m else ''
    if not nuoroda:
        continue          # ta kategorija peradresuoja kitur (ratai → /browse/wheels/)
    tikrink(('/paieska/' in nuoroda) == (kat in migruotos),
            '%s: „Detali paieška" → %s' % (kat, nuoroda[:60]))

for kat in sorted(migruotos):
    atsakymas = klientas.get('/paieska/%s/' % kat, {'price_min': '5000'})
    turinys = atsakymas.content.decode()
    tikrink(atsakymas.status_code == 200, '/paieska/%s/ atsidaro' % kat)
    tikrink(len(_re.findall(r'<a class="sp-mrow"', turinys)) > 3,
            '/paieska/%s/ turi drill-in eilutes' % kat)
    # Kainos laukas yra ne visose kategorijose (paslaugos jo neturi),
    # todėl tikrinam tik ten, kur konfigūracija jį aprašo.
    adv = panel_config.build_advanced(kat)
    if 'price_min' in drill_laukai(adv or {}):
        tikrink('/pasirinkti/?laukas=price_min' in turinys.replace('&amp;', '&'),
                '/paieska/%s/ kainos eilutė veda į reikšmių ekraną' % kat)

# ir iš ten grįžtama atgal į detalią paiešką, ne į rezultatus
atsakymas = klientas.get('/pasirinkti/', {
    'laukas': 'price_min', 'kategorija': 'cars', 'grizti': '/paieska/cars/',
    'reiksme': '5000'})
grizti = dict(parse_qsl(urlparse(atsakymas['Location']).query)).get('grizti', '')
tikrink(grizti.startswith('/paieska/cars/') and 'price_min=5000' in grizti,
        'iš detalios paieškos grįžtama į ją pačią: %s' % grizti)


print('\n' + '═' * 64)
print('gerai: %d, nepavyko: %d' % (gerai, nesekmes))
sys.exit(1 if nesekmes else 0)
