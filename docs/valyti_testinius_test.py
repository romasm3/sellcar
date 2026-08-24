# -*- coding: utf-8 -*-
"""
valyti_testinius — testas su tikrais modeliais ir tikrais failais.

Laikina sqlite atmintyje + laikinas media katalogas. Produkcinės DB ir
media NELIEČIA.

Paleidimas:  python docs/valyti_testinius_test.py
"""
import os, sys, shutil, tempfile, django
from django.conf import settings

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
MEDIA = tempfile.mkdtemp(prefix='valymo-testas-')
os.environ.setdefault('SECRET_KEY', 'x')
settings.configure(
    DEBUG=True, USE_I18N=True, USE_L10N=True, USE_TZ=True, LANGUAGE_CODE='lt',
    SECRET_KEY='x', ALLOWED_HOSTS=['*'], ROOT_URLCONF='config.urls',
    STRIPE_SECRET_KEY='sk_test_fake',
    INSTALLED_APPS=[
        "django.contrib.admin", "django.contrib.auth", "django.contrib.contenttypes",
        "django.contrib.sessions", "django.contrib.messages", "django.contrib.staticfiles",
        "django.contrib.humanize", "django.contrib.sitemaps",
        "apps.accounts", "apps.listings", "apps.conversations", "apps.broadcasts",
        "apps.payments", "apps.analytics",
        "crispy_forms", "crispy_bootstrap4", "django_filters", "rosetta",
    ],
    MIDDLEWARE=[],
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}},
    DEFAULT_AUTO_FIELD='django.db.models.BigAutoField',
    STATIC_URL='/static/', MEDIA_URL='/media/', MEDIA_ROOT=MEDIA,
    TEMPLATES=[{'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [os.path.join(BASE, 'templates')], 'APP_DIRS': True,
                'OPTIONS': {'context_processors': []}}],
)
django.setup()
from django.core.management import call_command
call_command('migrate', run_syncdb=True, verbosity=0)

from io import StringIO
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.utils import timezone
from apps.listings.models import (Listing, ListingImage, VehicleType,
                                  SavedListing, ListingReport)

gerai = blogai = 0
def tikrink(salyga, ka):
    global gerai, blogai
    if salyga: gerai += 1
    else:
        blogai += 1
        print('  NEPAVYKO: ' + ka)

U = get_user_model()
testai = U.objects.create_user(username='testai', email='testai@autoleft.local', password='x')
adminas = U.objects.create_user(username='romasm3', email='romasm3@gmail.com', password='x')
pirkejas = U.objects.create_user(username='romasm333', email='romasm333@gmail.com', password='x')
VT = VehicleType.objects.create(name='Automobiliai', slug='cars')

def _butini(model):
    out = {}
    for f in model._meta.concrete_fields:
        if (f.primary_key or f.null or f.blank or f.has_default() or f.auto_created
                or getattr(f, 'auto_now', False) or getattr(f, 'auto_now_add', False)):
            continue
        it = f.get_internal_type()
        if it.endswith('IntegerField'): out[f.name] = 0
        elif it in ('DecimalField', 'FloatField'): out[f.name] = 0
        elif it in ('CharField','TextField','SlugField','EmailField','URLField'): out[f.name] = ''
        elif it == 'BooleanField': out[f.name] = False
        elif it in ('DateTimeField','DateField'): out[f.name] = timezone.now()
    return out

BAZE = _butini(Listing)

def skelbimas(**kw):
    d = dict(BAZE); d.update(vehicle_type=VT, status='active', year=2018)
    d.update(kw)
    return Listing.objects.create(**d)

def nuotrauka(l, vardas):
    img = ListingImage(listing=l)
    img.image.save(vardas, ContentFile(b'JPEGDATA'), save=False)
    img.image_sm.save('sm-' + vardas, ContentFile(b'SMDATA'), save=False)
    img.save()
    return [img.image.path, img.image_sm.path]

# ── Duomenys: po vieną kiekvienai šakai ──────────────────────────────
t1 = skelbimas(seller=adminas, title='BMW 320d [TEST]', price=15900,
               description='TESTINIS SKELBIMAS — sukurta automatiškai, galima trinti.')
