"""MotorcycleModel eilutes nukopijuoja į Model prie suvienodinto Brand.

NENAUDOTI kartu su 0080 migracija — perkėlimą daro migracija. Ši komanda
palikta tik patikrinimui (`--plan`) ir naujoms aplinkoms, kur migracija
jau pritaikyta be duomenų. 2026-08-20 abu buvo paleisti vienu metu ir
davė 3732 dublikatus.

    python manage.py unify_models --plan
    python manage.py unify_models

Kaskadai reikia VIENO modelių šaltinio. Automobilių modeliai jau kabo
prie Brand (Model.brand), o motociklų — prie senosios MotorcycleBrand.
Du šaltiniai reikštų dvi kaskados šakas ir tą pačią klaidą, kurios
atsikratėm su markėmis.

Kopijavimas ADITYVUS: MotorcycleModel lentelė lieka nepaliesta, nes į ją
rodo esami skelbimai. Trinama nieko.
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify

from apps.listings.models import Brand, Model, MotorcycleModel


class Command(BaseCommand):
    help = 'Motociklų modeliai → Model prie suvienodinto Brand'

    def add_arguments(self, parser):
        parser.add_argument('--plan', action='store_true',
                            help='Tik parodo, nieko nekuria')

    def handle(self, *args, **options):
        # Brand → senoji moto markė
        by_legacy = {
            b.legacy_moto_id: b
            for b in Brand.objects.filter(legacy_moto__isnull=False)
        }
        rows = list(MotorcycleModel.objects.select_related('brand'))
        existing = {
            (m.brand_id, m.slug) for m in Model.objects.only('brand_id', 'slug')
        }
        # Sutapimas tikrinamas pagal PAVADINIMĄ, ne slug'ą. Anksčiau
        # esamam pavadinimui buvo generuojamas slug-2 ir kuriamas antras
        # įrašas — būtent taip atsirado 3732 dublikatai.
        have_names = {
            (m.brand_id, m.name) for m in Model.objects.only('brand_id', 'name')
        }

        planned, orphans, dupes = [], [], 0
        used = set(existing)
        for mm in rows:
            brand = by_legacy.get(mm.brand_id)
            if brand is None:
                orphans.append(mm.brand.name if mm.brand else '?')
                continue
            if (brand.id, mm.name) in have_names:
                dupes += 1
                continue
            have_names.add((brand.id, mm.name))
            slug = slugify(mm.name) or f'model-{mm.pk}'
            base, i = slug, 2
            while (brand.id, slug) in used:
                if any(p[0] == brand.id and p[2] == mm.name for p in planned):
                    break
                slug = f'{base}-{i}'
                i += 1
            if (brand.id, slug) in used:
                dupes += 1
                continue
            used.add((brand.id, slug))
            planned.append((brand.id, slug, mm.name))

        self.stdout.write(f'  MotorcycleModel eilučių:      {len(rows)}')
        self.stdout.write(f'  susietų su Brand:             {len(rows) - len(orphans)}')
        self.stdout.write(f'  jau yra Model lentelėje:      {dupes}')
        self.stdout.write(f'  bus sukurta:                  {len(planned)}')
        if orphans:
            self.stdout.write(self.style.WARNING(
                f'  be Brand atitikmens:          {len(orphans)} '
                f'({", ".join(sorted(set(orphans))[:5])}…)'))

        if options['plan']:
            self.stdout.write(self.style.WARNING('\n--plan: nieko nekurta'))
            return

        with transaction.atomic():
            Model.objects.bulk_create(
                [Model(brand_id=b, slug=s, name=n) for b, s, n in planned],
                batch_size=1000,
            )
        self.stdout.write(self.style.SUCCESS(
            f'\nSukurta {len(planned)} Model eilučių; MotorcycleModel nepaliesta '
            f'({MotorcycleModel.objects.count()} eilučių).'))
