# -*- coding: utf-8 -*-
"""
Adresai, į kuriuos siuntimas visada grįžtų atgal.

    python manage.py tikrinti_pasto_adresus            # tik parodo
    python manage.py tikrinti_pasto_adresus --taisyti  # perrašo į @example.com

Tikrinam VISUS projekto `EmailField` laukus (naudotojus, įmones, skelbimų
kontaktus, pranešimus…), o ne vien `User.email`: negyvas adresas įmonės
kortelėje taip pat pasiekia siuntimą.

`--taisyti` perrašo tik NAUDOTOJŲ ir ĮMONIŲ adresus — tai paskyros, kurių
savininkas yra mūsų pusėje. Skelbimų kontaktai ir pranešimai yra svetimi
duomenys: juos tik parodom, o siuntimą į juos ir taip sulaiko pašto
apsauga (apps/listings/pasto_apsauga.py).
"""

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import models

from apps.listings.pasto_apsauga import domenas_negyvas

# Į ką patys perrašom — toks adresas jau sutvarkytas, ne bėda
SUTVARKYTAS = 'example.com'

# Ką valia perrašyti automatiškai: (programa.Modelis, laukas)
TAISOMI = {
    ('auth.User', 'email'),
    ('imones.Imone', 'el_pastas'),
}


def pasto_laukai():
    """[(modelis, lauko_vardas)] — visi EmailField projekte."""
    out = []
    for modelis in apps.get_models():
        for laukas in modelis._meta.concrete_fields:
            if isinstance(laukas, models.EmailField):
                out.append((modelis, laukas.name))
    return out


class Command(BaseCommand):
    help = 'Parodo (arba pataiso) adresus su negyvais el. pašto domenais'

    def add_arguments(self, parser):
        parser.add_argument('--taisyti', action='store_true',
                            help='naudotojų ir įmonių adresus keisti į @example.com')

    def handle(self, *args, **options):
        rasta = []          # (etiketė, objektas, laukas, adresas, taisoma)
        for modelis, laukas in pasto_laukai():
            etikete = modelis._meta.label
            filtras = {'%s__isnull' % laukas: False}
            for obj in modelis.objects.filter(**filtras).exclude(**{laukas: ''}):
                adresas = getattr(obj, laukas) or ''
                if not adresas or not domenas_negyvas(adresas):
                    continue
                jau_sutvarkytas = adresas.rsplit('@', 1)[-1].lower() == SUTVARKYTAS
                rasta.append((etikete, obj, laukas, adresas,
                              (etikete, laukas) in TAISOMI and not jau_sutvarkytas,
                              jau_sutvarkytas))

        self.stdout.write('Patikrinta laukų: %d' % len(pasto_laukai()))
        if not rasta:
            self.stdout.write(self.style.SUCCESS('Negyvų adresų nerasta.'))
            return

        self.stdout.write('\n%-22s %-14s %-36s %s'
                          % ('MODELIS', 'LAUKAS', 'ADRESAS', 'BŪSENA'))
        for etikete, obj, laukas, adresas, taisoma, sutvarkytas in rasta:
            bukle = ('jau sutvarkytas' if sutvarkytas
                     else 'perrašom' if taisoma else 'svetimi duomenys — neliečiam')
            self.stdout.write('%-22s %-14s %-36s #%s %s'
                              % (etikete, laukas, adresas, obj.pk, bukle))

        taisomi = [r for r in rasta if r[4]]
        nauji = len(rasta) - sum(1 for r in rasta if r[5])
        self.stdout.write('\nRasta negyvų: %d (iš jų jau perrašytų į @%s: %d)'
                          % (len(rasta), SUTVARKYTAS, len(rasta) - nauji))
        self.stdout.write('Perrašomų šįkart: %d' % len(taisomi))

        if not taisomi:
            self.stdout.write(self.style.SUCCESS(
                'Naujų netvarkingų paskyrų nėra. Siuntimas į negyvus '
                'domenus ir taip blokuojamas.'))
            return

        if not options['taisyti']:
            self.stdout.write('Siuntimas į juos jau blokuojamas. '
                              'Norint perrašyti: --taisyti')
            return

        for etikete, obj, laukas, adresas, taisoma, _s in taisomi:
            vardas = (getattr(obj, 'username', None)
                      or getattr(obj, 'slug', None) or 'irasas%s' % obj.pk)
            naujas = '%s@example.com' % vardas
            setattr(obj, laukas, naujas)
            obj.save(update_fields=[laukas])
            self.stdout.write(self.style.WARNING('  %s → %s' % (adresas, naujas)))
        self.stdout.write(self.style.SUCCESS('Pataisyta: %d' % len(taisomi)))
