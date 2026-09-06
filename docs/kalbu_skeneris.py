# -*- coding: utf-8 -*-
"""
AR KIEKVIENA KALBA TIKRAI VEIKIA — be lietuviškų likučių.

Du matavimai:

  1. KATALOGAI. Kiek procentų msgid'ų turi vertimą (fuzzy neskaičiuojam:
     jie į .mo nepatenka ir vartotojui nerodomi).
  2. PUSLAPIAI. Atidarom kelis pagrindinius adresus kiekviena kalba ir
     ieškom lietuviškų raidžių (ą č ę ė į š ų ū ž) TEN, kur jų būti
     negali. Naudotojų duomenys (skelbimų pavadinimai, miestai, markės,
     žmonių vardai) į matavimą neįeina — jie lietuviški teisėtai.

    python docs/kalbu_skeneris.py            # abu matavimai
    python docs/kalbu_skeneris.py --tik-po   # tik katalogai (be DB)
"""
import os
import re
import sys
import tempfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

try:
    import polib
except ImportError:
    sys.exit('Reikia polib: pip install polib')

LT_RAIDES = re.compile('[ąčęėįšųūžĄČĘĖĮŠŲŪŽ]')

# Kalbų perjungiklis rodo pavadinimus GIMTĄJA kalba — „Lietuvių" ten yra
# teisingas užrašas bet kuria sąsajos kalba, o ne likutis.
GIMTIEJI = set()

# Elementai, kurių turinys ateina iš DB — juose lietuviški vardai teisėti
DUOMENU_ZYMES = ('script', 'style', 'noscript')


def po_kelias(kalba):
    return os.path.join(BASE, 'locale', kalba, 'LC_MESSAGES', 'django.po')


def kalbos():
    saknis = os.path.join(BASE, 'locale')
    return sorted(k for k in os.listdir(saknis) if os.path.exists(po_kelias(k)))


def katalogo_bukle(kalba):
    """(iš viso, išversta, fuzzy, procentai)."""
    po = polib.pofile(po_kelias(kalba))
    eilutes = [e for e in po if not e.obsolete]
    # Daugiskaitos įrašas laikomas išverstu, kai užpildytos VISOS formos
    isversta = 0
    fuzzy = 0
    for e in eilutes:
        if 'fuzzy' in e.flags:
            fuzzy += 1
            continue
        if e.msgid_plural:
            formos = (e.msgstr_plural or {}).values()
            if formos and all(v for v in formos):
                isversta += 1
        elif e.msgstr:
            isversta += 1
    viso = len(eilutes)
    return viso, isversta, fuzzy, 100.0 * isversta / max(1, viso)


def tekstas_be_duomenu(html):
    """Puslapio tekstas be scriptų, stilių ir naudotojų duomenų sričių."""
    from django.utils.html import strip_tags
    # Elementai, pažymėti data-duomenys → naudotojų turinys, praleidžiam
    html = re.sub(r'<(%s)\b.*?</\1>' % '|'.join(DUOMENU_ZYMES), ' ', html,
                  flags=re.S | re.I)
    html = re.sub(r'<[^>]+data-duomenys[^>]*>.*?</[a-zA-Z]+>', ' ', html, flags=re.S)
    html = re.sub(r'<!--.*?-->', ' ', html, flags=re.S)
    return strip_tags(html)


def main():
    tik_po = '--tik-po' in sys.argv

    print('KATALOGAI')
    print('%-10s %7s %9s %7s %7s' % ('kalba', 'msgid', 'išversta', 'fuzzy', '%'))
    bukles = {}
    for k in kalbos():
        viso, isversta, fuzzy, proc = katalogo_bukle(k)
        bukles[k] = proc
        print('%-10s %7d %9d %7d %6.1f%%' % (k, viso, isversta, fuzzy, proc))

    if tik_po:
        return 0

    # ── Puslapiai ──────────────────────────────────────────────────
    for kintamasis, reiksme in (('SECRET_KEY', 'x'), ('EMAIL_USER', 'x@x.lt'),
                                ('EMAIL_PASSWORD', 'x')):
        os.environ.setdefault(kintamasis, reiksme)
    import django
    from django.conf import settings
    laikina = tempfile.mkdtemp(prefix='skeneris-')
    import config.settings as pagrindas
    n = {k: v for k, v in vars(pagrindas).items() if k.isupper()}
    n.update(
        DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3',
                               'NAME': os.path.join(laikina, 'db.sqlite3')}},
        SECURE_SSL_REDIRECT=False, SESSION_COOKIE_SECURE=False,
        CSRF_COOKIE_SECURE=False, SECURE_HSTS_SECONDS=0,
        MEDIA_ROOT=laikina, DEBUG=False, ALLOWED_HOSTS=['*'],
        EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
        CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}},
        STORAGES={'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
                  'staticfiles': {'BACKEND':
                                  'django.contrib.staticfiles.storage.StaticFilesStorage'}},
    )
    settings.configure(**n)
    django.setup()
    from django.core.management import call_command
    call_command('migrate', run_syncdb=True, verbosity=0)
    from django.test import Client
    from apps.listings.templatetags.kalbu_tags import PAVADINIMAI
    GIMTIEJI.update(PAVADINIMAI.values())

    KELIAI = ['/', '/skelbimai/', '/imones/']
    print('\nPUSLAPIAI — lietuviškos raidės ten, kur neturėtų būti')
    print('%-10s %-16s %8s  %s' % ('kalba', 'kelias', 'likučių', 'pavyzdys'))
    blogai = 0
    for k in kalbos():
        # Django kalbos kodas: katalogas zh_Hans → kalba zh-hans
        kodas = k.replace('_', '-').lower()
        priesdelis = '' if kodas == settings.LANGUAGE_CODE else '/' + kodas
        for kelias in KELIAI:
            c = Client()
            c.cookies['django_language'] = kodas
            r = c.get(priesdelis + kelias)
            if r.status_code != 200:
                print('%-10s %-16s %8s  atsakymas %s' % (k, kelias, '—', r.status_code))
                blogai += 1
                continue
            tekstas = tekstas_be_duomenu(r.content.decode('utf-8'))
            radiniai = [ž for ž in re.findall(r'\S+', tekstas)
                        if LT_RAIDES.search(ž) and ž.strip('·,()') not in GIMTIEJI]
            if kodas == settings.LANGUAGE_CODE:
                continue                     # lietuviškame puslapyje jos vietoj
            pavyzdys = ' '.join(sorted(set(radiniai))[:5])
            print('%-10s %-16s %8d  %s' % (k, kelias, len(radiniai), pavyzdys[:70]))
    return 1 if blogai else 0


if __name__ == '__main__':
    sys.exit(main())
