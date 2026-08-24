"""
Management command: send_expiring_soon

Siunčia 'listing_expiring_soon' email pardavėjams, kurių skelbimai
baigsis per mažiau nei 1 dieną.

Paleidimas:
    python manage.py send_expiring_soon
    python manage.py send_expiring_soon --dry-run
    python manage.py send_expiring_soon --days 365      # testavimui
    python manage.py send_expiring_soon --force
"""

from datetime import timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone

from apps.listings.models import Listing
from apps.listings import formatai


class Command(BaseCommand):
    help = "Send 'listing_expiring_soon' email for listings expiring in 1 day."

    DEFAULT_DAYS = 1

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
            help=f'Days before expire. Default: {self.DEFAULT_DAYS}.',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Ignore last_reminder_sent_at check.',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        days_before = options['days']
        force = options['force']

        now = timezone.now()
        cutoff = now + timedelta(days=days_before)

        self.stdout.write(f"[send_expiring_soon] Start at {now.isoformat()}")
        self.stdout.write(f"  - days_before: {days_before}")
        self.stdout.write(f"  - cutoff     : {cutoff.isoformat()}")
        self.stdout.write(f"  - dry_run    : {dry_run}")
        self.stdout.write(f"  - force      : {force}")

        qs = Listing.objects.filter(
            status='active',
            is_shadow_banned=False,
            expires_at__isnull=False,
            expires_at__gte=now,
            expires_at__lte=cutoff,
        ).select_related('seller')

        if not force:
            one_day_ago = now - timedelta(hours=24)
            qs = qs.filter(
                Q(last_reminder_sent_at__isnull=True) |
                Q(last_reminder_sent_at__lt=one_day_ago)
            )

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
                continue

            hours_left = int((listing.expires_at - now).total_seconds() / 3600)
            self.stdout.write(
                f"  [{('DRY-RUN' if dry_run else 'SEND')}] Listing #{listing.pk} "
                f"({listing.title[:40]}) -> {seller.email} "
                f"[expires in {hours_left}h]"
            )

            if dry_run:
                continue

            ok = self._send_email(listing, seller)
            if ok:
                listing.last_reminder_sent_at = now
                listing.save(update_fields=['last_reminder_sent_at'])
                sent += 1
            else:
                failed += 1

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(
            f"Done. Sent: {sent}, Skipped: {skipped}, Failed: {failed}"
        ))

    def _send_email(self, listing, seller):
        try:
            from apps.listings.emails.sender import send_scenario

            now = timezone.now()
            seconds_left = (listing.expires_at - now).total_seconds()
            days_left = max(0, int(seconds_left // 86400))

            site_url = settings.SITE_URL
            listing_url = f'{site_url}{listing.get_absolute_url()}'
            my_listings_url = f'{site_url}/dashboard/announcements/'
            # Pratęsimas veda TIESIAI į plano/apmokėjimo puslapį, ne į edit
            extend_url = f'{site_url}/listings/{listing.pk}/select-plan/'

            # Vardas: first_name > email prefix (NE username, jis gali būti "COMPANY")
            if seller.first_name:
                user_name = seller.first_name
            elif seller.email:
                user_name = seller.email.split('@')[0]
            else:
                user_name = 'there'

            result = send_scenario(
                code='listing_expiring_soon',
                to_email=seller.email,
                to_user=seller,
                context={
                    'user_name': user_name,
                    'listing_title': listing.title,
                    'listing_price_display': formatai.kaina(listing.price, listing.currency_symbol),
                    'views_count': listing.views_count or 0,
                    'saves_count': listing.saved_by.count(),
                    'days_left': days_left,
                    'expires_at': listing.expires_at,
                    'listing_url': listing_url,
                    'extend_url': extend_url,
                    'renew_url': my_listings_url,
                    'my_listings_url': my_listings_url,
                    'site_url': site_url,
                },
            )
            return bool(result)

        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f"  [FAIL] Listing #{listing.pk}: {e}"
            ))
            return False