"""Apsauga nuo botų registracijos ir slaptažodžių spėliojimo.

Viskas laikoma vienoje vietoje, kad registracijos ir prisijungimo vaizdai
liktų trumpi, o ribos — vienodos. El. pašto patvirtinimo (dar) nedarom,
todėl čia yra keturi barjerai:

  • honeypot — nematomas laukas, kurį užpildo tik botai;
  • registracijų riba iš vieno IP (REGISTRACIJU_RIBA per valandą);
  • vienadienių („disposable") pašto domenų sąrašas;
  • prisijungimo bandymų riba (LOGIN_RIBA per LOGIN_LANGAS minučių).

Skaitikliai gyvena talpykloje (django.core.cache), todėl DB nekraunam ir
duomenys savaime pasensta.
"""

from django.core.cache import cache
from django.utils.translation import gettext_lazy as _

# ── Ribos ───────────────────────────────────────────────────────────
REGISTRACIJU_RIBA = 3            # registracijų per valandą iš vieno IP
REGISTRACIJU_LANGAS = 60 * 60    # sekundėmis

LOGIN_RIBA = 5                   # nepavykusių bandymų
LOGIN_LANGAS = 15 * 60           # per 15 min.

# Honeypot lauko vardas — toks pat kaip pranešimo apie skelbimą formoje.
HONEYPOT = 'website'

# Vienadieniai domenai, kurių nėra bibliotekos sąraše (mūsų spam'as).
PAPILDOMI_DOMENAI = {
    'immenseignite.info',
}

ZINUTES = {
    'disposable': _('Naudokite nuolatinį el. pašto adresą'),
    'per_daug_registraciju': _(
        'Per valandą iš vieno adreso galima sukurti ne daugiau kaip '
        '%(kiek)s paskyras. Bandykite vėliau.'),
    'login_blokas': _(
        'Per daug nepavykusių bandymų. Pabandykite po %(minutes)s min.'),
}


def _blocklist():
    """Vienadienių domenų sąrašas (biblioteka + mūsų papildymai)."""
    try:
        from disposable_email_domains import blocklist
    except ImportError:          # paketo nėra — lieka rankinis sąrašas
        blocklist = set()
    return blocklist


def domenas_vienadienis(email):
    """Ar el. pašto domenas yra laikinos pašto dėžutės."""
    if not email or '@' not in email:
        return False
    domenas = email.rsplit('@', 1)[1].strip().lower()
    if domenas in PAPILDOMI_DOMENAI:
        return True
    return domenas in _blocklist()


def kliento_ip(request):
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    if xff:
        return xff.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '')


def naudotojo_narsykle(request):
    return (request.META.get('HTTP_USER_AGENT') or '')[:400]


def honeypot_uzpildytas(request):
    return bool((request.POST.get(HONEYPOT) or '').strip())


# ── Registracijų skaitiklis ─────────────────────────────────────────

def _reg_raktas(ip):
    return f'antispam:reg:{ip}'


def registraciju_per_valanda(ip):
    return cache.get(_reg_raktas(ip), 0) if ip else 0


def registraciju_riba_virsyta(ip):
    return bool(ip) and registraciju_per_valanda(ip) >= REGISTRACIJU_RIBA


def zymeti_registracija(ip):
    if not ip:
        return
    raktas = _reg_raktas(ip)
    kiek = cache.get(raktas, 0) + 1
    cache.set(raktas, kiek, REGISTRACIJU_LANGAS)


# ── Prisijungimo bandymai ───────────────────────────────────────────

def _login_raktas(ip):
    return f'antispam:login:{ip}'


def login_bandymai(ip):
    return cache.get(_login_raktas(ip), 0) if ip else 0


def login_uzblokuotas(ip):
    return bool(ip) and login_bandymai(ip) >= LOGIN_RIBA


def zymeti_nepavykusi_login(ip):
    if not ip:
        return
    raktas = _login_raktas(ip)
    kiek = cache.get(raktas, 0) + 1
    cache.set(raktas, kiek, LOGIN_LANGAS)


def valyti_login_bandymus(ip):
    """Sėkmingas prisijungimas skaitiklį nuvalo."""
    if ip:
        cache.delete(_login_raktas(ip))
