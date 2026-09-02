# -*- coding: utf-8 -*-
"""
PATVIRTINTI TERMINAI — ar jie tikrai pasiekia vartotoją.

docs/terminai.md yra vienintelis šaltinis. Testas paima kiekvieną jo
eilutę ir per tikrą Django gettext patikrina, ką pamatys rusas ir anglas.

Krenta, jei bent vienas terminas neatitinka lentelės arba jei
patvirtintas vertimas pažymėtas `#, fuzzy` (tokia eilutė į .mo
nekompiliuojama ir vartotojui NERODOMA).

Paleidimas:  python docs/terminai_test.py
"""
import os, sys, tempfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
for k, v in (('SECRET_KEY', 'x'), ('EMAIL_USER', 'x@x.lt'), ('EMAIL_PASSWORD', 'x')):
    os.environ.setdefault(k, v)

import django
from django.conf import settings

LAIKINA = tempfile.mkdtemp(prefix='terminai-')
import config.settings as pagrindas
nustatymai = {k: v for k, v in vars(pagrindas).items() if k.isupper()}
nustatymai.update(
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3',
                           'NAME': os.path.join(LAIKINA, 'db.sqlite3')}},
    SECURE_SSL_REDIRECT=False, DEBUG=False, ALLOWED_HOSTS=['*'],
)
settings.configure(**nustatymai)
django.setup()

import polib
from django.utils import translation

gerai = blogai = 0
def tikrink(s, k):
    global gerai, blogai
    if s: gerai += 1
    else:
        blogai += 1
        print('  NEPAVYKO: ' + k)
def antraste(t):
    print('\n── ' + t + ' ' + '─' * max(0, 52 - len(t)))


def terminai():
    eilutes = []
    for eil in open(os.path.join(BASE, 'docs', 'terminai.md'), encoding='utf-8'):
        eil = eil.strip()
        if not eil.startswith('|') or eil.startswith('|---'):
            continue
        d = [x.strip() for x in eil.strip('|').split('|')]
        if len(d) == 3 and d[0] != 'Lietuviškai':
            eilutes.append(tuple(d))
    return eilutes


T = terminai()
antraste('1. Lentelė perskaitoma')
tikrink(len(T) >= 70, 'terminų per mažai: %d' % len(T))
tikrink(all(all(x) for x in T), 'yra tuščių langelių')

antraste('2. Ką pamato vartotojas')
for kalba, stulpelis in (('ru', 1), ('en', 2)):
    translation.activate(kalba)
    blogi = [(lt, translation.gettext(lt), laukta)
             for lt, ru, en in T
             for laukta in ((ru, en)[stulpelis - 1],)
             if translation.gettext(lt) != laukta]
    tikrink(not blogi, '%s: neatitinka %d — %s' % (kalba, len(blogi), blogi[:3]))
    print('  %s: patikrinta %d, visi sutampa: %s' % (kalba, len(T), not blogi))
translation.activate('lt')
tikrink(all(translation.gettext(lt) == lt for lt, _r, _e in T),
        'lietuviškai terminas pasikeitė (msgid = rodomas tekstas)')

antraste('3. Patvirtinti vertimai NĖRA fuzzy')
raktai = {lt.rstrip(':').lower() for lt, _r, _e in T}
for kalba in ('ru', 'en', 'lt'):
    po = polib.pofile(os.path.join(BASE, 'locale', kalba, 'LC_MESSAGES', 'django.po'))
    fuzzy = [i.msgid for i in po
             if not i.obsolete and i.msgid.rstrip(':').lower() in raktai
             and 'fuzzy' in i.flags]
    tikrink(not fuzzy, '%s: patvirtinti terminai pažymėti fuzzy (nerodomi): %s'
            % (kalba, fuzzy[:5]))

antraste('4. .mo naujesnis arba toks pat kaip .po')
for kalba in ('ru', 'en', 'lt'):
    po = os.path.join(BASE, 'locale', kalba, 'LC_MESSAGES', 'django.po')
    mo = po[:-3] + '.mo'
    tikrink(os.path.exists(mo), '%s: nėra .mo' % kalba)
    tikrink(os.path.getmtime(mo) >= os.path.getmtime(po) - 2,
            '%s: .mo senesnis už .po — vertimai nepasieks svetainės' % kalba)

antraste('5. Terminai užregistruoti makemessages\'ui')
td = open(os.path.join(BASE, 'apps', 'listings', 'translatable_db.py'), encoding='utf-8').read()
truksta = [lt for lt, _r, _e in T if ("_('%s')" % lt.replace("'", "\\'")) not in td]
tikrink(not truksta, 'translatable_db.py netrūksta: %s' % truksta[:5])

print('\n' + '═' * 60)
print('gerai: %d, nepavyko: %d' % (gerai, blogai))
sys.exit(1 if blogai else 0)
