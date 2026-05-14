"""
Management command: cleanup_old_expired

Runs weekly. Deletes expired listings older than AUTO_DELETE_AFTER_EXPIRY_DAYS (160 days).

Usage:
    python manage.py cleanup_old_expired
    python manage.py cleanup_old_expired --dry-run
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.listings.models import Listing


class Command(BaseCommand):
    help = 'Delete expired listings older than AUTO_DELETE_AFTER_EXPIRY_DAYS'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Preview without deleting',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        cutoff = timezone.now() - timedelta(days=Listing.AUTO_DELETE_AFTER_EXPIRY_DAYS)

        to_delete = Listing.objects.filter(
            status='expired',
            expires_at__lt=cutoff,
        )

        count = to_delete.count()

        if count == 0:
            self.stdout.write(self.style.SUCCESS('No old expired listings to delete.'))
            return

        self.stdout.write(
            self.style.WARNING(
                f'Found {count} expired listing(s) older than '
                f'{Listing.AUTO_DELETE_AFTER_EXPIRY_DAYS} days:'
            )
        )

        for listing in to_delete:
            days_expired = (timezone.now() - listing.expires_at).days
            self.stdout.write(
                f'  #{listing.pk} {listing.title} '
                f'(expired {days_expired} days ago, seller: {listing.seller.email})'
            )

        if dry_run:
            self.stdout.write(
                self.style.WARNING(f'\n[DRY RUN] Would have deleted {count} listing(s).')
            )
        else:
            deleted, _ = to_delete.delete()
            self.stdout.write(
                self.style.SUCCESS(f'\nDeleted {deleted} listing(s).')
            )
