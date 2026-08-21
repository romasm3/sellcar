from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from datetime import timedelta


class VehicleType(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    slug = models.SlugField(unique=True)
    order = models.IntegerField(default=0, verbose_name=_("Order"))

    class Meta:
        verbose_name=_("Vehicle Type")
        verbose_name_plural = "Vehicle Types"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    slug = models.SlugField()
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE, related_name='subcategories')

    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='children',
        verbose_name=_("Parent subcategory"),
    )
    order = models.IntegerField(default=0, verbose_name=_("Display order"))

    class Meta:
        verbose_name=_("SubCategory")
        verbose_name_plural = "SubCategories"
        ordering = ['order', 'name']
        unique_together = ['vehicle_type', 'slug']

    def __str__(self):
        return f"{self.vehicle_type.name} - {self.name}"


class BrandScope(models.Model):
    """Markių šeima — vienas sąrašas visoms tos pačios transporto priemonės
    kategorijoms.

    Autogide sąrašas yra vienas: motociklų (sec 02), motociklų dalių (sec 27)
    ir motociklų nuomos (sec 35) formose jis identiškas iki baito. Tą pačią
    logiką perimam: „motorcycles" šeima — viena, ją mato ir create forma, ir
    greitoji panelė, ir šoninė juosta, ir išplėstinė paieška.

    ``has_models`` — ar rodoma modelių kaskada. Autogide kaskada yra tik ten,
    kur jie turi modelių duomenų (automobiliai, motociklai); sunkvežimiams,
    priekaboms, žemės ūkiui modelis yra laisvas tekstas.
    """
    key = models.SlugField(unique=True, verbose_name=_("Raktas"))
    name = models.CharField(max_length=100, verbose_name=_("Pavadinimas"))
    has_models = models.BooleanField(default=False, verbose_name=_("Turi modelių kaskadą"))
    order = models.IntegerField(default=0, verbose_name=_("Eiliškumas"))

    class Meta:
        verbose_name = _("Markių šeima")
        verbose_name_plural = "Markių šeimos"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class BrandSuggestion(models.Model):
    """Vartotojo per „Kita" įvestas markės pavadinimas.

    Sąrašas pildosi pagal realų poreikį, o ne pagal spėjimus: jei penki
    žmonės įvedė „Jaecoo", admin'e tai matosi kaip pasiūlymas su
    skaitikliu ir vienu veiksmu virsta tikra marke.
    """
    STATUS_NEW = 'new'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    STATUS_CHOICES = [
        (STATUS_NEW, _('Naujas')),
        (STATUS_APPROVED, _('Patvirtinta')),
        (STATUS_REJECTED, _('Atmesta')),
    ]

    name = models.CharField(max_length=100, verbose_name=_("Pavadinimas"))
    scope = models.ForeignKey(
        'BrandScope', on_delete=models.CASCADE, related_name='suggestions',
        verbose_name=_("Šeima"),
    )
    times_used = models.PositiveIntegerField(default=1, verbose_name=_("Kiek kartų įvesta"))
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default=STATUS_NEW,
        verbose_name=_("Būsena"),
    )
    approved_brand = models.ForeignKey(
        'Brand', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='from_suggestions', verbose_name=_("Sukurta markė"),
    )
    first_seen = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Markės pasiūlymas")
        verbose_name_plural = "Markių pasiūlymai"
        ordering = ['-times_used', 'name']
        unique_together = ['scope', 'name']

    def __str__(self):
        return f'{self.name} ({self.scope.name}) ×{self.times_used}'


class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    slug = models.SlugField(unique=True)
    # Paliktas dėl suderinamumo su automobilių kodu; naujas šaltinis yra
    # ``scopes``. Vienas Brand gali priklausyti kelioms šeimoms (Volvo —
    # ir automobiliai, ir sunkvežimiai), todėl vieno VT nepakanka.
    vehicle_type = models.ForeignKey(
        VehicleType, on_delete=models.CASCADE, related_name='brands',
        null=True, blank=True,
    )
    scopes = models.ManyToManyField(
        BrandScope, related_name='brands', blank=True,
        verbose_name=_("Šeimos"),
    )
    logo = models.ImageField(
        upload_to='brand_logos/', null=True, blank=True,
        verbose_name=_("Logotipas"),
    )
    is_top = models.BooleanField(default=False, verbose_name=_("Top markė"))
    order = models.IntegerField(default=0, verbose_name=_("Eiliškumas"))

    # Kol senosios lentelės gyvos, formos rodo Brand, o saugo į senąjį FK.
    # Šios nuorodos leidžia tai padaryti be spėliojimo pagal pavadinimą.
    legacy_moto = models.OneToOneField(
        'MotorcycleBrand', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='unified',
    )
    legacy_truck = models.OneToOneField(
        'TruckBrand', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='unified',
    )
    legacy_gear = models.OneToOneField(
        'GearBrand', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='unified',
    )

    class Meta:
        verbose_name=_("Brand")
        verbose_name_plural = "Brands"
        ordering = ['name']

    def __str__(self):
        return self.name


class Model(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    slug = models.SlugField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='models')

    class Meta:
        verbose_name=_("Model")
        verbose_name_plural = "Models"
        ordering = ['name']
        # (brand, name) unikalumą saugo bazė: 2026-08-20 tas pats
        # perkėlimas buvo paleistas ir komanda, ir migracija — 3732
        # dublikatai. Dabar bazė tokio įrašo tiesiog nepriims.
        unique_together = [['brand', 'slug'], ['brand', 'name']]

    def __str__(self):
        return f"{self.brand.name} {self.name}"


