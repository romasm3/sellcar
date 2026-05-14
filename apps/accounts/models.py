from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.listings.constants import (
    ACCOUNT_TYPE_CHOICES, ACCOUNT_TYPE_PRIVATE,
    DEALER_STATUS_CHOICES, DEALER_STATUS_NONE,
)


class Profile(models.Model):
    """User Profile Model"""

    SELLER_TYPE_CHOICES = [
        ('private', 'Private Seller'),
        ('dealer', 'Car Dealer / Autohouse'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    # Personal Information
    bio = models.TextField(max_length=500, blank=True, verbose_name="Bio")
    location = models.CharField(max_length=100, blank=True, verbose_name="Location")
    phone_number = models.CharField(max_length=20, blank=True, verbose_name="Phone Number")
    phone_number_secondary = models.CharField(max_length=20, blank=True, verbose_name="Secondary Phone Number")
    street = models.CharField(max_length=200, blank=True, verbose_name="Street")
    house_number = models.CharField(max_length=20, blank=True, verbose_name="House Number")
    city = models.CharField(max_length=100, blank=True, verbose_name="City")
    country = models.CharField(max_length=100, blank=True, default="Lithuania", verbose_name="Country")
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True, verbose_name="Profile Picture")

    # Seller type (LEGACY — used for Listing filters; new logic uses account_type below)
    seller_type = models.CharField(
        max_length=20,
        choices=SELLER_TYPE_CHOICES,
        default='private',
        verbose_name="Seller Type"
    )
    company_name = models.CharField(max_length=200, blank=True, verbose_name="Company Name")
    company_logo = models.ImageField(upload_to='companies/', blank=True, null=True, verbose_name="Company Logo")
    banner_image = models.ImageField(upload_to='banners/', blank=True, null=True, verbose_name="Banner Image")
    working_hours = models.CharField(max_length=200, blank=True, verbose_name="Working Hours")
    contact_person = models.CharField(max_length=100, blank=True, verbose_name="Contact Person")
    company_description = models.TextField(max_length=1000, blank=True, verbose_name="Company Description")
    website = models.URLField(blank=True, verbose_name="Website")

    # Rating (updated via signals)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0, verbose_name="Rating")
    rating_count = models.IntegerField(default=0, verbose_name="Rating Count")

    # Wallet
    wallet_balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        verbose_name="Wallet Balance (points)"
    )

    # Notification Settings
    email_notifications = models.BooleanField(default=True, verbose_name="Email Notifications")
    email_messages = models.BooleanField(default=True, verbose_name="Email Messages Notifications")
    marketing_emails = models.BooleanField(default=False, verbose_name="Marketing Emails")
    sms_notifications = models.BooleanField(default=False, verbose_name="SMS Notifications")

    # Privacy Settings
    show_email = models.BooleanField(default=False, verbose_name="Show Email on Profile")
    show_phone = models.BooleanField(default=True, verbose_name="Show Phone on Listings")
    public_profile = models.BooleanField(default=True, verbose_name="Public Profile")
    show_location_map = models.BooleanField(
        default=True,
        verbose_name="Show Location on Map",
        help_text="Display your listing locations on Google Maps"
    )

    # ═══════════════════════════════════════════════════════════
    # ACCOUNT TYPE & DEALER FIELDS (added 2026-05-07)
    # ═══════════════════════════════════════════════════════════
    account_type = models.CharField(
        max_length=10,
        choices=ACCOUNT_TYPE_CHOICES,
        default=ACCOUNT_TYPE_PRIVATE,
        verbose_name='Account type',
    )
    dealer_status = models.CharField(
        max_length=10,
        choices=DEALER_STATUS_CHOICES,
        default=DEALER_STATUS_NONE,
        verbose_name='Dealer status',
    )

    # ─── Dealer business info (filled via apply form) ───
    dealer_company_name = models.CharField(max_length=200, blank=True)
    dealer_logo = models.ImageField(
        upload_to='dealer_logos/', blank=True, null=True,
    )
    dealer_address = models.CharField(max_length=300, blank=True)
    dealer_phone = models.CharField(max_length=30, blank=True)
    dealer_description = models.TextField(blank=True)

    # ─── Dealer subscription (€99/mėn — Stripe later) ───
    dealer_subscription_active = models.BooleanField(default=False)
    dealer_subscription_expires = models.DateTimeField(null=True, blank=True)
    dealer_applied_at = models.DateTimeField(null=True, blank=True)
    dealer_approved_at = models.DateTimeField(null=True, blank=True)

    # ─── Private subscription (/mėn → 5 skelbimai) ───
    private_subscription_active = models.BooleanField(default=False)
    private_subscription_expires = models.DateTimeField(null=True, blank=True)

    # ─── Dealer working hours (JSON struktūra) ───
    dealer_working_hours = models.JSONField(
        default=dict, blank=True,
        verbose_name='Dealer working hours',
        help_text='JSON: {"mon": {"open": "09:00", "close": "18:00", "closed": false}, ...}'
    )

    # ═══════════════════════════════════════════════════════════
    # LANGUAGE PREFERENCE (added 2026-05-09)
    # Auto-load user's preferred language across devices/sessions
    # ═══════════════════════════════════════════════════════════
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('lt', 'Lietuvių'),
        ('lv', 'Latviešu'),
        ('et', 'Eesti'),
        ('pl', 'Polski'),
        ('de', 'Deutsch'),
        ('ru', 'Русский'),
        ('fr', 'Français'),
    ]
    language = models.CharField(
        max_length=10,
        choices=LANGUAGE_CHOICES,
        default='en',
        blank=True,
        verbose_name='Preferred Language',
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def display_name(self):
        if self.seller_type == 'dealer' and self.company_name:
            return self.company_name
        if self.account_type == 'dealer' and self.dealer_company_name:
            return self.dealer_company_name
        return self.user.get_full_name() or self.user.username

    @property
    def is_dealer(self):
        return self.seller_type == 'dealer' or self.account_type == 'dealer'

    @property
    def is_approved_dealer(self):
        """True if user has approved dealer status with active subscription."""
        return (
            self.account_type == 'dealer'
            and self.dealer_status == 'approved'
            and self.dealer_subscription_active
        )

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        ordering = ['-created_at']


class WalletTransaction(models.Model):
    """Wallet transaction history (top-ups, spends, bonuses)."""

    TYPE_CHOICES = [
        ('topup', 'Top-up'),
        ('bonus', 'Bonus'),
        ('spend', 'Spend'),
        ('refund', 'Refund'),
        ('test_topup', 'Test top-up'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='wallet_transactions'
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2,
        verbose_name="Amount (points)",
        help_text="Positive for top-ups, negative for spends"
    )
    bonus_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        verbose_name="Bonus points"
    )
    transaction_type = models.CharField(
        max_length=20, choices=TYPE_CHOICES, default='topup'
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending'
    )
    description = models.CharField(max_length=200, blank=True)

    # Stripe integration (empty until Stripe enabled)
    stripe_session_id = models.CharField(max_length=200, blank=True, db_index=True)
    stripe_payment_intent = models.CharField(max_length=200, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Wallet Transaction"
        verbose_name_plural = "Wallet Transactions"

    def __str__(self):
        sign = '+' if self.amount >= 0 else ''
        return f"{self.user.username}: {sign}{self.amount} pts ({self.get_transaction_type_display()})"

    @property
    def total_amount(self):
        """Total points added (amount + bonus)."""
        return self.amount + self.bonus_amount


class SellerReview(models.Model):
    """Seller Review / Rating"""
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name="Rating")
    comment = models.TextField(max_length=500, blank=True, verbose_name="Comment")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['reviewer', 'seller']
        verbose_name = "Seller Review"
        verbose_name_plural = "Seller Reviews"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.reviewer.username} → {self.seller.username}: {self.rating}★"


def update_seller_rating(seller):
    """Recalculate and save seller rating"""
    reviews = SellerReview.objects.filter(seller=seller)
    count = reviews.count()
    if count > 0:
        avg = sum(r.rating for r in reviews) / count
        seller.profile.rating = round(avg, 1)
        seller.profile.rating_count = count
        seller.profile.save(update_fields=['rating', 'rating_count'])


# Signals
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create profile when user is created"""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save profile when user is saved"""
    if hasattr(instance, 'profile'):
        instance.profile.save()