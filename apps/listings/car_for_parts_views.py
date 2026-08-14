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
    Brand, Model, FuelType, Transmission,
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


CAR_FOR_PARTS_DRAFT_SESSION_KEY = 'active_car_for_parts_draft_id'
CAR_FOR_PARTS_SUBCATEGORY_SLUG = 'whole-car-for-parts'


# ═══════════════════════════════════════════════════════════
# HELPER funkcijos vidaus naudojimui
# ═══════════════════════════════════════════════════════════

def _get_or_create_draft(request):
    """Get session draft or create new car-for-parts draft."""
    draft_id = request.session.get(CAR_FOR_PARTS_DRAFT_SESSION_KEY)
    if draft_id:
        try:
            return Listing.objects.get(
                pk=draft_id,
                seller=request.user,
                status='draft',
            )
        except Listing.DoesNotExist:
            request.session[CAR_FOR_PARTS_DRAFT_SESSION_KEY] = None

    parts_vt = VehicleType.objects.filter(slug='parts').first()
    if not parts_vt:
        return None

    sub = SubCategory.objects.filter(
        vehicle_type=parts_vt,
        slug=CAR_FOR_PARTS_SUBCATEGORY_SLUG,
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
    request.session[CAR_FOR_PARTS_DRAFT_SESSION_KEY] = draft.pk
    request.session.modified = True
    return draft


def _parse_car_for_parts_specific_fields(request):
    """
    Parse'ina TIK car-for-parts SPECIFINIUS laukus iš POST.
    BENDRUS laukus parse'ina parse_common_listing_fields() helper'iu.
    """
    return {
        'brand_id': _int_or_none(request.POST.get('brand')),
        'model_id': _int_or_none(request.POST.get('model')),
        'modification': request.POST.get('modification', '').strip(),
        'version': request.POST.get('version', '').strip(),
        'fuel_type_id': _int_or_none(request.POST.get('fuel_type')),
        'engine_capacity': _float_or_none(request.POST.get('engine_capacity')),
        'power': _int_or_none(request.POST.get('power')),
        'mileage': _int_or_none(request.POST.get('mileage_km')),
        'transmission_id': _int_or_none(request.POST.get('transmission')),
        'body_type': request.POST.get('body_type', '').strip(),
        'doors': request.POST.get('doors', '').strip(),
        'drive_type': request.POST.get('drive_type', '').strip(),
        'color': request.POST.get('color', '').strip(),
        'color_code': request.POST.get('color_code', '').strip(),
        'engine_code': request.POST.get('engine_code', '').strip(),
        'gearbox_code': request.POST.get('gearbox_code', '').strip(),
    }


def _apply_car_for_parts_specific_fields(listing, specific_data):
    """
    Užpildo car-for-parts SPECIFINIUS laukus į listing objektą.
    BENDRUS laukus užpildo apply_common_fields_to_listing() helper'iu.
    """
    listing.modification = specific_data['modification']
    listing.version = specific_data['version']
    listing.body_type = specific_data['body_type']
    listing.doors = specific_data['doors']
    listing.drive_type = specific_data['drive_type']
    listing.color = specific_data['color']
    listing.color_code = specific_data['color_code']
    listing.engine_code = specific_data['engine_code']
    listing.gearbox_code = specific_data['gearbox_code']
    listing.engine_capacity = specific_data['engine_capacity']
    listing.power = specific_data['power']
    if specific_data['mileage'] is not None:
        listing.mileage = specific_data['mileage']

    # FK laukai (su safe lookup)
    if specific_data['brand_id']:
        try:
            listing.brand = Brand.objects.get(pk=specific_data['brand_id'])
        except Brand.DoesNotExist:
            pass
    if specific_data['model_id']:
        try:
            listing.model = Model.objects.get(pk=specific_data['model_id'])
        except Model.DoesNotExist:
            pass
    if specific_data['fuel_type_id']:
        try:
            listing.fuel_type = FuelType.objects.get(pk=specific_data['fuel_type_id'])
        except FuelType.DoesNotExist:
            pass
    else:
        listing.fuel_type = None
    if specific_data['transmission_id']:
        try:
            listing.transmission = Transmission.objects.get(pk=specific_data['transmission_id'])
        except Transmission.DoesNotExist:
            pass
    else:
        listing.transmission = None


def _build_context(request, draft_or_listing, is_edit_mode=False):
    """Bendras context builder CREATE ir EDIT view'ams."""
    user_phone = ''
    if hasattr(request.user, 'profile') and request.user.profile.phone_number:
        user_phone = request.user.profile.phone_number

    context = {
        'draft': draft_or_listing,
        'brands': Brand.objects.all().order_by('name'),
        'years': list(range(2026, 1949, -1)),
        'fuel_types': FuelType.objects.all().order_by('name'),
        'transmissions': Transmission.objects.all().order_by('name'),
        'condition_choices': Listing.CONDITION_CHOICES,
        'body_type_choices': Listing.BODY_TYPE_CHOICES,
        'door_choices': Listing.DOOR_CHOICES,
        'drive_type_choices': Listing.DRIVE_TYPE_CHOICES,
        'color_choices': Listing.COLOR_CHOICES,
        # Country/state lists come from contact_block_tags (this used to be
        # narrowed to the US only, which is why the dropdown had one option).
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
def car_for_parts_create(request):
    """Single-page form for 'Whole car for parts' listings."""

    if request.GET.get('new') == '1' and request.method == 'GET':
        request.session[CAR_FOR_PARTS_DRAFT_SESSION_KEY] = None
        request.session.modified = True

    resume_id = _int_or_none(request.GET.get('draft'))
    if resume_id:
        try:
            existing = Listing.objects.get(
                pk=resume_id,
                seller=request.user,
                status='draft',
            )
            request.session[CAR_FOR_PARTS_DRAFT_SESSION_KEY] = existing.pk
            request.session.modified = True
        except Listing.DoesNotExist:
            messages.error(request, 'Draft not found.')
            return redirect('car_for_parts_create')

    draft = _get_or_create_draft(request)
    if not draft:
        messages.error(request, "Parts category not configured.")
        return redirect('listing_list')

    if request.method == 'POST':
        # 1. Parse fields — BENDRUS per helper, SPECIFINIUS atskirai
        common = parse_common_listing_fields(request)
        specific = _parse_car_for_parts_specific_fields(request)

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
            _apply_car_for_parts_specific_fields(draft, specific)

            # 5. Build title
            draft.title = build_listing_title(
                brand_name=draft.brand.name if draft.brand else '',
                model_name=draft.model.name if draft.model else '',
                year=draft.year,
                suffix='(for parts)',
            )

            # 6. PUBLISH per helper
            # Atlieka: phone save + coords + save() + activate() + email
            finalize_listing_publish(draft, common['phone'], request.user)

            # 7. Cleanup session
            request.session[CAR_FOR_PARTS_DRAFT_SESSION_KEY] = None
            request.session.modified = True

            return redirect(
                reverse('listing_success', kwargs={'pk': draft.pk}) + '?action=published'
            )

    context = _build_context(request, draft, is_edit_mode=False)
    return render(request, 'listings/car_for_parts_create.html', context)


# ═══════════════════════════════════════════════════════════
# EDIT view
# ═══════════════════════════════════════════════════════════

@login_required
def car_for_parts_edit(request, pk):
    """Single-page edit form for existing 'Whole car for parts' listing."""
    listing = get_object_or_404(
        Listing,
        pk=pk,
        seller=request.user,
    )

    # Verify it IS a car-for-parts listing
    if not listing.subcategory or listing.subcategory.slug != CAR_FOR_PARTS_SUBCATEGORY_SLUG:
        messages.error(request, "This listing cannot be edited here.")
        return redirect('listing_edit_hub', pk=pk)

    if request.method == 'POST':
        # 1. Parse fields
        common = parse_common_listing_fields(request)
        specific = _parse_car_for_parts_specific_fields(request)

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
            _apply_car_for_parts_specific_fields(listing, specific)

            # 5. Update title
            listing.title = build_listing_title(
                brand_name=listing.brand.name if listing.brand else '',
                model_name=listing.model.name if listing.model else '',
                year=listing.year,
                suffix='(for parts)',
            )

            # 6. EDIT per helper
            # Atlieka: phone save + coords recalc + save()
            finalize_listing_edit(listing, common['phone'], request.user)

            messages.success(request, 'Listing updated successfully.')
            return redirect('listing_detail', pk=listing.pk)

    context = _build_context(request, listing, is_edit_mode=True)
    return render(request, 'listings/car_for_parts_create.html', context)


# ═══════════════════════════════════════════════════════════
# AJAX endpoints — CREATE (draft images)
# ═══════════════════════════════════════════════════════════

@login_required
@require_POST
def upload_car_for_parts_image(request):
    """AJAX upload image to draft."""
    draft = _get_or_create_draft(request)
    if not draft:
        return JsonResponse({'success': False, 'error': 'No draft'}, status=400)

    images = request.FILES.getlist('images')
    if not images:
        return JsonResponse({'success': False, 'error': 'No images'}, status=400)

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
            print(f"[car_for_parts] upload error: {e}")

    return JsonResponse({
        'success': True,
        'uploaded': uploaded,
        'total_count': draft.images.count(),
    })


@login_required
@require_POST
def reorder_car_for_parts_images(request):
    """AJAX reorder draft images."""
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

    image_ids = data.get('image_ids', [])
    if not image_ids:
        return JsonResponse({'success': False, 'error': 'No image_ids'}, status=400)

    draft_id = request.session.get(CAR_FOR_PARTS_DRAFT_SESSION_KEY)
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
def delete_car_for_parts_image(request, pk):
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
def upload_car_for_parts_edit_image(request, pk):
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
            print(f"[car_for_parts edit] upload error: {e}")

    return JsonResponse({
        'success': True,
        'uploaded': uploaded,
        'total_count': listing.images.count(),
    })


@login_required
@require_POST
def reorder_car_for_parts_edit_images(request, pk):
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