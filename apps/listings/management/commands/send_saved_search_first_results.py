"""
Management command: send_saved_search_first_results

Siunčia 'saved_search_first_results' email'ą kai SavedSearch (su notify_email=True)
pirmą kartą gauna matching skelbimų.

Sąlyga: last_notified_at IS NULL (niekada nebuvo notifikuota) IR yra >=1 match.

Po išsiuntimo paieška pažymima kaip notifikuota (last_notified_at = now).
Nuo tada ateities pranešimus apie naujus skelbimus tvarko
`send_saved_search_notifications` komanda.

Paleidimas:
    python manage.py send_saved_search_first_results
    python manage.py send_saved_search_first_results --dry-run
"""

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.listings.models import Listing, SavedSearch, EmailScenario


class Command(BaseCommand):
    help = "Send 'saved_search_first_results' email for never-notified saved searches with results."

    SCENARIO_CODE = 'saved_search_first_results'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Preview without sending or updating timestamps.',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']

        # ── 1. Scenarijus enabled? ───────────────────────────────────
        try:
            scenario = EmailScenario.objects.get(code=self.SCENARIO_CODE)
        except EmailScenario.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                f"EmailScenario '{self.SCENARIO_CODE}' not found in DB."
            ))
            return

        if not scenario.is_enabled:
            self.stdout.write(self.style.WARNING(
                f"Scenario '{self.SCENARIO_CODE}' is DISABLED."
            ))
            return

        # ── 2. Surask paieškas kurios niekada nenotifikuotos ─────────
        searches = SavedSearch.objects.filter(
            notify_email=True,
            last_notified_at__isnull=True,
        ).select_related('user')

        total = searches.count()
        self.stdout.write(
            f'Processing {total} never-notified saved search(es)...'
        )

        if total == 0:
            return

        sent = 0
        skipped_no_match = 0
        failed = 0
        now = timezone.now()
        site_url = getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')

        for search in searches:
            user = search.user
            if not user or not user.email:
                continue

            qs = self._build_queryset(search)
            count = qs.count()

            if count == 0:
                skipped_no_match += 1
                continue

            search_url = f'{site_url}/searches/'

            action = 'WOULD SEND' if dry_run else 'SEND'
            self.stdout.write(
                f'  [{action}] user={user.email} search="{search.name}" '
                f'first_count={count}'
            )

            if dry_run:
                sent += 1
                continue

            try:
                from apps.listings.emails.sender import send_scenario
                send_scenario(
                    code=self.SCENARIO_CODE,
                    to_email=user.email,
                    to_user=user,
                    context={
                        'search_name': search.name,
                        'count': count,
                        'search_url': search_url,
                        'site_url': site_url,
                    },
                )

                # Pažymėk kaip notifikuotą — ateityje
                # send_saved_search_notifications tvarkys naujus rezultatus
                search.last_notified_at = now
                search.save(update_fields=['last_notified_at'])

                sent += 1

            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f'    FAILED to send to {user.email}: {e}'
                ))
                failed += 1

        prefix = '[DRY RUN] Would have sent' if dry_run else 'Sent'
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(
            f'{prefix} {sent} notification(s). '
            f'Skipped {skipped_no_match} (no matches), '
            f'{failed} (failed).'
        ))

    def _build_queryset(self, search):
        """Pritaiko SavedSearch query_params filtrus į Listing queryset."""
        params = search.query_params or {}
        qs = Listing.objects.filter(
            status='active',
            is_shadow_banned=False,
        )

        if params.get('brand'):
            qs = qs.filter(brand_id=params['brand'])
        if params.get('model'):
            qs = qs.filter(model_id=params['model'])
        if params.get('price_min'):
            qs = qs.filter(price__gte=params['price_min'])
        if params.get('price_max'):
            qs = qs.filter(price__lte=params['price_max'])
        if params.get('year_min'):
            qs = qs.filter(year__gte=params['year_min'])
        if params.get('year_max'):
            qs = qs.filter(year__lte=params['year_max'])
        if params.get('fuel_type'):
            qs = qs.filter(fuel_type_id=params['fuel_type'])
        if params.get('transmission'):
            qs = qs.filter(transmission_id=params['transmission'])
        if params.get('state_filter'):
            qs = qs.filter(country='US', state=params['state_filter'])
        elif params.get('country_filter'):
            qs = qs.filter(country=params['country_filter'])

        return qs