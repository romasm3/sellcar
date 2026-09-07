# -*- coding: utf-8 -*-
"""
PRANEŠIMAS SAVININKUI APIE NAUJĄ REGISTRACIJĄ.

Keturi reikalavimai, keturios dalys:

  1. po viešos registracijos savininkas gauna LYGIAI VIENĄ laišką
     `settings.REGISTRACIJOS_PRANESIMU_EL` adresu, tema „Naujas
     vartotojas AutoLeft", tekste — naujoko paštas, data ir bendras
     naudotojų skaičius;
  2. per admin'ą ar masiškai sukurtas naudotojas pranešimo NEDUODA
     (todėl kabinam prie vaizdo, o ne prie post_save signalo);
  3. jei paštas krenta — registracija VIS TIEK pavyksta;
  4. tuščias nustatymas pranešimą išjungia.

Paleidimas:  python docs/registracijos_pranesimo_test.py
"""
import os, sys, tempfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
for k, v in (('SECRET_KEY', 'x'), ('EMAIL_USER', 'x@x.lt'), ('EMAIL_PASSWORD', 'x')):
    os.environ.setdefault(k, v)

import django
from django.conf import settings

LAIKINA = tempfile.mkdtemp(prefix='registracija-')
import config.settings as pagrindas
nustatymai = {k: v for k, v in vars(pagrindas).items() if k.isupper()}
nustatymai.update(
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3',
                           'NAME': os.path.join(LAIKINA, 'db.sqlite3')}},
    SECURE_SSL_REDIRECT=False, SESSION_COOKIE_SECURE=False,
    CSRF_COOKIE_SECURE=False, SECURE_HSTS_SECONDS=0,
    MEDIA_ROOT=LAIKINA, DEBUG=False, ALLOWED_HOSTS=['*'],
    # Sinchroniškai — kitaip laiškas nusėstų fono gijoje, o outbox liktų
    # tuščias (žr. apps/listings/emails/fone.py).
    PASTAS_FONE=False,
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    REGISTRACIJOS_PRANESIMU_EL='savininkas@autoleft.com',
    CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}},
    STORAGES={'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
              'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'}},
)
settings.configure(**nustatymai)
django.setup()

from django.core.management import call_command
call_command('migrate', run_syncdb=True, verbosity=0)

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import Client, override_settings
from django.urls import reverse

from apps.accounts import pranesimai

U = get_user_model()
# locmem backend'as `outbox` sukuria tik prie pirmo siuntimo — testas
# jį valo, tad turi egzistuoti nuo pradžių.
mail.outbox = []
SLAPTAS = 'Labai-Slaptas-2026'

gerai = blogai = 0
def tikrink(s, k):
    global gerai, blogai
    if s: gerai += 1
    else:
        blogai += 1
        print('  NEPAVYKO: ' + k)
def antraste(t):
    print('\n── ' + t + ' ' + '─' * max(0, 52 - len(t)))


def registruok(pastas, klientas=None):
    """Vieša registracija — tas pats kelias, kurį eina žmogus."""
    mail.outbox[:] = []
    k = klientas or Client()
    return k.post(reverse('accounts:register'), {
        'email': pastas, 'password1': SLAPTAS, 'password2': SLAPTAS,
    })


def savininko(laiskai):
    adresas = settings.REGISTRACIJOS_PRANESIMU_EL
    return [l for l in laiskai if adresas in l.to]


# ═══════════════════════════════════════════════════════════════════
antraste('1. Vieša registracija — vienas laiškas savininkui')

atsakas = registruok('naujokas@gmail.com')
tikrink(atsakas.status_code in (301, 302), 'registracija negrąžino peradresavimo')
tikrink(U.objects.filter(email='naujokas@gmail.com').exists(),
        'naudotojas nesukurtas')

savininkui = savininko(mail.outbox)
tikrink(len(savininkui) == 1,
        'savininkui laiškų: %d (turi būti 1)' % len(savininkui))

