from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count, Sum
from datetime import timedelta
from .models import (
    VehicleType,
    SubCategory,
    Brand,
    Model,
    MotorcycleBrand,
    MotorcycleModel,
    FuelType,
    Transmission,
    Listing,
    ListingImage,
    Equipment,
    ListingEquipment,
    EmailScenario,
    PricingPlan,
    # Truck system
    TruckBrand,
    TruckModel,
    Truck,
    TruckImage,
    TruckEquipment,
    SavedTruck,
    SavedTruckNotification,
    TruckView,
    TruckImpression,
    TruckSalesRecord,
)


# ═══════════════════════════════════════════════════════════
# REFERENCE DATA admin (Brand, Model, etc.)
# ═══════════════════════════════════════════════════════════

@admin.register(VehicleType)
class VehicleTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'subcategories_count']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order']
    search_fields = ['name', 'slug']
    ordering = ['order', 'name']

    def subcategories_count(self, obj):
        count = obj.subcategories.count()
        if count == 0:
            return '—'
        return format_html('<strong>{}</strong>', count)
    subcategories_count.short_description = 'Subcategories'


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'vehicle_type', 'slug']
    list_filter = ['vehicle_type']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'vehicle_type__name']
    ordering = ['vehicle_type__name', 'name']
    autocomplete_fields = ['vehicle_type']


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'vehicle_type', 'slug', 'listings_count']
    list_filter = ['vehicle_type']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    ordering = ['name']

    def listings_count(self, obj):
        count = Listing.objects.filter(brand=obj).count()
        if count == 0:
            return '—'
        return format_html('<strong>{}</strong>', count)
    listings_count.short_description = 'Listings'


@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'slug', 'listings_count']
    list_filter = ['brand']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'brand__name']
    ordering = ['brand__name', 'name']

    def listings_count(self, obj):
        count = Listing.objects.filter(model=obj).count()
        if count == 0:
            return '—'
        return format_html('<strong>{}</strong>', count)
    listings_count.short_description = 'Listings'


# ═══════════════════════════════════════════════════════════
# MOTORCYCLE BRANDS / MODELS admin
# ═══════════════════════════════════════════════════════════

@admin.register(MotorcycleBrand)
class MotorcycleBrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'models_count', 'listings_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    ordering = ['name']

    def models_count(self, obj):
        count = obj.models.count()
        if count == 0:
            return '—'
        return format_html('<strong>{}</strong>', count)
    models_count.short_description = 'Models'

    def listings_count(self, obj):
        count = Listing.objects.filter(motorcycle_brand=obj).count()
        if count == 0:
            return '—'
        return format_html('<strong>{}</strong>', count)
    listings_count.short_description = 'Listings'


@admin.register(MotorcycleModel)
class MotorcycleModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'slug', 'listings_count']
    list_filter = ['brand']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'brand__name']
    ordering = ['brand__name', 'name']
    autocomplete_fields = ['brand']

    def listings_count(self, obj):
        count = Listing.objects.filter(motorcycle_model=obj).count()
        if count == 0:
            return '—'
        return format_html('<strong>{}</strong>', count)
    listings_count.short_description = 'Listings'


@admin.register(FuelType)
class FuelTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Transmission)
class TransmissionAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'vehicle_type']
    list_filter = ['category', 'vehicle_type']
    search_fields = ['name']
    ordering = ['category', 'name']
    autocomplete_fields = ['vehicle_type']


# ═══════════════════════════════════════════════════════════
# PRICING PLAN admin — unified pricing
# ═══════════════════════════════════════════════════════════

@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    list_display = (
        'vehicle_type',
        'duration_days',
        'price_display',
        'old_price',
        'discount_percent',
        'is_popular_display',
        'is_active_display',
        'order',
    )
    list_filter = ('vehicle_type', 'is_active', 'is_popular')
    list_editable = ('order',)
    search_fields = ('vehicle_type__name', 'custom_label')
    ordering = ('vehicle_type', 'order', 'duration_days')

    fieldsets = (
        ('Category & Duration', {
            'fields': ('vehicle_type', 'duration_days', 'is_active'),
        }),
        ('Pricing', {
            'fields': ('price', 'old_price', 'discount_percent'),
            'description': (
                'Set price shown to customer. old_price is the crossed-out "value". '
                'discount_percent shows the -X% badge. Leave old_price/discount empty to hide them.'
            ),
        }),
        ('Display', {
            'fields': ('is_popular', 'order', 'custom_label'),
            'description': (
                'is_popular shows "MOST POPULAR" ribbon. '
                'order controls left-to-right placement (lower = left).'
            ),
        }),
        ('Bundled Features', {
            'fields': ('boost_days', 'vip_days', 'homepage_ad_days'),
            'description': 'Free addon days included with this plan.',
        }),
    )

    @admin.display(description='Price', ordering='price')
    def price_display(self, obj):
        return format_html('<strong style="color:#10b981">${}</strong>', obj.price)

    @admin.display(description='Popular', boolean=True)
    def is_popular_display(self, obj):
        return obj.is_popular

    @admin.display(description='Active', boolean=True)
    def is_active_display(self, obj):
        return obj.is_active


# ═══════════════════════════════════════════════════════════
# LISTING admin — core administration tool
# ═══════════════════════════════════════════════════════════

class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 0
    fields = ['image_preview', 'image', 'caption', 'is_main', 'order']
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height: 60px; border-radius: 4px;" />',
                obj.image.url
            )
        return '—'
    image_preview.short_description = 'Preview'


