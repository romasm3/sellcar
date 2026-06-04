"""
Management command: seed_fake_listings

Vieta:
    listings/management/commands/seed_fake_listings.py

Paleisti:
    python manage.py seed_fake_listings              # 10 mix (5 cars + 3 moto + 2 trucks)
    python manage.py seed_fake_listings --count 20
    python manage.py seed_fake_listings --no-images  # be paveikslėlių (greičiau)
    python manage.py seed_fake_listings --delete     # ištrina visus seed'intus

PASTABA: Title nebėra "[FAKE_SEED]" prefix. Seed listing'ai pažymimi
nematomu HTML komentaru description pabaigoje, todėl atrodo kaip tikri
skelbimai, bet --delete vis tiek randa ir ištrina tik juos.
"""

import random
from decimal import Decimal
from io import BytesIO

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone

from apps.listings.models import (
    Listing, ListingImage,
    VehicleType, SubCategory,
    Brand, Model as CarModel,
    MotorcycleBrand, MotorcycleModel,
    TruckBrand, TruckModel,
    Truck, TruckImage,
    FuelType, Transmission,
)

# Nematomas žymeklis HTML komentare description'o pabaigoje (delete'ui)
SEED_MARKER = "__SEEDED_FAKE__"


# ============ KAINŲ GENERATORIAI (realistiškos) ============

def realistic_car_price():
    """Realios automobilių kainos: $2,900-$48,900."""
    endings = [
        0, 100, 200, 300, 400, 500, 600, 700, 800, 900,
        500, 500, 900, 900, 900, 950, 990, 990,  # dažniau
    ]
    thousands = random.randint(2, 48)
    ending = random.choice(endings)
    return Decimal(thousands * 1000 + ending)


def realistic_moto_price():
    """Motociklų kainos: $1,500-$24,900."""
    endings = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900,
               500, 900, 950, 990]
    thousands = random.randint(1, 24)
    ending = random.choice(endings)
    return Decimal(thousands * 1000 + ending)


def realistic_truck_price():
    """Sunkvežimių kainos: $14,500-$125,000."""
    endings = [0, 500, 900, 500, 900, 950]
    thousands = random.randint(14, 125)
    ending = random.choice(endings)
    return Decimal(thousands * 1000 + ending)


# ============ DUOMENŲ POOL'AI ============

CAR_BODY_TYPES = ['sedan', 'hatchback', 'estate', 'suv', 'coupe', 'pickup']
CAR_COLORS = ['black', 'white', 'red', 'blue', 'green_khaki', 'brown_beige']
CAR_CONDITIONS = ['used', 'used', 'used', 'new']  # 75% used
CAR_DRIVE_TYPES = ['fwd', 'rwd', 'awd']
CAR_DOORS = ['2/3', '4/5']
CAR_STEERING = ['left', 'left', 'left', 'right']  # mostly LHD
CAR_EURO = ['euro4', 'euro5', 'euro6', 'euro6d']
CAR_CLIMATE = ['ac', 'climate', 'dual_climate']

MOTO_TYPES = ['sport', 'cruiser', 'touring', 'naked', 'enduro', 'scooter']
MOTO_COOLING = ['air', 'water', 'oil']
MOTO_ENGINE_TYPES = ['single', 'twin', 'parallel_twin', 'v_twin', 'inline_4']

TRUCK_TYPES = ['flatbed', 'tippers', 'curtain_side', 'refrigerators',
               'container_carriers', 'with_crane', 'tankers']
TRUCK_CAB_TYPES = ['day', 'sleeper', 'crew']
TRUCK_AXLE = ['4x2', '6x2', '6x4', '8x4']
TRUCK_SUSPENSION = ['air_air', 'air_spring', 'spring_spring']
TRUCK_FUEL = ['diesel', 'diesel', 'diesel', 'lng']
TRUCK_TRANS = ['manual', 'automatic', 'semi_automatic']

US_CITIES = [
    ('New York', 'NY'), ('Los Angeles', 'CA'), ('Chicago', 'IL'),
    ('Houston', 'TX'), ('Phoenix', 'AZ'), ('Philadelphia', 'PA'),
    ('San Antonio', 'TX'), ('San Diego', 'CA'), ('Dallas', 'TX'),
    ('Miami', 'FL'), ('Seattle', 'WA'), ('Denver', 'CO'),
    ('Atlanta', 'GA'), ('Boston', 'MA'), ('Portland', 'OR'),
]


