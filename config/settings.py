import os
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

# ═══════════════════════════════════════════════════════════
# GOOGLE TRANSLATE API
# ═══════════════════════════════════════════════════════════
# Nustatom TIK jei raktas realiai yra — anksčiau env kintamasis
# rodė į neegzistuojantį failą.
GOOGLE_CREDENTIALS_PATH = Path(config(
    "GOOGLE_APPLICATION_CREDENTIALS",
    default=str(BASE_DIR / "google-translate-key.json"),
))
if GOOGLE_CREDENTIALS_PATH.is_file():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(GOOGLE_CREDENTIALS_PATH)

# Antras kelias — paprastas API raktas. JSON rakto failo serveryje nėra,
# o .env jau turi Google raktą, tad vertimas gali dirbti ir su juo
# (žr. docs/vertimo-raktas.md). Pirmenybė — savas GOOGLE_TRANSLATE_API_KEY;
# jo nesant imamas GOOGLE_MAPS_API_KEY iš to paties projekto.
GOOGLE_TRANSLATE_API_KEY = config("GOOGLE_TRANSLATE_API_KEY", default="")

# Be default'o — jei .env nepasiekiamas, startas krenta garsiai,
# o ne pakyla su viešai žinomu raktu.
SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost,127.0.0.1").split(",")

# ═══════════════════════════════════════════════════════════
# HTTPS / saugūs slapukai
# ═══════════════════════════════════════════════════════════
# nginx terminuoja TLS ir perduoda X-Forwarded-Proto (proxy_params).
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Prod'e (DEBUG=False) įjungta, lokaliai — išjungta automatiškai.
# Kiekvieną galima perrašyti per .env.
_SECURE_DEFAULT = not DEBUG
SESSION_COOKIE_SECURE = config("SESSION_COOKIE_SECURE", default=_SECURE_DEFAULT, cast=bool)
CSRF_COOKIE_SECURE = config("CSRF_COOKIE_SECURE", default=_SECURE_DEFAULT, cast=bool)
SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=_SECURE_DEFAULT, cast=bool)

# CSRF patikimi šaltiniai. Django 4+ per HTTPS lygina Origin antraštę su
# host'u, todėl POST iš www.autoleft.com į autoleft.com (arba atvirkščiai,
# per nginx 301) baigiasi „CSRF verification failed". Sąrašą sudedam iš
# ALLOWED_HOSTS, kad nereikėtų prižiūrėti dviejose vietose.
CSRF_TRUSTED_ORIGINS = [
    f"https://{h}" for h in ALLOWED_HOSTS if h not in ("*",)
] + [f"http://{h}" for h in ALLOWED_HOSTS if h in ("localhost", "127.0.0.1")]

# Nepavykusio CSRF priežastis į žurnalą — kitą kartą nereikės spėlioti,
# kuri forma ir kodėl.
CSRF_FAILURE_VIEW = "apps.accounts.views.csrf_failure"

# HSTS — pradedam nuo 1 val. Kai įsitikinam, kad viskas per HTTPS,
# keliam iki 31536000 ir tik tada svarstom subdomains/preload.
SECURE_HSTS_SECONDS = config(
    "SECURE_HSTS_SECONDS", default=3600 if _SECURE_DEFAULT else 0, cast=int
)
SECURE_HSTS_INCLUDE_SUBDOMAINS = config(
    "SECURE_HSTS_INCLUDE_SUBDOMAINS", default=False, cast=bool
)
SECURE_HSTS_PRELOAD = config("SECURE_HSTS_PRELOAD", default=False, cast=bool)

