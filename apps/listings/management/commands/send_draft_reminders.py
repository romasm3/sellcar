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

from django.utils import translation
from django.utils.translation import gettext as _

from apps.listings.models import Listing, EmailScenario

# Temos — msgid angliški, vertimai locale/*/django.po (LT: „Užbaikite …").
TEMOS = {
    'draft_reminder_first': 'Complete your listing — just a few minutes left!',
    'draft_reminder_24h': "Don't let your listing go to waste",
    'draft_reminder_daily': 'Your listing is still waiting for activation',
}
SABLONAI = {
    'draft_reminder_first': 'emails/draft_reminder_first.html',
    'draft_reminder_24h': 'emails/draft_reminder_daily.html',
    'draft_reminder_daily': 'emails/draft_reminder_daily.html',
}


# Laiško kalba — viena funkcija visiems laiškams (profilis → LANGUAGE_CODE)
from apps.accounts.notifications import (  # noqa: E402
    galima_siusti, gavejo_kalba, prijunk_atsisakyma)


def rodomas_pavadinimas(draft):
    """Skelbimo pavadinimas laiške (vartotojo kalba jau aktyvuota)."""
    if (draft.title or '').strip():
        return draft.title.strip()
    if draft.is_motorcycle and draft.motorcycle_brand:
        dalys = [draft.motorcycle_brand.name]
        if draft.motorcycle_model:
            dalys.append(draft.motorcycle_model.name)
    elif draft.brand:
        dalys = [draft.brand.name]
        if draft.model:
            dalys.append(draft.model.name)
    else:
        return _('Your listing')
    if draft.year:
        dalys.append(str(draft.year))
    return ' '.join(dalys)


def priminimo_laiskas(draft, scenarijus, site_url=None):
    """(tema, tekstas, html) — gavėjo kalba, su vieno paspaudimo nuoroda.

    „Aktyvuoti skelbimą" = GET /listings/<id>/activate/?t=<pasirašytas
    tokenas> (apps/listings/aktyvavimas.py) — aktyvuoja iš karto. Anksčiau
    vesdavo į /<id>/activation-plans/, o iš ten į redagavimo formą.
    „Redaguoti skelbimą" — /<id>/edit/ (anksčiau /create/ — naujas skelbimas!).
    """
    from apps.listings.aktyvavimas import aktyvavimo_nuoroda
    site_url = site_url if site_url is not None else getattr(
        settings, 'SITE_URL', 'http://127.0.0.1:8000')
    seller = draft.seller
    kalba = gavejo_kalba(seller)
    with translation.override(kalba):
        aktyvavimas = aktyvavimo_nuoroda(draft, site_url)
        context = {
            'kalba': kalba,
            'seller_name': seller.first_name or seller.username,
            'listing': draft,
            'display_title': rodomas_pavadinimas(draft),
            'activation_url': aktyvavimas,
            'edit_url': f'{site_url}{draft.get_edit_url()}',
            'listings_url': f'{site_url}/dashboard/announcements/?status=inactive',
            'site_url': site_url,
        }
        html = render_to_string(SABLONAI[scenarijus], context)
        tema = _(TEMOS[scenarijus])
        tekstas = _('Activate your listing: %(url)s') % {'url': aktyvavimas}
    # „Atsisakyti šių pranešimų" — išjungia tik aktyvavimo priminimus
    tekstas, html = prijunk_atsisakyma(seller, 'aktyvavimas', tekstas, html)
    return tema, tekstas, html


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

        if draft.draft_reminder_count == 0:
            # First email — 1h after creation
            if age_hours >= 1:
                scenario_code = 'draft_reminder_first'
            else:
                return 'skipped'

        elif draft.draft_reminder_count == 1:
            # Second email — 24h after creation
            if age_hours >= 24:
                scenario_code = 'draft_reminder_24h'
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

        # Naudotojo nustatymai: „Priminimai aktyvuoti neaktyvuotą skelbimą"
        # ir pagrindinis „Nesiųsti jokių laiškų apie mano skelbimus"
        if not galima_siusti(seller, 'aktyvavimas'):
            self.stdout.write(f'  · Skip #{draft.pk}: išjungta nustatymuose')
            return 'skipped'

        # Check scenario enabled in DB
        try:
            scenario = EmailScenario.objects.get(code=scenario_code)
            if not scenario.is_enabled:
                self.stdout.write(f'  · Skip #{draft.pk}: scenario {scenario_code} disabled')
                return 'skipped'
        except EmailScenario.DoesNotExist:
            self.stdout.write(f'  · Skip #{draft.pk}: scenario {scenario_code} not in DB')
            return 'skipped'

        if dry_run:
            self.stdout.write(
                f'  [DRY RUN] Would send "{scenario_code}" to {seller.email} '
                f'(draft #{draft.pk}, age={age_hours:.1f}h, count={draft.draft_reminder_count})'
            )
            return 'sent'

        # Send email
        try:
            email_subject, tekstas, html_body = priminimo_laiskas(draft, scenario_code)
            msg = EmailMultiAlternatives(
                subject=email_subject,
                body=tekstas,
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