class Command(BaseCommand):
    help = "Generates fake listings (cars + motorcycles + trucks) for testing"

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=10,
                            help='Total number of listings (default: 10)')
        parser.add_argument('--delete', action='store_true',
                            help='Delete all previously seeded fake listings')
        parser.add_argument('--no-images', action='store_true',
                            help='Skip image generation (much faster)')

    def handle(self, *args, **options):
        if options['delete']:
            self._delete_seeds()
            return

        self.skip_images = options['no_images']
        self._create_seeds(options['count'])

    # ============ DELETE ============

    def _delete_seeds(self):
        # Trinam pagal description marker'į (title nebeturi prefix'o)
        listings_qs = Listing.objects.filter(description__contains=SEED_MARKER)
        trucks_qs = Truck.objects.filter(description__contains=SEED_MARKER)

        n_listings = listings_qs.count()
        n_trucks = trucks_qs.count()

        listings_qs.delete()
        trucks_qs.delete()

        self.stdout.write(self.style.SUCCESS(
            f"Ištrinta: {n_listings} listings + {n_trucks} trucks"
        ))

    # ============ CREATE ============

    def _create_seeds(self, count):
        user = User.objects.filter(is_superuser=True).first() or User.objects.first()
        if not user:
            self.stdout.write(self.style.ERROR("Nėra nei vieno user'io DB!"))
            return
        self.stdout.write(f"Seller: {user.username} ({user.email})")

        vt_cars = VehicleType.objects.filter(slug='cars').first()
        vt_moto = VehicleType.objects.filter(slug='motorcycles').first()
        vt_trucks = VehicleType.objects.filter(slug='trucks').first()

        if not vt_cars or not vt_moto:
            self.stdout.write(self.style.ERROR(
                "Nėra VehicleType įrašų (cars/motorcycles). Sukurk admin'e pirma!"
            ))
            return

        n_cars = max(1, count // 2)
        n_moto = max(1, (count * 3) // 10)
        n_trucks = max(0, count - n_cars - n_moto)

        created = 0

        self.stdout.write(self.style.WARNING(f"\n→ Generuoju {n_cars} cars..."))
        for i in range(n_cars):
            if self._create_car(user, vt_cars, i):
                created += 1

        self.stdout.write(self.style.WARNING(f"\n→ Generuoju {n_moto} motorcycles..."))
        for i in range(n_moto):
            if self._create_motorcycle(user, vt_moto, i):
                created += 1

        if n_trucks > 0:
            self.stdout.write(self.style.WARNING(f"\n→ Generuoju {n_trucks} trucks..."))
            for i in range(n_trucks):
                if self._create_truck(user, i):
                    created += 1

        self.stdout.write(self.style.SUCCESS(
            f"\n✓ Sukurta {created}/{count} fake skelbimų"
        ))
        self.stdout.write(self.style.WARNING(
            f"Trinti: python manage.py seed_fake_listings --delete"
        ))

    # ============ CAR ============

    def _create_car(self, user, vehicle_type, idx):
        brand = Brand.objects.filter(vehicle_type=vehicle_type).order_by('?').first()
        if not brand:
            brand = Brand.objects.order_by('?').first()
        if not brand:
            self.stdout.write(self.style.ERROR("  ✗ Nėra Brand DB"))
            return False

        model = CarModel.objects.filter(brand=brand).order_by('?').first()
        if not model:
            self.stdout.write(self.style.WARNING(f"  ⚠ {brand.name} neturi modelių, praleidžiu"))
            return False

        year = random.randint(2005, 2024)
        mileage_km = round(random.randint(20_000, 280_000), -3)
        price = realistic_car_price()
        city, state = random.choice(US_CITIES)

        fuel = FuelType.objects.order_by('?').first()
        trans = Transmission.objects.order_by('?').first()

        subcategory = SubCategory.objects.filter(
            vehicle_type=vehicle_type, slug='cars',
        ).first()

        listing = Listing.objects.create(
            seller=user,
            vehicle_type=vehicle_type,
            subcategory=subcategory,
            brand=brand,
            model=model,
            title=f"{brand.name} {model.name} {year}",
            description=self._car_description(brand.name, model.name, year),
            year=year,
            mileage=mileage_km,
            fuel_type=fuel,
            transmission=trans,
            body_type=random.choice(CAR_BODY_TYPES),
            engine_capacity=Decimal(str(round(random.uniform(1.0, 5.0), 1))),
            power=random.randint(70, 350),
            color=random.choice(CAR_COLORS),
            doors=random.choice(CAR_DOORS),
            condition=random.choice(CAR_CONDITIONS),
            steering=random.choice(CAR_STEERING),
            drive_type=random.choice(CAR_DRIVE_TYPES),
            seats=random.choice(['2', '4', '5', '7']),
            euro_standard=random.choice(CAR_EURO),
            climate=random.choice(CAR_CLIMATE),
            price=price,
            currency='USD',
            negotiable=random.choice([True, False]),
            has_service_book=random.choice([True, False]),
            valid_inspection=random.choice([True, False]),
            country='US',
            state=state,
            city=city,
            status='active',
            activated_at=timezone.now(),
            expires_at=timezone.now() + timezone.timedelta(days=30),
        )
        self._attach_image(listing, ListingImage, 'listing', 'car', idx)
        self.stdout.write(f"  ✓ Car: {listing.title} (${price})")
        return True

    # ============ MOTORCYCLE ============

    def _create_motorcycle(self, user, vehicle_type, idx):
        brand = MotorcycleBrand.objects.order_by('?').first()
        if not brand:
            self.stdout.write(self.style.ERROR("  ✗ Nėra MotorcycleBrand DB"))
            return False

        model = MotorcycleModel.objects.filter(brand=brand).order_by('?').first()
        if not model:
            self.stdout.write(self.style.WARNING(f"  ⚠ {brand.name} neturi modelių"))
            return False

        year = random.randint(2010, 2024)
        mileage_km = round(random.randint(1_000, 80_000), -3)
        price = realistic_moto_price()
        city, state = random.choice(US_CITIES)

        subcategory = SubCategory.objects.filter(
            vehicle_type=vehicle_type, slug='motorcycles',
        ).first()
        if not subcategory:
            subcategory = SubCategory.objects.filter(vehicle_type=vehicle_type).first()

        listing = Listing.objects.create(
            seller=user,
            vehicle_type=vehicle_type,
            subcategory=subcategory,
            motorcycle_brand=brand,
            motorcycle_model=model,
            title=f"{brand.name} {model.name} {year}",
            description=self._moto_description(brand.name, model.name, year),
            year=year,
            mileage=mileage_km,
            motorcycle_type=random.choice(MOTO_TYPES),
            cooling_type=random.choice(MOTO_COOLING),
            moto_engine_type=random.choice(MOTO_ENGINE_TYPES),
            engine_capacity_cc=random.choice([125, 250, 600, 750, 1000, 1200]),
            color=random.choice(CAR_COLORS),
            condition='used',
            price=price,
            currency='USD',
            country='US',
            state=state,
            city=city,
            status='active',
            activated_at=timezone.now(),
            expires_at=timezone.now() + timezone.timedelta(days=30),
        )
        self._attach_image(listing, ListingImage, 'listing', 'moto', idx)
        self.stdout.write(f"  ✓ Moto: {listing.title} (${price})")
        return True

    # ============ TRUCK ============

    def _create_truck(self, user, idx):
        brand = TruckBrand.objects.order_by('?').first()
        if not brand:
            self.stdout.write(self.style.ERROR("  ✗ Nėra TruckBrand DB"))
            return False

        model = TruckModel.objects.filter(brand=brand).order_by('?').first()
        if not model:
            self.stdout.write(self.style.WARNING(f"  ⚠ {brand.name} neturi modelių"))
            return False

        year = random.randint(2008, 2024)
        mileage_km = round(random.randint(100_000, 900_000), -3)
        price = realistic_truck_price()
        city, state = random.choice(US_CITIES)
        power_kw = random.randint(220, 450)

        truck = Truck.objects.create(
            seller=user,
            subcategory='trucks',
            brand=brand,
            model=model,
            title=f"{brand.name} {model.name} {year}",
            description=self._truck_description(brand.name, model.name, year),
            year=year,
            mileage=mileage_km,
            truck_type=random.choice(TRUCK_TYPES),
            cab_type=random.choice(TRUCK_CAB_TYPES),
            axle_config=random.choice(TRUCK_AXLE),
            suspension=random.choice(TRUCK_SUSPENSION),
            gross_weight=random.randint(7500, 40000),
            payload=random.randint(3000, 25000),
            number_of_seats=random.choice([2, 3]),
            fuel_type=random.choice(TRUCK_FUEL),
            transmission=random.choice(TRUCK_TRANS),
            engine_capacity=Decimal(str(round(random.uniform(6.0, 16.0), 1))),
            power=power_kw,
            power_hp=int(power_kw * 1.341),
            euro_standard=random.choice(['euro5', 'euro6', 'euro6d']),
            color=random.choice(CAR_COLORS),
            condition='used',
            price=price,
            currency='USD',
            country='US',
            state=state,
            city=city,
            status='active',
            activated_at=timezone.now(),
            expires_at=timezone.now() + timezone.timedelta(days=30),
        )
        self._attach_image(truck, TruckImage, 'truck', 'truck', idx)
        self.stdout.write(f"  ✓ Truck: {truck.title} (${price})")
        return True

    # ============ IMAGE ATTACHMENT ============

    def _attach_image(self, obj, ImageModel, relation_field, kind, idx):
        """Generuoja 3 placeholder nuotraukas lokaliai per Pillow."""
        if self.skip_images:
            return

        try:
            from PIL import Image, ImageDraw, ImageFont
        except ImportError:
            self.stdout.write(self.style.WARNING(
                "    ⚠ Pillow nerasta, praleidžiu nuotraukas"
            ))
            return

        bg_colors = {
            'car': [(52, 73, 94), (41, 128, 185), (39, 174, 96),
                    (142, 68, 173), (211, 84, 0)],
            'moto': [(192, 57, 43), (230, 126, 34), (22, 160, 133),
                     (44, 62, 80), (127, 140, 141)],
            'truck': [(44, 62, 80), (52, 73, 94), (149, 165, 166),
                      (127, 140, 141), (44, 62, 80)],
        }
        colors = bg_colors.get(kind, bg_colors['car'])

        title_text = getattr(obj, 'title', f"{kind} #{obj.pk}")
        if len(title_text) > 40:
            title_text = title_text[:37] + "..."

        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
        ]
        font_big = None
        font_small = None
        for fp in font_paths:
            try:
                font_big = ImageFont.truetype(fp, 48)
                font_small = ImageFont.truetype(fp.replace('-Bold', ''), 28)
                break
            except (OSError, IOError):
                continue
        if font_big is None:
            font_big = ImageFont.load_default()
            font_small = ImageFont.load_default()

        try:
            for i in range(3):
                bg = colors[i % len(colors)]
                img = Image.new('RGB', (800, 600), color=bg)
                draw = ImageDraw.Draw(img)

                bbox = draw.textbbox((0, 0), title_text, font=font_big)
                tw = bbox[2] - bbox[0]
                draw.text(
                    ((800 - tw) / 2, 250),
                    title_text,
                    fill=(255, 255, 255),
                    font=font_big,
                )

                photo_label = f"Photo {i + 1} of 3"
                bbox2 = draw.textbbox((0, 0), photo_label, font=font_small)
                tw2 = bbox2[2] - bbox2[0]
                draw.text(
                    ((800 - tw2) / 2, 330),
                    photo_label,
                    fill=(220, 220, 220),
                    font=font_small,
                )

                buf = BytesIO()
                img.save(buf, format='JPEG', quality=85)
                buf.seek(0)

                filename = f"{kind}_{obj.pk}_{idx}_{i}.jpg"
                image_content = ContentFile(buf.getvalue(), name=filename)

                kwargs = {
                    relation_field: obj,
                    'image': image_content,
                    'is_main': (i == 0),
                    'order': i,
                }
                ImageModel.objects.create(**kwargs)
        except Exception as e:
            self.stdout.write(self.style.WARNING(
                f"    ⚠ Image generate failed: {e}"
            ))

    # ============ DESCRIPTIONS (su nematomu marker'iu) ============

    def _car_description(self, brand, model, year):
        return (
            f"Well-maintained {year} {brand} {model}. "
            f"Regular service history, non-smoker owner. "
            f"All electronics working perfectly. New tires installed last year. "
            f"Clean title, no accidents. Available for inspection any day."
            f"\n\n<!-- {SEED_MARKER} -->"
        )

    def _moto_description(self, brand, model, year):
        return (
            f"{year} {brand} {model} in great condition. "
            f"Garage kept, always serviced on time. "
            f"New chain and sprockets installed recently. Ready to ride."
            f"\n\n<!-- {SEED_MARKER} -->"
        )

    def _truck_description(self, brand, model, year):
        return (
            f"{year} {brand} {model} commercial truck. "
            f"DOT inspected, all maintenance records available. "
            f"Reliable workhorse, ready for long hauls. EU-spec."
            f"\n\n<!-- {SEED_MARKER} -->"
        )