class ListingEquipmentInline(admin.TabularInline):
    model = ListingEquipment
    extra = 0
    autocomplete_fields = ['equipment']


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    # ─── LIST VIEW ───────────────────────────────────────────
    list_display = [
        'id_display',
        'thumbnail',
        'title_link',
        'vehicle_kind',
        'price_display',
        'status_colored',
        'shadow_ban_indicator',
        'seller_email',
        'views_count',
        'saved_count_display',
        'expires_at_display',
        'star_display',
        'created_at',
    ]
    list_display_links = ['title_link']
    list_filter = [
        'status',
        'is_shadow_banned',
        'star_level',
        'vehicle_type',
        'motorcycle_type',
        'fuel_type',
        'transmission',
        'condition',
        'negotiable',
        'country',
        'created_at',
    ]
    search_fields = [
        'id',
        'title',
        'description',
        'vin',
        'seller__email',
        'seller__username',
        'brand__name',
        'model__name',
        'motorcycle_brand__name',
        'motorcycle_model__name',
        'city',
    ]
    list_per_page = 50
    list_select_related = [
        'brand', 'model',
        'motorcycle_brand', 'motorcycle_model',
        'seller', 'vehicle_type', 'fuel_type',
    ]
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

    readonly_fields = [
        'id',
        'created_at',
        'updated_at',
        'views_count',
        'activated_at',
        'last_reminder_sent_at',
    ]

    autocomplete_fields = [
        'brand', 'model',
        'motorcycle_brand', 'motorcycle_model',
        'vehicle_type', 'fuel_type', 'transmission',
    ]
    inlines = [ListingImageInline, ListingEquipmentInline]

    actions = [
        'shadow_ban_listings',
        'remove_shadow_ban',
        'mark_as_active',
        'mark_as_expired',
        'mark_as_reserved',
        'mark_as_archived',
        'extend_by_30_days',
        'activate_one_star',
        'activate_two_stars',
        'deactivate_stars',
        'apply_boost_action',
    ]

    fieldsets = (
        ('🔑 Identification', {
            'fields': ('id', 'seller', 'title', 'status'),
        }),
        ('🚫 Admin Moderation', {
            'fields': ('is_shadow_banned',),
            'description': (
                'Shadow ban: slepia skelbimą nuo public, bet savininkas mato jį kaip ACTIVE. '
                'Naudojama spam, fake photos, fraud atvejais.'
            ),
        }),
        ('🚗 Car Vehicle', {
            'fields': (
                'vehicle_type', 'brand', 'model',
                'year', 'first_registration',
                'vin', 'registration_number',
            ),
            'description': 'For CARS and trucks. Leave empty for motorcycles.',
        }),
        ('🏍️ Motorcycle', {
            'fields': (
                'motorcycle_brand', 'motorcycle_model',
                'motorcycle_type', 'cooling_type',
                'moto_engine_type', 'engine_capacity_cc',
            ),
            'description': 'For MOTORCYCLES only. Leave empty for cars.',
            'classes': ('collapse',),
        }),
        ('🔧 Technical Details (Cars)', {
            'fields': (
                'body_type', 'fuel_type', 'transmission',
                'engine_capacity', 'power',
                'mileage', 'doors', 'condition',
                'color', 'steering', 'drive_type', 'seats',
            ),
            'classes': ('collapse',),
        }),
        ('💵 Price', {
            'fields': ('price', 'currency', 'negotiable'),
        }),
        ('📍 Location', {
            'fields': (
                'country', 'state', 'city',
                'address', 'postal_code',
                'hide_exact_address',
                'latitude', 'longitude',
            ),
            'classes': ('collapse',),
        }),
        ('📝 Content', {
            'fields': ('description', 'video_url', 'defects'),
            'classes': ('collapse',),
        }),
        ('⏱ Lifecycle', {
            'fields': (
                'activated_at',
                'expires_at',
                'last_reminder_sent_at',
                'reservation_note',
            ),
            'description': (
                'activated_at: when the listing went live. '
                'expires_at: when it will be auto-expired. '
                'Use actions below to extend or change status.'
            ),
        }),
        ('⭐ Premium Features', {
            'fields': ('star_level', 'star_expires_at', 'last_boosted_at'),
            'description': (
                'Star levels: 0 = none, 1 = ⭐ (7 days), 2 = ⭐⭐ (30 days). '
                'Leave star_expires_at empty to set manually, '
                'or use Actions menu below to activate automatically.'
            ),
            'classes': ('collapse',),
        }),
        ('📊 Meta', {
            'fields': ('created_at', 'updated_at', 'views_count'),
            'classes': ('collapse',),
        }),
    )

    # ─── LIST DISPLAY HELPERS ────────────────────────────────

    def id_display(self, obj):
        return format_html('<strong>#{}</strong>', obj.id)
    id_display.short_description = 'ID'
    id_display.admin_order_field = 'id'

    def thumbnail(self, obj):
        first_image = obj.images.first()
        if first_image:
            return format_html(
                '<img src="{}" style="width: 60px; height: 45px; object-fit: cover; border-radius: 4px;" />',
                first_image.image.url
            )
        return format_html(
            '<div style="width: 60px; height: 45px; background: #f3f4f6; border-radius: 4px; '
            'display: flex; align-items: center; justify-content: center; color: #9ca3af;">📷</div>'
        )
    thumbnail.short_description = ''

    def title_link(self, obj):
        # Automatiškai rodo teisingą brand/model pagal tipą
        if obj.motorcycle_brand_id:
            brand_name = obj.motorcycle_brand.name if obj.motorcycle_brand else ''
            model_name = obj.motorcycle_model.name if obj.motorcycle_model else ''
        else:
            brand_name = obj.brand.name if obj.brand else ''
            model_name = obj.model.name if obj.model else ''
        return format_html(
            '<strong>{} {} {}</strong>',
            brand_name, model_name, obj.year or ''
        )
    title_link.short_description = 'Vehicle'

    def vehicle_kind(self, obj):
        """Rodo ar tai Car ar Motorcycle."""
        if obj.motorcycle_brand_id:
            return format_html(
                '<span style="background:#fef3c7;color:#92400e;padding:2px 6px;'
                'border-radius:4px;font-size:11px;font-weight:600;">🏍️ MOTO</span>'
            )
        return format_html(
            '<span style="background:#dbeafe;color:#1e40af;padding:2px 6px;'
            'border-radius:4px;font-size:11px;font-weight:600;">🚗 CAR</span>'
        )
    vehicle_kind.short_description = 'Type'

    def price_display(self, obj):
        symbol = obj.currency_symbol if hasattr(obj, 'currency_symbol') else '$'
        return format_html(
            '<strong style="font-size: 13px;">{}{}</strong>',
            symbol, int(obj.price) if obj.price else 0
        )
    price_display.short_description = 'Price'
    price_display.admin_order_field = 'price'

    def status_colored(self, obj):
        colors = {
            'active':   ('#065f46', '#d1fae5'),
            'draft':    ('#92400e', '#fef3c7'),
            'reserved': ('#9a3412', '#ffedd5'),
            'expired':  ('#991b1b', '#fee2e2'),
            'sold':     ('#1e40af', '#dbeafe'),
            'archived': ('#374151', '#e5e7eb'),
        }
        text_color, bg_color = colors.get(obj.status, ('#374151', '#e5e7eb'))
        return format_html(
            '<span style="background: {}; color: {}; padding: 2px 8px; '
            'border-radius: 4px; font-size: 11px; font-weight: 600; text-transform: uppercase;">{}</span>',
            bg_color, text_color, obj.status
        )
    status_colored.short_description = 'Status'
    status_colored.admin_order_field = 'status'

    def shadow_ban_indicator(self, obj):
        """Rodo 🚫 jei skelbimas shadow banned, kitaip tuščia."""
        if obj.is_shadow_banned:
            return format_html(
                '<span style="color: #991b1b; font-weight: 600; font-size: 13px;" title="Hidden from public">🚫 BANNED</span>'
            )
        return ''
    shadow_ban_indicator.short_description = 'Shadow'
    shadow_ban_indicator.admin_order_field = 'is_shadow_banned'

    def seller_email(self, obj):
        if obj.seller:
            return obj.seller.email
        return '—'
    seller_email.short_description = 'Seller'
    seller_email.admin_order_field = 'seller__email'

    def saved_count_display(self, obj):
        count = obj.saved_by.count() if hasattr(obj, 'saved_by') else 0
        if count == 0:
            return '—'
        return format_html('❤ {}', count)
    saved_count_display.short_description = 'Saves'

    def expires_at_display(self, obj):
        if not obj.expires_at:
            return '—'
        days_left = obj.days_until_expiry
        if days_left is None:
            return obj.expires_at.strftime('%Y-%m-%d')
        if days_left < 0:
            return format_html(
                '<span style="color: #991b1b;">Expired {} d ago</span>',
                abs(days_left)
            )
        if days_left <= 3:
            return format_html(
                '<span style="color: #991b1b; font-weight: 600;">{} d left</span>',
                days_left
            )
        return format_html(
            '<span style="color: #6b7280;">{} d</span>',
            days_left
        )
    expires_at_display.short_description = 'Expires'
    expires_at_display.admin_order_field = 'expires_at'

    def star_display(self, obj):
        effective = obj.get_effective_star_level() if hasattr(obj, 'get_effective_star_level') else 0
        if effective == 2:
            return '⭐⭐'
        if effective == 1:
            return '⭐'
        if obj.star_level > 0:
            return format_html('<span style="color: #9ca3af;">{}⭐ expired</span>', obj.star_level)
        return '—'
    star_display.short_description = '⭐'

    # ─── SHADOW BAN ACTIONS ─────────────────────────────────

    @admin.action(description='🚫 Shadow ban (hide from public, seller sees as active)')
    def shadow_ban_listings(self, request, queryset):
        count = queryset.update(is_shadow_banned=True)
        self.message_user(
            request,
            f'{count} listing(s) shadow banned. Seller still sees them as ACTIVE, '
            f'but public (and search) cannot see them.'
        )

    @admin.action(description='✅ Remove shadow ban (restore public visibility)')
    def remove_shadow_ban(self, request, queryset):
        count = queryset.update(is_shadow_banned=False)
        self.message_user(
            request,
            f'{count} listing(s) restored to public visibility.'
        )

    # ─── LIFECYCLE ACTIONS ───────────────────────────────────

    @admin.action(description='✅ Mark as ACTIVE (activate with 30 days)')
    def mark_as_active(self, request, queryset):
        count = 0
        for listing in queryset:
            listing.activate(days=Listing.DEFAULT_ACTIVE_DAYS)
            count += 1
        self.message_user(request, f'{count} listing(s) activated for 30 days.')

    @admin.action(description='❌ Mark as EXPIRED')
    def mark_as_expired(self, request, queryset):
        count = queryset.update(
            status='expired',
            expires_at=timezone.now(),
        )
        self.message_user(request, f'{count} listing(s) marked as expired.')

    @admin.action(description='🟠 Mark as RESERVED')
    def mark_as_reserved(self, request, queryset):
        count = 0
        for listing in queryset:
            if listing.status == 'active':
                listing.reserve()
                count += 1
        self.message_user(request, f'{count} active listing(s) marked as reserved.')

    @admin.action(description='📦 Mark as ARCHIVED (hide from public)')
    def mark_as_archived(self, request, queryset):
        count = queryset.update(status='archived')
        self.message_user(request, f'{count} listing(s) archived.')

    @admin.action(description='⏱ Extend by 30 days')
    def extend_by_30_days(self, request, queryset):
        count = 0
        for listing in queryset:
            listing.activate(days=30)
            count += 1
        self.message_user(request, f'{count} listing(s) extended by 30 days.')

    # ─── STAR / BOOST ACTIONS ────────────────────────────────

    @admin.action(description='⭐ Activate 1 Star (7 days)')
    def activate_one_star(self, request, queryset):
        count = 0
        for listing in queryset:
            listing.activate_stars(1)
            count += 1
        self.message_user(request, f'{count} listing(s) activated with 1 ⭐ for 7 days.')

    @admin.action(description='⭐⭐ Activate 2 Stars (30 days)')
    def activate_two_stars(self, request, queryset):
        count = 0
        for listing in queryset:
            listing.activate_stars(2)
            count += 1
        self.message_user(request, f'{count} listing(s) activated with 2 ⭐⭐ for 30 days.')

    @admin.action(description='❌ Deactivate Stars')
    def deactivate_stars(self, request, queryset):
        count = 0
        for listing in queryset:
            listing.deactivate_stars()
            count += 1
        self.message_user(request, f'{count} listing(s) stars deactivated.')

    @admin.action(description='🚀 Apply Boost (move to top)')
    def apply_boost_action(self, request, queryset):
        count = queryset.update(last_boosted_at=timezone.now())
        self.message_user(request, f'{count} listing(s) boosted (moved to top).')


