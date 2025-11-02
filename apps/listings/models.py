from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class VehicleType(models.Model):
    """Vehicle Type"""
    name = models.CharField(max_length=100, verbose_name="Name")
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Vehicle Type"
        verbose_name_plural = "Vehicle Types"
        ordering = ['name']

    def __str__(self):
        return self.name


class Brand(models.Model):
    """Car Brand"""
    name = models.CharField(max_length=100, verbose_name="Name")
    slug = models.SlugField(unique=True)
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE, related_name='brands')

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"
        ordering = ['name']

    def __str__(self):
        return self.name


class Model(models.Model):
    """Car Model"""
    name = models.CharField(max_length=100, verbose_name="Name")
    slug = models.SlugField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='models')

    class Meta:
        verbose_name = "Model"
        verbose_name_plural = "Models"
        ordering = ['name']
        unique_together = ['brand', 'slug']

    def __str__(self):
        return f"{self.brand.name} {self.name}"


class FuelType(models.Model):
    """Fuel Type"""
    name = models.CharField(max_length=50, verbose_name="Name")

    class Meta:
        verbose_name = "Fuel Type"
        verbose_name_plural = "Fuel Types"
        ordering = ['name']

    def __str__(self):
        return self.name


class Transmission(models.Model):
    """Transmission Type"""
    name = models.CharField(max_length=50, verbose_name="Name")

    class Meta:
        verbose_name = "Transmission"
        verbose_name_plural = "Transmissions"
        ordering = ['name']

    def __str__(self):
        return self.name


class Listing(models.Model):
    """Car Listing"""

    CONDITION_CHOICES = [
        ('new', 'New'),
        ('used', 'Used'),
        ('damaged', 'Damaged'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('sold', 'Sold'),
        ('archived', 'Archived'),
    ]

    BODY_TYPE_CHOICES = [
        ('sedan', 'Sedan'),
        ('hatchback', 'Hatchback'),
        ('wagon', 'Wagon/Estate'),
        ('suv', 'SUV/Crossover'),
        ('van', 'Van/Minivan'),
        ('coupe', 'Coupe'),
        ('convertible', 'Convertible'),
        ('pickup', 'Pickup'),
    ]

    DOOR_CHOICES = [
        ('2/3', '2/3 doors'),
        ('4/5', '4/5 doors'),
    ]

    # Basic Information
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE, verbose_name="Vehicle Type")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name="Brand")
    model = models.ForeignKey(Model, on_delete=models.CASCADE, verbose_name="Model")

    # Main Details
    title = models.CharField(max_length=200, verbose_name="Title")
    description = models.TextField(verbose_name="Description", blank=True)
    year = models.IntegerField(verbose_name="Year")
    mileage = models.IntegerField(verbose_name="Mileage (km)")
    first_registration = models.DateField(verbose_name="First Registration Date", null=True, blank=True)

    # Technical Details
    fuel_type = models.ForeignKey(FuelType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Fuel Type")
    transmission = models.ForeignKey(Transmission, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Transmission")
    body_type = models.CharField(max_length=50, choices=BODY_TYPE_CHOICES, verbose_name="Body Type", blank=True)
    engine_capacity = models.DecimalField(max_digits=4, decimal_places=1, verbose_name="Engine Capacity (L)", null=True, blank=True)
    power = models.IntegerField(verbose_name="Power (kW)", null=True, blank=True)
    color = models.CharField(max_length=50, verbose_name="Color", blank=True)
    doors = models.CharField(max_length=10, choices=DOOR_CHOICES, verbose_name="Number of Doors", blank=True)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, verbose_name="Condition", default='used')

    # VIN and Registration
    vin = models.CharField(max_length=17, verbose_name="VIN Code", blank=True)
    registration_number = models.CharField(max_length=20, verbose_name="Registration Number", blank=True)

    # Price
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (€)")
    negotiable = models.BooleanField(default=False, verbose_name="Price Negotiable")

    # Location
    city = models.CharField(max_length=100, verbose_name="City")
    address = models.CharField(max_length=200, verbose_name="Address", blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    # Features and Description
    features = models.TextField(verbose_name="Additional Features", blank=True,
                                help_text="E.g.: Air conditioning, Alloy wheels")

    # Video
    video_url = models.URLField(verbose_name="Video URL (YouTube)", blank=True)

    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views_count = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Listing"
        verbose_name_plural = "Listings"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('listings:listing_detail', kwargs={'pk': self.pk})


class ListingImage(models.Model):
    """Listing Image"""
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='listings/%Y/%m/', verbose_name="Image")
    caption = models.CharField(max_length=200, blank=True, verbose_name="Caption")
    is_main = models.BooleanField(default=False, verbose_name="Main Image")
    order = models.IntegerField(default=0, verbose_name="Order")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"
        ordering = ['order', '-is_main']

    def __str__(self):
        return f"{self.listing.title} - {self.order}"


class Equipment(models.Model):
    """Vehicle Equipment"""

    CATEGORY_CHOICES = [
        ('interior', 'Interior'),
        ('electronics', 'Electronics'),
        ('safety', 'Safety'),
        ('audio_video', 'Audio/Video'),
        ('exterior', 'Exterior'),
        ('other', 'Other Features'),
    ]

    name = models.CharField(max_length=100, verbose_name="Name")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name="Category")

    class Meta:
        verbose_name = "Equipment"
        verbose_name_plural = "Equipment"
        ordering = ['category', 'name']

    def __str__(self):
        return self.name


class ListingEquipment(models.Model):
    """Listing Equipment Relationship"""
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='equipment_items')
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['listing', 'equipment']
        verbose_name = "Listing Equipment"
        verbose_name_plural = "Listing Equipment"

    def __str__(self):
        return f"{self.listing.title} - {self.equipment.name}"
