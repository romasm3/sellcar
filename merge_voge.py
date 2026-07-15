"""
Sulieja dublikuotus brandus (pvz. VOGE x2) i viena.
Paleisti: python manage.py shell < merge_voge.py
Saugu leisti kelis kartus.
"""
from django.utils.text import slugify
from apps.listings.models import MotorcycleBrand, MotorcycleModel, Listing
from django.db.models import Count

# Rasti VISUS dubliuotus brandus (ne tik VOGE)
dups = (MotorcycleBrand.objects
        .values('name')
        .annotate(c=Count('id'))
        .filter(c__gt=1))

if not dups:
    print('Dublikatu nera.')

for d in dups:
    name = d['name']
    brands = list(MotorcycleBrand.objects.filter(name=name).order_by('id'))
    keep = brands[0]
    print(f'\n=== {name} === paliekam id={keep.id}, suliejam {len(brands)-1} dublikata(-us)')

    for dup in brands[1:]:
        # 1) Perkelti skelbimus i 'keep'
        moved = Listing.objects.filter(motorcycle_brand=dup).update(motorcycle_brand=keep)
        print(f'  skelbimu perkelta: {moved}')

        # 2) Perkelti modelius (vengiant name/slug konfliktu)
        for m in list(dup.models.all()):
            if MotorcycleModel.objects.filter(brand=keep, name=m.name).exists():
                m.delete()  # toks modelis jau yra 'keep' brande
                continue
            base = m.slug or slugify(m.name) or 'model'
            s, i = base, 2
            while MotorcycleModel.objects.filter(brand=keep, slug=s).exists():
                s = f'{base}-{i}'
                i += 1
            m.slug = s
            m.brand = keep
            m.save()

        dup_id = dup.id
        dup.delete()
        print(f'  istrintas dublikatas id={dup_id}')

print('\nDONE. Patikra:')
left = list(MotorcycleBrand.objects.values('name').annotate(c=Count('id')).filter(c__gt=1))
print('likę dublikatai:', left)