# -*- coding: utf-8 -*-
"""
Esamiems skelbimams valiuta grąžinama į EUR.

0100 valiutą sudėliojo pagal šalį. Klaida buvo ta, kad keitėsi tik ŽYMĖ,
o suma ne: #789 Dodge RAM įvestas 43 000 € rodė „43 000 zł" (≈10 000 €),
#791 Lamborghini Urus — „327 250 kr", #798 Audi S5 — „45 942 CHF",
#792 ir #799 — „kr".

Kaina visuose įvesta eurais, tad taisom TIK žymę — sumų neliečiam.
Kursų svetainė neturi; daugiavaliutės (GBP/USD) bus atskiras darbas.
"""
from django.db import migrations

EUR = 'EUR'
LENTELES = ('Listing', 'Truck', 'SalesRecord', 'TruckSalesRecord')


def i_eurus(apps, schema_editor):
    for vardas in LENTELES:
        modelis = apps.get_model('listings', vardas)
        pakeista = modelis.objects.exclude(currency=EUR).update(currency=EUR)
        if pakeista:
            print('    %s: valiuta → EUR, %d eil.' % (vardas, pakeista))


def atgal(apps, schema_editor):
    """Atgal nesukam: sena reikšmė melavo apie kainą."""


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0102_listing_axle_count'),
    ]

    operations = [
        migrations.RunPython(i_eurus, atgal),
    ]
