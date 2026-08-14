from django.db import migrations


# (slug, English name = msgid, display order)
GEAR_SUBCATEGORIES = [
    ('helmets', 'Helmets', 1),
    ('jackets', 'Jackets', 2),
    ('pants', 'Pants', 3),
    ('suits', 'Suits / Combinations', 4),
    ('gloves', 'Gloves', 5),
    ('boots', 'Boots', 6),
    ('protective-gear', 'Protective gear', 7),
    ('bags', 'Travel bags', 8),
    ('other-gear', 'Goggles & other gear', 9),
]


def seed(apps, schema_editor):
    VehicleType = apps.get_model('listings', 'VehicleType')
    SubCategory = apps.get_model('listings', 'SubCategory')

    moto_vt = VehicleType.objects.filter(slug='motorcycles').first()
    if not moto_vt:
        return

    parent = SubCategory.objects.filter(
        vehicle_type=moto_vt, slug='moto-gear',
    ).first()
    if not parent:
        return

    for slug, name, order in GEAR_SUBCATEGORIES:
        SubCategory.objects.update_or_create(
            vehicle_type=moto_vt,
            slug=slug,
            defaults={'name': name, 'parent': parent, 'order': order},
        )


def unseed(apps, schema_editor):
    VehicleType = apps.get_model('listings', 'VehicleType')
    SubCategory = apps.get_model('listings', 'SubCategory')

    moto_vt = VehicleType.objects.filter(slug='motorcycles').first()
    if not moto_vt:
        return

    slugs = [slug for slug, _name, _order in GEAR_SUBCATEGORIES]
    # Only drop the rows that never got used by a listing.
    SubCategory.objects.filter(
        vehicle_type=moto_vt, slug__in=slugs, listings__isnull=True,
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0053_alter_listing_gear_subtype'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