class SubModel(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    slug = models.SlugField()
    model = models.ForeignKey(Model, on_delete=models.CASCADE, related_name='submodels')

    class Meta:
        verbose_name=_("SubModel")
        verbose_name_plural = "SubModels"
        ordering = ['name']
        unique_together = ['model', 'slug']

    def __str__(self):
        return f"{self.model.brand.name} {self.model.name} {self.name}"


class MotorcycleBrand(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name=_("Motorcycle Brand")
        verbose_name_plural = "Motorcycle Brands"
        ordering = ['name']

    def __str__(self):
        return self.name


class MotorcycleModel(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    slug = models.SlugField()
    brand = models.ForeignKey(MotorcycleBrand, on_delete=models.CASCADE, related_name='models')

    class Meta:
        verbose_name=_("Motorcycle Model")
        verbose_name_plural = "Motorcycle Models"
        ordering = ['name']
        unique_together = ['brand', 'slug']

    def __str__(self):
        return f"{self.brand.name} {self.name}"


# ═══════════════════════════════════════════════════════════
# TRUCK BRAND / MODEL — atskiros lentelės (kaip MotorcycleBrand)
# ═══════════════════════════════════════════════════════════

class TruckBrand(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name=_("Truck Brand")
        verbose_name_plural = "Truck Brands"
        ordering = ['name']

    def __str__(self):
        return self.name


class TruckModel(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    slug = models.SlugField()
    brand = models.ForeignKey(TruckBrand, on_delete=models.CASCADE, related_name='models')

    class Meta:
        verbose_name=_("Truck Model")
        verbose_name_plural = "Truck Models"
        ordering = ['name']
        unique_together = ['brand', 'slug']

    def __str__(self):
        return f"{self.brand.name} {self.name}"


# ═══════════════════════════════════════════════════════════
# GEAR BRAND — separate FK list (autoplius-style)
# ═══════════════════════════════════════════════════════════

class GearBrand(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    slug = models.SlugField(unique=True)
    order = models.IntegerField(default=0, verbose_name=_("Display order"))

    class Meta:
        verbose_name=_("Gear Brand")
        verbose_name_plural = "Gear Brands"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    @property
    def is_other(self):
        return self.slug == 'other'


class FuelType(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("Name"))

    class Meta:
        verbose_name=_("Fuel Type")
        verbose_name_plural = "Fuel Types"
        ordering = ['name']

    def __str__(self):
        return self.name


class Transmission(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("Name"))

    class Meta:
        verbose_name=_("Transmission")
        verbose_name_plural = "Transmissions"
        ordering = ['name']

    def __str__(self):
        return self.name


class Listing(models.Model):
    CONDITION_CHOICES = [
        ('new', _('New')),
        ('used', _('Used')),
        ('damaged', _('Damaged')),
    ]

    STATUS_CHOICES = [
        ('draft', _('Juodraštis')),
        ('active', _('Aktyvus')),
        ('reserved', _('Rezervuotas')),
        ('expired', _('Neaktyvus')),
        ('sold', _('Parduotas')),
        ('archived', _('Archyvuotas')),
    ]

    BODY_TYPE_CHOICES = [
        ('sedan', _('Sedan')), ('hatchback', _('Hatchback')),
        ('estate', _('Estate/Wagon')), ('minivan', _('Minivan')),
        ('suv', _('SUV/Crossover')), ('coupe', _('Coupe')),
        ('commercial', _('Commercial')), ('convertible', _('Convertible')),
        ('limousine', _('Limousine')), ('pickup', _('Pickup')),
        ('minibus', _('Minibus')), ('truck', _('Truck/Van')),
        ('other', _('Other')),
    ]

    # ═══ TRUCK TYPE — autoplius-style "Tipas" filter (23 types) ═══
    TRUCK_TYPE_CHOICES = [
        ('', _('— Select —')),
        ('tankers', _('Tankers')),
        ('car_carriers', _('Car Carriers')),
        ('concrete_mixers', _('Concrete Mixers')),
        ('flatbed', _('Flatbed')),
        ('flatbed_tarpaulin', _('Flatbed with Tarpaulin')),
        ('curtain_side', _('Curtain-Side')),
        ('double_cab', _('Double Cab')),
        ('livestock_carriers', _('Livestock Carriers')),
        ('insulated_box', _('Insulated Box')),
        ('hard_side_box', _('Hard-Side Box')),
        ('container_carriers', _('Container Carriers')),
        ('logging_trucks', _('Logging Trucks')),
        ('milk_tankers', _('Milk Tankers')),
        ('platforms', _('Platforms')),
        ('mobile_shop', _('Mobile Shop')),
        ('tippers', _('Tippers')),
        ('hook_lift_tippers', _('Hook-Lift Tippers')),
        ('crane_tippers', _('Crane Tippers')),
        ('with_crane', _('With Crane')),
        ('refrigerators', _('Refrigerators')),
        ('curtain_tarpaulin', _('Curtain / Tarpaulin')),
        ('chassis', _('Chassis')),
        ('other', _('Other')),
    ]

    # ═══ TRUCK WHEEL FORMULA — autoplius "Ratų formulė" ═══
    WHEEL_FORMULA_CHOICES = [
        ('', _('— Select —')),
        ('4x2', _('4x2')), ('4x4', _('4x4')),
        ('6x2', _('6x2')), ('6x2/4', _('6x2/4')),
        ('6x4', _('6x4')), ('6x4/2', _('6x4/2')),
        ('6x6', _('6x6')),
        ('8x2', _('8x2')), ('8x2/4', _('8x2/4')),
        ('8x4', _('8x4')), ('8x6', _('8x6')), ('8x8', _('8x8')),
        ('10x4', _('10x4')), ('10x6', _('10x6')), ('10x8', _('10x8')),
    ]

    # ═══ TRUCK MASS INTERVAL — autoplius "Masės intervalas" ═══
    MASS_INTERVAL_CHOICES = [
        ('', _('— Select —')),
        ('up_to_3.5t', _('Up to 3.5 t')),
        ('3.5_to_7.5t', _('3.5 - 7.5 t')),
        ('over_7.5t', _('Over 7.5 t')),
    ]

    # ═══ TRUCK SUSPENSION — autoplius "Pakaba" ═══
    TRUCK_SUSPENSION_CHOICES = [
        ('', _('— Select —')),
        ('air', _('Air')),
        ('spring', _('Spring')),
        ('parabolic', _('Parabolic')),
        ('hydraulic', _('Hydraulic')),
        ('rubber', _('Rubber')),
    ]

    # ═══ COLOR — 'Other' first ═══
    # 15 reikšmių pagal autogidas etaloną. Sidabrinė / Pilka / Smėlio /
    # Auksinė pridėtos nuomos vertikalėje; senų raktų NEKEIČIAM, kad esami
    # skelbimai liktų galioję — tik lt vertimai sutrumpinti iki pagrindinio
    # atspalvio („Žalia / chaki" → „Žalia"), nes dabar atspalviai atskiri.
    COLOR_CHOICES = [
        ('black', _('Black')), ('silver', _('Silver')), ('grey', _('Grey')),
        ('blue', _('Blue')), ('white', _('White')),
        ('red', _('Red / Burgundy')), ('green_khaki', _('Green / Khaki')),
        ('beige', _('Beige')), ('brown_beige', _('Brown / Beige')),
        ('gold', _('Gold')), ('yellow_gold', _('Yellow / Gold')),
        ('purple', _('Purple')), ('orange', _('Orange')),
        ('multicolor', _('Multicolor')), ('other', _('Other')),
    ]

    DEFECT_CHOICES = [
        ('none', _('No defects')), ('dented', _('Dented')),
        ('burned', _('Burned')), ('gearbox_defect', _('Gearbox defect')),
        ('hail_damage', _('Hail damage')), ('sunken', _('Sunken')),
        ('engine_defect', _('Engine defect')), ('major_defects', _('Major defects')),
        # Turistiniams nameliams reikėjo „Kiti smulkūs defektai"; tinka ir
        # automobiliams, todėl laikom bendrame sąraše.
        ('minor_defects', _('Kiti smulkūs defektai')),
    ]

    DOOR_CHOICES = [('2/3', _('2/3 doors')), ('4/5', _('4/5 doors')),
                    ('6/7', _('6/7 doors'))]

    STEERING_CHOICES = [
        ('left', _('Left-hand drive')),
        ('right', _('Right-hand drive (UK)')),
    ]

    DRIVE_TYPE_CHOICES = [
        ('fwd', _('Front-wheel drive (FWD)')),
        ('rwd', _('Rear-wheel drive (RWD)')),
        ('awd', _('All-wheel drive (AWD/4WD)')),
    ]

    EURO_STANDARD_CHOICES = [
        ('euro1', 'Euro 1'), ('euro2', 'Euro 2'),
        ('euro3', 'Euro 3'), ('euro4', 'Euro 4'),
        ('euro5', 'Euro 5'), ('euro6', 'Euro 6'),
        ('euro6d', 'Euro 6d'),
        # Priekaboms reikia 'Kitas'; laikom bendrame sąraše, kad
        # get_euro_standard_display() rodytų etiketę, o ne žalią 'other'.
        ('other', _('Kitas')),
    ]

    SEATS_CHOICES = [(str(i), str(i)) for i in range(1, 10)] + [('9+', '9+')]
    RIM_SIZE_CHOICES = [(str(i), f'{i}"') for i in range(13, 25)]

    CLIMATE_CHOICES = [
        ('none', _('No climate control')),
        ('ac', _('Air conditioning')),
        ('climate', _('Climate control')),
        ('dual_climate', _('Dual-zone climate control')),
        ('triple_climate', _('Triple-zone climate control')),
    ]

    MOTORCYCLE_TYPE_CHOICES = [
        ('sport', _('Sport')), ('cruiser', _('Cruiser')),
        ('touring', _('Touring')), ('enduro', _('Enduro')),
        ('motocross', _('Motocross')), ('chopper', _('Chopper')),
        ('naked', _('Naked')), ('scooter', _('Scooter')),
        ('moped', _('Moped')), ('atv', _('ATV / Quad')),
        ('trike', _('Trike')),
        # Nuomos vertikalė: etalone yra ir šitie trys
        ('kart', _('Kart')), ('mini_bike', _('Mini bike')),
        ('snowmobile', _('Snowmobile')),
        ('other', _('Other')),
    ]

    COOLING_TYPE_CHOICES = [
        ('air', _('Air-cooled')), ('water', _('Water-cooled')), ('oil', _('Oil-cooled')),
        ('mixed', _('Mixed cooling')),
    ]

    MOTO_ENGINE_TYPE_CHOICES = [
        ('single', _('Single-cylinder')), ('twin', _('Twin-cylinder')),
        ('parallel_twin', _('Parallel-twin')), ('v_twin', _('V-twin')),
        ('triple', _('Triple (3-cylinder)')), ('inline_4', _('Inline-4')),
        ('v4', _('V4')), ('boxer', _('Boxer')), ('other', _('Other')),
    ]

    GEAR_TYPE_CHOICES = [
        ('helmet', _('Helmet')),
        ('protective', _('Protective gear')),
        ('boots', _('Boots')),
        ('pants', _('Pants')),
        ('suit', _('Suit / Combination')),
        ('bag', _('Bag / Backpack')),
        ('gloves', _('Gloves')),
        ('jacket', _('Jacket')),
        ('other', _('Other')),
    ]

    # ═══ GEAR SUBTYPE — 'Other' first per gear_type ═══
    GEAR_SUBTYPE_CHOICES = [
        # Helmets
        ('helmet:other', _('Kita')),
        ('helmet:full_face', _('Uždaras (full face)')),
        ('helmet:integral', _('Integralinis')),
        ('helmet:modular', _('Atverčiamas (modular)')),
        ('helmet:open_face', _('Atviras (jet)')),
        ('helmet:off_road', _('Krosinis')),
        ('helmet:enduro', _('Enduro')),
        ('helmet:sport', _('Sportinis')),
        ('helmet:cruiser', _('Čioperistams')),
        ('helmet:dual_sport', _('Dual sport / kelioninis')),
        ('helmet:half', _('Pusinis')),
        # Jackets
        ('jacket:other', _('Kita')),
        ('jacket:sport', _('Sportinė')),
        ('jacket:touring', _('Kelioninė')),
        ('jacket:city', _('Miesto')),
        ('jacket:adventure', _('Adventure')),
        ('jacket:off_road', _('Krosinė')),
        ('jacket:cruiser', _('Čioperistams')),
        # Pants
        ('pants:other', _('Kita')),
        ('pants:sport', _('Sportinės')),
        ('pants:touring', _('Kelioninės')),
        ('pants:jeans', _('Džinsai')),
        ('pants:off_road', _('Krosinės')),
        ('pants:rain', _('Nuo lietaus')),
        # Suits
        ('suit:other', _('Kita')),
        ('suit:one_piece', _('Vientisas')),
        ('suit:two_piece', _('Dviejų dalių')),
        ('suit:rain', _('Nuo lietaus')),
        # Boots
        ('boots:other', _('Kita')),
        ('boots:sport', _('Sportiniai')),
        ('boots:classic', _('Klasikiniai')),
        ('boots:touring', _('Kelioniniai')),
        ('boots:off_road', _('Krosiniai')),
        ('boots:adventure', _('Adventure')),
        ('boots:urban', _('Miesto')),
        # Gloves
        ('gloves:other', _('Kita')),
        ('gloves:sport', _('Sportinės')),
        ('gloves:touring', _('Kelioninės')),
        ('gloves:off_road', _('Krosinės')),
        ('gloves:summer', _('Vasarinės')),
        ('gloves:winter', _('Žieminės / šildomos')),
        ('gloves:rain', _('Nuo lietaus')),
        # Bags
        ('bag:other', _('Kita')),
        ('bag:tank', _('Ant bako')),
        ('bag:tail', _('Ant sėdynės')),
        ('bag:saddle', _('Šoninės')),
        ('bag:backpack', _('Kuprinė')),
        ('bag:top_case', _('Bagažinė (top case)')),
        ('bag:roll', _('Ritininis')),
        # Protective gear
        ('protective:other', _('Kita')),
        ('protective:back', _('Nugaros apsauga')),
        ('protective:chest', _('Krūtinės apsauga')),
        ('protective:knee', _('Kelių apsaugos')),
        ('protective:elbow', _('Alkūnių apsaugos')),
        ('protective:neck', _('Kaklo apsauga')),
        ('protective:airbag', _('Oro pagalvės liemenė')),
    ]

    # ═══ GEAR SIZE — numeric first, then letters, 'Other' last ═══
    GEAR_SIZE_CHOICES = (
        [(str(n), str(n)) for n in range(34, 51)]
        + [(str(n), str(n)) for n in (52, 54, 56, 58, 60)]
        + [
            ('XXS', _('XXS')), ('XS', _('XS')),
            ('S', _('S')), ('M', _('M')),
            ('L', _('L')), ('XL', _('XL')),
            ('XXL', _('XXL')), ('XXXL', _('XXXL')),
            ('one_size', _('One size / Universal')),
            ('other', _('Other')),
        ]
    )

    # ═══ GEAR MATERIAL — 'Other' first ═══
    GEAR_MATERIAL_CHOICES = [
        ('other', _('Other')),
        ('leather', _('Leather')),
        ('textile', _('Textile')),
        ('mixed', _('Leather + Textile')),
        ('synthetic', _('Synthetic')),
        ('mesh', _('Mesh')),
        ('plastic', _('Plastic')),
        ('aluminium', _('Aluminium')),
    ]

    # ═══ GEAR GENDER — 'Other' first ═══
    GEAR_GENDER_CHOICES = [
        ('other', _('Other')),
        ('men', _('Men')),
        ('women', _('Women')),
        ('unisex', _('Unisex')),
        ('kids', _('Kids')),
    ]

    # ═══ GEAR SAFETY CERT — 'Other' first, 'None' second ═══
    GEAR_SAFETY_CERT_CHOICES = [
        ('other', _('Other')),
        ('none', _('No certification')),
        # Helmets
        ('ece_22_06', _('ECE 22.06')),
        ('ece_22_05', _('ECE 22.05')),
        ('dot', _('DOT (FMVSS 218)')),
        ('snell_m2020', _('Snell M2020')),
        ('snell_m2015', _('Snell M2015')),
        ('sharp_5', _('SHARP 5 stars')),
        ('sharp_4', _('SHARP 4 stars')),
        # Apparel CE
        ('ce_aaa', _('CE AAA (highest)')),
        ('ce_aa', _('CE AA')),
        ('ce_a', _('CE A')),
        ('ce_b', _('CE B')),
        ('ce_level_1', _('CE Level 1 (impact)')),
        ('ce_level_2', _('CE Level 2 (impact)')),
        ('en_certified', _('EN certified')),
    ]

    COUNTRY_CHOICES = [
        ('US', _('United States')), ('LT', _('Lithuania')),
        ('LV', _('Latvia')), ('EE', _('Estonia')),
        ('PL', _('Poland')), ('DE', _('Germany')),
        ('NL', _('Netherlands')), ('BE', _('Belgium')),
        ('FR', _('France')), ('IT', _('Italy')),
        ('ES', _('Spain')), ('AT', _('Austria')),
        ('CZ', _('Czech Republic')), ('SK', _('Slovakia')),
        ('HU', _('Hungary')), ('RO', _('Romania')),
        ('BG', _('Bulgaria')), ('SE', _('Sweden')),
        ('DK', _('Denmark')), ('FI', _('Finland')),
        ('NO', _('Norway')), ('GB', _('United Kingdom')),
        ('IE', _('Ireland')), ('CH', _('Switzerland')),
    ]

    US_STATE_CHOICES = [
        ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'),
        ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'),
        ('CT', 'Connecticut'), ('DE', 'Delaware'), ('FL', 'Florida'),
        ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'),
        ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'),
        ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'),
        ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'),
        ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'),
        ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'),
        ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'),
        ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'),
        ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'),
        ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'),
        ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'),
        ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'),
        ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'),
        ('WI', 'Wisconsin'), ('WY', 'Wyoming'),
    ]

    CURRENCY_CHOICES = [
        ('USD', 'US Dollar ($)'),
        ('EUR', 'Euro (€)'),
        ('GBP', 'British Pound (£)'),
    ]

    CURRENCY_SYMBOLS = {'USD': '$', 'EUR': '€', 'GBP': '£'}

    STAR_LEVEL_CHOICES = [
        (0, 'No Stars'),
        (1, '⭐ One Star (7 days)'),
        (2, '⭐⭐ Two Stars (30 days)'),
    ]

    STAR_DURATIONS = {1: 7, 2: 30}
    BOOST_COOLDOWN_HOURS = 1
    RENEWED_BADGE_HOURS = 48
    DEFAULT_ACTIVE_DAYS = 30
    EXPIRY_REMINDER_DAYS = 3
    POST_EXPIRY_REMINDER_INTERVAL_DAYS = 3
    AUTO_DELETE_AFTER_EXPIRY_DAYS = 160
    SOLD_DISPLAY_DAYS = 3

    PRICING_TIERS = [
        (5000, 5),
        (20000, 10),
        (float('inf'), 15),
    ]

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE, verbose_name=_("Vehicle Type"))

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name=_("Brand"), null=True, blank=True)
    model = models.ForeignKey(Model, on_delete=models.CASCADE, verbose_name=_("Model"), null=True, blank=True)
    submodel = models.ForeignKey(SubModel, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("SubModel"))

    motorcycle_brand = models.ForeignKey(
        MotorcycleBrand, on_delete=models.CASCADE,
        verbose_name=_("Motorcycle Brand"),
        null=True, blank=True, related_name='listings',
    )
    motorcycle_model = models.ForeignKey(
        MotorcycleModel, on_delete=models.CASCADE,
        verbose_name=_("Motorcycle Model"),
        null=True, blank=True, related_name='listings',
    )
    truck_brand = models.ForeignKey(
        TruckBrand, on_delete=models.CASCADE,
        verbose_name=_("Truck Brand"),
        null=True, blank=True, related_name='listings',
    )
    truck_model = models.ForeignKey(
        TruckModel, on_delete=models.CASCADE,
        verbose_name=_("Truck Model"),
        null=True, blank=True, related_name='listings',
    )
    truck_model_text = models.CharField(
        max_length=100, blank=True,
        verbose_name=_("Truck Model (free text)"),
        help_text="User-typed model name (e.g. 'FH16', 'Actros 1845')",
    )

    # ═══════════════════════════════════════════════════════════
    # TRUCK-SPECIFIC FIELDS (autoplius.lt 8x4 layout)
    # ═══════════════════════════════════════════════════════════

    wheel_formula = models.CharField(
        max_length=10, choices=WHEEL_FORMULA_CHOICES, blank=True,
        verbose_name=_('Wheel formula'),
    )
    mass_interval = models.CharField(
        max_length=20, choices=MASS_INTERVAL_CHOICES, blank=True,
        verbose_name=_('Mass interval'),
    )
    front_suspension = models.CharField(
        max_length=20, choices=TRUCK_SUSPENSION_CHOICES, blank=True,
        verbose_name=_('Front suspension'),
    )
    rear_suspension = models.CharField(
        max_length=20, choices=TRUCK_SUSPENSION_CHOICES, blank=True,
        verbose_name=_('Rear suspension'),
    )
    truck_length_mm = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(99999)],
        verbose_name=_('Length (mm)'),
    )
    truck_width_mm = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(99999)],
        verbose_name=_('Width (mm)'),
    )
    truck_height_mm = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(99999)],
        verbose_name=_('Height (mm)'),
    )
    truck_volume_m3 = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True,
        verbose_name=_('Volume (m³)'),
    )
    gross_weight_kg = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(999999)],
        verbose_name=_('Gross weight (kg)'),
    )
    payload_kg = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(999999)],
        verbose_name=_('Payload capacity (kg)'),
    )
    fuel_tank_capacity_l = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(9999)],
        verbose_name=_('Fuel tank capacity (L)'),
    )
    sleeping_seats = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        verbose_name=_('Sleeping seats'),
    )
    sdk_number = models.CharField(
        max_length=50, blank=True,
        verbose_name=_('SDK number'),
        help_text='Self-Declared Conformity number (Regitra)',
    )

    BOAT_TYPE_CHOICES = [
        ('jet_ski', _('Jet Ski / Personal watercraft')),
        ('kayak_canoe', _('Kayak / Canoe')),
        ('surfboard', _('Surfboard / Windsurf')),
        ('yacht', _('Yacht')),
        ('motorboat', _('Motorboat / Cabin cruiser')),
        ('boat', _('Boat / Ship')),
        ('dinghy_raft', _('Dinghy / Raft')),
        ('engine', _('Boat engine')),
        ('other', _('Other')),
    ]
    boat_type = models.CharField(max_length=20, choices=BOAT_TYPE_CHOICES, blank=True, verbose_name=_('Boat type'))
    boat_make_text = models.CharField(max_length=120, blank=True, default='')
    boat_model_text = models.CharField(max_length=120, blank=True, default='')
    boat_material = models.CharField(max_length=40, blank=True, default='')
    boat_length_m = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    boat_width_m = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    boat_engine_count = models.PositiveSmallIntegerField(null=True, blank=True)
    BOAT_ENGINE_TYPE_CHOICES = [
        ('petrol_4stroke_outboard', _('Petrol 4-stroke outboard')),
        ('petrol_4stroke_inboard', _('Petrol 4-stroke inboard')),
        ('diesel_inboard', _('Diesel inboard')),
        ('electric', _('Electric')),
        ('none', _('No engine')),
        ('petrol_2stroke_outboard', _('Petrol 2-stroke outboard')),
        ('petrol_2stroke_inboard', _('Petrol 2-stroke inboard')),
    ]
    boat_engine_type = models.CharField(max_length=30, choices=BOAT_ENGINE_TYPE_CHOICES, blank=True, verbose_name=_('Boat engine type'))
    boat_fuel_tank_l = models.DecimalField(max_digits=7, decimal_places=1, null=True, blank=True, verbose_name=_('Fuel tank capacity (L)'))
    boat_liftable_engine = models.BooleanField(default=False, verbose_name=_('Liftable engine'))
    boat_propeller = models.BooleanField(default=False, verbose_name=_('Propeller'))
    boat_water_turbine = models.BooleanField(default=False, verbose_name=_('Water turbine'))

    # ═══════════════════════════════════════════════════════════
    # TRAILERS — Priekabos / Puspriekabės (vehicle_type slug='trailers')
    # Matmenys, masės, tūris, TA, spalva, VIN, SDK, Euro — imami iš
    # bendrų / truck_* laukų aukščiau; čia tik tai, ko niekur nėra.
    # Ypatumai (25) saugomi kaip Equipment eilutės, kategorija 'trailer_*'.
    # ═══════════════════════════════════════════════════════════
    TRAILER_KIND_CHOICES = [
        ('trailer', _('Priekaba')),
        ('semi_trailer', _('Puspriekabė')),
        ('light_car_trailer', _('Lengvojo automobilio priekaba')),
    ]

    # Paskirtis — 22 reikšmės (autogidas.lt). subcategory išvedama iš šito,
    # žr. TRAILER_PURPOSE_TO_SUBCATEGORY (trailers_views.py).
    TRAILER_PURPOSE_CHOICES = [
        ('car_trailer', _('Automobilinė priekaba')),
        ('for_car_transport', _('Automobiliui vežti')),
        ('car_carrier', _('Automobilvežio')),
        ('concrete_mixer', _('Betonvežio')),
        ('flatbed', _('Bortinė')),
        ('flatbed_tarpaulin', _('Bortinė su tentu')),
        ('tanker', _('Cisterninė')),
        ('livestock', _('Gyvuliams vežti')),
        ('insulated_body', _('Izoterminis kėbulas')),
        ('swap_body', _('Keičiamas kėbulas')),
        ('container_chassis', _('Konteinerių važiuoklė')),
        ('cargo', _('Krovininė')),
        ('logging', _('Miškavežio')),
        ('motorcycle_trailer', _('Motociklų priekabos')),
        ('platform', _('Platforma')),
        ('refrigerator', _('Šaldytuvas')),
        ('tipper', _('Savivartė')),
        ('tarpaulin', _('Tentinė')),
        ('tractor_trailer', _('Traktoriaus priekaba')),
        ('touring', _('Turistinė')),
        ('watercraft', _('Vandens transporto')),
        ('other', _('Kita')),
    ]

    TRAILER_AXLE_COUNT_CHOICES = [
        ('1', _('1 ašis')),
        ('2', _('2 ašys')),
        ('3', _('3 ašys')),
        ('3plus', _('>3 ašių')),
        ('other', _('Kitas')),
    ]

    TRAILER_SUSPENSION_CHOICES = [
        ('mechanical', _('Mechaninė')),
        ('pneumatic', _('Pneumatinė')),
        ('pneumatic_liftable', _('Pneumatinė (pakeliama)')),
    ]

    trailer_kind = models.CharField(
        max_length=20, choices=TRAILER_KIND_CHOICES, blank=True, default='',
        verbose_name=_('Tipas'),
    )
    trailer_purpose = models.CharField(
        max_length=40, choices=TRAILER_PURPOSE_CHOICES, blank=True, default='',
        verbose_name=_('Paskirtis'),
    )
    trailer_brand_text = models.CharField(
        max_length=80, blank=True, default='', verbose_name=_('Markė'),
    )
    trailer_model_text = models.CharField(
        max_length=80, blank=True, default='', verbose_name=_('Modelis'),
    )
    trailer_wheel_count = models.CharField(
        max_length=8, blank=True, default='',
        verbose_name=_('Bendras ratų skaičius'),
        help_text="'2'-'13' arba '13plus'",
    )
    trailer_axle_make = models.CharField(
        max_length=40, blank=True, default='', verbose_name=_('Ašys (gamintojas)'),
    )
    trailer_axle_count = models.CharField(
        max_length=12, choices=TRAILER_AXLE_COUNT_CHOICES, blank=True, default='',
        verbose_name=_('Ašių skaičius'),
    )

    # ─── Pakaba ir padangos — po bloką kiekvienai iš 3 ašių ───
    trailer_susp_1 = models.CharField(max_length=20, choices=TRAILER_SUSPENSION_CHOICES, blank=True, default='', verbose_name=_('1 ašies pakabos tipas'))
    trailer_tyre_pct_1 = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name=_('1 ašies padangų likutis %'))
    trailer_tyre_size_1 = models.CharField(max_length=40, blank=True, default='', verbose_name=_('1 ašies padangų išmatavimai'))

    trailer_susp_2 = models.CharField(max_length=20, choices=TRAILER_SUSPENSION_CHOICES, blank=True, default='', verbose_name=_('2 ašies pakabos tipas'))
    trailer_tyre_pct_2 = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name=_('2 ašies padangų likutis %'))
    trailer_tyre_size_2 = models.CharField(max_length=40, blank=True, default='', verbose_name=_('2 ašies padangų išmatavimai'))

    trailer_susp_3 = models.CharField(max_length=20, choices=TRAILER_SUSPENSION_CHOICES, blank=True, default='', verbose_name=_('3 ašies pakabos tipas'))
    trailer_tyre_pct_3 = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name=_('3 ašies padangų likutis %'))
    trailer_tyre_size_3 = models.CharField(max_length=40, blank=True, default='', verbose_name=_('3 ašies padangų išmatavimai'))

    # ═══════════════════════════════════════════════════════════
    # ŽEMĖS ŪKIO TECHNIKA (vehicle_type slug='agriculture')
    # Metai/mėnuo, kaina, SDK, galia (kW), masės, tūris, komentarai —
    # imami iš bendrų / truck_* laukų aukščiau. Čia tik tai, ko niekur nėra.
    # Ypatumai (9) saugomi kaip Equipment eilutės, kategorija 'agri_*'.
    # ═══════════════════════════════════════════════════════════
    AGRI_TYPE_CHOICES = [
        ('akecios', _('Akėčios')),
        ('bulviu_kasamosios', _('Bulvių kasamosios')),
        ('buldozeris', _('Buldozeris')),
        ('ekskavatorius', _('Ekskavatorius')),
        ('greideris', _('Greideris')),
        ('grudu_valymo_iranga', _('Grūdų valymo įranga')),
        ('grudu_dziovinimo_iranga', _('Grūdų džiovinimo įranga')),
        ('grudu_sandeliavimo_iranga', _('Grūdų sandėliavimo įranga')),
        ('grudu_transportavimo_iranga', _('Grūdų transportavimo įranga')),
        ('kombainas', _('Kombainas')),
        ('krautuvas', _('Krautuvas')),
        ('kultivatorius', _('Kultivatorius')),
        ('manipuliatorius', _('Manipuliatorius')),
        ('mini_ekskavatorius', _('Mini ekskavatorius')),
        ('motoblokas', _('Motoblokas')),
        ('traktorius', _('Traktorius')),
        ('zoliapjove', _('Žoliapjovė')),
        ('grebliai', _('Grėbliai')),
        ('lekstiniai_skutikai', _('Lėkštiniai skutikai')),
        ('meslo_kratytuvai', _('Mėšlo kratytuvai')),
        ('pasaru_dalytuvai', _('Pašarų dalytuvai')),
        ('pienininkystes_ir_fermu_irengimai', _('Pienininkystės ir fermų įrengimai')),
        ('pjaunamosios', _('Pjaunamosios')),
        ('plugai', _('Plūgai')),
        ('presai', _('Presai')),
        ('purkstuvai_pakabinami', _('Purkštuvai pakabinami')),
        ('purkstuvai_prikabinami', _('Purkštuvai prikabinami')),
        ('razieniniai_skutikai', _('Ražieniniai skutikai')),
        ('rinktuvai', _('Rinktuvai')),
        ('savaeiges_pjaunamosios_smulkintuvai', _('Savaeigės pjaunamosios-smulkintuvai')),
        ('sejamosios', _('Sėjamosios')),
        ('sejos_agregatai', _('Sėjos agregatai')),
        ('smulkintuvai_pjaunamosios', _('Smulkintuvai-pjaunamosios')),
        ('sniego_peilis', _('Sniego peilis')),
        ('sodo_ir_parko_technika', _('Sodo ir parko technika')),
        ('srutu_laistytuvai', _('Srutų laistytuvai')),
        ('srutu_siurbliai', _('Srutų siurbliai')),
        ('trasu_barstytuvai', _('Trąšų barstytuvai')),
        ('vartytuvai', _('Vartytuvai')),
        ('volai', _('Volai')),
        ('vyniotuvai', _('Vyniotuvai')),
        ('kita', _('Kita')),
    ]

    AGRI_KIND_CHOICES = [
        ('implement', _('Padargas')),
        ('self_propelled', _('Savaeigė')),
    ]

    agri_type = models.CharField(
        max_length=40, choices=AGRI_TYPE_CHOICES, blank=True, default='',
        verbose_name=_('Tipas'),
    )
    agri_kind = models.CharField(
        max_length=20, choices=AGRI_KIND_CHOICES, blank=True, default='',
        verbose_name=_('Padargas / Savaeigė'),
    )
    agri_brand_text = models.CharField(
        max_length=80, blank=True, default='', verbose_name=_('Markė'),
    )
    agri_model_text = models.CharField(
        max_length=20, blank=True, default='', verbose_name=_('Modelis'),
    )
    engine_hours = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(999999)],
        verbose_name=_('Motovalandos'),
    )
    working_width_m = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        verbose_name=_('Darbinis plotis (m)'),
    )

    # ═══════════════════════════════════════════════════════════
    # STATYBINĖ TECHNIKA (vehicle_type slug='construction')
    # Dvi subkategorijos = dvi skirtingos formos:
    #   construction-machinery   → constr_type (39)
    #   construction-attachments → constr_attach_type (23), be markės
    # Galia, rida, kuro tipas, ratų formulė, bakas, svoriai, motovalandos —
    # imami iš esamų laukų. Matmenys metrais (length_m/width_m/height_m)
    # nauji: truck_*_mm yra milimetrai, sumaišius vienetus diapazono
    # filtrai lygintų metrus su milimetrais.
    # Ypatumų ši kategorija neturi (0 checkbox'ų).
    # ═══════════════════════════════════════════════════════════
    CONSTR_TYPE_CHOICES = [
        ('akmens_smulkinimo_masina', _('Akmens smulkinimo mašina')),
        ('asenizacine_masina', _('Asenizacinė mašina')),
        ('asfaloto_klojimo_masinos', _('Asfaloto klojimo mašinos')),
        ('automobilinis_bokstelis', _('Automobilinis bokštelis')),
        ('automobilinis_kranas', _('Automobilinis kranas')),
        ('automobilinis_krautuvas', _('Automobilinis krautuvas')),
        ('betono_gamybos_irenginys', _('Betono gamybos įrenginys')),
        ('betonvezis', _('Betonvežis')),
        ('buldozeris', _('Buldozeris')),
        ('dumperis_savivartis', _('Dumperis (savivartis)')),
        ('ekskavatorius_krautuvas', _('Ekskavatorius krautuvas')),
        ('ekskavatorius_griovimo', _('Ekskavatorius griovimo')),
        ('ekskavatorius_ratinis', _('Ekskavatorius ratinis')),
        ('ekskavatorius_viksrinis', _('Ekskavatorius vikšrinis')),
        ('frontalinis_krautuvas', _('Frontalinis krautuvas')),
        ('greideris', _('Greideris')),
        ('griebtuvas', _('Griebtuvas')),
        ('hidraulines_zirkles', _('Hidraulinės žirklės')),
        ('hidraulinis_graztas', _('Hidraulinis grąžtas')),
        ('hidraulinis_kujis', _('Hidraulinis kūjis')),
        ('kausinis_krautuvas', _('Kaušinis krautuvas')),
        ('kelkrasciu_prieziuros_masinos', _('Kelkraščių priežiūros mašinos')),
        ('keliu_tiesimo_masina', _('Kelių tiesimo mašina')),
        ('kompresorius', _('Kompresorius')),
        ('kranas', _('Kranas')),
        ('manipuliatorius', _('Manipuliatorius')),
        ('mini_ekskavatorius', _('Mini ekskavatorius')),
        ('mini_krautuvas', _('Mini krautuvas')),
        ('poliakales', _('Poliakalės')),
        ('skaldykle', _('Skaldyklė')),
        ('skaldos_rusiavimo_masina', _('Skaldos rūšiavimo mašina')),
        ('tankinimo_technika', _('Tankinimo technika')),
        ('vibracines_plokstes', _('Vibracinės plokštės')),
        ('vibrovolai', _('Vibrovolai')),
        ('volai', _('Volai')),
        ('zirklinis_keltuvas', _('Žirklinis keltuvas')),
        ('zirklinis_krautuvas', _('Žirklinis krautuvas')),
        ('vibro_masina', _('Vibro mašina')),
        ('kitas', _('Kitas')),
    ]

    CONSTR_ATTACH_TYPE_CHOICES = [
        ('a_barstytuvai', _('Barstytuvai')),
        ('a_betono_maisykles', _('Betono maišyklės')),
        ('a_asfalto_frezos', _('Asfalto frezos')),
        ('a_gerves_kabliai', _('Gervės / kabliai')),
        ('a_greideriai', _('Greideriai')),
        ('a_griebtuvai', _('Griebtuvai')),
        ('a_hidraulines_zirkles', _('Hidraulinės žirklės')),
        ('a_hidrauliniai_kujai', _('Hidrauliniai kūjai')),
        ('a_hidrauliniai_graztai', _('Hidrauliniai gražtai')),
        ('a_kausai', _('Kaušai')),
        ('a_kelimo_platformos', _('Kėlimo platformos')),
        ('a_kranai_manipuliatoriai', _('Kranai / manipuliatoriai')),
        ('a_paleciu_sakes', _('Palečių šakės')),
        ('a_sniego_buldozerio_peiliai', _('Sniego (buldozerio) peiliai')),
        ('a_sniego_putikai', _('Sniego pūtikai')),
        ('a_pjuklai', _('Pjūklai')),
        ('a_sijotuvai', _('Sijotuvai')),
        ('a_streles', _('Strėlės')),
        ('a_sluotos_sepeciai', _('Šluotos / šepečiai')),
        ('a_trupintuvai_smulkintuvai', _('Trupintuvai / smulkintuvai')),
        ('a_viksrai', _('Vikšrai')),
        ('a_volai', _('Volai')),
        ('a_kita', _('Kita')),
    ]

    # Bendras pavaros laukas statybinei ir krovimo technikai.
    # Krovimo technika prideda dvi hidraulines pavaras; jos prasmingos ir
    # statybinėje (mini krautuvai, ekskavatoriai).
    CONSTR_DRIVE_TYPE_CHOICES = [
        ('d_hidrauline_2_ratu', _('Hidraulinė–2 ratų')),
        ('d_hidrauline_4x4', _('Hidraulinė–4x4')),
        ('d_mechanine', _('Mechaninė')),
        ('d_automatine', _('Automatinė')),
        ('d_elektromechanine', _('Elektromechaninė')),
        ('d_hidrodinamine', _('Hidrodinaminė')),
        ('d_hidrostatine', _('Hidrostatinė')),
        ('d_kita', _('Kita')),
    ]

    constr_type = models.CharField(
        max_length=48, choices=CONSTR_TYPE_CHOICES, blank=True, default='',
        verbose_name=_('Tipas'),
    )
    constr_attach_type = models.CharField(
        max_length=48, choices=CONSTR_ATTACH_TYPE_CHOICES, blank=True, default='',
        verbose_name=_('Priedo tipas'),
    )
    constr_brand_text = models.CharField(
        max_length=80, blank=True, default='', verbose_name=_('Markė'),
    )
    constr_model_text = models.CharField(
        max_length=32, blank=True, default='', verbose_name=_('Modelis'),
    )
    constr_drive_type = models.CharField(
        max_length=24, choices=CONSTR_DRIVE_TYPE_CHOICES, blank=True, default='',
        verbose_name=_('Pavaros tipas'),
    )

    # Generiniai matmenys metrais — tinka ir kitoms kategorijoms
    length_m = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name=_('Ilgis (m)'))
    width_m = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name=_('Plotis (m)'))
    height_m = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name=_('Aukštis (m)'))

    # ═══════════════════════════════════════════════════════════
    # KROVIMO IR SANDĖLIAVIMO TECHNIKA (slug='loading-equipment')
    # Kategorija subkategorijų NETURI (etalone plokščias punktas), todėl
    # subcategory lieka NULL — subkategorijos išvedimo logikos nėra.
    # Matmenys — truck_*_mm (MILIMETRAI), skirtingai nei statybinėje,
    # kur length_m/width_m/height_m yra metrai.
    # Max keliamoji galia = payload_kg. Pavara = bendras constr_drive_type.
    # Ypatumai (15) — Equipment su 'load_*' prefiksu: „Hidraulika" ir
    # „Kabina" jau egzistuoja agri_other / trailer_body.
    # ═══════════════════════════════════════════════════════════
    LOAD_TYPE_CHOICES = [
        ('l_konteineriai', _('Konteineriai')),
        ('l_alkuninis_keltuvas', _('Alkūninis keltuvas')),
        ('l_ekskavatorinis_krautuvas', _('Ekskavatorinis krautuvas')),
        ('l_elektriniai_vezimeliai', _('Elektriniai vežimėliai')),
        ('l_krautuvas', _('Krautuvas')),
        ('l_paleciu_vyniotuvai', _('Palečių vyniotuvai')),
        ('l_sandeliavimo_technika', _('Sandėliavimo technika')),
        ('l_savaeigis_stiebinis_keltuvas', _('Savaeigis stiebinis keltuvas')),
        ('l_savaeigis_zirklinis_keltuvas', _('Savaeigis žirklinis keltuvas')),
        ('l_sakinis_krautuvas', _('Šakinis krautuvas')),
        ('l_teleskopinis_krautuvas', _('Teleskopinis krautuvas')),
        ('l_universalus_krautuvas', _('Universalus krautuvas')),
        ('l_kita', _('Kita')),
    ]

    LOAD_ENERGY_CHOICES = [
        ('e_akumuliatorinis_elektrinis', _('Akumuliatorinis/elektrinis')),
        ('e_benzininis_dujinis', _('Benzininis/dujinis')),
        ('e_benzininis', _('Benzininis')),
        ('e_dyzelininis_elektrinis', _('Dyzelininis/elektrinis')),
        ('e_dyzelininis', _('Dyzelininis')),
        ('e_dujinis', _('Dujinis')),
        ('e_rankinis_hidraulinis', _('Rankinis/hidraulinis')),
        ('e_rankinis', _('Rankinis')),
        ('e_kita', _('Kita')),
    ]

    load_type = models.CharField(
        max_length=40, choices=LOAD_TYPE_CHOICES, blank=True, default='',
        verbose_name=_('Tipas'),
    )
    load_brand_text = models.CharField(
        max_length=80, blank=True, default='', verbose_name=_('Markė'),
    )
    load_energy_source = models.CharField(
        max_length=32, choices=LOAD_ENERGY_CHOICES, blank=True, default='',
        verbose_name=_('Energijos šaltinis'),
    )
    lift_height_m = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        verbose_name=_('Max kėlimo aukštis (m)'),
    )
    aisle_width_m2 = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True,
        verbose_name=_('Kelplotis (m²)'),
    )
    fork_length_m = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        verbose_name=_('Šakių / strėlės ilgis (m)'),
    )

    # ═══════════════════════════════════════════════════════════
    # MIŠKO ŪKIO TECHNIKA (vehicle_type slug='forestry')
    # Nauji tik du laukai — visa kita perpanaudota: pavaros tipas
    # (constr_drive_type), modelis (constr_model_text), matmenys metrais
    # (length_m/width_m/height_m), ratų formulė, kuro tipas, galia,
    # motovalandos, masės, TA, VIN.
    # Kategorija NETURI nei subkategorijų, nei ypatumų, nei mėnesio lauko.
    # ═══════════════════════════════════════════════════════════
    FOREST_TYPE_CHOICES = [
        ('f_kitas', _('Kitas')),
        ('f_gerve', _('Gervė')),
        ('f_kapokle', _('Kapoklė')),
        ('f_krumapjove', _('Krūmapjovė')),
        ('f_manipuliatorius', _('Manipuliatorius')),
        ('f_medkirte', _('Medkirtė')),
        ('f_medveze', _('Medvežė')),
        ('f_misko_traktorius', _('Miško traktorius')),
        ('f_miskovezio_priekaba', _('Miškovežio priekaba')),
        ('f_miskovezio_puspriekabe', _('Miškovežio puspriekabė')),
        ('f_miskovezis', _('Miškovežis')),
        ('f_motorinis_pjuklas', _('Motorinis pjūklas')),
        ('f_pjovimo_galvute', _('Pjovimo galvutė')),
        ('f_savikrove_misko_priekaba', _('Savikrovė Miško priekaba')),
        ('f_medienos_smulkintuvas', _('Medienos smulkintuvas')),
    ]

    forest_type = models.CharField(
        max_length=40, choices=FOREST_TYPE_CHOICES, blank=True, default='',
        verbose_name=_('Tipas'),
    )
    forest_brand_text = models.CharField(
        max_length=80, blank=True, default='', verbose_name=_('Markė'),
    )

    # ═══════════════════════════════════════════════════════════
    # TURISTINIAI NAMELIAI (vehicle_type slug='camping-houses')
    # Ši kategorija artimesnė AUTOMOBILIAMS nei technikai: rida, spalva,
    # pavarų dėžė, varantieji ratai, darbinis tūris, defektai, ratlankiai,
    # sėdimos/miegamos vietos — visa tai jau egzistuoja ir perpanaudojama.
    # Nauji tik penki laukai.
    #
    # „Tinka su B kat. teisėmis" yra LAUKAS, ne ypatumas — jis filtruojamas
    # ir greitojoje panelėje, ir išplėstinėje.
    # ═══════════════════════════════════════════════════════════
    CAMP_TYPE_CHOICES = [
        ('touring_car', _('Turistinis automobilis')),
        ('towed_house', _('Prikabinamas namelis')),
        ('other', _('Kita')),
    ]

    camp_type = models.CharField(
        max_length=20, choices=CAMP_TYPE_CHOICES, blank=True, default='',
        verbose_name=_('Tipas'),
    )
    camp_brand_text = models.CharField(
        max_length=80, blank=True, default='', verbose_name=_('Markė'),
    )
    b_licence_ok = models.BooleanField(
        default=False, verbose_name=_('Tinka su B kat. teisėmis'),
    )
    # `gear_*` prefiksas jau užimtas motociklų aprangos (gear_type, gear_size...)
    gearbox_speeds = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(20)],
        verbose_name=_('Pavarų skaičius'),
    )
    # Bendras padangų likutis; trailer_tyre_pct_1..3 yra priekabų ašims
    tyre_condition_pct = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_('Padangų likutis %'),
    )

    # ═══════════════════════════════════════════════════════════
    # TRANSPORTO NUOMA (vehicle_type slug='rental', 5 subkategorijos)
    #
    # „Nuomos kaina parai" saugoma bendrame `price` lauke — ji privaloma
    # visose penkiose etalono sekcijose, todėl kortelės, rikiavimas ir
    # kainos diapazono filtras veikia be atskiro stulpelio. Valandinė
    # kaina neprivaloma, todėl jai reikia savo lauko.
    #
    # Sėdimoms vietoms NEUŽTENKA `seats` (CharField, choices iki „9+"):
    # etalone tai diapazono filtras iki 25, o diapazonas ant CharField
    # lygintų leksikografiškai („10" < „9").
    # ═══════════════════════════════════════════════════════════
    RENT_TYPE_CHOICES = [
        # sec 33 — Mikroautobusų, turistinio, vandens transporto nuoma
        ('bus', _('Autobusas')),
        ('water', _('Vandens transportas')),
        ('moto_rental', _('Motociklų nuoma')),
        ('passenger_minibus', _('Keleivinis mikroautobusas')),
        ('cargo_minibus', _('Krovininis mikroautobusas')),
        ('towed_house', _('Prikabinamas namelis')),
        ('touring_car', _('Turistinis automobilis')),
        # sec 34 — Sunkiojo transporto, priekabų nuoma
        ('road_train', _('Autotraukinys')),
        ('agri_constr', _('Žemės ūkio, statybos transportas')),
        ('truck', _('Sunkvežimis')),
        ('tractor_unit', _('Vilkikas')),
        ('warehouse', _('Sandėliavimo, krovimo technika')),
        ('trailer', _('Priekaba')),
    ]
    rent_type = models.CharField(
        max_length=20, choices=RENT_TYPE_CHOICES, blank=True, default='',
        verbose_name=_('Tipas'),
    )
    rent_brand_text = models.CharField(
        max_length=80, blank=True, default='', verbose_name=_('Markė'),
    )
    rent_price_hour = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        verbose_name=_('Nuomos kaina valandai'),
    )
    seats_count = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(99)],
        verbose_name=_('Sėdimų vietų skaičius'),
    )
    metallic = models.BooleanField(default=False, verbose_name=_('Metalikas'))

    # ═══════════════════════════════════════════════════════════
    # PASLAUGOS (vehicle_type slug='services')
    #
    # Plokščia kategorija: etalone subkategorijų nėra, todėl subcategory
    # lieka NULL, o pikeris veda tiesiai į formą (CREATE_URL_BY_VEHICLE_TYPE).
    #
    # Pavadinimą čia rašo pats vartotojas (kitose kategorijose jis
    # generuojamas iš markės + modelio + metų), o kaina NEPRIVALOMA —
    # tuščia išsaugoma kaip 0 ir rodoma „Sutartinė kaina".
    #
    # 18 paslaugų varnelių saugomos kaip Equipment eilutės ('svc_*').
    # Etalono filtruose jų nėra, todėl į paieškos konfigūraciją neįtrauktos.
    # ═══════════════════════════════════════════════════════════
    SERVICE_TYPE_CHOICES = [
        ('alarm_install', _('Apsaugos sistemų montavimas')),
        ('car_buying', _('Automobilių supirkimas')),
        ('service_equipment', _('Autoservisų įrangos aptarnavimas')),
        ('parts_buying', _('Dalių supirkimas')),
        ('lpg_install', _('Dujų įrangos montavimas')),
        ('audio_install', _('Garso aparatūros montavimas')),
        ('catalyst_buying', _('Katalizatorių supirkimas')),
        ('passenger_transport', _('Keleivių vežimas')),
        ('other_services', _('Kitos paslaugos')),
        ('cargo_transport', _('Krovinių gabenimas')),
        ('car_repair', _('Lengvųjų automobilių remontas')),
        ('moto_repair', _('Motociklų motorolerių remontas')),
        ('moto_buying', _('Motociklų supirkimas')),
        ('tyre_buying', _('Padangų supirkimas')),
        ('roadside_assistance', _('Pagalba kelyje')),
        ('washing', _('Plovimo paslaugos')),
        ('rim_buying', _('Ratlankių supirkimas')),
        ('tyre_service', _('Ratų montavimas, padangų remontas')),
        ('glass_tinting', _('Stiklų tonavimas, keitimas')),
        ('heavy_repair', _('Sunkiosios technikos remontas')),
        ('truck_buying', _('Sunkvežimių supirkimas')),
        ('tuning', _('Tiuning')),
        ('agri_buying', _('Žemės ūkio technikos supirkimas')),
        ('agri_repair', _('Žemės ūkio technikos remontas')),
    ]
    service_type = models.CharField(
        max_length=25, choices=SERVICE_TYPE_CHOICES, blank=True, default='',
        verbose_name=_('Paslaugos tipas'),
    )

    # ═══════════════════════════════════════════════════════════
    # VIDEO, AUDIO, NAVIGACIJOS (vehicle_type slug='electronics')
    #
    # Plokščia kategorija, subcategory lieka NULL. Pavadinimo lauko
    # etalone nėra — generuojam iš gamintojo, modelio ir tipo.
    #
    # `power_w` atskiras nuo `power` SĄMONINGAI: `power` visose kitose
    # kategorijose yra kW, o čia — vatai. Sudėjus į vieną stulpelį
    # diapazono filtras lygintų 50 W su 50 kW (ta pati klaida kaip
    # metrai vs milimetrai, žr. SKILL.md).
    #
    # Ypatumai (16) — Equipment eilutės su 'elec_' prefiksu. Dėmesio:
    # 'electronics' jau yra AUTOMOBILIŲ ypatumų kategorija, bet
    # startswith('elec_') jos nepagauna, todėl izoliacija veikia.
    # ═══════════════════════════════════════════════════════════
    ELEC_TYPE_CHOICES = [
        ('car_alarm', _('Automobilių signalizacija')),
        ('cd_player', _('CD grotuvas')),
        ('cd_changer', _('CD keitiklis')),
        ('cd_mp3_player', _('CD/MP3 grotuvas')),
        ('dvd_player', _('DVD grotuvas')),
        ('speaker', _('Garsiakalbis')),
        ('amplifier', _('Garso stiprintuvas')),
        ('player_with_nav', _('Grotuvas su navigacija')),
        ('capacitors', _('Kondensatoriai')),
        ('cables', _('Laidai/Laidų komplektai')),
        ('monitors', _('Monitoriai')),
        ('mc_radio', _('MC automagnetola')),
        ('moto_alarm', _('Motociklų signalizacija')),
        ('multimedia', _('Multimedia')),
        ('agri_navigation', _('Navigacija žemės ūkio technikai')),
        ('navigation_gps', _('Navigacija, GPS')),
        ('parking_system', _('Parkavimo sistema')),
        ('cb_radio', _('Radijas/CB radijo stotelės')),
        ('dashcam', _('Video registratorius')),
        ('subwoofer', _('Žemų dažnių garsiakalbis')),
        ('other', _('Kita')),
    ]
    elec_type = models.CharField(
        max_length=20, choices=ELEC_TYPE_CHOICES, blank=True, default='',
        verbose_name=_('Tipas'),
    )
    elec_brand_text = models.CharField(
        max_length=80, blank=True, default='', verbose_name=_('Gamintojas'),
    )
    elec_channels = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(6)],
        verbose_name=_('Kanalų skaičius'),
    )
    # Vatai — NE kilovatai; žr. komentarą aukščiau
    power_w = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(0)],
        verbose_name=_('Galingumas W'),
    )

    # ═══════════════════════════════════════════════════════════
    # EL. PASPIRTUKAI, RIEDŽIAI, DVIRAČIAI (vehicle_type slug='bicycles')
    #
    # Pikeris veda tiesiai į formą (etalone subkategorijų žingsnio nėra),
    # bet subkategorija IŠVEDAMA IŠ FORMOS lauko `bike_type`:
    # paspirtukas → electric-scooters, dviratis → electric-bikes.
    # „Elektrinis riedis" atitikmens DB neturi, todėl jam lieka NULL.
    #
    # Perpanaudota, nes vienetai sutampa: Galia W → power_w (tas pats
    # stulpelis kaip video/audio kategorijoje), Svoris kg → curb_weight,
    # Maks. apkrova kg → payload_kg.
    # ═══════════════════════════════════════════════════════════
    BIKE_TYPE_CHOICES = [
        ('e_scooter', _('Elektrinis paspirtukas')),
        ('e_board', _('Elektrinis riedis')),
        ('e_bike', _('Elektrinis dviratis')),
    ]
    TYRE_KIND_CHOICES = [
        ('solid', _('Pilnavidurės')),
        ('pneumatic', _('Pripučiamos')),
    ]
    bike_type = models.CharField(
        max_length=15, choices=BIKE_TYPE_CHOICES, blank=True, default='',
        verbose_name=_('Tipas'),
    )
    bike_brand_text = models.CharField(
        max_length=80, blank=True, default='', verbose_name=_('Gamintojas'),
    )
    max_speed_kmh = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(200)],
        verbose_name=_('Maksimalus greitis, km/h'),
    )
    range_km = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(0)],
        verbose_name=_('Rida su vienu įkrovimu, km'),
    )
    battery_ah = models.DecimalField(
        max_digits=6, decimal_places=1, null=True, blank=True,
        validators=[MinValueValidator(0)],
        verbose_name=_('Baterijos talpa, Ah'),
    )
    battery_pct = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_('Baterijos talpos likutis, %'),
    )
    charge_time_h = models.DecimalField(
        max_digits=5, decimal_places=1, null=True, blank=True,
        validators=[MinValueValidator(0)],
        verbose_name=_('Įkrovimo laikas, val.'),
    )
    tyre_kind = models.CharField(
        max_length=10, choices=TYRE_KIND_CHOICES, blank=True, default='',
        verbose_name=_('Padangų tipas'),
    )
    wheel_diameter_in = models.DecimalField(
        max_digits=4, decimal_places=1, null=True, blank=True,
        validators=[MinValueValidator(0)],
        verbose_name=_('Ratų skersmuo, coliais'),
    )
    max_incline_deg = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(90)],
        verbose_name=_('Įveikiama įkalnė, °'),
    )

    subcategory = models.ForeignKey(
        SubCategory, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='listings',
        verbose_name=_("Sub-category"),
    )

    title = models.CharField(max_length=200, verbose_name=_("Title"))
    description = models.TextField(verbose_name=_("Description"), blank=True)
    year = models.IntegerField(
        verbose_name=_("Year"),
        validators=[MinValueValidator(1900), MaxValueValidator(2100)]
    )
    mileage = models.IntegerField(
        verbose_name=_("Mileage (km)"),
        validators=[MinValueValidator(0), MaxValueValidator(9999999)]
    )
    first_registration = models.DateField(verbose_name=_("First Registration Date"), null=True, blank=True)

    fuel_type = models.ForeignKey(FuelType, on_delete=models.SET_NULL, null=True, blank=True)
    transmission = models.ForeignKey(Transmission, on_delete=models.SET_NULL, null=True, blank=True)
    body_type = models.CharField(max_length=50, choices=BODY_TYPE_CHOICES, blank=True)

    # ═══ TRUCK TYPE — autoplius-style "Tipas" (used when subcategory='trucks') ═══
    truck_type = models.CharField(
        max_length=30,
        choices=TRUCK_TYPE_CHOICES,
        blank=True,
        verbose_name=_('Truck type'),
        help_text="Used when subcategory is 'Trucks' (Sunkvežimiai)",
    )

    engine_capacity = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    power = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(9999)])
    color = models.CharField(max_length=50, choices=COLOR_CHOICES, blank=True)
    color_other_text = models.CharField(
        max_length=50, blank=True,
        verbose_name=_("Color (custom)"),
        help_text="Used when color='other' — free text fallback",
    )
    doors = models.CharField(max_length=10, choices=DOOR_CHOICES, blank=True)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='used')
    defects = models.CharField(max_length=50, choices=DEFECT_CHOICES, default='none')
    steering = models.CharField(max_length=10, choices=STEERING_CHOICES, blank=True)

    drive_type = models.CharField(max_length=10, choices=DRIVE_TYPE_CHOICES, blank=True)
    seats = models.CharField(max_length=5, choices=SEATS_CHOICES, blank=True)
    rim_size = models.CharField(max_length=5, choices=RIM_SIZE_CHOICES, blank=True)
    climate = models.CharField(max_length=20, choices=CLIMATE_CHOICES, blank=True)
    curb_weight = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(99999)])
    euro_standard = models.CharField(max_length=10, choices=EURO_STANDARD_CHOICES, blank=True)
    co2_emission = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(9999)])
    fuel_consumption_city = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    fuel_consumption_highway = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    fuel_consumption_combined = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    origin_country = models.CharField(max_length=2, choices=COUNTRY_CHOICES, blank=True)
    technical_inspection_month = models.IntegerField(null=True, blank=True)
    technical_inspection_year = models.IntegerField(null=True, blank=True)

    motorcycle_type = models.CharField(max_length=20, choices=MOTORCYCLE_TYPE_CHOICES, blank=True)
    cooling_type = models.CharField(max_length=10, choices=COOLING_TYPE_CHOICES, blank=True)
    moto_engine_type = models.CharField(max_length=20, choices=MOTO_ENGINE_TYPE_CHOICES, blank=True)
    engine_capacity_cc = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(9999)],
    )

    # ═══ MOTO GEAR FIELDS ═══
    gear_type = models.CharField(max_length=20, choices=GEAR_TYPE_CHOICES, blank=True)
    gear_subtype = models.CharField(max_length=50, choices=GEAR_SUBTYPE_CHOICES, blank=True)
    gear_subtype_other_text = models.CharField(
        max_length=100, blank=True,
        verbose_name=_("Subtype (custom)"),
        help_text="Used when subtype ends with ':other'",
    )

    gear_size = models.CharField(max_length=20, choices=GEAR_SIZE_CHOICES, blank=True)
    gear_size_other_text = models.CharField(
        max_length=50, blank=True,
        verbose_name=_("Size (custom)"),
        help_text="Used when size='other'",
    )

    # FK to GearBrand (autoplius-style dropdown)
    gear_brand = models.ForeignKey(
        'GearBrand', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='listings',
        verbose_name=_("Manufacturer"),
    )
    gear_brand_other_text = models.CharField(
        max_length=100, blank=True,
        verbose_name=_("Manufacturer (custom)"),
        help_text="Used when gear_brand=Other",
    )

    # Legacy free-text manufacturer (kept for migration of old data; new flow uses gear_brand FK)
    gear_brand_text = models.CharField(max_length=100, blank=True, verbose_name=_("Brand (legacy)"))

    gear_model_text = models.CharField(
        max_length=100, blank=True,
        verbose_name=_("Model name"),
    )

    gear_material = models.CharField(max_length=20, choices=GEAR_MATERIAL_CHOICES, blank=True)
    gear_material_other_text = models.CharField(
        max_length=50, blank=True,
        verbose_name=_("Material (custom)"),
    )

    gear_gender = models.CharField(max_length=10, choices=GEAR_GENDER_CHOICES, blank=True)
    gear_gender_other_text = models.CharField(
        max_length=50, blank=True,
        verbose_name=_("Gender (custom)"),
    )

    gear_safety_cert = models.CharField(max_length=20, choices=GEAR_SAFETY_CERT_CHOICES, blank=True)
    gear_safety_cert_other_text = models.CharField(
        max_length=100, blank=True,
        verbose_name=_("Safety certification (custom)"),
    )

    gear_ventilation_count = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(50)],
        verbose_name=_("Number of vents"),
    )

    vin = models.CharField(max_length=17, blank=True)
    registration_number = models.CharField(max_length=20, blank=True)

    # ─── PARTS-specific fields ───
    oem_code = models.CharField(
        max_length=50, blank=True, default='',
        db_index=True,
        verbose_name=_("OEM Code"),
        help_text="Manufacturer part number (e.g., 63217160797)"
    )
    part_category = models.ForeignKey(
        'PartCategory',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='listings',
        verbose_name=_("Part Category")
    )

    # ─── PARTS-specific: search by codes ───
    engine_code = models.CharField(
        max_length=30, blank=True, default='',
        db_index=True,
        verbose_name=_("Engine Code"),
        help_text="e.g., N52B30, M54B25"
    )
    transmission_code = models.CharField(
        max_length=30, blank=True, default='',
        db_index=True,
        verbose_name=_("Gearbox Code"),
        help_text="e.g., 6HP19, ZF8HP"
    )

    # ─── PARTS-specific: search by codes ───
    engine_code = models.CharField(
        max_length=30, blank=True, default='',
        db_index=True,
        verbose_name=_("Engine Code"),
        help_text="e.g., N52B30, M54B25"
    )
    transmission_code = models.CharField(
        max_length=30, blank=True, default='',
        db_index=True,
        verbose_name=_("Gearbox Code"),
        help_text="e.g., 6HP19, ZF8HP"
    )
    # ═══ CAR-FOR-PARTS specific fields ═══
    version = models.CharField(
        max_length=100, blank=True,
        verbose_name=_('Version'),
        help_text='e.g. "TDI Sportline" — used in car-for-parts category',
    )
    modification = models.CharField(
        max_length=100, blank=True,
        verbose_name=_('Modification'),
        help_text='e.g. "2.0 TDI 140kW"',
    )
    color_code = models.CharField(
        max_length=30, blank=True,
        verbose_name=_('Color code'),
        help_text='Manufacturer color code, e.g. "LY7G"',
    )
    engine_code = models.CharField(
        max_length=30, blank=True,
        verbose_name=_('Engine code'),
        help_text='e.g. "BKD"',
    )
    gearbox_code = models.CharField(
        max_length=30, blank=True,
        verbose_name=_('Gearbox code'),
        help_text='e.g. "DSG7"',
    )

    price = models.DecimalField(max_digits=10, decimal_places=2)
    export_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        verbose_name=_("Export price"),
        help_text="Optional separate price for export buyers",
    )
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    negotiable = models.BooleanField(default=False)
    open_to_trade = models.BooleanField(default=False, verbose_name=_("Open to trade"))

    # ═══ SPECIAL FEATURES (sidebar filters) ═══
    has_warranty = models.BooleanField(default=False, verbose_name=_('Warranty included'))
    available_on_lease = models.BooleanField(default=False, verbose_name=_('Available on lease'))
    is_sport_ready = models.BooleanField(default=False, verbose_name=_('Sport-ready'))
    disabled_friendly = models.BooleanField(default=False, verbose_name=_('Adapted for disabled'))
    has_service_book = models.BooleanField(default=False, verbose_name=_('Service book'))
    imported_from_us = models.BooleanField(default=False, verbose_name=_('Imported from US'))
    multiple_keys = models.BooleanField(default=False, verbose_name=_('Multiple key sets'))
    power_boosted = models.BooleanField(default=False, verbose_name=_('Increased engine power'))
    pneumatic_suspension = models.BooleanField(default=False, verbose_name=_('Pneumatic suspension'))
    remote_start = models.BooleanField(default=False, verbose_name=_('Remote start'))
    spare_wheel = models.BooleanField(default=False, verbose_name=_('Spare wheel'))
    valid_inspection = models.BooleanField(default=False, verbose_name=_('Valid technical inspection'))
    is_auction = models.BooleanField(default=False, verbose_name=_('From auction'))
    SELLER_TYPE_CHOICES_FILTER = [
        ('private', 'Private'),
        ('dealer', 'Dealer'),
    ]
    seller_type = models.CharField(max_length=20, choices=SELLER_TYPE_CHOICES_FILTER, default='private', blank=True)

    taxes_extra = models.BooleanField(
        default=False, verbose_name=_("+ Taxes"),
        help_text="Price excludes taxes — buyer should ask seller",
    )

    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES, default='US')
    state = models.CharField(max_length=2, choices=US_STATE_CHOICES, blank=True)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=200, blank=True)
    hide_exact_address = models.BooleanField(default=False)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    features = models.TextField(blank=True)
    video_url = models.URLField(blank=True)

    is_business_seller = models.BooleanField(default=False, verbose_name=_("Business seller"))

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_shadow_banned = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views_count = models.IntegerField(default=0)
    impressions_count = models.IntegerField(default=0)

    star_level = models.IntegerField(choices=STAR_LEVEL_CHOICES, default=0)
    star_count = models.IntegerField(default=0)
    star_expires_at = models.DateTimeField(null=True, blank=True)
    last_boosted_at = models.DateTimeField(null=True, blank=True)
    highlight_until = models.DateTimeField(null=True, blank=True, help_text="Listing card has highlighted background until this date")
    featured_until = models.DateTimeField(null=True, blank=True, help_text="Featured on homepage (Day's deals tab) until this date")

    activated_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    last_reminder_sent_at = models.DateTimeField(null=True, blank=True)
    last_no_sale_reminder_at = models.DateTimeField(null=True, blank=True)
    last_expired_reminder_at = models.DateTimeField(null=True, blank=True)
    first_views_notified_at = models.DateTimeField(null=True, blank=True)
    last_views_milestone = models.IntegerField(default=0)
    photo_tips_sent_at = models.DateTimeField(null=True, blank=True)
    last_draft_reminder_at = models.DateTimeField(null=True, blank=True)
    draft_reminder_count = models.IntegerField(default=0)

    reservation_note = models.CharField(max_length=200, blank=True)
    sold_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name=_("Listing")
        verbose_name_plural = "Listings"
        ordering = ['-created_at']

    @property
    def first_image(self):
        """Pirma nuotrauka per prefetch kešą.

        `listing.images.first()` kešo NENAUDOJA — Django jam kuria naują
        užklausą su LIMIT 1, todėl 12 kortelių duodavo 12 užklausų (per
        pagrindinį puslapį — 73). `images.all()` prefetch'ą naudoja.
        """
        imgs = list(self.images.all())
        return imgs[0] if imgs else None


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('listing_detail', kwargs={'pk': self.pk})



    def get_edit_url(self):

        slug = self.vehicle_type.slug if self.vehicle_type else None

        if self.status == 'draft':

            if slug == 'cars':

                return f"{reverse('listing_create_cars_quick')}?draft={self.pk}"

            if slug == 'motorcycles':

                return f"{reverse('motorcycle_listing_create')}?draft_id={self.pk}"

            if slug == 'trucks':

                return reverse('trucks_listing_create')

            return reverse('listing_create')

        if slug == 'motorcycles':

            return f"{reverse('motorcycle_listing_create')}?draft_id={self.pk}"

        return reverse('listing_edit_hub', kwargs={'pk': self.pk})


    def get_country_display_name(self):
        return dict(self.COUNTRY_CHOICES).get(self.country, self.country)

    def get_state_display_name(self):
        return dict(self.US_STATE_CHOICES).get(self.state, self.state)

    def get_display_location(self):
        parts = []
        if self.city:
            parts.append(self.city)
        if self.country == 'US' and self.state:
            parts.append(self.get_state_display_name())
        if self.country:
            parts.append(self.get_country_display_name())
        return ', '.join(parts)

    def get_full_address(self):
        parts = []
        if self.address:
            parts.append(self.address)
        if self.postal_code:
            parts.append(self.postal_code)
        if self.city:
            parts.append(self.city)
        if self.country == 'US' and self.state:
            parts.append(self.get_state_display_name())
        if self.country:
            parts.append(self.get_country_display_name())
        return ', '.join(parts)

    @property
    def is_motorcycle(self):
        return self.motorcycle_brand_id is not None

    @property
    def is_moto_gear(self):
        if not self.subcategory_id:
            return False
        if not (self.vehicle_type and self.vehicle_type.slug == 'motorcycles'):
            return False
        return self.subcategory.slug not in ('motorcycles', 'moto-gear')

    @property
    def is_truck(self):
        """True if this listing is in the 'Trucks' subcategory (uses truck_type)."""
        if not self.subcategory_id:
            return False
        return self.subcategory.slug == 'trucks'

    @property
    def display_brand(self):
        if self.is_motorcycle:
            return self.motorcycle_brand
        if self.is_moto_gear and self.gear_brand_id:
            if self.gear_brand.slug == 'other' and self.gear_brand_other_text:
                # Return a pseudo-object with name attribute
                class _Pseudo:
                    def __init__(self, name): self.name = name
                    def __str__(self): return self.name
                return _Pseudo(self.gear_brand_other_text)
            return self.gear_brand
        return self.brand

    @property
    def display_model(self):
        if self.is_motorcycle:
            return self.motorcycle_model
        if self.is_moto_gear and self.gear_model_text:
            class _Pseudo:
                def __init__(self, name): self.name = name
                def __str__(self): return self.name
            return _Pseudo(self.gear_model_text)
        return self.model

    @property
    def currency_symbol(self):
        return self.CURRENCY_SYMBOLS.get(self.currency, '$')

    # ═══ Helpers for resolving 'Other' fallback values ═══
    def get_color_display_value(self):
        if self.color == 'other' and self.color_other_text:
            return self.color_other_text
        return self.get_color_display() if self.color else ''

    def get_truck_type_display_value(self):
        """Returns truck type display name, or empty string."""
        if not self.truck_type:
            return ''
        return dict(self.TRUCK_TYPE_CHOICES).get(self.truck_type, self.truck_type)

    def get_gear_subtype_display_value(self):
        if self.gear_subtype and self.gear_subtype.endswith(':other') and self.gear_subtype_other_text:
            return self.gear_subtype_other_text
        return self.get_gear_subtype_display() if self.gear_subtype else ''

    def get_gear_size_display_value(self):
        if self.gear_size == 'other' and self.gear_size_other_text:
            return self.gear_size_other_text
        return self.get_gear_size_display() if self.gear_size else ''

    def get_gear_material_display_value(self):
        if self.gear_material == 'other' and self.gear_material_other_text:
            return self.gear_material_other_text
        return self.get_gear_material_display() if self.gear_material else ''

    def get_gear_gender_display_value(self):
        if self.gear_gender == 'other' and self.gear_gender_other_text:
            return self.gear_gender_other_text
        return self.get_gear_gender_display() if self.gear_gender else ''

    def get_gear_safety_cert_display_value(self):
        if self.gear_safety_cert == 'other' and self.gear_safety_cert_other_text:
            return self.gear_safety_cert_other_text
        return self.get_gear_safety_cert_display() if self.gear_safety_cert else ''

    def is_star_active(self):
        if self.star_level == 0 or not self.star_expires_at:
            return False
        return self.star_expires_at > timezone.now()

    @property
    def is_highlighted(self):
        """Check if listing should display with highlighted background."""
        if not self.highlight_until:
            return False
        return self.highlight_until > timezone.now()

    @property
    def is_featured(self):
        """Check if listing is currently featured on homepage (Day's deals)."""
        if not self.featured_until:
            return False
        return self.featured_until > timezone.now()

    def get_effective_star_level(self):
        return self.star_level if self.is_star_active() else 0

    def activate_stars(self, level):
        if level not in self.STAR_DURATIONS:
            return False
        self.star_level = level
        self.star_expires_at = timezone.now() + timedelta(days=self.STAR_DURATIONS[level])
        self.save(update_fields=['star_level', 'star_expires_at'])
        return True

    def deactivate_stars(self):
        self.star_level = 0
        self.star_expires_at = None
        self.save(update_fields=['star_level', 'star_expires_at'])

    def can_boost(self):
        if not self.last_boosted_at:
            return True
        return timezone.now() - self.last_boosted_at >= timedelta(hours=self.BOOST_COOLDOWN_HOURS)

    def get_seconds_until_next_boost(self):
        if self.can_boost():
            return 0
        available_at = self.last_boosted_at + timedelta(hours=self.BOOST_COOLDOWN_HOURS)
        return max(0, int((available_at - timezone.now()).total_seconds()))

    def apply_boost(self):
        if not self.can_boost():
            return False
        self.last_boosted_at = timezone.now()
        self.save(update_fields=['last_boosted_at'])
        return True

    def is_recently_boosted(self):
        if not self.last_boosted_at:
            return False
        return timezone.now() - self.last_boosted_at < timedelta(hours=24)

    @property
    def show_renewed_badge(self):
        if not self.last_boosted_at:
            return False
        return (timezone.now() - self.last_boosted_at) < timedelta(hours=self.RENEWED_BADGE_HOURS)

    def is_new_listing(self, days=3):
        if not self.created_at:
            return False
        return timezone.now() - self.created_at < timedelta(days=days)

    def get_sort_priority(self):
        level = self.get_effective_star_level()
        if level == 2: return 500
        if level == 1: return 400
        if self.is_recently_boosted(): return 300
        if self.is_new_listing(): return 200
        return 100

    @property
    def is_expired(self):
        return self.expires_at and self.expires_at < timezone.now()

    @property
    def days_until_expiry(self):
        if not self.expires_at:
            return None
        return max(0, (self.expires_at - timezone.now()).days)

    @property
    def hours_until_expiry(self):
        if not self.expires_at:
            return None
        return max(0, int((self.expires_at - timezone.now()).total_seconds() // 3600))

    @property
    def days_since_expired(self):
        if not self.expires_at or self.expires_at > timezone.now():
            return None
        return (timezone.now() - self.expires_at).days

    @property
    def is_sold(self):
        return self.status == 'sold'

    @property
    def days_since_sold(self):
        return (timezone.now() - self.sold_at).days if self.sold_at else None

    @property
    def sold_days_remaining(self):
        if not self.sold_at:
            return None
        return max(0, self.SOLD_DISPLAY_DAYS - self.days_since_sold)

    @property
    def should_auto_delete_sold(self):
        if self.status != 'sold' or not self.sold_at:
            return False
        return (timezone.now() - self.sold_at) >= timedelta(days=self.SOLD_DISPLAY_DAYS)

    def mark_as_sold(self):
        self.status = 'sold'
        self.sold_at = timezone.now()
        self.save(update_fields=['status', 'sold_at'])

    def activate(self, days=None):
        if days is None:
            days = self.DEFAULT_ACTIVE_DAYS
        self.status = 'active'
        self.activated_at = timezone.now()
        self.expires_at = timezone.now() + timedelta(days=days)
        self.last_reminder_sent_at = None
        self.last_no_sale_reminder_at = None
        self.last_expired_reminder_at = None
        self.last_draft_reminder_at = None
        self.draft_reminder_count = 0
        self.save(update_fields=[
            'status', 'activated_at', 'expires_at',
            'last_reminder_sent_at', 'last_no_sale_reminder_at',
            'last_expired_reminder_at',
            'last_draft_reminder_at', 'draft_reminder_count',
        ])
        return True

    def mark_expired(self):
        self.status = 'expired'
        self.last_reminder_sent_at = None
        self.save(update_fields=['status', 'last_reminder_sent_at'])

    def reserve(self, note=''):
        self.status = 'reserved'
        self.reservation_note = note
        self.save(update_fields=['status', 'reservation_note'])

    def unreserve(self):
        if self.expires_at and self.expires_at > timezone.now():
            self.status = 'active'
        else:
            self.status = 'expired'
        self.reservation_note = ''
        self.save(update_fields=['status', 'reservation_note'])

    def needs_expiry_reminder(self):
        if not self.expires_at:
            return False
        now = timezone.now()
        if self.status == 'active':
            if self.last_reminder_sent_at:
                return False
            d = self.days_until_expiry
            return d is not None and d <= self.EXPIRY_REMINDER_DAYS
        if self.status == 'expired':
            if self.last_reminder_sent_at:
                return now - self.last_reminder_sent_at >= timedelta(days=self.POST_EXPIRY_REMINDER_INTERVAL_DAYS)
            return True
        return False

    @property
    def should_auto_delete(self):
        if self.status != 'expired' or not self.expires_at:
            return False
        return (timezone.now() - self.expires_at) >= timedelta(days=self.AUTO_DELETE_AFTER_EXPIRY_DAYS)

    @classmethod
    def calculate_listing_fee(cls, price):
        try:
            price = float(price or 0)
        except (TypeError, ValueError):
            price = 0
        for threshold, fee in cls.PRICING_TIERS:
            if price < threshold:
                return fee
        return cls.PRICING_TIERS[-1][1]

    @property
    def listing_fee(self):
        return self.calculate_listing_fee(self.price)

    @property
    def click_through_rate(self):
        if not self.impressions_count:
            return 0.0
        return round((self.views_count / self.impressions_count) * 100, 1)

    @property
    def save_rate(self):
        if not self.views_count:
            return 0.0
        return round((self.saved_by.count() / self.views_count) * 100, 1)

    def get_position(self):
        from django.db.models import Case, When, IntegerField, Value
        if self.status != 'active' or self.is_shadow_banned:
            return None, None
        now = timezone.now()
        three_days_ago = now - timedelta(days=3)
        boost_cutoff = now - timedelta(hours=24)
        all_active = Listing.objects.filter(status='active', is_shadow_banned=False).annotate(
            sort_priority=Case(
                When(star_level=2, star_expires_at__gt=now, then=Value(500)),
                When(star_level=1, star_expires_at__gt=now, then=Value(400)),
                When(last_boosted_at__gt=boost_cutoff, then=Value(300)),
                When(created_at__gt=three_days_ago, then=Value(200)),
                default=Value(100),
                output_field=IntegerField(),
            )
        ).order_by('-sort_priority', '-created_at')
        total = all_active.count()
        my_priority = self.get_sort_priority()
        higher = all_active.filter(sort_priority__gt=my_priority).count()
        same = all_active.filter(sort_priority=my_priority, created_at__gt=self.created_at).count()
        return higher + same + 1, total


class ListingView(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='view_records')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='listing_views')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-viewed_at']
        indexes = [models.Index(fields=['listing', 'viewed_at'])]


class ListingImpression(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='impression_records')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='listing_impressions')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    shown_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-shown_at']
        indexes = [models.Index(fields=['listing', 'shown_at'])]


