# -*- coding: utf-8 -*-
"""
Pilni bandomieji įmonių duomenys — kad matytųsi tikras vaizdas.

    manage.py imones_testines              # sukuria arba atnaujina
    manage.py imones_testines --pasalinti  # pašalina TIK testines

Trys servisai (padangos, detailing, bendras remontas) su 5–6 paslaugomis
ir du prekiautojai. Visiems: logotipas, 5 nuotraukos, aprašymas, pilnas
darbo laikas (šeštadienis trumpesnis, sekmadienis nedirba) ir tikros
koordinatės Kaune bei Vilniuje.

Visos pažymėtos `testine=True`, todėl matomos admin filtre „Testinė" ir
pašalinamos viena komanda. Tikrų įmonių ši komanda neliečia.

Prekiautojai rišami prie JAU esamų paskyrų, kurios turi skelbimų —
skelbimų savininkų nekeičiam, todėl niekas realiai nepersirašo.
"""

import io

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.imones.models import Imone, ImonesNuotrauka, ImonesPaslauga, VeiklosSritis


def _darbas(sesta=('09:00', '14:00'), nuo='08:00', iki='18:00'):
    d = {str(x): [nuo, iki] for x in range(5)}
    d['5'] = list(sesta) if sesta else None
    d['6'] = None                      # sekmadienį nedirba
    return d


