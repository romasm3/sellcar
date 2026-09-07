# -*- coding: utf-8 -*-
"""
Management command: valyti_dubliuotas_nuotraukas

Sutvarko skelbimus, į kuriuos pakliuvo DVI nuotraukų partijos.

Kaip taip nutinka. Juodraščio nuotraukos keliauja AJAX'u iš karto, o
juodraštis laikomas sesijoje. Nulūžus pateikimui (500) sesijos raktas
likdavo, ir kitas bandymas pildė TĄ PATĮ juodraštį — skelbimas gaudavo
ir senas, ir naujas nuotraukas. Pati priežastis pataisyta
(apps/listings/juodrasciai.py + skaiciai.py); šita komanda sutvarko
tai, kas jau įvyko.

Naudojimas (visada pirma su --dry-run!):

    # parodo, kurios nuotraukos būtų ištrintos
    python manage.py valyti_dubliuotas_nuotraukas --skelbimas 754 \
        --palikti "rt460_" --dry-run

    # ištrina visas, kurių failo vardas prasideda „renault-t460_"
    python manage.py valyti_dubliuotas_nuotraukas --skelbimas 754 \
        --trinti "renault-t460_"

`--palikti` ir `--trinti` yra fragmentai failo varde. Nurodyti reikia
vieną iš jų: su `--palikti` trinama visa, kas NEATITINKA, su `--trinti`
— tik tai, kas atitinka. Po trynimo nuotraukos pernumeruojamos ir
pirmoji pažymima pagrindine.
"""
from django.core.management.base import BaseCommand, CommandError

from apps.listings.models import Listing


class Command(BaseCommand):
    help = 'Ištrina dubliuotas skelbimo nuotraukas pagal failo vardo fragmentą'

    def add_arguments(self, parser):
        parser.add_argument('--skelbimas', type=int, required=True,
                            help='Skelbimo id')
        parser.add_argument('--palikti', default='',
                            help='Palikti tik tas, kurių varde yra šis fragmentas')
        parser.add_argument('--trinti', default='',
                            help='Ištrinti tas, kurių varde yra šis fragmentas')
        parser.add_argument('--dry-run', action='store_true',
                            help='Tik parodo, ką trintų')

    def handle(self, *args, **options):
        pk = options['skelbimas']
        palikti = options['palikti']
        trinti = options['trinti']
        tik_parodyti = options['dry_run']

        if bool(palikti) == bool(trinti):
            raise CommandError('Nurodykite VIENĄ iš --palikti arba --trinti')

        try:
            skelbimas = Listing.objects.get(pk=pk)
        except Listing.DoesNotExist:
            raise CommandError('Skelbimo #%s nėra' % pk)

        visos = list(skelbimas.images.order_by('order', 'pk'))
        self.stdout.write('Skelbimas #%s „%s" — %d nuotraukos'
                          % (pk, (skelbimas.title or '—')[:40], len(visos)))

        smerkiamos = []
        for img in visos:
            vardas = (img.image.name or '').rsplit('/', 1)[-1]
            if palikti:
                if palikti not in vardas:
                    smerkiamos.append((img, vardas))
            elif trinti in vardas:
                smerkiamos.append((img, vardas))

        if not smerkiamos:
            self.stdout.write(self.style.SUCCESS('Nieko trinti nereikia'))
            return

        for img, vardas in smerkiamos:
            self.stdout.write('  − #%s  %s' % (img.pk, vardas))

        liks = len(visos) - len(smerkiamos)
        if liks <= 0:
            raise CommandError(
                'Taip būtų ištrintos VISOS %d nuotraukos — sustojam' % len(visos))

        if tik_parodyti:
            self.stdout.write(self.style.WARNING(
                'Trintume %d, liktų %d (dry-run)' % (len(smerkiamos), liks)))
            return

        for img, _vardas in smerkiamos:
            img.delete()

        # Pernumeruojam ir grąžinam pagrindinę — kitaip liktų skylės
        likusios = list(skelbimas.images.order_by('order', 'pk'))
        for eile, img in enumerate(likusios):
            img.order = eile
            img.is_main = (eile == 0)
            img.save(update_fields=['order', 'is_main'])

        self.stdout.write(self.style.SUCCESS(
            'Ištrinta %d, liko %d; pagrindinė — #%s'
            % (len(smerkiamos), len(likusios),
               likusios[0].pk if likusios else '—')))
