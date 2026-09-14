# -*- coding: utf-8 -*-
"""
SENŲ LANKYTOJŲ ĮRAŠŲ VALYMAS — VIENA VIETA.

Naudoja ir valdymo komanda (valyti_lankytojus), ir pats statistikos
puslapis: cron'o serveryje gali ir nebūti, o lentelė augti neturi.

Puslapis valo ne dažniau kaip kartą per parą — žymą laiko talpykloje,
tad dvidešimt atidarymų iš eilės nereiškia dvidešimties DELETE.
"""
from datetime import timedelta

from django.core.cache import cache
from django.utils import timezone

from .models import SAUGOM_DIENAS, VisitorHit

RAKTAS = 'analytics:paskutinis_valymas'


def _riba(dienos=None):
    return timezone.now() - timedelta(days=dienos or SAUGOM_DIENAS)


def kiek_senu(dienos=None):
    return VisitorHit.objects.filter(created_at__lt=_riba(dienos)).count()


def valyk(dienos=None):
    """Ištrina senus įrašus ir grąžina, kiek jų buvo."""
    return VisitorHit.objects.filter(created_at__lt=_riba(dienos)).delete()[0]


def valyk_karta_per_para(dienos=None):
    """Tyliai pavalo, jei šiandien dar nevalyta. Klaida nieko nelaužo."""
    if cache.get(RAKTAS):
        return 0
    try:
        istrinta = valyk(dienos)
    except Exception as e:
        print('[analytics] valymas nepavyko: %s' % e)
        return 0
    cache.set(RAKTAS, timezone.now().isoformat(), 60 * 60 * 24)
    return istrinta
