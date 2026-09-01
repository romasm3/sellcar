# -*- coding: utf-8 -*-
"""
STATINIŲ FAILŲ TALPYKLA.

Gyvoje svetainėje statiniai buvo atiduodami BE Cache-Control — tik su
ETag ir Last-Modified. Tada naršyklė kešuoja euristiškai: pati
nusprendžia, kiek laikyti, ir failo neperklausia. Po dizaino keitimo
lankytojas matydavo seną CSS su nauju HTML, t. y. sulaužytą puslapį, kol
nepaspausdavo Ctrl+Shift+R. Vietiniai testai to nemato iš principo —
127.0.0.1 talpyklos nėra.

Sprendimas — turinio maišas varde (ManifestStaticFilesStorage). Šitas
testas saugo, kad jis liktų įjungtas ir kad niekas jo nesulaužytų:

  * STORAGES['staticfiles'] yra manifesto saugykla;
  * šablonuose nėra kietai įrašytų „/static/…" kelių (išskyrus laiškus,
    kur reikia absoliutaus adreso ir NEsumaišyto vardo);
  * kiekvienas {% static 'x' %} rodo į tikrai esantį failą — su
    manifest_strict trūkstamas failas duoda 500, o ne tylų 404;
  * kelias sudėtas VIENOJE žymėje ({% static 'a/'|add:b %}), nes
    katalogo vardo manifeste nėra.

Paleidimas:  python docs/statiniu_kesas_test.py
"""
import os, re, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
os.environ.setdefault('SECRET_KEY', 'x')
os.environ.setdefault('EMAIL_USER', 'x@x.lt')
os.environ.setdefault('EMAIL_PASSWORD', 'x')

import config.settings as nustatymai

gerai = blogai = 0
def tikrink(s, k):
    global gerai, blogai
    if s: gerai += 1
    else:
        blogai += 1
        print('  NEPAVYKO: ' + k)
def antraste(t):
    print('\n── ' + t + ' ' + '─' * max(0, 56 - len(t)))


antraste('1. Manifesto saugykla įjungta')
sandelis = getattr(nustatymai, 'STORAGES', {}).get('staticfiles', {})
tikrink(sandelis.get('BACKEND', '').endswith('ManifestStaticFilesStorage'),
        'STORAGES[staticfiles] = ManifestStaticFilesStorage (yra %r)'
        % sandelis.get('BACKEND'))


antraste('2. Šablonuose nėra kietai įrašytų /static/ kelių')
# Laiškuose adresas privalo būti absoliutus ir NEsumaišytas: laiškas
# gyvena metus, o senas maišas po kelių deploy'ų nebeegzistuotų.
LAISKAI = ('/emails/', '\\emails\\')
kieti = []
for saknis, _d, failai in os.walk(os.path.join(BASE, 'templates')):
    for f in failai:
        if not f.endswith('.html'):
            continue
        kelias = os.path.join(saknis, f)
        santykinis = os.path.relpath(kelias, BASE)
        for nr, eil in enumerate(open(kelias, encoding='utf-8'), 1):
            if '/static/' in eil and '{% static' not in eil:
                if any(z in kelias for z in LAISKAI):
                    continue
                kieti.append('%s:%d' % (santykinis, nr))
tikrink(not kieti, 'jokių „/static/…" ranka (rasta: %s)' % kieti)


antraste('3. Kiekvienas {% static %} rodo į esantį failą')
STATINIAI = os.path.join(BASE, 'static')
turimi = set()
for saknis, _d, failai in os.walk(STATINIAI):
    for f in failai:
        turimi.add(os.path.relpath(os.path.join(saknis, f), STATINIAI).replace('\\', '/'))
tikrink(len(turimi) > 50, 'static/ rasta %d failų' % len(turimi))