# ═══════════════════════════════════════════════════════════
# LISTING IMAGES admin (standalone browse)
# ═══════════════════════════════════════════════════════════

@admin.register(ListingImage)
class ListingImageAdmin(admin.ModelAdmin):
    list_display = ['preview', 'listing', 'order', 'is_main', 'uploaded_at']
    list_filter = ['is_main', 'uploaded_at']
    search_fields = ['listing__title', 'listing__id', 'caption']
    readonly_fields = ['preview']
    autocomplete_fields = ['listing']

    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height: 50px; border-radius: 4px;" />',
                obj.image.url
            )
        return '—'
    preview.short_description = 'Preview'


# ═══════════════════════════════════════════════════════════
# EMAIL SCENARIO admin — email valdymas per Django admin
# ═══════════════════════════════════════════════════════════

@admin.register(EmailScenario)
class EmailScenarioAdmin(admin.ModelAdmin):
    list_display = (
        'status_icon',
        'name',
        'category',
        'code',
        'trigger',
        'send_count',
        'fail_count',
        'last_sent_at',
        'is_enabled',
    )
    list_editable = ('is_enabled',)
    list_filter = ('category', 'is_enabled')
    search_fields = ('code', 'name', 'description')
    list_per_page = 100
    ordering = ('category', 'name')

    readonly_fields = (
        'code',
        'send_count',
        'fail_count',
        'last_sent_at',
        'last_failed_at',
        'last_error',
        'created_at',
        'updated_at',
    )

    fieldsets = (
        ('Basic info', {
            'fields': ('code', 'name', 'category', 'description', 'trigger'),
        }),
        ('Control', {
            'fields': ('is_enabled',),
            'description': (
                'Jeigu uncheck - email nesisiunčia (runtime, be restart). '
                'ATMINK: jei email_settings.py faile False, čia jau nieko nepadarysi - '
                'tai "hard kill switch" kodo lygyje.'
            ),
        }),
        ('Statistics (readonly)', {
            'fields': (
                'send_count', 'fail_count',
                'last_sent_at', 'last_failed_at',
                'last_error',
            ),
            'classes': ('collapse',),
        }),
        ('Meta (readonly)', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    actions = ['enable_selected', 'disable_selected', 'reset_stats']

    def status_icon(self, obj):
        if obj.is_enabled:
            return format_html('<span style="color:#10b981;font-size:16px;">●</span>')
        return format_html('<span style="color:#ef4444;font-size:16px;">●</span>')
    status_icon.short_description = ''

    def enable_selected(self, request, queryset):
        count = queryset.update(is_enabled=True)
        self.message_user(request, f'{count} scenarios enabled.')
    enable_selected.short_description = 'Enable selected scenarios'

    def disable_selected(self, request, queryset):
        count = queryset.update(is_enabled=False)
        self.message_user(request, f'{count} scenarios disabled.')
    disable_selected.short_description = 'Disable selected scenarios'

    def reset_stats(self, request, queryset):
        count = queryset.update(
            send_count=0,
            fail_count=0,
            last_sent_at=None,
            last_failed_at=None,
            last_error='',
        )
        self.message_user(request, f'{count} scenarios reset.')
    reset_stats.short_description = 'Reset statistics counters'


# ═══════════════════════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════════════════
#
#   TRUCK SYSTEM — atskira admin sekcija (10 modelių)
#
# ═══════════════════════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════
# TRUCK BRAND
# ═══════════════════════════════════════════════════════════

@admin.register(TruckBrand)
class TruckBrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'models_count', 'trucks_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'slug']
    ordering = ['name']
    list_per_page = 50

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            _models_count=Count('models', distinct=True),
            _trucks_count=Count('trucks', distinct=True),
        )

    def models_count(self, obj):
        if obj._models_count == 0:
            return '—'
        return format_html('<strong>{}</strong>', obj._models_count)
    models_count.short_description = 'Models'
    models_count.admin_order_field = '_models_count'

    def trucks_count(self, obj):
        if obj._trucks_count == 0:
            return '—'
        return format_html('<strong>{}</strong>', obj._trucks_count)
    trucks_count.short_description = 'Trucks'
    trucks_count.admin_order_field = '_trucks_count'


# ═══════════════════════════════════════════════════════════
# TRUCK MODEL
# ═══════════════════════════════════════════════════════════

@admin.register(TruckModel)
class TruckModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'slug', 'trucks_count']
    list_filter = ['brand']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'brand__name']
    autocomplete_fields = ['brand']
    ordering = ['brand__name', 'name']
    list_per_page = 50

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('brand').annotate(
            _trucks_count=Count('trucks', distinct=True),
        )

    def trucks_count(self, obj):
        if obj._trucks_count == 0:
            return '—'
        return format_html('<strong>{}</strong>', obj._trucks_count)
    trucks_count.short_description = 'Trucks'
    trucks_count.admin_order_field = '_trucks_count'


