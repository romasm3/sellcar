# -*- coding: utf-8 -*-
"""
LANKYTOJŲ STATISTIKA: BE ŽALIO IP, BE 502.

Kas buvo.

1. /admin-moderate/sales-stats/ grąžindavo 502 Bad Gateway. Lankytojų
   blokas tame vaizde darė tris `set(...values_list('ip_address'))` BE
   jokio laiko rėžio — visi istoriniai įrašai į atmintį, ir dar
   `_daily_ips` su 30 dienų eilutėmis. Prie 400 tūkst. eilučių tai jau
   ~150 MB vienai užklausai, ir auga tiesiškai su lentele. Kai gunicorn
   darbininkas nebetelpa, nginx tai parodo kaip 502.

2. Lankytojo IP gulėdavo DB žalias (`PageView.ip_address`). Dabar
   saugom tik sha256(IP + SECRET_KEY) — `VisitorHit.ip_hash`.

3. Lentelė augo be galo — nebuvo jokio valymo.

Paleidimas:  python docs/lankytoju_statistikos_test.py
"""
import io, os, re, sys, tempfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
for k, v in (('SECRET_KEY', 'slapta-druska'), ('EMAIL_USER', 'x@x.lt'),
             ('EMAIL_PASSWORD', 'x')):
    os.environ.setdefault(k, v)

import django
from django.conf import settings

LAIKINA = tempfile.mkdtemp(prefix='lankytojai-')
import config.settings as pagrindas
n = {k: v for k, v in vars(pagrindas).items() if k.isupper()}
n.update(
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3',
                           'NAME': os.path.join(LAIKINA, 'db.sqlite3')}},
    SECURE_SSL_REDIRECT=False, SESSION_COOKIE_SECURE=False,
    CSRF_COOKIE_SECURE=False, SECURE_HSTS_SECONDS=0,
    MEDIA_ROOT=LAIKINA, DEBUG=False, ALLOWED_HOSTS=['*'], PASTAS_FONE=False,
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

# Be šito `response.context` lieka None: šablonų signalus įjungia būtent
# testų aplinka, o čia sukam Django be testų vykdyklės.
setup_test_environment()
call_command('migrate', run_syncdb=True, verbosity=0)

from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import Client, RequestFactory
from django.utils import timezone

from apps.analytics import valymas
from apps.analytics.middleware import (VisitorTrackingMiddleware, detect_bot,
                                       tikras_ip)
from apps.analytics.models import SAUGOM_DIENAS, VisitorHit, ip_maisa

gerai = blogai = 0
def tikrink(s, k):
    global gerai, blogai
    if s:
        gerai += 1
    else:
        blogai += 1
        print('  NEPAVYKO: ' + k)
def antraste(t):
    print('\n── ' + t + ' ' + '─' * max(0, 52 - len(t)))


U = get_user_model()
admin = U.objects.create_superuser(username='a@x.lt', email='a@x.lt', password='x')
if hasattr(admin, 'profile'):
    admin.profile.language = 'lt'
    admin.profile.save()


# ═══════════════════════════════════════════════════════════════════
antraste('1. Žalio IP DB nebėra')

stulpeliai = [f.name for f in VisitorHit._meta.concrete_fields]
tikrink('ip_address' not in stulpeliai, 'liko ip_address stulpelis')
tikrink('ip_hash' in stulpeliai, 'nėra ip_hash stulpelio')

IP = '203.0.113.7'
maisa = ip_maisa(IP)
tikrink(len(maisa) == 64 and re.fullmatch(r'[0-9a-f]{64}', maisa),
        'maiša ne sha256 heksais: %r' % maisa)
tikrink(IP not in maisa, 'maišoje matyti pats adresas')
tikrink(ip_maisa(IP) == maisa, 'ta pati maiša skiriasi tarp kvietimų')
tikrink(ip_maisa('203.0.113.8') != maisa, 'skirtingi IP duoda tą pačią maišą')
tikrink(ip_maisa('') == '', 'tuščias IP duoda maišą')

# Druska tikrai naudojama: be jos maiša sutaptų su grynu sha256
import hashlib
tikrink(maisa != hashlib.sha256(IP.encode()).hexdigest(),
        'maiša be druskos — perrenkama per visą IPv4 erdvę')