class SalesRecord(models.Model):
    seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sales_records')
    seller_email = models.EmailField(blank=True)
    listing_id = models.IntegerField(null=True, blank=True)
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.SET_NULL, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    model = models.ForeignKey(Model, on_delete=models.SET_NULL, null=True, blank=True)
    motorcycle_brand = models.ForeignKey(MotorcycleBrand, on_delete=models.SET_NULL, null=True, blank=True)
    motorcycle_model = models.ForeignKey(MotorcycleModel, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    year = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=2, blank=True)
    listing_created_at = models.DateTimeField(null=True, blank=True)
    sold_at = models.DateTimeField(auto_now_add=True, db_index=True)
    days_active = models.IntegerField(default=0)
    views_count = models.IntegerField(default=0)
    impressions_count = models.IntegerField(default=0)
    saves_count = models.IntegerField(default=0)
    marked_sold = models.BooleanField(default=False)

    class Meta:
        ordering = ['-sold_at']
        indexes = [
            models.Index(fields=['-sold_at']),
            models.Index(fields=['seller', '-sold_at']),
        ]

    def __str__(self):
        return f"{self.title} sold {self.currency} {self.price}"

    @property
    def currency_symbol(self):
        return {'USD': '$', 'EUR': '€', 'GBP': '£'}.get(self.currency, '$')

    @classmethod
    def create_from_listing(cls, listing, marked_sold=False):
        days_active = 0
        if listing.activated_at:
            days_active = (timezone.now() - listing.activated_at).days
        return cls.objects.create(
            seller=listing.seller,
            seller_email=listing.seller.email if listing.seller else '',
            listing_id=listing.pk,
            vehicle_type=listing.vehicle_type,
            brand=listing.brand,
            model=listing.model,
            motorcycle_brand=listing.motorcycle_brand,
            motorcycle_model=listing.motorcycle_model,
            title=listing.title,
            year=listing.year,
            price=listing.price,
            currency=listing.currency,
            city=listing.city,
            country=listing.country,
            listing_created_at=listing.created_at,
            days_active=days_active,
            views_count=listing.views_count or 0,
            impressions_count=listing.impressions_count or 0,
            saves_count=listing.saved_by.count(),
            marked_sold=marked_sold,
        )


