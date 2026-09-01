# -*- coding: utf-8 -*-
"""
LAIŠKAI — IŠ UŽKLAUSOS Į FONĄ.

Kodėl: laiškai siunčiami sinchroniškai per smtp.gmail.com. Kol vyksta
TLS rankos paspaudimas, prisijungimas ir siuntimas, gunicorn darbininkas
laukia, o kartu laukia ir lankytojas. Skelbimo puslapyje tai ypač
skaudu: `_track_listing_view` siunčia laišką, kai peržiūrų skaičius
peržengia 10, 100, 500 ar 1000 — tą akimirką eilinis lankytojas,
neturintis su laišku nieko bendra, laukia pašto serverio. Jei Gmail
neatsako, be `EMAIL_TIMEOUT` laukiama BE GALO ir darbininkas pakimba.

Sprendimas: užklausoje tik pastatom darbą į eilę, o siunčia atskiras
gijų telkinys. Puslapis atiduodamas iškart.

    from apps.listings.emails.fone import send_scenario_fone
    send_scenario_fone(code='listing_first_views', to_email=..., context={...})

Ką reikia žinoti:

* Telkinys gyvena PROCESE. Perkrovus gunicorn'ą (deploy) neišsiųsti
  darbai dingsta. Laiškams apie peržiūrų slenkstį tai priimtina — jie
  informaciniai; svarbiems (mokėjimai, slaptažodžio atkūrimas) siųsk
  sinchroniškai arba per management komandą.
* Gijoje uždarom DB jungtis (`connections.close_all()`) — kitaip po
  darbo liktų kaboti atviras seansas.
* `settings.PASTAS_FONE = False` grąžina sinchroninį elgesį. Taip daro
  testai, kad `mail.outbox` būtų užpildytas iškart, ir management
  komandos, kurioms reikia tikro rezultato ataskaitai.
"""
import logging
from concurrent.futures import ThreadPoolExecutor

from django.conf import settings
from django.db import connections

logger = logging.getLogger(__name__)

# Keturios gijos: laiškų srautas nedidelis, o telkinys neleidžia jam
# augti be ribų, jei paštas sulėtėtų.
_TELKINYS = ThreadPoolExecutor(max_workers=4, thread_name_prefix='pastas')


def _fone_leidziama():
    return getattr(settings, 'PASTAS_FONE', True)


def fone(funkcija, *args, **kwargs):
    """Paleidžia funkciją fone. Grąžina tuoj pat."""
    if not _fone_leidziama():
        return funkcija(*args, **kwargs)

    def _darbas():
        try:
            funkcija(*args, **kwargs)
        except Exception:
            # Fone niekas nebegaudo — įrašom patys, kad klaida nedingtų.
            logger.exception('[email] fono darbas nulūžo: %s', funkcija.__name__)
        finally:
            # Gija pasiėmė savo DB jungtį; be šito ji liktų atvira.
            connections.close_all()

    try:
        _TELKINYS.submit(_darbas)
    except RuntimeError:
        # Telkinys uždarytas (procesas baigiasi) — geriau išsiųsti
        # sinchroniškai, nei nusiųsti nieko.
        return funkcija(*args, **kwargs)
    return True


def send_scenario_fone(*args, **kwargs):
    """send_scenario, tik nelaikantis lankytojo.

    Grąžina True „priimta į eilę", o ne siuntimo rezultatą — tikro
    rezultato užklausa vis tiek nebelaukia. Nepavykus, klaida gula į
    žurnalą ir į EmailScenario.fail_count, kaip ir anksčiau.
    """
    from apps.listings.emails.sender import send_scenario
    return fone(send_scenario, *args, **kwargs)


def send_admin_scenario_fone(*args, **kwargs):
    from apps.listings.emails.sender import send_admin_scenario
    return fone(send_admin_scenario, *args, **kwargs)


def send_mail_fone(*args, **kwargs):
    from django.core.mail import send_mail
    return fone(send_mail, *args, **kwargs)
