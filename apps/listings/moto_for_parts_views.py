"""Motociklas dalimis („whole-moto-for-parts").

Tiesioginis car_for_parts_views dvynys — ta pati draft + AJAX nuotraukų
schema, tik automobilio laukų rinkinys pakeistas motociklo.

Laukai imti iš etalono motociklų dalių formos (sec 27): Būklė, Markė,
Modelis, Motociklo tipas, Metai, Darbinis tūris cm³, Kaina. Etalone
„ardomas dalimis" yra varnelė ant paprasto dalies skelbimo; mūsų
projekte tai atskira subkategorija su savo forma, kaip automobiliams
ir sunkvežimiams.
"""
import json
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .image_validation import split_valid_images, ImageValidationError, validate_images
from .models import (
    Listing, ListingImage, VehicleType, SubCategory,
    MotorcycleBrand, MotorcycleModel,
)
from .listing_helpers import (
    _int_or_none,
    _float_or_none,
    parse_common_listing_fields,
    validate_common_fields,
    apply_common_fields_to_listing,
    finalize_listing_publish,
    finalize_listing_edit,
    build_listing_title,
)


MOTO_FOR_PARTS_DRAFT_SESSION_KEY = 'active_moto_for_parts_draft_id'
MOTO_FOR_PARTS_SUBCATEGORY_SLUG = 'whole-moto-for-parts'


# ═══════════════════════════════════════════════════════════
# HELPER funkcijos vidaus naudojimui
# ═══════════════════════════════════════════════════════════

def _get_draft(request):
    """Sesijos draft'as, jei jis JAU yra. Nekuria naujo.

    GET užklausa naujo draft'o nebekuria: anksčiau vien atidarius formą
    DB atsirasdavo „Untitled draft" eilutė, net jei vartotojas nieko
    neįvedė. Eilutė sukuriama tik tada, kai vartotojas ką nors realiai
    padaro — įkelia nuotrauką (AJAX) arba pateikia formą (POST).
    """
    draft_id = request.session.get(MOTO_FOR_PARTS_DRAFT_SESSION_KEY)
    if not draft_id:
        return None
    try:
        return Listing.objects.get(
            pk=draft_id, seller=request.user, status='draft')
    except Listing.DoesNotExist:
        request.session[MOTO_FOR_PARTS_DRAFT_SESSION_KEY] = None
        return None


def _get_or_create_draft(request):
    """Get session draft or create new moto-for-parts draft."""
    draft_id = request.session.get(MOTO_FOR_PARTS_DRAFT_SESSION_KEY)
    if draft_id:
        try:
            return Listing.objects.get(
                pk=draft_id,
                seller=request.user,
                status='draft',
            )
        except Listing.DoesNotExist:
            request.session[MOTO_FOR_PARTS_DRAFT_SESSION_KEY] = None

    parts_vt = VehicleType.objects.filter(slug='parts').first()
    if not parts_vt:
        return None

    sub = SubCategory.objects.filter(
        vehicle_type=parts_vt,
        slug=MOTO_FOR_PARTS_SUBCATEGORY_SLUG,
    ).first()

    draft = Listing.objects.create(
        seller=request.user,
        vehicle_type=parts_vt,
        subcategory=sub,
        title='Untitled draft',
        year=date.today().year,
        mileage=0,
        price=0,
        country='US',
        city='—',
        status='draft',
        condition='',
        defects='none',
    )
    request.session[MOTO_FOR_PARTS_DRAFT_SESSION_KEY] = draft.pk
    request.session.modified = True
    return draft


