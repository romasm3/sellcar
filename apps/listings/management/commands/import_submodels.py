import os
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from apps.listings.models import Brand, Model, SubModel


class Command(BaseCommand):
    help = 'Import car submodels from submodels.txt'

    def handle(self, *args, **kwargs):
        txt_path = os.path.join(os.path.dirname(__file__), 'submodels.txt')
        if not os.path.exists(txt_path):
            self.stdout.write(self.style.ERROR(f'submodels.txt not found'))
            return

        with open(txt_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]

        created = skipped = not_found = 0

        for line in lines:
            if '|' not in line or ':' not in line:
                continue
            brand_model, submodels_str = line.split(':', 1)
            brand_name, model_name = brand_model.split('|')
            brand_name = brand_name.strip()
            model_name = model_name.strip()

            try:
                brand = Brand.objects.get(name=brand_name)
                model = Model.objects.get(brand=brand, name=model_name)
            except (Brand.DoesNotExist, Model.DoesNotExist):
                self.stdout.write(self.style.WARNING(f'  Not found: {brand_name} {model_name}'))
                not_found += 1
                continue

            for sub in [s.strip() for s in submodels_str.split(',') if s.strip()]:
                base_slug = slugify(sub) or f'sub-{sub.lower()}'
                slug = base_slug
                counter = 1
                while SubModel.objects.filter(model=model, slug=slug).exists():
                    slug = f'{base_slug}-{counter}'
                    counter += 1

                if SubModel.objects.filter(model=model, name=sub).exists():
                    skipped += 1
                else:
                    SubModel.objects.create(model=model, name=sub, slug=slug)
                    created += 1

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! Created: {created}, Skipped: {skipped}, Not found: {not_found}'
        ))