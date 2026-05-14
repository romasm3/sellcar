from django.core.management.base import BaseCommand
from apps.listings.models import VehicleType, SubCategory


class Command(BaseCommand):
    help = "Imports 3rd-level subcategories under 'Car Parts' (Parts → Car Parts → ...)"

    CHILDREN = [
        {'name': 'Whole car for parts', 'slug': 'whole-car-for-parts', 'order': 1},
        {'name': 'Single part / parts kit', 'slug': 'single-part-or-kit', 'order': 2},
    ]

    def handle(self, *args, **options):
        parts_vt = VehicleType.objects.filter(slug='parts').first()
        if not parts_vt:
            self.stdout.write(self.style.ERROR("VehicleType 'parts' not found."))
            return

        car_parts = SubCategory.objects.filter(
            vehicle_type=parts_vt,
            slug='car-parts',
            parent__isnull=True,
        ).first()
        if not car_parts:
            self.stdout.write(self.style.ERROR("SubCategory 'car-parts' (parent=None) not found."))
            return

        self.stdout.write(f"Parent: {car_parts} (id={car_parts.id})")

        created_count = 0
        updated_count = 0

        for entry in self.CHILDREN:
            child, created = SubCategory.objects.update_or_create(
                vehicle_type=parts_vt,
                slug=entry['slug'],
                defaults={
                    'name': entry['name'],
                    'parent': car_parts,
                    'order': entry['order'],
                },
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"  ✓ Created: {child.name} (id={child.id})"))
            else:
                # Ensure parent is set correctly
                if child.parent_id != car_parts.id:
                    child.parent = car_parts
                    child.save(update_fields=['parent'])
                updated_count += 1
                self.stdout.write(f"  ↻ Updated: {child.name} (id={child.id})")

        self.stdout.write(self.style.SUCCESS(
            f"\nDone. Created: {created_count}, Updated: {updated_count}"
        ))