PASTOVUS = re.compile(r"\{%\s*static\s+(['\"])([^'\"]+)\1\s*%\}")
truksta = []
for saknis, _d, failai in os.walk(os.path.join(BASE, 'templates')):
    for f in failai:
        if not f.endswith('.html'):
            continue
        kelias = os.path.join(saknis, f)
        t = open(kelias, encoding='utf-8').read()
        for m in PASTOVUS.finditer(t):
            if m.group(2) not in turimi:
                truksta.append('%s -> %s' % (os.path.relpath(kelias, BASE), m.group(2)))
tikrink(not truksta,
        'visi pastovūs keliai egzistuoja (trūksta: %s)' % truksta)


antraste('4. Kelias sudėtas vienoje žymėje')
# {% static 'a/' %}{{ b }} su manifestu lūžta: „a/" manifeste nėra.
sulipdyti = []
for saknis, _d, failai in os.walk(os.path.join(BASE, 'templates')):
    for f in failai:
        if not f.endswith('.html'):
            continue
        kelias = os.path.join(saknis, f)
        for nr, eil in enumerate(open(kelias, encoding='utf-8'), 1):
            for m in PASTOVUS.finditer(eil):
                # Baigiasi brūkšniu ir iškart po žymės eina kintamasis
                if m.group(2).endswith('/') and eil[m.end():m.end() + 2] == '{{':
                    sulipdyti.append('%s:%d' % (os.path.relpath(kelias, BASE), nr))
tikrink(not sulipdyti,
        '{%% static %%} + {{ kintamasis }} nesulipdyta (rasta: %s)' % sulipdyti)


antraste('5. Nėra kitų talpyklos sluoksnių, apie kuriuos nežinom')
# Service worker kešuoja agresyviau nei naršyklė; jei atsiras, jam
# reikės savo versijavimo (docs/pwa-pasiruosimas.md).
sw = []
for saknis, _d, failai in os.walk(BASE):
    if 'node_modules' in saknis or '/.git' in saknis or '/staticfiles' in saknis:
        continue
    for f in failai:
        if f in ('sw.js', 'service-worker.js', 'serviceworker.js'):
            sw.append(os.path.relpath(os.path.join(saknis, f), BASE))
tikrink(not sw, 'service worker dar neįdiegtas (rasta: %s)' % sw)
registracija = []
for saknis, _d, failai in os.walk(os.path.join(BASE, 'templates')):
    for f in failai:
        if not f.endswith('.html'):
            continue
        t = open(os.path.join(saknis, f), encoding='utf-8').read()
        if 'serviceWorker.register' in t:
            registracija.append(f)
tikrink(not registracija,
        'niekas neregistruoja service worker (rasta: %s)' % registracija)


antraste('6. Nginx taisyklės aprašytos repozitorijoje')
konf = os.path.join(BASE, 'deploy/nginx-statiniai.conf')
tikrink(os.path.exists(konf), 'yra deploy/nginx-statiniai.conf')
if os.path.exists(konf):
    t = open(konf, encoding='utf-8').read()
    tikrink('max-age=31536000, immutable' in t, 'sumaišytiems — metai ir immutable')
    tikrink('[0-9a-f]{8,12}' in t, 'taisyklė pagal maišo šabloną')
    tikrink('must-revalidate' in t, 'nesumaišytiems — privaloma patikra')


antraste('7. Deploy tikrina, ar maišas atsinaujino')
d = open(os.path.join(BASE, 'deploy-agent.sh'), encoding='utf-8').read()
tikrink('staticfiles.json' in d, 'deploy tikrina staticfiles.json')
tikrink('tikrinti_statinius' in d, 'yra statinių patikra')
tikrink('style\\.[a-z0-9]+\\.css' in d or 'style\\.' in d,
        'tikrinamas sumaišytas CSS vardas gyvame HTML')
tikrink(d.index('tikrinti_statinius "$PRIES_MT"') > d.index('apply\n'),
        'patikra vyksta PO collectstatic')


print('\n' + '═' * 60)
print('gerai: %d, nepavyko: %d' % (gerai, blogai))
sys.exit(1 if blogai else 0)
