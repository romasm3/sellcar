from django.core.management.base import BaseCommand
from django.utils.text import slugify
from apps.listings.models import VehicleType, Brand, Model, FuelType, Transmission, Equipment


class Command(BaseCommand):
    help = "Populate database with all brands, models, and equipment"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Starting to populate data..."))

        # 1. Create Vehicle Types
        self.stdout.write("Creating Vehicle Types...")
        vehicle_types_data = ["Cars", "SUV", "Trucks", "Vans", "Motorcycles"]
        default_vehicle_type = None
        
        for vt in vehicle_types_data:
            obj, created = VehicleType.objects.get_or_create(
                slug=slugify(vt),
                defaults={'name': vt}
            )
            if vt == "Cars":
                default_vehicle_type = obj
        
        self.stdout.write(self.style.SUCCESS(f"✓ Vehicle Types: {len(vehicle_types_data)}"))

        # 2. Create Fuel Types
        self.stdout.write("Creating Fuel Types...")
        fuel_types_data = ["Petrol", "Diesel", "Electric", "Hybrid", "Plug-in Hybrid", "LPG"]
        
        for fuel in fuel_types_data:
            FuelType.objects.get_or_create(name=fuel)
        
        self.stdout.write(self.style.SUCCESS(f"✓ Fuel Types: {len(fuel_types_data)}"))

        # 3. Create Transmissions
        self.stdout.write("Creating Transmissions...")
        transmission_data = ["Manual", "Automatic", "Semi-automatic", "CVT"]
        
        for trans in transmission_data:
            Transmission.objects.get_or_create(name=trans)
        
        self.stdout.write(self.style.SUCCESS(f"✓ Transmissions: {len(transmission_data)}"))

        # 4. Create Brands and Models
        self.stdout.write("Creating Brands and Models...")
        
        brands_models = {
            "Audi": ["A1", "A3", "A4", "A5", "A6", "A7", "A8", "Q2", "Q3", "Q5", "Q7", "Q8", "e-tron", "RS3", "RS4", "RS5", "RS6", "RS7", "S3", "S4", "S5", "S6", "S7", "S8", "TT", "R8"],
            "BMW": ["1 Series", "2 Series", "3 Series", "4 Series", "5 Series", "6 Series", "7 Series", "8 Series", "X1", "X2", "X3", "X4", "X5", "X6", "X7", "Z4", "i3", "i4", "i7", "iX", "M2", "M3", "M4", "M5", "M8"],
            "Mercedes-Benz": ["A-Class", "B-Class", "C-Class", "CLA", "CLS", "E-Class", "EQA", "EQB", "EQC", "EQE", "EQS", "G-Class", "GLA", "GLB", "GLC", "GLE", "GLS", "S-Class", "SL", "AMG GT", "V-Class", "Vito", "Sprinter"],
            "Volkswagen": ["Arteon", "Caddy", "Golf", "ID.3", "ID.4", "ID.5", "Jetta", "Passat", "Polo", "T-Cross", "T-Roc", "Taigo", "Tiguan", "Touareg", "Touran", "Transporter", "Up"],
            "Toyota": ["Aygo", "Aygo X", "C-HR", "Camry", "Corolla", "GR86", "GR Supra", "GR Yaris", "Highlander", "Hilux", "Land Cruiser", "Prius", "Proace", "RAV4", "Supra", "Yaris", "Yaris Cross", "bZ4X"],
            "Honda": ["Accord", "Civic", "CR-V", "e", "HR-V", "Jazz", "NSX", "ZR-V"],
            "Nissan": ["Ariya", "GT-R", "Juke", "Leaf", "Micra", "Navara", "Note", "Qashqai", "X-Trail"],
            "Mazda": ["2", "3", "6", "CX-3", "CX-30", "CX-5", "CX-60", "MX-30", "MX-5"],
            "Ford": ["Bronco", "EcoSport", "Explorer", "F-150", "Fiesta", "Focus", "Galaxy", "Kuga", "Mondeo", "Mustang", "Mustang Mach-E", "Puma", "Ranger", "S-Max", "Transit"],
            "Opel": ["Astra", "Combo", "Corsa", "Crossland", "Grandland", "Insignia", "Mokka", "Movano", "Vivaro", "Zafira"],
            "Peugeot": ["108", "2008", "208", "3008", "308", "408", "5008", "508", "Boxer", "Expert", "Partner", "Rifter"],
            "Renault": ["Arkana", "Austral", "Captur", "Clio", "Espace", "Kangoo", "Koleos", "Master", "Megane", "Scenic", "Trafic", "Twingo", "Zoe"],
            "Citroen": ["Berlingo", "C1", "C3", "C3 Aircross", "C4", "C4 X", "C5 Aircross", "C5 X", "Jumper", "Jumpy", "SpaceTourer"],
            "Fiat": ["500", "500L", "500X", "Ducato", "Panda", "Punto", "Tipo"],
            "Alfa Romeo": ["Giulia", "Giulietta", "Stelvio", "Tonale"],
            "Volvo": ["C40", "S60", "S90", "V60", "V90", "XC40", "XC60", "XC90", "EX30", "EX90"],
            "Skoda": ["Citigo", "Enyaq", "Fabia", "Kamiq", "Karoq", "Kodiaq", "Octavia", "Rapid", "Scala", "Superb"],
            "SEAT": ["Arona", "Ateca", "Ibiza", "Leon", "Tarraco"],
            "Cupra": ["Ateca", "Born", "Formentor", "Leon", "Tavascan"],
            "Hyundai": ["Bayon", "i10", "i20", "i30", "Ioniq", "Ioniq 5", "Ioniq 6", "Kona", "Nexo", "Santa Fe", "Tucson"],
            "Kia": ["Carens", "Ceed", "EV6", "EV9", "Niro", "Picanto", "ProCeed", "Rio", "Sorento", "Soul", "Sportage", "Stinger", "Stonic", "XCeed"],
            "Porsche": ["718 Boxster", "718 Cayman", "911", "Cayenne", "Macan", "Panamera", "Taycan"],
            "Land Rover": ["Defender", "Discovery", "Discovery Sport", "Range Rover", "Range Rover Evoque", "Range Rover Sport", "Range Rover Velar"],
            "Jaguar": ["E-Pace", "F-Pace", "F-Type", "I-Pace", "XE", "XF"],
            "MINI": ["Clubman", "Convertible", "Cooper", "Countryman", "Electric"],
            "Tesla": ["Cybertruck", "Model 3", "Model S", "Model X", "Model Y"],
            "Lexus": ["CT", "ES", "IS", "LC", "LS", "NX", "RC", "RX", "RZ", "UX"],
            "Infiniti": ["Q30", "Q50", "Q60", "QX30", "QX50", "QX55", "QX60", "QX80"],
            "Subaru": ["BRZ", "Crosstrek", "Forester", "Impreza", "Legacy", "Outback", "Solterra", "WRX"],
            "Suzuki": ["Across", "Baleno", "Ignis", "Jimny", "S-Cross", "Swift", "Swace", "Vitara"],
            "Mitsubishi": ["ASX", "Eclipse Cross", "L200", "Outlander", "Space Star"],
            "Jeep": ["Cherokee", "Compass", "Gladiator", "Grand Cherokee", "Renegade", "Wrangler"],
            "Dacia": ["Dokker", "Duster", "Jogger", "Logan", "Sandero", "Spring"],
            "Chevrolet": ["Camaro", "Colorado", "Corvette", "Equinox", "Malibu", "Silverado", "Tahoe", "Trax"],
            "Dodge": ["Challenger", "Charger", "Durango", "RAM 1500"],
            "Chrysler": ["300", "Pacifica"],
            "Cadillac": ["CT4", "CT5", "Escalade", "Lyriq", "XT4", "XT5", "XT6"],
            "Genesis": ["G70", "G80", "G90", "GV60", "GV70", "GV80"],
            "Maserati": ["Ghibli", "GranTurismo", "Grecale", "Levante", "MC20", "Quattroporte"],
            "Ferrari": ["296 GTB", "488", "812", "F8", "Portofino", "Purosangue", "Roma", "SF90"],
            "Lamborghini": ["Aventador", "Huracan", "Revuelto", "Urus"],
            "Bentley": ["Bentayga", "Continental", "Flying Spur"],
            "Rolls-Royce": ["Cullinan", "Dawn", "Ghost", "Phantom", "Spectre", "Wraith"],
            "Aston Martin": ["DB11", "DB12", "DBS", "DBX", "Vantage"],
            "McLaren": ["720S", "750S", "765LT", "Artura", "GT"],
            "Lotus": ["Eletre", "Elise", "Emira", "Evora", "Exige"],
            "Polestar": ["1", "2", "3", "4"],
            "BYD": ["Atto 3", "Dolphin", "Han", "Seal", "Tang"],
            "MG": ["4", "5", "HS", "Marvel R", "MG4", "ZS"],
            "NIO": ["EC6", "ES6", "ES7", "ES8", "ET5", "ET7"],
            "Rivian": ["R1S", "R1T"],
            "Lucid": ["Air"],
            "Smart": ["#1", "#3", "EQ fortwo", "forfour", "fortwo"],
            "Lada": ["Granta", "Niva", "Vesta"],
        }

        brand_count = 0
        model_count = 0

        for brand_name, models_list in brands_models.items():
            brand_slug = slugify(brand_name)
            
            # Create or get brand
            brand, created = Brand.objects.get_or_create(
                slug=brand_slug,
                defaults={
                    'name': brand_name,
                    'vehicle_type': default_vehicle_type
                }
            )
            if created:
                brand_count += 1

            # Create models for this brand
            for model_name in models_list:
                model_slug = slugify(model_name)
                
                # Handle duplicate slugs
                base_slug = model_slug
                counter = 1
                while Model.objects.filter(brand=brand, slug=model_slug).exists():
                    model_slug = f"{base_slug}-{counter}"
                    counter += 1
                
                _, model_created = Model.objects.get_or_create(
                    brand=brand,
                    slug=model_slug,
                    defaults={'name': model_name}
                )
                if model_created:
                    model_count += 1

        self.stdout.write(self.style.SUCCESS(f"✓ Brands: {brand_count}"))
        self.stdout.write(self.style.SUCCESS(f"✓ Models: {model_count}"))

        # 5. Create Equipment
        self.stdout.write("Creating Equipment...")
        
        equipment_data = {
            "safety": ["ABS", "ESP", "Airbag (driver)", "Airbag (passenger)", "Side airbags", "Parking sensors", "Rear camera", "Blind spot monitor", "Lane assist", "Adaptive cruise control"],
            "interior": ["Air conditioning", "Climate control", "Heated seats", "Leather seats", "Electric seats", "Sunroof", "Keyless entry", "Navigation"],
            "audio_video": ["Bluetooth", "Apple CarPlay", "Android Auto", "USB", "Premium sound system", "Touchscreen"],
            "exterior": ["Alloy wheels", "LED headlights", "Xenon headlights", "Fog lights", "Roof rails", "Tow hook"],
            "other": ["Cruise control", "Start/Stop", "4x4", "AWD", "Paddle shifters"]
        }

        equipment_count = 0
        for category, items in equipment_data.items():
            for item_name in items:
                _, created = Equipment.objects.get_or_create(
                    name=item_name,
                    defaults={'category': category}
                )
                if created:
                    equipment_count += 1

        self.stdout.write(self.style.SUCCESS(f"✓ Equipment: {equipment_count}"))

        # Summary
        self.stdout.write(self.style.SUCCESS("\n" + "=" * 50))
        self.stdout.write(self.style.SUCCESS("🎉 DATABASE POPULATED SUCCESSFULLY!"))
        self.stdout.write(self.style.SUCCESS("=" * 50))
        self.stdout.write(f"Vehicle Types: {VehicleType.objects.count()}")
        self.stdout.write(f"Fuel Types: {FuelType.objects.count()}")
        self.stdout.write(f"Transmissions: {Transmission.objects.count()}")
        self.stdout.write(f"Brands: {Brand.objects.count()}")
        self.stdout.write(f"Models: {Model.objects.count()}")
        self.stdout.write(f"Equipment: {Equipment.objects.count()}")