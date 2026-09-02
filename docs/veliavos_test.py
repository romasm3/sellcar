# -*- coding: utf-8 -*-
"""
ŠALIES VĖLIAVĖLĖS prie vietos — docs/taisykles.md 5 taisyklė.

Tikrinam: SVG (ne emoji), viena dalis be kopijų, keturios vietos,
formatas „[vėliava] Vilnius, Lietuva" su IŠVERSTU pilnu pavadinimu, ir
kad be šalies nelieka tuščio kvadrato.

Paleidimas:  python docs/veliavos_test.py
"""
import os, sys, re, django
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
    STATIC_URL='/static/', STATICFILES_DIRS=[os.path.join(BASE, 'static')],
    MEDIA_URL='/media/', MEDIA_ROOT='/tmp/m',
    TEMPLATES=[{'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [os.path.join(BASE, 'templates')], 'APP_DIRS': True,
                'OPTIONS': {'context_processors': [
                    'django.template.context_processors.request']}}],
)
django.setup()

from django.template import Template, Context
from django.utils import translation
from apps.listings import salys

gerai = blogai = 0
def tikrink(s, k):
    global gerai, blogai
    if s: gerai += 1
    else:
        blogai += 1
        print('  NEPAVYKO: ' + k)
def antraste(t):
    print('\n── ' + t + ' ' + '─' * max(0, 56 - len(t)))

VEL = Template("{% include 'partials/_veliava.html' %}")
def veliava(kodas):
    return VEL.render(Context({'kodas': kodas})).strip()


antraste('1. SVG rinkinys — visoms šalims, vienas šaltinis')
katalogas = os.path.join(BASE, 'static', 'flags')
turimos = {f[:-4].lower() for f in os.listdir(katalogas) if f.endswith('.svg')}
truksta = {k.lower() for k in salys.VARDAI} - turimos
tikrink(not truksta, 'visos šalys turi SVG (trūksta: %s)' % sorted(truksta))
# „visos.svg" — gaublys juostos punktui „Visos šalys", ne šalis
tikrink(turimos - {k.lower() for k in salys.VARDAI} == {'visos'},
        'be šalių tik gaublys (%s)' % sorted(turimos - {k.lower() for k in salys.VARDAI}))
for kodas in list(turimos)[:5]:
    turinys = open(os.path.join(katalogas, kodas + '.svg'), encoding='utf-8').read(400)
    tikrink(turinys.lstrip().startswith('<svg') or '<svg' in turinys[:200],
            '%s.svg yra tikras SVG' % kodas)


antraste('2. Viena dalis, jokių kopijų')
tikrink(os.path.exists(os.path.join(BASE, 'templates/partials/_veliava.html')),
        'yra templates/partials/_veliava.html')
kopijos = []
for saknis, _d, failai in os.walk(os.path.join(BASE, 'templates')):
    for f in failai:
        if not f.endswith('.html') or f == '_veliava.html':
            continue
        kelias = os.path.join(saknis, f)
        t = open(kelias, encoding='utf-8').read()
        # Kelias, paminėtas komentare, nėra kopija — tai paaiškinimas,
        # kodėl kalbų vėliavos imamos ne iš static/flags/.
        for sablonas in (r'\{%\s*comment\s*%\}.*?\{%\s*endcomment\s*%\}',
                         r'<!--.*?-->', r'/\*.*?\*/'):
            t = re.sub(sablonas, '', t, flags=re.S)
        if 'flags/' in t:
            kopijos.append(os.path.relpath(kelias, BASE))
tikrink(not kopijos, 'vėliavos kelias minimas tik vienoje dalyje (kopijos: %s)' % kopijos)
# Vietos eilutėse emoji vėliavų būti negali — Windows jų nerodo.
# (Kitur likę trys senos „🇺🇸" antraštėse — ne skelbimo vieta, tad į šią
# taisyklę neįeina; žr. docs/taisykles.md 5.)
VIETOS_FAILAI = [
    'templates/listings/partials/_pardavejo_blokas.html',
    'templates/listings/partials/_card_params.html',
    'templates/listings/partials/_zemelapio_burbulas.html',
    'templates/listings/saved_listings.html',
    'templates/listings/partials/_kort_vieta.html',
    'templates/partials/_veliava.html',
]
emoji = [f for f in VIETOS_FAILAI
         if re.search(r'[\U0001F1E6-\U0001F1FF]{2}',
                      open(os.path.join(BASE, f), encoding='utf-8').read())]
