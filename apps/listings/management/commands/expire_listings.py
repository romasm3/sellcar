"""
Management command: expire_listings

Runs daily. Finds all active listings whose expires_at < now and marks them as expired.

Usage:
    python manage.py expire_listings
    python manage.py expire_listings --dry-run  # preview without changes
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.listings.models import Listing


class Command(BaseCommand):
    help = 'Expire active listings whose expires_at has passed'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Preview changes without saving',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        now = timezone.now()

        # Find active listings that should be expired
        expiring = Listing.objects.filter(
            status='active',
            expires_at__lt=now,
        )

        count = expiring.count()

        if count == 0:
            self.stdout.write(self.style.SUCCESS('No listings to expire.'))
            return

        self.stdout.write(
            self.style.WARNING(f'Found {count} listing(s) to expire:')
        )

        for listing in expiring:
            days_overdue = (now - listing.expires_at).days
            self.stdout.write(
                f'  #{listing.pk} {listing.title} '
                f'(expired {days_overdue} day(s) ago)'
            )

            if not dry_run:
                listing.mark_expired()

        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f'\n[DRY RUN] Would have expired {count} listing(s).'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'\nSuccessfully expired {count} listing(s).'
                )
            )