def _parse_moto_for_parts_specific_fields(request):
    """Parse'ina TIK moto-for-parts SPECIFINIUS laukus iš POST.

    Bendrus (kaina, būklė, kontaktai, komentarai) tvarko
    parse_common_listing_fields().
    """
    return {
        'brand_id': _int_or_none(request.POST.get('motorcycle_brand')),
        'model_id': _int_or_none(request.POST.get('motorcycle_model')),
        'motorcycle_type': request.POST.get('motorcycle_type', '').strip(),
        'engine_capacity_cc': _int_or_none(request.POST.get('engine_capacity_cc')),
        'moto_engine_type': request.POST.get('moto_engine_type', '').strip(),
        'cooling_type': request.POST.get('cooling_type', '').strip(),
        'power': _int_or_none(request.POST.get('power')),
        'mileage': _int_or_none(request.POST.get('mileage_km')),
        'color': request.POST.get('color', '').strip(),
    }


def _apply_moto_for_parts_specific_fields(listing, specific_data):
    """Užpildo moto-for-parts SPECIFINIUS laukus į listing objektą."""
    listing.motorcycle_type = specific_data['motorcycle_type']
    listing.engine_capacity_cc = specific_data['engine_capacity_cc']
    listing.moto_engine_type = specific_data['moto_engine_type']
    listing.cooling_type = specific_data['cooling_type']
    listing.power = specific_data['power']
    listing.color = specific_data['color']
    if specific_data['mileage'] is not None:
        listing.mileage = specific_data['mileage']

    # FK laukai (su safe lookup)
    if specific_data['brand_id']:
        try:
            listing.motorcycle_brand = MotorcycleBrand.objects.get(
                pk=specific_data['brand_id'])
        except MotorcycleBrand.DoesNotExist:
            pass
    if specific_data['model_id']:
        try:
            listing.motorcycle_model = MotorcycleModel.objects.get(
                pk=specific_data['model_id'])
        except MotorcycleModel.DoesNotExist:
            pass


def _build_context(request, draft_or_listing, is_edit_mode=False):
    """Bendras context builder CREATE ir EDIT view'ams."""
    user_phone = ''
    if hasattr(request.user, 'profile') and request.user.profile.phone_number:
        user_phone = request.user.profile.phone_number

    context = {
        'draft': draft_or_listing,
        'brands': MotorcycleBrand.objects.all().order_by('name'),
        'years': list(range(2026, 1949, -1)),
        'condition_choices': Listing.CONDITION_CHOICES,
        'motorcycle_type_choices': Listing.MOTORCYCLE_TYPE_CHOICES,
        'engine_type_choices': Listing.MOTO_ENGINE_TYPE_CHOICES,
        'cooling_choices': Listing.COOLING_TYPE_CHOICES,
        'color_choices': Listing.COLOR_CHOICES,
        # Country/state sąrašai ateina iš contact_block_tags — iš view'o
        # jų NEPERDUODAM (žr. CLAUDE.md).
        'user_phone': user_phone,
    }

    if is_edit_mode:
        context['listing'] = draft_or_listing
        context['is_edit_mode'] = True

    return context


# ═══════════════════════════════════════════════════════════
# CREATE view
# ═══════════════════════════════════════════════════════════