class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    # ORIGINALAS — nekeičiamas ir netrinamas. Puslapiuose nerodomas.
    image = models.ImageField(upload_to='listings/%Y/%m/')
    # Išvestinės: 1600 px (lg) ir 668 px (sm), WebP + JPEG atsarga.
    # Žr. apps/listings/imaging.py — ten viena vieta, kur jos gaminamos.
    image_lg = models.ImageField(upload_to='listings/derived/%Y/%m/', blank=True, null=True)
    image_lg_webp = models.ImageField(upload_to='listings/derived/%Y/%m/', blank=True, null=True)
    image_sm = models.ImageField(upload_to='listings/derived/%Y/%m/', blank=True, null=True)
    image_sm_webp = models.ImageField(upload_to='listings/derived/%Y/%m/', blank=True, null=True)
    # lg matmenys — kad <img> turėtų width/height ir puslapis nešokinėtų
    # (CLS 0,119 buvo būtent dėl jų nebuvimo).
    w_lg = models.PositiveIntegerField(null=True, blank=True)
    h_lg = models.PositiveIntegerField(null=True, blank=True)
    caption = models.CharField(max_length=200, blank=True)
    is_main = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-is_main']

    def __str__(self):
        return f"{self.listing.title} - {self.order}"

    def save(self, *args, **kwargs):
        """Įkėlus naują failą — iškart pasigaminam išvestines.

        Taip problema nebegrįžta: nesvarbu, per kurią formą ar AJAX
        įkelta, rodomos versijos atsiranda kartu su originalu.
        """
        super().save(*args, **kwargs)
        if self.image and not self.image_lg:
            from apps.listings.imaging import build_derivatives
            try:
                build_derivatives(self)
            except Exception:
                pass          # originalas jau išsaugotas — rodysim jį

    # ── Ką rodyti šablonuose ────────────────────────────────────────
    @property
    def url_lg(self):
        return (self.image_lg or self.image).url

    @property
    def url_lg_webp(self):
        return self.image_lg_webp.url if self.image_lg_webp else None

    @property
    def url_sm(self):
        return (self.image_sm or self.image_lg or self.image).url

    @property
    def url_sm_webp(self):
        return self.image_sm_webp.url if self.image_sm_webp else None


