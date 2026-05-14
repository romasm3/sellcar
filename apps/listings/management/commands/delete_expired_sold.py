"""
Auto-delete SOLD listings that are older than SOLD_DISPLAY_DAYS.

USAGE:
    python manage.py delete_expired_sold

Paleidžiam per Task Scheduler (Windows) ar cron (Linux) kasdien.

FAILAS TURI BŪT ČIA:
    apps/listings/management/commands/delete_expired_sold.py

Jei neturi šių folder'ių, juos sukurk:
    apps/listings/management/
    apps/listings/management/__init__.py       (tuščias failas)
    apps/listings/management/commands/
    apps/listings/management/commands/__init__.py   (tuščias failas)
    apps/listings/management/commands/delete_expired_sold.py   <-- ŠITAS FAILAS
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from apps.listings.models import Listing


class Command(BaseCommand):
    help = 'Auto-delete SOLD listings that are older than SOLD_DISPLAY_DAYS.'

    def handle(self, *args, **options):
        cutoff = timezone.now() - timedelta(days=Listing.SOLD_DISPLAY_DAYS)

        # Surandame seno skelbimus
        expired_sold = Listing.objects.filter(
            status='sold',
            sold_at__lte=cutoff,
        )

        count = expired_sold.count()

        if count == 0:
            self.stdout.write(self.style.SUCCESS(
                f'No expired SOLD listings to delete (cutoff: {cutoff.strftime("%Y-%m-%d %H:%M")}).'
            ))
            return

        # Surašom informaciją prieš trynimą
        self.stdout.write(f'Found {count} expired SOLD listings to delete:')
        for listing in expired_sold[:10]:  # Pirmi 10 logui
            days_old = (timezone.now() - listing.sold_at).days if listing.sold_at else 0
            self.stdout.write(
                f'  #{listing.pk}: {listing.title} '
                f'(sold {days_old} days ago, seller: {listing.seller.email})'
            )

        if count > 10:
            self.stdout.write(f'  ... and {count - 10} more.')

        # Trinam (SalesRecord jau yra sukurtas, išliks)
        deleted, _ = expired_sold.delete()

        self.stdout.write(self.style.SUCCESS(
            f'✓ Successfully deleted {deleted} expired SOLD listings.'
        ))