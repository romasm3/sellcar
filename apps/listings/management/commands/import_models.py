import os
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from apps.listings.models import Brand, Model


class Command(BaseCommand):
    help = 'Import models from models.txt file'

    def handle(self, *args, **kwargs):
        txt_path = os.path.join(os.path.dirname(__file__), 'models.txt')
        if not os.path.exists(txt_path):
            self.stdout.write(self.style.ERROR(f'models.txt not found at: {txt_path}'))
            return

        created_models = 0
        skipped_brands = 0
        skipped_models = 0

        with open(txt_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or ':' not in line:
                    continue
                brand_name, _, models_str = line.partition(':')
                brand_name = brand_name.strip()
                brand = Brand.objects.filter(name=brand_name).first()
                if not brand:
                    skipped_brands += 1
                    continue
                for model_name in [m.strip() for m in models_str.split(',') if m.strip()]:
                    if Model.objects.filter(brand=brand, name=model_name).exists():
                        skipped_models += 1
                        continue
                    slug = slugify(model_name) or 'model'
                    base_slug = slug
                    counter = 1
                    while Model.objects.filter(brand=brand, slug=slug).exists():
                        slug = f"{base_slug}-{counter}"
                        counter += 1
                    Model.objects.create(brand=brand, name=model_name, slug=slug)
                    created_models += 1

        self.stdout.write(self.style.SUCCESS(
            f'Done! Models created: {created_models}, skipped brands: {skipped_brands}, skipped models: {skipped_models}'
        ))