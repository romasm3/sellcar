"""Sukuria trūkstamas Equipment eilutes visoms kategorijoms.

Idempotentiška — saugu leisti kiek nori kartų.

    python manage.py seed_equipment
    python manage.py seed_equipment --check   # tik parodo, nieko nekuria

Anksčiau eilutės buvo kuriamos tingiai (get_or_create renderinant create
formą), todėl išplėstinė paieška rodė 0 ypatumų, kol niekas neatidarė
formos. Dabar tą patį daro ir 0063 migracija, tad naujoje aplinkoje
komandos leisti nereikia — ji lieka rankiniam patikrinimui.
"""
from django.core.management.base import BaseCommand

from apps.listings.equipment_registry import CATEGORY_EQUIPMENT, seed
from apps.listings.models import Equipment


class Command(BaseCommand):
    help = 'Sukuria trūkstamas kategorijų ypatumų (Equipment) eilutes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--check', action='store_true',
            help='Tik parodo, kiek trūksta; nieko nekuria',
        )

    def handle(self, *args, **options):
        for slug, definition in sorted(CATEGORY_EQUIPMENT.items()):
            expected = sum(len(names) for _k, _l, names in definition)
            prefix = definition[0][0].split('_')[0] + '_'
            have = Equipment.objects.filter(category__startswith=prefix).count()
            mark = 'OK' if have >= expected else 'TRŪKSTA'
            self.stdout.write(f'  {slug:<20} DB {have:>3} / {expected:<3} {mark}')

        if options['check']:
            self.stdout.write(self.style.WARNING('--check: nieko nekurta'))
            return

        created, total = seed(Equipment)
        if created:
            self.stdout.write(self.style.SUCCESS(
                f'Sukurta {created} naujų eilučių (iš {total} aprašytų)'))
        else:
            self.stdout.write(self.style.SUCCESS(
                f'Viskas jau vietoje — {total} eilučių'))
