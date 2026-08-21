"""Nuotraukų perdirbimas — vienas šaltinis įkėlimui ir esamiems failams.

KODĖL: 2026-08-21 matavimas parodė, kad pagrindinis puslapis atsiunčia
9,7 MB nuotraukų, o rezultatų — 13,8 MB; dvi didžiausios (4,1 ir 3,3 MB)
yra originalūs telefono failai. Rezultatų puslapio LCP dėl to buvo 17,2 s.

KĄ DAROM: iš kiekvieno originalo pasigaminam keturias išvestines —
1600 px ir 668 px, kiekviena WebP ir JPEG. ORIGINALAS LIEKA nepaliestas
`image` lauke: jis reikalingas ir kaip atsarga, ir jei kada prireiks
kitokių dydžių.

KUR NAUDOJAMA:
  * įkeliant — ListingImage.save() (žr. models.py), todėl problema
    negrįžta su naujais skelbimais;
  * esamiems — `manage.py optimize_images`.
"""

import io
import os

from django.core.files.base import ContentFile

# (priesaga, ilgoji kraštinė) — 668 px riba paimta iš etalono mobilaus
# vaizdo (max-width: 668px atskiras failas).
SPECS = (('lg', 1600), ('sm', 668))
JPEG_QUALITY = 82
WEBP_QUALITY = 78


def _open_fixed(fp):
    """Atidaro ir pasuka pagal EXIF (telefonų nuotraukos be to gula šonu)."""
    from PIL import Image, ImageOps
    im = Image.open(fp)
    im = ImageOps.exif_transpose(im)
    if im.mode in ('P', 'LA'):
        im = im.convert('RGBA')
    return im


def _resized(im, longest):
    w, h = im.size
    scale = min(1.0, float(longest) / max(w, h))
    if scale >= 1.0:
        return im.copy()
    from PIL import Image
    return im.resize((max(1, round(w * scale)), max(1, round(h * scale))),
                     Image.LANCZOS)


def _encode(im, fmt):
    buf = io.BytesIO()
    if fmt == 'jpeg':
        rgb = im.convert('RGB')
        rgb.save(buf, 'JPEG', quality=JPEG_QUALITY, optimize=True, progressive=True)
    else:
        im.save(buf, 'WEBP', quality=WEBP_QUALITY, method=4)
    return buf.getvalue()


def build_derivatives(obj, force=False, save=True):
    """Sugeneruoja obj.image_{lg,sm}{,_webp} ir įsimena lg matmenis.

    Grąžina True, jei kas nors buvo perdaryta.
    """
    if not obj.image:
        return False
    if not force and obj.image_lg and obj.image_lg_webp and obj.w_lg:
        return False

    try:
        obj.image.open('rb')
        src = _open_fixed(obj.image)
    except Exception:
        return False

    base = os.path.splitext(os.path.basename(obj.image.name))[0][:60]
    changed = False

    for suffix, longest in SPECS:
        im = _resized(src, longest)
        if suffix == 'lg':
            obj.w_lg, obj.h_lg = im.size
        for fmt, ext in (('jpeg', 'jpg'), ('webp', 'webp')):
            field = f'image_{suffix}' + ('_webp' if fmt == 'webp' else '')
            data = _encode(im, fmt)
            getattr(obj, field).save(f'{base}-{suffix}.{ext}',
                                     ContentFile(data), save=False)
            changed = True

    if changed and save:
        obj.save(update_fields=['image_lg', 'image_lg_webp', 'image_sm',
                                'image_sm_webp', 'w_lg', 'h_lg'])
    return changed
