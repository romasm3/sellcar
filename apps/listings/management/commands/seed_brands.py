"""Sėja markes į vieną Brand lentelę su šeimomis (BrandScope).

    python manage.py seed_brands --plan    # tik parodo, nieko nekeičia
    python manage.py seed_brands           # sėja
    python manage.py seed_brands --scope trucks

Idempotentiška. Šaltiniai:
  * apps/listings/management/commands/*-markes.txt — autogidas sąrašai
  * senosios lentelės (MotorcycleBrand, TruckBrand, GearBrand) —
    kad kiekviena esamų skelbimų markė turėtų Brand eilutę ir
    legacy_* nuorodą

Rašyba: variantai, kurie skiriasi tik registru, diakritikais ar
skyrikliais, jungiami į vieną eilutę. Laimi variantas su diakritikais
(Kässbohrer > Kassbohrer), po to — ne vien didžiosiomis (Kogel >
KOGEL), po to — dažniausiai pasitaikantis.
"""
import unicodedata
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

# Nejungiam, nors normalizavimas juos sulygina — tai skirtingos markės
# (patvirtinta rankomis).
NEVER_MERGE = {
    frozenset({'В-100', '100'}),
    frozenset({'CF', 'C&F'}),
}

# Reikšmės, kurios nėra markės
SKIP_NAMES = {'kita', 'kita marke', 'kita markė', 'other', '--------', ''}


def norm(name):
    """Rašybos raktas: be diakritikų, be skyriklių, mažosiomis."""
    s = unicodedata.normalize('NFKD', name)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = s.replace('ß', 'ss').replace('ł', 'l').replace('Ł', 'L')
    return ''.join(c for c in s.lower() if c.isalnum())


def _diacritics(name):
    return sum(1 for c in name if ord(c) > 127)


def pick_winner(variants):
    """Kuris rašybos variantas lieka. variants: {pavadinimas: kiek kartų}"""
    def key(item):
        name, count = item
        all_caps = name.isupper() and len(name) > 3
        return (
            -_diacritics(name),   # diakritikai laimi
            all_caps,             # ne vien didžiosiomis laimi
            -count,               # dažnesnis laimi
            name,                 # stabilumui
        )
    return sorted(variants.items(), key=key)[0][0]


def collect():
    """Grąžina {scope_key: {norm_key: {raw_name: count}}} ir šaltinių žurnalą."""
    data = {}
    log = []
    for scope_key, files in reg.SCOPE_SEED_FILES.items():
        bucket = data.setdefault(scope_key, {})
        for fname in files:
            path = CMD_DIR / fname
            if not path.exists():
                log.append(f'  ! nerastas {fname} ({scope_key})')
                continue
            n = 0
            for line in path.read_text(encoding='utf-8').splitlines():
                name = line.strip()
                if not name or name.lower() in SKIP_NAMES:
                    continue
                bucket.setdefault(norm(name), {}).setdefault(name, 0)
                bucket[norm(name)][name] += 1
                n += 1
            log.append(f'  {fname:<34} {n:>4} → {scope_key}')

    for scope_key, model_name in reg.SCOPE_LEGACY_MODEL.items():
        bucket = data.setdefault(scope_key, {})
        n = 0
        for name in LEGACY_MODELS[model_name].objects.values_list('name', flat=True):
            name = (name or '').strip()
            if not name or name.lower() in SKIP_NAMES:
                continue
            bucket.setdefault(norm(name), {}).setdefault(name, 0)
            bucket[norm(name)][name] += 1
            n += 1
        log.append(f'  {model_name + " (DB)":<34} {n:>4} → {scope_key}')

    # esamos Brand eilutės (automobiliai) — kad nesukurtume dublikato
    bucket = data.setdefault('cars', {})
    for name in Brand.objects.values_list('name', flat=True):
        name = (name or '').strip()
        if not name or name.lower() in SKIP_NAMES:
            continue
        bucket.setdefault(norm(name), {}).setdefault(name, 0)
        bucket[norm(name)][name] += 1
    log.append(f'  {"Brand (DB, automobiliai)":<34} {Brand.objects.count():>4} → cars')
    return data, log


