# -*- coding: utf-8 -*-
"""
Prikabina nuotraukas prie skelbimo iš URL.

    python manage.py prikabink_nuotraukas <listing_id> --url <URL> [--url ...]
    python manage.py prikabink_nuotraukas 935 --url https://... --dry-run

Kam: dalių skelbimams, kurių nuotraukos jau yra kitur (Ovoko ir pan.).

Kelias TAS PATS kaip formos įkėlimas: ListingImage(image=...) — tas pats
ImageField ir upload_to, ListingImage.save() pagamina miniatiūras
(imaging.build_derivatives), patikra — image_validation.validate_image
(ta pati 20 MB riba ir formatai).

  • parsisiunčia; Content-Type turi būti image/*, dydis < 20 MB —
    kitaip URL praleidžiamas (komanda nekrenta, tęsia su kitais);
  • dublikatai pagal SHA-256 — ir tarp esamų skelbimo nuotraukų, ir
    tarp tame pačiame paleidime duotų URL. DĖMESIO: tas pats vaizdas
    kita raiška ar suspaudimu turi kitą SHA-256 ir dublikatu nelaikomas;
  • tvarka — kaip --url eilė, po esamų; pirma nauja tampa pagrindine,
    jei skelbimas pagrindinės dar neturi (arba su --pagrindine);
  • --dry-run — parsisiunčia ir patikrina, bet į DB ir diską nerašo.
"""
import hashlib
import os
import urllib.request
from urllib.parse import urlparse

from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Max

from apps.listings.image_validation import MAX_IMAGE_SIZE, ImageValidationError, validate_image
from apps.listings.models import Listing, ListingImage

USER_AGENT = 'AutoLeft/1.0 (+https://autoleft.com; photo import)'   # tik ASCII — HTTP antraštė
LAUKIMAS = 30


def sha256(duomenys):
    return hashlib.sha256(duomenys).hexdigest()


def parsisiusk(url):
    """(baitai, content_type) arba keliama ValueError su priežastimi."""
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    with urllib.request.urlopen(req, timeout=LAUKIMAS) as atsakymas:
        tipas = (atsakymas.headers.get('Content-Type') or '').split(';')[0].strip().lower()
        if not tipas.startswith('image/'):
            raise ValueError(f'ne paveikslėlis (Content-Type: {tipas or "nėra"})')
        ilgis = atsakymas.headers.get('Content-Length')
        if ilgis and ilgis.isdigit() and int(ilgis) >= MAX_IMAGE_SIZE:
            raise ValueError(f'per didelis ({int(ilgis) / 1048576:.1f} MB)')
        duomenys = atsakymas.read(MAX_IMAGE_SIZE + 1)
        if len(duomenys) >= MAX_IMAGE_SIZE:
            raise ValueError('per didelis (≥ 20 MB)')
        return duomenys, tipas


def failo_vardas(url, tipas, eile):
    vardas = os.path.basename(urlparse(url).path) or f'nuotrauka-{eile}'
    if '.' not in vardas:
        vardas += '.' + (tipas.split('/')[-1] or 'jpg')
    return vardas[-100:]


class Command(BaseCommand):
    help = 'Prikabina nuotraukas prie skelbimo iš URL (tas pats kelias kaip formos įkėlimas).'

    def add_arguments(self, parser):
        parser.add_argument('listing_id', type=int)
        parser.add_argument('--url', action='append', default=[], required=True,
                            help='Nuotraukos URL (galima kartoti; tvarka išlaikoma)')
        parser.add_argument('--dry-run', action='store_true',
                            help='Parsisiųsti ir patikrinti, bet nieko nerašyti')
        parser.add_argument('--pagrindine', action='store_true',
                            help='Pirma nauja nuotrauka tampa pagrindine net jei pagrindinė jau yra')

    def handle(self, *args, listing_id, url, dry_run, pagrindine, **kwargs):
        listing = Listing.objects.filter(pk=listing_id).first()
        if listing is None:
            raise CommandError(f'Skelbimo #{listing_id} nėra')

        esamos = list(listing.images.all())
        maisos = set()
        for img in esamos:
            try:
                with img.image.open('rb') as f:
                    maisos.add(sha256(f.read()))
            except Exception:                          # failo nėra diske — tęsiam
                pass
        eile = (listing.images.aggregate(m=Max('order'))['m'] or -1) + 1
        reikia_pagrindines = pagrindine or not any(i.is_main for i in esamos)

        prefiksas = '[DRY RUN] ' if dry_run else ''
        self.stdout.write(f'{prefiksas}#{listing.pk} „{listing.title}": esamų {len(esamos)}, '
                          f'URL {len(url)}')
        prideta = dublikatu = praleista = 0
        for nr, adresas in enumerate(url, 1):
            try:
                duomenys, tipas = parsisiusk(adresas)
                vardas = failo_vardas(adresas, tipas, nr)
                validate_image(SimpleUploadedFile(vardas, duomenys, content_type=tipas))
            except (ValueError, ImageValidationError, OSError) as klaida:
                praleista += 1
                self.stdout.write(self.style.WARNING(f'  ✗ {nr}. praleista: {klaida} — {adresas}'))
                continue

            maisa = sha256(duomenys)
            if maisa in maisos:
                dublikatu += 1
                self.stdout.write(f'  = {nr}. dublikatas (SHA-256 {maisa[:12]}) — {adresas}')
                continue
            maisos.add(maisa)

            pagr = reikia_pagrindines
            if not dry_run:
                if pagr:
                    listing.images.filter(is_main=True).update(is_main=False)
                img = ListingImage(listing=listing, is_main=pagr, order=eile)
                img.image.save(vardas, ContentFile(duomenys), save=False)
                img.save()                             # → miniatiūros (build_derivatives)
            reikia_pagrindines = False
            eile += 1
            prideta += 1
            self.stdout.write(self.style.SUCCESS(
                f'  ✓ {nr}. {"(pagrindinė) " if pagr else ""}{vardas} '
                f'{len(duomenys) / 1024:.0f} KB'))

        self.stdout.write(f'{prefiksas}Pridėta: {prideta}, dublikatų: {dublikatu}, '
                          f'praleista: {praleista}. Iš viso nuotraukų: '
                          f'{len(esamos) + (0 if dry_run else prideta)}'
                          + (f' (+{prideta} po tikro paleidimo)' if dry_run else ''))
