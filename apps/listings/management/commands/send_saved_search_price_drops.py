"""
Management command: send_saved_search_price_drops

Kasdien (cron) tikrina kiekvieną SavedSearch su notify_email=True:
  - Randa pigiausią skelbimą atitinkantį paieškos kriterijus
  - Lygina su `last_min_price` (paskutinė žinoma min kaina)
  - Jei pigiausia kaina krito → siunčia email
  - Atnaujina `last_min_price` ir `last_checked_at`

Paleidimas:
    python manage.py send_saved_search_price_drops
    python manage.py send_saved_search_price_drops --dry-run
    python manage.py send_saved_search_price_drops --force
"""

from django.conf import settings
from django.core.management.base import BaseCommand

from apps.listings import param_utils
from django.utils import timezone

from apps.listings.models import Listing, SavedSearch, EmailScenario


class Command(BaseCommand):
    help = "Send 'saved_search_price_drops' emails when lowest price in saved search drops."

    SCENARIO_CODE = 'saved_search_price_drops'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Preview without sending or updating timestamps.',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Ignore last_min_price check — send if any match exists.',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        force = options['force']

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

        # ── 2. Iterate saved searches ────────────────────────────────
        searches = SavedSearch.objects.filter(
            notify_email=True
        ).select_related('user')

        total = searches.count()
        self.stdout.write(f'Processing {total} saved search(es) with notifications enabled...')
        self.stdout.write('')

        sent = 0
        skipped_no_match = 0
        skipped_no_drop = 0
        failed = 0
        now = timezone.now()
        site_url = getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')

        for search in searches:
            user = search.user
            if not user or not user.email:
                continue

            qs = self._build_queryset(search)
            cheapest = qs.order_by('price').first()

            if not cheapest:
                skipped_no_match += 1
                continue

            current_min = float(cheapest.price)
            previous_min = float(search.last_min_price) if search.last_min_price else None

            # Nusprendžiam ar siųsti email
            should_send = False
            if force:
                should_send = True
            elif previous_min is None:
                # Pirmas kartas kai tikrinam — tik issaugom, nesiunčiam
                should_send = False
            elif current_min < previous_min:
                should_send = True

            if not should_send:
                skipped_no_drop += 1
                # Atnaujink min tik jei tikrinam pirmą kartą
                if not dry_run and previous_min is None:
                    search.last_min_price = current_min
                    search.last_checked_at = now
                    search.save(update_fields=['last_min_price', 'last_checked_at'])
                continue

            # Siųsk email
            old_price = previous_min if previous_min else current_min
            drop_amount = max(0, old_price - current_min)
            percent_off = int(round((drop_amount / old_price) * 100)) if old_price > 0 else 0
            sym = cheapest.currency_symbol

            try:
                listing_url = f'{site_url}{cheapest.get_absolute_url()}'
            except Exception:
                listing_url = f'{site_url}/listings/{cheapest.pk}/'

            listings_data = [{
                'title': cheapest.title,
                'old_price': f'{sym}{int(old_price)}',
                'new_price': f'{sym}{int(current_min)}',
                'percent_off': percent_off,
                'url': listing_url,
            }]

            self.stdout.write(
                f'  [{user.email}] "{search.name}" -> '
                f'{sym}{int(old_price)} → {sym}{int(current_min)} (-{percent_off}%)'
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
                        'listings': listings_data,
                        'search_url': f'{site_url}/searches/',
                        'site_url': site_url,
                    },
                )

                search.last_min_price = current_min
                search.last_checked_at = now
                search.save(update_fields=['last_min_price', 'last_checked_at'])

                sent += 1

            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f'    FAILED to send to {user.email}: {e}'
                ))
                failed += 1

        # ── 3. Santrauka ─────────────────────────────────────────────
        prefix = '[DRY RUN] Would have sent' if dry_run else 'Sent'
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(
            f'{prefix} {sent} notification(s). '
            f'Skipped {skipped_no_match} (no matches), '
            f'{skipped_no_drop} (no price drop), '
            f'{failed} (failed).'
        ))

    def _build_queryset(self, search):
        """Pritaiko SavedSearch query_params filtrus į Listing queryset (be is_shadow_banned, be created_at)."""
        params = search.query_params or {}
        qs = Listing.objects.filter(
            status='active',
            is_shadow_banned=False,
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