vidus = io.open(os.path.join(BASE, 'apps/analytics/middleware.py'),
                encoding='utf-8').read()
tikrink('ip_address' not in vidus, 'middleware vis dar mini ip_address')


# ═══════════════════════════════════════════════════════════════════
antraste('2. Tikras IP iš nginx antraščių')

rf = RequestFactory()
tikrink(tikras_ip(rf.get('/', HTTP_X_FORWARDED_FOR='198.51.100.5, 10.0.0.1',
                         REMOTE_ADDR='127.0.0.1')) == '198.51.100.5',
        'X-Forwarded-For grandinėje neimamas pirmas adresas')
tikrink(tikras_ip(rf.get('/', HTTP_X_REAL_IP='198.51.100.9',
                         REMOTE_ADDR='127.0.0.1')) == '198.51.100.9',
        'X-Real-IP nenaudojamas')
tikrink(tikras_ip(rf.get('/', REMOTE_ADDR='198.51.100.3')) == '198.51.100.3',
        'be antraščių neimamas REMOTE_ADDR')
tikrink(tikras_ip(rf.get('/', HTTP_X_FORWARDED_FOR='   ',
                         REMOTE_ADDR='198.51.100.4')) == '198.51.100.4',
        'tuščia XFF antraštė nustelbia REMOTE_ADDR')


# ═══════════════════════════════════════════════════════════════════
antraste('3. Botai atpažįstami ir skaičiuojami atskirai')

BOTAI = ['Googlebot/2.1', 'Mozilla/5.0 (compatible; bingbot/2.0)',
         'facebookexternalhit/1.1', 'python-requests/2.31',
         'curl/8.0.1', 'Wget/1.21', 'AhrefsBot/7.0', 'SemrushBot/7',
         'HeadlessChrome/120', 'Yandex/1.0 spider', 'Slurp',
         'Mozilla/5.0 ... crawler']
for ua in BOTAI:
    tikrink(detect_bot(ua, '/')[0], 'neatpažintas botas: %s' % ua)

ZMONES = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
          '(KHTML, like Gecko) Chrome/120.0 Safari/537.36',
          'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) '
          'AppleWebKit/605.1.15 Version/17.0 Mobile/15E148 Safari/604.1']
for ua in ZMONES:
    tikrink(not detect_bot(ua, '/')[0], 'žmogus palaikytas botu: %s' % ua[:40])

tikrink(detect_bot('', '/')[1] == 'empty_ua', 'tuščias UA ne empty_ua')
tikrink(detect_bot(ZMONES[0], '/wp-login.php')[1] == 'path_scan',
        'skenavimo kelias neatpažintas')


# ═══════════════════════════════════════════════════════════════════
antraste('4. Middleware įrašo maišą, o ne adresą')

from django.contrib.auth.models import AnonymousUser

def _uzklausa(kelias, ua, ip, metodas='get'):
    r = getattr(rf, metodas)(kelias, HTTP_USER_AGENT=ua,
                             HTTP_X_FORWARDED_FOR=ip)
    r.user = AnonymousUser()      # middleware'ą paprastai pasiekia jau su user
    return r

def per_middleware(kelias, ua, ip):
    mw = VisitorTrackingMiddleware(lambda r: None)
    mw._maybe_log(_uzklausa(kelias, ua, ip))

VisitorHit.objects.all().delete()
per_middleware('/', ZMONES[0], '198.51.100.20')
eil = VisitorHit.objects.first()
tikrink(eil is not None, 'apsilankymas neįrašytas')
if eil:
    tikrink(eil.ip_hash == ip_maisa('198.51.100.20'), 'įrašyta ne maiša')
    tikrink(not eil.is_bot, 'žmogus pažymėtas botu')

per_middleware('/', 'Googlebot/2.1', '198.51.100.21')
tikrink(VisitorHit.objects.filter(is_bot=True).count() == 1,
        'botas neužfiksuotas')

# Praleidžiami keliai
pries = VisitorHit.objects.count()
for kelias in ('/static/x.css', '/media/x.jpg', '/admin/', '/admin-moderate/',
               '/ajax/x/', '/health', '/favicon.ico'):
    per_middleware(kelias, ZMONES[0], '198.51.100.22')
tikrink(VisitorHit.objects.count() == pries,
        'praleidžiami keliai vis tiek įrašomi')

