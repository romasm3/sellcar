# -*- coding: utf-8 -*-
"""
REGISTRACIJA, PRISIJUNGIMAS, ATSIJUNGIMAS — tikru Django klientu.

Ne „ar kodas atrodo teisingai", o ar tikrai: ar įrašas atsirado bazėje,
ar sesija tikrai baigta, ar klaida grąžinama su aiškiu tekstu, o ne 500.

Kas tikrinama:
  1. registracija — įrašas DB, pasisveikinimo laiškas, ar iškart prijungia
  2. prisijungimas — teisingi duomenys, blogas slaptažodis, nesamas paštas,
     ?next= nukreipimas
  3. atsijungimas — sesija baigta, saugomi puslapiai vėl prašo prisijungti
  4. ribiniai atvejai — užimtas paštas, per trumpas slaptažodis,
     slaptažodžio priminimas

Paleidimas:  python docs/prisijungimo_testas.py
"""
import os, re, sys, tempfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
for k, v in (('SECRET_KEY', 'x'), ('EMAIL_USER', 'x@x.lt'), ('EMAIL_PASSWORD', 'x')):
    os.environ.setdefault(k, v)

import django
from django.conf import settings

LAIKINA = tempfile.mkdtemp(prefix='prisijungimas-')
import config.settings as pagrindas
n = {k: v for k, v in vars(pagrindas).items() if k.isupper()}
n.update(
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3',
                           'NAME': os.path.join(LAIKINA, 'db.sqlite3')}},
    SECURE_SSL_REDIRECT=False, SESSION_COOKIE_SECURE=False,
    CSRF_COOKIE_SECURE=False, SECURE_HSTS_SECONDS=0,
    MEDIA_ROOT=LAIKINA, DEBUG=False, ALLOWED_HOSTS=['*'],
    # Laiškus siunčiam SINCHRONIŠKAI ir į atmintį — kitaip fono gija
    # spėtų nespėti, ir testas mirksėtų.
    PASTAS_FONE=False,
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
from django.core import mail
from django.core.cache import cache
from django.test import Client

U = get_user_model()

gerai = blogai = 0
LUZO = []


def tikrink(pav, ok, papild=''):
    global gerai, blogai
    print((u'  ✓ ' if ok else u'  ✗ ') + pav + (u'   %s' % (papild,) if papild else ''))
    if ok:
        gerai += 1
    else:
        blogai += 1
        LUZO.append(u'%s   (%s)' % (pav, papild) if papild else pav)


def antraste(t):
    print(u'\n' + u'═' * 62 + u'\n' + t + u'\n' + u'═' * 62)


def klaidos(html):
    """Formos klaidų tekstai iš atsakymo — be HTML žymų."""
    t = re.sub(r'<[^>]+>', ' ', html)
    t = re.sub(r'\s+', ' ', t)
    rasta = []
    for sablonas in (r'Šis el\. paštas jau užregistruotas\.',
                     r'[A-ZĄČĘĖĮŠŲŪŽ][^.!]{10,120}(slaptažod|paštas|prisijung|neteising)[^.!]{0,80}[.!]',
                     r'(This password is too short[^.]*\.)',
                     r'(Enter a valid email address\.)'):
        rasta += [m.strip() for m in re.findall(sablonas, t)]
    return rasta


def pirma_klaida(r):
    """Trumpas klaidos tekstas iš formos arba messages."""
    html = r.content.decode('utf-8')
    f = r.context.get('form') if r.context else None
    if f is not None and getattr(f, 'errors', None):
        for laukas, kl in f.errors.items():
            return u'%s: %s' % (laukas, kl[0])
    if r.context and r.context.get('messages'):
        for m in r.context['messages']:
            return unicode(m) if str is bytes else str(m)
    k = klaidos(html)
    return k[0] if k else u'(klaidos teksto nerasta)'


# DĖMESIO: prisijungimo forma siunčia lauką `email`, NE `username`
# (apps/accounts/views.py login_view). Su `username` visos patikros
# praeina tuščiai — autentifikacija krenta dėl tuščio pašto, ir atrodo,
# lyg „bloga klaida rodoma teisingai".
SLAPTAS = 'Labai-Stiprus-2026'


# ═══════════════════════════════════════════════════════════════════
antraste(u'1. REGISTRACIJA  /accounts/register/')

c = Client()
r = c.get('/accounts/register/')
tikrink(u'forma atsidaro', r.status_code == 200, u'HTTP %s' % r.status_code)

mail.outbox = []
pries = U.objects.count()
r = c.post('/accounts/register/',
           {'email': 'naujas@pavyzdys.lt',
            'password1': SLAPTAS, 'password2': SLAPTAS}, follow=True)
kodas = r.redirect_chain[-1][1] if r.redirect_chain else r.status_code
tikrink(u'registracija priimta (ne 500)', r.status_code == 200,
        u'HTTP %s, nukreipimai %s' % (r.status_code, r.redirect_chain))