IMONES = [
    {
        'veikia_nuo': 2011, 'raktas': 'test-padangos', 'tipas': Imone.SERVISAS,
        'pavadinimas': 'Ratų Servisas',
        'aprasymas': 'Padangų montavimas ir remontas, ratų balansavimas bei '
                     'geometrijos reguliavimas. Dirbame su lengvaisiais '
                     'automobiliais ir mikroautobusais. Sezono metu '
                     'rekomenduojame registruotis iš anksto.',
        'adresas': 'Taikos pr. 88', 'miestas': 'Kaunas',
        'lat': 54.88374, 'lng': 23.94208,
        'telefonas': '+370 612 34567', 'el_pastas': 'demo.padangos@example.com',
        'svetaine': 'https://example.com/ratu-servisas',
        'darbo_laikas': _darbas(),
        'veiklos': ['padangu-montavimas', 'remontas'],
        'spalva': (0x37, 0x41, 0x51),
        'paslaugos': [
            ('Padangų montavimas — R13–R15', '4 ratai', 40, 30),
            ('Padangų montavimas — R16–R17', '4 ratai', 45, 38),
            ('Padangų montavimas — R18–R19', '4 ratai', 50, 44),
            ('Ratų balansavimas', '1 ratas', 10, 6),
            ('Geometrijos reguliavimas', 'Lengvasis automobilis', 60, 45),
            ('Padangų sandėliavimas', 'Sezonui · 4 ratai', None, 25),
        ],
    },
    {
        'veikia_nuo': 2018, 'raktas': 'test-detailing', 'tipas': Imone.SERVISAS,
        'pavadinimas': 'Blizgus Auto',
        'aprasymas': 'Kėbulo poliravimas, keraminės ir plėvelinės dangos, '
                     'salono cheminis valymas. Dirbame uždarose patalpose su '
                     'kontroliuojamu apšvietimu. Automobilį galima palikti '
                     'visai dienai.',
        'adresas': 'Savanorių pr. 174', 'miestas': 'Vilnius',
        'lat': 54.66892, 'lng': 25.23452,
        'telefonas': '+370 655 90210', 'el_pastas': 'demo.detailing@example.com',
        'svetaine': 'https://example.com/blizgus-auto',
        'darbo_laikas': _darbas(sesta=('10:00', '16:00'), iki='20:00'),
        'veiklos': ['detailing', 'autoplovykla'],
        'spalva': (0x1F, 0x29, 0x37),
        'paslaugos': [
            ('Kėbulo poliravimas — vienas etapas', 'Lengvasis automobilis', 240, 180),
            ('Kėbulo poliravimas — du etapai', 'Su gilių įbrėžimų šalinimu', 420, 320),
            ('Keramikinė danga', 'Su paruošimu · 2 metų garantija', 480, 450),
            ('Salono cheminis valymas', 'Sėdynės, kilimėliai, apdaila', 180, 120),
            ('Kvapo šalinimas ozonu', 'Salonas ir ventiliacija', 60, 40),
            ('Žibintų poliravimas', 'Pora', 45, 35),
        ],
    },
    {
        'veikia_nuo': 2004, 'raktas': 'test-remontas', 'tipas': Imone.SERVISAS,
        'pavadinimas': 'Auto Meistrai',
        'aprasymas': 'Bendras automobilių remontas: variklio ir važiuoklės '
                     'darbai, stabdžiai, diagnostika. Dirbame su visomis '
                     'markėmis, detales užsakome patys. Diagnostika '
                     'įskaičiuojama į remonto kainą.',
        'adresas': 'Europos pr. 122', 'miestas': 'Kaunas',
        'lat': 54.92677, 'lng': 23.88394,
        'telefonas': '+370 698 45312', 'el_pastas': 'demo.remontas@example.com',
        'svetaine': '',
        'darbo_laikas': _darbas(sesta=('09:00', '13:00'), iki='19:00'),
        'veiklos': ['remontas', 'elektronika-diagnostika', 'technine-apziura'],
        'spalva': (0x4B, 0x55, 0x63),
        'paslaugos': [
            ('Kompiuterinė diagnostika', 'Visos sistemos · su ataskaita', 45, 30),
            ('Tepalų ir filtrų keitimas', 'Be medžiagų kainos', 60, 35),
            ('Stabdžių kaladėlių keitimas', 'Viena ašis', 90, 55),
            ('Važiuoklės patikra', 'Su pakėlimu ir ataskaita', 40, 25),
            ('Paskirstymo diržo keitimas', 'Priklauso nuo variklio', 300, 220),
            ('Pasiruošimas techninei apžiūrai', 'Patikra ir smulkūs darbai', 60, 40),
        ],
    },
    {
        'veikia_nuo': 2009, 'raktas': 'test-prekiautojas', 'tipas': Imone.PREKIAUTOJAS,
        'pavadinimas': 'MIKAUTA',
        'aprasymas': 'Naudoti automobiliai iš Vokietijos ir Skandinavijos. '
                     'Visi automobiliai patikrinti, su servisų istorija. '
                     'Priimame seną automobilį kaip dalį apmokėjimo.',
        'adresas': 'Chemijos g. 12', 'miestas': 'Kaunas',
        'lat': 54.91162, 'lng': 23.97197,
        'telefonas': '+370 600 11122', 'el_pastas': 'demo.prekyba@example.com',
        'svetaine': 'https://example.com/mikauta',
        'darbo_laikas': _darbas(),
        'veiklos': ['automobiliu-prekyba', 'automobiliu-supirkimas'],
        'spalva': (0xE1, 0x4D, 0x28),
        'savininkas_nr': 0,
        'paslaugos': [],
    },
    {
        'veikia_nuo': 2021, 'raktas': 'test-prekiautojas-2', 'tipas': Imone.PREKIAUTOJAS,
        'pavadinimas': 'Auto Bravo',
        'aprasymas': 'Automobilių prekyba ir supirkimas Vilniuje. Perkame '
                     'automobilius su defektais ir be techninės apžiūros. '
                     'Atsiskaitome iš karto.',
        'adresas': 'Ukmergės g. 280', 'miestas': 'Vilnius',
        'lat': 54.73411, 'lng': 25.24019,
        'telefonas': '+370 611 33444', 'el_pastas': 'demo.bravo@example.com',
        'svetaine': '',
        'darbo_laikas': _darbas(sesta=('10:00', '15:00')),
        'veiklos': ['automobiliu-prekyba', 'automobiliu-supirkimas', 'evakuatorius'],
        'spalva': (0x06, 0x76, 0x47),
        'savininkas_nr': 1,
        'paslaugos': [],
    },
]


