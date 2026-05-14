"""
Užseed'ina Moto Gear gamintojus (brands).
Sąrašas iš autoplius.lt + papildomi gerai žinomi gamintojai.
'Other' visada pirma opcija (order=-1).

Naudojimas:
    python manage.py seed_gear_brands
    python manage.py seed_gear_brands --clean
"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from apps.listings.models import GearBrand


GEAR_BRANDS = [
    "Acerbis", "AGV", "Airoh", "Akito", "Alpinestars", "Arai", "Arlen Ness",
    "ARMR", "AXO", "Bates", "Bell", "Belstaff", "Berik", "Bering", "Bieffe",
    "Biltwell", "Blauer", "Blytz", "BMW", "Bolle", "Box", "BROGER", "Brubeck",
    "Bullson", "BY CITY", "Büse", "Caberg", "Can-Am", "Centurion", "CGM",
    "CKX", "Connelly", "Cortech", "Cycle Spirit", "Dainese", "Daytona",
    "Diadora", "Diesel", "DMD", "Dr. Martens", "Dragon", "Drift", "Drudi",
    "Ducati", "Duchinni", "EKS Brand", "Evs", "Falco", "Fieldsheer", "Firefox",
    "Five", "FLM", "Fly", "Fm", "Forcefield", "Forma", "Fox", "Frank Thomas",
    "Furygan", "G-Mac", "Gaerne", "Gerbing", "Germot", "Givi", "Grex",
    "Halvarssons", "Harley-Davidson", "Harro", "Hebo", "Hein Gericke", "Held",
    "Helix", "Highway 1", "HJC", "Honda", "Husqvarna", "Icon", "IMS", "INDIAN",
    "IXON", "IXS", "Jofama", "John Doe", "Kappa", "Kawasaki", "KENNY", "Klim",
    "Knox", "Kochmann", "Komine", "KTM", "KYT", "Lazer", "Leatt", "Lemans",
    "Levior", "Lindstrands", "LS2", "Macna", "Madhead", "Marushin", "MDS",
    "Merlin", "Modeka", "MoMo Design", "Mondial", "Moose Racing", "Motul",
    "MT Helmets", "Naki", "NEXO", "Nexx", "Nikko", "Nitro", "NoEnd", "Nolan",
    "Nuvo", "NZI", "O'Neal", "Oakley", "Off Road", "One Industries", "Original",
    "Oxford", "Oxtar", "Ozone", "Pando Moto", "Polo", "Premier", "Probiker",
    "Puig", "PUMA", "Raberg", "Race-Inn", "Racer", "Rayven", "Rebelhorn",
    "Red Bull", "Reevu", "REITER", "Rev'It", "Richa", "Riding Culture", "Rjays",
    "Roadsign", "Rocc", "Rocket", "Roeg", "Rokker", "Roleff", "Roof", "Rosso",
    "Royal Enfield", "RS Taichi", "RST", "Rukka", "Saber", "Safe-max",
    "Schampa", "Schuberth", "Schwabenleder", "Scorpion", "Scott", "Sedici",
    "Segura", "Shad", "Shark", "Shift", "Shima", "Shiro", "Shoei", "Shoo",
    "Shot", "Shox", "Sidi", "Sigma", "Simpson", "SixSixOne", "Smith", "SMK",
    "Snell", "SPADA", "Spidi", "Spyke", "Stadler", "Stormer", "Stylmartin",
    "Suomy", "Suzuki", "Swift", "Takachi", "TCX", "Tech Air", "Teknic", "Thor",
    "TMS", "Tour Master", "Triumph", "Tschul", "TSG", "Tucano Urbano", "Tuzo",
    "UFO", "Uvex", "V Quattro", "Vanson", "Vanucci", "Vega", "VEMAR", "Venice",
    "VENO", "Vespa", "Vicma", "VITO", "Voigt", "VR46", "W2", "Weise", "Wiley X",
    "Wintex", "WINX", "Worker", "Wulfsport", "X-Lite", "Xelement", "XPD",
    "Yamaha", "YOSHIMURA", "Zandona",
]


class Command(BaseCommand):
    help = 'Seeds GearBrand table (autoplius-style 229 brands + Other first)'

    def add_arguments(self, parser):
        parser.add_argument('--clean', action='store_true')

    def handle(self, *args, **options):
        if options['clean']:
            count = GearBrand.objects.count()
            GearBrand.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'Deleted {count} existing brands.'))

        # 'Other' first (order=-1)
        other, _ = GearBrand.objects.get_or_create(
            slug='other',
            defaults={'name': 'Other', 'order': -1},
        )
        if other.order != -1 or other.name != 'Other':
            other.order = -1
            other.name = 'Other'
            other.save(update_fields=['order', 'name'])

        created = 0
        existed = 0
        for idx, name in enumerate(GEAR_BRANDS):
            slug = slugify(name) or f'brand-{idx}'
            order = idx
            obj, was_created = GearBrand.objects.get_or_create(
                slug=slug,
                defaults={'name': name, 'order': order},
            )
            if was_created:
                created += 1
            else:
                existed += 1
                changed = False
                if obj.name != name:
                    obj.name = name
                    changed = True
                if obj.order != order:
                    obj.order = order
                    changed = True
                if changed:
                    obj.save(update_fields=['name', 'order'])

        total = GearBrand.objects.count()
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(
            f'Done. Created: {created}, existed: {existed}, total: {total} (incl. Other)'
        ))