u_ = U.objects.filter(email='naujas@pavyzdys.lt').first()
tikrink(u'įrašas atsirado bazėje', u_ is not None,
        u'vartotojų %d → %d' % (pries, U.objects.count()))
if u_:
    tikrink(u'username = el. paštas', u_.username == 'naujas@pavyzdys.lt',
            u_.username)
    tikrink(u'slaptažodis užšifruotas',
            u_.password != SLAPTAS and u_.check_password(SLAPTAS))

tikrink(u'IŠKART prijungia (patvirtinti pašto nereikia)',
        r.context['user'].is_authenticated if r.context else False,
        u'nukreipta į %s' % (r.redirect_chain[-1][0] if r.redirect_chain else '—'))

pasisveikinimas = [m for m in mail.outbox
                   if 'naujas@pavyzdys.lt' in (m.to or [])]
tikrink(u'išsiųstas pasisveikinimo laiškas', len(pasisveikinimas) >= 1,
        u'laiškų dėžutėje %d: %s' % (len(mail.outbox),
                                     [m.subject[:40] for m in mail.outbox[:3]]))

# Patvirtinimo scenarijaus nėra — paskyra aktyvi iš karto.
if u_:
    tikrink(u'paskyra iškart aktyvi (is_active)', u_.is_active is True)


# ═══════════════════════════════════════════════════════════════════
antraste(u'2. PRISIJUNGIMAS  /accounts/login/')

c.get('/accounts/logout/')          # po registracijos esam prisijungę
cache.clear()                       # antispam skaitiklis

c = Client()
r = c.get('/accounts/login/')
tikrink(u'forma atsidaro', r.status_code == 200, u'HTTP %s' % r.status_code)

r = c.post('/accounts/login/',
           {'email': 'naujas@pavyzdys.lt', 'password': SLAPTAS}, follow=True)
tikrink(u'teisingi duomenys → prisijungia',
        bool(r.context) and r.context['user'].is_authenticated,
        u'HTTP %s → %s' % (r.status_code,
                           r.redirect_chain[-1][0] if r.redirect_chain else '—'))
tikrink(u'nukreipia į puslapį, ne į klaidą', r.status_code == 200,
        u'HTTP %s' % r.status_code)

# ── Blogas slaptažodis ──────────────────────────────────────────────
cache.clear()
c2 = Client()
r = c2.post('/accounts/login/',
            {'email': 'naujas@pavyzdys.lt', 'password': 'blogas-slaptazodis'})
tikrink(u'blogas slaptažodis → NE 500', r.status_code in (200, 302),
        u'HTTP %s' % r.status_code)
tikrink(u'blogas slaptažodis → neprijungia',
        not (r.context and r.context['user'].is_authenticated))
tikrink(u'blogas slaptažodis → aiški klaida',
        bool(pirma_klaida(r)) and u'nerasta' not in pirma_klaida(r),
        pirma_klaida(r)[:90])

# ── Neegzistuojantis paštas ─────────────────────────────────────────
cache.clear()
c3 = Client()
r = c3.post('/accounts/login/',
            {'email': 'niekada-nebuvo@pavyzdys.lt', 'password': SLAPTAS})
tikrink(u'nesamas paštas → NE 500', r.status_code in (200, 302),
        u'HTTP %s' % r.status_code)
tikrink(u'nesamas paštas → neprijungia',
        not (r.context and r.context['user'].is_authenticated))
tikrink(u'nesamas paštas → aiški klaida',
        bool(pirma_klaida(r)) and u'nerasta' not in pirma_klaida(r),
        pirma_klaida(r)[:90])

# ── ?next= nukreipimas ──────────────────────────────────────────────
cache.clear()
c4 = Client()
r = c4.get('/create/')
tikrink(u'/create/ be prisijungimo → nukreipia į login',
        r.status_code == 302 and '/accounts/login/' in r['Location'],
        u'HTTP %s → %s' % (r.status_code, r.get('Location')))
kelias = r.get('Location', '')
tikrink(u'nukreipime yra ?next=/create/', 'next=' in kelias and 'create' in kelias,
        kelias)

r = c4.post('/accounts/login/?next=/create/',
            {'email': 'naujas@pavyzdys.lt', 'password': SLAPTAS})
tikrink(u'?next= grąžina atgal į /create/',
        r.status_code == 302 and '/create/' in r.get('Location', ''),
        u'HTTP %s → %s' % (r.status_code, r.get('Location')))


# ═══════════════════════════════════════════════════════════════════
antraste(u'3. ATSIJUNGIMAS  /accounts/logout/')

c5 = Client()
cache.clear()
c5.post('/accounts/login/', {'email': 'naujas@pavyzdys.lt',
                             'password': SLAPTAS})
