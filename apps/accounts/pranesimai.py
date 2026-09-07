# -*- coding: utf-8 -*-
"""
PRANEŠIMAS SAVININKUI APIE NAUJĄ REGISTRACIJĄ.

Kabinam prie REGISTRACIJOS VAIZDO, o ne prie `post_save` signalo.
Signalas suveiktų ir tada, kai naudotoją sukuria administratorius per
/admin/, `createsuperuser` ar duomenų perkėlimo skriptas — o pranešti
prašyta TIK apie viešą registraciją. Vaizdas yra vienintelis viešas
kelias, tad sąlygų tikrinti nebereikia.

Siunčiam fone (apps/listings/emails/fone.py): naujokas savo puslapyje
pašto serverio nelaukia. Testuose `PASTAS_FONE = False`, tad
`mail.outbox` užsipildo iš karto.

Adresas — `settings.REGISTRACIJOS_PRANESIMU_EL`; tuščias jį išjungia.
"""
import logging

from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)

TEMA = 'Naujas vartotojas AutoLeft'


def _gavejas():
    return (getattr(settings, 'REGISTRACIJOS_PRANESIMU_EL', '') or '').strip()


def _tekstas(user):
    from django.contrib.auth import get_user_model

    laikas = timezone.localtime(getattr(user, 'date_joined', None)
                                or timezone.now())
    eilutes = [
        'Svetainėje užsiregistravo naujas vartotojas.',
        '',
        'El. paštas: %s' % (user.email or '(nenurodytas)'),
        'Paskyra:    %s' % user.username,
        'Data:       %s' % laikas.strftime('%Y-%m-%d %H:%M:%S'),
    ]
    try:
        eilutes.append('Iš viso vartotojų: %d'
                       % get_user_model().objects.count())
    except Exception:
        # Skaičius yra malonumas, ne būtinybė — dėl jo laiškas nekrenta.
        logger.exception('[registracija] nepavyko suskaičiuoti vartotojų')
    eilutes += ['', 'https://autoleft.com/admin/auth/user/%s/change/' % user.pk]
    return '\n'.join(eilutes)


def pranesk_apie_registracija(user):
    """Praneša savininkui. NIEKADA nekelia klaidos.

    Registracija yra svarbesnė už pranešimą: jei paštas neveikia,
    žmogus vis tiek turi būti užregistruotas, o klaida gula į žurnalą.
    """
    try:
        gavejas = _gavejas()
        if not gavejas:
            return False
        from apps.listings.emails.fone import send_mail_fone
        send_mail_fone(
            TEMA,
            _tekstas(user),
            getattr(settings, 'DEFAULT_FROM_EMAIL', None),
            [gavejas],
            fail_silently=False,
        )
        return True
    except Exception:
        logger.exception('[registracija] pranešimo išsiųsti nepavyko')
        return False
