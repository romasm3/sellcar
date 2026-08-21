"""Esamų nuotraukų perdirbimas į rodomas versijas.

    manage.py optimize_images            # tik tos, kurios dar neturi
    manage.py optimize_images --force    # perdaro visas
    manage.py optimize_images --limit 20

Originalai NETRINAMI — jie lieka `image` lauke ir media/listings/ kataloge.
Perdirbimo logika viena, ta pati kaip įkeliant: apps/listings/imaging.py.
"""

from django.core.management.base import BaseCommand

from apps.listings.imaging import build_derivatives
from apps.listings.models import ListingImage


class Command(BaseCommand):
    help = 'Sugeneruoja nuotraukų 1600/668 px WebP ir JPEG versijas.'

    def add_arguments(self, parser):
        parser.add_argument('--force', action='store_true')
        parser.add_argument('--limit', type=int, default=0)

    def handle(self, *args, **o):
        qs = ListingImage.objects.all().order_by('id')
        if not o['force']:
            from django.db.models import Q
            qs = qs.filter(Q(image_lg='') | Q(image_lg__isnull=True))
        if o['limit']:
            qs = qs[:o['limit']]

        done = failed = 0
        before = after = 0
        for img in qs:
            try:
                src = img.image.size
            except Exception:
                src = 0
            ok = build_derivatives(img, force=o['force'])
            if ok:
                done += 1
                before += src
                try:
                    after += img.image_lg.size
                except Exception:
                    pass
            else:
                failed += 1
            if (done + failed) % 10 == 0:
                self.stdout.write(f'  … {done + failed}')

        mb = lambda b: b / 1024 / 1024
        self.stdout.write(self.style.SUCCESS(
            f'Perdirbta: {done}, praleista/nepavyko: {failed}. '
            f'Originalai {mb(before):.1f} MB → rodomos {mb(after):.1f} MB '
            f'({(1 - after / before) * 100:.0f}% mažiau)' if before else
            f'Perdirbta: {done}, praleista: {failed}'))