# ═══════════════════════════════════════════════════════════
# TRUCK IMAGE — inline
# ═══════════════════════════════════════════════════════════

class TruckImageInline(admin.TabularInline):
    model = TruckImage
    extra = 0
    fields = ['image_preview', 'image', 'caption', 'is_main', 'order']
    readonly_fields = ['image_preview']
    ordering = ['order', '-is_main']

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height: 60px; border-radius: 4px;" />',
                obj.image.url
            )
        return '—'
    image_preview.short_description = 'Preview'


# ═══════════════════════════════════════════════════════════
# TRUCK EQUIPMENT — inline
# ═══════════════════════════════════════════════════════════

class TruckEquipmentInline(admin.TabularInline):
    model = TruckEquipment
    extra = 0
    autocomplete_fields = ['equipment']


# ═══════════════════════════════════════════════════════════
# TRUCK — pagrindinis admin
# ═══════════════════════════════════════════════════════════

@admin.register(Truck)
class TruckAdmin(admin.ModelAdmin):
    # ─── LIST VIEW ───────────────────────────────────────────
    list_display = [
        'id_display',
        'thumbnail',
        'title_link',
        'subcategory_badge',
        'truck_type_display',
        'price_display',
        'status_colored',
        'shadow_ban_indicator',
        'seller_email',
        'views_count',
        'saved_count_display',
        'expires_at_display',
        'star_display',
        'created_at',
    ]
    list_display_links = ['title_link']
    list_filter = [
        'status',
        'subcategory',
        'truck_type',
        'cab_type',
        'axle_config',
        'suspension',
        'fuel_type',
        'transmission',
        'euro_standard',
        'condition',
        'is_business_seller',
        'is_shadow_banned',
        'star_level',
        'currency',
        'country',
        'created_at',
    ]
    search_fields = [
        'id',
        'title',
        'description',
        'vin',
        'registration_number',
        'seller__email',
        'seller__username',
        'brand__name',
        'model__name',
        'city',
    ]
    list_per_page = 50
    list_select_related = ['brand', 'model', 'seller']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

    readonly_fields = [
        'id',
        'created_at',
        'updated_at',
        'views_count',
        'impressions_count',
        'activated_at',
        'last_reminder_sent_at',
        'last_no_sale_reminder_at',
        'last_expired_reminder_at',
        'sold_at',
    ]

    autocomplete_fields = ['brand', 'model', 'seller']
    inlines = [TruckImageInline, TruckEquipmentInline]

    actions = [
        'shadow_ban_trucks',
        'remove_shadow_ban',
        'mark_as_active',
        'mark_as_expired',
        'mark_as_reserved',
        'mark_as_sold_action',
        'mark_as_archived',
        'extend_by_30_days',
        'activate_one_star',
        'activate_two_stars',
        'deactivate_stars',
        'apply_boost_action',
    ]

    fieldsets = (
        ('🔑 Identification', {
            'fields': ('id', 'seller', 'title', 'status', 'subcategory'),
        }),
        ('🚫 Admin Moderation', {
            'fields': ('is_shadow_banned',),
            'description': (
                'Shadow ban: slepia skelbimą nuo public, bet savininkas mato jį kaip ACTIVE. '
                'Naudojama spam, fake photos, fraud atvejais.'
            ),
        }),
        ('🚛 Truck Brand / Model', {
            'fields': ('brand', 'model'),
        }),
        ('📋 Identification & Year', {
            'fields': (
                'year', 'first_registration', 'mileage',
                'vin', 'registration_number', 'origin_country',
            ),
        }),
        ('🚚 Truck Specifics', {
            'fields': (
                'truck_type', 'cab_type', 'axle_config', 'suspension',
                'gross_weight', 'curb_weight', 'payload',
                'cargo_volume', 'cargo_length', 'cargo_width', 'cargo_height',
                'number_of_seats',
            ),
        }),
        ('🔧 Engine / Drivetrain', {
            'fields': (
                'fuel_type', 'transmission',
                'engine_capacity', 'power', 'power_hp', 'torque',
                'euro_standard',
                'fuel_consumption', 'fuel_tank_capacity',
            ),
            'classes': ('collapse',),
        }),
        ('🎨 Appearance & Condition', {
            'fields': (
                'color', 'color_other_text',
                'condition', 'defects', 'steering',
                'technical_inspection_month', 'technical_inspection_year',
            ),
            'classes': ('collapse',),
        }),
        ('💵 Price', {
            'fields': (
                'price', 'currency',
                'negotiable', 'open_to_trade',
                'price_excludes_vat',
            ),
        }),
        ('📍 Location', {
            'fields': (
                'country', 'state', 'city',
                'address', 'postal_code',
                'hide_exact_address',
                'latitude', 'longitude',
            ),
            'classes': ('collapse',),
        }),
        ('📝 Content & Extras', {
            'fields': (
                'description', 'features', 'video_url',
                'is_business_seller',
            ),
            'classes': ('collapse',),
        }),
        ('⏱ Lifecycle', {
            'fields': (
                'activated_at', 'expires_at',
                'last_reminder_sent_at',
                'last_no_sale_reminder_at',
                'last_expired_reminder_at',
                'reservation_note',
                'sold_at',
            ),
            'description': (
                'activated_at: when the truck went live. '
                'expires_at: when it will be auto-expired. '
                'Use actions below to extend or change status.'
            ),
            'classes': ('collapse',),
        }),
        ('⭐ Premium Features', {
            'fields': ('star_level', 'star_expires_at', 'last_boosted_at'),
            'description': (
                'Star levels: 0 = none, 1 = ⭐ (7 days), 2 = ⭐⭐ (30 days). '
                'Use Actions menu below to activate automatically.'
            ),
            'classes': ('collapse',),
        }),
        ('📊 Meta & Stats', {
            'fields': (
                'created_at', 'updated_at',
                'views_count', 'impressions_count',
            ),
            'classes': ('collapse',),
        }),
    )

    # ─── LIST DISPLAY HELPERS ────────────────────────────────

    def id_display(self, obj):
        return format_html('<strong>#{}</strong>', obj.id)
    id_display.short_description = 'ID'
    id_display.admin_order_field = 'id'

    def thumbnail(self, obj):
        first_image = obj.images.first()
        if first_image:
            return format_html(
                '<img src="{}" style="width: 60px; height: 45px; object-fit: cover; border-radius: 4px;" />',
                first_image.image.url
            )
        return format_html(
            '<div style="width: 60px; height: 45px; background: #f3f4f6; border-radius: 4px; '
            'display: flex; align-items: center; justify-content: center; color: #9ca3af;">🚛</div>'
        )
    thumbnail.short_description = ''

    def title_link(self, obj):
        brand_name = obj.brand.name if obj.brand_id else ''
        model_name = obj.model.name if obj.model_id else ''
        return format_html(
            '<strong>{} {} {}</strong>',
            brand_name, model_name, obj.year or ''
        )
    title_link.short_description = 'Truck'

    def subcategory_badge(self, obj):
        colors = {
            'trucks':                ('#92400e', '#fef3c7'),
            'vehicle-transporters':  ('#5b21b6', '#ede9fe'),
            'semi-trucks-tractors':  ('#9a3412', '#ffedd5'),
            'vans':                  ('#1e40af', '#dbeafe'),
        }
        text_color, bg_color = colors.get(obj.subcategory, ('#374151', '#e5e7eb'))
        label = dict(Truck.SUBCATEGORY_CHOICES).get(obj.subcategory, obj.subcategory)
        return format_html(
            '<span style="background: {}; color: {}; padding: 2px 6px; '
            'border-radius: 4px; font-size: 10px; font-weight: 600;">{}</span>',
            bg_color, text_color, label
        )
    subcategory_badge.short_description = 'Subcategory'
    subcategory_badge.admin_order_field = 'subcategory'

    def truck_type_display(self, obj):
        if not obj.truck_type:
            return '—'
        return obj.get_truck_type_display()
    truck_type_display.short_description = 'Tipas'
    truck_type_display.admin_order_field = 'truck_type'

    def price_display(self, obj):
        symbol = obj.currency_symbol
        return format_html(
            '<strong style="font-size: 13px;">{}{}</strong>',
            symbol, int(obj.price) if obj.price else 0
        )
    price_display.short_description = 'Price'
    price_display.admin_order_field = 'price'

    def status_colored(self, obj):
        colors = {
            'active':   ('#065f46', '#d1fae5'),
            'draft':    ('#92400e', '#fef3c7'),
            'reserved': ('#9a3412', '#ffedd5'),
            'expired':  ('#991b1b', '#fee2e2'),
            'sold':     ('#1e40af', '#dbeafe'),
            'archived': ('#374151', '#e5e7eb'),
        }
        text_color, bg_color = colors.get(obj.status, ('#374151', '#e5e7eb'))
        return format_html(
            '<span style="background: {}; color: {}; padding: 2px 8px; '
            'border-radius: 4px; font-size: 11px; font-weight: 600; text-transform: uppercase;">{}</span>',
            bg_color, text_color, obj.status
        )
    status_colored.short_description = 'Status'
    status_colored.admin_order_field = 'status'

    def shadow_ban_indicator(self, obj):
        if obj.is_shadow_banned:
            return format_html(
                '<span style="color: #991b1b; font-weight: 600; font-size: 13px;" '
                'title="Hidden from public">🚫 BANNED</span>'
            )
        return ''
    shadow_ban_indicator.short_description = 'Shadow'
    shadow_ban_indicator.admin_order_field = 'is_shadow_banned'

    def seller_email(self, obj):
        return obj.seller.email if obj.seller else '—'
    seller_email.short_description = 'Seller'
    seller_email.admin_order_field = 'seller__email'

    def saved_count_display(self, obj):
        count = obj.saved_by.count() if hasattr(obj, 'saved_by') else 0
        if count == 0:
            return '—'
        return format_html('❤ {}', count)
    saved_count_display.short_description = 'Saves'

    def expires_at_display(self, obj):
        if not obj.expires_at:
            return '—'
        days_left = obj.days_until_expiry
        if days_left is None:
            return obj.expires_at.strftime('%Y-%m-%d')
        if days_left < 0:
            return format_html(
                '<span style="color: #991b1b;">Expired {} d ago</span>',
                abs(days_left)
            )
        if days_left <= 3:
            return format_html(
                '<span style="color: #991b1b; font-weight: 600;">{} d left</span>',
                days_left
            )
        return format_html(
            '<span style="color: #6b7280;">{} d</span>',
            days_left
        )
    expires_at_display.short_description = 'Expires'
    expires_at_display.admin_order_field = 'expires_at'

    def star_display(self, obj):
        effective = obj.get_effective_star_level()
        if effective == 2:
            return '⭐⭐'
        if effective == 1:
            return '⭐'
        if obj.star_level > 0:
            return format_html('<span style="color: #9ca3af;">{}⭐ expired</span>', obj.star_level)
        return '—'
    star_display.short_description = '⭐'

    # ─── SHADOW BAN ACTIONS ──────────────────────────────────

    @admin.action(description='🚫 Shadow ban (hide from public, seller sees as active)')
    def shadow_ban_trucks(self, request, queryset):
        count = queryset.update(is_shadow_banned=True)
        self.message_user(
            request,
            f'{count} truck(s) shadow banned. Seller still sees them as ACTIVE, '
            f'but public (and search) cannot see them.'
        )

    @admin.action(description='✅ Remove shadow ban (restore public visibility)')
    def remove_shadow_ban(self, request, queryset):
        count = queryset.update(is_shadow_banned=False)
        self.message_user(request, f'{count} truck(s) restored to public visibility.')

    # ─── LIFECYCLE ACTIONS ───────────────────────────────────

    @admin.action(description='✅ Mark as ACTIVE (activate with 30 days)')
    def mark_as_active(self, request, queryset):
        count = 0
        for truck in queryset:
            truck.activate(days=Truck.DEFAULT_ACTIVE_DAYS)
            count += 1
        self.message_user(request, f'{count} truck(s) activated for 30 days.')

    @admin.action(description='❌ Mark as EXPIRED')
    def mark_as_expired(self, request, queryset):
        count = queryset.update(
            status='expired',
            expires_at=timezone.now(),
        )
        self.message_user(request, f'{count} truck(s) marked as expired.')

    @admin.action(description='🟠 Mark as RESERVED')
    def mark_as_reserved(self, request, queryset):
        count = 0
        for truck in queryset:
            if truck.status == 'active':
                truck.reserve()
                count += 1
        self.message_user(request, f'{count} active truck(s) marked as reserved.')

    @admin.action(description='💰 Mark as SOLD')
    def mark_as_sold_action(self, request, queryset):
        count = 0
        for truck in queryset:
            truck.mark_as_sold()
            try:
                TruckSalesRecord.create_from_truck(truck, marked_sold=True)
            except Exception:
                pass
            count += 1
        self.message_user(request, f'{count} truck(s) marked as sold (sales record created).')

    @admin.action(description='📦 Mark as ARCHIVED (hide from public)')
    def mark_as_archived(self, request, queryset):
        count = queryset.update(status='archived')
        self.message_user(request, f'{count} truck(s) archived.')

    @admin.action(description='⏱ Extend by 30 days')
    def extend_by_30_days(self, request, queryset):
        count = 0
        for truck in queryset:
            truck.activate(days=30)
            count += 1
        self.message_user(request, f'{count} truck(s) extended by 30 days.')

    # ─── STAR / BOOST ACTIONS ────────────────────────────────

    @admin.action(description='⭐ Activate 1 Star (7 days)')
    def activate_one_star(self, request, queryset):
        count = 0
        for truck in queryset:
            truck.activate_stars(1)
            count += 1
        self.message_user(request, f'{count} truck(s) activated with 1 ⭐ for 7 days.')

    @admin.action(description='⭐⭐ Activate 2 Stars (30 days)')
    def activate_two_stars(self, request, queryset):
        count = 0
        for truck in queryset:
            truck.activate_stars(2)
            count += 1
        self.message_user(request, f'{count} truck(s) activated with 2 ⭐⭐ for 30 days.')

    @admin.action(description='❌ Deactivate Stars')
    def deactivate_stars(self, request, queryset):
        count = 0
        for truck in queryset:
            truck.deactivate_stars()
            count += 1
        self.message_user(request, f'{count} truck(s) stars deactivated.')

    @admin.action(description='🚀 Apply Boost (move to top)')
    def apply_boost_action(self, request, queryset):
        count = queryset.update(last_boosted_at=timezone.now())
        self.message_user(request, f'{count} truck(s) boosted (moved to top).')


