"""Užsėja el. paspirtukų / riedžių / dviračių ypatumų eilutes.

Kaip 0063 / 0065 / 0067 / 0069 / 0071 — RunPython per visą registrą.
Idempotentiška; reverse duomenų neliečia.
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
        ('listings', '0072_bicycles_fields'),
    ]

    operations = [
        migrations.RunPython(seed_equipment, noop_reverse),
    ]
