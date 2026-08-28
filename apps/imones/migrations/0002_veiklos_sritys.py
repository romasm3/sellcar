# -*- coding: utf-8 -*-
"""Veiklos sritys — pradinis žodynas iš užduoties aprašo.

Tai ne turinys, o pasirinkimų sąrašas (kaip kuro tipai), todėl gyvena
migracijoje: naujoje aplinkoje jis atsiranda savaime.
"""
from django.db import migrations

SRITYS = [
    'Prekyba', 'Supirkimas', 'Servisas', 'Padangos', 'Detailing',
    'Evakuatorius', 'Plovykla', 'Techninė apžiūra',
]


def prideti(apps, schema_editor):
    VeiklosSritis = apps.get_model('imones', 'VeiklosSritis')
    from django.utils.text import slugify
    for i, pavadinimas in enumerate(SRITYS):
        VeiklosSritis.objects.get_or_create(
            slug=slugify(pavadinimas)[:64],
            defaults={'pavadinimas': pavadinimas, 'tvarka': i})


def atgal(apps, schema_editor):
    VeiklosSritis = apps.get_model('imones', 'VeiklosSritis')
    from django.utils.text import slugify
    VeiklosSritis.objects.filter(
        slug__in=[slugify(s)[:64] for s in SRITYS]).delete()


class Migration(migrations.Migration):
    dependencies = [('imones', '0001_initial')]
    operations = [migrations.RunPython(prideti, atgal)]
