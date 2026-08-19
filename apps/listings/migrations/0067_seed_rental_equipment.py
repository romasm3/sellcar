"""Užsėja transporto nuomos (ir bet kurių naujų) ypatumų eilutes.

Kaip ir 0063 / 0065 — RunPython per visą equipment_registry. Reikalinga,
nes jau įvykdytos migracijos nebepaleidžiamos, o be eilučių išplėstinė
paieška rodytų 0 ypatumų (žr. SKILL.md, SPĄSTAS 1).

Idempotentiška (get_or_create); reverse duomenų neliečia.
"""
from django.db import migrations

from apps.listings.equipment_registry import seed


def seed_equipment(apps, schema_editor):
    Equipment = apps.get_model('listings', 'Equipment')
    seed(Equipment)


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0066_rental_fields'),
    ]

    operations = [
        migrations.RunPython(seed_equipment, noop_reverse),
    ]
