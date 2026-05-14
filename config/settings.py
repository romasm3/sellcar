import os
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

# ═══════════════════════════════════════════════════════════
# GOOGLE TRANSLATE API
# ═══════════════════════════════════════════════════════════
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(
    BASE_DIR / 'google-translate-key.json'
)

SECRET_KEY = config("SECRET_KEY", default="django-insecure-change-this-key")
DEBUG = config("DEBUG", default=True, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost,127.0.0.1").split(",")

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
    # Local apps
    "apps.accounts",
    "apps.listings",
    "apps.conversations",
    "apps.broadcasts",
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
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "apps.accounts.middleware.UserLanguageMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
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
                "apps.conversations.context_processors.unread_messages",
                "apps.listings.context_processors.saved_searches_count",
                "apps.listings.context_processors.saved_listings_count",
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

AUTH_PASSWORD_VALIDATORS = []

from django.utils.translation import gettext_lazy as _

LANGUAGE_CODE = "en"
TIME_ZONE = "Europe/Vilnius"
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
    ("en", _("English")),
    ("lt", _("Lithuanian")),
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

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

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

# ═══════════════════════════════════════════════════════════
# Email Configuration
# ═══════════════════════════════════════════════════════════
# Default: realus SMTP (siunčia tikrus email'us)
# Jei nori lokaliai tiktai printint į console - .env faile pridėk:
#   EMAIL_USE_CONSOLE=True
# ═══════════════════════════════════════════════════════════
EMAIL_USE_CONSOLE = config("EMAIL_USE_CONSOLE", default=False, cast=bool)

if EMAIL_USE_CONSOLE:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = config("EMAIL_USER")
    EMAIL_HOST_PASSWORD = config("EMAIL_PASSWORD")

DEFAULT_FROM_EMAIL = config("EMAIL_USER", default="helpautoinfo@gmail.com")

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
PAYMENTS_ENABLED = False

# ═══════════════════════════════════════════════════════════
# File uploads (skelbimo nuotraukoms)
# ═══════════════════════════════════════════════════════════
DATA_UPLOAD_MAX_NUMBER_FILES = 500                  # iki 500 failų per request
DATA_UPLOAD_MAX_MEMORY_SIZE = 200 * 1024 * 1024     # 200 MB total request
FILE_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024      # 50 MB per failas


# ═══ ROSETTA SETTINGS ═══
ROSETTA_SHOW_AT_ADMIN_PANEL = True
ROSETTA_ENABLE_TRANSLATION_SUGGESTIONS = True
ROSETTA_MESSAGES_PER_PAGE = 25
ROSETTA_REQUIRES_AUTH = True
ROSETTA_LOGIN_URL = '/accounts/login/'