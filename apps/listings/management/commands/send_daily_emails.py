"""
═══════════════════════════════════════════════════════════════════
DĖK Į: apps/listings/management/commands/send_daily_emails.py
═══════════════════════════════════════════════════════════════════

Daily cron komanda - tikrina visus skelbimus/searches/users ir siunčia
reikalingus email'us.

PALEIDIMAS:
    python manage.py send_daily_emails              # paleidžia visus
    python manage.py send_daily_emails --dry-run    # nieko nesiunčia
    python manage.py send_daily_emails --only listing_expiring_soon

WINDOWS TASK SCHEDULER (kasdien 9:00):
    Action: Start a program
    Program: C:\\Users\\user\\Desktop\\programos\\sellcar\\venv\\Scripts\\python.exe
    Arguments: manage.py send_daily_emails
    Start in: C:\\Users\\user\\Desktop\\programos\\sellcar
═══════════════════════════════════════════════════════════════════
"""

from django.core.management.base import BaseCommand

from apps.listings import param_utils
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from django.db.models import Count, F, Q
from datetime import timedelta

from apps.listings.models import Listing, SavedListing, SalesRecord
from apps.listings.emails.sender import send_scenario
from apps.listings import formatai


# Views milestones - kai pasiekia šiuos skaičius, siunčia notification
VIEW_MILESTONES = [50, 100, 250, 500, 1000, 2500, 5000]