class Equipment(models.Model):
    CATEGORY_CHOICES = [
        ('interior', _('Interior')),
        ('electronics', _('Electronics')),
        ('safety', _('Safety')),
        ('audio_video', _('Audio/Video')),
        ('exterior', _('Exterior')),
        ('other', _('Other Features')),
        ('motorcycle', _('Motorcycle Features')),
        ('gear', _('Gear Features')),
        ('truck', _('Truck Features')),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE, null=True, blank=True, related_name='equipment')
    gear_types = models.CharField(max_length=200, blank=True, help_text="CSV gear_types (helmet,jacket,...). Empty=all.")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['category', 'order', 'name']

    def __str__(self):
        return self.name

    def applies_to_gear_type(self, gear_type):
        if self.category != 'gear':
            return False
        if not self.gear_types:
            return True
        return gear_type in [g.strip() for g in self.gear_types.split(',')]


class ListingEquipment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='equipment_items')
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['listing', 'equipment']

    def __str__(self):
        return f"{self.listing.title} - {self.equipment.name}"


class SavedListing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_listings')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'listing']
        ordering = ['-saved_at']


class SavedListingNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='save_notifications')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='save_notifications')
    notified_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'listing']
        ordering = ['-notified_at']


class SavedSearch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_searches')
    name = models.CharField(max_length=200)
    query_params = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    notify_email = models.BooleanField(default=False)
    last_viewed_at = models.DateTimeField(null=True, blank=True)
    track_price_drop = models.BooleanField(default=False)
    last_checked_at = models.DateTimeField(null=True, blank=True)
    last_min_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    last_results_count = models.IntegerField(null=True, blank=True)
    last_notified_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']


