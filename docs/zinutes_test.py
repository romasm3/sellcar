# -*- coding: utf-8 -*-
"""
ŽINUTĖS — serverio pusė.

Tikrina tai, ko naršyklėje nepamatysi:
  * el. paštas NIEKADA nepatenka į rodomą vardą (net kai username yra
    el. paštas — taip jis kuriamas registruojantis);
  * /conversations/check-new/ grąžina naujas žinutes po nurodyto id ir
    pažymi jas perskaitytomis;
  * vertimo klaida grąžinama kaip klaida, o ne kaip originalus tekstas.

Paleidimas:  python docs/zinutes_test.py
"""
import os, sys, tempfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
for k, v in (('SECRET_KEY', 'x'), ('EMAIL_USER', 'x@x.lt'), ('EMAIL_PASSWORD', 'x')):
    os.environ.setdefault(k, v)

import django
from django.conf import settings

LAIKINA = tempfile.mkdtemp(prefix='zinutes-')
import config.settings as pagrindas
nustatymai = {k: v for k, v in vars(pagrindas).items() if k.isupper()}
nustatymai.update(
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3',
                           'NAME': os.path.join(LAIKINA, 'db.sqlite3')}},
    SECURE_SSL_REDIRECT=False, SESSION_COOKIE_SECURE=False,
    CSRF_COOKIE_SECURE=False, SECURE_HSTS_SECONDS=0,
    MEDIA_ROOT=LAIKINA, DEBUG=False, ALLOWED_HOSTS=['*'],
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}},
    STORAGES={'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
              'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'}},
)
settings.configure(**nustatymai)
django.setup()

from django.core.management import call_command
call_command('migrate', run_syncdb=True, verbosity=0)

import json
from django.contrib.auth import get_user_model
from django.test import Client
from apps.conversations.models import Conversation, Message
from apps.conversations.templatetags.pokalbiu_tags import vardas, vardo_raide

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
# Registruojantis username = el. paštas (accounts/forms.py) — atkuriam tiksliai
a = U.objects.create_user(username='pirkejas@x.lt', email='pirkejas@x.lt', password='x')
b = U.objects.create_user(username='pardavejas@x.lt', email='pardavejas@x.lt', password='x')

def lietuviskai(u):
    """accounts.middleware.UserLanguageMiddleware prisijungusiam taiko
    PROFILIO kalbą, o ne Accept-Language. Be šito adresai nueina į /en/
    ir testas gauna 404."""
    p = getattr(u, 'profile', None)
    if p is not None:
        p.language = 'lt'
        p.save(update_fields=['language'])
lietuviskai(a); lietuviskai(b)


antraste('1. Vardas vietoj el. pašto')
tikrink('@' not in vardas(a), 'be vardo grąžinamas el. paštas: %r' % vardas(a))
tikrink(str(a.pk) in vardas(a), 'be vardo nerodomas paskyros numeris: %r' % vardas(a))
tikrink(vardo_raide(a) == 'N', 'avataro raidė ne iš vardo: %r' % vardo_raide(a))

a.first_name, a.last_name = 'Tomas', 'Petraitis'
a.save()
tikrink(vardas(a) == 'Tomas Petraitis', 'nerodomas tikras vardas: %r' % vardas(a))
tikrink(vardo_raide(a) == 'T', 'avataro raidė ne iš vardo: %r' % vardo_raide(a))
tikrink('@' not in vardas(None) and vardas(None), 'be vartotojo nulūžta')


antraste('2. Šablonuose nebeliko el. pašto')
import re
blogos = []
for f in ('conversation_list.html', 'conversation_detail.html'):
    kelias = os.path.join(BASE, 'templates', 'conversations', f)
    t = open(kelias, encoding='utf-8').read()
    for m in re.finditer(r'\{\{[^}]*\.email[^}]*\}\}', t):
        blogos.append('%s: %s' % (f, m.group(0)))
for saknis, _k, failai in os.walk(os.path.join(BASE, 'templates', 'conversations')):
    for f in failai:
        t = open(os.path.join(saknis, f), encoding='utf-8').read()
        for m in re.finditer(r'\{\{[^}]*\.email[^}]*\}\}', t):
            blogos.append('%s: %s' % (f, m.group(0)))
tikrink(not blogos, 'el. paštas šablonuose: %s' % blogos)


antraste('3. check-new grąžina žinutes, ne tik skaičių')
c = Conversation.objects.create(listing=None)
c.participants.add(a, b)
m1 = Message.objects.create(conversation=c, sender=a, content='Pirma')
m2 = Message.objects.create(conversation=c, sender=a, content='Antra')

# LT — be kalbos priešdėlio (i18n_patterns prefix_default_language=False).
# Be šito antraštės klientas nueina į „en" ir gauna 404.
kl = Client(HTTP_ACCEPT_LANGUAGE='lt')
kl.force_login(b)
r = kl.get('/conversations/check-new/?conv=%s&po=%s' % (c.pk, m1.pk))
tikrink(r.status_code == 200, 'check-new atsakė %s (%s)'
        % (r.status_code, r.get('Location', r.content[:120])))
