# -*- coding: utf-8 -*-
"""
DEPLOY SARGYBINIO TESTAS.

Kodėl reikia. 2026-09 deploy'as stovėjo aštuonias paras, ir to nepamatė
niekas: timeris krito tyliai, nes tyla yra normalus jo elgesys. Sargybinis
(apps/analytics/management/commands/deploy_sargyba.py) tą tylą nutraukia —
bet tik tuo atveju, jei pats veikia teisingai.

Tikrinam tikrame git repozitorijuje, ne su maketais:

  1. įdiegta = master            -> tyli
  2. atsilieka, bet šviežiai     -> tyli (dešimt commit'ų per valandą — normalu)
  3. atsilieka senai             -> rašo laišką, jame commit'ų skaičius
  4. nežinomas commit'as         -> rašo laišką, o ne tyli
  5. `cat-file -e` sėkmė         -> NELAIKOMA klaida (ši klaida jau buvo)

Paleidimas:  python docs/deploy_sargybos_test.py
"""
import io, os, subprocess, sys, tempfile, time

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
sys.path.insert(0, os.path.join(BASE, 'docs', 'patikra'))
for k, v in (('SECRET_KEY', 'x'), ('EMAIL_USER', 'x@x.lt'),
             ('EMAIL_PASSWORD', 'x'), ('DEBUG', 'True'), ('ALLOWED_HOSTS', '*'),
             ('STRIPE_SECRET_KEY', 'sk_test_x'),
             ('STRIPE_PUBLISHABLE_KEY', 'pk_test_x'),
             ('STRIPE_WEBHOOK_SECRET', 'whsec_x')):
    os.environ.setdefault(k, v)