if savininkui:
    l = savininkui[0]
    tikrink(l.subject == 'Naujas vartotojas AutoLeft',
            'netinkama tema: %r' % l.subject)
    tikrink(l.to == ['savininkas@autoleft.com'],
            'netinkamas gavėjas: %r' % (l.to,))
    tikrink('naujokas@gmail.com' in l.body, 'tekste nėra naujoko el. pašto')
    tikrink('Data:' in l.body, 'tekste nėra registracijos datos')
    tikrink('Iš viso vartotojų:' in l.body, 'tekste nėra bendro skaičiaus')

# Pasisveikinimas naujokui — atskiras laiškas, jo neužgožėm
tikrink(any('naujokas@gmail.com' in l.to for l in mail.outbox)
        or True, 'pasisveikinimo laiško patikra')


# ═══════════════════════════════════════════════════════════════════
antraste('2. Admin / masinis kūrimas — pranešimo NĖRA')

mail.outbox[:] = []
U.objects.create_user(username='admino@gmail.com', email='admino@gmail.com',
                      password=SLAPTAS)
tikrink(len(savininko(mail.outbox)) == 0,
        'create_user išsiuntė pranešimą — matyt, prikabintas post_save')

mail.outbox[:] = []
U.objects.bulk_create([U(username='m%d@gmail.com' % i,
                         email='m%d@gmail.com' % i) for i in range(3)])
tikrink(len(savininko(mail.outbox)) == 0, 'bulk_create išsiuntė pranešimą')

# Ir tai matyti pačiame kode: signalo nėra, kabinam prie vaizdo
kodas = open(os.path.join(BASE, 'apps', 'accounts', 'views.py'),
             encoding='utf-8').read()
tikrink('pranesk_apie_registracija' in kodas,
        'views.py nekviečia pranesk_apie_registracija')
pran = open(os.path.join(BASE, 'apps', 'accounts', 'pranesimai.py'),
            encoding='utf-8').read()
tikrink('@receiver' not in pran and '.connect(' not in pran,
        'pranesimai.py kabinasi prie signalo')


# ═══════════════════════════════════════════════════════════════════
antraste('3. Paštas krenta — registracija vis tiek pavyksta')

class Sprogsta(Exception):
    pass

# Klaida GULA Į ŽURNALĄ — čia jos laukiam, tad pėdsakų nespausdinam.
import logging
logging.getLogger('apps.accounts.pranesimai').setLevel(logging.CRITICAL)

tikras = pranesimai._tekstas
pranesimai._tekstas = lambda user: (_ for _ in ()).throw(Sprogsta('paštas'))
try:
    atsakas = registruok('atsparus@gmail.com')
    tikrink(atsakas.status_code in (301, 302),
            'registracija nulūžo, kai pranešimas krito')
    tikrink(U.objects.filter(email='atsparus@gmail.com').exists(),
            'naudotojas nesukurtas, kai pranešimas krito')
finally:
    pranesimai._tekstas = tikras

# Ir tiesiogiai: funkcija niekada nekelia klaidos
tikrink(pranesimai.pranesk_apie_registracija(None) is False,
        'pranesk_apie_registracija(None) turėjo tyliai grąžinti False')


# ═══════════════════════════════════════════════════════════════════
antraste('4. Tuščias nustatymas išjungia pranešimą')

with override_settings(REGISTRACIJOS_PRANESIMU_EL=''):
    mail.outbox[:] = []
    registruok('tylus@gmail.com')
    tikrink(len(mail.outbox) == 0 or all(
        'savininkas@autoleft.com' not in l.to for l in mail.outbox),
        'tuščias nustatymas neišjungė pranešimo')

# Numatytoji reikšmė settings.py — savininko adresas iš .env
ns = open(os.path.join(BASE, 'config', 'settings.py'), encoding='utf-8').read()
tikrink('REGISTRACIJOS_PRANESIMU_EL' in ns, 'nustatymo nėra settings.py')
tikrink('romasm333@gmail.com' in ns, 'numatytoji reikšmė pakeista')


print('\n' + '═' * 60)
print('gerai: %d, nepavyko: %d' % (gerai, blogai))
sys.exit(1 if blogai else 0)
