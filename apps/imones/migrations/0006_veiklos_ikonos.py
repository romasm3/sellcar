# -*- coding: utf-8 -*-
"""Kiekviena veiklos sritis gauna savo Font Awesome ikoną.

Rinkinys tas pats kaip kategorijų ikonoms (listing_filters), todėl
sąraše nebelieka penkių vienodų raktų.
"""
from django.db import migrations, models

IKONOS = {
    'automobiliu-prekyba': 'fa-car-side',
    'automobiliu-supirkimas': 'fa-hand-holding-dollar',
    'remontas': 'fa-screwdriver-wrench',
    'padangu-montavimas': 'fa-circle-notch',
    'detailing': 'fa-spray-can-sparkles',
    'autoplovykla': 'fa-soap',
    'evakuatorius': 'fa-truck-ramp-box',
    'technine-apziura': 'fa-clipboard-check',
    'dazymas-kebulo-remontas': 'fa-paint-roller',
    'elektronika-diagnostika': 'fa-microchip',
    'duju-iranga': 'fa-gas-pump',
    'stiklai': 'fa-car-side',
    'apsaugos-sistemos': 'fa-shield-halved',
}


def prideti(apps, schema_editor):
    V = apps.get_model('imones', 'VeiklosSritis')
    for slug, ikona in IKONOS.items():
        V.objects.filter(slug=slug).update(ikona=ikona)


class Migration(migrations.Migration):
    dependencies = [('imones', '0005_imone_veikia_nuo')]
    operations = [
        migrations.AddField(
            model_name='veiklossritis',
            name='ikona',
            field=models.CharField(default='fa-screwdriver-wrench', max_length=48),
        ),
        migrations.RunPython(prideti, migrations.RunPython.noop),
    ]
