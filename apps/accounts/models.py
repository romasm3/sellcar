from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


# Custom User model
class User(AbstractUser):
    """Custom User model"""

    bio = models.TextField(blank=True, verbose_name="Bio")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Phone")
    city = models.CharField(max_length=100, blank=True, verbose_name="City")
    profile_image = models.ImageField(
        upload_to="profiles/", blank=True, null=True, verbose_name="Profile Image"
    )

    class Meta:
        db_table = "accounts_user"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username


# User Profile
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    address = models.CharField(max_length=255, blank=True, verbose_name="Address")
    country = models.CharField(
        max_length=100, default="Lithuania", verbose_name="Country"
    )
    avatar = models.ImageField(
        upload_to="avatars/", blank=True, null=True, verbose_name="Avatar"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated")

    def __str__(self):
        return f"{self.user.username} Profile"

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"


# Signals - automatically create user profile when user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
