
"""

Seed PartCategory tree — Single part / parts kit flow.



Trys lygiai:

  0 = TOP CATEGORY  (Lighting, Engine, Brakes...)

  1 = GROUP         (Rear Lights, Front Lights...)

  2 = SUBCATEGORY   (Rear Light Bulb — galutinis pasirinkimas)



Run:

    python manage.py seed_part_categories

    python manage.py seed_part_categories --dry-run

    python manage.py seed_part_categories --reset

"""



from django.core.management.base import BaseCommand

from django.db import transaction

from django.utils.text import slugify



from apps.listings.models import PartCategory





# ═══════════════════════════════════════════════════════════════════════════

# PARTS TREE — pagal autogidas.lt struktūrą

# ═══════════════════════════════════════════════════════════════════════════

# Formatas:

#   "Top Category" : {

#       "icon": "icon-name",

#       "groups": {

#           "Group Name": ["Subcategory 1", "Subcategory 2", ...]

#       }

#   }



PARTS_TREE = {

    "Lighting": {

        "icon": "lightbulb",

        "groups": {

            "Rear Lights": [

                "Rear Light", "Rear Light Bulb", "Rear Light Lens",

                "Rear Light Housing", "Rear Light Wiring", "Brake Light",

                "Reverse Light", "License Plate Light", "Reflector",

            ],

            "Front Lights": [

                "Headlight", "Headlight Bulb", "Headlight Lens",

                "Headlight Housing", "Headlight Wiring", "Headlight Adjuster",

                "Xenon Module", "LED Module", "Daytime Running Light",

                "Headlight Washer",

            ],

            "Turn Lights": [

                "Turn Signal Front", "Turn Signal Rear", "Turn Signal Side",

                "Turn Signal Bulb", "Turn Signal Lens", "Hazard Switch",

            ],

            "Fog Lights": [

                "Fog Light Front", "Fog Light Rear", "Fog Light Bulb",

                "Fog Light Switch", "Fog Light Housing",

            ],

            "Interior Lighting": [

                "Dome Light", "Map Light", "Trunk Light", "Glove Box Light",

                "Door Light", "Ambient Light", "Reading Light",

            ],

        },

    },

    "Engine": {

        "icon": "engine",

        "groups": {

            "Engine Block": [

                "Engine Assembly", "Cylinder Head", "Cylinder Block",

                "Piston", "Piston Ring", "Connecting Rod", "Crankshaft",

                "Camshaft", "Engine Bearing", "Engine Gasket Set",

                "Head Gasket", "Oil Pan", "Timing Belt", "Timing Chain",

                "Timing Cover",

            ],

            "Intake & Boost": [

                "Intake Manifold", "Throttle Body", "Air Filter",

                "Air Filter Housing", "MAF Sensor", "Turbocharger",

                "Supercharger", "Intercooler", "Intercooler Hose",

                "Boost Pressure Sensor",

            ],

            "Engine Auxiliary": [

                "Engine Mount", "Engine Oil Cooler", "Oil Filter Housing",

                "PCV Valve", "EGR Valve", "EGR Cooler", "Vacuum Pump",

                "Engine Wiring Harness", "Belt Tensioner", "Drive Belt",

                "Idler Pulley",

            ],

        },

    },

    "Brakes": {

        "icon": "brake-disc",

        "groups": {

            "Brake Parts": [

                "Brake Disc", "Brake Pad", "Brake Caliper", "Brake Drum",

                "Brake Shoe", "Brake Hose", "Brake Line", "Brake Master Cylinder",

                "Brake Booster", "ABS Sensor", "ABS Module", "Handbrake Cable",

            ],

        },

    },

    "Exhaust System": {

        "icon": "exhaust",

        "groups": {

            "Exhaust Parts": [

                "Exhaust Manifold", "Catalytic Converter", "DPF Filter",

                "Particulate Filter", "Muffler", "Resonator", "Exhaust Pipe",

                "Exhaust Clamp", "Exhaust Hanger", "Lambda Sensor",

            ],

        },

    },

    "Fuel System": {

        "icon": "fuel",

        "groups": {

            "Fuel Parts": [

                "Fuel Pump", "Fuel Injector", "Fuel Rail", "Fuel Filter",

                "Fuel Tank", "Fuel Line", "Fuel Pressure Regulator",

                "Fuel Pressure Sensor", "High Pressure Pump",

            ],

        },

    },

    "Gearbox / Clutch / Transmission": {

        "icon": "gearbox",

        "groups": {

            "Manual Transmission": [

                "Manual Gearbox", "Gear Shifter", "Shift Linkage",

                "Clutch Kit", "Clutch Disc", "Clutch Pressure Plate",

                "Flywheel", "Clutch Master Cylinder", "Clutch Slave Cylinder",

            ],

            "Automatic Transmission": [

                "Automatic Gearbox", "Torque Converter", "Valve Body",

                "ATF Filter", "Mechatronics", "DSG Clutch",

            ],

            "Drivetrain": [

                "Driveshaft", "CV Joint", "CV Boot", "Differential",

                "Transfer Case",

            ],

        },

    },

    "Front Axle": {

        "icon": "axle-front",

        "groups": {

            "Front Axle Parts": [

                "Control Arm Front", "Ball Joint Front", "Tie Rod",

                "Tie Rod End", "Wheel Bearing Front", "Wheel Hub Front",

                "Shock Absorber Front", "Coil Spring Front", "Strut Mount Front",

                "Anti-roll Bar Front", "Anti-roll Bar Link Front",

                "Steering Knuckle Front", "Subframe Front",

            ],

        },

    },

    "Rear Axle": {

        "icon": "axle-rear",

        "groups": {

            "Rear Axle Parts": [

                "Control Arm Rear", "Wheel Bearing Rear", "Wheel Hub Rear",

                "Shock Absorber Rear", "Coil Spring Rear", "Strut Mount Rear",

                "Anti-roll Bar Rear", "Anti-roll Bar Link Rear",

                "Trailing Arm", "Subframe Rear",

            ],

        },

    },

    "Wheels / Tyres": {

        "icon": "wheel",

        "groups": {

            "Wheels": [

                "Alloy Wheel", "Steel Wheel", "Wheel Bolt", "Wheel Nut",

                "Wheel Center Cap", "TPMS Sensor",

            ],

            "Tyres": [

                "Summer Tyre", "Winter Tyre",

            ],

        },

    },

    "Body": {

        "icon": "car-body",

        "groups": {

            "Body Panels": [

                "Fender", "Hood", "Trunk Lid", "Tailgate", "Roof Panel",

                "Quarter Panel", "Sill Panel", "Floor Pan", "Firewall",

                "Body Side Molding", "Wheel Arch Trim", "Body Cladding",

                "Underbody Cover",

            ],

        },

    },

    "Front Exterior Parts": {

        "icon": "car-front",

        "groups": {

            "Front Body": [

                "Front Bumper", "Front Bumper Grille", "Front Bumper Spoiler",

                "Radiator Grille", "Front Splitter", "Front Lip",

                "Front Reinforcement Bar", "Front Crash Bar",

            ],

        },

    },

    "Rear Exterior Parts": {

        "icon": "car-rear",

        "groups": {

            "Rear Body": [

                "Rear Bumper", "Rear Bumper Grille", "Rear Spoiler",

                "Rear Diffuser", "Rear Reinforcement Bar", "Rear Crash Bar",

                "Tow Hook Cover Rear", "Trunk Spoiler", "Roof Spoiler",

            ],

        },

    },

    "Doors": {

        "icon": "door",

        "groups": {

            "Door Parts": [

                "Door Front Left", "Door Front Right", "Door Rear Left",

                "Door Rear Right", "Door Handle Exterior", "Door Handle Interior",

                "Door Mirror", "Door Lock", "Door Hinge", "Window Regulator",

                "Window Motor", "Door Seal",

            ],

        },

    },

    "Glass": {

        "icon": "windshield",

        "groups": {

            "Vehicle Glass": [

                "Windshield Front", "Windshield Rear", "Door Window Front",

                "Door Window Rear", "Quarter Glass", "Sunroof Glass",

                "Mirror Glass", "Windshield Trim", "Windshield Seal",

            ],

        },

    },

    "Window / Light Wash System": {

        "icon": "wiper",

        "groups": {

            "Wash & Wipe": [

                "Wiper Blade Front", "Wiper Blade Rear", "Wiper Arm Front",

                "Wiper Arm Rear", "Wiper Motor Front", "Wiper Motor Rear",

                "Washer Pump", "Washer Reservoir", "Washer Nozzle",

                "Headlight Washer Pump",

            ],

        },

    },

    "Interior": {

        "icon": "seat",

        "groups": {

            "Seats": [

                "Front Seat Left", "Front Seat Right", "Rear Seat",

                "Seat Cover", "Seat Belt", "Seat Belt Tensioner",

                "Seat Motor", "Seat Heater",

            ],

            "Dashboard": [

                "Dashboard", "Instrument Cluster", "Glove Box",

                "Center Console", "Steering Wheel", "Steering Column",

                "Pedal Assembly",

            ],

            "Trim & Carpet": [

                "Door Panel Trim", "Headliner", "Pillar Trim",

                "Floor Carpet", "Trunk Carpet",

            ],

            "Infotainment": [

                "Head Unit Radio", "Display Screen", "Speaker",

                "Amplifier", "Antenna", "Microphone", "Reversing Camera",

            ],

        },

    },

    "Electrical Systems": {

        "icon": "bolt",

        "groups": {

            "Power": [

                "Battery", "Starter Motor", "Alternator", "Battery Cable",

                "Battery Tray", "Fuse Box", "Main Wiring Harness",

            ],

            "Control Units": [

                "ECU Engine Control", "TCU Transmission", "BCM Body Control",

                "Comfort Module", "Gateway Module", "Immobilizer",

                "Key Fob", "Lock Module",

            ],

            "Sensors": [

                "Crankshaft Sensor", "Camshaft Sensor", "Knock Sensor",

                "Oxygen Sensor", "Parking Sensor",

            ],

            "Ignition": [

                "Spark Plug", "Glow Plug", "Ignition Coil",

                "Ignition Switch",

            ],

        },

    },

    "A/C, Heating, Radiators": {

        "icon": "snowflake",

        "groups": {

            "Climate": [

                "A/C Compressor", "A/C Condenser", "A/C Evaporator",

                "A/C Expansion Valve", "A/C Hose", "A/C Pipe",

                "A/C Pressure Switch", "Heater Core", "Heater Blower Motor",

                "Heater Resistor", "Climate Control Panel", "Cabin Filter",

            ],

            "Cooling": [

                "Radiator", "Radiator Fan", "Radiator Hose Upper",

                "Radiator Hose Lower", "Coolant Reservoir",

                "Water Pump", "Thermostat",

            ],

        },

    },

    "Other Parts": {

        "icon": "wrench",

        "groups": {

            "Other": [

                "Tow Hook", "Tow Bar", "Tools Kit", "Jack",

                "Warning Triangle", "First Aid Kit",

                "Roof Rack", "Floor Mats",

            ],

        },

    },

}