class EmailScenario(models.Model):
    CATEGORY_CHOICES = [
        ('Seller', _('Seller notifications')),
        ('Buyer (Saved)', _('Buyer - saved listings')),
        ('Saved Search', _('Saved search alerts')),
        ('Account', _('Account / auth')),
        ('Communication', _('Messaging')),
        ('Payments', _('Payments / Stripe')),
        ('Marketing', _('Marketing / newsletter')),
        ('Admin', _('Admin notifications')),
        ('Extra', _('Extra / experimental')),
        ('Truck', _('Truck-specific notifications')),
    ]
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Seller')
    trigger = models.CharField(max_length=200, blank=True)
    is_enabled = models.BooleanField(default=True)
    send_count = models.IntegerField(default=0)
    fail_count = models.IntegerField(default=0)
    last_sent_at = models.DateTimeField(null=True, blank=True)
    last_failed_at = models.DateTimeField(null=True, blank=True)
    last_error = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        status = '✓' if self.is_enabled else '✗'
        return f'{status} [{self.category}] {self.name}'


class PricingPlan(models.Model):
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE, related_name='pricing_plans')
    duration_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    old_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    discount_percent = models.PositiveIntegerField(null=True, blank=True)
    is_popular = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    custom_label = models.CharField(max_length=50, blank=True)
    boost_days = models.PositiveIntegerField(default=0)
    vip_days = models.PositiveIntegerField(default=0)
    homepage_ad_days = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['vehicle_type', 'order', 'duration_days']
        unique_together = [['vehicle_type', 'duration_days']]

    def __str__(self):
        return f'{self.vehicle_type.name} — {self.duration_days}d — ${self.price}'

    # ═══ NEW FIELDS for select_plan flow ═══
    # (Pridėti per migration — kad veiktų autoplius-style 3 plan'ai)
    code = models.CharField(
        max_length=30, blank=True,
        help_text="Plan code: 'basic_30', 'standard_60', 'premium_90'",
    )
    label = models.CharField(
        max_length=50, blank=True,
        help_text="Display name: 'Basic', 'Standard', 'Recommended'",
    )
    boost_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of stars (1-3) shown on listing card",
    )
    featured_days = models.PositiveIntegerField(
        default=0,
        help_text="Days listing appears on homepage Day's deals",
    )
    highlight_days = models.PositiveIntegerField(
        default=0,
        help_text="Days listing card has highlighted background",
    )
    is_recommended = models.BooleanField(
        default=False,
        help_text="Show 'RECOMMENDED' badge on this plan",
    )

    @property
    def features_list(self):
        return [
            {'label': 'Listing duration', 'value': f'{self.duration_days} d.'},
            {'label': 'Boost in list', 'value': f'{self.boost_days} d.' if self.boost_days else '—'},
            {'label': 'VIP listing', 'value': f'{self.vip_days} d.' if self.vip_days else '—'},
            {'label': 'Homepage ad', 'value': f'{self.homepage_ad_days} d.' if self.homepage_ad_days else '—'},
            {'label': 'Phone number protection', 'value': f'{self.duration_days} d.'},
        ]


# ═══════════════════════════════════════════════════════════════════════════
# PRICING SETTINGS — singleton (multiplier on/off)
# ═══════════════════════════════════════════════════════════════════════════

class PricingSettings(models.Model):
    """Singleton: globalūs pricing nustatymai.
    Visada yra TIK 1 įrašas (id=1)."""

    multiplier_enabled = models.BooleanField(
        default=False,
        help_text="ĮJUNGTI dynamic pricing (kuo brangesnis listing → tuo brangesnis plan'as)",
    )
    addon_renew_price = models.DecimalField(
        max_digits=6, decimal_places=2, default=1.00,
        help_text="Cena už 1 žvaigždutę per dieną ($)",
    )
    addon_featured_price = models.DecimalField(
        max_digits=6, decimal_places=2, default=0.30,
        help_text="Cena už Featured on homepage per dieną ($)",
    )
    addon_renew_max_count = models.PositiveIntegerField(default=20)
    addon_renew_max_days = models.PositiveIntegerField(default=42)
    addon_featured_max_days = models.PositiveIntegerField(default=42)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name=_("Pricing Settings")
        verbose_name_plural = "Pricing Settings"

    def __str__(self):
        return f"Pricing Settings (multiplier: {'ON' if self.multiplier_enabled else 'OFF'})"

    def save(self, *args, **kwargs):
        # Force singleton — visada id=1
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        """Visada grąžina settings instance (sukuriam jei nėra)."""
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


# ═══════════════════════════════════════════════════════════════════════════
# PRICE MULTIPLIER TIER — pagal listing.price keičia plan kainą
# ═══════════════════════════════════════════════════════════════════════════

class PriceMultiplierTier(models.Model):
    """Tier'ai pagal listing.price.
    Pavyzdžiui: 0-5k = 1.0x, 5k-20k = 1.2x, 20k-50k = 1.5x, etc."""

    min_price = models.DecimalField(
        max_digits=12, decimal_places=2,
        help_text="Listing.price minimum (inclusive)",
    )
    max_price = models.DecimalField(
        max_digits=12, decimal_places=2,
        help_text="Listing.price maximum (exclusive)",
    )
    multiplier = models.DecimalField(
        max_digits=4, decimal_places=2, default=1.0,
        help_text="Plano kaina × multiplier (pvz. 1.5 = +50%)",
    )
    label = models.CharField(
        max_length=50, blank=True,
        help_text="Optional label (pvz. 'Pigus', 'Brangus', 'Luxury')",
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name=_("Price Multiplier Tier")
        verbose_name_plural = "Price Multiplier Tiers"
        ordering = ['min_price']

    def __str__(self):
        return f"${int(self.min_price)}-${int(self.max_price)} → {self.multiplier}x"


# ═══════════════════════════════════════════════════════════════════════════
# PROMO CODE — akcijų kodai
# ═══════════════════════════════════════════════════════════════════════════

class PromoCode(models.Model):
    """Akcijos kodai (pvz. 'SPRING25' = -25%, 'TRUCK10' = - nuo trucks)."""

    DISCOUNT_PERCENT = 'percent'
    DISCOUNT_FIXED = 'fixed'
    DISCOUNT_TYPE_CHOICES = [
        (DISCOUNT_PERCENT, 'Percentage (%)'),
        (DISCOUNT_FIXED, 'Fixed amount ($)'),
    ]

    code = models.CharField(
        max_length=30, unique=True,
        help_text="Pvz. 'SPRING25', 'WELCOME10' (ne case-sensitive)",
    )
    description = models.CharField(
        max_length=200, blank=True,
        help_text="Vidinis aprašymas (admin tik mato)",
    )

    # Discount
    discount_type = models.CharField(
        max_length=20, choices=DISCOUNT_TYPE_CHOICES, default=DISCOUNT_PERCENT,
    )
    discount_value = models.DecimalField(
        max_digits=8, decimal_places=2,
        help_text="25 = -25% (jei percent), arba 10 = - (jei fixed)",
    )

    # Valid period
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_until = models.DateTimeField(null=True, blank=True)

    # Usage limits
    max_uses = models.PositiveIntegerField(
        null=True, blank=True,
        help_text="Maksimalus panaudojimų skaičius (null = unlimited)",
    )
    used_count = models.PositiveIntegerField(default=0)
    once_per_user = models.BooleanField(
        default=True,
        help_text="Vienas user'is gali naudoti tik kartą",
    )

    # Category restrictions
    applies_to_cars = models.BooleanField(default=True)
    applies_to_trucks = models.BooleanField(default=True)
    applies_to_motorcycles = models.BooleanField(default=True)

    # Plan restrictions
    applies_to_basic = models.BooleanField(default=True)
    applies_to_standard = models.BooleanField(default=True)
    applies_to_premium = models.BooleanField(default=True)

    # Min listing price (jei nori — 'kodas veikia tik virš ')
    min_listing_price = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True,
        help_text="Minimum listing.price kad kodas veiktų (null = no limit)",
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name=_("Promo Code")
        verbose_name_plural = "Promo Codes"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.code} ({self.discount_value}{'%' if self.discount_type == 'percent' else '$'})"

    def is_valid(self, user=None, listing=None, plan_code=None):
        """Patikrina ar kodas dabar veikia tomis sąlygomis.
        Grąžina (True, '') arba (False, 'Reason')."""
        from django.utils import timezone

        if not self.is_active:
            return (False, 'Code is inactive')

        now = timezone.now()
        if self.valid_from and now < self.valid_from:
            return (False, 'Code not yet valid')
        if self.valid_until and now > self.valid_until:
            return (False, 'Code expired')

        if self.max_uses and self.used_count >= self.max_uses:
            return (False, 'Code usage limit reached')

        # Per-user check
        if user and self.once_per_user:
            if PromoCodeUsage.objects.filter(promo_code=self, user=user).exists():
                return (False, 'You already used this code')

        # Category check
        if listing and listing.vehicle_type:
            slug = listing.vehicle_type.slug
            if slug == 'cars' and not self.applies_to_cars:
                return (False, 'Code not valid for Cars')
            if slug == 'trucks' and not self.applies_to_trucks:
                return (False, 'Code not valid for Trucks')
            if slug == 'motorcycles' and not self.applies_to_motorcycles:
                return (False, 'Code not valid for Motorcycles')

        # Plan check
        if plan_code:
            if plan_code == 'basic_30' and not self.applies_to_basic:
                return (False, 'Code not valid for Basic plan')
            if plan_code == 'standard_60' and not self.applies_to_standard:
                return (False, 'Code not valid for Standard plan')
            if plan_code == 'premium_90' and not self.applies_to_premium:
                return (False, 'Code not valid for Recommended plan')

        # Min listing price
        if self.min_listing_price and listing and listing.price < self.min_listing_price:
            return (False, f'Listing price must be at least ${int(self.min_listing_price)}')

        return (True, '')

    def calculate_discount(self, original_price):
        """Apskaičiuoja nuolaidos sumą."""
        from decimal import Decimal
        original = Decimal(str(original_price))

        if self.discount_type == self.DISCOUNT_PERCENT:
            return (original * self.discount_value / Decimal('100')).quantize(Decimal('0.01'))
        else:
            return min(self.discount_value, original)


class PromoCodeUsage(models.Model):
    """Track promo code panaudojimus (kas, kada, su kuriuo listing)."""

    promo_code = models.ForeignKey(
        PromoCode, on_delete=models.CASCADE, related_name='usages',
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='promo_code_usages',
    )
    listing = models.ForeignKey(
        Listing, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='promo_usages',
    )
    discount_amount = models.DecimalField(max_digits=8, decimal_places=2)
    used_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-used_at']
        verbose_name=_("Promo Code Usage")
        verbose_name_plural = "Promo Code Usages"

    def __str__(self):
        return f"{self.user.email} used {self.promo_code.code} (-${self.discount_amount})"




# ═══════════════════════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════════════════
#
#   TRUCK SYSTEM — atskira DB sistema (NEPRIKLAUSO nuo Listing)
#   (Šis Truck modelis dar nenaudojamas; trucks šiuo metu naudoja Listing)
#
# ═══════════════════════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════════════════


