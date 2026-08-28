# -*- coding: utf-8 -*-
"""
Bandomosios įmonės — kad būtų ką pamatyti, kol tikrų dar nėra.

    manage.py imones_testines              # sukuria arba atnaujina
    manage.py imones_testines --pasalinti  # pašalina TIK testines

Visos sukuriamos su `testine=True`, todėl jas visada galima rasti
(admin filtras „Testinė") ir pašalinti viena komanda. Tikrų įmonių ši
komanda neliečia.

Prekiautojas rišamas prie JAU esamos paskyros, kuri turi skelbimų —
skelbimų savininkų nekeičiam, todėl niekas realiai nepersirašo.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.imones.models import Imone, ImonesPaslauga, VeiklosSritis

DARBAS = {str(d): ['08:00', '18:00'] for d in range(5)}
DARBAS['5'] = ['09:00', '14:00']
DARBAS['6'] = None

DARBAS_ILGAS = {str(d): ['08:00', '20:00'] for d in range(5)}
DARBAS_ILGAS['5'] = ['10:00', '16:00']
DARBAS_ILGAS['6'] = None

IMONES = [
    {
        'raktas': 'test-prekiautojas',
        'tipas': Imone.PREKIAUTOJAS,
        'pavadinimas': 'AutoLeft Demo prekyba',
        'aprasymas': 'Bandomoji įmonė. Naudoti automobiliai, mikroautobusai '
                     'ir sunkusis transportas. Priimame seną automobilį '
                     'kaip dalį apmokėjimo.',
        'adresas': 'Chemijos g. 12',
        'miestas': 'Kaunas',
        'lat': 54.91162, 'lng': 23.97197,
        'telefonas': '+370 600 11122',
        'el_pastas': 'demo.prekyba@example.com',
        'svetaine': 'https://example.com/prekyba',
        'darbo_laikas': DARBAS,
        'veiklos': ['prekyba', 'supirkimas'],
        'su_skelbimais': True,
        'paslaugos': [],
    },
    {
        'raktas': 'test-padangos',
        'tipas': Imone.SERVISAS,
        'pavadinimas': 'AutoLeft Demo padangos',
        'aprasymas': 'Bandomoji įmonė. Padangų montavimas, balansavimas, '
                     'geometrija ir sezoninis padangų sandėliavimas.',
        'adresas': 'Taikos pr. 88',
        'miestas': 'Kaunas',
        'lat': 54.88374, 'lng': 23.94208,
        'telefonas': '+370 612 34567',
        'el_pastas': 'demo.padangos@example.com',
        'svetaine': '',
        'darbo_laikas': DARBAS,
        'veiklos': ['padangos', 'servisas'],
        'su_skelbimais': False,
        'paslaugos': [
            ('Padangų montavimas — R13–R15', '4 ratai', 40, 30),
            ('Padangų montavimas — R17–R19', '4 ratai', 50, 44),
            ('Ratų balansavimas', '1 ratas', 10, 6),
            ('Geometrijos reguliavimas', 'Lengvasis automobilis', 60, 45),
            ('Padangų sandėliavimas', 'Sezonui · 4 ratai', None, 25),
        ],
    },
    {
        'raktas': 'test-detailing',
        'tipas': Imone.SERVISAS,
        'pavadinimas': 'AutoLeft Demo detailing',
        'aprasymas': 'Bandomoji įmonė. Kėbulo poliravimas, keramikinė danga, '
                     'salono valymas ir kvapo šalinimas.',
        'adresas': 'Savanorių pr. 174',
        'miestas': 'Vilnius',
        'lat': 54.66892, 'lng': 25.23452,
        'telefonas': '+370 655 90210',
        'el_pastas': 'demo.detailing@example.com',
        'svetaine': 'https://example.com/detailing',
        'darbo_laikas': DARBAS_ILGAS,
        'veiklos': ['detailing', 'plovykla'],
        'su_skelbimais': False,
        'paslaugos': [
            ('Kėbulo poliravimas', 'Vieno etapo · lengvasis automobilis', 240, 180),
            ('Keramikinė danga', 'Su paruošimu · 2 metų garantija', 480, 450),
            ('Salono cheminis valymas', 'Sėdynės, kilimėliai, apdaila', 180, 120),
            ('Kvapo šalinimas ozonu', 'Salonas ir ventiliacija', 60, 40),
        ],
    },
]


class Command(BaseCommand):
    help = 'Sukuria (arba pašalina) bandomąsias įmones'

    def add_arguments(self, parser):
        parser.add_argument('--pasalinti', action='store_true',
                            help='pašalina visas testines įmones')

    def handle(self, *args, **o):
        if o['pasalinti']:
            kiek = Imone.objects.filter(testine=True).count()
            Imone.objects.filter(testine=True).delete()
            self.stdout.write(self.style.SUCCESS(f'Pašalinta testinių įmonių: {kiek}'))
            return

        savininkas = self._savininkas_su_skelbimais()
        for aprasas in IMONES:
            self._viena(aprasas, savininkas)

        self.stdout.write('')
        for i in Imone.objects.filter(testine=True).order_by('tipas', 'pavadinimas'):
            self.stdout.write(f'  {i.get_tipas_display():13} {i.pavadinimas:26} '
                              f'{i.miestas:9} /imone/{i.slug}/')
        self.stdout.write(self.style.SUCCESS(
            '\nPašalinti: manage.py imones_testines --pasalinti'))

    @staticmethod
    def _savininkas_su_skelbimais():
        """Paskyra, kuri JAU turi skelbimų — jų savininko nekeičiam."""
        from django.db.models import Count
        from apps.listings.views import _public_listings_qs
        eil = (_public_listings_qs(None).values('seller_id')
               .annotate(n=Count('id')).order_by('-n').first())
        if not eil:
            return None
        from django.contrib.auth import get_user_model
        return get_user_model().objects.filter(pk=eil['seller_id']).first()

    def _viena(self, a, savininkas):
        with transaction.atomic():
            imone, nauja = Imone.objects.get_or_create(
                slug=a['raktas'],
                defaults={'pavadinimas': a['pavadinimas'], 'tipas': a['tipas']})
            imone.tipas = a['tipas']
            imone.pavadinimas = a['pavadinimas']
            imone.aprasymas = a['aprasymas']
            imone.adresas = a['adresas']
            imone.miestas = a['miestas']
            imone.salis = 'LT'
            imone.latitude = a['lat']
            imone.longitude = a['lng']
            imone.telefonas = a['telefonas']
            imone.el_pastas = a['el_pastas']
            imone.svetaine = a['svetaine']
            imone.darbo_laikas = a['darbo_laikas']
            imone.savininkas = savininkas if a['su_skelbimais'] else None
            imone.patvirtinta = True
            imone.testine = True
            imone.save()

            imone.veiklos.set(VeiklosSritis.objects.filter(slug__in=a['veiklos']))
            imone.paslaugos.all().delete()
            for i, (pav, apie, trukme, kaina) in enumerate(a['paslaugos']):
                ImonesPaslauga.objects.create(
                    imone=imone, pavadinimas=pav, aprasymas=apie,
                    trukme_min=trukme, kaina=kaina, tvarka=i)
        self.stdout.write(('sukurta ' if nauja else 'atnaujinta ') + imone.pavadinimas)