@login_required
def moto_for_parts_create(request):
    """Vieno puslapio forma: 'Whole moto for parts' listings."""

    if request.GET.get('new') == '1' and request.method == 'GET':
        request.session[MOTO_FOR_PARTS_DRAFT_SESSION_KEY] = None
        request.session.modified = True

    resume_id = _int_or_none(request.GET.get('draft'))
    if resume_id:
        try:
            existing = Listing.objects.get(
                pk=resume_id,
                seller=request.user,
                status='draft',
            )
            request.session[MOTO_FOR_PARTS_DRAFT_SESSION_KEY] = existing.pk
            request.session.modified = True
        except Listing.DoesNotExist:
            messages.error(request, 'Draft not found.')
            return redirect('moto_for_parts_create')

    # GET tik atidaro formą — eilutės DB nekuriam (žr. _get_draft).
    draft = _get_draft(request)

    if request.method == 'POST':
        if draft is None:
            draft = _get_or_create_draft(request)
        if not draft:
            messages.error(request, "Parts category not configured.")
            return redirect('listing_list')

        # 1. Parse fields — BENDRUS per helper, SPECIFINIUS atskirai
        common = parse_common_listing_fields(request)
        specific = _parse_moto_for_parts_specific_fields(request)

        # 2. Validate — BENDRUS per helper + SPECIFINIUS rankiniu būdu
        errors = validate_common_fields(common, require_terms=True)
        if not specific['brand_id']:
            errors.append('Brand is required')

        if errors:
            for e in errors:
                messages.error(request, e)
        else:
            # 3. Apply BENDRUS laukus per helper
            apply_common_fields_to_listing(draft, common)

            # 4. Apply SPECIFINIUS laukus
            _apply_moto_for_parts_specific_fields(draft, specific)

            # 5. Build title
            draft.title = build_listing_title(
                brand_name=draft.motorcycle_brand.name if draft.motorcycle_brand else '',
                model_name=draft.motorcycle_model.name if draft.motorcycle_model else '',
                year=draft.year,
                suffix='(for parts)',
            )

            # 6. PUBLISH per helper
            # Atlieka: phone save + coords + save() + activate() + email
            finalize_listing_publish(draft, common['phone'], request.user)

            # 7. Cleanup session
            request.session[MOTO_FOR_PARTS_DRAFT_SESSION_KEY] = None
            request.session.modified = True

            return redirect(
                reverse('listing_success', kwargs={'pk': draft.pk}) + '?action=published'
            )

    context = _build_context(request, draft, is_edit_mode=False)
    return render(request, 'listings/moto_for_parts_create.html', context)


# ═══════════════════════════════════════════════════════════
# EDIT view
# ═══════════════════════════════════════════════════════════

@login_required
def moto_for_parts_edit(request, pk):
    """Vieno puslapio redagavimas: 'Whole moto for parts' listing."""
    listing = get_object_or_404(
        Listing,
        pk=pk,
        seller=request.user,
    )

    # Verify it IS a moto-for-parts listing
    if not listing.subcategory or listing.subcategory.slug != MOTO_FOR_PARTS_SUBCATEGORY_SLUG:
        messages.error(request, "This listing cannot be edited here.")
        return redirect('listing_edit_hub', pk=pk)

    if request.method == 'POST':
        # 1. Parse fields
        common = parse_common_listing_fields(request)
        specific = _parse_moto_for_parts_specific_fields(request)

        # 2. Validate
        errors = validate_common_fields(common)
        if not specific['brand_id']:
            errors.append('Brand is required')

        if errors:
            for e in errors:
                messages.error(request, e)
        else:
            # 3. Apply BENDRUS laukus
            apply_common_fields_to_listing(listing, common)

            # 4. Apply SPECIFINIUS laukus
            _apply_moto_for_parts_specific_fields(listing, specific)

            # 5. Update title
            listing.title = build_listing_title(
                brand_name=listing.motorcycle_brand.name if listing.motorcycle_brand else '',
                model_name=listing.motorcycle_model.name if listing.motorcycle_model else '',
                year=listing.year,
                suffix='(for parts)',
            )

            # 6. EDIT per helper
            # Atlieka: phone save + coords recalc + save()
            finalize_listing_edit(listing, common['phone'], request.user)

            messages.success(request, 'Listing updated successfully.')
            return redirect('listing_detail', pk=listing.pk)

    context = _build_context(request, listing, is_edit_mode=True)
    return render(request, 'listings/moto_for_parts_create.html', context)


# ═══════════════════════════════════════════════════════════
# AJAX endpoints — CREATE (draft images)
# ═══════════════════════════════════════════════════════════

