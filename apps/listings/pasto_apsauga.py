# -*- coding: utf-8 -*-
"""
APSAUGA NUO LAIŠKŲ Į NEGYVUS DOMENUS

Testinės paskyros turi adresus, kurių pasaulyje nėra (`@autoleft.local`).
Kiekvienas laiškas tokiam adresui grįžta atgal „Delivery Status
Notification (Failure)" į siuntėjo dėžutę, o kasdieniai darbai tai daro
kas dieną.

Sprendimas — pašto galas (`EMAIL_BACKEND`), pro kurį eina VISI laiškai:
Django `send_mail`, `EmailMultiAlternatives`, slaptažodžio priminimai,
administratoriaus siuntimai ir mūsų `emails/sender.py`. Gavėjai su
negyvais domenais išmetami dar prieš SMTP, o kiekvienas praleistas
adresas įrašomas į žurnalą.

Sąrašą plėsti čia — vienoje vietoje (RFC 2606 / RFC 6761 rezervuoti
vardai, kuriems pašto niekada nebus).
"""

import logging

from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from django.utils.module_loading import import_string

logger = logging.getLogger(__name__)

# Galūnės, į kurias niekada nesiunčiam
NESIUNCIAMOS_GALUNES = (
    '.local', '.test', '.invalid', '.example', '.localhost',
    '.internal', '.lan', '.home', '.corp',
)

# Pilni domenai, kurie yra rezervuoti pavyzdžiams
NESIUNCIAMI_DOMENAI = {
    'example.com', 'example.org', 'example.net', 'localhost',
}


def domenas_negyvas(adresas):
    """Ar į šį adresą siųsti neverta (domeno pasaulyje nėra)."""
    if not adresas or '@' not in adresas:
        return True
    domenas = adresas.rsplit('@', 1)[1].strip().lower().rstrip('.')
    if not domenas or '.' not in domenas:
        return True                       # „vartotojas@localhost" ir pan.
    # example.com ir jo padomeniai (mail.example.com) — irgi rezervuoti
    if any(domenas == d or domenas.endswith('.' + d) for d in NESIUNCIAMI_DOMENAI):
        return True
    return domenas.endswith(NESIUNCIAMOS_GALUNES)


def gyvi_adresai(adresai):
    """Palieka tik tuos, į kuriuos verta siųsti."""
    return [a for a in (adresai or []) if not domenas_negyvas(a)]


class ApsaugotasBackend(BaseEmailBackend):
    """Filtruoja gavėjus ir perduoda tikram pašto galui.

    Tikras galas nurodomas `settings.EMAIL_BACKEND_TIKRAS` (SMTP arba
    konsolė) — taip apsauga nepriklauso nuo to, kaip sukonfigūruotas
    paštas, ir veikia ir vietinėje aplinkoje.
    """

    def __init__(self, fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently)
        tikras = getattr(settings, 'EMAIL_BACKEND_TIKRAS',
                         'django.core.mail.backends.smtp.EmailBackend')
        self.vidinis = import_string(tikras)(fail_silently=fail_silently, **kwargs)

    def send_messages(self, email_messages):
        praleisti = []
        siunciami = []

        for laiskas in email_messages or []:
            gyvi = gyvi_adresai(laiskas.to)
            negyvi = [a for a in (laiskas.to or []) if a not in gyvi]
            if negyvi:
                praleisti.extend(negyvi)
            if not gyvi:
                continue                    # nė vieno gyvo gavėjo — nesiunčiam
            laiskas.to = gyvi
            laiskas.cc = gyvi_adresai(getattr(laiskas, 'cc', None))
            laiskas.bcc = gyvi_adresai(getattr(laiskas, 'bcc', None))
            siunciami.append(laiskas)

        if praleisti:
            logger.warning('[email] praleisti negyvi adresai (%s): %s',
                           len(praleisti), ', '.join(sorted(set(praleisti))))

        if not siunciami:
            return 0
        return self.vidinis.send_messages(siunciami)
