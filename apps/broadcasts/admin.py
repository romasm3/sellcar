import time

from django.conf import settings
from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone

from .models import Broadcast

User = get_user_model()


@admin.register(Broadcast)
class BroadcastAdmin(admin.ModelAdmin):
    list_display = (
        "subject",
        "status",
        "recipients_count",
        "success_count",
        "failed_count",
        "created_at",
        "sent_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("subject", "message")
    readonly_fields = (
        "status",
        "recipients_count",
        "success_count",
        "failed_count",
        "created_at",
        "sent_at",
        "created_by",
    )

    fieldsets = (
        ("Žinutė", {"fields": ("subject", "message")}),
        (
            "Statusas (read-only)",
            {
                "fields": (
                    "status",
                    "recipients_count",
                    "success_count",
                    "failed_count",
                    "created_at",
                    "sent_at",
                    "created_by",
                ),
            },
        ),
    )

    actions = ["send_test_to_me", "send_to_all_users"]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    # ───────────────────────────────────────────────────────
    # Test send – tau pačiam
    # ───────────────────────────────────────────────────────
    def send_test_to_me(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(
                request,
                "Pasirink TIK VIENĄ broadcast testavimui.",
                level=messages.ERROR,
            )
            return

        broadcast = queryset.first()

        if not request.user.email:
            self.message_user(
                request,
                "Tavo admin user'is neturi email adreso.",
                level=messages.ERROR,
            )
            return

        try:
            send_mail(
                subject=f"[TEST] {broadcast.subject}",
                message=broadcast.message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[request.user.email],
                fail_silently=False,
            )
            self.message_user(
                request,
                f"✅ Test išsiųstas į {request.user.email}",
                level=messages.SUCCESS,
            )
        except Exception as e:
            self.message_user(
                request, f"❌ Klaida siunčiant: {e}", level=messages.ERROR
            )

    send_test_to_me.short_description = "📧 Siųsti TEST sau"

    # ───────────────────────────────────────────────────────
    # Tikras siuntimas visiems
    # ───────────────────────────────────────────────────────
    def send_to_all_users(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(
                request,
                "Pasirink TIK VIENĄ broadcast siuntimui.",
                level=messages.ERROR,
            )
            return

        broadcast = queryset.first()

        if broadcast.status == Broadcast.STATUS_SENT:
            self.message_user(
                request,
                "⚠ Šis broadcast jau buvo išsiųstas. Sukurk naują, jei nori siųsti dar kartą.",
                level=messages.WARNING,
            )
            return

        # Surenkam unikalius email'us iš aktyvių userių
        recipients = (
            User.objects.filter(is_active=True)
            .exclude(email="")
            .exclude(email__isnull=True)
            .values_list("email", flat=True)
            .distinct()
        )
        recipients_list = list(recipients)

        if not recipients_list:
            self.message_user(
                request,
                "Nėra nei vieno aktyvaus user'io su email.",
                level=messages.ERROR,
            )
            return

        broadcast.status = Broadcast.STATUS_SENDING
        broadcast.recipients_count = len(recipients_list)
        broadcast.save(update_fields=["status", "recipients_count"])

        success = 0
        failed = 0
        batch_size = 50

        for i, email in enumerate(recipients_list):
            try:
                send_mail(
                    subject=broadcast.subject,
                    message=broadcast.message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False,
                )
                success += 1
            except Exception:
                failed += 1

            # Throttling – kas 50 laiškų pauzė 2s (Gmail SMTP rate limit apsauga)
            if (i + 1) % batch_size == 0:
                time.sleep(2)

        broadcast.success_count = success
        broadcast.failed_count = failed
        broadcast.status = (
            Broadcast.STATUS_SENT if failed == 0 else Broadcast.STATUS_FAILED
        )
        broadcast.sent_at = timezone.now()
        broadcast.save(
            update_fields=["success_count", "failed_count", "status", "sent_at"]
        )

        if failed == 0:
            self.message_user(
                request,
                f"✅ Sėkmingai išsiųsta {success} email'ų (iš {len(recipients_list)})",
                level=messages.SUCCESS,
            )
        else:
            self.message_user(
                request,
                f"⚠ Išsiųsta {success} sėkmingai, {failed} nepavyko (iš {len(recipients_list)})",
                level=messages.WARNING,
            )

    send_to_all_users.short_description = "🚀 SIŲSTI VISIEMS aktyviems user'iams"