def merge_groups(data):
    """Visų šeimų rašybos grupės, kuriose daugiau nei vienas variantas."""
    merged = {}
    for scope_key, bucket in data.items():
        for key, variants in bucket.items():
            tgt = merged.setdefault(key, {})
            for name, count in variants.items():
                tgt[name] = tgt.get(name, 0) + count
    groups = []
    for key, variants in merged.items():
        if len(variants) < 2:
            continue
        if frozenset(variants) in NEVER_MERGE:
            continue
        groups.append((key, variants, pick_winner(variants)))
    groups.sort(key=lambda g: pick_winner(g[1]).lower())
    return groups


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

        groups = merge_groups(data)
        self.stdout.write(self.style.MIGRATE_HEADING(
            f'\nRašybos sujungimas: {len(groups)} grupių'))
        for _key, variants, winner in groups:
            losers = ', '.join(sorted(n for n in variants if n != winner))
            self.stdout.write(f'  {winner:<28} ← {losers}')

        # kanoninis pavadinimas kiekvienam normalizuotam raktui
        canon = {}
        for scope_key, bucket in data.items():
            for key, variants in bucket.items():
                canon.setdefault(key, {})
                for name, count in variants.items():
                    canon[key][name] = canon[key].get(name, 0) + count
        canon = {k: pick_winner(v) for k, v in canon.items()}

        self.stdout.write(self.style.MIGRATE_HEADING('\nŠeimos:'))
        total = 0
        for scope_key, _name, _hm, _o in reg.SCOPES:
            if scope_key not in data:
                continue
            n = len(data[scope_key])
            total += n
            self.stdout.write(f'  {scope_key:<14} {n:>4} unikalių markių')
        self.stdout.write(f'  {"IŠ VISO eilučių":<14} {len(canon):>4} '
                          f'(be sujungimo būtų {total})')

        renames = []
        for b in Brand.objects.all():
            want = canon.get(norm(b.name))
            if want and want != b.name:
                renames.append((b.name, want))
        self.stdout.write(self.style.MIGRATE_HEADING(
            f'\nEsamos Brand eilutės, kurios būtų pervadintos: {len(renames)}'))
        for old_name, new_name in sorted(renames):
            self.stdout.write(f'  {old_name:<28} → {new_name}')

        shared = {}
        for scope_key, bucket in data.items():
            for key in bucket:
                shared.setdefault(key, []).append(scope_key)
        multi = sorted(
            (canon[k], v) for k, v in shared.items() if len(v) > 1
        )
        self.stdout.write(self.style.MIGRATE_HEADING(
            f'\nMarkės, priklausančios kelioms šeimoms: {len(multi)}'))
        for name, scope_keys in multi[:15]:
            self.stdout.write(f'  {name:<28} {", ".join(sorted(scope_keys))}')
        if len(multi) > 15:
            self.stdout.write(f'  ... ir dar {len(multi) - 15}')

        if options['plan']:
            self.stdout.write(self.style.WARNING('\n--plan: nieko nekeista'))
            return

        self._seed(data, canon)

    @transaction.atomic
    def _seed(self, data, canon):
        scopes = {}
        for key, name, has_models, order in reg.SCOPES:
            obj, _ = BrandScope.objects.update_or_create(
                key=key,
                defaults={'name': name, 'has_models': has_models, 'order': order},
            )
            scopes[key] = obj

        # esamos Brand eilutės pagal normalizuotą raktą
        by_key = {}
        for b in Brand.objects.all():
            by_key.setdefault(norm(b.name), b)

        created = 0
        for scope_key, bucket in data.items():
            scope = scopes.get(scope_key)
            if scope is None:
                continue
            for key in bucket:
                brand = by_key.get(key)
                if brand is not None and brand.name != canon[key]:
                    brand.name = canon[key]
                    brand.save(update_fields=['name'])
                if brand is None:
                    name = canon[key]
                    slug = slugify(name) or key
                    base, i = slug, 2
                    while Brand.objects.filter(slug=slug).exists():
                        slug = f'{base}-{i}'
                        i += 1
                    brand = Brand.objects.create(name=name, slug=slug)
                    by_key[key] = brand
                    created += 1
                brand.scopes.add(scope)

        linked = self._link_legacy(by_key)

        self.stdout.write(self.style.SUCCESS(
            f'\nSukurta {created} naujų Brand eilučių, iš viso '
            f'{Brand.objects.count()}. Susieta su senosiomis lentelėmis: {linked}'))

    def _link_legacy(self, by_key):
        linked = 0
        field_by_model = {
            'MotorcycleBrand': 'legacy_moto',
            'TruckBrand': 'legacy_truck',
            'GearBrand': 'legacy_gear',
        }
        for model_name, field in field_by_model.items():
            for row in LEGACY_MODELS[model_name].objects.all():
                brand = by_key.get(norm(row.name or ''))
                if brand is None:
                    continue
                if getattr(brand, f'{field}_id') == row.id:
                    continue
                # OneToOne — jei eilutė jau užimta kito Brand, praleidžiam
                if Brand.objects.filter(**{f'{field}_id': row.id}).exclude(pk=brand.pk).exists():
                    continue
                setattr(brand, field, row)
                brand.save(update_fields=[field])
                linked += 1
        return linked
