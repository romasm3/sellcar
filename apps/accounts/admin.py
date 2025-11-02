from django.contrib import admin
from .models import Profile


@admin.register(Profile)  # <-- PAKEISTA iš UserProfile į Profile
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "phone_number",
        "location",
        "email_notifications",
        "public_profile",
        "created_at"
    ]

    list_filter = [
        "email_notifications",
        "public_profile",
        "show_email",
        "show_phone",
        "created_at"
    ]

    search_fields = [
        "user__username",
        "user__email",
        "phone_number",
        "location"
    ]

    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        ("User", {
            "fields": ("user",)
        }),
        ("Contact Information", {
            "fields": ("phone_number", "location")
        }),
        ("Profile Info", {
            "fields": ("profile_picture", "bio")
        }),
        ("Notification Settings", {
            "fields": ("email_notifications", "marketing_emails", "sms_notifications")
        }),
        ("Privacy Settings", {
            "fields": ("show_email", "show_phone", "public_profile")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at")
        }),
    )