tikrink(not emoji, 'vietos eilutėse jokių emoji vėliavų (%s)' % emoji)


antraste('3. Dalies išvestis')
h = veliava('LT')
tikrink('<img' in h, 'atiduoda <img>')
tikrink(re.search(r'flags/lt(\.[0-9a-f]{8,12})?\.svg', h),
        'teisingas failas: %s' % h[:90])
tikrink('width="16"' in h and 'height="12"' in h, '16×12')
tikrink('class="veliava"' in h, 'klasė .veliava')
tikrink('alt="Lietuva"' in h and 'title="Lietuva"' in h,
        'alt ir title — pilnas pavadinimas: %s' % h[:120])
tikrink(veliava('de') and re.search(r'flags/de(\.[0-9a-f]{8,12})?\.svg',
                                    veliava('de')), 'mažosiomis irgi veikia')
tikrink(veliava('') == '', 'be šalies — nieko (ne tuščias kvadratas)')
tikrink(veliava(None) == '', 'None — nieko')
tikrink(veliava('XX') == '', 'nežinomas kodas — nieko, be klaidos')


antraste('4. Pavadinimas vietos eilutėje — IŠVERSTAS')
with translation.override('lt'):
    tikrink('alt="Vokietija"' in veliava('DE'), 'lt: DE → Vokietija')
with translation.override('en'):
    tikrink('alt="Germany"' in veliava('DE'), 'en: DE → Germany')
# o šalies juostoje virš panelės — angliškas ir NEverčiamas
with translation.override('lt'):
    tikrink(salys.vardas_en('DE') == 'Germany',
            'juostos vardas lieka angliškas ir lietuviškoje sąsajoje')


antraste('5. Keturios vietos')
VIETOS = {
    'templates/listings/partials/_pardavejo_blokas.html': 'kontaktų blokas skelbime',
    'templates/listings/partials/_kort_vieta.html': 'kortelės vietos eilutė',
    'templates/listings/partials/_card_params.html': 'kortelė sąraše',
    'templates/listings/partials/_zemelapio_burbulas.html': 'žemėlapio burbulas',
    'templates/listings/saved_listings.html': 'išsaugoti skelbimai',
}
for kelias, aprasymas in VIETOS.items():
    t = open(os.path.join(BASE, kelias), encoding='utf-8').read()
    tikrink("partials/_veliava.html" in t, '%s naudoja dalį' % aprasymas)

# Kortelė: formatas „Vilnius, Lithuania [vėliava]" — vardas ANGLIŠKAS,
# toks pat kaip darbalaukio kortelėje ir šalies sąrašuose.
t = open(os.path.join(BASE, 'templates/listings/partials/_card_params.html'),
         encoding='utf-8').read()
tikrink('salies_vardas_en' in t, 'kortelėje pilnas angliškas šalies pavadinimas')
tikrink('cp-vieta' in t and '<span>' in t,
        'vietos tekstas atskirame <span> — vėliava nedingsta trumpinant')

# Žemėlapio burbului duomenys ateina iš korteles.kortele()
k = open(os.path.join(BASE, 'apps/listings/korteles.py'), encoding='utf-8').read()
tikrink("'salis'" in k and "'salies_vardas'" in k,
        'korteles.py paduoda šalį ir pavadinimą burbului')

# Kortelės vietos eilutė — viena dalis, be savo <img>, vėliava PO teksto
kv = open(os.path.join(BASE, 'templates/listings/partials/_kort_vieta.html'),
          encoding='utf-8').read()