class Truck(models.Model):
    SUBCATEGORY_CHOICES = [
        ('trucks', _('Trucks (Sunkvežimiai)')),
        ('vehicle-transporters', _('Vehicle Transporters')),
        ('semi-trucks-tractors', _('Semi-trucks / Tractors')),
        ('vans', _('Vans')),
    ]

    CONDITION_CHOICES = [
        ('new', _('New')),
        ('used', _('Used')),
    ]

    STATUS_CHOICES = [
        ('draft', _('Juodraštis')),
        ('active', _('Aktyvus')),
        ('reserved', _('Rezervuotas')),
        ('expired', _('Neaktyvus')),
        ('sold', _('Parduotas')),
        ('archived', _('Archyvuotas')),
    ]

    # ═══ TRUCK TYPE — autoplius-style "Tipas" filter (23 types) ═══
    TRUCK_TYPE_CHOICES = [
        ('', _('— Select —')),
        ('tankers', _('Tankers')),
        ('car_carriers', _('Car Carriers')),
        ('concrete_mixers', _('Concrete Mixers')),
        ('flatbed', _('Flatbed')),
        ('flatbed_tarpaulin', _('Flatbed with Tarpaulin')),
        ('curtain_side', _('Curtain-Side')),
        ('double_cab', _('Double Cab')),
        ('livestock_carriers', _('Livestock Carriers')),
        ('insulated_box', _('Insulated Box')),
        ('hard_side_box', _('Hard-Side Box')),
        ('container_carriers', _('Container Carriers')),
        ('logging_trucks', _('Logging Trucks')),
        ('milk_tankers', _('Milk Tankers')),
        ('platforms', _('Platforms')),
        ('mobile_shop', _('Mobile Shop')),
        ('tippers', _('Tippers')),
        ('hook_lift_tippers', _('Hook-Lift Tippers')),
        ('crane_tippers', _('Crane Tippers')),
        ('with_crane', _('With Crane')),
        ('refrigerators', _('Refrigerators')),
        ('curtain_tarpaulin', _('Curtain / Tarpaulin')),
        ('chassis', _('Chassis')),
        ('other', _('Other')),
    ]

    CAB_TYPE_CHOICES = [
        ('', _('Any')),
        ('day', _('Day cab')),
        ('sleeper', _('Sleeper')),
        ('crew', _('Crew cab')),
        ('extended', _('Extended cab')),
    ]

    AXLE_CONFIG_CHOICES = [
        ('', _('Any')),
        ('4x2', _('4x2')),
        ('4x4', _('4x4')),
        ('6x2', _('6x2')),
        ('6x4', _('6x4')),
        ('6x6', _('6x6')),
        ('8x2', _('8x2')),
        ('8x4', _('8x4')),
        ('8x6', _('8x6')),
        ('8x8', _('8x8')),
    ]

    SUSPENSION_CHOICES = [
        ('', _('Any')),
        ('air_air', _('Air / Air')),
        ('air_spring', _('Air / Spring')),
        ('spring_air', _('Spring / Air')),
        ('spring_spring', _('Spring / Spring')),
    ]

    TRANSMISSION_CHOICES = [
        ('', _('Any')),
        ('manual', _('Manual')),
        ('automatic', _('Automatic')),
        ('semi_automatic', _('Semi-automatic')),
    ]

    FUEL_TYPE_CHOICES = [
        ('', _('Any')),
        ('diesel', _('Diesel')),
        ('petrol', _('Petrol / Gasoline')),
        ('lpg', _('LPG')),
        ('cng', _('CNG')),
        ('lng', _('LNG')),
        ('electric', _('Electric')),
        ('hybrid', _('Hybrid')),
        ('hydrogen', _('Hydrogen')),
        ('other', _('Other')),
    ]

    EURO_STANDARD_CHOICES = [
        ('', 'Any'),
        ('euro1', 'Euro 1'), ('euro2', 'Euro 2'),
        ('euro3', 'Euro 3'), ('euro4', 'Euro 4'),
        ('euro5', 'Euro 5'), ('euro6', 'Euro 6'),
        ('euro6d', 'Euro 6d'),
    ]

    COLOR_CHOICES = [
        ('other', _('Other')),
        ('white', _('White')), ('black', _('Black')),
        ('red', _('Red / Burgundy')), ('blue', _('Blue')),
        ('green_khaki', _('Green / Khaki')), ('yellow_gold', _('Yellow / Gold')),
        ('orange', _('Orange')), ('brown_beige', _('Brown / Beige')),
        ('multicolor', _('Multicolor')),
    ]

    DEFECT_CHOICES = [
        ('none', _('No defects')),
        ('engine_defect', _('Engine defect')),
        ('gearbox_defect', _('Gearbox defect')),
        ('dented', _('Dented')),
        ('burned', _('Burned')),
        ('major_defects', _('Major defects')),
    ]

    STEERING_CHOICES = [
        ('left', _('Left-hand drive')),
        ('right', _('Right-hand drive (UK)')),
    ]

    COUNTRY_CHOICES = [
        ('US', _('United States')), ('LT', _('Lithuania')),
        ('LV', _('Latvia')), ('EE', _('Estonia')),
        ('PL', _('Poland')), ('DE', _('Germany')),
        ('NL', _('Netherlands')), ('BE', _('Belgium')),
        ('FR', _('France')), ('IT', _('Italy')),
        ('ES', _('Spain')), ('AT', _('Austria')),
        ('CZ', _('Czech Republic')), ('SK', _('Slovakia')),
        ('HU', _('Hungary')), ('RO', _('Romania')),
        ('BG', _('Bulgaria')), ('SE', _('Sweden')),
        ('DK', _('Denmark')), ('FI', _('Finland')),
        ('NO', _('Norway')), ('GB', _('United Kingdom')),
        ('IE', _('Ireland')), ('CH', _('Switzerland')),
    ]

    US_STATE_CHOICES = [
        ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'),
        ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'),
        ('CT', 'Connecticut'), ('DE', 'Delaware'), ('FL', 'Florida'),
        ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'),
        ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'),
        ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'),
        ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'),
        ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'),
        ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'),
        ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'),
        ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'),
        ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'),
        ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'),
        ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'),
        ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'),
        ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'),
        ('WI', 'Wisconsin'), ('WY', 'Wyoming'),
    ]

    CURRENCY_CHOICES = [
        ('USD', 'US Dollar ($)'),
        ('EUR', 'Euro (€)'),
        ('GBP', 'British Pound (£)'),
    ]

    CURRENCY_SYMBOLS = {'USD': '$', 'EUR': '€', 'GBP': '£'}

    STAR_LEVEL_CHOICES = [
        (0, 'No Stars'),
        (1, '⭐ One Star (7 days)'),
        (2, '⭐⭐ Two Stars (30 days)'),
    ]

    STAR_DURATIONS = {1: 7, 2: 30}
    BOOST_COOLDOWN_HOURS = 1
    RENEWED_BADGE_HOURS = 48
    DEFAULT_ACTIVE_DAYS = 30
    EXPIRY_REMINDER_DAYS = 3
    POST_EXPIRY_REMINDER_INTERVAL_DAYS = 3
    AUTO_DELETE_AFTER_EXPIRY_DAYS = 160
    SOLD_DISPLAY_DAYS = 3

    PRICING_TIERS = [
        (5000, 5),
        (20000, 10),
        (float('inf'), 15),
    ]

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trucks')

    subcategory = models.CharField(
        max_length=30,
        choices=SUBCATEGORY_CHOICES,
        default='trucks',
        verbose_name=_("Sub-category"),
    )

    brand = models.ForeignKey(
        TruckBrand, on_delete=models.CASCADE,
        related_name='trucks',
        verbose_name=_("Truck Brand"),
    )
    model = models.ForeignKey(
        TruckModel, on_delete=models.CASCADE,
        related_name='trucks',
        verbose_name=_("Truck Model"),
    )

    title = models.CharField(max_length=200, verbose_name=_("Title"))
    description = models.TextField(verbose_name=_("Description"), blank=True)

    year = models.IntegerField(
        verbose_name=_("Year"),
        validators=[MinValueValidator(1900), MaxValueValidator(2100)],
    )
    mileage = models.IntegerField(
        verbose_name=_("Mileage (km)"),
        validators=[MinValueValidator(0), MaxValueValidator(9999999)],
    )
    first_registration = models.DateField(
        verbose_name=_("First Registration Date"), null=True, blank=True,
    )

    truck_type = models.CharField(
        max_length=30, choices=TRUCK_TYPE_CHOICES, blank=True,
        verbose_name=_('Truck type'),
    )
    cab_type = models.CharField(
        max_length=20, choices=CAB_TYPE_CHOICES, blank=True,
        verbose_name=_('Cab type'),
    )
    axle_config = models.CharField(
        max_length=10, choices=AXLE_CONFIG_CHOICES, blank=True,
        verbose_name=_('Axle configuration'),
    )
    suspension = models.CharField(
        max_length=20, choices=SUSPENSION_CHOICES, blank=True,
        verbose_name=_('Suspension'),
    )

    gross_weight = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(999999)],
        verbose_name=_('Gross weight (kg)'),
    )
    curb_weight = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(999999)],
        verbose_name=_('Curb weight (kg)'),
    )
    payload = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(999999)],
        verbose_name=_('Payload capacity (kg)'),
    )
    cargo_volume = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True,
        verbose_name=_('Cargo volume (m³)'),
    )
    cargo_length = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        verbose_name=_('Cargo length (m)'),
    )
    cargo_width = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        verbose_name=_('Cargo width (m)'),
    )
    cargo_height = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        verbose_name=_('Cargo height (m)'),
    )
    number_of_seats = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(20)],
        verbose_name=_('Number of seats'),
    )

    fuel_type = models.CharField(
        max_length=20, choices=FUEL_TYPE_CHOICES, blank=True,
    )
    transmission = models.CharField(
        max_length=20, choices=TRANSMISSION_CHOICES, blank=True,
    )
    engine_capacity = models.DecimalField(
        max_digits=5, decimal_places=1, null=True, blank=True,
        verbose_name=_('Engine capacity (L)'),
    )
    power = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(9999)],
        verbose_name=_('Power (kW)'),
    )
    power_hp = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(9999)],
        verbose_name=_('Power (HP)'),
    )
    torque = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(99999)],
        verbose_name=_('Torque (Nm)'),
    )
    euro_standard = models.CharField(
        max_length=10, choices=EURO_STANDARD_CHOICES, blank=True,
    )
    fuel_consumption = models.DecimalField(
        max_digits=4, decimal_places=1, null=True, blank=True,
        verbose_name=_('Fuel consumption (L/100km)'),
    )
    fuel_tank_capacity = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(9999)],
        verbose_name=_('Fuel tank (L)'),
    )

    color = models.CharField(max_length=50, choices=COLOR_CHOICES, blank=True)
    color_other_text = models.CharField(
        max_length=50, blank=True,
        verbose_name=_("Color (custom)"),
    )
    condition = models.CharField(
        max_length=20, choices=CONDITION_CHOICES, default='used',
    )
    defects = models.CharField(
        max_length=50, choices=DEFECT_CHOICES, default='none',
    )
    steering = models.CharField(max_length=10, choices=STEERING_CHOICES, blank=True)

    technical_inspection_month = models.IntegerField(null=True, blank=True)
    technical_inspection_year = models.IntegerField(null=True, blank=True)

    vin = models.CharField(max_length=17, blank=True)
    registration_number = models.CharField(max_length=20, blank=True)
    origin_country = models.CharField(max_length=2, choices=COUNTRY_CHOICES, blank=True)

    price = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    negotiable = models.BooleanField(default=False)
    open_to_trade = models.BooleanField(default=False, verbose_name=_("Open to trade"))
    price_excludes_vat = models.BooleanField(
        default=False, verbose_name=_("Price excludes VAT"),
    )

    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES, default='US')
    state = models.CharField(max_length=2, choices=US_STATE_CHOICES, blank=True)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=200, blank=True)
    hide_exact_address = models.BooleanField(default=False)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    features = models.TextField(blank=True)
    video_url = models.URLField(blank=True)

    is_business_seller = models.BooleanField(default=False, verbose_name=_("Business seller"))

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_shadow_banned = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views_count = models.IntegerField(default=0)
    impressions_count = models.IntegerField(default=0)

    star_level = models.IntegerField(choices=STAR_LEVEL_CHOICES, default=0)
    star_count = models.IntegerField(default=0)
    star_expires_at = models.DateTimeField(null=True, blank=True)
    last_boosted_at = models.DateTimeField(null=True, blank=True)
    highlight_until = models.DateTimeField(null=True, blank=True, help_text="Listing card has highlighted background until this date")
    highlight_until = models.DateTimeField(null=True, blank=True, help_text="Listing card has highlighted background until this date")
    featured_until = models.DateTimeField(null=True, blank=True, help_text="Featured on homepage (Day's deals tab) until this date")

    activated_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    last_reminder_sent_at = models.DateTimeField(null=True, blank=True)
    last_no_sale_reminder_at = models.DateTimeField(null=True, blank=True)
    last_expired_reminder_at = models.DateTimeField(null=True, blank=True)
    first_views_notified_at = models.DateTimeField(null=True, blank=True)
    last_views_milestone = models.IntegerField(default=0)
    photo_tips_sent_at = models.DateTimeField(null=True, blank=True)
    last_draft_reminder_at = models.DateTimeField(null=True, blank=True)
    draft_reminder_count = models.IntegerField(default=0)

    reservation_note = models.CharField(max_length=200, blank=True)
    sold_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name=_("Truck")
        verbose_name_plural = "Trucks"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['subcategory', 'status']),
            models.Index(fields=['brand', 'model']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('truck_detail', kwargs={'pk': self.pk})

    def get_country_display_name(self):
        return dict(self.COUNTRY_CHOICES).get(self.country, self.country)

    def get_state_display_name(self):
        return dict(self.US_STATE_CHOICES).get(self.state, self.state)

    def get_display_location(self):
        parts = []
        if self.city:
            parts.append(self.city)
        if self.country == 'US' and self.state:
            parts.append(self.get_state_display_name())
        if self.country:
            parts.append(self.get_country_display_name())
        return ', '.join(parts)

    def get_full_address(self):
        parts = []
        if self.address:
            parts.append(self.address)
        if self.postal_code:
            parts.append(self.postal_code)
        if self.city:
            parts.append(self.city)
        if self.country == 'US' and self.state:
            parts.append(self.get_state_display_name())
        if self.country:
            parts.append(self.get_country_display_name())
        return ', '.join(parts)

    def get_color_display_value(self):
        if self.color == 'other' and self.color_other_text:
            return self.color_other_text
        return self.get_color_display() if self.color else ''

    def get_truck_type_display_value(self):
        if not self.truck_type:
            return ''
        return dict(self.TRUCK_TYPE_CHOICES).get(self.truck_type, self.truck_type)

    @property
    def display_brand(self):
        return self.brand

    @property
    def display_model(self):
        return self.model

    @property
    def is_truck(self):
        return True

    @property
    def currency_symbol(self):
        return self.CURRENCY_SYMBOLS.get(self.currency, '$')

    def is_star_active(self):
        if self.star_level == 0 or not self.star_expires_at:
            return False
        return self.star_expires_at > timezone.now()

    @property
    def is_highlighted(self):
        """Check if listing should display with highlighted background."""
        if not self.highlight_until:
            return False
        return self.highlight_until > timezone.now()

    def get_effective_star_level(self):
        return self.star_level if self.is_star_active() else 0

    def activate_stars(self, level):
        if level not in self.STAR_DURATIONS:
            return False
        self.star_level = level
        self.star_expires_at = timezone.now() + timedelta(days=self.STAR_DURATIONS[level])
        self.save(update_fields=['star_level', 'star_expires_at'])
        return True

    def deactivate_stars(self):
        self.star_level = 0
        self.star_expires_at = None
        self.save(update_fields=['star_level', 'star_expires_at'])

    def can_boost(self):
        if not self.last_boosted_at:
            return True
        return timezone.now() - self.last_boosted_at >= timedelta(hours=self.BOOST_COOLDOWN_HOURS)

    def get_seconds_until_next_boost(self):
        if self.can_boost():
            return 0
        available_at = self.last_boosted_at + timedelta(hours=self.BOOST_COOLDOWN_HOURS)
        return max(0, int((available_at - timezone.now()).total_seconds()))

    def apply_boost(self):
        if not self.can_boost():
            return False
        self.last_boosted_at = timezone.now()
        self.save(update_fields=['last_boosted_at'])
        return True

    def is_recently_boosted(self):
        if not self.last_boosted_at:
            return False
        return timezone.now() - self.last_boosted_at < timedelta(hours=24)

    @property
    def show_renewed_badge(self):
        if not self.last_boosted_at:
            return False
        return (timezone.now() - self.last_boosted_at) < timedelta(hours=self.RENEWED_BADGE_HOURS)

    def is_new_listing(self, days=3):
        if not self.created_at:
            return False
        return timezone.now() - self.created_at < timedelta(days=days)

    def get_sort_priority(self):
        level = self.get_effective_star_level()
        if level == 2: return 500
        if level == 1: return 400
        if self.is_recently_boosted(): return 300
        if self.is_new_listing(): return 200
        return 100

    @property
    def is_expired(self):
        return self.expires_at and self.expires_at < timezone.now()

    @property
    def days_until_expiry(self):
        if not self.expires_at:
            return None
        return max(0, (self.expires_at - timezone.now()).days)

    @property
    def hours_until_expiry(self):
        if not self.expires_at:
            return None
        return max(0, int((self.expires_at - timezone.now()).total_seconds() // 3600))

    @property
    def days_since_expired(self):
        if not self.expires_at or self.expires_at > timezone.now():
            return None
        return (timezone.now() - self.expires_at).days

    @property
    def is_sold(self):
        return self.status == 'sold'

    @property
    def days_since_sold(self):
        return (timezone.now() - self.sold_at).days if self.sold_at else None

    @property
    def sold_days_remaining(self):
        if not self.sold_at:
            return None
        return max(0, self.SOLD_DISPLAY_DAYS - self.days_since_sold)

    @property
    def should_auto_delete_sold(self):
        if self.status != 'sold' or not self.sold_at:
            return False
        return (timezone.now() - self.sold_at) >= timedelta(days=self.SOLD_DISPLAY_DAYS)

    def mark_as_sold(self):
        self.status = 'sold'
        self.sold_at = timezone.now()
        self.save(update_fields=['status', 'sold_at'])

    def activate(self, days=None):
        if days is None:
            days = self.DEFAULT_ACTIVE_DAYS
        self.status = 'active'
        self.activated_at = timezone.now()
        self.expires_at = timezone.now() + timedelta(days=days)
        self.last_reminder_sent_at = None
        self.last_no_sale_reminder_at = None
        self.last_expired_reminder_at = None
        self.last_draft_reminder_at = None
        self.draft_reminder_count = 0
        self.save(update_fields=[
            'status', 'activated_at', 'expires_at',
            'last_reminder_sent_at', 'last_no_sale_reminder_at',
            'last_expired_reminder_at',
            'last_draft_reminder_at', 'draft_reminder_count',
        ])
        return True

    def mark_expired(self):
        self.status = 'expired'
        self.last_reminder_sent_at = None
        self.save(update_fields=['status', 'last_reminder_sent_at'])

    def reserve(self, note=''):
        self.status = 'reserved'
        self.reservation_note = note
        self.save(update_fields=['status', 'reservation_note'])

    def unreserve(self):
        if self.expires_at and self.expires_at > timezone.now():
            self.status = 'active'
        else:
            self.status = 'expired'
        self.reservation_note = ''
        self.save(update_fields=['status', 'reservation_note'])

    def needs_expiry_reminder(self):
        if not self.expires_at:
            return False
        now = timezone.now()
        if self.status == 'active':
            if self.last_reminder_sent_at:
                return False
            d = self.days_until_expiry
            return d is not None and d <= self.EXPIRY_REMINDER_DAYS
        if self.status == 'expired':
            if self.last_reminder_sent_at:
                return now - self.last_reminder_sent_at >= timedelta(days=self.POST_EXPIRY_REMINDER_INTERVAL_DAYS)
            return True
        return False

    @property
    def should_auto_delete(self):
        if self.status != 'expired' or not self.expires_at:
            return False
        return (timezone.now() - self.expires_at) >= timedelta(days=self.AUTO_DELETE_AFTER_EXPIRY_DAYS)

    @classmethod
    def calculate_listing_fee(cls, price):
        try:
            price = float(price or 0)
        except (TypeError, ValueError):
            price = 0
        for threshold, fee in cls.PRICING_TIERS:
            if price < threshold:
                return fee
        return cls.PRICING_TIERS[-1][1]

    @property
    def listing_fee(self):
        return self.calculate_listing_fee(self.price)

    @property
    def click_through_rate(self):
        if not self.impressions_count:
            return 0.0
        return round((self.views_count / self.impressions_count) * 100, 1)

    @property
    def save_rate(self):
        if not self.views_count:
            return 0.0
        return round((self.saved_by.count() / self.views_count) * 100, 1)

    def get_position(self):
        from django.db.models import Case, When, IntegerField, Value
        if self.status != 'active' or self.is_shadow_banned:
            return None, None
        now = timezone.now()
        three_days_ago = now - timedelta(days=3)
        boost_cutoff = now - timedelta(hours=24)
        all_active = Truck.objects.filter(
            status='active', is_shadow_banned=False,
            subcategory=self.subcategory,
        ).annotate(
            sort_priority=Case(
                When(star_level=2, star_expires_at__gt=now, then=Value(500)),
                When(star_level=1, star_expires_at__gt=now, then=Value(400)),
                When(last_boosted_at__gt=boost_cutoff, then=Value(300)),
                When(created_at__gt=three_days_ago, then=Value(200)),
                default=Value(100),
                output_field=IntegerField(),
            )
        ).order_by('-sort_priority', '-created_at')
        total = all_active.count()
        my_priority = self.get_sort_priority()
        higher = all_active.filter(sort_priority__gt=my_priority).count()
        same = all_active.filter(
            sort_priority=my_priority, created_at__gt=self.created_at,
        ).count()
        return higher + same + 1, total


class TruckImage(models.Model):
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='trucks/%Y/%m/')
    caption = models.CharField(max_length=200, blank=True)
    is_main = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-is_main']
        verbose_name=_("Truck Image")
        verbose_name_plural = "Truck Images"

    def __str__(self):
        return f"{self.truck.title} - {self.order}"


class TruckEquipment(models.Model):
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE, related_name='equipment_items')
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['truck', 'equipment']
        verbose_name=_("Truck Equipment Selection")
        verbose_name_plural = "Truck Equipment Selections"

    def __str__(self):
        return f"{self.truck.title} - {self.equipment.name}"


class SavedTruck(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_trucks')
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'truck']
        ordering = ['-saved_at']
        verbose_name=_("Saved Truck")
        verbose_name_plural = "Saved Trucks"


class SavedTruckNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='truck_save_notifications')
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE, related_name='save_notifications')
    notified_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'truck']
        ordering = ['-notified_at']


