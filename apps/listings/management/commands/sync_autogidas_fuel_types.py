from django.core.management.base import BaseCommand
from apps.listings.models import FuelType, Listing


class Command(BaseCommand):
    help = "Syncs FuelType list to autogidas.lt exact list (English names)."

    AUTOGIDAS_FUEL_TYPES = [
        ('Diesel',                      ['Dyzelinas', 'diesel']),
        ('Petrol',                      ['Benzinas', 'gasoline', 'petrol']),
        ('Petrol / LPG',                ['Benzinas/Dujos']),
        ('Petrol / Electric (Hybrid)',  ['Benzinas/Elektra', 'hybrid']),
        ('Petrol / Electric (Plug-in)', ['Benzinas/Elektra (Plug-in)']),
        ('Petrol / Electric / LPG',     ['Benzinas/Elektra/Dujos']),
        ('Electric',                    ['Elektra', 'electric']),
        ('Diesel / Electric (Hybrid)',  ['Dyzelinas/Elektra']),
        ('Diesel / Electric (Plug-in)', ['Dyzelinas/Elektra (Plug-in)']),
        ('LPG',                         ['Dujos', 'lpg']),
        ('Petrol / CNG',                ['Benzinas/Gamtinės dujos', 'cng']),
        ('Ethanol',                     ['Etanolis', 'ethanol']),
        ('Other',                       ['Kitas', 'other']),
    ]

    def handle(self, *args, **options):
        # ─── 1. Map old → new ───
        new_by_name = {}
        for new_name, _aliases in self.AUTOGIDAS_FUEL_TYPES:
            ft, created = FuelType.objects.get_or_create(name=new_name)
            new_by_name[new_name] = ft
            tag = '✓ Created' if created else '↻ Exists'
            self.stdout.write(f"  {tag}: {ft.name} (id={ft.id})")

        # ─── 2. Migrate existing Listings from old aliases → new ───
        migrated = 0
        for new_name, aliases in self.AUTOGIDAS_FUEL_TYPES:
            new_ft = new_by_name[new_name]
            for alias in aliases:
                old_qs = FuelType.objects.filter(name__iexact=alias).exclude(pk=new_ft.pk)
                for old_ft in old_qs:
                    cnt = Listing.objects.filter(fuel_type=old_ft).update(fuel_type=new_ft)
                    if cnt:
                        self.stdout.write(f"    → Migrated {cnt} listings: '{old_ft.name}' → '{new_name}'")
                        migrated += cnt
                    old_ft.delete()
                    self.stdout.write(f"    ✗ Deleted old: '{old_ft.name}'")

        # ─── 3. Delete any other leftover FuelTypes not in the list ───
        valid_names = {n for n, _ in self.AUTOGIDAS_FUEL_TYPES}
        leftover = FuelType.objects.exclude(name__in=valid_names)
        for ft in leftover:
            cnt = Listing.objects.filter(fuel_type=ft).count()
            if cnt:
                self.stdout.write(self.style.WARNING(
                    f"  ⚠ Skipping '{ft.name}' — has {cnt} listings still linked"
                ))
                continue
            ft.delete()
            self.stdout.write(f"    ✗ Deleted unused: '{ft.name}'")

        self.stdout.write(self.style.SUCCESS(f"\nDone. Migrated {migrated} listings."))