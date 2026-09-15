# -*- coding: utf-8 -*-
"""
Esamiems skelbimams — savas telefono numeris.

Iki šiol numeris gulėjo tik paskyroje (`profile.phone_number`): vienas
laukas visiems žmogaus skelbimams. Pakeitus jį viename skelbime jis
tyliai pasikeisdavo VISUOSE kituose (#821–#825 ėmė rodyti tą patį
numerį). Nuo šiol kiekvienas skelbimas turi savo `contact_phone`.

Kad niekas neliktų be kontakto, visiems esamiems skelbimams įrašom
dabartinį SAVININKO paskyros numerį — tai reikšmė, kurią jie ir rodė iki
šiol, tad vartotojui niekas nepasikeičia. Skirtumas tik toks, kad nuo
dabar ji yra skelbimo, o ne paskyros.

Antra dalis: išvalom `contact_email`, jei jame netyčia atsidūrė portalo
palaikymo adresas (DEFAULT_FROM_EMAIL). Vartotojo skelbime jis neturi
atsirasti niekada; ištrynus laukas tampa tuščias, o
`kontaktinis_pastas` tada grąžina paskyros adresą.

Atgal nesukam: `contact_phone` stulpelį pašalintų pati 0105 migracija.
"""
from django.conf import settings
from django.db import migrations


def i_skelbimus(apps, schema_editor):
    Listing = apps.get_model('listings', 'Listing')

    # Grupuojam pagal pardavėją — tiek pat užklausų, kiek pardavėjų, o ne
    # kiek skelbimų.
    Profile = None
    for modelis in ('Profile', 'UserProfile'):
        try:
            Profile = apps.get_model('accounts', modelis)
            break
        except LookupError:
            continue

    pakeista = 0
    if Profile is not None:
        numeriai = dict(
            Profile.objects.exclude(phone_number='')
            .exclude(phone_number__isnull=True)
            .values_list('user_id', 'phone_number')
        )
        for user_id, numeris in numeriai.items():
            pakeista += (Listing.objects
                         .filter(seller_id=user_id, contact_phone='')
                         .update(contact_phone=(numeris or '')[:30]))
    if pakeista:
        print('    skelbimų su savo telefono numeriu: %d' % pakeista)

    liko = Listing.objects.filter(contact_phone='').count()
    if liko:
        print('    be numerio liko %d (savininkas jo neturi nė paskyroje)' % liko)


def isvalyk_portalo_pasta(apps, schema_editor):
    """Portalo palaikymo adresas vartotojo skelbime neturi atsirasti."""
    Listing = apps.get_model('listings', 'Listing')
    portalo = (getattr(settings, 'DEFAULT_FROM_EMAIL', '') or '').strip()
    if not portalo:
        return
    istrinta = (Listing.objects
                .filter(contact_email__iexact=portalo)
                .update(contact_email=''))
    if istrinta:
        print('    skelbimų, kuriuose buvo portalo paštas (%s): %d'
              % (portalo, istrinta))


def atgal(apps, schema_editor):
    """Atgal nesukam — stulpelį pašalina 0105."""


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0105_listing_contact_phone'),
    ]

    operations = [
        migrations.RunPython(i_skelbimus, atgal),
        migrations.RunPython(isvalyk_portalo_pasta, atgal),
    ]
