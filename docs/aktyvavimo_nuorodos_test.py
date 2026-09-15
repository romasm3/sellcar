# -*- coding: utf-8 -*-
"""
AKTYVAVIMO NUORODA IŠ PRIMINIMO LAIŠKO NEBEGRĄŽINA 500.

Kas buvo. Priminimo laiškas (send_draft_reminders.py) siunčia nuorodą į
/<pk>/activation-plans/. Puslapis krito su 500 KIEKVIENAM prisijungusiam
savininkui — bet tik tada, kai kategorijai yra sukurtų planų:

    django.template.exceptions.TemplateSyntaxError:
        'counter' argument to 'blocktrans' tag must be a number

Šablonas naudojo `plan.days`, o `PricingPlan` laukas vadinasi
`duration_days`. Neegzistuojantis kintamasis šablone virsta tuščia
eilute, o `{% blocktrans count counter='' %}` meta klaidą. Tuščias planų
sąrašas ciklo kūno nevykdo, todėl vietiniuose testuose be planų puslapis
atrodė sveikas.

Tuo pačiu `plan.discount` (yra `discount_percent`) ir `plan.features`
(yra `features_list`) tyliai nieko nerodė, o forma siuntė
`name="plan" = dienų skaičius`, nors vaizdas laukia `plan_id` — tad net
ir atsidaręs puslapis kiekvieną pasirinkimą atmesdavo.

Antra dalis: nuoroda iš laiško spaudžiama po savaitės, kitame įrenginyje,
kartais ne tos paskyros naršyklėje. Nė vienas toks atvejis neturi baigtis
klaidos ar 404 puslapiu.

Paleidimas:  python docs/aktyvavimo_nuorodos_test.py
"""
import io, os, sys, tempfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
for k, v in (('SECRET_KEY', 'x'), ('EMAIL_USER', 'x@x.lt'), ('EMAIL_PASSWORD', 'x')):
    os.environ.setdefault(k, v)

import django
from django.conf import settings

LAIKINA = tempfile.mkdtemp(prefix='aktyvavimas-')
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

setup_test_environment()
call_command('migrate', run_syncdb=True, verbosity=0)

from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import Client
from django.utils import timezone

from apps.listings.models import Listing, PricingPlan, VehicleType

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
sav = U.objects.create_user(username='s@x.lt', email='s@x.lt', password='x')
kitas = U.objects.create_user(username='k@x.lt', email='k@x.lt', password='x')
for u in (sav, kitas):
    if hasattr(u, 'profile'):
        u.profile.language = 'lt'
        u.profile.phone_number = '+37060000000'
        u.profile.save()

VT, _s = VehicleType.objects.get_or_create(slug='cars', defaults={'name': 'Automobiliai'})
TUSCIA_VT, _s = VehicleType.objects.get_or_create(slug='boats', defaults={'name': 'Laivai'})

# BŪTINA: be planų ciklo kūnas nevykdomas ir klaida nepasirodo.
for eile, (d, kaina) in enumerate(((30, '9.99'), (60, '14.99'), (90, '19.99'))):
    PricingPlan.objects.create(vehicle_type=VT, duration_days=d, price=kaina,
                               is_active=True, order=eile,
                               boost_days=(3 if d == 60 else 0),
                               vip_days=(7 if d == 90 else 0),
                               discount_percent=(20 if d == 90 else None),
                               is_popular=(d == 60))


def skelbimas(status, vt=None, **extra):
    d = dict(seller=sav, vehicle_type=vt or VT, title='Testas', year=2018,
             mileage=1000, price=5000, country='LT', city='Vilnius',
             status=status, condition='used', defects='none',
             first_registration=date(2018, 5, 1))
    d.update(extra)
    return Listing.objects.create(**d)


def atidaryk(klientas, pk, metodas='get', **duom):
    url = '/%d/activation-plans/' % pk
    if metodas == 'post':
        return url, klientas.post(url, duom, follow=True)
    return url, klientas.get(url, follow=True)


def zinutes(atsakas):
    if not atsakas.context or 'messages' not in atsakas.context:
        return []
    return [str(m.message) for m in atsakas.context['messages']]


