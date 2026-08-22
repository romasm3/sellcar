"""
Management command: send_saved_search_notifications

Runs daily. For each SavedSearch with notify_email=True:
  - Runs the same filters as saved_searches_list view
  - Finds listings created after last_notified_at (or last_viewed_at if never notified)
  - If 1+ new results found, sends saved_search_new_results email
  - Updates last_notified_at timestamp

Usage:
    python manage.py send_saved_search_notifications
    python manage.py send_saved_search_notifications --dry-run
    python manage.py send_saved_search_notifications --force  (ignore last_notified_at)
"""
from django.core.management.base import BaseCommand

from apps.listings import param_utils
from django.conf import settings
from django.utils import timezone

from apps.listings.models import Listing, SavedSearch


MAX_LISTINGS_IN_EMAIL = 5


class Command(BaseCommand):
    help = 'Send saved search notification emails for new matching listings'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Preview without sending emails or updating timestamps',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Ignore last_notified_at (send even if recently notified)',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        force = options['force']

        searches = SavedSearch.objects.filter(
            notify_email=True
        ).select_related('user')

        total = searches.count()
        self.stdout.write(f'Processing {total} saved search(es) with notifications enabled...')
        self.stdout.write('')

        sent_count = 0
        skipped_no_results = 0
        skipped_no_email = 0

        for search in searches:
            user = search.user

            if not user.email:
                skipped_no_email += 1
                continue

            # Cutoff = last_notified_at (or last_viewed_at if never notified, or creation if never viewed)
            if not force:
                cutoff = search.last_notified_at or search.last_viewed_at or search.created_at
            else:
                cutoff = search.created_at

            # Run the same filters as saved_searches_list view
            qs = self._build_queryset(search, cutoff)
            new_count = qs.count()

            if new_count == 0:
                skipped_no_results += 1
                continue

            top_listings = list(qs.order_by('-created_at')[:MAX_LISTINGS_IN_EMAIL])
            listings_data = [
                {
                    'title': l.title,
                    'price_display': f'{l.currency_symbol}{int(l.price)}',
                    'url': f'{self._site_url()}{l.get_absolute_url()}',
                }
                for l in top_listings
            ]

            self.stdout.write(
                f'  [{search.user.email}] "{search.name}" -> {new_count} new result(s)'
            )

            success = self._send(search, user, new_count, listings_data, dry_run)

            if success:
                sent_count += 1
                if not dry_run:
                    search.last_notified_at = timezone.now()
                    search.save(update_fields=['last_notified_at'])

        prefix = '[DRY RUN] Would have sent' if dry_run else 'Sent'
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(
            f'{prefix} {sent_count} notification(s). '
            f'Skipped {skipped_no_results} (no new results), '
            f'{skipped_no_email} (no email).'
        ))

    def _site_url(self):
        return getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')

    def _build_queryset(self, search, cutoff):
        """Build filtered queryset matching saved search params + created_at > cutoff."""
        params = search.query_params or {}
        qs = Listing.objects.filter(
            status='active',
            is_shadow_banned=False,
            created_at__gt=cutoff,
        )

        qs = param_utils.filtruoti_id(qs, 'brand_id', params.get('brand'))
        qs = param_utils.filtruoti_id(qs, 'model_id', params.get('model'))
        qs = param_utils.filtruoti_reziu(qs, 'price__gte', params.get('price_min'))
        qs = param_utils.filtruoti_reziu(qs, 'price__lte', params.get('price_max'))
        qs = param_utils.filtruoti_reziu(qs, 'year__gte', params.get('year_min'))
        qs = param_utils.filtruoti_reziu(qs, 'year__lte', params.get('year_max'))
        qs = param_utils.filtruoti_id(qs, 'fuel_type_id', params.get('fuel_type'))
        qs = param_utils.filtruoti_id(qs, 'transmission_id', params.get('transmission'))
        if params.get('state_filter'):
            qs = qs.filter(country='US', state=param_utils.viena(params['state_filter']))
        elif params.get('country_filter'):
            qs = qs.filter(country=param_utils.viena(params['country_filter']))

        return qs

    def _send(self, search, user, new_count, listings_data, dry_run):
        if dry_run:
            return True

        try:
            from apps.listings.emails.sender import send_scenario
            return send_scenario(
                code='saved_search_new_results',
                to_email=user.email,
                to_user=user,
                context={
                    'user_name': user.first_name or user.username,
                    'search_name': search.name,
                    'new_count': new_count,
                    'listings': listings_data,
                    'search_url': f'{self._site_url()}/searches/',
                },
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'    FAILED to send to {user.email}: {e}'
            ))
            return False