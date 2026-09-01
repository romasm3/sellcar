# -*- coding: utf-8 -*-
"""LĖTAS pašto backend'as — docs/pasto_fone_test.py.

Atskiras modulis, o ne testo viduje: Django backend'ą importuoja pagal
kelią, tad gyvendamas teste jis paleistų visą testo failą iš naujo ir
`settings.configure()` būtų kviečiamas antrą kartą.
"""
import threading
import time

from django.core.mail.backends.base import BaseEmailBackend

DELSA = 2.0                 # kiek „užtrunka" pašto serveris
issiusta = []
_uzraktas = threading.Lock()


class LetasBackend(BaseEmailBackend):
    """Paštas, kuris atsako lėtai — kaip neatsakantis smtp.gmail.com."""

    def send_messages(self, email_messages):
        time.sleep(DELSA)
        with _uzraktas:
            for m in email_messages:
                issiusta.append(m.subject)
        return len(email_messages)
