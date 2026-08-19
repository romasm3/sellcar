"""Užsėja turistinių namelių (ir bet kurių naujų) ypatumų eilutes.

0063 užsėjo tai, kas buvo registre tuo metu. Pridėjus naują kategoriją
(camping-houses, 52 ypatumai) reikia dar vieno RunPython — jau įvykdytos
migracijos pakartotinai nebepaleidžiamos.

seed() eina per VISĄ registrą, todėl ši migracija užsėja ir bet kurias
kitas, kurios per tą laiką atsirado. Idempotentiška (get_or_create).

reverse_code duomenų neliečia: eilučių trynimas nutrauktų jau esamas
ListingEquipment nuorodas.
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
        ('listings', '0064_camping_houses_fields'),
    ]

    operations = [
        migrations.RunPython(seed_equipment, noop_reverse),
    ]