# Stripe — leave empty until ready to enable payments
STRIPE_PUBLISHABLE_KEY = config("STRIPE_PUBLISHABLE_KEY", default="")
STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY", default="")
STRIPE_WEBHOOK_SECRET = config("STRIPE_WEBHOOK_SECRET", default="")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.sitemaps",
    # Local apps
    "apps.accounts",
    "apps.listings",
    "apps.imones",
    "apps.conversations",
    "apps.broadcasts",
    "apps.payments",
    "apps.analytics",
    # Third party apps
    "crispy_forms",
    "crispy_bootstrap4",
    "django_filters",
    "rosetta",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    # HTML atsakymai — „pasitikslink prieš rodydamas" (apps/listings/kesavimas.py)
    "apps.listings.kesavimas.HtmlBeKesoMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "apps.accounts.middleware.UserLanguageMiddleware",
    # PO UserLanguageMiddleware: jis prisijungusiam įjungia profilio kalbą,
    # o be kalbos priešdėlio toks kelias nebeatitinka nė vieno maršruto
    # (404). Šitas nukreipia į /<kalba>/… Žr. apps/listings/kalbos_kelias.py
    "apps.listings.kalbos_kelias.KalbosKelioMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "apps.analytics.middleware.VisitorTrackingMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
                # LANGUAGES ir LANGUAGE_CODE šablonams (kalbos perjungiklis,
                # <html lang>). Be jo LANGUAGE_CODE buvo tuščias ir visi
                # puslapiai skelbdavosi angliškais.
                "django.template.context_processors.i18n",
                "apps.conversations.context_processors.unread_messages",
                "apps.listings.context_processors.saved_searches_count",
                "apps.listings.context_processors.saved_listings_count",
                "apps.listings.context_processors.search_panel_tab",
                "apps.listings.context_processors.device_kind",
                # Privalomų laukų klaidos šablonuose: error_fields / error_messages
                "apps.listings.context_processors.form_error_fields",
                # Šalis — viena reikšmė visai svetainei (partials/_salis.html)
                "apps.listings.context_processors.salis",
                "apps.listings.context_processors.versija",
                "apps.listings.context_processors.rodymo_jungikliai",
                "apps.listings.context_processors.antrine_navigacija",
                "apps.listings.context_processors.antrastes_paieska",
                # Mokėjimų jungiklis: slepia piniginę ir kainų lenteles
                "apps.listings.context_processors.mokejimai",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME", default="sellcar_db"),
        "USER": config("DB_USER", default="postgres"),
        "PASSWORD": config("DB_PASSWORD", default="postgres"),
        "HOST": config("DB_HOST", default="localhost"),
        "PORT": config("DB_PORT", default="5432"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 8},
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
]


from django.utils.translation import gettext_lazy as _

LANGUAGE_CODE = "lt"
TIME_ZONE = "Europe/Vilnius"
USE_I18N = True
USE_L10N = True
USE_TZ = True
# Tūkstančių skirtuko iš Django lokalės NEIMAM.
#
# Komentaras čia anksčiau žadėjo „lt 5 000", bet Django lt lokalė skiria
# TAŠKU: intcomma(48320) → „48.320". Todėl įjungtas USE_THOUSAND_SEPARATOR
# gadino viską, kas renderinama plikai — metai virsdavo „2.018", o formų
# laukuose atsirasdavo „15.000 km", kurio nebeišsaugosi.
#
# Skaičius, kuriems tarpas TIKRAI reikalingas (kiekiai, peržiūros, rida,
# kainos), formatuojam patys per apps/listings/formatai.py — filtrai
# |sk ir |kaina duoda nedalomą tarpą lietuviškai ir kablelį angliškai.
# Metai, ID ir formų reikšmės lieka plikos, kaip ir turi būti.
USE_THOUSAND_SEPARATOR = False

# Kalbos perjungiklyje matomos VISOS, kurioms locale/ turi .po failą.
# 8dd8851 sąrašas buvo apkarpytas iki lt/en, o .po failai liko — grąžinta
# atgal visa trylika.
#
# Pavadinimai eina per gettext: msgid angliškas, o kiekviena kalba jį
# verčia savaip (lt.po: „Latvian" → „Latviešu"). Todėl angliškame
# puslapyje jie lieka angliški — to reikalauja ir vertimų sargyba
# (apps/imones/tests.py: /en/ puslapiuose lietuviškų raidžių būti negali).
#
# lt yra numatytoji ir adreso priešdėlio negauna (i18n_patterns su
# prefix_default_language=False), visos kitos gauna: /en/, /lv/, /ru/…
#
# DĖMESIO: lt ir en išverstos, likusios — apie 69 %. Neišverstos eilutės
# krenta į msgid, t. y. rodomos lietuviškai.
LANGUAGES = [
    ("lt", _("Lithuanian")),
    ("en", _("English")),
    ("lv", _("Latvian")),
    ("et", _("Estonian")),
    ("pl", _("Polish")),
    ("de", _("German")),
    ("ru", _("Russian")),
    ("fr", _("French")),
    ("es", _("Spanish")),
    ("zh-hans", _("Chinese")),
    ("vi", _("Vietnamese")),
    ("ar", _("Arabic")),
    ("ko", _("Korean")),
]

LOCALE_PATHS = [
    BASE_DIR / "locale",
]

# Language cookie — išlieka 1 metus
LANGUAGE_COOKIE_NAME = "django_language"
LANGUAGE_COOKIE_AGE = 60 * 60 * 24 * 365  # 1 metai (sekundėmis)
LANGUAGE_COOKIE_SAMESITE = "Lax"
LANGUAGE_COOKIE_HTTPONLY = False

