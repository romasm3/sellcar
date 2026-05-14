"""
═══════════════════════════════════════════════════════════════════
DĖK Į: apps/listings/management/commands/sync_email_scenarios.py
═══════════════════════════════════════════════════════════════════

Sinchronizuoja email_settings.py sąrašą su Django DB EmailScenario įrašais.

Naudojimas:
    python manage.py sync_email_scenarios

Kas vyksta:
    - Jei scenarijus yra Python faile, bet DB nėra -> sukuria DB įrašą
    - Jei yra DB, bet nebėra Python faile -> IŠTRINA DB įrašą
    - Atnaujina name/description/category/trigger iš metadata
    - NEKEIČIA is_enabled reikšmės (tavo admin'o toggle nedings)

Paleisk po bet kurio EMAIL_SCENARIOS pakeitimo!
═══════════════════════════════════════════════════════════════════
"""

from django.core.management.base import BaseCommand

from apps.listings.email_settings import EMAIL_SCENARIOS, SCENARIO_METADATA
from apps.listings.models import EmailScenario


class Command(BaseCommand):
    help = 'Synchronize EMAIL_SCENARIOS dict with EmailScenario DB records'

    def add_arguments(self, parser):
        parser.add_argument(
            '--delete-orphans',
            action='store_true',
            help='Delete DB records not present in EMAIL_SCENARIOS',
        )

    def handle(self, *args, **options):
        delete_orphans = options['delete_orphans']

        self.stdout.write(f"\n{'='*60}")
        self.stdout.write("EMAIL SCENARIOS SYNC")
        self.stdout.write(f"{'='*60}")
        self.stdout.write(f"Code-side scenarios: {len(EMAIL_SCENARIOS)}")
        self.stdout.write(f"DB-side scenarios:   {EmailScenario.objects.count()}")
        self.stdout.write(f"{'='*60}\n")

        created = 0
        updated = 0
        deleted = 0

        # 1. Create / update
        for code, _enabled in EMAIL_SCENARIOS.items():
            meta = SCENARIO_METADATA.get(code, {})
            defaults = {
                'name':        meta.get('name', code),
                'description': meta.get('description', ''),
                'category':    meta.get('category', 'Extra'),
                'trigger':     meta.get('trigger', ''),
            }

            obj, was_created = EmailScenario.objects.get_or_create(
                code=code,
                defaults={**defaults, 'is_enabled': True},
            )

            if was_created:
                created += 1
                self.stdout.write(self.style.SUCCESS(f"  + Created: {code}"))
            else:
                # Atnaujinam metadata (bet NE is_enabled - tas yra admin'o teritorija)
                changed = False
                for field, value in defaults.items():
                    if getattr(obj, field) != value:
                        setattr(obj, field, value)
                        changed = True
                if changed:
                    obj.save(update_fields=list(defaults.keys()))
                    updated += 1
                    self.stdout.write(f"  ~ Updated: {code}")

        # 2. Delete orphans (jei yra DB bet nebėra code)
        db_codes = set(EmailScenario.objects.values_list('code', flat=True))
        code_codes = set(EMAIL_SCENARIOS.keys())
        orphans = db_codes - code_codes

        if orphans:
            self.stdout.write(self.style.WARNING(f"\n  Orphans (DB only): {len(orphans)}"))
            for code in orphans:
                self.stdout.write(self.style.WARNING(f"    - {code}"))

            if delete_orphans:
                deleted, _ = EmailScenario.objects.filter(code__in=orphans).delete()
                self.stdout.write(self.style.ERROR(f"  Deleted {deleted} orphans"))
            else:
                self.stdout.write(self.style.WARNING(
                    "  Use --delete-orphans to remove them"
                ))

        self.stdout.write(f"\n{'='*60}")
        self.stdout.write(self.style.SUCCESS(
            f"DONE: +{created} created, ~{updated} updated, -{deleted} deleted"
        ))
        self.stdout.write(f"Total DB scenarios: {EmailScenario.objects.count()}")
        self.stdout.write(f"{'='*60}\n")