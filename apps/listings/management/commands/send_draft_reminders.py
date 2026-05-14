"""
Send draft reminder emails to sellers with unactivated draft listings.

Schedule:
- 1h after creation → 'draft_reminder_first'
- 24h after creation → 'draft_reminder_24h'
- Every 24h after that → 'draft_reminder_daily' (until activated or deleted)

Usage:
    python manage.py send_draft_reminders
    python manage.py send_draft_reminders --dry-run

Cron: Run every hour (command handles throttling internally)
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import timedelta

from apps.listings.models import Listing, EmailScenario


class Command(BaseCommand):
    help = 'Send reminders for unactivated draft listings'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Print what would be sent without actually sending emails',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        now = timezone.now()

        drafts = Listing.objects.filter(status='draft').select_related(
            'seller', 'motorcycle_brand', 'motorcycle_model', 'brand', 'model'
        )

        sent_count = 0
        skipped_count = 0

        self.stdout.write(f'\n=== Draft Reminder Check @ {now} ===')
        self.stdout.write(f'Found {drafts.count()} draft listings\n')

        for draft in drafts:
            result = self._process_draft(draft, now, dry_run)
            if result == 'sent':
                sent_count += 1
            else:
                skipped_count += 1

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(
            f'Done! Sent: {sent_count}, Skipped: {skipped_count}'
        ))

    def _process_draft(self, draft, now, dry_run):
        """Decide which email (if any) to send for this draft."""
        seller = draft.seller
        if not seller or not seller.email:
            self.stdout.write(f'  · Skip #{draft.pk}: no seller email')
            return 'skipped'

        age = now - draft.created_at
        age_hours = age.total_seconds() / 3600

        # Determine which reminder to send
        scenario_code = None
        email_subject = None
        template_name = None

        if draft.draft_reminder_count == 0:
            # First email — 1h after creation
            if age_hours >= 1:
                scenario_code = 'draft_reminder_first'
                email_subject = 'Complete your listing — just a few minutes left!'
                template_name = 'emails/draft_reminder_first.html'
            else:
                return 'skipped'

        elif draft.draft_reminder_count == 1:
            # Second email — 24h after creation
            if age_hours >= 24:
                scenario_code = 'draft_reminder_24h'
                email_subject = "Don't let your listing go to waste"
                template_name = 'emails/draft_reminder_daily.html'
            else:
                return 'skipped'

        else:
            # Daily — at least 24h since last reminder
            if not draft.last_draft_reminder_at:
                return 'skipped'
            since_last = now - draft.last_draft_reminder_at
            if since_last.total_seconds() < 24 * 3600:
                return 'skipped'

            scenario_code = 'draft_reminder_daily'
            email_subject = 'Your listing is still waiting for activation'
            template_name = 'emails/draft_reminder_daily.html'

        # Check scenario enabled in DB
        try:
            scenario = EmailScenario.objects.get(code=scenario_code)
            if not scenario.is_enabled:
                self.stdout.write(f'  · Skip #{draft.pk}: scenario {scenario_code} disabled')
                return 'skipped'
        except EmailScenario.DoesNotExist:
            self.stdout.write(f'  · Skip #{draft.pk}: scenario {scenario_code} not in DB')
            return 'skipped'

        # Build email context
        display_title = self._build_display_title(draft)
        site_url = getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')

        context = {
            'seller_name': seller.first_name or seller.username,
            'listing': draft,
            'display_title': display_title,
            'activation_url': f'{site_url}/{draft.pk}/activation-plans/',
            'listings_url': f'{site_url}/dashboard/announcements/?status=inactive',
            'age_hours': int(age_hours),
            'age_days': int(age.days),
            'site_url': site_url,
        }

        if dry_run:
            self.stdout.write(
                f'  [DRY RUN] Would send "{scenario_code}" to {seller.email} '
                f'(draft #{draft.pk}, age={age_hours:.1f}h, count={draft.draft_reminder_count})'
            )
            return 'sent'

        # Send email
        try:
            html_body = render_to_string(template_name, context)
            msg = EmailMultiAlternatives(
                subject=email_subject,
                body=f'Complete your listing: {context["activation_url"]}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[seller.email],
            )
            msg.attach_alternative(html_body, 'text/html')
            msg.send()

            # Update draft counters
            draft.last_draft_reminder_at = now
            draft.draft_reminder_count += 1
            draft.save(update_fields=['last_draft_reminder_at', 'draft_reminder_count'])

            # Update scenario stats
            scenario.send_count += 1
            scenario.last_sent_at = now
            scenario.save(update_fields=['send_count', 'last_sent_at'])

            self.stdout.write(self.style.SUCCESS(
                f'  ✓ Sent "{scenario_code}" to {seller.email} (draft #{draft.pk})'
            ))
            return 'sent'

        except Exception as e:
            try:
                scenario.fail_count += 1
                scenario.last_failed_at = now
                scenario.last_error = str(e)[:500]
                scenario.save(update_fields=['fail_count', 'last_failed_at', 'last_error'])
            except Exception:
                pass

            self.stdout.write(self.style.ERROR(
                f'  ✗ Failed #{draft.pk}: {e}'
            ))
            return 'skipped'

    def _build_display_title(self, draft):
        """Build display title for email (handles cars + motorcycles)."""
        if draft.is_motorcycle:
            if draft.motorcycle_brand:
                parts = [draft.motorcycle_brand.name]
                if draft.motorcycle_model:
                    parts.append(draft.motorcycle_model.name)
                if draft.year:
                    parts.append(str(draft.year))
                return ' '.join(parts)
            return 'Your motorcycle listing'
        else:
            if draft.brand:
                parts = [draft.brand.name]
                if draft.model:
                    parts.append(draft.model.name)
                if draft.year:
                    parts.append(str(draft.year))
                return ' '.join(parts)
            return 'Your vehicle listing'