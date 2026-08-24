"""
Management command: send_renew_reminders

Siunčia 'listing_auto_renew_reminder' email pardavėjams, kurių
skelbimai netrukus baigsis (default: likę 3 dienos).

Paleidimas:
    python manage.py send_renew_reminders
    python manage.py send_renew_reminders --dry-run
    python manage.py send_renew_reminders --days 5
    python manage.py send_renew_reminders --force
"""

from datetime import timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.listings.models import Listing
from apps.listings import formatai


class Command(BaseCommand):
    help = "Send 'listing_auto_renew_reminder' email for listings expiring soon."

    DEFAULT_DAYS_BEFORE_EXPIRE = 3

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='List listings that would receive emails, but do not send.',
        )
        parser.add_argument(
            '--days',
            type=int,
            default=self.DEFAULT_DAYS_BEFORE_EXPIRE,
            help=f'Days before expire to send reminder. Default: {self.DEFAULT_DAYS_BEFORE_EXPIRE}.',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Ignore last_reminder_sent_at check (re-send even if already sent).',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        days_before = options['days']
        force = options['force']

        now = timezone.now()
        cutoff = now + timedelta(days=days_before)

        self.stdout.write(f"[send_renew_reminders] Start at {now.isoformat()}")
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
            from django.db.models import Q
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
                self.stdout.write(f"  [SKIP] Listing #{listing.pk}: no seller email")
                continue

            days_until_expire = (listing.expires_at - now).days
            self.stdout.write(
                f"  [{('DRY-RUN' if dry_run else 'SEND')}] Listing #{listing.pk} "
                f"({listing.title[:40]}) -> {seller.email} "
                f"[expires in {days_until_expire}d, {listing.views_count} views]"
            )

            if dry_run:
                continue

            ok = self._send_email(listing, seller, days_until_expire)
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

    def _send_email(self, listing, seller, days_until_expire):
        try:
            from apps.listings.emails.sender import send_scenario

            my_listings_url = f'{settings.SITE_URL}/dashboard/announcements/'

            result = send_scenario(
                code='listing_auto_renew_reminder',
                to_email=seller.email,
                to_user=seller,
                context={
                    'user_name': seller.first_name or seller.username,
                    'listing_title': listing.title,
                    'listing_price_display': formatai.kaina(listing.price, listing.currency_symbol),
                    'days_until_expire': max(days_until_expire, 0),
                    'views_count': listing.views_count or 0,
                    'saves_count': listing.saved_by.count(),
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