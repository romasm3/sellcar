from django.core.management.base import BaseCommand
from apps.listings.models import VehicleType, Brand, Model, FuelType, Transmission


class Command(BaseCommand):
    help = "Populate database with initial data for vehicle listings"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Starting to populate data..."))

        # Create Fuel Types
        self.stdout.write("Creating Fuel Types...")
        fuel_types_data = [
            "petrol",
            "diesel",
            "electric",
            "hybrid",
            "lpg",
            "other",
        ]

        for fuel in fuel_types_data:
            FuelType.objects.get_or_create(name=fuel)

        self.stdout.write(
            self.style.SUCCESS(f"✓ Created {len(fuel_types_data)} Fuel Types")
        )

        # Create Transmissions
        self.stdout.write("Creating Transmissions...")
        transmission_data = [
            "manual",
            "automatic",
            "semi_automatic",
        ]

        for trans in transmission_data:
            Transmission.objects.get_or_create(name=trans)

        self.stdout.write(
            self.style.SUCCESS(f"✓ Created {len(transmission_data)} Transmissions")
        )

        # Create Vehicle Types
        self.stdout.write("Creating Vehicle Types...")
        vehicle_types_data = [
            "Sedan",
            "SUV",
            "Hatchback",
            "Coupe",
            "Convertible",
            "Wagon",
            "Van",
            "Pickup Truck",
            "Minivan",
            "Sports Car",
        ]

        for vtype in vehicle_types_data:
            VehicleType.objects.get_or_create(name=vtype)

        self.stdout.write(
            self.style.SUCCESS(f"✓ Created {len(vehicle_types_data)} Vehicle Types")
        )

        # Create Brands and Models
        self.stdout.write("Creating Brands and Models...")

        brands_models = {
            "BMW": ["320d", "330i", "520d", "X5", "X3", "M3", "M5", "740i"],
            "Audi": ["A3", "A4", "A6", "Q5", "Q7", "S3", "RS6", "TT"],
            "Mercedes-Benz": ["C200", "E220", "S500", "GLE", "GLA", "AMG GT", "CLS"],
            "Volkswagen": ["Golf", "Passat", "Tiguan", "Polo", "Arteon", "Touareg"],
            "Toyota": ["Corolla", "Camry", "RAV4", "Land Cruiser", "Yaris", "Prius"],
            "Honda": ["Civic", "Accord", "CR-V", "HR-V", "Jazz"],
            "Ford": ["Focus", "Fiesta", "Mustang", "Mondeo", "Kuga", "Ranger"],
            "Opel": ["Astra", "Insignia", "Corsa", "Mokka", "Grandland"],
            "Renault": ["Clio", "Megane", "Captur", "Kadjar", "Talisman"],
            "Peugeot": ["208", "308", "508", "2008", "3008", "5008"],
            "Volvo": ["S60", "S90", "V60", "XC60", "XC90"],
            "Nissan": ["Qashqai", "Juke", "X-Trail", "Leaf", "Micra"],
            "Mazda": ["CX-5", "Mazda3", "Mazda6", "CX-3", "MX-5"],
            "Skoda": ["Octavia", "Superb", "Fabia", "Kodiaq", "Kamiq"],
            "Hyundai": ["i30", "Tucson", "Santa Fe", "Kona", "i20"],
            "Kia": ["Ceed", "Sportage", "Sorento", "Stonic", "Rio"],
        }

        brand_count = 0
        model_count = 0

        for brand_name, models_list in brands_models.items():
            brand, created = Brand.objects.get_or_create(name=brand_name)
            if created:
                brand_count += 1

            for model_name in models_list:
                _, created = Model.objects.get_or_create(brand=brand, name=model_name)
                if created:
                    model_count += 1

        self.stdout.write(self.style.SUCCESS(f"✓ Created {brand_count} Brands"))
        self.stdout.write(self.style.SUCCESS(f"✓ Created {model_count} Models"))

        self.stdout.write(self.style.SUCCESS("\n🎉 Database populated successfully!"))
        self.stdout.write(
            self.style.SUCCESS(
                "You can now add more brands/models via admin or run this command again."
            )
        )