# ═══════════════════════════════════════════════════════════
# TRUCK IMAGES admin (standalone browse)
# ═══════════════════════════════════════════════════════════

@admin.register(TruckImage)
class TruckImageAdmin(admin.ModelAdmin):
    list_display = ['preview', 'truck', 'order', 'is_main', 'uploaded_at']
    list_filter = ['is_main', 'uploaded_at']
    search_fields = ['truck__title', 'truck__id', 'caption']
    readonly_fields = ['preview']
    autocomplete_fields = ['truck']

    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height: 50px; border-radius: 4px;" />',
                obj.image.url
            )
        return '—'
    preview.short_description = 'Preview'


# ═══════════════════════════════════════════════════════════
# TRUCK EQUIPMENT admin (standalone browse)
# ═══════════════════════════════════════════════════════════

@admin.register(TruckEquipment)
class TruckEquipmentAdmin(admin.ModelAdmin):
    list_display = ['truck', 'equipment']
    list_filter = ['equipment__category']
    search_fields = ['truck__title', 'equipment__name']
    autocomplete_fields = ['truck', 'equipment']


# ═══════════════════════════════════════════════════════════
# SAVED TRUCK admin
# ═══════════════════════════════════════════════════════════

@admin.register(SavedTruck)
class SavedTruckAdmin(admin.ModelAdmin):
    list_display = ['user_email', 'truck_link', 'saved_at']
    list_filter = ['saved_at']
    search_fields = [
        'user__email', 'user__username',
        'truck__title', 'truck__id',
    ]
    autocomplete_fields = ['user', 'truck']
    date_hierarchy = 'saved_at'
    ordering = ['-saved_at']
    readonly_fields = ['saved_at']

    def user_email(self, obj):
        return obj.user.email if obj.user else '—'
    user_email.short_description = 'User'
    user_email.admin_order_field = 'user__email'

    def truck_link(self, obj):
        if not obj.truck_id:
            return '—'
        url = reverse('admin:%s_truck_change' % obj.truck._meta.app_label, args=[obj.truck.pk])
        return format_html('<a href="{}">{} (#{})</a>', url, obj.truck.title, obj.truck.pk)
    truck_link.short_description = 'Truck'