anon = Client()
savas = Client(); savas.force_login(sav)
svetimas = Client(); svetimas.force_login(kitas)


# ═══════════════════════════════════════════════════════════════════
antraste('1. Puslapis atsidaro, kai planai YRA (buvo 500)')

pasibaiges = skelbimas('expired')
url, r = atidaryk(savas, pasibaiges.pk)
tikrink(r.status_code == 200, 'planų puslapis → %s' % r.status_code)
kunas = r.content.decode('utf-8')
tikrink(kunas.count('plan-card') >= 3, 'rodomos ne visos planų kortelės')
tikrink('30 d' in kunas or '30 dien' in kunas, 'nesimato plano trukmės')
tikrink('9,99' in kunas or '9.99' in kunas, 'nesimato plano kainos')
tikrink('-20%' in kunas, 'nuolaida nerodoma (plan.discount_percent)')
tikrink('Listing duration' in kunas or 'Boost' in kunas,
        'planų savybės nerodomos (plan.features_list)')


# ═══════════════════════════════════════════════════════════════════
antraste('2. Šablonas naudoja TIKRUS modelio laukus')

sab = io.open(os.path.join(BASE,
              'templates/listings/listing_activation_plans.html'),
              encoding='utf-8').read()
laukai = {f.name for f in PricingPlan._meta.concrete_fields}
for vardas in ('duration_days', 'discount_percent', 'price', 'old_price',
               'is_popular'):
    tikrink(vardas in laukai, 'PricingPlan nebeturi lauko %s' % vardas)
tikrink('plan.days' not in sab, 'šablone vėl plan.days (nėra tokio lauko)')
tikrink('plan.discount }' not in sab, 'šablone vėl plan.discount')
tikrink('plan.features %' not in sab, 'šablone vėl plan.features')
tikrink('counter=plan.duration_days' in sab,
        'blocktrans skaičiuoja ne iš duration_days')
tikrink(hasattr(PricingPlan, 'features_list'), 'nebėra features_list')


# ═══════════════════════════════════════════════════════════════════
antraste('3. Forma siunčia plano ID, ne dienas')

tikrink('name="plan_id"' in sab, 'forma nesiunčia plan_id')
tikrink('data-plan-id' in sab, 'kortelė neturi plano ID')
tikrink('card.dataset.planId' in sab, 'JS vis dar deda dienų skaičių')

planas = PricingPlan.objects.get(vehicle_type=VT, duration_days=30)
url, r = atidaryk(savas, pasibaiges.pk, 'post', plan_id=str(planas.id))
tikrink(r.status_code == 200, 'pateikimas → %s' % r.status_code)
tikrink('/success/' in (r.redirect_chain[-1][0] if r.redirect_chain else ''),
        'po pateikimo nepatenkam į „pavyko" puslapį')
pasibaiges.refresh_from_db()
tikrink(pasibaiges.status == 'active',
        'skelbimas neaktyvuotas: %s' % pasibaiges.status)
tikrink(pasibaiges.expires_at is not None
        and pasibaiges.expires_at > timezone.now() + timedelta(days=29),
        'galiojimas nepratęstas 30 d.')


# ═══════════════════════════════════════════════════════════════════
antraste('4. Penki atvejai — jokio 500 ir jokio 404')

# 1) neprisijungęs → prisijungimas su ?next=
juodrastis = skelbimas('draft')
url, r = atidaryk(anon, juodrastis.pk)
paskutinis = r.redirect_chain[-1][0] if r.redirect_chain else ''
tikrink(r.status_code == 200, 'neprisijungęs gavo %s' % r.status_code)
tikrink('login' in paskutinis, 'neprisijungęs nenuvestas į prisijungimą')
tikrink('next=' in paskutinis and 'activation-plans' in paskutinis,
        'prisijungus negrįš atgal į nuorodą: %s' % paskutinis)