# POST neskaičiuojamas
mw = VisitorTrackingMiddleware(lambda r: None)
mw._maybe_log(_uzklausa('/', ZMONES[0], '198.51.100.23', metodas='post'))
tikrink(VisitorHit.objects.count() == pries, 'POST užfiksuotas kaip apsilankymas')


# ═══════════════════════════════════════════════════════════════════
antraste('5. Puslapis: laikotarpiai ir skaičiai')

VisitorHit.objects.all().delete()
now = timezone.now()

def hit(ip, salis, vardas, pries_dienas, botas=False, kiek=1):
    for _ in range(kiek):
        e = VisitorHit.objects.create(
            ip_hash=ip_maisa(ip), path='/', country=salis,
            country_name=vardas, user_agent='ua', is_bot=botas)
        VisitorHit.objects.filter(pk=e.pk).update(
            created_at=now - timedelta(days=pries_dienas, hours=1))

hit('1.1.1.1', 'LT', 'Lithuania', 0, kiek=3)
hit('1.1.1.2', 'LT', 'Lithuania', 0)
hit('1.1.1.3', 'DE', 'Germany', 3, kiek=2)
hit('1.1.1.4', 'PL', 'Poland', 20)
hit('1.1.1.5', 'PL', 'Poland', 60)
hit('9.9.9.9', 'LT', 'Lithuania', 0, botas=True, kiek=7)

c = Client()
c.force_login(admin)

def puslapis(laikotarpis):
    r = c.get('/admin-moderate/visitors/?laikotarpis=' + laikotarpis)
    return r, r.content.decode('utf-8')

for zyme in ('today', '7d', '30d', 'all', 'nesamone'):
    r, _k = puslapis(zyme)
    tikrink(r.status_code == 200, '%s → %s' % (zyme, r.status_code))

r, _k = puslapis('all')
ctx = r.context
tikrink(ctx['apsilankymu'] == 8, 'viso apsilankymų %s, laukta 8' % ctx['apsilankymu'])
tikrink(ctx['unikaliu'] == 5, 'unikalių %s, laukta 5' % ctx['unikaliu'])
tikrink(ctx['botu'] == 7, 'botų %s, laukta 7' % ctx['botu'])

r, _k = puslapis('today')
tikrink(r.context['unikaliu'] == 2, 'šiandien unikalių %s, laukta 2'
        % r.context['unikaliu'])
tikrink(r.context['botu'] == 7, 'šiandien botų %s, laukta 7' % r.context['botu'])

r, _k = puslapis('7d')
tikrink(r.context['unikaliu'] == 3, '7 d. unikalių %s, laukta 3'
        % r.context['unikaliu'])

r, _k = puslapis('30d')
tikrink(r.context['unikaliu'] == 4, '30 d. unikalių %s, laukta 4'
        % r.context['unikaliu'])

# Lentelė: šalys mažėjančiai, procentai, vėliavėlė
r, kunas = puslapis('all')
salys = r.context['salys']
tikrink([e['kodas'] for e in salys] == ['LT', 'PL', 'DE'],
        'šalių eilė: %s' % [e['kodas'] for e in salys])
tikrink(salys[0]['unikaliu'] == 2 and salys[0]['apsilankymu'] == 4,
        'LT: %s unik., %s apsil.' % (salys[0]['unikaliu'], salys[0]['apsilankymu']))
tikrink(abs(salys[0]['procentai'] - 40.0) < 0.05,
        'LT procentai %s, laukta 40.0' % salys[0]['procentai'])
tikrink(sum(e['unikaliu'] for e in salys) == 5, 'šalių suma ne 5')
tikrink('flags/lt.svg' in kunas, 'nėra Lietuvos vėliavėlės')
tikrink('9.9.9.9' not in kunas and '1.1.1.1' not in kunas,
        'puslapyje matyti žali IP')

# Botai į „realius lankytojus" neįeina
tikrink(all(e['kodas'] != 'LT' or e['unikaliu'] == 2 for e in salys),
        'boto IP pateko į unikalius lankytojus')


# ═══════════════════════════════════════════════════════════════════
antraste('6. Meniu nuoroda ir prieiga')

