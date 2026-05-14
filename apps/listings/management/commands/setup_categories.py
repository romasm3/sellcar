from django.core.management.base import BaseCommand
from apps.listings.models import VehicleType, SubCategory


CATEGORIES = [
    {'name': 'Cars', 'slug': 'cars', 'order': 1, 'subcategories': []},
    {'name': 'Minibuses, Buses & Campers', 'slug': 'vans', 'order': 2, 'subcategories': [
        {'name': 'Passenger Minibuses', 'slug': 'passenger-minibuses'},
        {'name': 'Buses', 'slug': 'buses'},
        {'name': 'Cargo Minibuses up to 3.5t', 'slug': 'cargo-minibuses-up-to-3-5t'},
        {'name': 'Cargo Minibuses over 3.5t', 'slug': 'cargo-minibuses-over-3-5t'},
        {'name': 'Campers', 'slug': 'campers'},
    ]},
    {'name': 'Motorcycles & Moto Gear', 'slug': 'motorcycles', 'order': 3, 'subcategories': [
        {'name': 'Motorcycles', 'slug': 'motorcycles'},
        {'name': 'Mopeds / Scooters', 'slug': 'mopeds-scooters'},
        {'name': 'ATV / Quad', 'slug': 'atv-quad'},
        {'name': 'Enduro / Motocross', 'slug': 'enduro-motocross'},
        {'name': 'Chopper / Cruiser', 'slug': 'chopper-cruiser'},
        {'name': 'Trike', 'slug': 'trike'},
        {'name': 'Moto Gear', 'slug': 'moto-gear'},
    ]},
    {'name': 'Trucks & Commercial', 'slug': 'trucks', 'order': 4, 'subcategories': [
        {'name': 'Semi-Trucks / Tractors', 'slug': 'semi-trucks'},
        {'name': 'Trucks', 'slug': 'trucks'},
        {'name': 'Vans', 'slug': 'vans'},
        {'name': 'Tippers', 'slug': 'tippers'},
        {'name': 'Refrigerator Trucks', 'slug': 'refrigerator-trucks'},
        {'name': 'Tankers', 'slug': 'tankers'},
        {'name': 'Crane Trucks', 'slug': 'crane-trucks'},
        {'name': 'Flatbed Trucks', 'slug': 'flatbed-trucks'},
    ]},
    {'name': 'Parts', 'slug': 'parts', 'order': 5, 'subcategories': [
        {'name': 'Car Parts', 'slug': 'car-parts'},
        {'name': 'Truck Parts', 'slug': 'truck-parts'},
        {'name': 'Moto Parts', 'slug': 'moto-parts'},
    ]},
    {'name': 'Tyres & Wheels', 'slug': 'tires', 'order': 6, 'subcategories': [
        {'name': 'Summer Tyres', 'slug': 'summer-tyres'},
        {'name': 'Winter Tyres', 'slug': 'winter-tyres'},
        {'name': 'All-Season Tyres', 'slug': 'all-season-tyres'},
        {'name': 'Rims', 'slug': 'rims'},
    ]},
    {'name': 'Boats & Water Transport', 'slug': 'boats', 'order': 7, 'subcategories': [
        {'name': 'Boats', 'slug': 'boats'},
        {'name': 'Yachts', 'slug': 'yachts'},
        {'name': 'Motorboats', 'slug': 'motorboats'},
        {'name': 'Sailboats', 'slug': 'sailboats'},
        {'name': 'Jet Skis', 'slug': 'jet-skis'},
        {'name': 'Inflatable Boats', 'slug': 'inflatable-boats'},
        {'name': 'Fishing Boats', 'slug': 'fishing-boats'},
        {'name': 'Other Watercraft', 'slug': 'other-watercraft'},
    ]},
    {'name': 'Trailers & Semi-trailers', 'slug': 'trailers', 'order': 8, 'subcategories': [
        {'name': 'Semi-trailers', 'slug': 'semi-trailers'},
        {'name': 'Car Trailers', 'slug': 'car-trailers'},
        {'name': 'Boat Trailers', 'slug': 'boat-trailers'},
        {'name': 'Curtainsider Trailers', 'slug': 'curtainsider-trailers'},
        {'name': 'Tipper Trailers', 'slug': 'tipper-trailers'},
        {'name': 'Refrigerator Trailers', 'slug': 'refrigerator-trailers'},
        {'name': 'Flatbed Trailers', 'slug': 'flatbed-trailers'},
        {'name': 'Caravans', 'slug': 'caravans'},
        {'name': 'Other Trailers', 'slug': 'other-trailers'},
    ]},
    {'name': 'Construction & Warehouse Equipment', 'slug': 'construction', 'order': 9, 'subcategories': [
        {'name': 'Excavators', 'slug': 'excavators'},
        {'name': 'Loaders', 'slug': 'loaders'},
        {'name': 'Cranes', 'slug': 'cranes'},
        {'name': 'Bulldozers', 'slug': 'bulldozers'},
        {'name': 'Forklifts', 'slug': 'forklifts'},
        {'name': 'Concrete Mixers', 'slug': 'concrete-mixers'},
        {'name': 'Compactors', 'slug': 'compactors'},
        {'name': 'Other Construction', 'slug': 'other-construction'},
    ]},
    {'name': 'Agricultural & Forestry', 'slug': 'agriculture', 'order': 10, 'subcategories': [
        {'name': 'Tractors', 'slug': 'tractors'},
        {'name': 'Combine Harvesters', 'slug': 'combines'},
        {'name': 'Sprayers', 'slug': 'sprayers'},
        {'name': 'Ploughs', 'slug': 'ploughs'},
        {'name': 'Cultivators', 'slug': 'cultivators'},
        {'name': 'Balers', 'slug': 'balers'},
        {'name': 'Forestry Machines', 'slug': 'forestry-machines'},
        {'name': 'Other Agricultural', 'slug': 'other-agricultural'},
    ]},
    {'name': 'Bicycles & Scooters', 'slug': 'bicycles', 'order': 11, 'subcategories': [
        {'name': 'Bicycles', 'slug': 'bicycles'},
        {'name': 'Electric Bikes', 'slug': 'electric-bikes'},
        {'name': 'Electric Scooters', 'slug': 'electric-scooters'},
    ]},
    {'name': 'Services', 'slug': 'services', 'order': 12, 'subcategories': [
        {'name': 'Car Service', 'slug': 'car-service'},
        {'name': 'Diagnostics', 'slug': 'diagnostics'},
        {'name': 'Body Repair', 'slug': 'body-repair'},
        {'name': 'Painting', 'slug': 'painting'},
        {'name': 'Car Wash', 'slug': 'car-wash'},
        {'name': 'Towing', 'slug': 'towing'},
    ]},
    {'name': 'Car Rental', 'slug': 'rental', 'order': 13, 'subcategories': []},
    {'name': 'Planes & Aircraft', 'slug': 'planes', 'order': 14, 'subcategories': [
        {'name': 'Airplanes', 'slug': 'airplanes'},
        {'name': 'Helicopters', 'slug': 'helicopters'},
        {'name': 'Drones', 'slug': 'drones'},
        {'name': 'Ultralight Aircraft', 'slug': 'ultralight'},
    ]},
    {'name': 'Aircraft Parts', 'slug': 'planes-parts', 'order': 15, 'subcategories': [
        {'name': 'Engine Parts', 'slug': 'engine-parts'},
        {'name': 'Avionics', 'slug': 'avionics'},
        {'name': 'Aircraft Accessories', 'slug': 'aircraft-accessories'},
    ]},
]


class Command(BaseCommand):
    help = 'Reset and seed vehicle type categories'

    def handle(self, *args, **options):
        self.stdout.write('Deleting existing categories...')
        SubCategory.objects.all().delete()
        VehicleType.objects.all().delete()

        self.stdout.write('Creating new categories...')
        for cat in CATEGORIES:
            vt = VehicleType.objects.create(
                name=cat['name'],
                slug=cat['slug'],
                order=cat['order'],
            )
            for sub in cat['subcategories']:
                SubCategory.objects.create(
                    name=sub['name'],
                    slug=sub['slug'],
                    vehicle_type=vt,
                )
            self.stdout.write(f"  ok {vt.name} ({len(cat['subcategories'])} subcategories)")

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! Created {VehicleType.objects.count()} categories, '
            f'{SubCategory.objects.count()} subcategories.'
        ))