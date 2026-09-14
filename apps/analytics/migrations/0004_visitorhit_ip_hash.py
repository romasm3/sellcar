# -*- coding: utf-8 -*-
"""
PageView → VisitorHit, žalias IP → sha256 maiša.

Lentelė ta pati, seni įrašai lieka — tik `ip_address` virsta `ip_hash`.
Maiša skaičiuojama iš turimo adreso, tad „tas pats lankytojas" atpažįstamas
ir istoriniuose įrašuose; paskui žalias stulpelis pašalinamas ir adreso DB
nebelieka.

Skaičiuojam paketais: lentelė gali būti didelė, o `.iterator()` +
`bulk_update` neužima atminties tiek, kiek visas sąrašas iš karto.
"""
from django.db import migrations, models


def i_maisa(apps, schema_editor):
    from django.utils import timezone
    from datetime import timedelta

    from apps.analytics.models import ip_maisa, SAUGOM_DIENAS

    Modelis = apps.get_model('analytics', 'VisitorHit')

    # Pirma išvalom tai, ko ir taip nebelaikom (>90 d.) — tada maišuoti
    # reikia mažiau eilučių ir migracija nestabdo diegimo. Kartu tai iškart
    # įgyvendina saugojimo terminą seniems įrašams.
    riba = timezone.now() - timedelta(days=SAUGOM_DIENAS)
    istrinta = Modelis.objects.filter(created_at__lt=riba).delete()[0]
    if istrinta:
        print('    senų (>%d d.) lankytojų įrašų ištrinta: %d'
              % (SAUGOM_DIENAS, istrinta))

    paketas = []
    pakeista = 0
    for eil in Modelis.objects.only('id', 'ip_address').iterator(chunk_size=5000):
        eil.ip_hash = ip_maisa(eil.ip_address)
        paketas.append(eil)
        if len(paketas) >= 5000:
            Modelis.objects.bulk_update(paketas, ['ip_hash'])
            pakeista += len(paketas)
            paketas = []
    if paketas:
        Modelis.objects.bulk_update(paketas, ['ip_hash'])
        pakeista += len(paketas)
    if pakeista:
        print('    lankytojų įrašų su maiša: %d' % pakeista)


def atgal(apps, schema_editor):
    """Atgal nesukam: maiša vienakryptė, IP atstatyti neįmanoma."""


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0003_pageview_bot_reason_pageview_is_bot_and_more'),
    ]

    operations = [
        migrations.RenameModel(old_name='PageView', new_name='VisitorHit'),
        migrations.AddField(
            model_name='visitorhit',
            name='ip_hash',
            field=models.CharField(db_index=True, default='', max_length=64),
            preserve_default=False,
        ),
        migrations.RunPython(i_maisa, atgal),
        # Senas (ip_address, created_at) indeksas — kartu su pačiu stulpeliu.
        migrations.RemoveIndex(model_name='visitorhit',
                               name='analytics_p_ip_addr_22a8c3_idx'),
        migrations.RemoveField(model_name='visitorhit', name='ip_address'),
    ]