# ═══════════════════════════════════════════════════════════
# SAVED TRUCK NOTIFICATION admin (anti-spam throttling)
# ═══════════════════════════════════════════════════════════

@admin.register(SavedTruckNotification)
class SavedTruckNotificationAdmin(admin.ModelAdmin):
    list_display = ['user_email', 'truck_title', 'notified_at']
    list_filter = ['notified_at']
    search_fields = [
        'user__email', 'user__username',
        'truck__title', 'truck__id',
    ]
    autocomplete_fields = ['user', 'truck']
    date_hierarchy = 'notified_at'
    ordering = ['-notified_at']
    readonly_fields = ['notified_at']

    def user_email(self, obj):
        return obj.user.email if obj.user else '—'
    user_email.short_description = 'User'
    user_email.admin_order_field = 'user__email'

    def truck_title(self, obj):
        return obj.truck.title if obj.truck_id else '—'
    truck_title.short_description = 'Truck'


# ═══════════════════════════════════════════════════════════
# TRUCK VIEW admin (analytics)
# ═══════════════════════════════════════════════════════════

@admin.register(TruckView)
class TruckViewAdmin(admin.ModelAdmin):
    list_display = ['truck_title', 'user_email', 'ip_address', 'viewed_at']
    list_filter = ['viewed_at']
    search_fields = [
        'truck__title', 'truck__id',
        'user__email', 'ip_address',
    ]
    autocomplete_fields = ['truck', 'user']
    date_hierarchy = 'viewed_at'
    ordering = ['-viewed_at']
    readonly_fields = ['viewed_at']
    list_per_page = 100

    def truck_title(self, obj):
        return obj.truck.title if obj.truck_id else '—'
    truck_title.short_description = 'Truck'

    def user_email(self, obj):
        return obj.user.email if obj.user else '(anon)'
    user_email.short_description = 'User'


