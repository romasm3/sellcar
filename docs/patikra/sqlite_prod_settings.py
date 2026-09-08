# -*- coding: utf-8 -*-
"""Kaip sqlite_settings, tik statinių dalis — kaip produkcijoje.

Kam: sqlite_settings tyčia naudoja paprastą statinių saugyklą ir
DEBUG=True, todėl vietinė patikra NEATIDARO staticfiles.json. Serveryje
(DEBUG=False + ManifestStaticFilesStorage) tas pats šablonas krinta su
„Missing staticfiles manifest entry", jei manifestas dar neatnaujintas.
Šitas failas atkuria būtent tą būklę, kad tokį deploy'o stabdį būtų
galima pagauti vietoje.

    PYTHONPATH=docs/patikra python manage.py test apps.listings \
        --settings=sqlite_prod_settings \
        --testrunner=config.test_runner.BeDuombazes
"""
from sqlite_settings import *          # noqa

DEBUG = False

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"},
}
