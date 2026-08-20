"""Sunkiojo transporto dalis — trūkstama „Dalys" šakos subkategorija.

Etalone (sec 23) „Sunkiojo transporto dalys" yra normali dalies forma, o
pas mus po `truck-parts` buvo tik „Sunkvežimis dalimis". Naršymas
(/browse/truck-parts/) ir išplėstinė paieška veikė, bet įdėti tokio
skelbimo nebuvo kaip — aklavietė iš vartotojo pusės.

Aptarnaus bendra dalių forma (parts_listing_create), kaip ir žemės ūkio
bei aksesuarų šakos.
"""
from django.db import migrations


SLUG = 'single-truck-part'


def create_sub(apps, schema_editor):
    SubCategory = apps.get_model('listings', 'SubCategory')
    VehicleType = apps.get_model('listings', 'VehicleType')

    parts_vt = VehicleType.objects.filter(slug='parts').first()
    if not parts_vt:
        return
    parent = SubCategory.objects.filter(
        vehicle_type=parts_vt, slug='truck-parts').first()
    if not parent:
        return
    SubCategory.objects.get_or_create(
        vehicle_type=parts_vt,
        slug=SLUG,
        defaults={
            'name': 'Single truck part',
            'parent': parent,
            'order': 2,
        },
    )


def drop_sub(apps, schema_editor):
    """Atgal — tik jei eilutė tuščia; su skelbimais netrinam."""
    SubCategory = apps.get_model('listings', 'SubCategory')
    Listing = apps.get_model('listings', 'Listing')
    sub = SubCategory.objects.filter(slug=SLUG).first()
    if sub and not Listing.objects.filter(subcategory=sub).exists():
        sub.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0074_wheel_rim_features'),
    ]

    operations = [
        migrations.RunPython(create_sub, drop_sub),
    ]
