# -*- coding: utf-8 -*-
"""
Aktyvuoja skelbimus, įstrigusius laukiant apmokėjimo.

Kol mokėjimai buvo įjungti, užpildytas skelbimas likdavo `draft` tol,
kol žmogus nusipirks planą. Išjungus mokėjimus tokie skelbimai patys
neatsirastų — juos aktyvuoja ši komanda.

Aktyvuojami TIK užpildyti juodraščiai: pusiau tuščias skelbimas į
svetainę nepakliūva (ta pati sąlyga, kurią naudoja planų puslapis ir
nemokamas publikavimas — apps/listings/views.py:_skelbimas_uzpildytas).

    python manage.py aktyvuok_istrigusius --bandymas   # tik parodo
    python manage.py aktyvuok_istrigusius              # aktyvuoja
    python manage.py aktyvuok_istrigusius --laiskai    # ir išsiunčia laiškus
"""
from django.conf import settings
from django.core.management.base import BaseCommand

from apps.listings.models import Listing


class Command(BaseCommand):
    help = 'Aktyvuoja užpildytus juodraščius, kurie kabo laukdami apmokėjimo'

    def add_arguments(self, parser):
        parser.add_argument('--bandymas', action='store_true',
                            help='tik parodo, ką aktyvuotų')
        parser.add_argument('--laiskai', action='store_true',
                            help='išsiųsti „skelbimas paskelbtas" laiškus')
        parser.add_argument('--dienos', type=int, default=None,
                            help='galiojimo dienos (numatytai kaip visur)')

    def handle(self, *args, **o):
        from apps.listings.views import _skelbimas_uzpildytas

        if getattr(settings, 'MOKEJIMAI_IJUNGTI', False):
            self.stdout.write(self.style.WARNING(
                'MOKEJIMAI_IJUNGTI = True — mokėjimai įjungti. Komanda vis '
                'tiek aktyvuos įstrigusius, bet pasitikrink, ar to nori.'))

        juodrasciai = (Listing.objects.filter(status='draft')
                       .select_related('vehicle_type', 'subcategory'))
        uzpildyti, tusti = [], []
        for l in juodrasciai:
            (uzpildyti if _skelbimas_uzpildytas(l) else tusti).append(l)

        self.stdout.write('Juodraščių iš viso: %d' % len(uzpildyti + tusti))
        self.stdout.write('  užpildytų (aktyvuosim): %d' % len(uzpildyti))
        self.stdout.write('  neužpildytų (liks juodraščiais): %d' % len(tusti))

        for l in uzpildyti[:20]:
            self.stdout.write('    #%s %s' % (l.pk, str(l)[:70]))
        if len(uzpildyti) > 20:
            self.stdout.write('    … dar %d' % (len(uzpildyti) - 20))

        if o['bandymas']:
            self.stdout.write(self.style.WARNING('\nBandymas — nieko nepakeista.'))
            return

        dienos = o['dienos'] or Listing.DEFAULT_ACTIVE_DAYS
        aktyvuota = laiskų = 0
        for l in uzpildyti:
            l.activate(days=dienos)
            aktyvuota += 1
            if o['laiskai'] and l.seller_id:
                try:
                    from apps.listings.views import _send_listing_published_email
                    _send_listing_published_email(l, l.seller)
                    laiskų += 1
                except Exception as e:
                    self.stderr.write('  #%s laiškas nepavyko: %s' % (l.pk, e))

        self.stdout.write(self.style.SUCCESS(
            '\nAktyvuota: %d (po %d d.), laiškų išsiųsta: %d'
            % (aktyvuota, dienos, laiskų)))
