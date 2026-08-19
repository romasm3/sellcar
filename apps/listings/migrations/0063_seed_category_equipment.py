"""Sukuria kategorijų ypatumų (Equipment) eilutes.

Anksčiau jos buvo kuriamos TINGIAI — `get_or_create` renderinant create
formą. Pasekmė: kol niekas neatidarė formos, išplėstinė paieška rodė 0
ypatumų, nes build_advanced() ieško jau egzistuojančių eilučių. Naujoje
aplinkoje (naujas deploy, atstatyta DB) priekabų, žemės ūkio ir krovimo
technikos filtruose varnelių tiesiog nebūtų.

Duomenų migracija, idempotentiška (get_or_create). Apibrėžimai imami iš
equipment_registry — jame nėra Django importų, todėl migracija jį gali
saugiai importuoti.

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
        ('listings', '0062_forestry_fields'),
    ]

    operations = [
        migrations.RunPython(seed_equipment, noop_reverse),
    ]
