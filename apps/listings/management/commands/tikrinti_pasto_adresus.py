# -*- coding: utf-8 -*-
"""
Paskyros su adresais, į kuriuos siuntimas visada grįžta atgal.

    python manage.py tikrinti_pasto_adresus            # tik parodo
    python manage.py tikrinti_pasto_adresus --taisyti  # perrašo į @example.com

Negyvi domenai (.local, .test, example.com…) aprašyti vienoje vietoje —
apps/listings/pasto_apsauga.py. Laiškai į juos ir taip nebeišeina (pašto
apsauga), bet švarūs duomenys aiškesni: matyti, kurios paskyros testinės.
"""

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db.models import Count

from apps.listings.pasto_apsauga import domenas_negyvas


class Command(BaseCommand):
    help = 'Parodo (arba pataiso) paskyras su negyvais el. pašto domenais'

    def add_arguments(self, parser):
        parser.add_argument('--taisyti', action='store_true',
                            help='pakeisti adresus į <naudotojas>@example.com')

    def handle(self, *args, **options):
        blogi = [u for u in User.objects.annotate(n=Count('listings')).exclude(email='')
                 if domenas_negyvas(u.email)]

        if not blogi:
            self.stdout.write(self.style.SUCCESS('Negyvų adresų nerasta.'))
            return

        self.stdout.write('%-22s %-34s %s' % ('PASKYRA', 'EL. PAŠTAS', 'SKELBIMŲ'))
        for u in blogi:
            self.stdout.write('%-22s %-34s %s' % (u.username, u.email, u.n))

        if not options['taisyti']:
            self.stdout.write('\nSiuntimas į juos jau blokuojamas. '
                              'Norint perrašyti adresus: --taisyti')
            return

        for u in blogi:
            senas = u.email
            u.email = '%s@example.com' % u.username
            u.save(update_fields=['email'])
            self.stdout.write(self.style.WARNING('  %s → %s' % (senas, u.email)))
        self.stdout.write(self.style.SUCCESS('Pataisyta: %s' % len(blogi)))
