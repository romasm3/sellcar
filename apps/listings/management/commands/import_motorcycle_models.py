import os
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from apps.listings.models import MotorcycleBrand, MotorcycleModel


class Command(BaseCommand):
    help = 'Import motorcycle models from motorcycle_models.txt (BRAND|MODEL format)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete all existing MotorcycleModel records before import',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be imported without saving to DB',
        )

    def handle(self, *args, **options):
        # motorcycle_models.txt must be in the same folder as this file
        txt_path = os.path.join(os.path.dirname(__file__), 'motorcycle_models.txt')

        if not os.path.exists(txt_path):
            self.stdout.write(self.style.ERROR(
                f'motorcycle_models.txt not found at: {txt_path}'
            ))
            return

        # Parse BRAND|MODEL lines (skip comments and empty lines)
        entries = []
        with open(txt_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '|' not in line:
                    self.stdout.write(self.style.WARNING(
                        f'Line {line_num}: skipping (no |): {line}'
                    ))
                    continue
                brand_name, model_name = line.split('|', 1)
                entries.append((brand_name.strip(), model_name.strip()))

        if options['dry_run']:
            self.stdout.write(self.style.WARNING(
                f'DRY RUN - would import {len(entries)} models'
            ))
            for brand, model in entries[:20]:
                self.stdout.write(f'  - {brand} | {model}')
            if len(entries) > 20:
                self.stdout.write(f'  ... and {len(entries) - 20} more')
            return

        if options['clear']:
            count = MotorcycleModel.objects.count()
            MotorcycleModel.objects.all().delete()
            self.stdout.write(self.style.WARNING(
                f'Deleted {count} existing MotorcycleModel records'
            ))

        created = 0
        skipped = 0
        missing_brands = set()

        # Track slug conflicts per brand: {brand_id: {base_slug: count}}
        slug_counters = {}

        for brand_name, model_name in entries:
            # Get brand (must exist - run populate_motorcycle_brands first)
            try:
                brand = MotorcycleBrand.objects.get(name=brand_name)
            except MotorcycleBrand.DoesNotExist:
                missing_brands.add(brand_name)
                continue

            # Generate slug - handle empty slugs (e.g. "-kita-" -> "kita")
            base_slug = slugify(model_name)
            if not base_slug:
                # Fallback for names that slugify to empty
                base_slug = model_name.lower().replace(' ', '-').replace('|', '-')
                if not base_slug or base_slug == '-':
                    base_slug = 'model'

            # Handle slug conflicts within same brand
            brand_slugs = slug_counters.setdefault(brand.id, {})
            slug = base_slug
            counter = brand_slugs.get(base_slug, 0)
            if counter > 0:
                slug = f'{base_slug}-{counter + 1}'

            # Also check existing DB slugs for this brand (in case of reruns)
            while MotorcycleModel.objects.filter(
                brand=brand, slug=slug
            ).exclude(name=model_name).exists():
                counter += 1
                slug = f'{base_slug}-{counter + 1}'

            brand_slugs[base_slug] = counter + 1

            obj, was_created = MotorcycleModel.objects.get_or_create(
                brand=brand,
                name=model_name,
                defaults={'slug': slug},
            )
            if was_created:
                created += 1
            else:
                skipped += 1

        # Automatiskai prideti "Other" modeli kiekvienam brand'ui
        # (kad UI butu galima pasirinkti "Other" jei nera tikslaus modelio)
        other_created = 0
        for brand in MotorcycleBrand.objects.all():
            obj, was_created = MotorcycleModel.objects.get_or_create(
                brand=brand,
                name='Other',
                defaults={'slug': 'other'},
            )
            if was_created:
                other_created += 1

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! Created: {created}, Already existed: {skipped}, '
            f'Total in file: {len(entries)}'
        ))
        self.stdout.write(self.style.SUCCESS(
            f'Auto-added "Other" model to {other_created} brands'
        ))

        if missing_brands:
            self.stdout.write(self.style.ERROR(
                f'\nMissing brands ({len(missing_brands)}) - '
                f'run "python manage.py populate_motorcycle_brands" first:'
            ))
            for b in sorted(missing_brands):
                self.stdout.write(f'  - {b}')