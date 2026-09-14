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
    """Užpildo ip_hash iš turimo adreso.

    Ne eilutė po eilutės: skirtingų ADRESŲ yra kartais dešimt kartų mažiau
    nei eilučių (tas pats lankytojas atsiveria dešimt puslapių), tad
    maišuojam adresų sąrašą ir vienu UPDATE pažymim visas to adreso
    eilutes. `bulk_update` su modelio objektais tam pačiam darbui siunčia
    tūkstančius CASE sakinių ir dideliėje lentelėje užtrunka tiek, kad
    stabdo patį diegimą.
    """
    from datetime import timedelta

    from django.utils import timezone

    from apps.analytics.models import SAUGOM_DIENAS, ip_maisa

    Modelis = apps.get_model('analytics', 'VisitorHit')

    # Pirma išvalom tai, ko ir taip nebelaikom (>90 d.) — tada maišuoti
    # reikia mažiau eilučių. Kartu tai iškart įgyvendina saugojimo terminą.
    riba = timezone.now() - timedelta(days=SAUGOM_DIENAS)
    istrinta = Modelis.objects.filter(created_at__lt=riba).delete()[0]
    if istrinta:
        print('    senų (>%d d.) lankytojų įrašų ištrinta: %d'
              % (SAUGOM_DIENAS, istrinta))

    lentele = Modelis._meta.db_table
    # TIK `isnull`: GenericIPAddressField tuščią eilutę paverčia į None,
    # tad `.exclude(ip_address='')` virsta `NOT (ip_address = None)` ir
    # atmeta VISAS eilutes — maiša tada neįrašoma niekur.
    adresai = (Modelis.objects.exclude(ip_address__isnull=True)
               .values_list('ip_address', flat=True)
               .distinct().order_by())

    PAKETAS = 500
    buferis = []
    pakeista = 0

    def _israsyk(pora):
        # UPDATE ... SET ip_hash = CASE ip_address WHEN ? THEN ? ... END
        # WHERE ip_address IN (?, ?, ...) — vienas sakinys visam paketui.
        kai = ' '.join(['WHEN %s THEN %s'] * len(pora))
        vietos = ', '.join(['%s'] * len(pora))
        sql = ('UPDATE %s SET ip_hash = CASE ip_address %s END '
               'WHERE ip_address IN (%s)' % (lentele, kai, vietos))
        reiksmes = []
        for ip, maisa in pora:
            reiksmes.extend([ip, maisa])
        reiksmes.extend([ip for ip, _m in pora])
        with schema_editor.connection.cursor() as zymeklis:
            zymeklis.execute(sql, reiksmes)
            return zymeklis.rowcount or 0

    for ip in adresai.iterator(chunk_size=5000):
        buferis.append((ip, ip_maisa(ip)))
        if len(buferis) >= PAKETAS:
            pakeista += _israsyk(buferis)
            buferis = []
    if buferis:
        pakeista += _israsyk(buferis)

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
