"""Rankinis kelių skelbimų trynimas — su atsargine kopija ir patikromis.

    # 1. Atsarginė kopija (BŪTINA, komanda be jos neleis trinti):
    mkdir -p /root/autoleft_backups
    venv/bin/python manage.py dumpdata listings > /root/autoleft_backups/listings_pries_trynima.json

    # 2. Sausas bėgimas — tik parodo, ką rastų (nieko netrina):
    venv/bin/python manage.py trinti_skelbimus 748 746 321 --saugoti 754 749

    # 3. Tikras trynimas:
    venv/bin/python manage.py trinti_skelbimus 748 746 321 --saugoti 754 749 --patvirtinu

Ką daro:
  · reikalauja, kad kopijos failas egzistuotų ir būtų netuščias;
  · nutraukia darbą, jei rado ne tiek įrašų, kiek nurodyta ID (parodo, kurių nerado);
  · nutraukia darbą, jei tarp trinamų ID pakliuvo --saugoti ID;
  · pirma ištrina nuotraukų failus iš media/ (visas 5 versijas), tada įrašus;
  · pabaigoje parodo, kiek Listing liko ir ar --saugoti skelbimai vietoje.

Visos susijusios lentelės (ListingImage, ListingView, ListingImpression,
PerziuretasSkelbimas, ListingEquipment, ListingReport, SavedListing,
SavedListingNotification, Conversation) yra on_delete=CASCADE — Django
jas išvalys pati. PROTECT ryšių nėra.
"""

import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.listings.models import Listing, ListingImage

# ListingImage failų laukai — originalas + 4 išvestinės
FAILU_LAUKAI = ('image', 'image_lg', 'image_lg_webp', 'image_sm', 'image_sm_webp')

NUTYLIMA_KOPIJA = '/root/autoleft_backups/listings_pries_trynima.json'


class Command(BaseCommand):
    help = 'Ištrina nurodytus skelbimus (ID) kartu su jų nuotraukų failais.'

    def add_arguments(self, parser):
        parser.add_argument('ids', nargs='+', type=int,
                            help='Trinamų skelbimų ID.')
        parser.add_argument('--saugoti', nargs='*', type=int, default=[],
                            help='ID, kurie PRIVALO išlikti (patikra prieš ir po).')
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
                f'  mkdir -p {os.path.dirname(kelias)}\n'
                f'  venv/bin/python manage.py dumpdata listings > {kelias}'
            )
        dydis = os.path.getsize(kelias)
        if dydis < 1024:
            raise CommandError(f'Kopija {kelias} įtartinai maža ({dydis} B) — nutraukiu.')
        self.stdout.write(self.style.SUCCESS(
            f'✓ Kopija rasta: {kelias} ({dydis / 1024 / 1024:.1f} MB)'))

    def _failu_keliai(self, ids):
        """Absoliutūs nuotraukų keliai, priklausantys TIK šiems skelbimams."""
        saknis = os.path.realpath(str(settings.MEDIA_ROOT))
        keliai = []
        for img in ListingImage.objects.filter(listing_id__in=ids):
            for laukas in FAILU_LAUKAI:
                f = getattr(img, laukas, None)
                if not f or not f.name:
                    continue
                pilnas = os.path.realpath(os.path.join(saknis, f.name))
                # apsauga: niekada neišeinam iš media/
                if pilnas.startswith(saknis + os.sep):
                    keliai.append(pilnas)
        return sorted(set(keliai))

    # ── pagrindinis ───────────────────────────────────────────────
    def handle(self, *args, **o):
        ids = sorted(set(o['ids']))
        saugoti = sorted(set(o['saugoti']))
        tikra = o['patvirtinu']

        if not o['be_kopijos']:
            self._tikrinti_kopija(o['kopija'])
        else:
            self.stdout.write(self.style.WARNING('⚠ Kopijos patikra praleista.'))

        # 1. Ar nesikerta su saugomais?
        sankirta = set(ids) & set(saugoti)
        if sankirta:
            raise CommandError(f'NUTRAUKTA: trinamų sąraše yra saugomi ID: {sorted(sankirta)}')

        # 2. Ar saugomi apskritai egzistuoja?
        for pk in saugoti:
            if not Listing.objects.filter(pk=pk).exists():
                raise CommandError(f'NUTRAUKTA: saugomas skelbimas #{pk} neegzistuoja — patikrink ID.')

        # 3. Ar radome tiek, kiek nurodyta?
        qs = Listing.objects.filter(pk__in=ids)
        rasta = qs.count()
        self.stdout.write(f'\nNurodyta ID: {len(ids)} · rasta DB: {rasta}')
        if rasta != len(ids):
            nerasti = sorted(set(ids) - set(qs.values_list('pk', flat=True)))
            raise CommandError(
                f'NUTRAUKTA: rasta {rasta}, o nurodyta {len(ids)}.\n'
                f'Nerasti ID: {nerasti}'
            )

        for l in qs.order_by('-pk'):
            self.stdout.write(f'  #{l.pk}: {l.title} ({l.status})')

        # 4. Nuotraukų failai
        keliai = self._failu_keliai(ids)
        self.stdout.write(f'\nNuotraukų failų media/: {len(keliai)}')

        if not tikra:
            self.stdout.write(self.style.WARNING(
                '\nSAUSAS BĖGIMAS — niekas neištrinta. Pridėk --patvirtinu.'))
            return

        # 5. Failai iš disko
        istrinta_failu = nerasta_failu = 0
        for kelias in keliai:
            try:
                os.remove(kelias)
                istrinta_failu += 1
            except FileNotFoundError:
                nerasta_failu += 1
            except OSError as e:
                self.stdout.write(self.style.WARNING(f'  nepavyko {kelias}: {e}'))
        self.stdout.write(self.style.SUCCESS(
            f'✓ Failų ištrinta: {istrinta_failu} (nerasta diske: {nerasta_failu})'))

        # 6. Įrašai
        with transaction.atomic():
            visi, pagal_modelius = Listing.objects.filter(pk__in=ids).delete()
        self.stdout.write(self.style.SUCCESS(f'✓ Ištrinta eilučių iš viso: {visi}'))
        for modelis, kiek in sorted(pagal_modelius.items()):
            self.stdout.write(f'    {modelis}: {kiek}')

        # 7. Patikra po trynimo
        liko = Listing.objects.count()
        self.stdout.write(f'\nListing liko iš viso: {liko}')
        for pk in saugoti:
            if Listing.objects.filter(pk=pk).exists():
                l = Listing.objects.get(pk=pk)
                self.stdout.write(self.style.SUCCESS(f'✓ #{pk} vietoje: {l.title}'))
            else:
                self.stdout.write(self.style.ERROR(f'✗ #{pk} DINGO — tikrink kopiją!'))
