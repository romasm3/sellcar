"""Sec 04/02/05 ypatumai, kurių registre nebuvo.

Be jų išplėstinė paieška rodė 5 iš 16 sunkvežimių ypatumų, 10 iš 25
motociklų ir 4 iš 11 vandens transporto (2026-08-20 auditas).
"""
from django.db import migrations

from apps.listings.equipment_registry import seed


def forwards(apps, schema_editor):
    Equipment = apps.get_model('listings', 'Equipment')
    seed(Equipment)


def backwards(apps, schema_editor):
    """Sėja idempotentiška — atgal nieko netrinam."""


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0078_brand_suggestions'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