d = json.loads(r.content) if r.status_code == 200 else {'zinutes': [], 'unread_count': 0}
tikrink('zinutes' in d, 'atsakyme nėra „zinutes" lauko')
tikrink([z['id'] for z in d['zinutes']] == [m2.pk],
        'grąžintos ne tos žinutės: %s' % d.get('zinutes'))
pirma = (d.get('zinutes') or [{}])[0]
tikrink(pirma.get('tekstas') == 'Antra', 'neatiduodamas tekstas')
tikrink(pirma.get('mano') is False, 'svetima žinutė pažymėta kaip sava')
tikrink(bool(pirma.get('diena')), 'nėra datos skirtuko užrašo')
m2.refresh_from_db()
tikrink(m2.is_read, 'atiduota žinutė nepažymėta perskaityta')

r2 = kl.get('/conversations/check-new/?conv=%s&po=%s' % (c.pk, m2.pk))
tikrink(json.loads(r2.content)['zinutes'] == [], 'tos pačios žinutės grąžinamos antrą kartą')

r3 = kl.get('/conversations/check-new/')
tikrink('unread_count' in json.loads(r3.content), 'be conv nebegrąžinamas skaitiklis')

# Svetimo pokalbio pamatyti negalima
sveti = Conversation.objects.create(listing=None)
c2a = U.objects.create_user(username='c@x.lt', email='c@x.lt', password='x')
c2b = U.objects.create_user(username='d@x.lt', email='d@x.lt', password='x')
sveti.participants.add(c2a, c2b)
Message.objects.create(conversation=sveti, sender=c2a, content='Slapta')
r4 = kl.get('/conversations/check-new/?conv=%s&po=0' % sveti.pk)
tikrink(json.loads(r4.content)['zinutes'] == [], 'atiduodamas svetimas pokalbis!')


antraste('4. Šablonuose nebeliko location.reload()')
def be_komentaru(t):
    """Šablonas be {% comment %} blokų — kad paminėjimas paaiškinime
    nebūtų palaikytas tikru kvietimu."""
    return re.sub(r'\{%\s*comment\s*%\}.*?\{%\s*endcomment\s*%\}', '', t, flags=re.S)

blogos = []
for saknis, _k, failai in os.walk(os.path.join(BASE, 'templates', 'conversations')):
    for f in failai:
        t = be_komentaru(open(os.path.join(saknis, f), encoding='utf-8').read())
        if 'location.reload' in t:
            blogos.append(f)
tikrink(not blogos, 'liko location.reload(): %s' % blogos)


antraste('5. Vertimas — logika kaip buvo, klaida nekabo')
# Vertimo servisas 2026-09-02 ATSUKTAS į buvusią būseną (vartotojo
# sprendimas): jis pats susitvarko su API klaidomis. Čia tikrinam tik tai,
# kad neatsakius paslaugai atsakymas BŪTŲ, o ne amžinas „Verčiama…".
SERVISAS = os.path.join(BASE, 'apps', 'conversations', 'translate_service.py')
tikrink('Failsafe' in open(SERVISAS, encoding='utf-8').read(),
        'servisas nebe toks, koks buvo (dingo failsafe)')

# google-cloud-translate šitame konteineryje neįdiegtas — pakišam tuščią
# modulį, kad būtų galima patikrinti PATĮ KELIĄ, o ne biblioteką.
import types
if 'google.cloud.translate_v2' not in sys.modules:
    g = types.ModuleType('google'); g.__path__ = []
    gc = types.ModuleType('google.cloud'); gc.__path__ = []
    tv = types.ModuleType('google.cloud.translate_v2')
    tv.Client = lambda *a, **k: None
    gc.translate_v2 = tv; g.cloud = gc
    sys.modules.setdefault('google', g)
    sys.modules.setdefault('google.cloud', gc)
    sys.modules['google.cloud.translate_v2'] = tv

import apps.conversations.translate_service as ts
kl2 = Client(HTTP_ACCEPT_LANGUAGE='lt')
kl2.force_login(a)
Message.objects.create(conversation=c, sender=a, content='Labas')
orig = ts.translate_messages_for_user

def sprogsta(*args, **kw):
    raise RuntimeError('API nepasiekiamas')
ts.translate_messages_for_user = sprogsta
try:
    r6 = kl2.get('/conversations/%s/translate/' % c.pk)
    tikrink(r6.status_code == 500, 'neatsakius vertimui grąžinamas %s' % r6.status_code)
    d6 = json.loads(r6.content)
    tikrink(d6.get('success') is False, 'klaida praneša apie sėkmę — sąsaja liktų kaboti')
    tikrink(d6.get('error_type') == 'RuntimeError',
            'atsakyme nėra klaidos tipo — nematyti, KUR problema: %r' % d6.get('error_type'))
finally:
    ts.translate_messages_for_user = orig

# Sąsajoje turi būti ir laiko riba, ir klaidos užrašas
JS = os.path.join(BASE, 'templates', 'conversations', 'partials', '_pokalbio_js.html')
js = open(JS, encoding='utf-8').read()
tikrink('Nepavyko išversti' in js, 'sąsaja nerodo „Nepavyko išversti"')
tikrink('setTimeout' in js and 'abort' in js, 'nėra laiko ribos — „Verčiama…" gali kaboti')


