# -*- coding: utf-8 -*-
"""
SENŲ LANKYTOJŲ ĮRAŠŲ VALYMAS.

Kiekvienas apsilankymas — eilutė DB (apps/analytics/middleware.py), o
botų skenavimų būna daugiau nei žmonių. Be valymo lentelė auga be galo:
kartu auga ir /admin-moderate/visitors/ bei /sales-stats/ užklausos.

Statistikai užtenka `SAUGOM_DIENAS` (90) dienų — tiek ir laikom.

Paleidimas:
    python manage.py valyti_lankytojus              # >90 d.
    python manage.py valyti_lankytojus --dienos 30
    python manage.py valyti_lankytojus --parodyk    # tik parodo, netrina

Automatiškai: tą patį daro ir pats puslapis (žr. apps/analytics/valymas.py),
tad atskiro cron'o nebūtina.
"""
from django.core.management.base import BaseCommand

from apps.analytics.models import SAUGOM_DIENAS
from apps.analytics.valymas import kiek_senu, valyk


class Command(BaseCommand):
    help = 'Ištrina lankytojų įrašus, senesnius nei N dienų (numatyta 90).'

    def add_arguments(self, parser):
        parser.add_argument('--dienos', type=int, default=SAUGOM_DIENAS)
        parser.add_argument('--parodyk', action='store_true',
                            help='Tik parodo, kiek būtų ištrinta.')

    def handle(self, *args, **o):
        dienos = o['dienos']
        senu = kiek_senu(dienos)
        if o['parodyk']:
            self.stdout.write('Senesnių nei %d d. įrašų: %d' % (dienos, senu))
            return
        istrinta = valyk(dienos)
        self.stdout.write(self.style.SUCCESS(
            'Ištrinta %d įrašų, senesnių nei %d d.' % (istrinta, dienos)))