# Komentaras faile irgi mini <img> ir _veliava.html, todėl tikrinam tik
# tikrą žymėjimą — viską po {% endcomment %}.
kv_zym = kv.split('{% endcomment %}', 1)[1]
tikrink('<img' not in kv_zym, 'kortelės eilutė savo <img> neturi')
tikrink(kv_zym.index('class="txt"') < kv_zym.index('_veliava.html'),
        'vėliava PO teksto, ne prieš')
# SVG matmenys — PAČIOJE žymėje, ne tik CSS (docs/taisykles.md 5)
import re as _re
be_matmenu = [t for t in _re.findall(r'<svg[^>]*>', kv_zym) if 'width=' not in t]
tikrink(not be_matmenu, 'kiekvienas SVG su width/height: %s' % be_matmenu)
tikrink('class="pin"' in kv_zym and 'width="11" height="11"' in kv_zym,
        'smeigtukas 11×11 žymėje')
tikrink('salies_vardas_en' in kv, 'kortelėje angliškas šalies vardas')
naudoja = []
for kelias in ('templates/listings/listing_list.html',):
    t = open(os.path.join(BASE, kelias), encoding='utf-8').read()
    naudoja.append(t.count('_kort_vieta.html'))
tikrink(naudoja[0] >= 6,
        'visos pagrindinio kortelės + rezultatai naudoja dalį (%d)' % naudoja[0])


antraste('6. CSS pagal specifikaciją')
css = open(os.path.join(BASE, 'static/css/style.css'), encoding='utf-8').read()
blokas = css[css.index('.veliava {'):css.index('}', css.index('.veliava {'))]
for reiksme, ka in (('width: 16px', 'plotis 16px'), ('height: 12px', 'aukštis 12px'),
                    ('margin-left: 6px', 'tarpas 6px (vėliava gale)'),
                    ('border-radius: 2px', 'apvalinimas 2px'),
                    # Rėmelis — outline su neigiamu offset'u, ne border:
                    # 16×12 turi likti tikslūs (etalonas naudoja
                    # box-shadow inset, bet ten <svg>, o pas mus <img>).
                    ('outline: 1px solid rgba(0, 0, 0, .10)',
                     'rėmelis 1px rgba(0,0,0,.10)'),
                    ('outline-offset: -1px', 'rėmelis viduje, matmenų nekeičia')):
    tikrink(reiksme in blokas, 'CSS: %s' % ka)


antraste('6b. Vietos eilutės stilius — bendrame faile')
css = open(os.path.join(BASE, 'static/css/style.css'), encoding='utf-8').read()
for zyma in ('.vieta {', '.vieta .pin', '.vieta .txt', '.vieta-zalia',
             '.vieta-eilute'):
    tikrink(zyma in css, 'static/css/style.css turi %s' % zyma)
ll = open(os.path.join(BASE, 'templates/listings/listing_list.html'),
          encoding='utf-8').read()
stiliai = ll[:ll.index('</style>')] if '<style>' in ll else ''
tikrink('.vieta' not in stiliai,
        'listing_list.html <style> bloke vietos taisyklių nėra')


antraste('7. Taisyklės įrašytos')
for kelias, zyma in (
        ('docs/taisykles.md', 'VIETA YRA SVARBIAUSIAS FILTRAS'),
        ('.claude/skills/nauja-kategorija/SKILL.md', 'NUOLATINĖS TAISYKLĖS'),
        ('CLAUDE.md', 'docs/taisykles.md')):
    t = open(os.path.join(BASE, kelias), encoding='utf-8').read()
    tikrink(zyma in t, '%s turi taisykles' % kelias)
taisykles = open(os.path.join(BASE, 'docs/taisykles.md'), encoding='utf-8').read()
for punktas in ('šalis → miestas → spindulys', 'contact_block.html',
                '_veliava.html', 'Kaip nuvažiuoti', 'įmonėms ir meistrams',
                'SVG', '16×12'):
    tikrink(punktas in taisykles, 'taisyklėse yra „%s"' % punktas)


print('\n' + '═' * 60)
print('gerai: %d, nepavyko: %d' % (gerai, blogai))
sys.exit(1 if blogai else 0)