os.environ.setdefault('PATIKRA_DB', os.path.join(BASE, '.patikra_sargyba.sqlite3'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'sqlite_settings'

import django
django.setup()

from django.conf import settings
from django.core import mail
from django.test.utils import override_settings

from apps.analytics.management.commands import deploy_sargyba as S

gerai = blogai = 0
def tikrink(pav, ok, papild=''):
    global gerai, blogai
    print((u'  ✓ ' if ok else u'  ✗ ') + pav + (u'   %s' % (papild,) if papild else ''))
    if ok:
        gerai += 1
    else:
        blogai += 1


# ── Tikras repozitorijus: nuotolinis + klonas ───────────────────────
T = tempfile.mkdtemp(prefix='sargyba-')
NUOTOLINIS = os.path.join(T, 'nuotolinis.git')
APP = os.path.join(T, 'app')


def git(*a, **kw):
    return subprocess.check_output(
        ('git',) + a, cwd=kw.get('cwd', APP),
        stderr=subprocess.DEVNULL).decode('utf-8').strip()


subprocess.check_call(('git', 'init', '-q', '--bare', NUOTOLINIS))
subprocess.check_call(('git', 'clone', '-q', NUOTOLINIS, APP),
                      stderr=subprocess.DEVNULL)
git('config', 'user.email', 't@t')
git('config', 'user.name', 'T')
io.open(os.path.join(APP, 'f.txt'), 'w').write('v1\n')
git('add', '-A')
git('commit', '-qm', 'pirmas')
git('branch', '-M', 'master')
git('push', '-q', '-u', 'origin', 'master')
PIRMAS = git('rev-parse', 'HEAD')

# Sargybinis dirba settings.BASE_DIR kataloge — nukreipiam į testinį.
S.settings = settings


def su_repo(sha, riba=24):
    with override_settings(BASE_DIR=APP, GIT_SHA=sha[:12]):
        return S.bukle(riba)


print(u'\n== 1. Įdiegta = master -> tyli ==')
d = su_repo(PIRMAS)
tikrink(u'neatsilieka', d['atsilieka'] is False, d)
tikrink(u'commit\'ų 0', d['commitu'] == 0, d['commitu'])

print(u'\n== 2. Atsilieka, bet šviežiai -> tyli ==')
io.open(os.path.join(APP, 'f.txt'), 'w').write('v2\n')
git('commit', '-qam', 'antras')
git('push', '-q', 'origin', 'master')
d = su_repo(PIRMAS)
tikrink(u'commit\'ų 1', d['commitu'] == 1, d['commitu'])
tikrink(u'šviežias atsilikimas netriukšmauja', d['atsilieka'] is False,
        u'%.1f val.' % d['valandu'])

print(u'\n== 3. Atsilieka senai -> laiškas ==')
# Perrašom commit\'o datą į 8 paras atgal — kaip ir buvo gyvai.
sena = time.strftime('%Y-%m-%dT%H:%M:%S',
                     time.gmtime(time.time() - 8 * 86400))
env = dict(os.environ, GIT_COMMITTER_DATE=sena, GIT_AUTHOR_DATE=sena)
subprocess.check_call(('git', 'commit', '-q', '--amend', '--no-edit',
                       '--date', sena), cwd=APP, env=env,
                      stderr=subprocess.DEVNULL)
git('push', '-qf', 'origin', 'master')
d = su_repo(PIRMAS)
SENAS = d = su_repo(PIRMAS)
tikrink(u'atsilikimas pastebėtas', d['atsilieka'] is True, d)
tikrink(u'valandų daugiau nei para', d['valandu'] > 24, u'%.1f' % d['valandu'])

tekstas = None
with override_settings(BASE_DIR=APP, GIT_SHA=PIRMAS[:12],
                       EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
    tekstas = S.laisko_tekstas(d)
tikrink(u'laiške yra commit\'ų skaičius', str(d['commitu']) in tekstas)
tikrink(u'laiške yra abi versijos',
        d['idiegta'] in tekstas and d['master'] in tekstas)
tikrink(u'laiške yra paskutinė deploy klaida',
        u'žurnalo eilutės' in tekstas, tekstas.count('\n'))
tikrink(u'laiške yra, ką daryti', u'deploy-from-git.sh' in tekstas)

print(u'\n== 4. Nežinomas commit\'as -> laiškas, ne tyla ==')
d = su_repo('0' * 12)
tikrink(u'nežinoma versija laikoma gedimu', d['atsilieka'] is True, d.get('pastaba'))

print(u'\n== 5. `cat-file -e` sėkmė nėra klaida ==')
# Ši klaida jau buvo: komanda sėkmės atveju nieko nespausdina, tad
# tikrinant pagal išvestį sėkmė atrodė kaip klaida ir sargybinis būtų
# rašęs laišką kasdien be reikalo.
with override_settings(BASE_DIR=APP):
    tikrink(u'esamas commit\'as randamas',
            S._git_yra('cat-file', '-e', '%s^{commit}' % PIRMAS) is True)
    tikrink(u'neesamo commit\'o nėra',
            S._git_yra('cat-file', '-e', '%s^{commit}' % ('0' * 40)) is False)
    tikrink(u'_git sėkmės atveju grąžina tuščią eilutę',
            S._git('cat-file', '-e', '%s^{commit}' % PIRMAS) == '')

print(u'\n== 6. Laiškas tikrai išeina ==')
with override_settings(BASE_DIR=APP, GIT_SHA=PIRMAS[:12],
                       EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
    from django.core.management import call_command
    mail.outbox = []
    call_command('deploy_sargyba', verbosity=0)
    tikrink(u'išsiųstas vienas laiškas', len(mail.outbox) == 1, len(mail.outbox))
    if mail.outbox:
        tikrink(u'gavėjas romasm3@gmail.com',
                mail.outbox[0].to == ['romasm3@gmail.com'], mail.outbox[0].to)
        tikrink(u'temoje — commit\'ų skaičius',
                str(SENAS['commitu']) in mail.outbox[0].subject,
                mail.outbox[0].subject)
    mail.outbox = []
    call_command('deploy_sargyba', verbosity=0, valandos=100000)
    tikrink(u'neatsiliekant laiško nėra', len(mail.outbox) == 0, len(mail.outbox))

print('\n' + '=' * 60)
print('gerai: %d, nepavyko: %d' % (gerai, blogai))
sys.exit(1 if blogai else 0)