paprastas = U.objects.create_user(username='b@x.lt', email='b@x.lt', password='x')
if hasattr(paprastas, 'profile'):
    paprastas.profile.language = 'lt'
    paprastas.profile.save()
c2 = Client()
tikrink(c2.get('/admin-moderate/visitors/').status_code in (301, 302),
        'neprisijungęs patenka į statistiką')
c2.force_login(paprastas)
tikrink(c2.get('/admin-moderate/visitors/').status_code in (301, 302),
        'paprastas vartotojas patenka į statistiką')

kunas = c.get('/').content.decode('utf-8')
tikrink('/admin-moderate/visitors/' in kunas, 'meniu nėra nuorodos')
tikrink('Lankytoj' in kunas, 'meniu nėra „Lankytojų statistika"')


# ═══════════════════════════════════════════════════════════════════
antraste('7. Senų įrašų valymas')

tikrink(SAUGOM_DIENAS == 90, 'saugom ne 90 d.: %s' % SAUGOM_DIENAS)
hit('2.2.2.1', 'LT', 'Lithuania', 200)
hit('2.2.2.2', 'LT', 'Lithuania', 91)
pries = VisitorHit.objects.count()
tikrink(valymas.kiek_senu() == 2, 'senų rasta %s, laukta 2' % valymas.kiek_senu())
istrinta = valymas.valyk()
tikrink(istrinta == 2, 'ištrinta %s, laukta 2' % istrinta)
tikrink(VisitorHit.objects.count() == pries - 2, 'liko ne tiek įrašų')

# Komanda
from io import StringIO
isvestis = StringIO()
hit('2.2.2.3', 'LT', 'Lithuania', 120)
call_command('valyti_lankytojus', '--parodyk', stdout=isvestis)
tikrink('1' in isvestis.getvalue(), 'komanda --parodyk nerodo skaičiaus')
tikrink(VisitorHit.objects.filter(ip_hash=ip_maisa('2.2.2.3')).exists(),
        '--parodyk vis tiek ištrynė')
call_command('valyti_lankytojus', stdout=StringIO())
tikrink(not VisitorHit.objects.filter(ip_hash=ip_maisa('2.2.2.3')).exists(),
        'komanda neištrynė seno įrašo')

# Puslapis valo pats, bet ne dažniau kaip kartą per parą
from django.core.cache import cache
cache.clear()
hit('2.2.2.4', 'LT', 'Lithuania', 150)
c.get('/admin-moderate/visitors/')
tikrink(not VisitorHit.objects.filter(ip_hash=ip_maisa('2.2.2.4')).exists(),
        'puslapis nepavalė senų įrašų')
hit('2.2.2.5', 'LT', 'Lithuania', 150)
c.get('/admin-moderate/visitors/')
tikrink(VisitorHit.objects.filter(ip_hash=ip_maisa('2.2.2.5')).exists(),
        'puslapis valo kas kartą, o ne kartą per parą')


# ═══════════════════════════════════════════════════════════════════
antraste('8. /sales-stats/ nebetraukia eilučių į atmintį')

vaizdai = io.open(os.path.join(BASE, 'apps/listings/views.py'),
                  encoding='utf-8').read()
pradzia = vaizdai.index('def admin_sales_stats(')
galas = vaizdai.index('\n@', pradzia + 10) if '\n@' in vaizdai[pradzia + 10:] else len(vaizdai)
blokas = vaizdai[pradzia:galas]
kodas = '\n'.join(e for e in blokas.split('\n')
                  if not e.lstrip().startswith('#'))
tikrink('_before_month =' not in kodas and '_daily_ips =' not in kodas,
        'liko seni pilno nuskaitymo rinkiniai')
tikrink('set(_human_qs' not in kodas and "values_list('ip_hash'" not in kodas,
        'lankytojų blokas vis dar traukia eilutes į Python')
tikrink('values(\'ip_hash\').distinct().count()' in blokas,
        'unikalūs lankytojai neskaičiuojami DB pusėje')

r = c.get('/admin-moderate/sales-stats/')
tikrink(r.status_code == 200, '/sales-stats/ → %s' % r.status_code)
tikrink(r.context['visitors_month'] >= 0, 'nėra visitors_month')


print('\n' + '═' * 60)
print('gerai: %d, nepavyko: %d' % (gerai, blogai))
sys.exit(1 if blogai else 0)
