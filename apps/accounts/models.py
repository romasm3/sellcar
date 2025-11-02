from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """User Profile Model"""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    # Personal Information
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name="Bio"
    )
    location = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Location"
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Phone Number"
    )
    profile_picture = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True,
        verbose_name="Profile Picture"
    )

    # Notification Settings
    email_notifications = models.BooleanField(
        default=True,
        verbose_name="Email Notifications"
    )
    marketing_emails = models.BooleanField(
        default=False,
        verbose_name="Marketing Emails"
    )
    sms_notifications = models.BooleanField(
        default=False,
        verbose_name="SMS Notifications"
    )

    # Privacy Settings
    show_email = models.BooleanField(
        default=False,
        verbose_name="Show Email on Profile"
    )
    show_phone = models.BooleanField(
        default=True,
        verbose_name="Show Phone on Listings"
    )
    public_profile = models.BooleanField(
        default=True,
        verbose_name="Public Profile"
    )
    show_location_map = models.BooleanField(
            default=True,
            verbose_name="Show Location on Map",
            help_text="Display your listing locations on Google Maps"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        ordering = ['-created_at']


# Signals to automatically create/update profile
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
