from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify


class VehicleType(models.Model):
    """Vehicle Type"""

    name = models.CharField(max_length=50, unique=True, verbose_name="Name")
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Vehicle Type"
        verbose_name_plural = "Vehicle Types"


class Brand(models.Model):
    """Brand"""

    name = models.CharField(max_length=100, unique=True, verbose_name="Name")
    slug = models.SlugField(max_length=100, unique=True)
    logo = models.ImageField(upload_to="brands/", blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"
        ordering = ["name"]


class Model(models.Model):
    """Model"""

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="models")
    name = models.CharField(max_length=100, verbose_name="Name")
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return f"{self.brand.name} {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Model"
        verbose_name_plural = "Models"
        ordering = ["name"]
        unique_together = ["brand", "name"]


class FuelType(models.Model):
    """Fuel Type"""

    FUEL_CHOICES = [
        ("petrol", "Petrol"),
        ("diesel", "Diesel"),
        ("electric", "Electric"),
        ("hybrid", "Hybrid"),
        ("lpg", "LPG"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=50, choices=FUEL_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()

    class Meta:
        verbose_name = "Fuel Type"
        verbose_name_plural = "Fuel Types"


class Transmission(models.Model):
    """Transmission"""

    TRANSMISSION_CHOICES = [
        ("manual", "Manual"),
        ("automatic", "Automatic"),
        ("semi_automatic", "Semi-Automatic"),
    ]

    name = models.CharField(max_length=50, choices=TRANSMISSION_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()

    class Meta:
        verbose_name = "Transmission"
        verbose_name_plural = "Transmissions"


class Listing(models.Model):
    """Listing"""

    STATUS_CHOICES = [
        ("active", "Active"),
        ("sold", "Sold"),
        ("reserved", "Reserved"),
        ("inactive", "Inactive"),
    ]

    CONDITION_CHOICES = [
        ("new", "New"),
        ("used", "Used"),
        ("damaged", "Damaged"),
    ]

    # Basic information
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="listings"
    )
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.PROTECT)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    model = models.ForeignKey(Model, on_delete=models.PROTECT)

    title = models.CharField(max_length=200, verbose_name="Title")
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    description = models.TextField(verbose_name="Description")

    # Technical specifications
    year = models.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2030)],
        verbose_name="Year",
    )
    mileage = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name="Mileage (km)",
        help_text="Kilometers",
    )
    fuel_type = models.ForeignKey(
        FuelType, on_delete=models.PROTECT, verbose_name="Fuel Type"
    )
    transmission = models.ForeignKey(
        Transmission, on_delete=models.PROTECT, verbose_name="Transmission"
    )
    engine_capacity = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        validators=[MinValueValidator(0)],
        verbose_name="Engine Capacity (L)",
        blank=True,
        null=True,
    )
    power = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name="Power (kW)",
        blank=True,
        null=True,
    )
    color = models.CharField(max_length=50, verbose_name="Color", blank=True)
    condition = models.CharField(
        max_length=20,
        choices=CONDITION_CHOICES,
        default="used",
        verbose_name="Condition",
    )

    # VIN and registration
    vin = models.CharField(max_length=17, blank=True, verbose_name="VIN Code")
    registration_number = models.CharField(
        max_length=20, blank=True, verbose_name="Registration Number"
    )
    first_registration = models.DateField(
        blank=True, null=True, verbose_name="First Registration"
    )

    # Price
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Price (€)",
    )
    negotiable = models.BooleanField(default=False, verbose_name="Negotiable")

    # Location
    city = models.CharField(max_length=100, verbose_name="City")
    address = models.CharField(max_length=255, blank=True, verbose_name="Address")
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True, verbose_name="Latitude"
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True, verbose_name="Longitude"
    )

    # Status
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="active", verbose_name="Status"
    )

    # Additional information
    features = models.TextField(
        blank=True, verbose_name="Features", help_text="Separate with commas"
    )

    # Meta
    views = models.IntegerField(default=0, verbose_name="Views")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.brand.name} {self.model.name} {self.year}")
            slug = base_slug
            counter = 1
            while Listing.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_main_image(self):
        """Get main image"""
        main_image = self.images.filter(is_main=True).first()
        if main_image:
            return main_image.image.url
        first_image = self.images.first()
        if first_image:
            return first_image.image.url
        return None

    class Meta:
        verbose_name = "Listing"
        verbose_name_plural = "Listings"
        ordering = ["-created_at"]


class ListingImage(models.Model):
    """Listing Image"""

    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="listings/%Y/%m/%d/", verbose_name="Image")
    is_main = models.BooleanField(default=False, verbose_name="Main Image")
    caption = models.CharField(max_length=200, blank=True, verbose_name="Caption")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.listing.title} - image {self.id}"

    def save(self, *args, **kwargs):
        # If this is main image, remove main status from others
        if self.is_main:
            ListingImage.objects.filter(listing=self.listing, is_main=True).update(
                is_main=False
            )
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"
        ordering = ["-is_main", "uploaded_at"]


class SavedListing(models.Model):
    """Saved Listing (favorites)"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="saved_listings",
    )
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="saved_by"
    )
    saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.listing.title}"

    class Meta:
        verbose_name = "Saved Listing"
        verbose_name_plural = "Saved Listings"
        unique_together = ["user", "listing"]
        ordering = ["-saved_at"]
