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
tikrink(len(turimos) == len(salys.VARDAI),
        'failų tiek pat, kiek šalių (%d / %d)' % (len(turimos), len(salys.VARDAI)))
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
    'templates/partials/_veliava.html',
]
emoji = [f for f in VIETOS_FAILAI
         if re.search(r'[\U0001F1E6-\U0001F1FF]{2}',
                      open(os.path.join(BASE, f), encoding='utf-8').read())]
tikrink(not emoji, 'vietos eilutėse jokių emoji vėliavų (%s)' % emoji)


antraste('3. Dalies išvestis')
h = veliava('LT')
tikrink('<img' in h, 'atiduoda <img>')
tikrink('flags/lt.svg' in h, 'teisingas failas: %s' % h[:90])
tikrink('width="16"' in h and 'height="12"' in h, '16×12')
tikrink('class="veliava"' in h, 'klasė .veliava')
tikrink('alt="Lietuva"' in h and 'title="Lietuva"' in h,
        'alt ir title — pilnas pavadinimas: %s' % h[:120])
tikrink(veliava('de') and 'flags/de.svg' in veliava('de'), 'mažosiomis irgi veikia')
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
    'templates/listings/partials/_card_params.html': 'kortelė sąraše',
    'templates/listings/partials/_zemelapio_burbulas.html': 'žemėlapio burbulas',
    'templates/listings/saved_listings.html': 'išsaugoti skelbimai',
}
for kelias, aprasymas in VIETOS.items():
    t = open(os.path.join(BASE, kelias), encoding='utf-8').read()
    tikrink("partials/_veliava.html" in t, '%s naudoja dalį' % aprasymas)

# Kortelė: formatas „[vėliava] Vilnius, Lietuva"
t = open(os.path.join(BASE, 'templates/listings/partials/_card_params.html'),
         encoding='utf-8').read()
tikrink('get_country_display' in t, 'kortelėje pilnas šalies pavadinimas')

# Žemėlapio burbului duomenys ateina iš korteles.kortele()
k = open(os.path.join(BASE, 'apps/listings/korteles.py'), encoding='utf-8').read()
tikrink("'salis'" in k and "'salies_vardas'" in k,
        'korteles.py paduoda šalį ir pavadinimą burbului')


antraste('6. CSS pagal specifikaciją')
css = open(os.path.join(BASE, 'static/css/style.css'), encoding='utf-8').read()
blokas = css[css.index('.veliava {'):css.index('}', css.index('.veliava {'))]
for reiksme, ka in (('width: 16px', 'plotis 16px'), ('height: 12px', 'aukštis 12px'),
                    ('margin-right: 6px', 'tarpas 6px'),
                    ('border-radius: 2px', 'apvalinimas 2px'),
                    ('rgba(0, 0, 0, .08)', 'rėmelis rgba(0,0,0,.08)')):
    tikrink(reiksme in blokas, 'CSS: %s' % ka)


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