# ═══════════════════════════════════════════════════════════
# TRUCK IMPRESSION admin (analytics)
# ═══════════════════════════════════════════════════════════

@admin.register(TruckImpression)
class TruckImpressionAdmin(admin.ModelAdmin):
    list_display = ['truck_title', 'user_email', 'ip_address', 'shown_at']
    list_filter = ['shown_at']
    search_fields = [
        'truck__title', 'truck__id',
        'user__email', 'ip_address',
    ]
    autocomplete_fields = ['truck', 'user']
    date_hierarchy = 'shown_at'
    ordering = ['-shown_at']
    readonly_fields = ['shown_at']
    list_per_page = 100

    def truck_title(self, obj):
        return obj.truck.title if obj.truck_id else '—'
    truck_title.short_description = 'Truck'

    def user_email(self, obj):
        return obj.user.email if obj.user else '(anon)'
    user_email.short_description = 'User'


# ═══════════════════════════════════════════════════════════
# TRUCK SALES RECORD admin (po pardavimo)
# ═══════════════════════════════════════════════════════════

@admin.register(TruckSalesRecord)
class TruckSalesRecordAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'subcategory_badge',
        'brand',
        'model',
        'year',
        'price_display',
        'days_active',
        'views_count',
        'saves_count',
        'marked_sold_display',
        'sold_at',
    ]
    list_filter = [
        'subcategory',
        'currency',
        'marked_sold',
        'sold_at',
        'country',
    ]
    search_fields = [
        'title',
        'seller__email',
        'seller_email',
        'brand__name',
        'model__name',
        'truck_id',
    ]
    autocomplete_fields = ['seller', 'brand', 'model']
    readonly_fields = [
        'truck_id',
        'truck_created_at',
        'sold_at',
        'days_active',
        'views_count',
        'impressions_count',
        'saves_count',
    ]
    date_hierarchy = 'sold_at'
    ordering = ['-sold_at']
    list_per_page = 50

    fieldsets = (
        ('Sale info', {
            'fields': (
                'truck_id', 'title', 'subcategory',
                'sold_at', 'marked_sold',
            ),
        }),
        ('Vehicle', {
            'fields': ('brand', 'model', 'year'),
        }),
        ('Seller', {
            'fields': ('seller', 'seller_email'),
        }),
        ('Price', {
            'fields': ('price', 'currency'),
        }),
        ('Location', {
            'fields': ('city', 'country'),
        }),
        ('Performance', {
            'fields': (
                'truck_created_at', 'days_active',
                'views_count', 'impressions_count', 'saves_count',
            ),
            'classes': ('collapse',),
        }),
    )

    def subcategory_badge(self, obj):
        colors = {
            'trucks':                ('#92400e', '#fef3c7'),
            'vehicle-transporters':  ('#5b21b6', '#ede9fe'),
            'semi-trucks-tractors':  ('#9a3412', '#ffedd5'),
            'vans':                  ('#1e40af', '#dbeafe'),
        }
        text_color, bg_color = colors.get(obj.subcategory, ('#374151', '#e5e7eb'))
        return format_html(
            '<span style="background: {}; color: {}; padding: 2px 6px; '
            'border-radius: 4px; font-size: 10px; font-weight: 600;">{}</span>',
            bg_color, text_color, obj.subcategory or '—'
        )
    subcategory_badge.short_description = 'Subcategory'
    subcategory_badge.admin_order_field = 'subcategory'

    def price_display(self, obj):
        return format_html(
            '<strong style="color:#10b981">{}{}</strong>',
            obj.currency_symbol, int(obj.price) if obj.price else 0
        )
    price_display.short_description = 'Price'
    price_display.admin_order_field = 'price'

    def marked_sold_display(self, obj):
        if obj.marked_sold:
            return format_html('<span style="color:#10b981;">✓ Manual</span>')
        return format_html('<span style="color:#9ca3af;">Auto</span>')
    marked_sold_display.short_description = 'Marked'
    marked_sold_display.admin_order_field = 'marked_sold'


