# -*- coding: utf-8 -*-
"""
Management command: valyti_juodrascius

Šluoja PAKIBUSIUS juodraščius — tuos, kurių niekas nebetęsia.

Kodėl reikia. Įkėlimo formos juodraštį laiko sesijoje, o nuotraukos
AJAX'u keliauja tiesiai į jį. Nulūžus pateikimui (pvz. per didelis
skaičius — žr. apps/listings/skaiciai.py) juodraštis lieka gulėti su
nuotraukomis. Nuo šiol šviežias formos atidarymas prie tokio
nebeprisiriša (apps/listings/juodrasciai.py), tad jie tiesiog kaupiasi
— šita komanda juos ir surenka.

Cron (serveryje, šalia expire_listings 03:30):

    30 3 * * *  cd /root/autoleft && .venv/bin/python manage.py expire_listings
    40 3 * * *  cd /root/autoleft && .venv/bin/python manage.py valyti_juodrascius

Naudojimas:
    python manage.py valyti_juodrascius --dry-run     # tik parodo
    python manage.py valyti_juodrascius               # trina (30 d.)
    python manage.py valyti_juodrascius --dienos 7
    python manage.py valyti_juodrascius --ir-su-nuotraukomis

Numatytai TUŠČIUS juodraščius trinam po 30 dienų, o turinčius
nuotraukų ar aprašymo — NE: tai žmogaus darbas, jis mato juos „Mano
skelbimuose". Su `--ir-su-nuotraukomis` trinami ir tokie (tada verta
imti didesnį `--dienos`).
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from apps.listings.juodrasciai import tuscias
from apps.listings.models import Listing

NUMATYTOS_DIENOS = 30


class Command(BaseCommand):
    help = 'Ištrina pakibusius juodraščius, senesnius nei N dienų'

    def add_arguments(self, parser):
        parser.add_argument('--dienos', type=int, default=NUMATYTOS_DIENOS,
                            help='Kiek dienų juodraštis laikomas (30)')
        parser.add_argument('--dry-run', action='store_true',
                            help='Tik parodo, ką trintų')
        parser.add_argument('--ir-su-nuotraukomis', action='store_true',
                            help='Trinti ir turinčius nuotraukų ar aprašymo')

    def handle(self, *args, **options):
        dienos = options['dienos']
        tik_parodyti = options['dry_run']
        ir_su_turiniu = options['ir_su_nuotraukomis']
        riba = timezone.now() - timedelta(days=dienos)

        seni = (Listing.objects.filter(status='draft', updated_at__lt=riba)
                .order_by('pk'))

        trinami, palikti = [], []
        for juodrastis in seni.iterator():
            if ir_su_turiniu or tuscias(juodrastis):
                trinami.append(juodrastis)
            else:
                palikti.append(juodrastis)

        for juodrastis in trinami:
            self.stdout.write('  #%s  %s  (%s)' % (
                juodrastis.pk,
                (juodrastis.title or '—')[:40],
                juodrastis.updated_at.strftime('%Y-%m-%d')))
            if not tik_parodyti:
                juodrastis.delete()

        self.stdout.write(self.style.SUCCESS(
            '%s %d juodraščių (senesnių nei %d d.); palikta su turiniu: %d'
            % ('Rastume' if tik_parodyti else 'Ištrinta',
               len(trinami), dienos, len(palikti))))
