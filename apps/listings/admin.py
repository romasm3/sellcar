from django.contrib import admin
from .models import (
    VehicleType,
    Brand,
    Model,
    FuelType,
    Transmission,
    Listing,
    ListingImage,
    SavedListing,
)


@admin.register(VehicleType)
class VehicleTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]


@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ["name", "brand", "slug"]
    list_filter = ["brand"]
    search_fields = ["name", "brand__name"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(FuelType)
class FuelTypeAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Transmission)
class TransmissionAdmin(admin.ModelAdmin):
    list_display = ["name"]


class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 1
    fields = ["image", "caption", "is_main"]


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "seller",
        "brand",
        "model",
        "year",
        "price",
        "status",
        "views",
        "created_at",
    ]
    list_filter = [
        "status",
        "vehicle_type",
        "brand",
        "fuel_type",
        "transmission",
        "condition",
        "created_at",
    ]
    search_fields = ["title", "description", "seller__username", "vin"]
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ["views", "created_at", "updated_at"]
    inlines = [ListingImageInline]

    fieldsets = (
        (
            "Pagrindinė informacija",
            {
                "fields": (
                    "seller",
                    "vehicle_type",
                    "brand",
                    "model",
                    "title",
                    "slug",
                    "description",
                    "status",
                )
            },
        ),
        (
            "Techninės specifikacijos",
            {
                "fields": (
                    "year",
                    "mileage",
                    "fuel_type",
                    "transmission",
                    "engine_capacity",
                    "power",
                    "color",
                    "condition",
                    "vin",
                    "registration_number",
                    "first_registration",
                )
            },
        ),
        ("Kaina", {"fields": ("price", "negotiable")}),
        ("Vieta", {"fields": ("city", "address", "latitude", "longitude")}),
        ("Papildoma informacija", {"fields": ("features",)}),
        ("Meta", {"fields": ("views", "created_at", "updated_at")}),
    )


@admin.register(ListingImage)
class ListingImageAdmin(admin.ModelAdmin):
    list_display = ["listing", "is_main", "uploaded_at"]
    list_filter = ["is_main", "uploaded_at"]
    search_fields = ["listing__title", "caption"]


@admin.register(SavedListing)
class SavedListingAdmin(admin.ModelAdmin):
    list_display = ["user", "listing", "saved_at"]
    list_filter = ["saved_at"]
    search_fields = ["user__username", "listing__title"]
