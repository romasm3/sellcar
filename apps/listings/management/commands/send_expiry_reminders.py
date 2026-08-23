"""
Management command: send_expiry_reminders

Runs daily. Sends email reminders:
- Active listings with <= EXPIRY_REMINDER_DAYS days left → first reminder
- Expired listings → every POST_EXPIRY_REMINDER_INTERVAL_DAYS days (repeat)

Usage:
    python manage.py send_expiry_reminders
    python manage.py send_expiry_reminders --dry-run
"""
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from apps.listings.models import Listing


class Command(BaseCommand):
    help = 'Send expiry reminder emails to listing sellers'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Preview without sending emails',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']

        # Collect all listings that need a reminder
        # Active with <= 3 days left (and not yet reminded), or expired (based on last reminder)
        active_candidates = Listing.objects.filter(
            status='active',
            expires_at__isnull=False,
            last_reminder_sent_at__isnull=True,
        ).select_related('seller', 'brand', 'model')

        expired_candidates = Listing.objects.filter(
            status='expired',
            expires_at__isnull=False,
        ).select_related('seller', 'brand', 'model')

        sent_count = 0
        skipped_count = 0

        for listing in list(active_candidates) + list(expired_candidates):
            if not listing.needs_expiry_reminder():
                skipped_count += 1
                continue

            if not listing.seller.email:
                self.stdout.write(
                    self.style.WARNING(
                        f'  Skipping #{listing.pk} — seller has no email'
                    )
                )
                skipped_count += 1
                continue

            if listing.status == 'active':
                subject, result = self._send_expiring_soon(listing, dry_run)
            else:
                subject, result = self._send_expired(listing, dry_run)

            if result:
                sent_count += 1
                self.stdout.write(
                    f'  [{listing.status}] → {listing.seller.email} '
                    f'({subject})'
                )
                if not dry_run:
                    listing.last_reminder_sent_at = timezone.now()
                    listing.save(update_fields=['last_reminder_sent_at'])

        prefix = '[DRY RUN] Would have sent' if dry_run else 'Sent'
        self.stdout.write(
            self.style.SUCCESS(
                f'\n{prefix} {sent_count} reminder(s). Skipped {skipped_count}.'
            )
        )

    def _build_listing_url(self, listing):
        """Pratęsimo nuoroda — planų/apmokėjimo puslapis, ne redagavimo forma."""
        base = getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')
        return f'{base}/listings/{listing.pk}/select-plan/'

    def _send_expiring_soon(self, listing, dry_run):
        subject = f'Your listing expires in {listing.days_until_expiry} day(s)'
        context = {
            'listing': listing,
            'seller': listing.seller,
            'edit_url': self._build_listing_url(listing),
            'days_left': listing.days_until_expiry,
            'expires_at': listing.expires_at,
            'fee': listing.listing_fee,
            'payments_enabled': getattr(settings, 'PAYMENTS_ENABLED', False),
        }

        html_body = render_to_string(
            'listings/emails/expiring_soon.html', context
        )
        text_body = render_to_string(
            'listings/emails/expiring_soon.txt', context
        )

        if dry_run:
            return subject, True

        send_mail(
            subject=subject,
            message=text_body,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@sellcar.com'),
            recipient_list=[listing.seller.email],
            html_message=html_body,
            fail_silently=False,
        )
        return subject, True

    def _send_expired(self, listing, dry_run):
        days_since = listing.days_since_expired or 0
        subject = f'Your listing is inactive — reactivate to sell'

        context = {
            'listing': listing,
            'seller': listing.seller,
            'edit_url': self._build_listing_url(listing),
            'days_since_expired': days_since,
            'fee': listing.listing_fee,
            'payments_enabled': getattr(settings, 'PAYMENTS_ENABLED', False),
        }

        html_body = render_to_string(
            'listings/emails/expired.html', context
        )
        text_body = render_to_string(
            'listings/emails/expired.txt', context
        )

        if dry_run:
            return subject, True

        send_mail(
            subject=subject,
            message=text_body,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@sellcar.com'),
            recipient_list=[listing.seller.email],
            html_message=html_body,
            fail_silently=False,
        )
        return subject, True
