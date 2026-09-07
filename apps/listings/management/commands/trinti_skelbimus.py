"""Rankinis skelbimų trynimas — su atsargine kopija ir patikromis.

Du režimai:

  A) NURODYTI ID — trina tik juos, tikrina, kad kiekis sutaptų:

     venv/bin/python manage.py trinti_skelbimus 748 746 321 \
         --saugoti 754 749 --patvirtinu

  B) VISKAS — išvalo visus skelbimus ir juodraščius („pradedam iš naujo"):

     venv/bin/python manage.py trinti_skelbimus --visus --patvirtinu

Prieš bet kurį — BŪTINA atsarginė kopija (be jos komanda neleis trinti):

    mkdir -p /root/autoleft_backups
    venv/bin/python manage.py dumpdata listings \
        > /root/autoleft_backups/listings_pries_valyma_$(date +%Y%m%d_%H%M).json
    venv/bin/python manage.py trinti_skelbimus --visus \
        --kopija /root/autoleft_backups/listings_pries_valyma_*.json --patvirtinu

Be --patvirtinu viskas yra sausas bėgimas: tik parodo, ką darytų.

Ką liečia. Dvi skelbimų lentelės: Listing (visos kategorijos) ir
WheelListing (ratlankiai/padangos — atskira lentelė). --visus išvalo
abi; --be-ratlankiu palieka ratlankius. Nuotraukų failai iš media/
trinami abiem (Listing turi 5 versijas, WheelListing — 1).

Ko NELIEČIA: naudotojų, markių/modelių, kategorijų, vertimų, kainų
planų. Migracijų nereikia.

Susiję objektai visi on_delete=CASCADE, PROTECT ryšių nėra — Django
išvalo pati: ListingImage, ListingView, ListingImpression,
PerziuretasSkelbimas, ListingEquipment, ListingReport, SavedListing,
SavedListingNotification, Conversation (su žinutėmis),
WheelImage, SavedWheelListing.
"""

import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import Count

from apps.listings.models import (
    Listing, ListingImage, WheelListing, WheelImage,
)

# ListingImage failų laukai — originalas + 4 išvestinės
LISTING_FAILU_LAUKAI = ('image', 'image_lg', 'image_lg_webp', 'image_sm', 'image_sm_webp')
# WheelImage — tik originalas
WHEEL_FAILU_LAUKAI = ('image',)

NUTYLIMA_KOPIJA = '/root/autoleft_backups/listings_pries_trynima.json'


