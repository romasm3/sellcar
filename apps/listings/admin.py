from django.contrib import admin
from .models import (
    VehicleType,
    Brand,
    Model,
    FuelType,
    Transmission,
    Listing,
    ListingImage,
    Equipment,
    ListingEquipment,
)


@admin.register(VehicleType)
class VehicleTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'vehicle_type', 'slug']
    list_filter = ['vehicle_type']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'slug']
    list_filter = ['brand']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'brand__name']


@admin.register(FuelType)
class FuelTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Transmission)
class TransmissionAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 1
    fields = ['image', 'caption', 'is_main', 'order']


class ListingEquipmentInline(admin.TabularInline):
    model = ListingEquipment
    extra = 1


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'brand', 'model', 'year', 'price', 'seller', 'status', 'created_at']
    list_filter = ['status', 'vehicle_type', 'brand', 'fuel_type', 'transmission', 'condition']
    search_fields = ['title', 'description', 'vin']
    readonly_fields = ['created_at', 'updated_at', 'views_count']
    inlines = [ListingImageInline, ListingEquipmentInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('seller', 'vehicle_type', 'brand', 'model', 'title', 'status')
        }),
        ('Main Details', {
            'fields': ('year', 'mileage', 'first_registration', 'description')
        }),
        ('Technical Details', {
            'fields': ('fuel_type', 'transmission', 'body_type', 'engine_capacity',
                      'power', 'color', 'doors', 'condition')
        }),
        ('VIN and Registration', {
            'fields': ('vin', 'registration_number')
        }),
        ('Price', {
            'fields': ('price', 'negotiable')
        }),
        ('Location', {
            'fields': ('city', 'address', 'latitude', 'longitude')
        }),
        ('Media', {
            'fields': ('video_url',)
        }),
        ('Features', {
            'fields': ('features',)
        }),
        ('Meta', {
            'fields': ('created_at', 'updated_at', 'views_count'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']
    search_fields = ['name']


@admin.register(ListingImage)
class ListingImageAdmin(admin.ModelAdmin):
    list_display = ['listing', 'order', 'is_main', 'uploaded_at']
    list_filter = ['is_main', 'uploaded_at']
    search_fields = ['listing__title', 'caption']