# ═══════════════════════════════════════════════════════════
# PRICING SYSTEM admin (Settings, Multiplier Tiers, Promo Codes)
# ═══════════════════════════════════════════════════════════

from .models import (
    PricingSettings, PriceMultiplierTier, PromoCode, PromoCodeUsage,
)


@admin.register(PricingSettings)
class PricingSettingsAdmin(admin.ModelAdmin):
    """Singleton: pricing globalūs nustatymai (multiplier on/off, addon kainos)."""

    fieldsets = (
        ('Multiplier', {
            'fields': ('multiplier_enabled',),
            'description': (
                '<b>Įjungti dynamic pricing</b> (kuo brangesnis listing → tuo brangesnis plan\'as). '
                'Tier\'ai nustatomi <a href="/admin/listings/pricemultipliertier/">Price Multiplier Tiers</a>.'
            ),
        }),
        ('Addon Prices', {
            'fields': (
                'addon_renew_price',
                'addon_featured_price',
            ),
            'description': 'Kainos už addons (per dieną/per žvaigždutę).',
        }),
        ('Addon Limits', {
            'fields': (
                'addon_renew_max_count',
                'addon_renew_max_days',
                'addon_featured_max_days',
            ),
            'classes': ('collapse',),
        }),
    )

    def has_add_permission(self, request):
        return not PricingSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        from django.shortcuts import redirect
        obj = PricingSettings.get_solo()
        return redirect(f'/admin/listings/pricingsettings/{obj.pk}/change/')


@admin.register(PriceMultiplierTier)
class PriceMultiplierTierAdmin(admin.ModelAdmin):
    """Tier'ai pagal listing.price."""

    list_display = ('label', 'min_price', 'max_price', 'multiplier', 'is_active')
    list_editable = ('multiplier', 'is_active')
    list_filter = ('is_active',)
    ordering = ('min_price',)

    fieldsets = (
        ('Price Range', {
            'fields': ('min_price', 'max_price'),
            'description': 'Listing.price range (inclusive min, exclusive max).',
        }),
        ('Multiplier', {
            'fields': ('multiplier', 'label'),
            'description': '1.0 = bazinė kaina, 1.5 = +50%, 2.0 = ×2.',
        }),
        ('Status', {
            'fields': ('is_active',),
        }),
    )


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    """Akcijų kodai (SPRING25, WELCOME10, etc.)."""

    list_display = (
        'code', 'description_short', 'discount_display',
        'used_count', 'max_uses', 'is_active', 'valid_until',
    )
    list_filter = ('is_active', 'discount_type')
    search_fields = ('code', 'description')
    readonly_fields = ('used_count',)

    fieldsets = (
        ('Code', {
            'fields': ('code', 'description', 'is_active'),
            'description': 'Pvz. SPRING25, WELCOME10, BLACKFRIDAY50',
        }),
        ('Discount', {
            'fields': ('discount_type', 'discount_value'),
            'description': (
                '<b>Percent</b>: discount_value=25 reiškia -25% nuo kainos. '
                '<b>Fixed</b>: discount_value=5 reiškia -$5.'
            ),
        }),
        ('Validity Period', {
            'fields': ('valid_from', 'valid_until'),
        }),
        ('Usage Limits', {
            'fields': ('max_uses', 'used_count', 'once_per_user'),
        }),
        ('Applies To Categories', {
            'fields': ('applies_to_cars', 'applies_to_trucks', 'applies_to_motorcycles'),
            'description': 'Pažymėk kurioms kategorijoms galioja.',
        }),
        ('Applies To Plans', {
            'fields': ('applies_to_basic', 'applies_to_standard', 'applies_to_premium'),
            'classes': ('collapse',),
        }),
        ('Conditions', {
            'fields': ('min_listing_price',),
            'classes': ('collapse',),
            'description': 'Min. listing kaina, kad nuolaida galiotų.',
        }),
    )

    def description_short(self, obj):
        return (obj.description or '')[:50]
    description_short.short_description = 'Description'

    def discount_display(self, obj):
        if obj.discount_type == 'percent':
            return f'-{obj.discount_value}%'
        return f'-${obj.discount_value}'
    discount_display.short_description = 'Discount'


@admin.register(PromoCodeUsage)
class PromoCodeUsageAdmin(admin.ModelAdmin):
    """Akcijų kodų panaudojimo istorija (read-only)."""

    list_display = ('promo_code', 'user', 'listing', 'discount_amount', 'used_at')
    list_filter = ('promo_code', 'used_at')
    readonly_fields = ('promo_code', 'user', 'listing', 'discount_amount', 'used_at')
    date_hierarchy = 'used_at'

    def has_add_permission(self, request):
        return False