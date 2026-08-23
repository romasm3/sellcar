"""Sulieja savybes, kurios po pervadinimo atsidūrė dviese.

Tas pats angliškas pavadinimas kai kur gulėjo dviejose kategorijose
(pvz. „Sunroof" — interjere ir eksterjere, „Parking sensors" — elektronikoje
ir saugume). Pervadinus abi eilutes gavosi dublikatas. Paliekam seniausią
(mažiausią pk), pažymėjimus perkeliam į ją, likusią iškeliam į „legacy" —
netrinam nieko.
"""
from django.db import migrations

AUTO_KAT = ['interior', 'exterior', 'electronics', 'safety',
            'audio_video', 'other', 'electric']


def pirmyn(apps, schema_editor):
    Equipment = apps.get_model('listings', 'Equipment')
    ListingEquipment = apps.get_model('listings', 'ListingEquipment')

    matyti = {}
    for eq in Equipment.objects.filter(category__in=AUTO_KAT).order_by('pk'):
        raktas = (eq.name, eq.category)
        if raktas not in matyti:
            matyti[raktas] = eq
            continue
        tikslas = matyti[raktas]
        for ryšys in ListingEquipment.objects.filter(equipment=eq):
            if ListingEquipment.objects.filter(listing_id=ryšys.listing_id,
                                               equipment=tikslas).exists():
                ryšys.delete()
            else:
                ryšys.equipment = tikslas
                ryšys.save(update_fields=['equipment'])
        eq.category = 'legacy'
        eq.save(update_fields=['category'])


class Migration(migrations.Migration):

    dependencies = [('listings', '0089_savybes_lietuviskai')]

    operations = [migrations.RunPython(pirmyn, migrations.RunPython.noop)]
