# -*- coding: utf-8 -*-
"""
Atsukam 0106 užpildymą: paskyros numeris skelbime nėra skelbimo numeris.

0106 visiems be numerio esantiems skelbimams įrašė SAVININKO paskyros
numerį — tuo metu tai atrodė saugu, nes būtent tą numerį jie ir rodė.
Pasirodė kitaip: skelbimuose, kuriuos kuriant žmogus įvedė kitą numerį
(#833, #841, #844, #847 — įvestas +49 171 39200xx), tas įvestas numeris
buvo prarastas dar prieš 0106, o 0106 ant tuščios vietos užrašė asmeninį
+370 671 12478. Pirkėjas skambina ne ten, kur pardavėjas prašė.

Įvesto numerio atkurti nebėra iš ko — jis niekur nenugulė. Todėl
paliekam TUŠČIA: geriau jokio numerio, negu svetimas. Skelbimo
savininkas jį įrašys redaguodamas, o forma jam pasiūlys paskyros numerį
kaip numatytąją reikšmę (kontaktai.telefono_reiksme).

Valom TIKSLIAI tai, ką įrašė 0106, ir nieko daugiau:
  • skelbimas sukurtas PRIEŠ 0106 pritaikymą (vėlesni patys išsisaugo
    savo numerį — tiksli riba imama iš django_migrations.applied);
  • contact_phone sutampa su dabartiniu savininko paskyros numeriu.
Numeris, kurį žmogus pats įvedė ir kuris atsitiktinai sutampa su
paskyros numeriu, irgi bus išvalytas — atskirti jų nėra iš ko, o
rodyti svetimą numerį blogiau.

Atgal nesukam: prarastos reikšmės vis tiek nebėra.
"""
from django.db import migrations


def isvalyk_paskyros_numeri(apps, schema_editor):
    Listing = apps.get_model('listings', 'Listing')

    Profile = None
    for modelis in ('Profile', 'UserProfile'):
        try:
            Profile = apps.get_model('accounts', modelis)
            break
        except LookupError:
            continue
    if Profile is None:
        return

    # Kada 0106 buvo pritaikyta — po to sukurti skelbimai jos neliestos.
    riba = None
    with schema_editor.connection.cursor() as zymeklis:
        zymeklis.execute(
            "SELECT applied FROM django_migrations "
            "WHERE app = %s AND name = %s",
            ['listings', '0106_kontaktai_i_skelbima'])
        eilute = zymeklis.fetchone()
        if eilute:
            riba = eilute[0]

    numeriai = dict(
        Profile.objects.exclude(phone_number='')
        .exclude(phone_number__isnull=True)
        .values_list('user_id', 'phone_number')
    )

    isvalyta = 0
    for user_id, numeris in numeriai.items():
        qs = Listing.objects.filter(seller_id=user_id,
                                    contact_phone=(numeris or '')[:30])
        if riba is not None:
            qs = qs.filter(created_at__lt=riba)
        isvalyta += qs.update(contact_phone='')

    if isvalyta:
        print('    išvalyta paskyros numerių iš skelbimų: %d' % isvalyta)


def atgal(apps, schema_editor):
    """Nieko negrąžinam: 0106 reikšmė buvo klaidinga, o įvestos nebėra."""


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0106_kontaktai_i_skelbima'),
    ]

    operations = [
        migrations.RunPython(isvalyk_paskyros_numeri, atgal),
    ]
