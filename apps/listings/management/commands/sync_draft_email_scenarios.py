"""
Create EmailScenario DB records for draft reminder emails.

Usage: python manage.py sync_draft_email_scenarios
"""
from django.core.management.base import BaseCommand
from apps.listings.models import EmailScenario


SCENARIOS = [
    {
        'code': 'draft_reminder_first',
        'name': 'Draft - First reminder (1h after creation)',
        'description': 'Sent 1 hour after a draft listing is created, reminding the seller to complete and activate it.',
        'category': 'Seller',
        'trigger': 'Cron: 1 hour after draft creation',
    },
    {
        # Savo šablono NETURI ir jam nereikia: send_draft_reminders renderina
        # bendrą 'emails/draft_reminder_daily.html', o temą nurodo kode.
        # Per send_scenario šis kodas nesiunčiamas (jo nėra EMAIL_SCENARIOS).
        'code': 'draft_reminder_24h',
        'name': 'Draft - 24h reminder',
        'description': 'Sent 24 hours after draft creation if still not activated.',
        'category': 'Seller',
        'trigger': 'Cron: 24 hours after draft creation',
    },
    {
        'code': 'draft_reminder_daily',
        'name': 'Draft - Daily reminder (after 24h)',
        'description': 'Sent daily after the 24h mark until the draft is activated or deleted.',
        'category': 'Seller',
        'trigger': 'Cron: Daily while status=draft',
    },
]


class Command(BaseCommand):
    help = 'Create/update EmailScenario records for draft reminder emails'

    def handle(self, *args, **options):
        created = 0
        updated = 0

        for scenario in SCENARIOS:
            obj, was_created = EmailScenario.objects.get_or_create(
                code=scenario['code'],
                defaults={
                    'name': scenario['name'],
                    'description': scenario['description'],
                    'category': scenario['category'],
                    'trigger': scenario['trigger'],
                    'is_enabled': True,
                }
            )
            if was_created:
                created += 1
                self.stdout.write(self.style.SUCCESS(
                    f"Created: {scenario['code']}"
                ))
            else:
                obj.name = scenario['name']
                obj.description = scenario['description']
                obj.trigger = scenario['trigger']
                obj.save(update_fields=['name', 'description', 'trigger'])
                updated += 1
                self.stdout.write(
                    f"Updated: {scenario['code']}"
                )

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(
            f'Done! Created: {created}, Updated: {updated}'
        ))