# ═══════════════════════════════════════════════════════════
# VERSIJOS ŽYMĖ — kuri kodo versija TIKRAI sukasi
#
# Kiekvieno puslapio <head> gauna <meta name="versija" content="…">.
# Be jos neįmanoma iš šalies pasakyti, ar darbas pasiekė svetainę:
# 2026-09-01 keturi darbai iš eilės gulėjo master'yje, o deploy taimeris
# serveryje tyliai neveikė — nei žmogus, nei Claude to nematė.
#
# Iš kur imama, iš eilės:
#   1. APP_DIR/VERSIJA — failą rašo deploy-agent.sh po git pull.
#      Jis NEĮTRAUKTAS į EXCLUDES, tad keliauja kartu su snapshot'u:
#      atsukus kodą į last_good, grįžta ir TA PATI sena žyma, o ne nauja.
#   2. GIT_SHA aplinkos kintamasis — jei kas paleidžia be deploy skripto.
#   3. .git/HEAD — vietinėje aplinkoje, kur nei failo, nei kintamojo nėra.
#   4. „nezinoma" — geriau tuščia reikšmė nei melaginga.
# ═══════════════════════════════════════════════════════════
def _versija():
    failas = BASE_DIR / "VERSIJA"
    try:
        sha = failas.read_text(encoding="utf-8").strip()
        if sha:
            return sha[:12]
    except OSError:
        pass

    sha = config("GIT_SHA", default="").strip()
    if sha:
        return sha[:12]

    try:
        galva = (BASE_DIR / ".git" / "HEAD").read_text(encoding="utf-8").strip()
        if galva.startswith("ref: "):
            vardas = galva[5:].strip()
            nuoroda = BASE_DIR / ".git" / vardas
            if nuoroda.exists():
                return nuoroda.read_text(encoding="utf-8").strip()[:12]
            # Supakuotos nuorodos (po `git gc`) atskiro failo neturi
            supakuotos = BASE_DIR / ".git" / "packed-refs"
            if supakuotos.exists():
                for eil in supakuotos.read_text(encoding="utf-8").splitlines():
                    if eil.endswith(" " + vardas):
                        return eil.split(" ", 1)[0][:12]
        elif galva:
            return galva[:12]
    except OSError:
        pass

    return "nezinoma"


GIT_SHA = _versija()

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# ═══════════════════════════════════════════════════════════
# TURINIO MAIŠAS STATINIAMS FAILAMS
#
# Kodėl: nginx statiniams neduoda jokio Cache-Control, tik ETag ir
# Last-Modified. Tada naršyklė kešuoja EURISTIŠKAI — pati nusprendžia,
# kiek laikyti, ir seno style.css neperklausia. Po dizaino keitimo dalis
# lankytojų matydavo sulaužytą puslapį, kol nepaspausdavo Ctrl+Shift+R.
#
# ManifestStaticFilesStorage įrašo turinio maišą į vardą —
# style.css → style.a1b2c3d4e5f6.css. Pakeitus failą pasikeičia vardas,
# tad naršyklė gauna naują failą pati, o senojo kešas nebetrukdo. Tik
# tada nginx'e prasminga `immutable` su metų galiojimu (deploy/README.md).
#
# Ką reikia žinoti rašant šablonus:
#   * kelias VISADA per {% static %}, niekada „/static/…" ranka;
#   * kelias turi būti pilnas VIENOJE žymėje — {% static 'a/'|add:b %},
#     o ne {% static 'a/' %}{{ b }}: katalogo vardo manifeste nėra ir
#     puslapis nulūžtų su ValueError;
#   * nurodytas failas privalo egzistuoti (manifest_strict), kitaip
#     puslapis grąžins 500, o ne tylų 404.
#
# Laiškuose kelias lieka absoliutus ir BE maišo: laiškas gyvena metus,
# o senas maišas po kelių deploy'ų nebeegzistuotų. collectstatic
# nesumaišytą kopiją palieka šalia, tad tokios nuorodos veikia.
# ═══════════════════════════════════════════════════════════
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
    },
}

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Crispy forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"

# Login/Logout URLs
LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "/"     # po login → home (root)
LOGOUT_REDIRECT_URL = "/"    # po logout → home (root)

# Google Maps API Key
GOOGLE_MAPS_API_KEY = config("GOOGLE_MAPS_API_KEY", default="")
# Map ID reikia AdvancedMarkerElement žymekliams (įmonių žemėlapis).
# „DEMO_MAP_ID" veikia be Cloud Console įrašo; tikram stiliui verta
# susikurti savą ir įrašyti į .env.
GOOGLE_MAPS_ID = config("GOOGLE_MAPS_ID", default="DEMO_MAP_ID")

