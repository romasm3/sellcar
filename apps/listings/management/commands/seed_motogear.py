"""
Pervadina Motorcycles VehicleType -> "Motorcycles & Moto Gear"
ir sukuria 3-level subcategory hierarchija:

    Motorcycles & Moto Gear (VehicleType)
      |- Motorcycles                  (SubCategory, parent=None, slug='motorcycles')
      |- Moto Gear, accessories       (SubCategory, parent=None, slug='moto-gear')
           |- Helmets                  (SubCategory, parent=moto-gear, slug='helmets')
           |- Protective gear          (slug='protective-gear')
           |- Boots                    (slug='boots')
           |- Pants                    (slug='pants')
           |- Suits / Combinations     (slug='suits')
           |- Bags / Backpacks         (slug='bags')
           |- Gloves                   (slug='gloves')
           |- Jackets                  (slug='jackets')
           |- Other                    (slug='other-gear')

Naudojimas:
    python manage.py seed_motogear
"""
from django.core.management.base import BaseCommand
from apps.listings.models import VehicleType, SubCategory


GEAR_CHILDREN = [
    ('helmets', 'Helmets', 1),
    ('protective-gear', 'Protective gear', 2),
    ('boots', 'Boots', 3),
    ('pants', 'Pants', 4),
    ('suits', 'Suits / Combinations', 5),
    ('bags', 'Bags / Backpacks', 6),
    ('gloves', 'Gloves', 7),
    ('jackets', 'Jackets', 8),
    ('other-gear', 'Other', 9),
]


class Command(BaseCommand):
    help = 'Renames Motorcycles VehicleType + seeds Moto Gear subcategories'

    def handle(self, *args, **options):
        # 1. Find/rename VehicleType
        moto_vt = VehicleType.objects.filter(slug='motorcycles').first()
        if not moto_vt:
            self.stdout.write(self.style.ERROR(
                'VehicleType slug=motorcycles not found. Create it first via admin.'
            ))
            return

        new_name = 'Motorcycles & Moto Gear'
        if moto_vt.name != new_name:
            moto_vt.name = new_name
            moto_vt.save(update_fields=['name'])
            self.stdout.write(self.style.SUCCESS(f'Renamed VehicleType -> {new_name}'))
        else:
            self.stdout.write(f'VehicleType already named: {new_name}')

        # 2. Top-level: Motorcycles
        motorcycles_sub, created = SubCategory.objects.get_or_create(
            vehicle_type=moto_vt,
            slug='motorcycles',
            defaults={'name': 'Motorcycles', 'order': 1, 'parent': None},
        )
        if created:
            self.stdout.write(self.style.SUCCESS('  + Top: Motorcycles'))
        else:
            # Make sure name/order/parent are correct
            changed = False
            if motorcycles_sub.name != 'Motorcycles':
                motorcycles_sub.name = 'Motorcycles'
                changed = True
            if motorcycles_sub.order != 1:
                motorcycles_sub.order = 1
                changed = True
            if motorcycles_sub.parent_id is not None:
                motorcycles_sub.parent = None
                changed = True
            if changed:
                motorcycles_sub.save()
                self.stdout.write(self.style.WARNING('  ~ Top: Motorcycles updated'))
            else:
                self.stdout.write('  = Top: Motorcycles')

        # 3. Top-level: Moto Gear (parent of all gear types)
        moto_gear_sub, created = SubCategory.objects.get_or_create(
            vehicle_type=moto_vt,
            slug='moto-gear',
            defaults={'name': 'Moto Gear, accessories', 'order': 2, 'parent': None},
        )
        if created:
            self.stdout.write(self.style.SUCCESS('  + Top: Moto Gear, accessories'))
        else:
            changed = False
            if moto_gear_sub.name != 'Moto Gear, accessories':
                moto_gear_sub.name = 'Moto Gear, accessories'
                changed = True
            if moto_gear_sub.order != 2:
                moto_gear_sub.order = 2
                changed = True
            if moto_gear_sub.parent_id is not None:
                moto_gear_sub.parent = None
                changed = True
            if changed:
                moto_gear_sub.save()
                self.stdout.write(self.style.WARNING('  ~ Top: Moto Gear updated'))
            else:
                self.stdout.write('  = Top: Moto Gear, accessories')

        # 4. Children of Moto Gear
        for slug, name, order in GEAR_CHILDREN:
            child, created = SubCategory.objects.get_or_create(
                vehicle_type=moto_vt,
                slug=slug,
                defaults={'name': name, 'order': order, 'parent': moto_gear_sub},
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'    + {name}'))
            else:
                changed = False
                if child.name != name:
                    child.name = name
                    changed = True
                if child.order != order:
                    child.order = order
                    changed = True
                if child.parent_id != moto_gear_sub.id:
                    child.parent = moto_gear_sub
                    changed = True
                if changed:
                    child.save()
                    self.stdout.write(self.style.WARNING(f'    ~ {name} updated'))
                else:
                    self.stdout.write(f'    = {name}')

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('Done.'))