class Command(BaseCommand):
    help = 'Ištrina nurodytus (arba visus) skelbimus kartu su nuotraukų failais.'

    def add_arguments(self, parser):
        parser.add_argument('ids', nargs='*', type=int,
                            help='Trinamų skelbimų ID (Listing).')
        parser.add_argument('--visus', action='store_true',
                            help='Išvalyti VISUS skelbimus ir juodraščius.')
        parser.add_argument('--be-ratlankiu', action='store_true',
                            help='Su --visus: palikti WheelListing (ratlankius/padangas).')
        parser.add_argument('--saugoti', nargs='*', type=int, default=[],
                            help='ID, kurie PRIVALO išlikti (tik ID režime).')
        parser.add_argument('--kopija', default=NUTYLIMA_KOPIJA,
                            help=f'dumpdata failas (nutylint {NUTYLIMA_KOPIJA}).')
        parser.add_argument('--patvirtinu', action='store_true',
                            help='Be šito — tik sausas bėgimas, niekas netrinama.')
        parser.add_argument('--be-kopijos', action='store_true',
                            help='Praleisti kopijos patikrą (nerekomenduojama).')

    # ── pagalbinės ────────────────────────────────────────────────
    def _tikrinti_kopija(self, kelias):
        if not os.path.exists(kelias):
            raise CommandError(
                f'Atsarginės kopijos nėra: {kelias}\n'
                f'Pirma paleisk:\n'
                f'  mkdir -p {os.path.dirname(kelias) or "."}\n'
                f'  venv/bin/python manage.py dumpdata listings > {kelias}'
            )
        dydis = os.path.getsize(kelias)
        if dydis < 1024:
            raise CommandError(f'Kopija {kelias} įtartinai maža ({dydis} B) — nutraukiu.')
        self.stdout.write(self.style.SUCCESS(
            f'✓ Kopija rasta: {kelias} ({dydis / 1024 / 1024:.1f} MB)'))

    def _keliai(self, qs, laukai):
        """Absoliutūs nuotraukų keliai iš duoto image-queryset. Tik media/ viduje."""
        saknis = os.path.realpath(str(settings.MEDIA_ROOT))
        keliai = []
        for img in qs.iterator():
            for laukas in laukai:
                f = getattr(img, laukas, None)
                if not f or not f.name:
                    continue
                pilnas = os.path.realpath(os.path.join(saknis, f.name))
                if pilnas.startswith(saknis + os.sep):   # niekada neišeinam iš media/
                    keliai.append(pilnas)
        return sorted(set(keliai))

    def _pagal_statusa(self, modelis, antraste):
        eilutes = (modelis.objects.values('status')
                   .annotate(kiek=Count('id')).order_by('status'))
        viso = modelis.objects.count()
        self.stdout.write(f'\n{antraste}: {viso}')
        for e in eilutes:
            self.stdout.write(f'    {e["status"] or "(be statuso)"}: {e["kiek"]}')
        return viso

    def _trinti_failus(self, keliai):
        istrinta = nerasta = 0
        for kelias in keliai:
            try:
                os.remove(kelias)
                istrinta += 1
            except FileNotFoundError:
                nerasta += 1
            except OSError as e:
                self.stdout.write(self.style.WARNING(f'  nepavyko {kelias}: {e}'))
        return istrinta, nerasta

    def _valyti_tuscius_katalogus(self):
        """Po failų trynimo lieka tušti metų/mėnesių katalogai — nušluojam."""
        saknis = os.path.realpath(str(settings.MEDIA_ROOT))
        pasalinta = 0
        for poaplankis in ('listings', 'wheels'):
            virsus = os.path.join(saknis, poaplankis)
            if not os.path.isdir(virsus):
                continue
            for katalogas, _, _ in sorted(os.walk(virsus), key=lambda t: -len(t[0])):
                if os.path.realpath(katalogas) == virsus:
                    continue
                try:
                    os.rmdir(katalogas)     # pavyks tik jei tuščias
                    pasalinta += 1
                except OSError:
                    pass
        if pasalinta:
            self.stdout.write(f'✓ Pašalinta tuščių katalogų: {pasalinta}')

    # ── pagrindinis ───────────────────────────────────────────────
    def handle(self, *args, **o):
        if o['visus'] and o['ids']:
            raise CommandError('Rinkis vieną: arba ID sąrašą, arba --visus.')
        if not o['visus'] and not o['ids']:
            raise CommandError('Nurodyk ID arba --visus. Nieko nedarau.')

        if not o['be_kopijos']:
            self._tikrinti_kopija(o['kopija'])
        else:
            self.stdout.write(self.style.WARNING('⚠ Kopijos patikra praleista.'))

        if o['visus']:
            self._viskas(o)
        else:
            self._pagal_ids(o)

    # ── režimas A: nurodyti ID ────────────────────────────────────
    def _pagal_ids(self, o):
        ids = sorted(set(o['ids']))
        saugoti = sorted(set(o['saugoti']))

        sankirta = set(ids) & set(saugoti)
        if sankirta:
            raise CommandError(f'NUTRAUKTA: trinamų sąraše yra saugomi ID: {sorted(sankirta)}')

        for pk in saugoti:
            if not Listing.objects.filter(pk=pk).exists():
                raise CommandError(f'NUTRAUKTA: saugomas skelbimas #{pk} neegzistuoja — patikrink ID.')

        qs = Listing.objects.filter(pk__in=ids)
        rasta = qs.count()
        self.stdout.write(f'\nNurodyta ID: {len(ids)} · rasta DB: {rasta}')
        if rasta != len(ids):
            nerasti = sorted(set(ids) - set(qs.values_list('pk', flat=True)))
            raise CommandError(
                f'NUTRAUKTA: rasta {rasta}, o nurodyta {len(ids)}.\nNerasti ID: {nerasti}')

        for l in qs.order_by('-pk'):
            self.stdout.write(f'  #{l.pk}: {l.title} ({l.status})')

        keliai = self._keliai(
            ListingImage.objects.filter(listing_id__in=ids), LISTING_FAILU_LAUKAI)
        self.stdout.write(f'\nNuotraukų failų media/: {len(keliai)}')

        if not o['patvirtinu']:
            self.stdout.write(self.style.WARNING(
                '\nSAUSAS BĖGIMAS — niekas neištrinta. Pridėk --patvirtinu.'))
            return

        istrinta, nerasta = self._trinti_failus(keliai)
        self.stdout.write(self.style.SUCCESS(
            f'✓ Failų ištrinta: {istrinta} (nerasta diske: {nerasta})'))

        with transaction.atomic():
            visi, pagal_modelius = Listing.objects.filter(pk__in=ids).delete()
        self._ataskaita(visi, pagal_modelius)

        self.stdout.write(f'\nListing liko iš viso: {Listing.objects.count()}')
        for pk in saugoti:
            l = Listing.objects.filter(pk=pk).first()
            if l:
                self.stdout.write(self.style.SUCCESS(f'✓ #{pk} vietoje: {l.title}'))
            else:
                self.stdout.write(self.style.ERROR(f'✗ #{pk} DINGO — tikrink kopiją!'))

    # ── režimas B: viskas ─────────────────────────────────────────
    def _viskas(self, o):
        if o['saugoti']:
            raise CommandError('--saugoti su --visus neveikia: --visus trina viską.')

        su_ratlankiais = not o['be_ratlankiu']

        self.stdout.write(self.style.WARNING('\n═══ PRIEŠ TRYNIMĄ ═══'))
        listing_viso = self._pagal_statusa(Listing, 'Listing (visos kategorijos)')
        wheel_viso = self._pagal_statusa(WheelListing, 'WheelListing (ratlankiai/padangos)')
        if not su_ratlankiais:
            self.stdout.write(self.style.WARNING(
                '  → --be-ratlankiu: WheelListing NEBUS trinamas.'))

        keliai = self._keliai(ListingImage.objects.all(), LISTING_FAILU_LAUKAI)
        if su_ratlankiais:
            keliai += self._keliai(WheelImage.objects.all(), WHEEL_FAILU_LAUKAI)
        keliai = sorted(set(keliai))
        self.stdout.write(f'\nNuotraukų failų media/: {len(keliai)}')

        if listing_viso == 0 and (wheel_viso == 0 or not su_ratlankiais):
            self.stdout.write(self.style.SUCCESS('\nNieko trinti — jau tuščia.'))
            return

        if not o['patvirtinu']:
            self.stdout.write(self.style.WARNING(
                f'\nSAUSAS BĖGIMAS — niekas neištrinta.\n'
                f'Būtų ištrinta: {listing_viso} Listing'
                + (f' + {wheel_viso} WheelListing' if su_ratlankiais else '')
                + f' ir {len(keliai)} failai.\nPridėk --patvirtinu.'))
            return

        istrinta, nerasta = self._trinti_failus(keliai)
        self.stdout.write(self.style.SUCCESS(
            f'✓ Failų ištrinta: {istrinta} (nerasta diske: {nerasta})'))

        with transaction.atomic():
            visi, pagal_modelius = Listing.objects.all().delete()
            if su_ratlankiais:
                w_visi, w_pagal = WheelListing.objects.all().delete()
                visi += w_visi
                for k, v in w_pagal.items():
                    pagal_modelius[k] = pagal_modelius.get(k, 0) + v
        self._ataskaita(visi, pagal_modelius)
        self._valyti_tuscius_katalogus()

        self.stdout.write(self.style.WARNING('\n═══ PO TRYNIMO ═══'))
        liko_l = Listing.objects.count()
        liko_w = WheelListing.objects.count()
        self.stdout.write(f'Listing liko: {liko_l}')
        self.stdout.write(f'WheelListing liko: {liko_w}')

        blogai = liko_l != 0 or (su_ratlankiais and liko_w != 0)
        if blogai:
            self.stdout.write(self.style.ERROR('✗ Liko įrašų — patikrink!'))
        else:
            self.stdout.write(self.style.SUCCESS('✓ Skelbimų lentelės tuščios.'))

        # Ko NELIETĖM — kad iškart matytųsi, jog liko vietoje
        from django.contrib.auth.models import User
        from apps.listings.models import Brand, VehicleType
        self.stdout.write('\nNepaliesta (turi likti):')
        self.stdout.write(f'    naudotojų: {User.objects.count()}')
        self.stdout.write(f'    markių: {Brand.objects.count()}')
        self.stdout.write(f'    kategorijų: {VehicleType.objects.count()}')

    def _ataskaita(self, visi, pagal_modelius):
        self.stdout.write(self.style.SUCCESS(f'\n✓ Ištrinta eilučių iš viso: {visi}'))
        for modelis, kiek in sorted(pagal_modelius.items()):
            self.stdout.write(f'    {modelis}: {kiek}')