antraste('6. Negyvo paketo nebėra, admin užregistruotas')
tikrink(not os.path.exists(os.path.join(BASE, 'apps', 'conversations', 'conversations')),
        'apps/conversations/conversations/ vis dar yra')
from django.contrib import admin as dj_admin
tikrink(Conversation in dj_admin.site._registry, 'Conversation neregistruotas admin\'e')
tikrink(Message in dj_admin.site._registry, 'Message neregistruotas admin\'e')


antraste('7. Vertimas — jungiklis, ne vienkartinis veiksmas')
from apps.conversations.models import ConversationTranslation

# Pakišam veikiantį „Google" — tikrinam elgseną, ne biblioteką.
def netikras(messages, target_lang='en'):
    return [{'id': m.id, 'original': m.content,
             'translated': '[%s] %s' % (target_lang, m.content),
             'detected': 'lt', 'klaida': False} for m in messages]

import apps.conversations.views as V
orig_v = ts.translate_messages_for_user
ts.translate_messages_for_user = netikras
try:
    mano = Message.objects.create(conversation=c, sender=b, content='Mano tekstas')
    svetima = Message.objects.create(conversation=c, sender=a, content='Svetimas tekstas')

    tikrink(not ConversationTranslation.ijungta(b, c), 'iš pradžių turi būti išjungta')

    r7 = kl.post('/conversations/%s/translate/toggle/' % c.pk, {'ijungti': '1'})
    d7 = json.loads(r7.content)
    tikrink(r7.status_code == 200 and d7.get('ijungta') is True,
            'jungiklis neįsijungė: %s' % r7.status_code)
    tikrink(ConversationTranslation.ijungta(b, c), 'būsena neišsaugota serveryje')
    tikrink(str(svetima.pk) in d7.get('vertimai', {}),
            'įjungus negrąžinti esamų žinučių vertimai')
    tikrink(str(mano.pk) not in d7.get('vertimai', {}),
            'verčiamas SAVO tekstas — turi likti originalus')

    # Nauja žinutė ateina jau išversta
    nauja = Message.objects.create(conversation=c, sender=a, content='Nauja svetima')
    r8 = kl.get('/conversations/check-new/?conv=%s&po=%s' % (c.pk, svetima.pk))
    z = {x['id']: x for x in json.loads(r8.content)['zinutes']}
    tikrink(z.get(nauja.pk, {}).get('vertimas', '').startswith('['),
            'nauja žinutė ateina neišversta, nors jungiklis įjungtas')

    mano2 = Message.objects.create(conversation=c, sender=b, content='Vėl mano')
    r9 = kl.get('/conversations/check-new/?conv=%s&po=%s' % (c.pk, nauja.pk))
    z2 = {x['id']: x for x in json.loads(r9.content)['zinutes']}
    tikrink(not z2.get(mano2.pk, {}).get('vertimas'),
            'sava nauja žinutė verčiama')

    # Klaida — jungiklis lieka įjungtas
    def su_klaida(messages, target_lang='en'):
        return [{'id': m.id, 'original': m.content, 'translated': m.content,
                 'detected': '', 'klaida': True} for m in messages]
    ts.translate_messages_for_user = su_klaida
    v = V._vertimai([svetima], b)
    tikrink(v.get(svetima.pk, {}).get('klaida') is True,
            'nepavykęs vertimas nepažymimas — sąsaja neparodys „Nepavyko išversti"')
    tikrink(ConversationTranslation.ijungta(b, c), 'po klaidos jungiklis išsijungė')
    ts.translate_messages_for_user = netikras

    r10 = kl.post('/conversations/%s/translate/toggle/' % c.pk, {'ijungti': '0'})
    tikrink(json.loads(r10.content).get('ijungta') is False, 'jungiklis neišsijungė')
    tikrink(not ConversationTranslation.ijungta(b, c), 'išjungta būsena neišsaugota')

    # Svetimo pokalbio jungiklio pasiekti negalima
    r11 = kl.post('/conversations/%s/translate/toggle/' % sveti.pk, {'ijungti': '1'})
    tikrink(r11.status_code == 404, 'svetimą pokalbį galima įjungti (%s)' % r11.status_code)
finally:
    ts.translate_messages_for_user = orig_v

# Užrašai — tokie, kokių prašyta
A_ = open(os.path.join(BASE, 'templates', 'conversations', 'partials',
                       '_apacia.html'), encoding='utf-8').read()
for uzrasas in ('IŠVERSTI POKALBĮ', 'RODYTI ORIGINALIAS ŽINUTES',
                'Rodomi originalūs pranešimai', 'Pranešimai verčiami automatiškai'):
    tikrink(uzrasas in A_, 'trūksta užrašo „%s"' % uzrasas)


print('\n' + '═' * 60)
print('gerai: %d, nepavyko: %d' % (gerai, blogai))
sys.exit(1 if blogai else 0)