t2 = skelbimas(seller=adminas, title='Audi A6 2019', price=12000,
               description='Nice car. <!-- __SEEDED_FAKE__ -->')
t3 = skelbimas(seller=testai, title='Honda CB500F', price=5200,
               description='Paprastas aprašymas apie motociklą, pakankamai ilgas.')
t4 = skelbimas(seller=adminas, title='Opel Astra [test]', price=3000,
               description='Aprašymas pakankamai ilgas, kad nepatektų į klaustukus.')

k1 = skelbimas(seller=adminas, title='aaa', price=5000,
               description='Aprašymas pakankamai ilgas, kad nebūtų dėl ilgio.')
k2 = skelbimas(seller=adminas, title='Nissan Qashqai', price=1,
               description='Aprašymas pakankamai ilgas, kad nebūtų dėl ilgio.')
k3 = skelbimas(seller=adminas, title='Toyota Yaris', price=4500, description='trumpai')
k4 = skelbimas(seller=pirkejas, title='Mano Volkswagen Golf VII', price=8900,
               description='Tikrai geras automobilis, aprašymas ilgas ir prasmingas.')

r1 = skelbimas(seller=adminas, title='Mercedes-Benz E220 CDI', price=11500,
               description='Tvarkingas automobilis, aptarnautas, be defektų — tikras skelbimas.')
# „Testarossa", „Assist", „naujas BMW" prasideda įtartinais žodžiais —
# tikrinamas VISAS pavadinimas, ne dalis, todėl jie lieka tikri.
r2 = skelbimas(seller=adminas, title='Testarossa replika', price=25000,
               description='Ferrari Testarossa replika, pilnas aprašymas ir istorija.')
r3 = skelbimas(seller=adminas, title='Škoda Octavia', price=1, description='')  # klaustukas: 1€ + be nuotr.

failai_t1 = nuotrauka(t1, 't1.jpg')
failai_r1 = nuotrauka(r1, 'r1.jpg')
failai_r2 = nuotrauka(r2, 'r2.jpg')
nuotrauka(k1, 'k1.jpg')       # kad k1 nepatektų dėl „be nuotraukų"

SavedListing.objects.create(user=pirkejas, listing=t1)
ListingReport.objects.create(listing=t1, reason='spam', reporter_email='x@x.lt')

print('── 1. Sąrašas (nieko nekeičia) ───────────────────────────────')
buvo = Listing.objects.count()
isv = StringIO()
call_command('valyti_testinius', stdout=isv)
tekstas = isv.getvalue()
tikrink(Listing.objects.count() == buvo, 'sąrašas nieko neištrynė')
for l in (t1, t2, t3, t4, k1, k2, k3, k4, r1, r2, r3):
    tikrink(('Listing %-6s' % l.pk).split()[1] in tekstas or str(l.pk) in tekstas,
            'lentelėje yra #%s' % l.pk)
tikrink('Iš viso 11' in tekstas, 'suskaičiuoti visi 11: ' +
        [x for x in tekstas.splitlines() if x.startswith('Iš viso')][:1].__str__())

print('── 2. Klasifikacija ──────────────────────────────────────────')
from apps.listings.management.commands.valyti_testinius import ivertinti
def v(l, n=0):
    return ivertinti(l, 'Listing', n)[0]
tikrink(v(t1, 1) == 'testinis', 't1 „TESTINIS SKELBIMAS" → testinis')
tikrink(v(t2) == 'testinis', 't2 __SEEDED_FAKE__ → testinis')
tikrink(v(t3) == 'testinis', 't3 testai@autoleft.local → testinis')
tikrink(v(t4) == 'testinis', 't4 [test] pavadinime → testinis')
tikrink(v(k1, 1) == 'klaustukas', 'k1 „aaa" → klaustukas')
tikrink(v(k2) == 'klaustukas', 'k2 1 € be nuotraukų → klaustukas')
tikrink(v(k3) == 'klaustukas', 'k3 be nuotraukų, trumpas aprašymas → klaustukas')
tikrink(v(k4) == 'klaustukas', 'k4 romasm333 → klaustukas')
tikrink(v(r1, 1) == 'tikras', 'r1 → tikras')
tikrink(v(r2, 2) == 'tikras', 'r2 „Testarossa" NĖRA testinis')
from apps.listings.management.commands.valyti_testinius import ITARTINI_PAVADINIMAI as RE
for pav, itartinas in [('test', True), ('TEST', True), ('aaa', True), ('asd', True),
                       ('qwe123', True), ('123', True), ('bandymas', True), ('xxx', True),
                       ('Testarossa replika', False), ('Assist', False),
                       ('naujas BMW', False), ('Toyota Yaris', False),
                       ('Audi A6 2019', False)]:
    tikrink(bool(RE.match(pav)) == itartinas, 'pavadinimas %r → %s' % (pav, itartinas))
