import os
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from apps.listings.models import Brand, VehicleType


class Command(BaseCommand):
    help = 'Import car brands from brands.txt file'

    def handle(self, *args, **kwargs):
        # Get or create "Car" vehicle type
        vehicle_type, _ = VehicleType.objects.get_or_create(
            slug='cars',
            defaults={'name': 'Cars', 'order': 1}
        )

        # brands.txt must be in the same folder as this file
        txt_path = os.path.join(os.path.dirname(__file__), 'brands.txt')

        if not os.path.exists(txt_path):
            self.stdout.write(self.style.ERROR(f'brands.txt not found at: {txt_path}'))
            return

        with open(txt_path, 'r', encoding='utf-8') as f:
            brands = [line.strip() for line in f if line.strip()]

        created = 0
        skipped = 0
        for name in brands:
            # Check if already exists by name
            if Brand.objects.filter(name=name).exists():
                skipped += 1
                continue

            # Generate unique slug
            base_slug = slugify(name) or slugify(name.encode('ascii', 'ignore').decode()) or f'brand-{name.lower().replace(" ", "-")}'
            slug = base_slug
            counter = 1
            while Brand.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1

            Brand.objects.create(
                name=name,
                slug=slug,
                vehicle_type=vehicle_type
            )
            created += 1
            self.stdout.write(f'  + {name}')

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! Created: {created}, Already existed: {skipped}, Total: {len(brands)}'
        ))