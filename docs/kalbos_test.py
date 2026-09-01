# -*- coding: utf-8 -*-
"""
KALBOS — perjungiklyje matomos visos, kurioms yra .po failas.

Kalbų sąrašas 8dd8851 buvo apkarpytas nuo 13 iki 2 (kartu su
i18n_patterns). Failai locale/ liko, tad grąžinimas — viena eilutė
settings.py. Šis testas saugo, kad sąrašas ir failai nebeišsiskirtų.

Paleidimas:  python docs/kalbos_test.py
"""
import io, os, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
# Tikrinam TIKRĄ config/settings.py, bet jo NEIMPORTUOJAM: modulis
# traukia decouple, DB ir kitą aplinką, o mums reikia tik dviejų
# konstantų. Nuskaitom jas iš teksto per ast — be jokių šalutinių
# poveikių ir be paruoštos aplinkos.
import ast, polib

class Nustatymai:
    pass

modulis = Nustatymai()
medis = ast.parse(io.open(os.path.join(BASE, 'config', 'settings.py'),
                          encoding='utf-8').read())
def _reiksme(mazgas):
    """Kalbos pavadinimas: paprasta eilutė arba _( 'x' ) — grąžinam msgid."""
    if isinstance(mazgas, ast.Constant):
        return mazgas.value, False
    if isinstance(mazgas, ast.Call) and mazgas.args:
        vidus = mazgas.args[0]
        if isinstance(vidus, ast.Constant):
            return vidus.value, True
    return None, False

for mazgas in medis.body:
    if not isinstance(mazgas, ast.Assign):
        continue
    vardai = [t.id for t in mazgas.targets if isinstance(t, ast.Name)]
    if 'LANGUAGE_CODE' in vardai:
        modulis.LANGUAGE_CODE = ast.literal_eval(mazgas.value)
    elif 'LANGUAGES' in vardai:
        # literal_eval netinka: pavadinimai apvynioti gettext'u
        modulis.LANGUAGES = []
        modulis.PER_GETTEXT = []
        for el in mazgas.value.elts:
            kodas = ast.literal_eval(el.elts[0])
            vardas, per_gettext = _reiksme(el.elts[1])
            modulis.LANGUAGES.append((kodas, vardas))
            modulis.PER_GETTEXT.append(per_gettext)

gerai = blogai = 0
def tikrink(salyga, ka):
    global gerai, blogai
    if salyga: gerai += 1
    else:
        blogai += 1
        print('  NEPAVYKO: ' + ka)

def antraste(t):
    print('\n── ' + t + ' ' + '─' * max(0, 56 - len(t)))


LANGUAGES = modulis.LANGUAGES
kodai = [k for k, _v in LANGUAGES]

antraste('1. Sąrašas atkurtas')
LAUKIAMI = ['lt', 'en', 'lv', 'et', 'pl', 'de', 'ru', 'fr', 'es',
            'zh-hans', 'vi', 'ar', 'ko']
tikrink(len(LANGUAGES) == 13, 'kalbų 13 (rasta %d)' % len(LANGUAGES))
for k in LAUKIAMI:
    tikrink(k in kodai, 'sąraše yra %r' % k)
tikrink(kodai[0] == modulis.LANGUAGE_CODE == 'lt',
        'lt pirma ir numatytoji (%r, %r)' % (kodai[0], modulis.LANGUAGE_CODE))
tikrink(len(set(kodai)) == len(kodai), 'be dublikatų')

antraste('2. Kiekviena kalba turi savo .po ir .mo')
def katalogas(kodas):
    # Django kodą „zh-hans" atitinka katalogas „zh_Hans"
    if '-' in kodas:
        a, b = kodas.split('-', 1)
        return '%s_%s' % (a, b.capitalize())
    return kodas

for kodas in kodai:
    d = os.path.join(BASE, 'locale', katalogas(kodas), 'LC_MESSAGES')
    tikrink(os.path.exists(os.path.join(d, 'django.po')),
            '%s: yra django.po (%s)' % (kodas, katalogas(kodas)))
    tikrink(os.path.exists(os.path.join(d, 'django.mo')),
            '%s: yra django.mo (%s)' % (kodas, katalogas(kodas)))

