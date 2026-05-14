from django.core.management.base import BaseCommand
from django.utils.text import slugify
from apps.listings.models import VehicleType, SubCategory


SUBCATEGORIES = {
    'cars': [
        'Sedan', 'Hatchback', 'Estate / Wagon', 'SUV / Crossover',
        'Coupe', 'Convertible', 'Minivan', 'Pickup', 'Microcar',
    ],
    'vans': [
        'Passenger Minibus', 'Bus', 'Cargo Van up to 3.5t',
        'Cargo Van over 3.5t', 'Camper / Motorhome',
    ],
    'motorcycles': [
        'Motorcycle', 'Moped / Scooter', 'ATV / Quad',
        'Trike', 'Enduro / Motocross', 'Chopper / Cruiser',
    ],
    'trucks': [
        'Semi-Truck / Tractor', 'Truck', 'Tipper',
        'Refrigerator Truck', 'Flatbed Truck', 'Crane Truck', 'Tanker',
    ],
    'agricultural': [
        'Tractor', 'Combine Harvester', 'Sprayer',
        'Baler', 'Plough', 'Cultivator', 'Other Agricultural',
    ],
    'construction': [
        'Excavator', 'Bulldozer', 'Loader', 'Crane',
        'Forklift', 'Concrete Mixer', 'Compactor', 'Other Construction',
    ],
    'boats': [
        'Motorboat', 'Sailboat', 'Yacht', 'Jet Ski',
        'Inflatable Boat', 'Fishing Boat', 'Other Watercraft',
    ],
    'trailers': [
        'Car Trailer', 'Curtainsider Trailer', 'Refrigerator Trailer',
        'Flatbed Trailer', 'Tipper Trailer', 'Boat Trailer', 'Caravan', 'Other Trailer',
    ],
    'buses': [
        'City Bus', 'Coach', 'School Bus', 'Minibus', 'Electric Bus',
    ],
    'suv': [
        'Compact SUV', 'Mid-Size SUV', 'Full-Size SUV', 'Off-Road 4x4', 'Luxury SUV',
    ],
}


class Command(BaseCommand):
    help = 'Import subcategories for all vehicle types'

    def handle(self, *args, **kwargs):
        self.stdout.write('Importing subcategories...')

        for vtype_slug, subcats in SUBCATEGORIES.items():
            try:
                vehicle_type = VehicleType.objects.get(slug=vtype_slug)
            except VehicleType.DoesNotExist:
                self.stdout.write(f'  Skipping "{vtype_slug}" - not found')
                continue

            self.stdout.write(f'  {vehicle_type.name}:')
            for name in subcats:
                slug = slugify(name)
                base_slug = slug
                counter = 1
                while SubCategory.objects.filter(vehicle_type=vehicle_type, slug=slug).exists():
                    slug = f'{base_slug}-{counter}'
                    counter += 1

                obj, created = SubCategory.objects.get_or_create(
                    vehicle_type=vehicle_type,
                    name=name,
                    defaults={'slug': slug}
                )
                if created:
                    self.stdout.write(f'    + {name}')

        self.stdout.write(self.style.SUCCESS('Done! All subcategories imported.'))