tikrink(u'prieš atsijungimą sesija yra',
        '_auth_user_id' in c5.session, list(c5.session.keys())[:3])

r = c5.get('/accounts/logout/', follow=True)
tikrink(u'atsijungimas atsako be klaidos', r.status_code == 200,
        u'HTTP %s' % r.status_code)
tikrink(u'sesija TIKRAI baigta', '_auth_user_id' not in c5.session,
        list(c5.session.keys())[:3])
tikrink(u'kontekste nebeprisijungęs',
        not (r.context and r.context['user'].is_authenticated))

for adresas in ('/saved/', '/create/'):
    r = c5.get(adresas)
    tikrink(u'%-10s po atsijungimo vėl prašo prisijungti' % adresas,
            r.status_code == 302 and '/accounts/login/' in r.get('Location', ''),
            u'HTTP %s → %s' % (r.status_code, r.get('Location')))


# ═══════════════════════════════════════════════════════════════════
antraste(u'4. RIBINIAI ATVEJAI')

# ── Užimtas paštas ──────────────────────────────────────────────────
cache.clear()
c6 = Client()
kiek_pries = U.objects.count()
r = c6.post('/accounts/register/',
            {'email': 'naujas@pavyzdys.lt',
             'password1': SLAPTAS, 'password2': SLAPTAS})
tikrink(u'užimtas paštas → NE 500', r.status_code in (200, 302),
        u'HTTP %s' % r.status_code)
tikrink(u'užimtas paštas → antro įrašo nesukuria',
        U.objects.filter(email='naujas@pavyzdys.lt').count() == 1,
        u'tokių įrašų: %d' % U.objects.filter(email='naujas@pavyzdys.lt').count())
tikrink(u'užimtas paštas → aiški klaida',
        u'jau užregistruotas' in pirma_klaida(r)
        or u'already' in pirma_klaida(r).lower(),
        pirma_klaida(r)[:90])

# ── Per trumpas slaptažodis ─────────────────────────────────────────
cache.clear()
c7 = Client()
r = c7.post('/accounts/register/',
            {'email': 'trumpas@pavyzdys.lt', 'password1': 'abc', 'password2': 'abc'})
tikrink(u'trumpas slaptažodis → NE 500', r.status_code in (200, 302),
        u'HTTP %s' % r.status_code)
tikrink(u'trumpas slaptažodis → vartotojo nesukuria',
        not U.objects.filter(email='trumpas@pavyzdys.lt').exists())
tikrink(u'trumpas slaptažodis → aiški klaida', bool(pirma_klaida(r)),
        pirma_klaida(r)[:90])

# ── Slaptažodžio priminimas ─────────────────────────────────────────
cache.clear()
c8 = Client()
r = c8.get('/accounts/password-reset/')
tikrink(u'priminimo forma atsidaro', r.status_code == 200,
        u'HTTP %s' % r.status_code)

mail.outbox = []
r = c8.post('/accounts/password-reset/', {'email': 'naujas@pavyzdys.lt'},
            follow=True)
tikrink(u'priminimas priimtas (ne 500)', r.status_code == 200,
        u'HTTP %s → %s' % (r.status_code,
                           r.redirect_chain[-1][0] if r.redirect_chain else '—'))
tikrink(u'priminimo laiškas IŠĖJO', len(mail.outbox) >= 1,
        u'laiškų %d: %s' % (len(mail.outbox),
                            [m.subject[:40] for m in mail.outbox[:2]]))
if mail.outbox:
    kunas = mail.outbox[0].body
    nuoroda = re.search(r'/accounts/password-reset-confirm/[^\s"\']+', kunas)
    tikrink(u'laiške yra atstatymo nuoroda', nuoroda is not None,
            nuoroda.group(0)[:60] if nuoroda else kunas[:60])
    if nuoroda:
        r = c8.get(nuoroda.group(0), follow=True)
        tikrink(u'nuoroda iš laiško atsidaro', r.status_code == 200,
                u'HTTP %s' % r.status_code)

# Nesamas paštas priminime neturi nei krist, nei išduoti, kad tokio nėra.
mail.outbox = []
r = c8.post('/accounts/password-reset/', {'email': 'nera@pavyzdys.lt'},
            follow=True)
tikrink(u'priminimas nesamam paštui → NE 500', r.status_code == 200,
        u'HTTP %s' % r.status_code)
tikrink(u'nesamam paštui laiško nesiunčia', len(mail.outbox) == 0,
        u'laiškų %d' % len(mail.outbox))


# ═══════════════════════════════════════════════════════════════════
print(u'\n' + u'═' * 62)
print(u'gerai: %d, nepavyko: %d' % (gerai, blogai))
if LUZO:
    print(u'\nKAS LŪŽO:')
    for x in LUZO:
        print(u'  • %s' % x)
sys.exit(1 if blogai else 0)
