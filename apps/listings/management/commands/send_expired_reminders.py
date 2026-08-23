"""
Management command: send_expired_reminders

Siunčia 'listing_expired_reminder' email pardavėjams, kurių
skelbimai jau pasibaigė (status='expired') ir nebuvo aktyvuoti.
Siunčia kas 4 dienas iki kol user'is aktyvuos arba ištrins.

Paleidimas:
    python manage.py send_expired_reminders
    python manage.py send_expired_reminders --dry-run
    python manage.py send_expired_reminders --interval 1   # testavimui
    python manage.py send_expired_reminders --force
"""

from datetime import timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils import timezone

from apps.listings.models import Listing, EmailScenario


class Command(BaseCommand):
    help = "Send 'listing_expired_reminder' email every 4 days for expired listings."

    SCENARIO_CODE = 'listing_expired_reminder'
    DEFAULT_INTERVAL_DAYS = 4

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='List listings that would receive emails, but do not send.',
        )
        parser.add_argument(
            '--interval',
            type=int,
            default=self.DEFAULT_INTERVAL_DAYS,
            help=f'Days between reminders. Default: {self.DEFAULT_INTERVAL_DAYS}.',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Ignore last_expired_reminder_at check. Sends to ALL expired listings.',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        interval = options['interval']
        force = options['force']

        # ── 1. Patikrink ar scenarijus įjungtas ──────────────────────
        try:
            scenario = EmailScenario.objects.get(code=self.SCENARIO_CODE)
        except EmailScenario.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                f"EmailScenario '{self.SCENARIO_CODE}' not found in DB. "
                f"Run: python manage.py sync_email_scenarios"
            ))
            return

        if not scenario.is_enabled:
            self.stdout.write(self.style.WARNING(
                f"Scenario '{self.SCENARIO_CODE}' is DISABLED. Nothing to send."
            ))
            return

        # ── 2. Surask expired skelbimus ──────────────────────────────
        now = timezone.now()
        cutoff = now - timedelta(days=interval)

        qs = Listing.objects.filter(status='expired').select_related('seller')

        if not force:
            # Tik tie, kurie (a) dar niekada nebuvo priminti ARBA (b) paskutinis
            # priminimas buvo > `interval` dienų atgal.
            qs = qs.filter(
                Q(last_expired_reminder_at__isnull=True)
                | Q(last_expired_reminder_at__lt=cutoff)
            )

        total = qs.count()

        if total == 0:
            self.stdout.write(self.style.SUCCESS(
                "No expired listings need reminders right now."
            ))
            return

        self.stdout.write(f"Found {total} expired listing(s) eligible for reminder.")
        if dry_run:
            self.stdout.write(self.style.WARNING("DRY-RUN mode — no emails will be sent."))

        # ── 3. Siųsk email'us ────────────────────────────────────────
        sent = 0
        skipped = 0
        failed = 0
        site_url = getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')

        for listing in qs:
            seller = listing.seller

            # Skip jei user'is išjungęs notifikacijas
            profile = getattr(seller, 'profile', None)
            if profile and hasattr(profile, 'email_notifications'):
                if not profile.email_notifications:
                    self.stdout.write(
                        f"  ⊘ SKIP (notifications off): {seller.email} — {listing.title}"
                    )
                    skipped += 1
                    continue

            # Paskaičiuok kiek dienų jau pasibaigęs
            days_expired = None
            if listing.expires_at:
                days_expired = (now - listing.expires_at).days

            context = {
                'user_name': seller.email.split('@')[0] if seller.email else 'there',
                'listing_title': str(listing),
                # Kelias iš paties modelio — „/listings/<id>/" maršruto nėra
                'listing_url': f"{site_url}{listing.get_absolute_url()}",
                'activate_url': f"{site_url}/my-listings/",
                'days_expired': days_expired,
                'site_url': site_url,
            }

            try:
                subject = render_to_string(
                    'emails/listing_expired_reminder_subject.txt',
                    context
                ).strip()
                body = render_to_string(
                    'emails/listing_expired_reminder.txt',
                    context
                )
            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f"  ✗ TEMPLATE ERROR ({listing.pk}): {e}"
                ))
                failed += 1
                continue

            if dry_run:
                self.stdout.write(
                    f"  → WOULD SEND to {seller.email} — {listing.title} "
                    f"(expired {days_expired}d ago)"
                )
                sent += 1
                continue

            try:
                send_mail(
                    subject=subject,
                    message=body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[seller.email],
                    fail_silently=False,
                )

                # Atnaujink timestamp ant listing'o
                listing.last_expired_reminder_at = now
                listing.save(update_fields=['last_expired_reminder_at'])

                # Atnaujink scenarijaus statistiką
                scenario.total_sent = (scenario.total_sent or 0) + 1
                scenario.last_sent_at = now
                scenario.save(update_fields=['total_sent', 'last_sent_at'])

                self.stdout.write(self.style.SUCCESS(
                    f"  ✓ SENT to {seller.email} — {listing.title}"
                ))
                sent += 1

            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f"  ✗ FAILED for {seller.email}: {e}"
                ))
                failed += 1

        # ── 4. Santrauka ─────────────────────────────────────────────
        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(
            f"Done. Sent: {sent} | Skipped: {skipped} | Failed: {failed}"
        ))