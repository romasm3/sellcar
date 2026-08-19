"""Užsėja paslaugų (ir bet kurių naujų) ypatumų eilutes.

Kaip 0063 / 0065 / 0067 — RunPython per visą equipment_registry, nes jau
įvykdytos migracijos nebepaleidžiamos. Idempotentiška; reverse duomenų
neliečia, kad nenutrūktų esamos ListingEquipment nuorodos.
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
        ('listings', '0068_services_fields'),
    ]

    operations = [
        migrations.RunPython(seed_equipment, noop_reverse),
    ]