class Command(BaseCommand):
    help = 'Sends daily/scheduled email notifications (cron-style task)'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true',
                          help='Print what would be sent without sending')
        parser.add_argument('--only', type=str,
                          help='Run only this scenario (e.g. listing_expiring_soon)')

    def handle(self, *args, **options):
        self.dry_run = options.get('dry_run', False)
        self.only = options.get('only')

        if self.dry_run:
            self.stdout.write(self.style.WARNING('=== DRY RUN MODE - nothing will be sent ==='))

        self.stdout.write(self.style.SUCCESS('Running daily email tasks...'))
        self.stdout.write('')

        # Visi cron daily scenarijai (registruoti čia)
        scenarios = [
            ('listing_expiring_soon', self.send_listing_expiring_soon),
            ('listing_expired', self.send_listing_expired),
            ('listing_first_views', self.send_listing_first_views),
            ('listing_views_milestone', self.send_listing_views_milestone),
            ('listing_popular', self.send_listing_popular),
            ('listing_no_sale_reminder', self.send_listing_no_sale_reminder),
            ('listing_saved_by_users', self.send_listing_saved_by_users),
            ('saved_listing_price_drop', self.send_saved_listing_price_drop),
            ('saved_search_new_results', self.send_saved_search_new_results),
        ]

        total_sent = 0
        for code, method in scenarios:
            if self.only and self.only != code:
                continue

            self.stdout.write(self.style.MIGRATE_HEADING(f'>>> {code}'))
            try:
                count = method()
                total_sent += count
                self.stdout.write(self.style.SUCCESS(f'    {count} email(s) sent\n'))
            except Exception as e:
                import traceback
                self.stdout.write(self.style.ERROR(f'    FAILED: {e}'))
                self.stdout.write(self.style.ERROR(traceback.format_exc()))

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(
            f'=== DONE: {total_sent} email(s) sent in total ==='
        ))

    # ════════════════════════════════════════════════════════════
    # HELPERS
    # ════════════════════════════════════════════════════════════

    def _send(self, code, user, context):
        """Wrapper - dry run check + send"""
        if self.dry_run:
            return True
        return send_scenario(
            code=code, to_email=user.email, to_user=user, context=context,
        )

    # ════════════════════════════════════════════════════════════
    # 1. LISTING EXPIRING SOON
    # ════════════════════════════════════════════════════════════

    def send_listing_expiring_soon(self):
        now = timezone.now()
        cutoff_3_days = now + timedelta(days=3)
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

        listings = Listing.objects.filter(
            status='active',
            is_shadow_banned=False,
            expires_at__lte=cutoff_3_days,
            expires_at__gt=now,
        ).exclude(
            last_reminder_sent_at__gte=today_start
        ).select_related('seller', 'brand', 'model')

        count = 0
        for listing in listings:
            user = listing.seller
            if not user or not user.email:
                continue

            days_left = max(0, (listing.expires_at - now).days)
            self.stdout.write(f'    -> {user.email} | {listing.title} | {days_left}d left')

            success = self._send('listing_expiring_soon', user, {
                'user_name': user.first_name or user.username,
                'listing_title': listing.title,
                'listing_price_display': formatai.kaina(listing.price, listing.currency_symbol),
                'listing_url': f'{settings.SITE_URL}{listing.get_absolute_url()}',
                # Pratęsimas veda TIESIAI į plano/apmokėjimo puslapį, ne į edit
                'extend_url': f'{settings.SITE_URL}/listings/{listing.pk}/select-plan/',
                'renew_url': f'{settings.SITE_URL}/dashboard/announcements/',
                'days_left': days_left,
                'expires_at': listing.expires_at,
                'views_count': listing.views_count or 0,
            })

            if success and not self.dry_run:
                listing.last_reminder_sent_at = now
                listing.save(update_fields=['last_reminder_sent_at'])
                count += 1
            elif self.dry_run:
                count += 1

        return count

    # ════════════════════════════════════════════════════════════
    # 2. LISTING EXPIRED (šiandien expired)
    # ════════════════════════════════════════════════════════════

    def send_listing_expired(self):
        now = timezone.now()
        yesterday = now - timedelta(days=1)
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

        # Skelbimai kurie expire'avo per paskutines 24h
        listings = Listing.objects.filter(
            status='expired',
            expires_at__gte=yesterday,
            expires_at__lt=now,
        ).exclude(
            last_reminder_sent_at__gte=today_start
        ).select_related('seller', 'brand', 'model')

        count = 0
        for listing in listings:
            user = listing.seller
            if not user or not user.email:
                continue

            self.stdout.write(f'    -> {user.email} | {listing.title} | expired')

            success = self._send('listing_expired', user, {
                'user_name': user.first_name or user.username,
                'listing_title': listing.title,
                'listing_price_display': formatai.kaina(listing.price, listing.currency_symbol),
                'reactivate_url': f'{settings.SITE_URL}/{listing.pk}/edit/',
                'views_count': listing.views_count or 0,
            })

            if success and not self.dry_run:
                listing.last_reminder_sent_at = now
                listing.save(update_fields=['last_reminder_sent_at'])
                count += 1
            elif self.dry_run:
                count += 1

        return count

    # ════════════════════════════════════════════════════════════
    # 3. LISTING FIRST VIEWS (5+ views per pirma diena)
    # ════════════════════════════════════════════════════════════

    def send_listing_first_views(self):
        now = timezone.now()
        yesterday = now - timedelta(days=1)
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

        # Naujas skelbimas (1-3d) su 5+ views, kuriam dar nesiuntem first_views
        listings = Listing.objects.filter(
            status='active',
            is_shadow_banned=False,
            created_at__gte=now - timedelta(days=3),
            views_count__gte=5,
        ).exclude(
            last_reminder_sent_at__gte=today_start
        ).select_related('seller')

        count = 0
        for listing in listings:
            user = listing.seller
            if not user or not user.email:
                continue

            self.stdout.write(f'    -> {user.email} | {listing.title} | {listing.views_count} views')

            success = self._send('listing_first_views', user, {
                'user_name': user.first_name or user.username,
                'listing_title': listing.title,
                'listing_url': f'{settings.SITE_URL}{listing.get_absolute_url()}',
                'views_count': listing.views_count,
            })

            if success and not self.dry_run:
                listing.last_reminder_sent_at = now
                listing.save(update_fields=['last_reminder_sent_at'])
                count += 1
            elif self.dry_run:
                count += 1

        return count

    # ════════════════════════════════════════════════════════════
    # 4. LISTING VIEWS MILESTONE
    # ════════════════════════════════════════════════════════════

    def send_listing_views_milestone(self):
        """Siunčia kai pasiekia 50/100/250/500/1000+ views"""
        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

        listings = Listing.objects.filter(
            status='active',
            is_shadow_banned=False,
            views_count__gte=min(VIEW_MILESTONES),
        ).exclude(
            last_reminder_sent_at__gte=today_start
        ).select_related('seller')

        count = 0
        for listing in listings:
            user = listing.seller
            if not user or not user.email:
                continue

            # Find highest milestone reached
            milestone = None
            for m in VIEW_MILESTONES:
                if listing.views_count >= m:
                    milestone = m
                else:
                    break

            if not milestone:
                continue

            self.stdout.write(f'    -> {user.email} | {listing.title} | {listing.views_count} views')

            success = self._send('listing_views_milestone', user, {
                'user_name': user.first_name or user.username,
                'listing_title': listing.title,
                'listing_price_display': formatai.kaina(listing.price, listing.currency_symbol),
                # Laiške rodom TIKSLŲ skaičių (154), o ne pakopą (100) —
                # pakopa lieka tik tam, kad žinotume, kada verta siųsti.
                'views_count': listing.views_count,
                'milestone': milestone,
                'stats_url': f'{settings.SITE_URL}/{listing.pk}/stats/',
            })

            if success and not self.dry_run:
                listing.last_reminder_sent_at = now
                listing.save(update_fields=['last_reminder_sent_at'])
                count += 1
            elif self.dry_run:
                count += 1

        return count

    # ════════════════════════════════════════════════════════════
    # 5. LISTING POPULAR (top 10% by CTR)
    # ════════════════════════════════════════════════════════════

    def send_listing_popular(self):
        """Top 10% pagal views/impressions ratio"""
        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

        # Tik aktyvūs su >10 views ir >50 impressions
        candidates = Listing.objects.filter(
            status='active',
            is_shadow_banned=False,
            views_count__gte=10,
            impressions_count__gte=50,
        ).exclude(
            last_reminder_sent_at__gte=today_start
        ).select_related('seller')

        count = 0
        for listing in candidates:
            user = listing.seller
            if not user or not user.email:
                continue

            ctr = listing.views_count / listing.impressions_count if listing.impressions_count else 0
            # Top 10% = CTR > 0.10 (10%)
            if ctr < 0.10:
                continue

            self.stdout.write(f'    -> {user.email} | {listing.title} | CTR {ctr*100:.1f}%')

            success = self._send('listing_popular', user, {
                'user_name': user.first_name or user.username,
                'listing_title': listing.title,
                'listing_price_display': formatai.kaina(listing.price, listing.currency_symbol),
                'listing_url': f'{settings.SITE_URL}{listing.get_absolute_url()}',
                'views_count': listing.views_count,
                'percentile': 10,
            })

            if success and not self.dry_run:
                listing.last_reminder_sent_at = now
                listing.save(update_fields=['last_reminder_sent_at'])
                count += 1
            elif self.dry_run:
                count += 1

        return count

    # ════════════════════════════════════════════════════════════
    # 6. LISTING NO SALE REMINDER (14 dienos be sale)
    # ════════════════════════════════════════════════════════════

    def send_listing_no_sale_reminder(self):
        now = timezone.now()
        cutoff = now - timedelta(days=14)
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

        listings = Listing.objects.filter(
            status='active',
            is_shadow_banned=False,
            created_at__lte=cutoff,
        ).exclude(
            last_reminder_sent_at__gte=today_start
        ).select_related('seller')

        count = 0
        for listing in listings:
            user = listing.seller
            if not user or not user.email:
                continue

            days_active = (now - listing.created_at).days
            saves_count = listing.saved_by.count() if hasattr(listing, 'saved_by') else 0

            self.stdout.write(f'    -> {user.email} | {listing.title} | {days_active}d active')

            success = self._send('listing_no_sale_reminder', user, {
                'user_name': user.first_name or user.username,
                'listing_title': listing.title,
                'listing_price_display': formatai.kaina(listing.price, listing.currency_symbol),
                'days_active': days_active,
                'views_count': listing.views_count or 0,
                'saves_count': saves_count,
                'edit_url': f'{settings.SITE_URL}/{listing.pk}/edit/',
                'photo_edit_url': f'{settings.SITE_URL}/{listing.pk}/edit/section/images/',
                'renew_url': f'{settings.SITE_URL}/dashboard/announcements/',
            })

            if success and not self.dry_run:
                listing.last_reminder_sent_at = now
                listing.save(update_fields=['last_reminder_sent_at'])
                count += 1
            elif self.dry_run:
                count += 1

        return count

    # ════════════════════════════════════════════════════════════
    # 7. LISTING SAVED BY USERS (kai išsaugoja N kartų)
    # ════════════════════════════════════════════════════════════

    def send_listing_saved_by_users(self):
        """Siunčiamas, kai skelbimas yra išsaugotas 3+ kartų"""
        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

        # Skelbimai su 3+ saves
        listings = Listing.objects.filter(
            status='active',
            is_shadow_banned=False,
        ).exclude(
            last_reminder_sent_at__gte=today_start
        ).annotate(
            saves_count=Count('saved_by')
        ).filter(saves_count__gte=3).select_related('seller')

        count = 0
        for listing in listings:
            user = listing.seller
            if not user or not user.email:
                continue

            saves_count = listing.saves_count
            self.stdout.write(f'    -> {user.email} | {listing.title} | {saves_count} saves')

            success = self._send('listing_saved_by_users', user, {
                'user_name': user.first_name or user.username,
                'listing_title': listing.title,
                'listing_price_display': formatai.kaina(listing.price, listing.currency_symbol),
                'listing_url': f'{settings.SITE_URL}{listing.get_absolute_url()}',
                'saves_count': saves_count,
            })

            if success and not self.dry_run:
                listing.last_reminder_sent_at = now
                listing.save(update_fields=['last_reminder_sent_at'])
                count += 1
            elif self.dry_run:
                count += 1

        return count

    # ════════════════════════════════════════════════════════════
    # 8. SAVED LISTING PRICE DROP
    # ════════════════════════════════════════════════════════════

    def send_saved_listing_price_drop(self):
        """
        TODO: Reikia kainos istorijos lentelės (PriceHistory).
        Kol jos nėra - skip.
        """
        self.stdout.write('    [SKIP] Reikia PriceHistory modelio (dar neimplementuota)')
        return 0

    # ════════════════════════════════════════════════════════════
    # 9. SAVED SEARCH NEW RESULTS
    # ════════════════════════════════════════════════════════════

    def send_saved_search_new_results(self):
        """
        Tikrina visas SavedSearch su notify_email=True ir
        siunčia jei rado naujų skelbimų po last_viewed_at.
        """
        from apps.listings.models import SavedSearch

        searches = SavedSearch.objects.filter(notify_email=True).select_related('user')

        count = 0
        for search in searches:
            user = search.user
            if not user or not user.email:
                continue

            params = search.query_params
            qs = Listing.objects.filter(status='active', is_shadow_banned=False)

            qs = param_utils.filtruoti_id(qs, 'brand_id', params.get('brand'))
            qs = param_utils.filtruoti_id(qs, 'model_id', params.get('model'))
            qs = param_utils.filtruoti_reziu(qs, 'price__gte', params.get('price_min'))
            qs = param_utils.filtruoti_reziu(qs, 'price__lte', params.get('price_max'))
            qs = param_utils.filtruoti_reziu(qs, 'year__gte', params.get('year_min'))
            qs = param_utils.filtruoti_reziu(qs, 'year__lte', params.get('year_max'))
            qs = param_utils.filtruoti_id(qs, 'fuel_type_id', params.get('fuel_type'))

            # Tik nauji po paskutinio peržiūrėjimo
            if search.last_viewed_at:
                qs = qs.filter(created_at__gt=search.last_viewed_at)

            new_count = qs.count()
            if new_count == 0:
                continue

            top_listings = qs.order_by('-created_at')[:5]
            listings_data = [{
                'title': l.title,
                'price_display': formatai.kaina(l.price, l.currency_symbol),
                'url': f'{settings.SITE_URL}{l.get_absolute_url()}',
            } for l in top_listings]

            self.stdout.write(f'    -> {user.email} | search: {search.name} | {new_count} new')

            self._send('saved_search_new_results', user, {
                'user_name': user.first_name or user.username,
                'search_name': search.name,
                'new_count': new_count,
                'listings': listings_data,
                'search_url': f'{settings.SITE_URL}/searches/',
            })

            if not self.dry_run:
                count += 1
            else:
                count += 1

        return count
