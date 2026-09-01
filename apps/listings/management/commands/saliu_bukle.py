# -*- coding: utf-8 -*-
"""
Management command: saliu_bukle

Kiek skelbimų kurioje šalyje — tiems patiems skaičiukams, kuriuos rodo
šalies juosta virš paieškos panelės.

TIK SKAITO — nieko nekeičia.

Kodėl verta pažiūrėti: `Listing.country` numatytasis migracijose 0018–0032
buvo 'US', ir tik vėliau tapo 'LT'. Tuo laikotarpiu sukurti skelbimai gali
gulėti su 'US', nors realiai yra Lietuvoje.

    python manage.py saliu_bukle
    python manage.py saliu_bukle --visi     # ir juodraščiai, ir pasibaigę
"""
from collections import Counter

from django.core.management.base import BaseCommand

from apps.listings import salys
from apps.listings.models import Listing


class Command(BaseCommand):
    help = 'Skelbimų pasiskirstymas pagal šalį.'

    def add_arguments(self, p):
        p.add_argument('--visi', action='store_true',
                       help='Skaičiuoti visus, ne tik viešai matomus')

    def handle(self, *args, **o):
        from apps.listings.views import _public_listings_qs
        qs = Listing.objects.all() if o['visi'] else _public_listings_qs(None)

        kiekiai = Counter(qs.values_list('country', flat=True))
        viso = sum(kiekiai.values())
        if not viso:
            self.stdout.write('Skelbimų nėra.')
            return

        self.stdout.write('%-4s %-24s %7s  %s'
                          % ('KOD', 'ŠALIS', 'KIEK', 'DALIS'))
        self.stdout.write('─' * 52)
        for kodas, kiek in kiekiai.most_common():
            zyma = '' if kodas in salys.VARDAI else '  ← nežinomas kodas'
            self.stdout.write('%-4s %-24s %7d  %5.1f %%%s'
                              % (kodas or '(tuščia)', salys.vardas_en(kodas),
                                 kiek, 100.0 * kiek / viso, zyma))
        self.stdout.write('─' * 52)
        self.stdout.write('iš viso %d' % viso)

        numatyta = kiekiai.get(salys.NUMATYTA, 0)
        if not numatyta:
            self.stdout.write(self.style.WARNING(
                '\nDĖMESIO: numatytoje šalyje (%s) skelbimų nėra. Juosta ją '
                'rodys, bet filtro netaikys, kad sąrašas neliktų tuščias '
                '(žr. salies_juosta.filtruoti).' % salys.NUMATYTA))
        if kiekiai.get('US'):
            self.stdout.write(self.style.WARNING(
                '\n%d skelbimų su country=US. Jei tai seni lietuviški įrašai '
                '(numatytasis buvo US), juos galima perkelti — bet tai '
                'duomenų keitimas, todėl atskirai ir tik paprašius.'
                % kiekiai['US']))
