"""Užsėja senųjų kategorijų ypatumų eilutes.

Automobilių, motociklų, moto aprangos, sunkvežimių ir sunkiojo
transporto dalių ypatumai (349 eilutės) DB egzistavo tik todėl, kad
kažkas kadaise atidarė jų create formą — jos kuriamos tingiai per
get_or_create. Švarioje aplinkoje tos formos rodytų 0 varnelių, o
filtrai būtų tušti (SKILL.md, SPĄSTAS 1).

Turinys perkeltas į equipment_registry, ši migracija jį užsėja.
Idempotentiška (get_or_create); reverse duomenų neliečia, kad
nenutrūktų esamos ListingEquipment nuorodos.
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
        ('listings', '0075_single_truck_part'),
    ]

    operations = [
        migrations.RunPython(seed_equipment, noop_reverse),
    ]