antraste('3. .mo atitinka .po (compilemessages nieko nepakeistų)')
for kodas in kodai:
    d = os.path.join(BASE, 'locale', katalogas(kodas), 'LC_MESSAGES')
    po = polib.pofile(os.path.join(d, 'django.po'))
    mo = {e.msgid: e.msgstr for e in polib.mofile(os.path.join(d, 'django.mo'))
          if e.msgstr}
    # msgfmt „fuzzy" įrašų į .mo nededa — jie ne trūkumas
    laukiama = {e.msgid: e.msgstr for e in po
                if e.msgstr and not e.obsolete and 'fuzzy' not in e.flags}
    truksta = [k for k, v in laukiama.items() if mo.get(k) != v]
    tikrink(not truksta,
            '%s: .mo neturi %d .po vertimų (pvz. %r)' %
            (kodas, len(truksta), truksta[:1]))

antraste('4. Nė vienas locale/ katalogas nepamirštas')
esami = {d for d in os.listdir(os.path.join(BASE, 'locale'))
         if os.path.isdir(os.path.join(BASE, 'locale', d))}
sarase = {katalogas(k) for k in kodai}
tikrink(esami == sarase,
        'locale/ ir LANGUAGES sutampa (tik locale/: %s; tik sąraše: %s)'
        % (sorted(esami - sarase), sorted(sarase - esami)))

antraste('5. Pavadinimai eina per gettext')
# LANGUAGES nuskaitytas per ast.literal_eval, o _( ) jam netinka — jei
# reikšmė None, vadinasi pavadinimai TIKRAI apvynioti gettext'u.
tekstas = io.open(os.path.join(BASE, 'config', 'settings.py'), encoding='utf-8').read()
blokas = tekstas[tekstas.index('LANGUAGES = ['):tekstas.index(']', tekstas.index('LANGUAGES = ['))]
tikrink(blokas.count('_(') == 13,
        'visi 13 pavadinimų apvynioti _( ) (rasta %d)' % blokas.count('_('))
tikrink('gettext_lazy as _' in tekstas, 'settings.py importuoja gettext_lazy as _')
# Angliškame puslapyje pavadinimai privalo likti angliški — to reikalauja
# vertimų sargyba (apps/imones/tests.py). Native pavadinimai („Lietuvių",
# „Latviešu") ją griovė, todėl msgid'ai angliški.
for vardas in ('Lithuanian', 'Latvian', 'Russian', 'Chinese', 'Korean'):
    tikrink('_("%s")' % vardas in blokas, 'msgid angliškas: %r' % vardas)

antraste('6. Perjungiklis šablone renderina visas')
tikrink('get_available_languages' in
        open(os.path.join(BASE, 'templates/base.html'), encoding='utf-8').read(),
        'base.html ima kalbas per {% get_available_languages %}')
tikrink('django.template.context_processors.i18n' in
        open(os.path.join(BASE, 'config/settings.py'), encoding='utf-8').read(),
        'i18n kontekstinis procesorius įjungtas (imones/sarasas.html ima LANGUAGES iš jo)')

antraste('7. Gyvai: perjungiklis ir adresai (jei aplinka paruošta)')
try:
    for raktas, reiksme in (('SECRET_KEY', 'x'), ('EMAIL_USER', 'x@x.lt'),
                            ('EMAIL_PASSWORD', 'x')):
        os.environ.setdefault(raktas, reiksme)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
    import django
    from django.conf import settings as gyvi
    gyvi.DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3',
                                 'NAME': ':memory:'}
    django.setup()
except Exception as klaida:
    print('  praleista — aplinka neparuošta (%s: %s)'
          % (type(klaida).__name__, str(klaida)[:60]))
