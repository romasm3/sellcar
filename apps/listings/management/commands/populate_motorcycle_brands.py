from django.core.management.base import BaseCommand
from django.utils.text import slugify
from apps.listings.models import MotorcycleBrand


class Command(BaseCommand):
    help = 'Populate MotorcycleBrand table with motorcycle brands from autoplius.lt'

    BRANDS = [
        'ABM', 'Access Motor', 'Adiva', 'ADVENTO', 'Aeon', 'Aermacchi', 'AGM',
        'Aixam', 'AJP', 'AJS', 'Alfarad', 'Alfer', 'Amazonas', 'American Eagle',
        'AODES', 'APG', 'Apollo', 'Aprilia', 'Archive Motorcycle', 'Arctic Cat',
        'Ardie', 'Argo', 'Asix', 'Askoll', 'ATK', 'Atlant', 'ATM', 'ATV', 'Azel',
        'BamX', 'Baotian', 'Barton', 'Bashan', 'BENDA', 'Benelli', 'Benzhou',
        'Beta', 'Bifei', 'Big Bear Choppers', 'Big Dog', 'Bimota', 'Blata',
        'Blinc', 'BLUROC', 'BM', 'BMC Choppers', 'BMW', 'Bombardier',
        'Boom Trike Family', 'Borile', 'Boss Hoss', 'Bravo', 'Brixton', 'BSA',
        'Bucci Moto', 'Buell', 'Bullit', 'Bultaco', 'Cagiva', 'Campagna',
        'Can-Am', 'Cannondale', 'CCM', 'CECTEK', 'CF', 'CFMOTO', 'Champ',
        'Chang Jiang', 'Citycoco', 'Cirax', 'Club Car', 'Cobra', 'Comarth',
        'Comfimax', 'Confederate', 'Cooper', 'Cpi', 'Crowne', 'CZ', 'Daelim',
        'Dafier', 'Dandy', 'Defiant', 'Delta', 'DemonX', 'Derbi', 'Diabolini',
        'Dinli', 'Dirtmax', 'DKW', 'DM Telai', 'Dniepr', 'Dodge', 'Donghai',
        'Doohan', 'Dorton', 'Dragster', 'Ducar', 'Ducati', 'E-MIO', 'E-RIDE',
        'E.V.A.', 'Easycool', 'EGL Moto', 'Egimotor', 'Ekomoto',
        'Electric Motion', 'Electron', 'Elegant', 'EMCO', 'Energica', 'Enfield',
        'Enticer', 'eWind', 'Explorer', 'Fabrikat', 'Factory', 'Factory Bike',
        'Fantic', 'FB mondial', 'Fine Custom Mechanics', 'Fischer',
        'Flyrite Choppers', 'FN', 'Forsage', 'Fosti', 'Futong', 'Fuxin',
        'G max', 'G&G', 'Gas Gas', 'Geely', 'Generic', 'Ghezzi Brian',
        'Ghezzi-Brian', 'Gilera', 'Goes', 'Govecs', 'GX moto', 'Hanway',
        'Haojin', 'Harley-Davidson', 'Hartford', 'Hawk', 'Hecht', 'Hercules',
        'Highland', 'Highper', 'Himoto', 'HM', 'Honda', 'Honling', 'Horex',
        'HORWIN', 'Horwin', 'HUONIAO', 'Husaberg', 'Husqvarna', 'Hyosung',
        'IKUDZO', 'Inca', 'Indian', 'Indian Challenger', 'Indian FTR',
        'Indian Pursuit', 'Indian Springfield', 'Indian Super Chief', 'IRBIS',
        'Iron Horse', 'Italjet', 'Izh', 'Jawa', 'Jawa CZ', 'Jialing',
        'Jianshe Yamaha', 'Jincheng', 'Jinlun', 'Jinpeng', 'JM', 'JMC',
        'John Deere', 'Johnny Pag', 'Jonway', 'Junak', 'Kandi', 'Kangda',
        'Kanuni', 'Karpat', 'Kawasaki', 'Kaxa Motos', 'KAYO', 'Keeway', 'Keren',
        'Kinlon Motors', 'KM', 'KMT MOTORS', 'KMZ', 'KOVE', 'Kramit',
        'Kreidler', 'KSR MOTO', 'KTM', 'KUBERG', 'KXD', 'Kymco', 'Lambretta',
        'Lantana', 'Lascari', 'Laverda', 'Legend', 'Lexmoto', 'Lifan',
        'Lingben', 'Linhai', 'Lintex', 'LIYA', 'LIZZARD', 'Loncin', 'Longjia',
        'Macbor', 'MADEMOTO', 'Magni', 'Magpower', 'Maico', 'Malaguti',
        'Malanca', 'Masai', 'Mash', 'Matchless', 'MBK', 'MBS', 'Metrakit',
        'Midual', 'Mikilon', 'Minsk', 'MM', 'MM3', 'Mondial', 'Monkey',
        'Montesa', 'Morbidelli', 'Mosca', 'Moser', 'Moto Guzzi', 'Moto Morini',
        'Motobi', 'Motoland', 'Motolevo', 'Motor hispania', 'Mototrans',
        'Motowell', 'Motrac', 'Motron', 'Mountain Max', 'MTT', 'Münch', 'Munch',
        'Mutt', 'MuZ', 'MV Agusta', 'MV Agusta Turismo Veloce', 'MZ', 'NCR',
        'Neander', 'NECO', 'Neval', 'Nexus', 'Nipponia', 'Nitro Motors', 'NIU',
        'Norton', 'NSU', 'Omaks Motors', 'Online', 'Orange County Choppers',
        'Orion', 'Ossa', 'Ovation', 'Pagsta', 'Pannonia', 'Patron', 'Pegasus',
        'Petronas', 'Peugeot', 'PGO', 'Phazer', 'Piaggio', 'Pioneer', 'Pitmoto',
        'Pitsterpro', 'Polaris', 'Polini', 'Praga', 'Praktik', 'PUCH', 'Qingi',
        'QJMOTOR', 'Quadro', 'QWMOTO', 'Rajdoot', 'Rally USA', 'Regal Raptor',
        'Renly', 'Rerode', 'Rewaco', 'REX', 'RFN', 'Ride', 'Rieju', 'Riga',
        'RM', 'Roadsign', 'ROAR', 'Romet', 'Rover', 'Roxon', 'Royal Enfield',
        'Sachs', 'Sagitta', 'Samurai', 'Sanglas', 'Saxon', 'Scooterking',
        'Scorpa', 'SCUT', 'Sea-Doo', 'SEAT MÓ', 'Secma', 'Segway', 'Senke',
        'Senlong', 'Sherco', 'Shineray', 'SHINERAY', 'Siamoto', 'Silence',
        'SiM', 'Simson', 'SINNIS', 'Ski Doo', 'Skygo', 'Skyteam', 'SMC',
        'Sodikart', 'Solo', 'SONIK', 'Sonik', 'Sora', 'SPYRACING',
        'SRT 5', 'SRV', 'SRX', 'Stark', 'Stels', 'Stomp', 'Sturmey-Archer',
        'SunL', 'Sunra', 'Super Soco', 'Super Soco/Vmoto', 'Sur-Ron', 'Suzuki',
        'SVM', 'Swift', 'SWM', 'Sym',
        'Talaria', 'Tank', 'TAO', 'Tauris', 'TGB', 'Tianying', 'Titan',
        'TM Racing', 'Tomos', 'Tomoto', 'Toro', 'Torrot', 'Traverson',
        'Trinity', 'Tripl', 'Triumph', 'Turist', 'TVS',
        'UNU', 'URBET', 'Ural', 'UTV',
        'V-Max', 'Van Veen', 'Vanderhall', 'Vario', 'VASSLA', 'Vastro',
        'Vento', 'Venture', 'Vertemati', 'Vespa', 'Viatka', 'Victory',
        'Viking', 'VMODE', 'Viper', 'Voge', 'VOGE', 'Von Dutch', 'VOR',
        'Voschod', 'Voxan', 'Vyrus',
        'Wangye', 'Wayel', 'Wayscral', 'WONJAN', 'Wottan', 'WSM',
        'Wuyang', 'Wuyi Wusheng Electric',
        'X-motos', 'Xingfu', 'Xingyue', 'Xmotos', 'X.star', 'XTR',
        'YADEA', 'Yamaha', 'Yamasaki', 'Yangtze', 'YCF', 'Yeti 500', 'Yiben',
        'Yiying',
        'Z Bike', 'Zeeho', 'Zero', 'ZEV', 'Zhongqing', 'Zipp', 'ZNEN',
        'Zongshen', 'Zontes', 'Zundapp', 'Zweirad Union', 'ZZ',
        'Other',
    ]

    def handle(self, *args, **options):
        created_count = 0
        skipped_count = 0
        slug_conflicts = {}

        self.stdout.write(f'Processing {len(self.BRANDS)} motorcycle brands...\n')

        for name in self.BRANDS:
            base_slug = slugify(name)
            if not base_slug:
                # Fallback if slugify returns empty (e.g. non-ASCII only names)
                base_slug = name.lower().replace(' ', '-')

            # Handle slug conflicts (e.g. "Münch" and "Munch" both slugify to "munch")
            slug = base_slug
            counter = slug_conflicts.get(base_slug, 0)
            if counter > 0:
                slug = f'{base_slug}-{counter + 1}'
            slug_conflicts[base_slug] = counter + 1

            brand, created = MotorcycleBrand.objects.get_or_create(
                slug=slug,
                defaults={'name': name},
            )

            if created:
                created_count += 1
                self.stdout.write(f'  ✓ Created: {name} (slug: {slug})')
            else:
                skipped_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! Created: {created_count}, Skipped (already exist): {skipped_count}'
        ))
        self.stdout.write(f'Total motorcycle brands in DB: {MotorcycleBrand.objects.count()}')