"""Sėja markes į vieną Brand lentelę su šeimomis (BrandScope).

    python manage.py seed_brands --plan    # tik parodo, nieko nekeičia
    python manage.py seed_brands           # sėja
    python manage.py seed_brands --scope trucks

Idempotentiška. Šaltiniai:
  * apps/listings/management/commands/*-markes.txt — autogidas sąrašai
  * senosios lentelės (MotorcycleBrand, TruckBrand, GearBrand) —
    kad kiekviena esamų skelbimų markė turėtų Brand eilutę ir
    legacy_* nuorodą

RAŠYBA NEKEIČIAMA. Pavadinimai sėjami lygiai tokie, kokie yra
šaltinyje: „SKODA", „Skoda" ir „Škoda" lieka trys atskiros eilutės,
jei tokios yra autogide. Esamos Brand eilutės niekada nepervadinamos.
Ta pati markė kelioms šeimoms sujungiama tik tada, kai pavadinimas
sutampa RAIDĖ Į RAIDĘ (Volvo automobiliuose ir sunkvežimiuose — viena
eilutė su dviem šeimomis).

Vartotojų per „Kita" įvesti pavadinimai čia nesėjami — jie kaupiami
kaip BrandSuggestion ir tvirtinami admin'e.
"""
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify

from apps.listings import brand_registry as reg
from apps.listings.models import (
    Brand, BrandScope, GearBrand, MotorcycleBrand, TruckBrand,
)

CMD_DIR = Path(__file__).resolve().parent

LEGACY_MODELS = {
    'MotorcycleBrand': MotorcycleBrand,
    'TruckBrand': TruckBrand,
    'GearBrand': GearBrand,
}

# „Kita" nėra markė — tai laisvo teksto išeitis. Autogide ji irgi
# rodoma atskirai, sąrašo apačioje.
SKIP_NAMES = {'kita', 'kita marke', 'kita markė', '--------', ''}


def collect():
    """Grąžina {scope_key: {pavadinimas: šaltinių_kiekis}} ir žurnalą."""
    data = {}
    log = []

    def add(scope_key, name):
        name = (name or '').strip()
        if not name or name.lower() in SKIP_NAMES:
            return False
        bucket = data.setdefault(scope_key, {})
        bucket[name] = bucket.get(name, 0) + 1
        return True

    for scope_key, files in reg.SCOPE_SEED_FILES.items():
        for fname in files:
            path = CMD_DIR / fname
            if not path.exists():
                log.append(f'  ! nerastas {fname} ({scope_key})')
                continue
            n = sum(1 for line in path.read_text(encoding='utf-8').splitlines()
                    if add(scope_key, line))
            log.append(f'  {fname:<34} {n:>4} → {scope_key}')

    for scope_key, model_name in reg.SCOPE_LEGACY_MODEL.items():
        n = sum(1 for name in LEGACY_MODELS[model_name].objects
                .values_list('name', flat=True) if add(scope_key, name))
        log.append(f'  {model_name + " (DB)":<34} {n:>4} → {scope_key}')

    n = sum(1 for name in Brand.objects.values_list('name', flat=True)
            if add('cars', name))
    log.append(f'  {"Brand (DB, automobiliai)":<34} {n:>4} → cars')
    return data, log


