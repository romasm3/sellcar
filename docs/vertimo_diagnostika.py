# -*- coding: utf-8 -*-
"""
KODĖL NEVEIKIA VERTIMAS — paleisti SERVERYJE.

Atsako į tą patį klausimą, kurio kitaip reikia ieškoti žurnaluose:
ar įdiegtas paketas, ar yra raktas, ar yra lentelė, ar atsako API.

    cd /root/autoleft && source venv/bin/activate
    python docs/vertimo_diagnostika.py
"""
import os, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

print('python:', sys.executable)

# ── 1. Paketas ─────────────────────────────────────────────────────
try:
    from google.cloud import translate_v2                      # noqa: F401
    import google.cloud.translate_v2 as tv
    print('1. paketas:      YRA  (%s)' % getattr(tv, '__file__', '?'))
    paketas = True
except Exception as e:
    print('1. paketas:      NĖRA — %s: %s' % (type(e).__name__, e))
    print('   Taisymas:     pip install -r requirements.txt && systemctl restart gunicorn')
    paketas = False

# ── 2. Raktas ──────────────────────────────────────────────────────
import django
try:
    django.setup()
except Exception as e:
    print('   django.setup() nulūžo: %s: %s' % (type(e).__name__, e))
    raise SystemExit(1)

from django.conf import settings
kelias = getattr(settings, 'GOOGLE_CREDENTIALS_PATH', None)
env = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', '')
print('2. rakto kelias: %s' % kelias)
print('   failas yra:   %s' % (os.path.isfile(str(kelias)) if kelias else False))
print('   env GOOGLE_APPLICATION_CREDENTIALS: %r' % env)
if env and not os.path.isfile(env):
    print('   DĖMESIO: env rodo į neegzistuojantį failą')

# ── 3. Lentelė ─────────────────────────────────────────────────────
from apps.conversations.models import MessageTranslation
try:
    print('3. lentelė:      YRA, įrašų %d' % MessageTranslation.objects.count())
except Exception as e:
    print('3. lentelė:      NĖRA — %s: %s' % (type(e).__name__, e))
    print('   Taisymas:     python manage.py migrate')

# ── 4. Tikras kvietimas ────────────────────────────────────────────
if paketas:
    try:
        from google.cloud import translate_v2 as translate
        c = translate.Client()
        r = c.translate(['Labas'], target_language='en', format_='text')
        print('4. API:          VEIKIA → %r' % r[0].get('translatedText'))
    except Exception as e:
        print('4. API:          NEATSAKO — %s: %s' % (type(e).__name__, e))
        print('   DefaultCredentialsError → nėra rakto;')
        print('   Forbidden/PermissionDenied → API neįjungtas projekte arba nėra teisių;')
        print('   ResourceExhausted → kvota.')
else:
    print('4. API:          netikrinta (nėra paketo)')
