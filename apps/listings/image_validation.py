# apps/listings/image_validation.py
# ═══════════════════════════════════════════════════════════
# Bendras įkeliamų nuotraukų validatorius.
#
# Django ImageField tikrina failą TIK per formą. Visi mūsų upload'ai
# kuria įrašus tiesiai iš request.FILES, tad iki šiol į media/ galėjo
# patekti bet koks failas (pvz. .html ar .svg — nginx juos atiduoda
# iš to paties domeno, t.y. stored XSS).
#
# Naudojimas:
#     from .image_validation import validate_images, ImageValidationError
#
#     try:
#         validate_images(request.FILES.getlist('images'))
#     except ImageValidationError as e:
#         return JsonResponse({'success': False, 'error': str(e)}, status=400)
# ═══════════════════════════════════════════════════════════

import os

from django.utils.translation import gettext as _
from PIL import Image

ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp'}

# Pillow formatų pavadinimai, atitinkantys leidžiamus plėtinius.
ALLOWED_IMAGE_FORMATS = {'JPEG', 'PNG', 'WEBP'}

MAX_IMAGE_SIZE = 20 * 1024 * 1024  # 20 MB


class ImageValidationError(Exception):
    """Netinkamas įkeliamas failas. str(e) — žinutė vartotojui (LT)."""


def validate_image(upload):
    """Patikrina vieną failą. Meta ImageValidationError, jei netinka."""
    name = getattr(upload, 'name', '') or _('failas')

    size = getattr(upload, 'size', 0) or 0
    if size > MAX_IMAGE_SIZE:
        raise ImageValidationError(_(
            'Failas „%(name)s“ per didelis (%(size).1f MB). '
            'Maksimalus dydis — 20 MB.'
        ) % {'name': name, 'size': size / (1024 * 1024)})

    ext = os.path.splitext(name)[1].lower()
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise ImageValidationError(_(
            'Netinkamas failo formatas: „%(name)s“. '
            'Leidžiami tik JPG, PNG ir WEBP failai.'
        ) % {'name': name})

    # Turinio patikra — plėtinį lengva pervadinti, tad tikrinam patį failą.
    try:
        upload.seek(0)
        img = Image.open(upload)
        img.verify()
        image_format = img.format
    except ImageValidationError:
        raise
    except Exception:
        raise ImageValidationError(_(
            'Failas „%(name)s“ nėra tinkamas paveikslėlis arba yra sugadintas.'
        ) % {'name': name})
    finally:
        # verify() „suvartoja“ failą — grąžinam poziciją, kad Django
        # galėtų jį išsaugoti.
        try:
            upload.seek(0)
        except Exception:
            pass

    if image_format not in ALLOWED_IMAGE_FORMATS:
        raise ImageValidationError(_(
            'Netinkamas failo formatas: „%(name)s“. '
            'Leidžiami tik JPG, PNG ir WEBP failai.'
        ) % {'name': name})


def validate_images(uploads):
    """Patikrina visus failus. Meta ImageValidationError dėl pirmo netinkamo.

    Tikrinam VISUS prieš įrašant bent vieną, kad nebūtų pusiau
    įkeltų skelbimų.
    """
    for upload in uploads:
        validate_image(upload)


def split_valid_images(uploads):
    """Grąžina (tinkami, klaidų_žinutės) — kai reikia praleisti blogus failus."""
    valid, errors = [], []
    for upload in uploads:
        try:
            validate_image(upload)
        except ImageValidationError as exc:
            errors.append(str(exc))
        else:
            valid.append(upload)
    return valid, errors