# 2) jau aktyvus
aktyvus = skelbimas('active')
url, r = atidaryk(savas, aktyvus.pk)
tikrink(r.status_code == 200, 'aktyvus → %s' % r.status_code)
tikrink(any('jau aktyvus' in z for z in zinutes(r)),
        'nėra žinutės apie jau aktyvų skelbimą: %s' % zinutes(r))

# 3) ištrintas / neegzistuoja
url, r = atidaryk(savas, 987654)
tikrink(r.status_code == 200, 'neegzistuojantis → %s' % r.status_code)
tikrink(any('nebėra' in z for z in zinutes(r)),
        'nėra žinutės apie dingusį skelbimą: %s' % zinutes(r))

# 4) svetimas skelbimas — TA PATI žinutė, kad neatskleistume, ar toks yra
url, r2 = atidaryk(svetimas, juodrastis.pk)
tikrink(r2.status_code == 200, 'svetimas → %s' % r2.status_code)
tikrink(zinutes(r2) == zinutes(r),
        'svetimo ir neegzistuojančio atsakymai skiriasi — galima tikrinti pk')

# 5) galiojimas pasibaigęs
kitas_pasibaiges = skelbimas('expired')
url, r = atidaryk(savas, kitas_pasibaiges.pk)
tikrink(r.status_code == 200, 'pasibaigęs → %s' % r.status_code)
tikrink(any('pasibaig' in z for z in zinutes(r)),
        'nėra žinutės apie pasibaigusį galiojimą: %s' % zinutes(r))
tikrink('plan-card' in r.content.decode('utf-8'),
        'pasibaigusiam nerodomi planai pratęsimui')

# parduotas — irgi ne klaida
parduotas = skelbimas('sold')
url, r = atidaryk(savas, parduotas.pk)
tikrink(r.status_code == 200, 'parduotas → %s' % r.status_code)
tikrink(any('parduot' in z for z in zinutes(r)),
        'nėra žinutės apie parduotą skelbimą: %s' % zinutes(r))


# ═══════════════════════════════════════════════════════════════════
antraste('5. Sugadintas pateikimas irgi ne 500')

vel_pasibaiges = skelbimas('expired')
for zyme, duom in (('plan_id=abc', {'plan_id': 'abc'}),
                   ('plan_id tuščias', {'plan_id': ''}),
                   ('be plan_id', {}),
                   ('nesamas plan_id', {'plan_id': '987654'})):
    url, r = atidaryk(savas, vel_pasibaiges.pk, 'post', **duom)
    tikrink(r.status_code == 200, '%s → %s' % (zyme, r.status_code))
    tikrink(any('plan' in z.lower() for z in zinutes(r)),
            '%s: nėra žinutės apie planą' % zyme)
    vel_pasibaiges.refresh_from_db()
    tikrink(vel_pasibaiges.status == 'expired',
            '%s: skelbimas aktyvuotas be galiojančio plano!' % zyme)

# kategorija be planų — žinutė, o ne tuščias puslapis su neveikiančiu mygtuku
be_planu = skelbimas('expired', vt=TUSCIA_VT)
url, r = atidaryk(savas, be_planu.pk)
tikrink(r.status_code == 200, 'be planų → %s' % r.status_code)
tikrink(any('planų' in z for z in zinutes(r)),
        'nėra žinutės, kad planų nėra: %s' % zinutes(r))


# ═══════════════════════════════════════════════════════════════════
antraste('6. Laiško nuoroda veda į tą patį adresą')

komanda = io.open(os.path.join(BASE,
                  'apps/listings/management/commands/send_draft_reminders.py'),
                  encoding='utf-8').read()
tikrink('/activation-plans/' in komanda,
        'priminimo laiškas nebeveda į aktyvavimo puslapį')
for f in ('draft_reminder_first.html', 'draft_reminder_daily.html'):
    t = io.open(os.path.join(BASE, 'templates/emails', f), encoding='utf-8').read()
    tikrink('{{ activation_url }}' in t, '%s: nėra aktyvavimo nuorodos' % f)


print('\n' + '═' * 60)
print('gerai: %d, nepavyko: %d' % (gerai, blogai))
sys.exit(1 if blogai else 0)