class Command(BaseCommand):
    help = 'Sukuria (arba pašalina) pilnus bandomuosius įmonių duomenis'

    def add_arguments(self, parser):
        parser.add_argument('--pasalinti', action='store_true')

    def handle(self, *args, **o):
        if o['pasalinti']:
            kiek = Imone.objects.filter(testine=True).count()
            Imone.objects.filter(testine=True).delete()
            self.stdout.write(self.style.SUCCESS(
                f'Pašalinta testinių įmonių: {kiek}'))
            return

        savininkai = self._savininkai()
        for a in IMONES:
            self._viena(a, savininkai)

        self.stdout.write('')
        for i in Imone.objects.filter(testine=True).order_by('tipas', 'pavadinimas'):
            self.stdout.write(f'  {i.get_tipas_display():13} {i.pavadinimas:16} '
                              f'{i.miestas:9} /imone/{i.slug}/')
        self.stdout.write(self.style.SUCCESS(
            '\nPašalinti: manage.py imones_testines --pasalinti'))

    # ── pagalbinės ──────────────────────────────────────────────────
    @staticmethod
    def _savininkai():
        """Paskyros, kurios JAU turi skelbimų — jų savininkų nekeičiam."""
        from django.contrib.auth import get_user_model
        from django.db.models import Count
        from apps.listings.views import _public_listings_qs
        eil = (_public_listings_qs(None).values('seller_id')
               .annotate(n=Count('id')).order_by('-n')[:2])
        U = get_user_model()
        return [U.objects.filter(pk=e['seller_id']).first() for e in eil]

    @staticmethod
    def _piesinys(tekstas, spalva, plotis, aukstis, logotipas=False):
        """Paprastas vietos rezervavimo paveikslėlis (Pillow)."""
        from PIL import Image, ImageDraw
        img = Image.new('RGB', (plotis, aukstis), spalva)
        p = ImageDraw.Draw(img)
        if logotipas:
            p.ellipse([plotis * .12, aukstis * .12, plotis * .88, aukstis * .88],
                      fill=(255, 255, 255))
            p.text((plotis / 2 - 12, aukstis / 2 - 8), tekstas[:2].upper(),
                   fill=spalva)
        else:
            # švelnus dryžis, kad nuotraukos skirtųsi viena nuo kitos
            for i in range(0, plotis, 40):
                p.line([(i, 0), (i - aukstis, aukstis)],
                       fill=tuple(min(255, c + 18) for c in spalva), width=14)
            p.text((16, aukstis - 26), tekstas, fill=(255, 255, 255))
        buferis = io.BytesIO()
        img.save(buferis, format='JPEG', quality=80)
        return ContentFile(buferis.getvalue())

    @staticmethod
    def _nuotraukos(kiek):
        """Tikros nuotraukos — pasiskolintos iš jau įkeltų skelbimų.

        Piešti dryžius nebeverta: bandomosios įmonės turi atrodyti kaip
        tikros. Failai kopijuojami, originalūs skelbimai nepaliečiami.
        """
        from apps.listings.models import ListingImage

        eilutes = (ListingImage.objects.exclude(image='')
                   .order_by('?')[:kiek])
        isvestis = []
        for e in eilutes:
            try:
                e.image.open('rb')
                isvestis.append(ContentFile(e.image.read()))
                e.image.close()
            except Exception:
                continue
        return isvestis

    def _viena(self, a, savininkai):
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
            imone.veikia_nuo = a.get('veikia_nuo')
            nr = a.get('savininkas_nr')
            imone.savininkas = (savininkai[nr] if nr is not None
                                and nr < len(savininkai) else None)
            imone.patvirtinta = True
            imone.testine = True
            if not imone.logotipas:
                imone.logotipas.save(
                    f"{a['raktas']}-logo.jpg",
                    self._piesinys(a['pavadinimas'], a['spalva'], 200, 200, True),
                    save=False)
            imone.save()

            imone.veiklos.set(VeiklosSritis.objects.filter(slug__in=a['veiklos']))

            imone.paslaugos.all().delete()
            for i, (pav, apie, trukme, kaina) in enumerate(a['paslaugos']):
                ImonesPaslauga.objects.create(
                    imone=imone, pavadinimas=pav, aprasymas=apie,
                    trukme_min=trukme, kaina=kaina, tvarka=i)

            if imone.nuotraukos.count() < 5:
                imone.nuotraukos.all().delete()
                for i, failas in enumerate(self._nuotraukos(5)):
                    n = ImonesNuotrauka(imone=imone, tvarka=i)
                    n.nuotrauka.save(f"{a['raktas']}-{i + 1}.jpg", failas, save=False)
                    n.save()
        self.stdout.write(('sukurta ' if nauja else 'atnaujinta ') + imone.pavadinimas)