else:
    from django.template import Template, Context
    from django.urls import resolve
    from django.utils import translation

    eilutes = Template('{% load i18n %}{% get_available_languages as LANGUAGES %}'
                       '{% for k,v in LANGUAGES %}{{ k }};{% endfor %}'
                       ).render(Context({})).strip(';').split(';')
    tikrink(sorted(eilutes) == sorted(kodai),
            'perjungiklis rodo visas %d kalbas (rodo %d)' % (len(kodai), len(eilutes)))

    # i18n_patterns priešdėlį lygina su AKTYVIA kalba, todėl kiekvieną
    # tikrinam jos pačios kontekste — taip pat, kaip po set_language.
    for kodas in kodai:
        with translation.override(kodas):
            kelias = '/imones/' if kodas == 'lt' else '/%s/imones/' % kodas
            try:
                rastas = resolve(kelias).view_name
            except Exception:
                rastas = None
            tikrink(rastas == 'imones:sarasas', '%s: %s veikia' % (kodas, kelias))

    with translation.override('lt'):
        try:
            resolve('/lt/imones/')
            rasta = True
        except Exception:
            rasta = False
        tikrink(not rasta, '/lt/imones/ lieka 404 (lt be priešdėlio)')

    # Pavadinimai perjungiklyje: lt puslapyje lietuviški, en — angliški
    for kalba, kodas, laukiama in (('lt', 'lv', 'Latviešu'),
                                   ('lt', 'pl', 'Lenkų'),
                                   ('en', 'lv', 'Latvian'),
                                   ('en', 'ru', 'Russian')):
        with translation.override(kalba):
            gauta = str(dict(gyvi.LANGUAGES)[kodas])
        tikrink(gauta == laukiama,
                '%s puslapyje %s → %r (laukta %r)' % (kalba, kodas, gauta, laukiama))

    # Vertimai tikrai užsikrauna — ne tik failai guli
    for kodas, laukiama in (('ru', 'Объявления'), ('de', 'Anzeigen'),
                            ('lv', 'Sludinājumi'), ('ko', '매물')):
        with translation.override(kodas):
            gauta = translation.gettext('Skelbimai')
        tikrink(gauta == laukiama,
                '%s: „Skelbimai" → %r (laukta %r)' % (kodas, gauta, laukiama))


antraste('8. Perjungiklis telefone — viena bendra dalis')
dalis = os.path.join(BASE, 'templates/partials/_kalbos.html')
tikrink(os.path.exists(dalis), 'yra templates/partials/_kalbos.html')
turinys = io.open(dalis, encoding='utf-8').read() if os.path.exists(dalis) else ''
for stilius in ('sarasas', 'iskleidziamas', 'porastes'):
    tikrink("'%s'" % stilius in turinys, 'dalis moka stilių %r' % stilius)
tikrink('request.get_full_path' in turinys,
        'perjungimas grįžta į tą patį adresą su GET parametrais')
tikrink("{% url 'set_language' %}" in turinys, 'naudojamas django set_language')

baze = io.open(os.path.join(BASE, 'templates/base.html'), encoding='utf-8').read()
# Keturios vietos, viena dalis: darbalaukio iškrentantis sąrašas,
# telefono apatinis lakštas, mėsainio meniu ir poraštė.
tikrink(baze.count("include 'partials/_kalbos.html'") == 4,
        'base.html įtraukia dalį 4 vietose (rasta %d)'
        % baze.count("include 'partials/_kalbos.html'"))
for stilius in ("stilius='iskleidziamas'", "stilius='sarasas'", "stilius='porastes'"):
    tikrink(stilius in baze, 'base.html naudoja %s' % stilius)
for klase in ('kalbos-mygtukas', 'kalbos-lakstas', 'mm-kalbos', 'kalbos-porastes'):
    tikrink(klase in baze, 'base.html turi .%s' % klase)

# Senoji 13 šakų vėliavų grandinė turi būti dingusi — dėl jos pridėjus
# kalbą reikėdavo taisyti penkias vietas.
tikrink("CURRENT_LANG == 'zh-hans' %}cn" not in baze,
        'base.html nebeliko nukopijuotos vėliavų grandinės')
tikrink('mm-flag' not in baze, 'senas kodų ženkleliu blokas pašalintas')

from apps.listings.templatetags.kalbu_tags import veliavos_kodas, kalbos_pavadinimas, VELIAVOS
for kodas, veliava in (('en', 'us'), ('et', 'ee'), ('zh-hans', 'cn'),
                       ('vi', 'vn'), ('ar', 'sa'), ('ko', 'kr'), ('lt', 'lt')):
    tikrink(veliavos_kodas(kodas) == veliava,
            'vėliava %s → %s (gauta %s)' % (kodas, veliava, veliavos_kodas(kodas)))
tikrink(set(VELIAVOS) == set(kodai), 'vėliavos aprašytos visoms kalboms')
tikrink(kalbos_pavadinimas('ru') == 'Русский', 'ru → Русский')
tikrink(kalbos_pavadinimas('nezinoma', 'Atsarginis') == 'Atsarginis', 'nežinomai — atsarginis')


print('\n' + '═' * 60)
print('gerai: %d, nepavyko: %d' % (gerai, blogai))
sys.exit(1 if blogai else 0)
