# -*- coding: utf-8 -*-
"""Pilnas veiklos sričių sąrašas su grupėmis.

Senieji įrašai ne trinami, o PERVADINAMI (slug + pavadinimas), todėl
įmonių ryšiai išlieka: „padangos" tampa „padangu-montavimas" ir t. t.
"""
from django.db import migrations, models

# senas slug -> (naujas slug, pavadinimas, grupė, tvarka)
PERVADINTI = {
    'prekyba': ('automobiliu-prekyba', 'Automobilių prekyba', 'prekyba', 0),
    'supirkimas': ('automobiliu-supirkimas', 'Automobilių supirkimas', 'prekyba', 1),
    'servisas': ('remontas', 'Remontas', 'servisas', 10),
    'padangos': ('padangu-montavimas', 'Padangų montavimas', 'servisas', 11),
    'detailing': ('detailing', 'Detailing, poliravimas, keramika', 'servisas', 12),
    'plovykla': ('autoplovykla', 'Autoplovykla', 'servisas', 13),
    'evakuatorius': ('evakuatorius', 'Evakuatorius', 'servisas', 14),
    'technine-apziura': ('technine-apziura', 'Techninė apžiūra', 'servisas', 15),
}

# naujos sritys
NAUJOS = [
    ('dazymas-kebulo-remontas', 'Dažymas ir kėbulo remontas', 'servisas', 16),
    ('elektronika-diagnostika', 'Elektronika ir diagnostika', 'servisas', 17),
    ('duju-iranga', 'Dujų įranga', 'servisas', 18),
    ('stiklai', 'Stiklai', 'servisas', 19),
    ('apsaugos-sistemos', 'Apsaugos sistemos', 'servisas', 20),
]


def pilnas(apps, schema_editor):
    V = apps.get_model('imones', 'VeiklosSritis')
    for senas, (naujas, pav, grupe, tvarka) in PERVADINTI.items():
        eil = V.objects.filter(slug=senas).first()
        if eil:
            eil.slug, eil.pavadinimas = naujas, pav
            eil.grupe, eil.tvarka = grupe, tvarka
            eil.save()
        else:
            V.objects.get_or_create(slug=naujas, defaults={
                'pavadinimas': pav, 'grupe': grupe, 'tvarka': tvarka})
    for slug, pav, grupe, tvarka in NAUJOS:
        V.objects.get_or_create(slug=slug, defaults={
            'pavadinimas': pav, 'grupe': grupe, 'tvarka': tvarka})


def atgal(apps, schema_editor):
    V = apps.get_model('imones', 'VeiklosSritis')
    for senas, (naujas, _p, _g, _t) in PERVADINTI.items():
        V.objects.filter(slug=naujas).update(slug=senas)
    V.objects.filter(slug__in=[s for s, *_ in NAUJOS]).delete()


class Migration(migrations.Migration):
    dependencies = [('imones', '0003_imone_testine')]
    operations = [
        migrations.AddField(
            model_name='veiklossritis',
            name='grupe',
            field=models.CharField(choices=[('prekyba', 'Prekyba'),
                                            ('servisas', 'Servisai')],
                                   default='servisas', max_length=16),
        ),
        migrations.RunPython(pilnas, atgal),
    ]
