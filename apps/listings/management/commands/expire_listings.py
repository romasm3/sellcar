"""
Management command: expire_listings

Runs daily (cron 03:30). Finds all active listings whose expires_at < now
and marks them as expired.

Covers every model that has status/expires_at/mark_expired():
Listing, Truck, WheelListing.

Usage:
    python manage.py expire_listings
    python manage.py expire_listings --dry-run  # preview without changes
"""
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.listings.models import Listing, Truck, WheelListing

EXPIRABLE_MODELS = (Listing, Truck, WheelListing)


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
        total = 0

        for model in EXPIRABLE_MODELS:
            label = model.__name__

            expiring = model.objects.filter(
                status='active',
                expires_at__lt=now,
            )
            count = expiring.count()
            if count == 0:
                self.stdout.write(f'{label}: nothing to expire.')
                continue

            total += count
            self.stdout.write(
                self.style.WARNING(f'{label}: found {count} listing(s) to expire:')
            )

            for listing in expiring:
                days_overdue = (now - listing.expires_at).days
                self.stdout.write(
                    f'  #{listing.pk} {listing.title} '
                    f'(expired {days_overdue} day(s) ago)'
                )

                if not dry_run:
                    listing.mark_expired()

        if total == 0:
            self.stdout.write(self.style.SUCCESS('No listings to expire.'))
        elif dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f'\n[DRY RUN] Would have expired {total} listing(s).'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'\nSuccessfully expired {total} listing(s).'
                )
            )