tikrink(v(r3) == 'klaustukas', 'r3 1 € be nuotraukų → klaustukas')

print('── 3. --trinti be --tikrai ───────────────────────────────────')
from django.core.management.base import CommandError
try:
    call_command('valyti_testinius', trinti=True, stdout=StringIO())
    tikrink(False, '--trinti be --tikrai turi mesti klaidą')
except CommandError:
    tikrink(Listing.objects.count() == buvo, '--trinti be --tikrai nieko neištrynė')

print('── 4. Trynimas ───────────────────────────────────────────────')
tikrink(all(os.path.exists(p) for p in failai_t1), 'prieš: t1 failai diske')
isv = StringIO()
call_command('valyti_testinius', trinti=True, tikrai=True, be_kopijos=True, stdout=isv)
tekstas = isv.getvalue()

liko = set(Listing.objects.values_list('pk', flat=True))
tikrink(liko == {k1.pk, k2.pk, k3.pk, k4.pk, r1.pk, r2.pk, r3.pk},
        'ištrinti tik 4 testiniai, liko %s' % sorted(liko))
tikrink(not any(os.path.exists(p) for p in failai_t1), 't1 nuotraukos pašalintos nuo disko')
tikrink(all(os.path.exists(p) for p in failai_r1), 'r1 nuotraukos NEPALIESTOS')
tikrink(all(os.path.exists(p) for p in failai_r2), 'r2 nuotraukos NEPALIESTOS')
tikrink(SavedListing.objects.filter(listing_id=t1.pk).count() == 0, 'saved išvalyta (cascade)')
tikrink(ListingReport.objects.filter(listing_id=t1.pk).count() == 0, 'reports išvalyta (cascade)')
tikrink(ListingImage.objects.filter(listing_id=t1.pk).count() == 0, 'images eilutės išvalytos')
tikrink('KLAUSTUKAI' in tekstas, 'ataskaitoje yra klaustukų sąrašas')
tikrink('IŠTRINTA 4' in tekstas, 'ataskaitoje „IŠTRINTA 4"')

print('── 5. Klaustukas per --id ────────────────────────────────────')
isv = StringIO()
call_command('valyti_testinius', trinti=True, tikrai=True, be_kopijos=True,
             id='Listing:%d' % k1.pk, stdout=isv)
tikrink(not Listing.objects.filter(pk=k1.pk).exists(), 'k1 ištrintas nurodžius --id')
tikrink(Listing.objects.filter(pk=k4.pk).exists(), 'k4 (nenurodytas) liko')
tikrink(Listing.objects.filter(pk=r1.pk).exists(), 'r1 liko')

print('── 6. Be kopijos negalima (PostgreSQL patikra) ───────────────')
try:
    call_command('valyti_testinius', trinti=True, tikrai=True,
                 id='Listing:%d' % k2.pk, stdout=StringIO())
    tikrink(False, 'be PostgreSQL pg_dump turi mesti klaidą')
except CommandError as e:
    tikrink('pg_dump' in str(e), 'aiški klaida apie pg_dump: %s' % e)
    tikrink(Listing.objects.filter(pk=k2.pk).exists(), 'nepavykus kopijai NIEKAS neištrinta')

shutil.rmtree(MEDIA, ignore_errors=True)
print('\n' + '═' * 64)
print('gerai: %d, nepavyko: %d' % (gerai, blogai))
sys.exit(1 if blogai else 0)
