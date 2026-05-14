"""
Užpildo Equipment lentelę moto gear features'ais (autoplius-style).

Naudojimas:
    python manage.py seed_motogear_equipment
    python manage.py seed_motogear_equipment --clean
"""
from django.core.management.base import BaseCommand
from apps.listings.models import Equipment


GEAR_FEATURES = [
    # ═══ HELMET-only ═══
    ('Anti-scratch visor',           'helmet',                            10),
    ('Anti-fog visor',               'helmet',                            20),
    ('Heated visor',                 'helmet',                            30),
    ('UV protection',                'helmet',                            40),
    ('Internal sun visor',           'helmet',                            50),
    ('Pinlock ready',                'helmet',                            60),
    ('Quick-release strap',          'helmet',                            70),
    ('Micrometric buckle',           'helmet',                            80),
    ('Double D-ring buckle',         'helmet',                            90),
    ('Glasses-friendly',             'helmet',                           100),
    ('Bluetooth-ready',              'helmet',                           110),
    ('Removable cheek pads',         'helmet',                           120),

    # ═══ APPAREL ═══
    ('CE armor — shoulders',         'jacket,suit,protective',           200),
    ('CE armor — elbows',            'jacket,suit,protective',           210),
    ('CE armor — back',              'jacket,suit,pants,protective',     220),
    ('CE armor — chest',             'jacket,suit,protective',           230),
    ('CE armor — knees',             'pants,suit,protective',            240),
    ('CE armor — hips',              'pants,suit,protective',            250),
    ('Waterproof',                   'jacket,pants,suit,gloves,boots,bag', 260),
    ('Windproof',                    'jacket,pants,suit,gloves',         270),
    ('Thermal liner',                'jacket,pants,suit,gloves',         280),
    ('Removable liner',              'jacket,pants,suit',                290),
    ('Ventilation zippers',          'jacket,pants,suit',                300),
    ('Reflective elements',          'jacket,pants,suit,gloves,boots',   310),
    ('Reinforced impact zones',      'jacket,pants,suit',                320),
    ('Connection zipper (jacket↔pants)', 'jacket,pants',                 330),
    ('Hump (aerodynamic)',           'jacket,suit',                      340),

    # ═══ LINING / COMFORT ═══
    ('Breathable lining',            'helmet,jacket,pants,suit,gloves',  400),
    ('Hypoallergenic lining',        'helmet,jacket,pants,suit',         410),
    ('Removable & washable lining',  'helmet,jacket,pants,suit',         420),
    ('Moisture-wicking lining',      'helmet,jacket,pants,suit',         430),

    # ═══ GLOVES ═══
    ('Touchscreen-compatible',       'gloves',                           500),
    ('Knuckle protector',            'gloves',                           510),
    ('Palm slider',                  'gloves',                           520),
    ('Long cuff',                    'gloves',                           530),
    ('Short cuff',                   'gloves',                           540),

    # ═══ BOOTS ═══
    ('Ankle protection',             'boots',                            600),
    ('Shin protection',              'boots',                            610),
    ('Toe slider',                   'boots',                            620),
    ('Heel protection',              'boots',                            630),
    ('Reinforced sole',              'boots',                            640),

    # ═══ BAGS ═══
    ('Magnetic mount',               'bag',                              700),
    ('Strap mount',                  'bag',                              710),
    ('Rain cover',                   'bag',                              720),
    ('Expandable',                   'bag',                              730),
    ('Laptop compartment',           'bag',                              740),

    # ═══ UNIVERSAL ═══
    ('Open to trade',                '',                                 900),
]


class Command(BaseCommand):
    help = 'Seeds Equipment table with moto gear features'

    def add_arguments(self, parser):
        parser.add_argument('--clean', action='store_true')

    def handle(self, *args, **options):
        if options['clean']:
            count = Equipment.objects.filter(category='gear').count()
            Equipment.objects.filter(category='gear').delete()
            self.stdout.write(self.style.WARNING(f'Deleted {count} existing gear features.'))

        created = 0
        updated = 0
        for name, gear_types, order in GEAR_FEATURES:
            obj, was_created = Equipment.objects.get_or_create(
                name=name, category='gear',
                defaults={'gear_types': gear_types, 'order': order, 'vehicle_type': None},
            )
            if was_created:
                created += 1
            else:
                changed = False
                if obj.gear_types != gear_types:
                    obj.gear_types = gear_types
                    changed = True
                if obj.order != order:
                    obj.order = order
                    changed = True
                if changed:
                    obj.save(update_fields=['gear_types', 'order'])
                    updated += 1

        self.stdout.write(self.style.SUCCESS(
            f'Done. Created: {created}, Updated: {updated}, Total gear features: {Equipment.objects.filter(category="gear").count()}'
        ))