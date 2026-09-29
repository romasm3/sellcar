# -*- coding: utf-8 -*-
"""
„REDAGUOTI" NUORODOS SKELBIMŲ SĄRAŠE — VISADA /<id>/edit/.

Klaida: /dashboard/announcements/?status=inactive juodraščių „Redaguoti"
vedė į /create/trucks/ ar /create/ BE ID (tuščia forma), motociklų — į
/create/motorcycle/?draft_id=. Listing.get_edit_url() juodraščiams
grąžindavo kūrimo adresus.

Tikrinam TIKRĄ HTML:
  • neaktyvaus (expired — rodomas „Neaktyvus") ir juodraščio (draft) sunkiasvorio, taip pat
    motociklo juodraščio „Redaguoti" = /<id>/edit/
  • sąrašo kortelėse nėra nė vienos /create/ nuorodos su skelbimo ID
    ar be jo (išskyrus mygtuką „Naujas skelbimas")
  • /<id>/edit/ (→ sunkiasvorių forma) išvestame HTML yra ABIEJŲ
    nuotraukų media adresai ir jų id (trynimui)
  • skelbimo puslapyje savininkas mato „Aktyvuoti" → /listings/<id>/select-plan/

Paleidimas (TIK su laikina sqlite baze, ne produkcijoje):
    PATIKRA_DB=<laikinas failas> python docs/redagavimo_nuorodu_test.py
Nuotraukos rašomos į laikiną MEDIA_ROOT, ne į media/.
"""
import os
import sys
import tempfile

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sqlite_settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'patikra'))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

import io                                            # noqa: E402
import re                                            # noqa: E402
from decimal import Decimal                          # noqa: E402

from django.core.files.base import ContentFile       # noqa: E402
from django.test import Client, override_settings    # noqa: E402
from django.test.utils import setup_test_environment  # noqa: E402
from PIL import Image                                # noqa: E402

import formu_seed                                    # noqa: E402
from apps.listings.models import (Listing, ListingImage,  # noqa: E402
                                  SubCategory, VehicleType)

MEDIA = tempfile.mkdtemp(prefix='redagavimo_media_')

gerai = blogai = 0


def tikrink(salyga, tekstas, papildomai=''):
    global gerai, blogai
    if salyga:
        gerai += 1
        print(f'  OK   {tekstas}')
    else:
        blogai += 1
        print(f'  BLOGAI {tekstas}' + (f'\n         {papildomai}' if papildomai else ''))


def jpeg(spalva):
    b = io.BytesIO()
    Image.new('RGB', (64, 48), spalva).save(b, 'JPEG')
    return ContentFile(b.getvalue())


def skelbimas(u, vt_slug, sub_slug, pav, statusas):
    vt, _ = VehicleType.objects.get_or_create(slug=vt_slug,
                                              defaults={'name': vt_slug.title()})
    sub, _ = SubCategory.objects.get_or_create(vehicle_type=vt, slug=sub_slug,
                                               defaults={'name': sub_slug})
    l = Listing.objects.filter(seller=u, title=pav).first() or Listing(seller=u, title=pav)
    l.vehicle_type, l.subcategory, l.status = vt, sub, statusas
    l.year, l.mileage, l.price = 2018, 250000, Decimal('25000')
    l.city, l.country = 'Vilnius', 'LT'
    l.save()
    return l


def main():
    setup_test_environment()
    u = formu_seed.vartotojas()

    sunkus = skelbimas(u, 'trucks', 'trucks', 'Patikra redaguoti neaktyvus sunkvežimis', 'expired')
    sunkus.images.all().delete()
    for i, spalva in enumerate(('red', 'blue')):
        img = ListingImage(listing=sunkus, is_main=(i == 0), order=i)
        img.image.save(f'patikra_redag_{i}.jpg', jpeg(spalva), save=False)
        img.save()
    nuotraukos = list(sunkus.images.order_by('order'))

    juodrastis = skelbimas(u, 'trucks', 'trucks', 'Patikra redaguoti juodraštis sunkvežimis', 'draft')
    moto = skelbimas(u, 'motorcycles', 'motorcycles', 'Patikra redaguoti moto juodraštis', 'draft')

    c = Client()
    c.force_login(u)

    print('\n— /dashboard/announcements/?status=inactive')
    a = c.get('/dashboard/announcements/?status=inactive', follow=True)
    html = a.content.decode('utf-8', 'replace')
    tikrink(a.status_code == 200, f'200 (gauta {a.status_code})')
    for l, pav in ((sunkus, 'neaktyvus sunkiasvoris'), (juodrastis, 'sunkiasvorio juodraštis'),
                   (moto, 'motociklo juodraštis')):
        tikrink(f'href="/{l.pk}/edit/"' in html,
                f'{pav} #{l.pk}: „Redaguoti" → /{l.pk}/edit/')
    # Vienintelė leistina /create/ nuoroda — „Naujas skelbimas" (be parametrų)
    kurimo = sorted(set(re.findall(r'href="(/create/[^"]*)"', html)) - {'/create/'})
    tikrink(not kurimo, 'kortelėse nėra /create/* redagavimo nuorodų', f'rasta {kurimo}')
    tikrink('draft_id=' not in html, 'nėra ?draft_id= nuorodų')

    print(f'\n— /{sunkus.pk}/edit/ (tikras HTML)')
    a = c.get(f'/{sunkus.pk}/edit/', follow=True)
    html = a.content.decode('utf-8', 'replace')
    tikrink(a.status_code == 200, f'200 (gauta {a.status_code}, '
            f'kelias {a.redirect_chain[-1][0] if a.redirect_chain else "-"})')
    for n in nuotraukos:
        tikrink(n.image.url in html, f'nuotrauka {n.image.url} yra')
        tikrink(re.search(rf'data-id="{n.pk}"|mpDelete\({n.pk}\)|'
                          rf'data-existing-img-id="{n.pk}"', html) is not None,
                f'   nuotraukos id {n.pk} yra (trynimui)')
    tikrink(re.search(r'class="[^"]*delete[^"]*"|mpDelete\(', html) is not None,
            'yra trynimo mygtukai')

    print(f'\n— /{juodrastis.pk}/edit/ neveda į tuščią kūrimo formą')
    a = c.get(f'/{juodrastis.pk}/edit/', follow=True)
    galas = a.redirect_chain[-1][0] if a.redirect_chain else ''
    tikrink(a.status_code == 200 and str(juodrastis.pk) in galas,
            f'juodraštis atidaromas su ID ({galas})')

    print('\n— Kitas žingsnis po išsaugojimo: „Aktyvuoti"')
    for l in (sunkus, juodrastis):
        html = c.get(f'/{l.pk}/', follow=True).content.decode('utf-8', 'replace')
        tikrink(f'href="/listings/{l.pk}/select-plan/"' in html and 'data-aktyvuoti' in html,
                f'#{l.pk} ({l.status}) puslapyje yra „Aktyvuoti" → select-plan')
    tikrink(Listing(pk=sunkus.pk, status='draft').get_edit_url() == f'/{sunkus.pk}/edit/',
            'get_edit_url() juodraščiui = /<id>/edit/')

    print(f'\n════ {gerai} gerai / {blogai} blogai ════')
    return 1 if blogai else 0


if __name__ == '__main__':
    with override_settings(MEDIA_ROOT=MEDIA):
        kodas = main()
    sys.exit(kodas)