@login_required
@require_POST
def upload_moto_for_parts_image(request):
    """AJAX upload image to draft."""
    # Tikrinam PRIEŠ kurdami draft'ą — tuščia užklausa eilutės DB nepalieka
    images = request.FILES.getlist('images')
    if not images:
        return JsonResponse({'success': False, 'error': 'No images'}, status=400)

    draft = _get_or_create_draft(request)
    if not draft:
        return JsonResponse({'success': False, 'error': 'No draft'}, status=400)

    try:
        validate_images(images)
    except ImageValidationError as exc:
        return JsonResponse({'success': False, 'error': str(exc)}, status=400)

    existing = draft.images.count()
    uploaded = []

    for i, img_file in enumerate(images[:36]):
        try:
            img = ListingImage.objects.create(
                listing=draft,
                image=img_file,
                is_main=(existing == 0 and i == 0),
                order=existing + i,
            )
            uploaded.append({
                'id': img.pk,
                'url': img.image.url,
                'is_main': img.is_main,
            })
        except Exception as e:
            print(f"[moto_for_parts] upload error: {e}")

    return JsonResponse({
        'success': True,
        'uploaded': uploaded,
        'total_count': draft.images.count(),
    })


@login_required
@require_POST
def reorder_moto_for_parts_images(request):
    """AJAX reorder draft images."""
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

    image_ids = data.get('image_ids', [])
    if not image_ids:
        return JsonResponse({'success': False, 'error': 'No image_ids'}, status=400)

    draft_id = request.session.get(MOTO_FOR_PARTS_DRAFT_SESSION_KEY)
    if not draft_id:
        return JsonResponse({'success': False, 'error': 'No draft'}, status=400)

    for new_order, img_id in enumerate(image_ids):
        try:
            img = ListingImage.objects.get(
                pk=img_id,
                listing_id=draft_id,
                listing__seller=request.user,
            )
            img.order = new_order
            img.is_main = (new_order == 0)
            img.save(update_fields=['order', 'is_main'])
        except ListingImage.DoesNotExist:
            continue

    return JsonResponse({'success': True})


@login_required
@require_POST
def delete_moto_for_parts_image(request, pk):
    """AJAX delete one image (works for both draft and active listings)."""
    try:
        img = ListingImage.objects.get(
            pk=pk,
            listing__seller=request.user,
        )
        was_main = img.is_main
        listing = img.listing
        img.delete()
        if was_main:
            first = listing.images.order_by('order').first()
            if first:
                first.is_main = True
                first.save(update_fields=['is_main'])
        return JsonResponse({'success': True})
    except ListingImage.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Not found'}, status=404)


# ═══════════════════════════════════════════════════════════
# AJAX endpoints — EDIT (active listing images)
# ═══════════════════════════════════════════════════════════

@login_required
@require_POST
def upload_moto_for_parts_edit_image(request, pk):
    """AJAX upload image to existing (active) listing."""
    listing = get_object_or_404(
        Listing,
        pk=pk,
        seller=request.user,
    )

    images = request.FILES.getlist('images')
    if not images:
        return JsonResponse({'success': False, 'error': 'No images'}, status=400)

    try:
        validate_images(images)
    except ImageValidationError as exc:
        return JsonResponse({'success': False, 'error': str(exc)}, status=400)

    existing = listing.images.count()
    uploaded = []

    for i, img_file in enumerate(images[:36]):
        try:
            img = ListingImage.objects.create(
                listing=listing,
                image=img_file,
                is_main=(existing == 0 and i == 0),
                order=existing + i,
            )
            uploaded.append({
                'id': img.pk,
                'url': img.image.url,
                'is_main': img.is_main,
            })
        except Exception as e:
            print(f"[moto_for_parts edit] upload error: {e}")

    return JsonResponse({
        'success': True,
        'uploaded': uploaded,
        'total_count': listing.images.count(),
    })


@login_required
@require_POST
def reorder_moto_for_parts_edit_images(request, pk):
    """AJAX reorder existing listing images."""
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

    image_ids = data.get('image_ids', [])
    if not image_ids:
        return JsonResponse({'success': False, 'error': 'No image_ids'}, status=400)

    listing = get_object_or_404(Listing, pk=pk, seller=request.user)

    for new_order, img_id in enumerate(image_ids):
        try:
            img = ListingImage.objects.get(
                pk=img_id,
                listing=listing,
            )
            img.order = new_order
            img.is_main = (new_order == 0)
            img.save(update_fields=['order', 'is_main'])
        except ListingImage.DoesNotExist:
            continue

    return JsonResponse({'success': True})