def make_slug(text, max_length=140):

    """Generate slug, max 140 chars."""

    s = slugify(text)

    return s[:max_length]





class Command(BaseCommand):

    help = "Seed PartCategory tree (categories → groups → subcategories) for Single part flow."



    def add_arguments(self, parser):

        parser.add_argument(

            '--reset',

            action='store_true',

            help='Delete ALL existing PartCategory rows before seeding.',

        )

        parser.add_argument(

            '--dry-run',

            action='store_true',

            help='Show what would be created without saving anything.',

        )



    @transaction.atomic

    def handle(self, *args, **opts):

        dry_run = opts['dry_run']

        reset = opts['reset']



        if reset and not dry_run:

            count = PartCategory.objects.count()

            PartCategory.objects.all().delete()

            self.stdout.write(self.style.WARNING(

                f"🗑️  Deleted {count} existing PartCategory rows."

            ))



        created_cats = 0

        created_groups = 0

        created_subs = 0

        skipped = 0



        for cat_order, (cat_name, cat_data) in enumerate(PARTS_TREE.items()):

            cat_slug = make_slug(cat_name)

            cat_icon = cat_data.get('icon', '')



            if dry_run:

                self.stdout.write(f"📁 [LVL 0] {cat_name} (slug={cat_slug}, icon={cat_icon})")

                cat = None

            else:

                cat, was_created = PartCategory.objects.get_or_create(

                    slug=cat_slug,

                    defaults={

                        'name_en': cat_name,

                        'level': PartCategory.LEVEL_CATEGORY,

                        'parent': None,

                        'icon': cat_icon,

                        'order': cat_order,

                    },

                )

                if was_created:

                    created_cats += 1

                    self.stdout.write(self.style.SUCCESS(f"  ✅ Category: {cat_name}"))

                else:

                    skipped += 1

                    # Atnaujinam icon/order jei pasikeitė

                    cat.icon = cat_icon

                    cat.order = cat_order

                    cat.save(update_fields=['icon', 'order'])



            for group_order, (group_name, subs) in enumerate(cat_data['groups'].items()):

                group_slug = make_slug(f"{cat_name}-{group_name}")



                if dry_run:

                    self.stdout.write(f"  📂 [LVL 1] {group_name} (slug={group_slug})")

                    group = None

                else:

                    group, was_created = PartCategory.objects.get_or_create(

                        slug=group_slug,

                        defaults={

                            'name_en': group_name,

                            'level': PartCategory.LEVEL_GROUP,

                            'parent': cat,

                            'order': group_order,

                        },

                    )

                    if was_created:

                        created_groups += 1

                        self.stdout.write(f"    ✅ Group: {group_name}")

                    else:

                        skipped += 1



                for sub_order, sub_name in enumerate(subs):

                    sub_slug = make_slug(f"{cat_name}-{group_name}-{sub_name}")



                    if dry_run:

                        self.stdout.write(f"    📄 [LVL 2] {sub_name} (slug={sub_slug})")

                    else:

                        _, was_created = PartCategory.objects.get_or_create(

                            slug=sub_slug,

                            defaults={

                                'name_en': sub_name,

                                'level': PartCategory.LEVEL_SUBCATEGORY,

                                'parent': group,

                                'order': sub_order,

                            },

                        )

                        if was_created:

                            created_subs += 1

                        else:

                            skipped += 1



        # ═══ Summary ═══

        self.stdout.write("")

        self.stdout.write(self.style.SUCCESS("═" * 60))

        if dry_run:

            self.stdout.write(self.style.WARNING("DRY-RUN — nothing was saved."))

        else:

            self.stdout.write(self.style.SUCCESS(

                f"✅ Created: {created_cats} categories, {created_groups} groups, {created_subs} subcategories"

            ))

            if skipped:

                self.stdout.write(self.style.WARNING(f"⏭️  Skipped (already existed): {skipped}"))

            total = PartCategory.objects.count()

            self.stdout.write(self.style.SUCCESS(f"📊 Total PartCategory rows now: {total}"))

        self.stdout.write(self.style.SUCCESS("═" * 60))

