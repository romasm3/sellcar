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
            # Skaičiuojam TIKSLIAI aprašytas (kategorija, pavadinimas) poras.
            # Anksčiau buvo spėjamas prefiksas iš pirmos grupės rakto —
            # tai griūdavo ten, kur raktai neturi bendro prefikso
            # (automobiliai: 'interior', 'safety'...) arba kur dvi
            # kategorijos dalinasi prefiksu (trucks / truck-parts).
            have = sum(
                Equipment.objects.filter(category=key, name__in=names).count()
                for key, _label, names in definition
            )
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