# ═══════════════════════════════════════════════════════════
# Email Configuration
# ═══════════════════════════════════════════════════════════
# Default: realus SMTP (siunčia tikrus email'us)
# Jei nori lokaliai tiktai printint į console - .env faile pridėk:
#   EMAIL_USE_CONSOLE=True
# ═══════════════════════════════════════════════════════════
EMAIL_USE_CONSOLE = config("EMAIL_USE_CONSOLE", default=False, cast=bool)

# Visi laiškai eina pro apsaugą (apps/listings/pasto_apsauga.py): ji išmeta
# gavėjus su negyvais domenais (.local, .test, example.com...), kad
# nebegrįžtų „Delivery Status Notification (Failure)".
EMAIL_BACKEND = "apps.listings.pasto_apsauga.ApsaugotasBackend"

if EMAIL_USE_CONSOLE:
    EMAIL_BACKEND_TIKRAS = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_BACKEND_TIKRAS = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = config("EMAIL_USER")
    EMAIL_HOST_PASSWORD = config("EMAIL_PASSWORD")

DEFAULT_FROM_EMAIL = config("EMAIL_USER", default="helpautoinfo@gmail.com")

# Kiek laukti pašto serverio. BE ŠITO Django naudoja sisteminį numatytąjį
# socket timeout'ą, t. y. laukia BE GALO: neatsakantis smtp.gmail.com
# pakabindavo gunicorn darbininką visam laikui.
EMAIL_TIMEOUT = 10

# Laiškai, siunčiami užklausos metu, keliauja į foną
# (apps/listings/emails/fone.py) — lankytojas pašto serverio nelaukia.
# Testai ir management komandos šitą išjungia, kad matytų tikrą rezultatą.
PASTAS_FONE = config("PASTAS_FONE", default=True, cast=bool)

# Password Reset settings
PASSWORD_RESET_TIMEOUT = 259200

# Session settings
SESSION_COOKIE_AGE = 15552000  # 6 mėnesiai
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = True

# ═══════════════════════════════════════════════════════════
# Listing lifecycle (expire / reminders / cleanup)
# ═══════════════════════════════════════════════════════════
SITE_URL = config("SITE_URL", default="http://127.0.0.1:8000")

# ═══════════════════════════════════════════════════════════
# MOKĖJIMAI — vienas jungiklis visai svetainei
# ═══════════════════════════════════════════════════════════
# False (dabar): VISŲ skelbimų įkėlimas nemokamas. Skelbimas
# aktyvuojamas iš karto, planų puslapis ir „Apmokėti" ekranai
# nerodomi, piniginė ir mokami priedai paslėpti.
# True: grįžta senas srautas — planų pasirinkimas, piniginės nurašymas.
#
# Mokėjimo kodas NIEKUR neištrintas: payments programa, modeliai,
# migracijos, Stripe servisas ir planų puslapis vietoje. Šis jungiklis
# tik APEINA juos.
#
# Kur veikia (visos vietos eina per šį vieną jungiklį):
#   * apps/listings/constants.py:can_create_free_listing — visų
#     kategorijų įkėlimo formos per jį sprendžia, ar publikuoti iš karto;
#   * apps/listings/views.py:listing_activate — skydelio „Aktyvuoti";
#   * listing_select_plan / listing_pay_plan — senos nuorodos ir laiškų
#     saitai nebeatsiduria aklavietėje: aktyvuoja nemokamai;
#   * apps/listings/context_processors.py:mokejimai — šablonų jungiklis.
MOKEJIMAI_IJUNGTI = config("MOKEJIMAI_IJUNGTI", default=False, cast=bool)

# Senas vardas — tas pats jungiklis. Kodas, rašytas anksčiau, skaito jį.
# Stripe raktas vienas savaime mokėjimų nebeįjungia: jungiklis viršesnis.
PAYMENTS_ENABLED = MOKEJIMAI_IJUNGTI and bool(STRIPE_SECRET_KEY)

# ═══════════════════════════════════════════════════════════
# File uploads (skelbimo nuotraukoms)
# ═══════════════════════════════════════════════════════════
DATA_UPLOAD_MAX_NUMBER_FILES = 500                  # iki 500 failų per request
DATA_UPLOAD_MAX_MEMORY_SIZE = 200 * 1024 * 1024     # 200 MB total request
FILE_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024      # 50 MB per failas
FILE_UPLOAD_PERMISSIONS = 0o644                     # nuotraukos skaitomos Nginx
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755           # nauji katalogai pasiekiami Nginx


# ═══ ROSETTA SETTINGS ═══
ROSETTA_SHOW_AT_ADMIN_PANEL = True
ROSETTA_ENABLE_TRANSLATION_SUGGESTIONS = True
ROSETTA_MESSAGES_PER_PAGE = 25
ROSETTA_REQUIRES_AUTH = True
ROSETTA_LOGIN_URL = '/accounts/login/'