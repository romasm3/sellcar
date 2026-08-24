"""Testiniai skelbimai — po vieną kiekvienai kategorijai ir sekcijai.

    manage.py testiniai_skelbimai            # sukuria trūkstamus
    manage.py testiniai_skelbimai --sarasas  # tik parodo, ką turi
    manage.py testiniai_skelbimai --trinti   # pašalina (klausia patvirtinimo)

Visi pažymėti trimis būdais, kad vėliau būtų lengva rasti:
  · aprašymas prasideda „TESTINIS SKELBIMAS"
  · savininkas — paskyra testai@example.com
  · pavadinime priesaga „[TEST]"
"""

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone

ZYMA = 'TESTINIS SKELBIMAS'
TEST_EMAIL = 'testai@example.com'

# (vehicle_type slug, sekcijos raktas|None, pavadinimas, metai, kaina, miestas, papildomi laukai)
SPEC = [
    ('cars',              None,   'BMW 320d Touring',                2018, 15900, 'Vilnius',   {}),
    ('motorcycles',       None,   'Honda CB500F',                    2020,  5200, 'Kaunas',    {}),
    ('trucks',            'main', 'MAN TGX 18.480',                  2016, 32000, 'Klaipėda',  {}),
    ('trucks',            'buses', 'Mercedes-Benz Sprinter 519',     2019, 41000, 'Šiauliai',  {}),
    ('trailers',          None,   'Schmitz Cargobull SKO 24',        2015, 12500, 'Panevėžys', {}),
    ('boats',             None,   'Bayliner VR5 Bowrider',           2021, 28900, 'Neringa',   {}),
    ('agriculture',       None,   'John Deere 6155M',                2017, 78000, 'Marijampolė', {}),
    ('construction',      None,   'JCB 3CX Sitemaster',              2014, 34500, 'Alytus',    {}),
    ('forestry',          None,   'Ponsse Beaver',                   2013, 96000, 'Utena',     {}),
    ('loading-equipment', None,   'Linde H25 krautuvas',             2018, 15400, 'Kėdainiai', {}),
    ('camping-houses',    None,   'Hobby De Luxe 460',               2019, 18700, 'Palanga',   {}),
    ('electronics',       None,   'Pioneer AVH-Z5200DAB',            2022,   320, 'Vilnius',   {}),
    ('bicycles',          None,   'Xiaomi Mi Scooter Pro 2',         2023,   380, 'Kaunas',    {}),
    ('services',          None,   'Automobilių supirkimas visoje LT',2024,     0, 'Vilnius',   {'service_type': 'car_buying'}),
    ('parts',             None,   'BMW E90 priekinis žibintas',      2010,   120, 'Vilnius',   {}),
    ('rental',            None,   'Škoda Octavia nuoma parai',       2021,    39, 'Vilnius',   {}),
]


class Command(BaseCommand):
    help = 'Sukuria po vieną testinį skelbimą kiekvienoje kategorijoje.'

    def add_arguments(self, parser):
        parser.add_argument('--sarasas', action='store_true')
        parser.add_argument('--trinti', action='store_true')

    def handle(self, *args, **o):
        from apps.listings.models import Listing, ListingImage, VehicleType

        User = get_user_model()
        qs = Listing.objects.filter(description__startswith=ZYMA)

        if o['sarasas'] or o['trinti']:
            self.stdout.write(f'Testinių skelbimų: {qs.count()}')
            for l in qs.order_by('vehicle_type__slug'):
                self.stdout.write(f'  {l.vehicle_type.slug:20} #{l.pk:<5} {l.title[:40]:42} /{l.pk}/')
            if o['trinti']:
                self.stdout.write(self.style.WARNING(
                    'Trynimas per šią komandą neatliekamas — pašalinkite admin\'e '
                    'arba paleiskite Listing.objects.filter(description__startswith=…).delete() rankiniu būdu.'))
            return

        seller, created = User.objects.get_or_create(
            email=TEST_EMAIL, defaults={'username': 'testai', 'is_active': False})
        if created:
            seller.set_unusable_password(); seller.save()
            self.stdout.write(f'Sukurta testinė paskyra {TEST_EMAIL}')

        from PIL import Image
        import io

        sukurta, praleista = [], []
        for slug, sek, title, year, price, city, extra in SPEC:
            vt = VehicleType.objects.filter(slug=slug).first()
            if not vt:
                praleista.append((slug, 'nėra tokios kategorijos')); continue
            if Listing.objects.filter(vehicle_type=vt, description__startswith=ZYMA,
                                      title__startswith=title[:12]).exists():
                praleista.append((slug, 'jau yra')); continue

            l = Listing(
                seller=seller, vehicle_type=vt, title=f'{title} [TEST]',
                description=f'{ZYMA}. Sukurtas apžiūrai — realių duomenų neatitinka.',
                year=year, price=price, city=city, country='LT',
                mileage=0, status='active', **extra)
            l.save()

            # paprastas spalvotas paveikslėlis, kad kortelė nebūtų tuščia
            buf = io.BytesIO()
            spalva = (60 + (hash(slug) % 150), 90, 140)
            Image.new('RGB', (1600, 1200), spalva).save(buf, 'JPEG', quality=80)
            img = ListingImage(listing=l)
            img.image.save(f'test-{slug}.jpg', ContentFile(buf.getvalue()), save=True)

            sukurta.append((slug, l.pk, l.title))

        self.stdout.write('')
        self.stdout.write(f"{'kategorija':22} {'ID':>6}  nuoroda")
        for slug, pk, title in sukurta:
            self.stdout.write(f'{slug:22} {pk:>6}  /{pk}/   {title}')
        for slug, kodel in praleista:
            self.stdout.write(self.style.WARNING(f'{slug:22} praleista — {kodel}'))
        self.stdout.write(self.style.SUCCESS(f'\nSukurta: {len(sukurta)}, praleista: {len(praleista)}'))
