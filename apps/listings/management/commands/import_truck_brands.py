"""
Management command to import truck brands.

Usage:
    python manage.py import_truck_brands

Idempotent — uses get_or_create, safe to run multiple times.
Combines brands from autoplius.lt (European market) + US-specific truck makers.
"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from apps.listings.models import TruckBrand


# All brands from autoplius.lt screenshots + US-specific truck makers
TRUCK_BRANDS = [
    # ─── European / autoplius.lt brands ───
    'Astra',
    'Avia',
    'Belaz',
    'Bremach',
    'Challenger',
    'Chevrolet',
    'Chrysler',
    'Citroen',
    'DAF',
    'Daewoo',
    'Daihatsu',
    'Dodge',
    'Faun',
    'Fiat',
    'Foden',
    'Ford',
    'Freightliner',
    'GAZ',
    'GMC',
    'Ginaf',
    'Hino',
    'Hyundai',
    'International',
    'Isuzu',
    'Iveco',
    'KRAZ',
    'KamAZ',
    'Kassbohrer',
    'Kia',
    'Komatsu',
    'LDV',
    'M1078 LMTV',
    'MAN',
    'MAZ',
    'Magirus Deutz',
    'Mazda',
    'Mega',
    'MEILLER-KIPPER',
    'Mercedes-Benz',
    'Mitsubishi',
    'Mitsubishi Fuso',
    'Multicar',
    'Nissan',
    'Opel',
    'Peugeot',
    'Plandex',
    'Renault',
    'Rolfo',
    'Roman',
    'Scam',
    'Scania',
    'Seat',
    'Sisu',
    'Stewart & Stevenson',
    'Suzuki',
    'Tatra',
    'Terberg',
    'Toyota',
    'Trail-Eze',
    'UAZ',
    'Unimog',
    'Ural',
    'Volkswagen',
    'Volvo',
    'ZIL',
    'Ze135g',
    'Ze26go',
    'Zoomlion',
    'Zs090v',

    # ─── US market — Class 7-8 heavy trucks ───
    'Kenworth',
    'Peterbilt',
    'Mack',
    'Western Star',
    'Autocar',
    'Sterling',
    'Oshkosh',
    'Navistar',
    'Pierce',           # Fire trucks / specialty
    'Crane Carrier',    # CCC — refuse trucks
    'Marmon',
    'White',
    'Brockway',
    'Diamond T',
    'REO',
    'FWD',
    'Hendrickson',
    'Caterpillar',
    'Sany',
    'XCMG',

    # ─── Class 1-6 light/medium duty US ───
    'Ram',
    'Workhorse',
    'Hino USA',
    'Spartan Motors',
    'Capacity Trucks',
    'Ottawa',           # Yard trucks
    'TICO',             # Yard trucks

    # ─── Misc / Other ───
    'Other',
]


class Command(BaseCommand):
    help = 'Import all truck brands (autoplius.lt + US market)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be imported without writing to DB',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']

        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN — no DB writes'))

        created_count = 0
        existed_count = 0
        skipped_count = 0

        # Sort alphabetically for consistent output
        sorted_brands = sorted(set(TRUCK_BRANDS), key=lambda x: x.lower())

        for name in sorted_brands:
            name = name.strip()
            if not name:
                skipped_count += 1
                continue

            slug = slugify(name)
            if not slug:
                self.stdout.write(self.style.ERROR(f'  ✗ Cannot slugify: "{name}"'))
                skipped_count += 1
                continue

            if dry_run:
                exists = TruckBrand.objects.filter(name__iexact=name).exists()
                if exists:
                    existed_count += 1
                    self.stdout.write(f'  · {name}  (exists)')
                else:
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(f'  + {name}  (would create)'))
                continue

            # Real run
            obj, created = TruckBrand.objects.get_or_create(
                name=name,
                defaults={'slug': slug},
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'  + Created: {name}'))
            else:
                existed_count += 1
                self.stdout.write(f'  · Exists: {name}')

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(
            f'Done. Created: {created_count}, '
            f'existed: {existed_count}, '
            f'skipped: {skipped_count}, '
            f'total in DB: {TruckBrand.objects.count()}'
        ))