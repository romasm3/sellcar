# -*- coding: utf-8 -*-
"""
Prekiautojų profiliai iš jau turimų paskyrų (1 etapas).

Prekiautojas naujos formos nepildo: įmonė sukuriama iš to, kas paskyroje
jau yra — pavadinimo, logotipo, adreso, telefono, aprašymo ir darbo
laiko. Komandą galima leisti kartotinai: esami įrašai atnaujinami, o ne
dubliuojami.

    manage.py imones_is_paskyru [--sausas] [--patvirtinti]
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.imones.models import Imone


class Command(BaseCommand):
    help = 'Sukuria/atnaujina prekiautojų įmonių profilius iš paskyrų duomenų'

    def add_arguments(self, parser):
        parser.add_argument('--sausas', action='store_true',
                            help='tik parodo, ką darytų')
        parser.add_argument('--patvirtinti', action='store_true',
                            help='iškart pažymi patvirtinta=True')

    def handle(self, *args, **o):
        from apps.accounts.models import Profile

        profiliai = Profile.objects.filter(dealer_subscription_active=True)
        if not profiliai.exists():
            self.stdout.write('Aktyvių prekiautojų paskyrų nėra — nieko nedaryta.')
            return

        sukurta = atnaujinta = 0
        for p in profiliai.select_related('user'):
            vardas = (p.dealer_company_name or p.company_name
                      or p.user.get_username())
            reiksmes = {
                'tipas': Imone.PREKIAUTOJAS,
                'pavadinimas': vardas,
                'aprasymas': p.dealer_description or p.company_description or '',
                'adresas': p.dealer_address or '',
                'telefonas': p.dealer_phone or '',
                'el_pastas': p.user.email or '',
                'darbo_laikas': self._laikas(p.dealer_working_hours),
            }
            if p.dealer_logo:
                reiksmes['logotipas'] = p.dealer_logo
            elif p.company_logo:
                reiksmes['logotipas'] = p.company_logo
            if o['patvirtinti']:
                reiksmes['patvirtinta'] = True

            if o['sausas']:
                self.stdout.write(f'  būtų: {vardas} ({p.user_id})')
                continue
            with transaction.atomic():
                imone, nauja = Imone.objects.get_or_create(
                    savininkas=p.user, tipas=Imone.PREKIAUTOJAS,
                    defaults=reiksmes)
                if not nauja:
                    for k, v in reiksmes.items():
                        setattr(imone, k, v)
                    imone.save()
            sukurta += 1 if nauja else 0
            atnaujinta += 0 if nauja else 1

        self.stdout.write(self.style.SUCCESS(
            f'Sukurta: {sukurta}, atnaujinta: {atnaujinta}'))

    @staticmethod
    def _laikas(reiksme):
        """Paskyros darbo laikas -> {"0": ["08:00","18:00"]}.

        Paskyroje jis laikomas laisvu tekstu arba žodynu; ko nesuprantam,
        paliekam tuščią — administratorius užpildys.
        """
        if isinstance(reiksme, dict):
            svarus = {}
            for k, v in reiksme.items():
                if isinstance(v, (list, tuple)) and len(v) == 2:
                    svarus[str(k)] = [str(v[0]), str(v[1])]
            return svarus
        return {}
