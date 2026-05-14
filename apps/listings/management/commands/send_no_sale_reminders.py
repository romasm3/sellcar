"""
Management command: send_no_sale_reminders

Siunčia 'listing_no_sale_reminder' email pardavėjams, kurių
skelbimai aktyvūs 7+ dienas ir dar nepardavę.

Paleidimas:
    python manage.py send_no_sale_reminders
    python manage.py send_no_sale_reminders --dry-run     # tik parodo, nesiunčia
    python manage.py send_no_sale_reminders --days 3      # testavimui: 3 dienos vietoj 7
    python manage.py send_no_sale_reminders --force       # ignoruoja anksčiau siųstus
"""

from datetime import timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.listings.models import Listing


class Command(BaseCommand):
    help = "Send 'listing_no_sale_reminder' email for listings active 7+ days without a sale."

    DEFAULT_DAYS = 7

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='List listings that would receive emails, but do not send.',
        )
        parser.add_argument(
            '--days',
            type=int,
            default=self.DEFAULT_DAYS,
            help=f'Minimum days a listing must be active. Default: {self.DEFAULT_DAYS}.',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Ignore last_no_sale_reminder_at check (re-send even if already sent).',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        min_days = options['days']
        force = options['force']

        now = timezone.now()
        cutoff = now - timedelta(days=min_days)

        self.stdout.write(f"[send_no_sale_reminders] Start at {now.isoformat()}")
        self.stdout.write(f"  - min_days: {min_days}")
        self.stdout.write(f"  - cutoff  : {cutoff.isoformat()}")
        self.stdout.write(f"  - dry_run : {dry_run}")
        self.stdout.write(f"  - force   : {force}")

        # Kandidatai:
        # - status = active
        # - ne shadow-banned
        # - activated_at yra ir senesnis nei cutoff
        # - (jei ne --force) dar nebuvo siųsta reminder
        qs = Listing.objects.filter(
            status='active',
            is_shadow_banned=False,
            activated_at__isnull=False,
            activated_at__lte=cutoff,
        ).select_related('seller')

        if not force:
            qs = qs.filter(last_no_sale_reminder_at__isnull=True)

        total = qs.count()
        self.stdout.write(f"  - Matching listings: {total}")

        if total == 0:
            self.stdout.write(self.style.SUCCESS("Nothing to send. Done."))
            return

        sent = 0
        skipped = 0
        failed = 0

        for listing in qs.iterator():
            seller = listing.seller
            if not seller or not seller.email:
                skipped += 1
                self.stdout.write(f"  [SKIP] Listing #{listing.pk}: no seller email")
                continue

            days_active = (now - listing.activated_at).days
            self.stdout.write(
                f"  [{('DRY-RUN' if dry_run else 'SEND')}] Listing #{listing.pk} "
                f"({listing.title[:40]}) → {seller.email} "
                f"[{days_active}d active, {listing.views_count} views]"
            )

            if dry_run:
                continue

            ok = self._send_email(listing, seller, days_active)
            if ok:
                listing.last_no_sale_reminder_at = now
                listing.save(update_fields=['last_no_sale_reminder_at'])
                sent += 1
            else:
                failed += 1

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(
            f"Done. Sent: {sent}, Skipped: {skipped}, Failed: {failed}"
        ))

    def _send_email(self, listing, seller, days_active):
        """Siunčia email'ą per scenarijų sistemą. Grąžina True jei OK."""
        try:
            from apps.listings.emails.sender import send_scenario

            edit_url = f'{settings.SITE_URL}/{listing.pk}/edit/'
            my_listings_url = f'{settings.SITE_URL}/dashboard/announcements/'

            result = send_scenario(
                code='listing_no_sale_reminder',
                to_email=seller.email,
                to_user=seller,
                context={
                    'user_name': seller.first_name or seller.username,
                    'listing_title': listing.title,
                    'listing_price_display': f'{listing.currency_symbol}{int(listing.price)}',
                    'days_active': days_active,
                    'views_count': listing.views_count or 0,
                    'saves_count': listing.saved_by.count(),
                    'edit_url': edit_url,
                    'my_listings_url': my_listings_url,
                    'listing_url': f'{settings.SITE_URL}{listing.get_absolute_url()}',
                },
            )
            return bool(result)

        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f"  [FAIL] Listing #{listing.pk}: {e}"
            ))
            return False