class TruckView(models.Model):
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE, related_name='view_records')
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='truck_views',
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-viewed_at']
        indexes = [models.Index(fields=['truck', 'viewed_at'])]


class TruckImpression(models.Model):
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE, related_name='impression_records')
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='truck_impressions',
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    shown_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-shown_at']
        indexes = [models.Index(fields=['truck', 'shown_at'])]


class TruckSalesRecord(models.Model):
    seller = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name='truck_sales_records',
    )
    seller_email = models.EmailField(blank=True)
    truck_id = models.IntegerField(null=True, blank=True)
    subcategory = models.CharField(max_length=30, blank=True)
    brand = models.ForeignKey(
        TruckBrand, on_delete=models.SET_NULL, null=True, blank=True,
    )
    model = models.ForeignKey(
        TruckModel, on_delete=models.SET_NULL, null=True, blank=True,
    )
    title = models.CharField(max_length=200)
    year = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=2, blank=True)
    truck_created_at = models.DateTimeField(null=True, blank=True)
    sold_at = models.DateTimeField(auto_now_add=True, db_index=True)
    days_active = models.IntegerField(default=0)
    views_count = models.IntegerField(default=0)
    impressions_count = models.IntegerField(default=0)
    saves_count = models.IntegerField(default=0)
    marked_sold = models.BooleanField(default=False)

    class Meta:
        ordering = ['-sold_at']
        indexes = [
            models.Index(fields=['-sold_at']),
            models.Index(fields=['seller', '-sold_at']),
        ]
        verbose_name=_("Truck Sales Record")
        verbose_name_plural = "Truck Sales Records"

    def __str__(self):
        return f"{self.title} sold {self.currency} {self.price}"

    @property
    def currency_symbol(self):
        return {'USD': '$', 'EUR': '€', 'GBP': '£'}.get(self.currency, '$')

    @classmethod
    def create_from_truck(cls, truck, marked_sold=False):
        days_active = 0
        if truck.activated_at:
            days_active = (timezone.now() - truck.activated_at).days
        return cls.objects.create(
            seller=truck.seller,
            seller_email=truck.seller.email if truck.seller else '',
            truck_id=truck.pk,
            subcategory=truck.subcategory,
            brand=truck.brand,
            model=truck.model,
            title=truck.title,
            year=truck.year,
            price=truck.price,
            currency=truck.currency,
            city=truck.city,
            country=truck.country,
            truck_created_at=truck.created_at,
            days_active=days_active,
            views_count=truck.views_count or 0,
            impressions_count=truck.impressions_count or 0,
            saves_count=truck.saved_by.count(),
            marked_sold=marked_sold,
        )





# ═══════════════════════════════════════════════════════════════════════════

# PART CATEGORY — Single part / parts kit srauto kategorijų medis

# (Lighting → Rear Lights → Rear Light Bulb)

# ═══════════════════════════════════════════════════════════════════════════





class PartCategory(models.Model):

    """

    Self-referencing hierarchija auto dalims (Single part flow).

    Trys lygiai:

      0 = TOP CATEGORY  (Lighting, Engine, Brakes...)

      1 = GROUP         (Rear Lights, Front Lights...)

      2 = SUBCATEGORY   (Rear Light Bulb — galutinis pasirinkimas)

    """



    LEVEL_CATEGORY = 0

    LEVEL_GROUP = 1

    LEVEL_SUBCATEGORY = 2

    LEVEL_CHOICES = (

        (LEVEL_CATEGORY, "Category"),

        (LEVEL_GROUP, "Group"),

        (LEVEL_SUBCATEGORY, "Subcategory"),

    )



    name_en = models.CharField(max_length=120)

    name_lt = models.CharField(max_length=120, blank=True)

    slug = models.SlugField(max_length=140, unique=True)

    parent = models.ForeignKey(

        "self",

        null=True,

        blank=True,

        related_name="children",

        on_delete=models.CASCADE,

    )

    level = models.PositiveSmallIntegerField(

        choices=LEVEL_CHOICES,

        default=LEVEL_CATEGORY,

    )

    icon = models.CharField(max_length=50, blank=True)

    order = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)



    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)



    class Meta:

        ordering = ["level", "order", "name_en"]

        verbose_name=_("Part Category")

        verbose_name_plural = "Part Categories"

        indexes = [

            models.Index(fields=["level", "parent"]),

            models.Index(fields=["slug"]),

        ]



    def __str__(self):

        prefix = {0: "📁", 1: "📂", 2: "📄"}.get(self.level, "")

        return f"{prefix} {self.name_en}"



    @property

    def is_subcategory(self):

        return self.level == self.LEVEL_SUBCATEGORY



    def get_top_category(self):

        node = self

        while node.parent_id is not None:

            node = node.parent

        return node



    def breadcrumb(self):

        chain = []

        node = self

        while node is not None:

            chain.insert(0, node)

            node = node.parent

        return chain



    def breadcrumb_text(self, separator=" › "):

        return separator.join(n.name_en for n in self.breadcrumb())

WHEEL_PURPOSE_CHOICES = [
    ('passenger', _('Passenger cars')),
    ('suv', _('SUV / Off-road')),
    ('commercial', _('Commercial / Van')),
    ('truck', _('Trucks')),
    ('moto', _('Motorcycles')),
    ('industrial', _('Industrial')),
]
 
# Padangų plotis (mm) — 125..355 žingsniu 10
TYRE_WIDTH_CHOICES = [(str(w), str(w)) for w in range(125, 356, 10)]
 
# Padangų profilis / aukštis (%)
TYRE_PROFILE_CHOICES = [
    (str(p), str(p)) for p in
    [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85]
]
 
# Skersmuo (R) — bendras padangoms ir ratlankiams
WHEEL_DIAMETER_CHOICES = [(str(d), f'R{d}') for d in range(10, 25)]  # R10..R24
 
TYRE_SEASON_CHOICES = [
    ('summer', _('Summer')),
    ('winter', _('Winter')),
    ('all_season', _('All-season')),
]
 
TYRE_SPEED_CHOICES = [
    (c, c) for c in ['J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S',
                     'T', 'U', 'H', 'V', 'W', 'Y', 'Z']
]
 
# Protektoriaus gylis (mm) — dropdown 1..10
TYRE_TREAD_CHOICES = [(str(x), f'{x} mm') for x in range(1, 11)]
 
# Padangų likutis (%) — dropdown 10..100 žingsniu 10
TYRE_REMAINING_CHOICES = [(str(p), f'{p}%') for p in range(10, 101, 10)]
 
# Pagaminimo metai (DOT) — dropdown (paskutiniai 20 metų)
import datetime as _dt
_YR = _dt.date.today().year
TYRE_DOT_YEAR_CHOICES = [(str(y), str(y)) for y in range(_YR, _YR - 21, -1)]
 
# ─── Ratlankiai ─────────────────────────────────────────────
RIM_WIDTH_CHOICES = [
    (f'{w/2:.1f}'.rstrip('0').rstrip('.'), f'{w/2:.1f}'.rstrip('0').rstrip('.') + 'J')
    for w in range(8, 27)  # 4.0J .. 13.0J
]
 
RIM_PCD_CHOICES = [
    (v, v) for v in [
        '3x98', '4x98', '4x100', '4x108', '4x114.3',
        '5x98', '5x100', '5x108', '5x110', '5x112', '5x114.3',
        '5x115', '5x118', '5x120', '5x127', '5x130', '5x139.7',
        '6x114.3', '6x130', '6x139.7', '8x165.1', '8x170',
    ]
]
 
RIM_BOLT_COUNT_CHOICES = [(str(n), str(n)) for n in [3, 4, 5, 6, 8, 10]]
 
# Ratlankių „Tipas" — 7 reikšmės pagal autogidas etaloną (sec 11).
# Stulpelis istoriškai vadinasi `rim_material`, nors etalone laukas yra
# „Tipas": jis maišo medžiagą (lydinio / štampuoti / kalti) su gaminio
# rūšimi (priedai / atsarginis ratas / gaubtai / dangteliai). Stulpelio
# nepervadinam — jis minimas 7 gyvuose failuose (naršymas, išplėstinė
# paieška, panelė), o pervadinimas nieko vartotojui neduotų.
# „Steel" msgid nenaudojam: jis bendras su laivų korpuso medžiaga.
RIM_MATERIAL_CHOICES = [
    ('accessory', _('Accessories')),
    ('alloy', _('Alloy')),
    ('steel', _('Stamped steel')),
    ('forged', _('Forged')),
    ('spare', _('Spare wheel')),
    ('hubcap', _('Wheel covers')),
    ('centercap', _('Centre caps')),
]
 
WHEEL_CONDITION_CHOICES = [
    ('new', _('New')),
    ('used', _('Used')),
]
 
WHEEL_STATUS_CHOICES = [
    ('draft', _('Draft')),
    ('active', _('Active')),
    ('reserved', _('Reserved')),
    ('sold', _('Sold')),
    ('expired', _('Expired')),
    ('archived', _('Archived')),
]
 
WHEEL_DEFAULT_ACTIVE_DAYS = 30
WHEEL_SOLD_DISPLAY_DAYS = 7
WHEEL_AUTO_DELETE_AFTER_EXPIRY_DAYS = 160
 
 
class WheelListing(models.Model):
    """Tyres + Rims vienoje lentelėje. product_type skiria."""
 
    PRODUCT_TYPE_CHOICES = [
        ('tyre', _('Tyres')),
        ('rim', _('Rims')),
    ]
 
    DEFAULT_ACTIVE_DAYS = WHEEL_DEFAULT_ACTIVE_DAYS
    SOLD_DISPLAY_DAYS = WHEEL_SOLD_DISPLAY_DAYS
    AUTO_DELETE_AFTER_EXPIRY_DAYS = WHEEL_AUTO_DELETE_AFTER_EXPIRY_DAYS
 
    COUNTRY_CHOICES = Listing.COUNTRY_CHOICES
    US_STATE_CHOICES = Listing.US_STATE_CHOICES
 
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='wheel_listings',
    )
    product_type = models.CharField(max_length=8, choices=PRODUCT_TYPE_CHOICES, db_index=True)
 
    # ─── Bendri ───
    title = models.CharField(max_length=200, blank=True)
    brand_name = models.CharField(max_length=80, blank=True)   # Manufacturer (Nokian, BBS...)
    model_name = models.CharField(max_length=80, blank=True)
    purpose = models.CharField(max_length=20, choices=WHEEL_PURPOSE_CHOICES, blank=True, db_index=True)
    diameter = models.CharField(max_length=4, choices=WHEEL_DIAMETER_CHOICES, blank=True, db_index=True)  # R
    condition = models.CharField(max_length=8, choices=WHEEL_CONDITION_CHOICES, default='used')
    quantity = models.PositiveSmallIntegerField(default=4)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    negotiable = models.BooleanField(default=False)
    description = models.TextField(blank=True)
 
    # ─── Padangoms (product_type='tyre') ───
    tyre_width = models.CharField(max_length=4, choices=TYRE_WIDTH_CHOICES, blank=True, db_index=True)
    tyre_profile = models.CharField(max_length=4, choices=TYRE_PROFILE_CHOICES, blank=True, db_index=True)
    tyre_season = models.CharField(max_length=12, choices=TYRE_SEASON_CHOICES, blank=True, db_index=True)
    tyre_speed_index = models.CharField(max_length=2, choices=TYRE_SPEED_CHOICES, blank=True)
    tyre_load_index = models.CharField(max_length=6, blank=True)
    tyre_tread_mm = models.CharField(max_length=4, choices=TYRE_TREAD_CHOICES, blank=True)      # Tread depth mm
    tyre_remaining_pct = models.CharField(max_length=4, choices=TYRE_REMAINING_CHOICES, blank=True)  # Padangų likutis %
    tyre_dot_year = models.CharField(max_length=4, choices=TYRE_DOT_YEAR_CHOICES, blank=True)   # Production year
 
    # ─── Tyre Features (autogidas "Ypatumai") ───
    feat_spare_thin = models.BooleanField(default=False)   # Spare tyre "thin"
    feat_sold_single = models.BooleanField(default=False)  # Sold individually
    feat_sport = models.BooleanField(default=False)        # Sport tyres
    feat_suv = models.BooleanField(default=False)          # SUV tyres
    feat_rain = models.BooleanField(default=False)         # Rain tyres
    feat_run_flat = models.BooleanField(default=False)     # Run on flat
    feat_reinforced = models.BooleanField(default=False)   # Reinforced
    feat_studded = models.BooleanField(default=False)      # Studded winter
 
    # ─── Ratlankiams (product_type='rim') ───
    rim_width = models.CharField(max_length=6, choices=RIM_WIDTH_CHOICES, blank=True, db_index=True)  # J
    rim_pcd = models.CharField(max_length=12, choices=RIM_PCD_CHOICES, blank=True, db_index=True)
    rim_bolt_count = models.CharField(max_length=2, choices=RIM_BOLT_COUNT_CHOICES, blank=True)
    rim_et = models.IntegerField(null=True, blank=True)
    rim_dia = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    rim_material = models.CharField(max_length=16, choices=RIM_MATERIAL_CHOICES, blank=True)

    # Ypatumai (etalonas sec 11) — iki šiol formoje buvo rodomi, bet
    # modelyje neegzistavo, todėl view'as juos praleisdavo per hasattr()
    # ir vartotojo pažymėtos varnelės tyliai dingdavo.
    # feat_sold_single („Parduodu po vieną") jau yra aukščiau — bendras su padangomis.
    rim_feat_bent = models.BooleanField(default=False)      # Aplankstyti ratlankiai
    rim_feat_original = models.BooleanField(default=False)  # Originalūs ratlankiai
    rim_feat_with_tyres = models.BooleanField(default=False)  # Su padangom
    rim_feat_chromed = models.BooleanField(default=False)   # Chromuoti

    # „Ratlankiai tinkami markei" — etalone atskira sekcija; pas mus
    # laisvas tekstas (formoje maxlength=200). Irgi nebuvo saugomas.
    fits_brands = models.CharField(max_length=200, blank=True, default='')
 
    # ─── Lokacija + kontaktai ───
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES, default='LT')
    state = models.CharField(max_length=64, blank=True)
    city = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    contact_phone = models.CharField(max_length=30, blank=True)
    contact_email = models.EmailField(blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
 
    # ─── Marketplace (star / boost / expires) ───
    status = models.CharField(max_length=12, choices=WHEEL_STATUS_CHOICES, default='draft', db_index=True)
    star_level = models.PositiveSmallIntegerField(default=0)
    star_count = models.PositiveSmallIntegerField(default=0)
    star_expires_at = models.DateTimeField(null=True, blank=True)
    last_boosted_at = models.DateTimeField(null=True, blank=True)
    featured_until = models.DateTimeField(null=True, blank=True)
    highlight_until = models.DateTimeField(null=True, blank=True)
    is_shadow_banned = models.BooleanField(default=False)
 
    views_count = models.PositiveIntegerField(default=0)
    impressions_count = models.PositiveIntegerField(default=0)
 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    activated_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    sold_at = models.DateTimeField(null=True, blank=True)
 
    class Meta:
        verbose_name=_("Wheel Listing")
        verbose_name_plural = "Wheel Listings"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['product_type', 'status']),
            models.Index(fields=['tyre_width', 'tyre_profile', 'diameter']),
            models.Index(fields=['rim_width', 'diameter', 'rim_pcd']),
        ]
 
    def __str__(self):
        if self.product_type == 'tyre':
            return f'{self.tyre_width}/{self.tyre_profile} {self.diameter} ({self.brand_name})'
        return f'{self.diameter}x{self.rim_width} {self.rim_pcd} ({self.brand_name})'
 
    def get_absolute_url(self):
        return reverse('wheels_detail', kwargs={'pk': self.pk})
 
    @property
    def currency_symbol(self):
        return '$' if self.country == 'US' else '€'
 
    def build_title(self):
        if self.product_type == 'tyre':
            size = f'{self.tyre_width}/{self.tyre_profile} {self.diameter}'
            return f'{self.brand_name} {size}'.strip()
        size = f'{self.diameter}x{self.rim_width} {self.rim_pcd}'
        return f'{self.brand_name} {size}'.strip()
 
    def activate(self, days=None):
        if days is None:
            days = self.DEFAULT_ACTIVE_DAYS
        now = timezone.now()
        self.status = 'active'
        self.activated_at = now
        self.expires_at = now + timedelta(days=days)
        if not self.title:
            self.title = self.build_title()
        self.save()
        return True

    # ─── Galiojimas (ta pati logika kaip Listing/Truck) ───

    @property
    def is_expired(self):
        return self.expires_at and self.expires_at < timezone.now()

    @property
    def days_until_expiry(self):
        if not self.expires_at:
            return None
        return max(0, (self.expires_at - timezone.now()).days)

    @property
    def days_since_expired(self):
        if not self.expires_at or self.expires_at > timezone.now():
            return None
        return (timezone.now() - self.expires_at).days

    def mark_expired(self):
        # WheelListing neturi last_reminder_sent_at lauko, tad tik status.
        self.status = 'expired'
        self.save(update_fields=['status'])

    @property
    def should_auto_delete(self):
        if self.status != 'expired' or not self.expires_at:
            return False
        return (timezone.now() - self.expires_at) >= timedelta(
            days=self.AUTO_DELETE_AFTER_EXPIRY_DAYS
        )

    def is_star_active(self):
        return (self.star_level > 0 and self.star_expires_at
                and self.star_expires_at > timezone.now())
 
 
class WheelImage(models.Model):
    listing = models.ForeignKey(WheelListing, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='wheels/%Y/%m/')
    is_main = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)
 
    class Meta:
        ordering = ['order', '-is_main']
        verbose_name=_("Wheel Image")
        verbose_name_plural = "Wheel Images"
 
 
class SavedWheelListing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_wheels')
    listing = models.ForeignKey(WheelListing, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)
 
    class Meta:
        unique_together = ('user', 'listing')
        ordering = ['-saved_at']

