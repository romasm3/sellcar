"""
Moto Gear listing creation, browse and search.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST, require_GET
from django.db.models import Count, Q, Case, When, IntegerField, Value
from django.db.models.functions import Greatest, Coalesce
from datetime import timedelta

from .models import (
    Listing,
    ListingImage,
    VehicleType,
    SubCategory,
    SavedListing,
    Equipment,
    ListingEquipment,
    GearBrand,
)


NEW_LISTING_DAYS = 3

GEAR_TYPE_BY_SLUG = {
    'helmets': 'helmet',
    'protective-gear': 'protective',
    'boots': 'boots',
    'pants': 'pants',
    'suits': 'suit',
    'bags': 'bag',
    'gloves': 'gloves',
    'jackets': 'jacket',
    'other-gear': 'other',
}

GEAR_SLUGS = set(GEAR_TYPE_BY_SLUG.keys())

MOTO_GEAR_DRAFT_SESSION_KEY = 'active_motogear_draft_id'


def _int_or_none(value):
    if value is None or value == '':
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def _float_or_none(value):
    if value is None or value == '':
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def _build_title(subcategory_name, brand_name, model_name, size):
    parts = []
    if brand_name:
        parts.append(brand_name)
    if model_name:
        parts.append(model_name)
    if not parts and subcategory_name:
        parts.append(subcategory_name)
    if size:
        parts.append(f'({size})')
    title = ' '.join(parts).strip()
    return title or 'Moto gear listing'


def _moto_gear_public_qs(request_user=None):
    now = timezone.now()
    sold_cutoff = now - timedelta(days=Listing.SOLD_DISPLAY_DAYS)
    qs = Listing.objects.filter(
        Q(status='active') | Q(status='sold', sold_at__gte=sold_cutoff)
    ).filter(
        vehicle_type__slug='motorcycles',
        subcategory__slug__in=list(GEAR_SLUGS),
    )
    if request_user and request_user.is_authenticated and request_user.is_superuser:
        return qs
    return qs.filter(is_shadow_banned=False)


def _gear_equipment_for_type(gear_type):
    qs = Equipment.objects.filter(category='gear').order_by('order', 'name')
    return [eq for eq in qs if eq.applies_to_gear_type(gear_type)]


def _subtypes_for_gear_type(gear_type):
    if not gear_type:
        return []
    prefix = f'{gear_type}:'
    return [(c, l) for c, l in Listing.GEAR_SUBTYPE_CHOICES if c.startswith(prefix)]


# ═══════════════════════════════════════════════════════════
# AJAX
# ═══════════════════════════════════════════════════════════

@require_GET
def get_gear_equipment_ajax(request):
    gear_type = request.GET.get('gear_type', '').strip()
    if not gear_type:
        return JsonResponse([], safe=False)
    equipment_list = _gear_equipment_for_type(gear_type)
    data = [{'id': eq.id, 'name': eq.name, 'order': eq.order} for eq in equipment_list]
    return JsonResponse(data, safe=False)


@require_GET
def get_gear_subtypes_ajax(request):
    gear_type = request.GET.get('gear_type', '').strip()
    subtypes = _subtypes_for_gear_type(gear_type)
    data = [{'code': c, 'label': l} for c, l in subtypes]
    return JsonResponse(data, safe=False)


# ═══════════════════════════════════════════════════════════
# IMAGE AUTOSAVE — same pattern as cars (upload_draft_images_ajax)
# ═══════════════════════════════════════════════════════════

def _get_or_create_draft(request):
    """Returns active motogear draft, creating one if needed."""
    draft_id = request.session.get(MOTO_GEAR_DRAFT_SESSION_KEY)
    if draft_id:
        try:
            return Listing.objects.get(
                pk=draft_id, seller=request.user, status='draft'
            )
        except Listing.DoesNotExist:
            pass

    moto_vt = VehicleType.objects.filter(slug='motorcycles').first()
    if not moto_vt:
        return None

    listing = Listing.objects.create(
        seller=request.user,
        vehicle_type=moto_vt,
        title='Moto gear draft',
        year=2024,
        mileage=0,
        defects='none',
        price=0,
        city='—',
        status='draft',
    )
    request.session[MOTO_GEAR_DRAFT_SESSION_KEY] = listing.pk
    request.session.modified = True
    return listing


@login_required
@require_POST
def upload_motogear_draft_images_ajax(request):
    """Upload one or more images to the active motogear draft."""
    listing = _get_or_create_draft(request)
    if not listing:
        return JsonResponse({'success': False, 'error': 'Cannot create draft'}, status=500)

    images = request.FILES.getlist('images')
    if not images:
        return JsonResponse({'success': False, 'error': 'No images uploaded'}, status=400)

    existing_count = listing.images.count()
    available = max(0, 40 - existing_count)
    if available <= 0:
        return JsonResponse({'success': False, 'error': 'Maximum 40 photos reached'}, status=400)

    uploaded = []
    for i, image in enumerate(images[:available]):
        try:
            img = ListingImage.objects.create(
                listing=listing,
                image=image,
                is_main=(existing_count == 0 and i == 0),
                order=existing_count + i,
            )
            uploaded.append({
                'id': img.pk,
                'url': img.image.url,
                'is_main': img.is_main,
                'order': img.order,
            })
        except Exception as e:
            print(f"[motogear image upload] {e}")

    return JsonResponse({
        'success': True,
        'uploaded': uploaded,
        'total_count': listing.images.count(),
        'listing_id': listing.pk,
    })


@login_required
@require_POST
def delete_motogear_draft_image_ajax(request, pk):
    """Delete a single image from the active motogear draft."""
    try:
        img = ListingImage.objects.get(
            pk=pk,
            listing__seller=request.user,
            listing__status='draft',
        )
    except ListingImage.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Image not found'}, status=404)

    listing = img.listing
    was_main = img.is_main
    img.delete()

    # If we deleted the main image, promote the next one
    if was_main:
        next_img = listing.images.order_by('order').first()
        if next_img:
            next_img.is_main = True
            next_img.save(update_fields=['is_main'])

    return JsonResponse({'success': True, 'remaining': listing.images.count()})


@login_required
@require_POST
def reorder_motogear_draft_images_ajax(request):
    """Reorder images by ID list. First in list becomes main."""
    import json
    try:
        data = json.loads(request.body or '{}')
    except Exception:
        return JsonResponse({'success': False, 'error': 'Bad JSON'}, status=400)

    image_ids = data.get('image_ids', [])
    if not image_ids:
        return JsonResponse({'success': False, 'error': 'No image_ids'}, status=400)

    # Verify all belong to the same draft owned by user
    images = list(ListingImage.objects.filter(
        pk__in=image_ids,
        listing__seller=request.user,
        listing__status='draft',
    ))
    if len(images) != len(image_ids):
        return JsonResponse({'success': False, 'error': 'Some images not found'}, status=404)

    img_map = {img.pk: img for img in images}
    for new_order, img_id in enumerate(image_ids):
        img = img_map.get(img_id)
        if img:
            img.order = new_order
            img.is_main = (new_order == 0)
            img.save(update_fields=['order', 'is_main'])

    return JsonResponse({'success': True})


# ═══════════════════════════════════════════════════════════
# CREATE FORM
# ═══════════════════════════════════════════════════════════

def _get_user_phone(user):
    phone = getattr(user, 'phone', None)
    if phone:
        return phone
    profile = getattr(user, 'profile', None)
    if profile:
        phone = getattr(profile, 'phone', None)
        if phone:
            return phone
    return ''


@login_required
def motogear_listing_create(request):
    if request.method == 'GET' and request.GET.get('new'):
        if MOTO_GEAR_DRAFT_SESSION_KEY in request.session:
            del request.session[MOTO_GEAR_DRAFT_SESSION_KEY]
            request.session.modified = True

    if request.method == 'POST':
        return _handle_post(request)

    draft_id = request.session.get(MOTO_GEAR_DRAFT_SESSION_KEY)
    submitted = {}
    selected_subcategory_slug = request.GET.get('subcategory', '')
    selected_equipment_ids = []
    current_draft = None

    if draft_id:
        try:
            current_draft = Listing.objects.get(pk=draft_id, seller=request.user, status='draft')
            submitted = _draft_to_submitted(current_draft)
            if current_draft.subcategory:
                selected_subcategory_slug = current_draft.subcategory.slug
            selected_equipment_ids = list(
                current_draft.equipment_items.values_list('equipment_id', flat=True)
            )
        except Listing.DoesNotExist:
            del request.session[MOTO_GEAR_DRAFT_SESSION_KEY]
            request.session.modified = True
            draft_id = None

    if selected_subcategory_slug and selected_subcategory_slug not in GEAR_SLUGS:
        selected_subcategory_slug = ''

    return render(
        request,
        'listings/motogear_create.html',
        _build_context(
            request,
            submitted=submitted,
            draft_id=draft_id,
            current_draft=current_draft,
            selected_subcategory_slug=selected_subcategory_slug,
            selected_equipment_ids=selected_equipment_ids,
        ),
    )


def _build_context(request, submitted=None, errors=None, draft_id=None, current_draft=None,
                   selected_subcategory_slug='', selected_equipment_ids=None):
    moto_vt = VehicleType.objects.filter(slug='motorcycles').first()

    gear_subcategories = []
    if moto_vt:
        gear_subcategories = list(
            SubCategory.objects.filter(
                vehicle_type=moto_vt, slug__in=list(GEAR_SLUGS),
            ).order_by('order', 'name')
        )

    initial_gear_type = ''
    if selected_subcategory_slug:
        initial_gear_type = GEAR_TYPE_BY_SLUG.get(selected_subcategory_slug, '')

    initial_equipment = []
    initial_subtypes = []
    if initial_gear_type:
        initial_equipment = _gear_equipment_for_type(initial_gear_type)
        initial_subtypes = _subtypes_for_gear_type(initial_gear_type)

    gear_brands = list(GearBrand.objects.all().order_by('order', 'name'))

    submitted = submitted or {}
    if not submitted.get('phone'):
        submitted['phone'] = _get_user_phone(request.user)
    if not submitted.get('email'):
        submitted['email'] = request.user.email or ''

    def _safe(name, default=None):
        try:
            return getattr(Listing, name)
        except AttributeError:
            return default or []

    return {
        'gear_subcategories': gear_subcategories,
        'gear_brands': gear_brands,
        'gear_size_choices': _safe('GEAR_SIZE_CHOICES'),
        'gear_material_choices': _safe('GEAR_MATERIAL_CHOICES'),
        'gear_gender_choices': _safe('GEAR_GENDER_CHOICES'),
        'gear_safety_cert_choices': _safe('GEAR_SAFETY_CERT_CHOICES'),
        'condition_choices': _safe('CONDITION_CHOICES', [('new', 'New'), ('used', 'Used')]),
        'color_choices': _safe('COLOR_CHOICES'),
        'country_choices': _safe('COUNTRY_CHOICES', [('US', 'United States')]),
        'us_states': _safe('US_STATE_CHOICES'),
        'submitted': submitted,
        'errors': errors or [],
        'draft_id': draft_id,
        'current_draft': current_draft,
        'selected_subcategory_slug': selected_subcategory_slug,
        'initial_gear_type': initial_gear_type,
        'initial_equipment': initial_equipment,
        'initial_subtypes': initial_subtypes,
        'selected_equipment_ids': selected_equipment_ids or [],
    }


def _draft_to_submitted(draft):
    return {
        'subcategory': str(draft.subcategory_id) if draft.subcategory_id else '',
        'gear_subtype': draft.gear_subtype or '',
        'gear_subtype_other_text': draft.gear_subtype_other_text or '',
        'gear_size': draft.gear_size or '',
        'gear_size_other_text': draft.gear_size_other_text or '',
        'gear_brand': str(draft.gear_brand_id) if draft.gear_brand_id else '',
        'gear_brand_other_text': draft.gear_brand_other_text or '',
        'gear_model_text': draft.gear_model_text or '',
        'gear_material': draft.gear_material or '',
        'gear_material_other_text': draft.gear_material_other_text or '',
        'gear_gender': draft.gear_gender or '',
        'gear_gender_other_text': draft.gear_gender_other_text or '',
        'gear_safety_cert': draft.gear_safety_cert or '',
        'gear_safety_cert_other_text': draft.gear_safety_cert_other_text or '',
        'gear_ventilation_count': str(draft.gear_ventilation_count) if draft.gear_ventilation_count else '',
        'condition': draft.condition or '',
        'color': draft.color or '',
        'color_other_text': draft.color_other_text or '',
        'price': str(int(draft.price)) if draft.price else '',
        'negotiable': 'on' if draft.negotiable else '',
        'open_to_trade': 'on' if draft.open_to_trade else '',
        'description': draft.description or '',
        'video_url': draft.video_url or '',
        'country': draft.country or 'US',
        'state': draft.state or '',
        'city': draft.city if draft.city and draft.city != '—' else '',
        'postal_code': draft.postal_code or '',
        'address': draft.address or '',
        'hide_exact_address': 'on' if draft.hide_exact_address else '',
        'is_business_seller': 'on' if draft.is_business_seller else '',
    }


def _build_fields_from_post(request, POST):
    moto_vt = VehicleType.objects.filter(slug='motorcycles').first()
    if not moto_vt:
        return None

    sub_id = _int_or_none(POST.get('subcategory'))
    subcategory = None
    if sub_id:
        try:
            subcategory = SubCategory.objects.get(
                id=sub_id, vehicle_type=moto_vt, slug__in=list(GEAR_SLUGS),
            )
        except SubCategory.DoesNotExist:
            pass

    gear_type = ''
    if subcategory:
        gear_type = GEAR_TYPE_BY_SLUG.get(subcategory.slug, '')

    brand_id = _int_or_none(POST.get('gear_brand'))
    gear_brand = None
    if brand_id:
        try:
            gear_brand = GearBrand.objects.get(id=brand_id)
        except GearBrand.DoesNotExist:
            pass

    price = _float_or_none(POST.get('price'))
    country = POST.get('country', 'US')
    state = POST.get('state', '') if country == 'US' else ''
    city = POST.get('city', '')

    from .views import get_coordinates_for_location
    if country == 'US' and state:
        state_label = dict(getattr(Listing, 'US_STATE_CHOICES', [])).get(state, state)
        city_for_display = city if city else state_label
    else:
        city_for_display = city
    if not city_for_display:
        city_for_display = '—'

    lat, lng = get_coordinates_for_location(city_for_display, country)

    submitted_subtype = POST.get('gear_subtype', '')
    if submitted_subtype and gear_type and not submitted_subtype.startswith(f'{gear_type}:'):
        submitted_subtype = ''

    brand_name = ''
    if gear_brand:
        if gear_brand.slug == 'other':
            brand_name = POST.get('gear_brand_other_text', '').strip()
        else:
            brand_name = gear_brand.name

    sub_name = subcategory.name if subcategory else ''
    title = _build_title(
        sub_name, brand_name,
        POST.get('gear_model_text', ''),
        POST.get('gear_size', ''),
    )

    fields = {
        'vehicle_type': moto_vt,
        'subcategory': subcategory,
        'title': title,
        'gear_type': gear_type,
        'gear_subtype': submitted_subtype,
        'gear_subtype_other_text': POST.get('gear_subtype_other_text', '').strip(),
        'gear_size': POST.get('gear_size', ''),
        'gear_size_other_text': POST.get('gear_size_other_text', '').strip(),
        'gear_brand': gear_brand,
        'gear_brand_other_text': POST.get('gear_brand_other_text', '').strip(),
        'gear_model_text': POST.get('gear_model_text', '').strip(),
        'gear_material': POST.get('gear_material', ''),
        'gear_material_other_text': POST.get('gear_material_other_text', '').strip(),
        'gear_gender': POST.get('gear_gender', ''),
        'gear_gender_other_text': POST.get('gear_gender_other_text', '').strip(),
        'gear_safety_cert': POST.get('gear_safety_cert', ''),
        'gear_safety_cert_other_text': POST.get('gear_safety_cert_other_text', '').strip(),
        'gear_ventilation_count': _int_or_none(POST.get('gear_ventilation_count')),
        'condition': POST.get('condition') or 'used',
        'color': POST.get('color', ''),
        'color_other_text': POST.get('color_other_text', '').strip(),
        'price': price if price else 0,
        'negotiable': POST.get('negotiable') == 'on',
        'open_to_trade': POST.get('open_to_trade') == 'on',
        'description': POST.get('description', ''),
        'video_url': POST.get('video_url', ''),
        'country': country,
        'city': city_for_display,
        'postal_code': POST.get('postal_code', ''),
        'address': POST.get('address', ''),
        'hide_exact_address': POST.get('hide_exact_address') == 'on',
        'is_business_seller': POST.get('is_business_seller') == 'on',
        'latitude': lat,
        'longitude': lng,
        'status': 'draft',
        'year': 2024,
        'mileage': 0,
        'defects': 'none',
    }
    if hasattr(Listing, 'state'):
        fields['state'] = state
    return fields


def _save_equipment(listing, equipment_ids):
    if not listing:
        return
    listing.equipment_items.filter(equipment__category='gear').delete()
    for eq_id in equipment_ids:
        try:
            eq = Equipment.objects.get(id=eq_id, category='gear')
            ListingEquipment.objects.get_or_create(listing=listing, equipment=eq)
        except (Equipment.DoesNotExist, ValueError):
            pass


def _save_draft_fields(request, POST, draft_id):
    fields = _build_fields_from_post(request, POST)
    if not fields:
        return None

    listing = None
    if draft_id:
        try:
            listing = Listing.objects.get(pk=draft_id, seller=request.user, status='draft')
            for key, value in fields.items():
                setattr(listing, key, value)
            listing.save()
        except Listing.DoesNotExist:
            listing = None

    if listing is None:
        fields['seller'] = request.user
        listing = Listing.objects.create(**fields)

    equipment_ids = []
    for raw_id in POST.getlist('equipment'):
        try:
            equipment_ids.append(int(raw_id))
        except (TypeError, ValueError):
            continue
    _save_equipment(listing, equipment_ids)
    return listing


@login_required
@require_POST
def save_motogear_draft_ajax(request):
    POST = request.POST
    draft_id = _int_or_none(POST.get('draft_id'))

    if not VehicleType.objects.filter(slug='motorcycles').exists():
        return JsonResponse({'success': False, 'error': 'Motorcycles not configured'}, status=400)

    try:
        listing = _save_draft_fields(request, POST, draft_id)
    except Exception as e:
        print(f"[motogear autosave] {e}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

    if not listing:
        return JsonResponse({'success': False, 'error': 'Save failed'}, status=500)

    if not draft_id and not (
        listing.images.exists()
        or (listing.price and float(listing.price) > 0)
        or (listing.description or '').strip()
        or getattr(listing, 'subcategory_id', None)
        or getattr(listing, 'gear_brand_id', None)
        or (getattr(listing, 'gear_model_text', '') or '').strip()
        or (listing.condition or '').strip()
    ):
        listing.delete()
        request.session.pop(MOTO_GEAR_DRAFT_SESSION_KEY, None)
        request.session.modified = True
        return JsonResponse({'success': True, 'listing_id': None, 'skipped': 'empty'})

    request.session[MOTO_GEAR_DRAFT_SESSION_KEY] = listing.pk
    request.session.modified = True

    return JsonResponse({
        'success': True,
        'listing_id': listing.pk,
        'saved_at': timezone.now().isoformat(),
    })


def _handle_post(request):
    POST = request.POST
    FILES = request.FILES
    draft_id = _int_or_none(POST.get('draft_id'))

    submitted = {k: POST.get(k, '') for k in [
        'subcategory', 'gear_subtype', 'gear_subtype_other_text',
        'gear_size', 'gear_size_other_text',
        'gear_brand', 'gear_brand_other_text', 'gear_model_text',
        'gear_material', 'gear_material_other_text',
        'gear_gender', 'gear_gender_other_text',
        'gear_safety_cert', 'gear_safety_cert_other_text',
        'gear_ventilation_count',
        'condition', 'color', 'color_other_text',
        'price', 'negotiable', 'open_to_trade',
        'description', 'video_url',
        'phone', 'email',
        'country', 'state', 'city', 'postal_code', 'address',
        'hide_exact_address', 'is_business_seller',
    ]}

    errors = []
    if not POST.get('subcategory'):
        errors.append('Category is required.')
    if not POST.get('condition'):
        errors.append('Condition is required.')
    price = _float_or_none(POST.get('price'))
    if not price or price <= 0:
        errors.append('Valid price is required.')
    if not POST.get('agree_terms'):
        errors.append('You must agree to terms and conditions.')

    if errors:
        equipment_ids = []
        for raw_id in POST.getlist('equipment'):
            try:
                equipment_ids.append(int(raw_id))
            except (TypeError, ValueError):
                continue
        return render(
            request, 'listings/motogear_create.html',
            _build_context(
                request, submitted=submitted, errors=errors, draft_id=draft_id,
                selected_equipment_ids=equipment_ids,
            ),
        )

    try:
        listing = _save_draft_fields(request, POST, draft_id)
    except Exception as e:
        errors.append(f'Save failed: {e}')
        return render(
            request, 'listings/motogear_create.html',
            _build_context(request, submitted=submitted, errors=errors, draft_id=draft_id),
        )

    if not listing:
        errors.append('Save failed.')
        return render(
            request, 'listings/motogear_create.html',
            _build_context(request, submitted=submitted, errors=errors, draft_id=draft_id),
        )

    # Final submit may also include extra images (fallback) — but normally
    # they were uploaded via AJAX during typing.
    images = FILES.getlist('images')
    existing_count = listing.images.count()
    for i, image in enumerate(images[:40 - existing_count]):
        try:
            ListingImage.objects.create(
                listing=listing, image=image,
                is_main=(existing_count == 0 and i == 0),
                order=existing_count + i,
            )
        except Exception as e:
            print(f"[motogear final] image upload failed: {e}")

    if MOTO_GEAR_DRAFT_SESSION_KEY in request.session:
        del request.session[MOTO_GEAR_DRAFT_SESSION_KEY]
        request.session.modified = True

    # ═══ Pirmi 3 nemokami (bendrai per visas kategorijas) ═══
    from .constants import can_create_free_listing, FREE_LISTING_DAYS
    is_free, _, _ = can_create_free_listing(request.user)

    if is_free:
        listing.activate(days=FREE_LISTING_DAYS)
        from .views import _send_listing_published_email
        _send_listing_published_email(listing, request.user)
        return redirect(
            reverse('listing_success', kwargs={'pk': listing.pk}) + '?action=published'
        )
    else:
        return redirect('listing_select_plan', pk=listing.pk)


# ═══════════════════════════════════════════════════════════
# BROWSE / LIST
# ═══════════════════════════════════════════════════════════

def motogear_list(request):
    _now = timezone.now()
    _three_days_ago = _now - timedelta(days=NEW_LISTING_DAYS)

    listings = _moto_gear_public_qs(request.user).select_related(
        'subcategory', 'vehicle_type', 'gear_brand'
    ).annotate(
        effective_date=Greatest('created_at', Coalesce('last_boosted_at', 'created_at')),
    ).annotate(
        sort_priority=Case(
            When(star_level=2, star_expires_at__gt=_now, then=Value(500)),
            When(star_level=1, star_expires_at__gt=_now, then=Value(400)),
            When(effective_date__gt=_three_days_ago, then=Value(200)),
            default=Value(100),
            output_field=IntegerField(),
        )
    ).order_by('-sort_priority', '-effective_date')

    moto_vt = VehicleType.objects.filter(slug='motorcycles').first()
    gear_subcategories = []
    sub_counts = {}
    if moto_vt:
        gear_subcategories = list(
            SubCategory.objects.filter(
                vehicle_type=moto_vt, slug__in=list(GEAR_SLUGS),
            ).order_by('order', 'name')
        )
        sub_counts = {
            item['subcategory_id']: item['count']
            for item in _moto_gear_public_qs(request.user)
                .values('subcategory_id').annotate(count=Count('id'))
        }
    for sub in gear_subcategories:
        sub.listings_count = sub_counts.get(sub.id, 0)

    f = request.GET
    subcategory_filter = [v for v in f.getlist('subcategory') if v]
    gear_size_filter = [v for v in f.getlist('gear_size') if v]
    gear_material_filter = [v for v in f.getlist('gear_material') if v]
    gear_gender_filter = [v for v in f.getlist('gear_gender') if v]
    gear_brand_filter = [v for v in f.getlist('gear_brand') if v]
    condition_filter = [v for v in f.getlist('condition') if v]
    price_min = f.get('price_min')
    price_max = f.get('price_max')
    search_query = f.get('search', '')
    country_filter = f.get('country_filter', '')
    state_filter = f.get('state_filter', '')

    if search_query:
        listings = listings.filter(
            Q(title__icontains=search_query) |
            Q(gear_brand__name__icontains=search_query) |
            Q(gear_brand_other_text__icontains=search_query) |
            Q(gear_model_text__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    if subcategory_filter:
        listings = listings.filter(subcategory_id__in=subcategory_filter)
    if gear_size_filter:
        listings = listings.filter(gear_size__in=gear_size_filter)
    if gear_material_filter:
        listings = listings.filter(gear_material__in=gear_material_filter)
    if gear_gender_filter:
        listings = listings.filter(gear_gender__in=gear_gender_filter)
    if gear_brand_filter:
        listings = listings.filter(gear_brand_id__in=gear_brand_filter)
    if condition_filter:
        listings = listings.filter(condition__in=condition_filter)
    if price_min:
        listings = listings.filter(price__gte=price_min)
    if price_max:
        listings = listings.filter(price__lte=price_max)
    if state_filter:
        listings = listings.filter(country='US', state=state_filter)
    elif country_filter:
        listings = listings.filter(country=country_filter)

    saved_ids = []
    if request.user.is_authenticated:
        saved_ids = list(SavedListing.objects.filter(
            user=request.user
        ).values_list('listing_id', flat=True))

    listings_list = list(listings[:60])

    from .views import _track_listing_impressions
    _track_listing_impressions(request, listings_list)

    new_listing_ids = [
        l.id for l in listings_list
        if l.created_at >= timezone.now() - timedelta(days=NEW_LISTING_DAYS)
    ]

    def _safe(name, default=None):
        try:
            return getattr(Listing, name)
        except AttributeError:
            return default or []

    context = {
        'listings': listings_list,
        'total_count': listings.count(),
        'gear_subcategories': gear_subcategories,
        'gear_brands': list(GearBrand.objects.all().order_by('order', 'name')),
        'gear_size_choices': _safe('GEAR_SIZE_CHOICES'),
        'gear_material_choices': _safe('GEAR_MATERIAL_CHOICES'),
        'gear_gender_choices': _safe('GEAR_GENDER_CHOICES'),
        'condition_choices': _safe('CONDITION_CHOICES', [('new', 'New'), ('used', 'Used')]),
        'us_states': _safe('US_STATE_CHOICES'),
        'country_choices': _safe('COUNTRY_CHOICES', []),
        'selected_subcategories': subcategory_filter,
        'selected_sizes': gear_size_filter,
        'selected_materials': gear_material_filter,
        'selected_genders': gear_gender_filter,
        'selected_brands': gear_brand_filter,
        'selected_conditions': condition_filter,
        'selected_country': country_filter,
        'selected_state': state_filter,
        'search_query': search_query,
        'saved_ids': saved_ids,
        'new_listing_ids': new_listing_ids,
        'selected_category': 'moto-gear',
    }
    return render(request, 'listings/motogear_list.html', context)





def _apply_gear_filters(qs, p):

    def has(k):

        return bool((p.get(k) or '').strip())

    if has('gear_type'):

        qs = qs.filter(gear_type=p['gear_type'])

    if has('gear_subtype'):

        qs = qs.filter(gear_subtype=p['gear_subtype'])

    if has('gear_size'):

        qs = qs.filter(gear_size=p['gear_size'])

    if has('gear_material'):

        qs = qs.filter(gear_material=p['gear_material'])

    if has('gear_gender'):

        qs = qs.filter(gear_gender=p['gear_gender'])

    if has('gear_safety_cert'):

        qs = qs.filter(gear_safety_cert=p['gear_safety_cert'])

    if has('gear_brand'):

        qs = qs.filter(gear_brand_id=p['gear_brand'])

    if has('condition'):

        qs = qs.filter(condition=p['condition'])

    if has('color'):
        qs = qs.filter(color=p['color'])
    if has('price_min'):

        qs = qs.filter(price__gte=p['price_min'])

    if has('price_max'):

        qs = qs.filter(price__lte=p['price_max'])

    if has('city'):

        qs = qs.filter(city__icontains=p['city'].strip())

    if has('state_filter'):

        qs = qs.filter(country='US', state=p['state_filter'])

    elif has('country_filter'):

        qs = qs.filter(country=p['country_filter'])

    _eq = p.getlist('equipment') if hasattr(p, 'getlist') else []
    for _e in _eq:
        if _e:
            qs = qs.filter(equipment_items__equipment_id=_e)
    if has('posted_within'):

        try:

            cutoff = timezone.now() - timedelta(days=int(p['posted_within']))

            qs = qs.filter(created_at__gte=cutoff)

        except (ValueError, TypeError):

            pass

    _q = (p.get('search') or p.get('q') or '').strip()

    if _q:

        qs = qs.filter(

            Q(title__icontains=_q) |

            Q(gear_brand__name__icontains=_q) |

            Q(gear_model_text__icontains=_q) |

            Q(description__icontains=_q)

        )

    return qs





def _gear_choice(name, default=None):

    try:

        return getattr(Listing, name)

    except AttributeError:

        return default or []





def motogear_advanced_search(request):

    qs = _apply_gear_filters(_moto_gear_public_qs(request.user), request.GET)

    context = {

        'f': request.GET,

        'total_count': qs.count(),

        'gear_type_choices': _gear_choice('GEAR_TYPE_CHOICES'),

        'gear_subtype_choices': _gear_choice('GEAR_SUBTYPE_CHOICES'),

        'gear_size_choices': _gear_choice('GEAR_SIZE_CHOICES'),

        'gear_material_choices': _gear_choice('GEAR_MATERIAL_CHOICES'),

        'gear_gender_choices': _gear_choice('GEAR_GENDER_CHOICES'),

        'gear_safety_cert_choices': _gear_choice('GEAR_SAFETY_CERT_CHOICES'),

        'condition_choices': _gear_choice('CONDITION_CHOICES', [('new', 'New'), ('used', 'Used')]),

        'gear_brands': list(GearBrand.objects.all().order_by('order', 'name')),

        'country_choices': _gear_choice('COUNTRY_CHOICES', []),

        'us_states': _gear_choice('US_STATE_CHOICES'),

    }

    return render(request, 'listings/motogear_advanced.html', context)





def motogear_count_ajax(request):

    qs = _apply_gear_filters(_moto_gear_public_qs(request.user), request.GET)

    return JsonResponse({'count': qs.count()})

