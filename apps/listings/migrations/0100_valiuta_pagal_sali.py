# -*- coding: utf-8 -*-
"""
Esamiems skelbimams valiuta pagal šalį.

Iki šiol įkėlimo formos valiutos nesirinko — jos siųsdavo paslėptą
„USD", tad vokiškas #749 ir kroatiškas #754 rodė „$", nors kaina įvesta
eurais. Lietuviškas #727 rodė „€" tik todėl, kad modelio numatytoji
reikšmė yra EUR.

Keičiam TIK žymę, ne sumą: kaina buvo įvesta tos šalies valiuta, tik
pavadinta ne taip. Žemėlapis — apps/listings/valiutos.py.
"""
from django.db import migrations


def pagal_sali(apps, schema_editor):
    from apps.listings import valiutos

    Listing = apps.get_model('listings', 'Listing')
    pakeista = 0
    # Grupuojam pagal šalį — tiek pat užklausų, kiek šalių, o ne eilučių
    salys = (Listing.objects.values_list('country', flat=True)
             .distinct().order_by())
    for salis in salys:
        valiuta = valiutos.pagal_sali(salis)
        pakeista += (Listing.objects
                     .filter(country=salis)
                     .exclude(currency=valiuta)
                     .update(currency=valiuta))
    if pakeista:
        print('    valiuta pataisyta %d skelbimų' % pakeista)


def atgal(apps, schema_editor):
    """Atgal nesukam: sena reikšmė buvo klaidinga visoms šalims."""


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0099_alter_listing_boat_length_m_and_more'),
    ]

    operations = [
        migrations.RunPython(pagal_sali, atgal),
    ]