class Command(BaseCommand):
    help = 'Sėja markes į Brand su šeimomis (BrandScope)'

    def add_arguments(self, parser):
        parser.add_argument('--plan', action='store_true',
                            help='Tik parodo, ką darytų; nieko nekeičia')
        parser.add_argument('--scope', default='',
                            help='Tik viena šeima')

    def handle(self, *args, **options):
        data, log = collect()
        if options['scope']:
            data = {k: v for k, v in data.items() if k == options['scope']}

        self.stdout.write(self.style.MIGRATE_HEADING('Šaltiniai:'))
        for line in log:
            self.stdout.write(line)

        self.stdout.write(self.style.MIGRATE_HEADING('\nŠeimos:'))
        total = 0
        for scope_key, _name, _hm, _o in reg.SCOPES:
            if scope_key not in data:
                continue
            n = len(data[scope_key])
            total += n
            self.stdout.write(f'  {scope_key:<14} {n:>4} markių')

        all_names = set()
        for bucket in data.values():
            all_names |= set(bucket)
        existing = set(Brand.objects.values_list('name', flat=True))
        self.stdout.write(
            f'  {"IŠ VISO eilučių":<14} {len(all_names):>4} '
            f'(šeimų sumoje {total}; skirtumą duoda ta pati markė keliose '
            f'šeimose)')
        self.stdout.write(f'  {"naujų":<14} {len(all_names - existing):>4}')

        if options['plan']:
            self.stdout.write(self.style.WARNING('\n--plan: nieko nekeista'))
            return

        self._seed(data)

    @transaction.atomic
    def _seed(self, data):
        scopes = {}
        for key, name, has_models, order in reg.SCOPES:
            obj, _ = BrandScope.objects.update_or_create(
                key=key,
                defaults={'name': name, 'has_models': has_models, 'order': order},
            )
            scopes[key] = obj

        by_name = {b.name: b for b in Brand.objects.all()}
        used_slugs = set(Brand.objects.values_list('slug', flat=True))

        created = 0
        for scope_key, bucket in data.items():
            scope = scopes.get(scope_key)
            if scope is None:
                continue
            for name in bucket:
                brand = by_name.get(name)
                if brand is None:
                    slug = slugify(name) or 'brand'
                    base, i = slug, 2
                    while slug in used_slugs:
                        slug = f'{base}-{i}'
                        i += 1
                    used_slugs.add(slug)
                    brand = Brand.objects.create(name=name, slug=slug)
                    by_name[name] = brand
                    created += 1
                brand.scopes.add(scope)

        mirrored = self._mirror_to_legacy(by_name)
        linked = self._link_legacy(by_name)
        if mirrored:
            self.stdout.write(self.style.SUCCESS(
                f'Senosiose lentelėse sukurta {mirrored} trūkstamų eilučių '
                f'(kad FK paviršiai rodytų visą šeimą)'))
        self.stdout.write(self.style.SUCCESS(
            f'\nSukurta {created} naujų Brand eilučių, iš viso '
            f'{Brand.objects.count()}. Susieta su senosiomis lentelėmis: {linked}'))


    def _mirror_to_legacy(self, by_name):
        """Šeimos markės, kurių dar nėra senojoje lentelėje, sukuriamos ten.

        Kol skelbimai rodo į MotorcycleBrand / TruckBrand / GearBrand,
        tų lentelių sąrašas yra tai, ką mato create forma ir filtrai.
        Be šio žingsnio sunkvežimių šeima turėtų 301 markę, o forma
        rodytų 97 — t. y. du skirtingi sąrašai, kurių kaip tik ir
        atsisakom. Antrame etape FK persuksim į Brand ir šios lentelės
        nebereikės.
        """
        created = 0
        for scope_key, model_name in reg.SCOPE_LEGACY_MODEL.items():
            model = LEGACY_MODELS[model_name]
            existing = {(r.name or '').strip() for r in model.objects.all()}
            used_slugs = set(model.objects.values_list('slug', flat=True))
            for brand in Brand.objects.filter(scopes__key=scope_key):
                if brand.name in existing:
                    continue
                slug = slugify(brand.name) or 'brand'
                base, i = slug, 2
                while slug in used_slugs:
                    slug = f'{base}-{i}'
                    i += 1
                used_slugs.add(slug)
                model.objects.create(name=brand.name, slug=slug)
                existing.add(brand.name)
                created += 1
        return created

    def _link_legacy(self, by_name):
        """Brand → senoji eilutė pagal tikslų pavadinimą."""
        linked = 0
        field_by_model = {
            'MotorcycleBrand': 'legacy_moto',
            'TruckBrand': 'legacy_truck',
            'GearBrand': 'legacy_gear',
        }
        for model_name, field in field_by_model.items():
            for row in LEGACY_MODELS[model_name].objects.all():
                brand = by_name.get((row.name or '').strip())
                if brand is None or getattr(brand, f'{field}_id') == row.id:
                    continue
                if Brand.objects.filter(**{f'{field}_id': row.id}).exclude(pk=brand.pk).exists():
                    continue
                setattr(brand, field, row)
                brand.save(update_fields=[field])
                linked += 1
        return linked
