"""Motociklų modeliai — į bendrą Model lentelę.

Kaskadai reikia vieno šaltinio: automobilių modeliai jau kabo prie Brand,
motociklų kabojo tik prie senosios MotorcycleBrand. Kopijavimas adityvus —
MotorcycleModel lieka, nes į ją rodo esami skelbimai.
"""
from django.db import migrations


def forwards(apps, schema_editor):
    from django.utils.text import slugify

    Brand = apps.get_model('listings', 'Brand')
    Model = apps.get_model('listings', 'Model')
    MotorcycleModel = apps.get_model('listings', 'MotorcycleModel')

    by_legacy = {b.legacy_moto_id: b.id
                 for b in Brand.objects.filter(legacy_moto__isnull=False)}
    used = {(m.brand_id, m.slug) for m in Model.objects.only('brand_id', 'slug')}
    # Idempotentiškumas: tą patį perkėlimą buvo paleidusi ir management
    # komanda — be šios aibės migracija sukūrė antrą 3726 eilučių kopiją.
    have_names = {(m.brand_id, m.name) for m in Model.objects.only('brand_id', 'name')}

    new = []
    for mm in MotorcycleModel.objects.all():
        brand_id = by_legacy.get(mm.brand_id)
        if brand_id is None or (brand_id, mm.name) in have_names:
            continue
        have_names.add((brand_id, mm.name))
        slug = slugify(mm.name) or f'model-{mm.pk}'
        base, i = slug, 2
        while (brand_id, slug) in used:
            slug = f'{base}-{i}'
            i += 1
        used.add((brand_id, slug))
        new.append(Model(brand_id=brand_id, slug=slug, name=mm.name))
    Model.objects.bulk_create(new, batch_size=1000)


def backwards(apps, schema_editor):
    """Adityvu — atgal nieko netrinam."""


class Migration(migrations.Migration):

    dependencies = [('listings', '0079_seed_advanced_equipment')]

    operations = [migrations.RunPython(forwards, backwards)]
