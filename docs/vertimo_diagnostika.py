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
# Du keliai: JSON failas arba API raktas (žr. docs/vertimo-raktas.md).
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

from apps.conversations.translate_service import _api_raktas, _rakto_failas
raktas = _api_raktas()
print('   API raktas:   %s' % ('YRA (…%s)' % raktas[-4:] if raktas else 'NĖRA'))
print('   kelias:       %s' % ('JSON failas' if _rakto_failas()
                               else ('API raktas' if raktas else 'NĖRA NĖ VIENO')))
if not _rakto_failas() and not raktas:
    print('   Taisymas:     .env → GOOGLE_TRANSLATE_API_KEY=… ; '
          'žr. docs/vertimo-raktas.md')

# ── 3. Lentelė ─────────────────────────────────────────────────────
from apps.conversations.models import MessageTranslation
try:
    print('3. lentelė:      YRA, įrašų %d' % MessageTranslation.objects.count())
except Exception as e:
    print('3. lentelė:      NĖRA — %s: %s' % (type(e).__name__, e))
    print('   Taisymas:     python manage.py migrate')

# ── 4. Tikras kvietimas ────────────────────────────────────────────
# Kviečiam TĄ PATĮ kelią, kurį naudoja svetainė (_versk), kad diagnostika
# nemeluotų apie kitą kelią nei tikrasis.
from apps.conversations.translate_service import _versk
try:
    r = _versk(['Labas'], 'en')
    print('4. API:          VEIKIA → %r' % (r[0].get('translatedText') if r else None))
except Exception as e:
    print('4. API:          NEATSAKO — %s: %s' % (type(e).__name__, e))
    print('   VertimoNera             → nėra nei failo, nei rakto;')
    print('   403 „has not been used" → Cloud Translation API neįjungtas projekte;')
    print('   403 „referer/API_KEY"   → raktas apribotas (Maps-only arba HTTP referrer);')
    print('   429                     → viršyta kvota;')
    print('   DefaultCredentialsError → JSON failas nurodytas, bet netinka.')
    print('   Žr. docs/vertimo-raktas.md')
