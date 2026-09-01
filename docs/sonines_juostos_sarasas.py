# -*- coding: utf-8 -*-
"""
ŠONINĖS JUOSTOS TURINIO IŠRAŠAS — įrodymas, kad pertvarkius išvaizdą
filtrai nepasikeitė.

Išveda filtrus EILĖS TVARKA, kaip juos mato naršyklė: kiekvienas laukas
su vardu, tipu ir reikšmių skaičiumi, plius antraštės, nuorodos ir
mygtukai. Nieko apie stilių — tik turinys ir tvarka.

    python docs/sonines_juostos_sarasas.py > /tmp/pries.txt
    ...pertvarkom išvaizdą...
    python docs/sonines_juostos_sarasas.py > /tmp/po.txt
    diff /tmp/pries.txt /tmp/po.txt        # turi būti tuščia

Kategorijų imam kelias, nes juostą sudeda search_config.panels pagal
kategoriją — vienos neužtenka.
"""
import os, re, sys, shutil, tempfile
from html.parser import HTMLParser

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
for k, v in (('SECRET_KEY', 'x'), ('EMAIL_USER', 'x@x.lt'), ('EMAIL_PASSWORD', 'x')):
    os.environ.setdefault(k, v)

import django
from django.conf import settings

LAIKINA = tempfile.mkdtemp(prefix='juosta-')
import config.settings as pagrindas
n = {k: v for k, v in vars(pagrindas).items() if k.isupper()}
n.update(
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3',
                           'NAME': os.path.join(LAIKINA, 'db.sqlite3')}},
    SECURE_SSL_REDIRECT=False, SESSION_COOKIE_SECURE=False,
    CSRF_COOKIE_SECURE=False, SECURE_HSTS_SECONDS=0, MEDIA_ROOT=LAIKINA,
    DEBUG=False, ALLOWED_HOSTS=['*'],
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    STORAGES={'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
              'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'}},
    CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}},
)
settings.configure(**n)
django.setup()
from django.core.management import call_command
call_command('migrate', run_syncdb=True, verbosity=0)

from django.contrib.auth import get_user_model
from django.test import Client
from django.utils import timezone
from apps.listings.models import Listing, VehicleType

U = get_user_model()
u = U.objects.create_user(username='p', email='p@x.lt', password='x')

def _butini(model):
    out = {}
    for f in model._meta.concrete_fields:
        if (f.primary_key or f.null or f.blank or f.has_default() or f.auto_created
                or getattr(f, 'auto_now', False) or getattr(f, 'auto_now_add', False)):
            continue
        it = f.get_internal_type()
        if it.endswith('IntegerField'): out[f.name] = 0
        elif it in ('DecimalField', 'FloatField'): out[f.name] = 0
        elif it in ('CharField', 'TextField', 'SlugField', 'EmailField', 'URLField'): out[f.name] = ''
        elif it == 'BooleanField': out[f.name] = False
        elif it in ('DateTimeField', 'DateField'): out[f.name] = timezone.now()
    return out

B = _butini(Listing)
KATEGORIJOS = ['cars', 'motorcycles', 'trucks', 'boats', 'trailers',
               'agriculture', 'construction', 'bicycles', 'services', 'rental']
for slug in KATEGORIJOS:
    vt, _ = VehicleType.objects.get_or_create(
        slug=slug, defaults={'name': slug.title()})
    d = dict(B)
    d.update(seller=u, vehicle_type=vt, title='%s 1' % slug, price=5000,
             year=2018, status='active', country='LT', city='Vilnius')
    Listing.objects.create(**d)


class Juosta(HTMLParser):
    """Ištraukia TIK <aside> viduje esantį turinį eilės tvarka."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.gylis = 0
        self.viduj = False
        self.eilutes = []
        self.tekstas = []
        self.laukia_teksto = None
        self.select = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'aside' and 'no-print' in (a.get('class') or ''):
            self.viduj = True
            self.gylis = 0
        if not self.viduj:
            return
        if tag == 'aside':
            self.gylis += 1
        if tag == 'form':
            self.eilutes.append('FORMA method=%s action=%s'
                                % (a.get('method'), a.get('action')))
        elif tag == 'input':
            self.eilutes.append('LAUKAS input type=%s name=%s value=%s'
                                % (a.get('type'), a.get('name'), a.get('value')))
        elif tag == 'select':
            self.select = {'name': a.get('name'), 'kiek': 0}
        elif tag == 'option' and self.select is not None:
            self.select['kiek'] += 1
        elif tag == 'textarea':
            self.eilutes.append('LAUKAS textarea name=%s' % a.get('name'))
        elif tag == 'button':
            self.laukia_teksto = ('MYGTUKAS type=%s' % a.get('type'), [])
        elif tag == 'a':
            self.laukia_teksto = ('NUORODA href=%s' % a.get('href'), [])
        elif tag in ('h4', 'label', 'legend'):
            self.laukia_teksto = ('ANTRAŠTĖ <%s>' % tag, [])

    def handle_endtag(self, tag):
        if not self.viduj:
            return
        if tag == 'select' and self.select is not None:
            self.eilutes.append('LAUKAS select name=%s reikšmių=%d'
                                % (self.select['name'], self.select['kiek']))
            self.select = None
        if self.laukia_teksto and tag in ('button', 'a', 'h4', 'label', 'legend'):
            pav, t = self.laukia_teksto
            tekstas = re.sub(r'\s+', ' ', ''.join(t)).strip()
            self.eilutes.append('%s · %s' % (pav, tekstas[:60]))
            self.laukia_teksto = None
        if tag == 'aside':
            self.gylis -= 1
            if self.gylis <= 0:
                self.viduj = False

    def handle_data(self, data):
        if self.viduj and self.laukia_teksto:
            self.laukia_teksto[1].append(data)


c = Client()
for slug in KATEGORIJOS:
    r = c.get('/?section=%s&sidebar=1&category=%s' % (slug, slug))
    p = Juosta()
    p.feed(r.content.decode())
    print('═' * 66)
    print('KATEGORIJA: %s   (HTTP %s)' % (slug, r.status_code))
    print('═' * 66)
    for i, e in enumerate(p.eilutes, 1):
        print('%3d. %s' % (i, e))
    print()

shutil.rmtree(LAIKINA, ignore_errors=True)
