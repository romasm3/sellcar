# -*- coding: utf-8 -*-
"""
Vietinei patikrai: tie patys nustatymai, tik su sqlite ir be HTTPS.

    PYTHONPATH=docs/patikra python manage.py runserver 127.0.0.1:8899 \
        --settings=sqlite_settings --noreload

Kodėl repo, o ne laikinajame kataloge: be šito failo nepasileidžia nei
vietinis serveris, nei `manage.py test`, o docs/*_playwright.js testai
be jo neturi ką tikrinti. Anksčiau jis gyveno tik /tmp ir dingdavo su
sesija.
"""
import os as _os
from pathlib import Path as _Path

from config.settings import *          # noqa

# DB kelias — perrašomas per aplinką, kad kelios patikros nesikirstų
DATABASES = {'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': _os.environ.get('PATIKRA_DB',
                            str(_Path(BASE_DIR) / '.patikra.sqlite3')),
}}

DEBUG = True
ALLOWED_HOSTS = ['*']

# Vietinei patikrai per http (produkcijoje viskas lieka kaip buvo)
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = 0

# Vietinė patikra atiduoda statinius iš static/ per runserver, o
# sumaišytų vardų ten nėra (jie gyvena staticfiles/ po collectstatic).
# Todėl VIETOJE naudojam paprastą saugyklą — kitaip Playwright puslapiai
# liktų be CSS. Tikrąjį maišo elgesį tikrina docs/statiniu_kesas_test.py
# ir patikra gyvoje svetainėje (SKILL.md 8 taisyklė).
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}

# Mokėjimų jungiklis vietinei patikrai — perrašomas per aplinkos kintamąjį,
# kad tą patį serverį būtų galima paleisti abiem padėtim.
MOKEJIMAI_IJUNGTI = _os.environ.get('MOKEJIMAI_IJUNGTI', '0') in ('1', 'true', 'True')
PAYMENTS_ENABLED = MOKEJIMAI_IJUNGTI
