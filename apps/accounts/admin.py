from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "country", "created_at"]
    list_filter = ["country", "created_at"]
    search_fields = ["user__username", "user__email"]
