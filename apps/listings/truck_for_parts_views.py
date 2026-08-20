from .search_params import sanitize as sanitize_search_params
"""
Whole truck for parts — autogidas "Sunkiojo transporto dalys" 1:1.
Klonas iš car_for_parts_views.py: Brand→TruckBrand, Model→truck_model_text,
+ truck_type (Tipas) + Ypatumai (truck_* equipment checkbox'ai).
URL: /create/truck-for-parts/
"""

from django.utils.translation import gettext_lazy as _
import json
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .image_validation import ImageValidationError, validate_images
from .models import (
    Listing, ListingImage, VehicleType, SubCategory,
    TruckBrand, FuelType, Equipment, ListingEquipment,
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

TRUCK_FOR_PARTS_DRAFT_SESSION_KEY = 'active_truck_for_parts_draft_id'
TRUCK_FOR_PARTS_SUBCATEGORY_SLUG = 'whole-truck-for-parts'

# Ypatumai grupės (truck equipment kategorijos) — rodymo tvarka + label
TRUCK_PART_CATEGORIES = [
    ('truck_part_body', _('Body parts')),
    ('truck_part_chassis', _('Chassis / transmission parts')),
    ('truck_part_cooling', _('Cooling system parts')),
    ('truck_part_electrical', _('Electrical system parts')),
    ('truck_part_engine', _('Engine parts')),
    ('truck_part_interior', _('Cabin / interior parts')),
    ('truck_part_superstructure', _('Superstructure parts')),
]


# ─────────────────────── HELPERS ───────────────────────

def _get_draft(request):
    """Sesijos draft'as, jei jis JAU yra. Nekuria naujo.

    GET užklausa naujo draft'o nebekuria: anksčiau vien atidarius formą
    DB atsirasdavo „Untitled draft" eilutė, net jei vartotojas nieko
    neįvedė. Eilutė sukuriama tik tada, kai vartotojas ką nors realiai
    padaro — įkelia nuotrauką (AJAX) arba pateikia formą (POST).
    """
    draft_id = request.session.get(TRUCK_FOR_PARTS_DRAFT_SESSION_KEY)
    if not draft_id:
        return None
    try:
        return Listing.objects.get(
            pk=draft_id, seller=request.user, status='draft')
    except Listing.DoesNotExist:
        request.session[TRUCK_FOR_PARTS_DRAFT_SESSION_KEY] = None
        return None


def _get_or_create_draft(request):
    draft_id = request.session.get(TRUCK_FOR_PARTS_DRAFT_SESSION_KEY)
    if draft_id:
        try:
            return Listing.objects.get(pk=draft_id, seller=request.user, status='draft')
        except Listing.DoesNotExist:
            request.session[TRUCK_FOR_PARTS_DRAFT_SESSION_KEY] = None

    parts_vt = VehicleType.objects.filter(slug='parts').first()
    if not parts_vt:
        return None

    sub = SubCategory.objects.filter(
        vehicle_type=parts_vt, slug=TRUCK_FOR_PARTS_SUBCATEGORY_SLUG,
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
    request.session[TRUCK_FOR_PARTS_DRAFT_SESSION_KEY] = draft.pk
    request.session.modified = True
    return draft


def _parse_specific(request):
    return {
        'truck_brand_id': _int_or_none(request.POST.get('truck_brand')),
        'truck_model_text': (request.POST.get('truck_model_text') or '').strip(),
        'truck_type': (request.POST.get('truck_type') or '').strip(),
        'fuel_type_id': _int_or_none(request.POST.get('fuel_type')),
        'engine_capacity': _float_or_none(request.POST.get('engine_capacity')),
        'power': _int_or_none(request.POST.get('power')),
        'mileage': _int_or_none(request.POST.get('mileage_km')),
        'color': (request.POST.get('color') or '').strip(),
        'part_types': [v for v in request.POST.getlist('part_types') if v],
    }


def _apply_specific(listing, d):
    listing.truck_model_text = d['truck_model_text']
    listing.truck_type = d['truck_type']
    listing.color = d['color']
    listing.engine_capacity = d['engine_capacity']
    listing.power = d['power']
    if d['mileage'] is not None:
        listing.mileage = d['mileage']

    if d['truck_brand_id']:
        try:
            listing.truck_brand = TruckBrand.objects.get(pk=d['truck_brand_id'])
        except TruckBrand.DoesNotExist:
            pass
    if d['fuel_type_id']:
        try:
            listing.fuel_type = FuelType.objects.get(pk=d['fuel_type_id'])
        except FuelType.DoesNotExist:
            pass
    else:
        listing.fuel_type = None


def _sync_part_types(listing, part_type_ids):
    """Perrašo Ypatumai (ListingEquipment) pagal pažymėtus checkbox'us."""
    listing.equipment_items.all().delete()
    for eid in part_type_ids:
        try:
            ListingEquipment.objects.create(listing=listing, equipment_id=int(eid))
        except (ValueError, TypeError):
            pass


def _part_groups(selected_ids=None):
    selected_ids = set(str(x) for x in (selected_ids or []))
    groups, sel = [], []
    for key, label in TRUCK_PART_CATEGORIES:
        items = list(Equipment.objects.filter(category=key).order_by('name'))
        if items:
            groups.append({'key': key, 'label': label, 'items': items})
    return groups, selected_ids


def _build_context(request, draft_or_listing, is_edit_mode=False):
    user_phone = ''
    if hasattr(request.user, 'profile') and request.user.profile.phone_number:
        user_phone = request.user.profile.phone_number

    # draft_or_listing gali būti None: GET nebekuria draft'o eilutės
    if draft_or_listing is not None:
        sel = list(draft_or_listing.equipment_items.values_list('equipment_id', flat=True))
    else:
        sel = []
    part_groups, sel_ids = _part_groups(sel)

    context = {
        'draft': draft_or_listing,
        'truck_brands': TruckBrand.objects.all().order_by('name'),
        'truck_type_choices': Listing._meta.get_field('truck_type').choices,
        'years': list(range(2026, 1949, -1)),
        'fuel_types': FuelType.objects.all().order_by('name'),
        'condition_choices': Listing.CONDITION_CHOICES,
        'color_choices': Listing.COLOR_CHOICES,
        # Country/state lists come from contact_block_tags (was US-only here).
        'part_groups': part_groups,
        'sel_part_types': sel_ids,
        'user_phone': user_phone,
    }
    if is_edit_mode:
        context['listing'] = draft_or_listing
        context['is_edit_mode'] = True
    return context


# ─────────────────────── CREATE ───────────────────────

@login_required
def truck_for_parts_create(request):
    if request.GET.get('new') == '1' and request.method == 'GET':
        request.session[TRUCK_FOR_PARTS_DRAFT_SESSION_KEY] = None
        request.session.modified = True

    resume_id = _int_or_none(request.GET.get('draft'))
    if resume_id:
        try:
            existing = Listing.objects.get(pk=resume_id, seller=request.user, status='draft')
            request.session[TRUCK_FOR_PARTS_DRAFT_SESSION_KEY] = existing.pk
            request.session.modified = True
        except Listing.DoesNotExist:
            messages.error(request, 'Draft not found.')
            return redirect('truck_for_parts_create')

    # GET tik atidaro formą — eilutės DB nekuriam (žr. _get_draft).
    draft = _get_draft(request)

    if request.method == 'POST':
        if draft is None:
            draft = _get_or_create_draft(request)
        if not draft:
            messages.error(request, "Parts category not configured.")
            return redirect('listing_list')

        common = parse_common_listing_fields(request)
        specific = _parse_specific(request)

        errors = validate_common_fields(common, require_terms=True)
        if not specific['truck_brand_id']:
            errors.append('Brand is required')
        if not specific['truck_model_text']:
            errors.append('Model is required')
        if not specific['truck_type']:
            errors.append('Type is required')

        if errors:
            for e in errors:
                messages.error(request, e)
        else:
            apply_common_fields_to_listing(draft, common)
            _apply_specific(draft, specific)
            draft.title = build_listing_title(
                brand_name=draft.truck_brand.name if draft.truck_brand else '',
                model_name=specific['truck_model_text'],
                year=draft.year,
                suffix='(for parts)',
            )
            finalize_listing_publish(draft, common['phone'], request.user)
            _sync_part_types(draft, specific['part_types'])

            request.session[TRUCK_FOR_PARTS_DRAFT_SESSION_KEY] = None
            request.session.modified = True
            return redirect(reverse('listing_success', kwargs={'pk': draft.pk}) + '?action=published')

    context = _build_context(request, draft, is_edit_mode=False)
    return render(request, 'listings/truck_for_parts_create.html', context)


# ─────────────────────── EDIT ───────────────────────

@login_required
def truck_for_parts_edit(request, pk):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user)
    if not listing.subcategory or listing.subcategory.slug != TRUCK_FOR_PARTS_SUBCATEGORY_SLUG:
        messages.error(request, "This listing cannot be edited here.")
        return redirect('listing_edit_hub', pk=pk)

    if request.method == 'POST':
        common = parse_common_listing_fields(request)
        specific = _parse_specific(request)

        errors = validate_common_fields(common)
        if not specific['truck_brand_id']:
            errors.append('Brand is required')
        if not specific['truck_model_text']:
            errors.append('Model is required')
        if not specific['truck_type']:
            errors.append('Type is required')

        if errors:
            for e in errors:
                messages.error(request, e)
        else:
            apply_common_fields_to_listing(listing, common)
            _apply_specific(listing, specific)
            listing.title = build_listing_title(
                brand_name=listing.truck_brand.name if listing.truck_brand else '',
                model_name=specific['truck_model_text'],
                year=listing.year,
                suffix='(for parts)',
            )
            finalize_listing_edit(listing, common['phone'], request.user)
            _sync_part_types(listing, specific['part_types'])

            messages.success(request, 'Listing updated successfully.')
            return redirect('listing_detail', pk=listing.pk)

    context = _build_context(request, listing, is_edit_mode=True)
    return render(request, 'listings/truck_for_parts_create.html', context)


# ─────────────────────── AJAX images (CREATE draft) ───────────────────────

@login_required
@require_POST
def upload_truck_for_parts_image(request):
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
                listing=draft, image=img_file,
                is_main=(existing == 0 and i == 0), order=existing + i,
            )
            uploaded.append({'id': img.pk, 'url': img.image.url, 'is_main': img.is_main})
        except Exception as e:
            print(f"[truck_for_parts] upload error: {e}")
    return JsonResponse({'success': True, 'uploaded': uploaded, 'total_count': draft.images.count()})


@login_required
@require_POST
def reorder_truck_for_parts_images(request):
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
    image_ids = data.get('image_ids', [])
    if not image_ids:
        return JsonResponse({'success': False, 'error': 'No image_ids'}, status=400)
    draft_id = request.session.get(TRUCK_FOR_PARTS_DRAFT_SESSION_KEY)
    if not draft_id:
        return JsonResponse({'success': False, 'error': 'No draft'}, status=400)
    for new_order, img_id in enumerate(image_ids):
        try:
            img = ListingImage.objects.get(pk=img_id, listing_id=draft_id, listing__seller=request.user)
            img.order = new_order
            img.is_main = (new_order == 0)
            img.save(update_fields=['order', 'is_main'])
        except ListingImage.DoesNotExist:
            continue
    return JsonResponse({'success': True})


@login_required
@require_POST
def delete_truck_for_parts_image(request, pk):
    try:
        img = ListingImage.objects.get(pk=pk, listing__seller=request.user)
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


# ─────────────────────── AJAX images (EDIT active) ───────────────────────

@login_required
@require_POST
def upload_truck_for_parts_edit_image(request, pk):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user)
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
                listing=listing, image=img_file,
                is_main=(existing == 0 and i == 0), order=existing + i,
            )
            uploaded.append({'id': img.pk, 'url': img.image.url, 'is_main': img.is_main})
        except Exception as e:
            print(f"[truck_for_parts edit] upload error: {e}")
    return JsonResponse({'success': True, 'uploaded': uploaded, 'total_count': listing.images.count()})


@login_required
@require_POST
def reorder_truck_for_parts_edit_images(request, pk):
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
            img = ListingImage.objects.get(pk=img_id, listing=listing)
            img.order = new_order
            img.is_main = (new_order == 0)
            img.save(update_fields=['order', 'is_main'])
        except ListingImage.DoesNotExist:
            continue
    return JsonResponse({'success': True})




# ═══════════════════════ BROWSE + ADVANCED SEARCH ═══════════════════════



def _truck_part_groups():

    groups, total = [], 0

    for key, label in TRUCK_PART_CATEGORIES:

        items = list(Equipment.objects.filter(category=key).order_by('name'))

        if items:

            groups.append({'key': key, 'label': label, 'items': items})

            total += len(items)

    return groups, total





def _truck_country_choices():

    from apps.listings.views import COUNTRY_FLAGS as _flag

    all_c = list(Listing.COUNTRY_CHOICES)

    us = [c for c in all_c if c[0] == 'US']

    rest = sorted([c for c in all_c if c[0] != 'US'], key=lambda x: x[1])

    return [(code, f"{_flag.get(code, '🌍')} {name}") for code, name in (us + rest)]





def _tp_clean_list(values):

    return [v for v in values if v not in (None, '')]





def truck_parts_browse(request):

    # Sugadintos skaitinės reikšmės (?price_min=abc) tyliai išmetamos.

    request.GET = sanitize_search_params(request.GET)

    from django.db.models import Q

    from django.utils import timezone

    from datetime import timedelta



    qs = (

        Listing.objects

        .filter(

            vehicle_type__slug='parts',

            subcategory__slug=TRUCK_FOR_PARTS_SUBCATEGORY_SLUG,

            status='active',

        )

        .select_related('truck_brand', 'fuel_type')

        .prefetch_related('images')

    )

    G = request.GET



    part_types = _tp_clean_list(G.getlist('part_types'))

    if part_types:

        # related_name yra equipment_items — „listingequipment" metė FieldError (500).
        qs = qs.filter(equipment_items__equipment_id__in=part_types).distinct()



    brand_id = _int_or_none(G.get('truck_brand'))

    if brand_id:

        qs = qs.filter(truck_brand_id=brand_id)



    truck_types = _tp_clean_list(G.getlist('truck_type'))

    if truck_types:

        qs = qs.filter(truck_type__in=truck_types)



    model_q = (G.get('truck_model_text', '') or '').strip()

    if model_q:

        qs = qs.filter(truck_model_text__icontains=model_q)



    conditions = _tp_clean_list(G.getlist('condition'))

    if conditions:

        qs = qs.filter(condition__in=conditions)



    fuel_id = _int_or_none(G.get('fuel_type'))

    if fuel_id:

        qs = qs.filter(fuel_type_id=fuel_id)



    year_min = _int_or_none(G.get('year_min'))

    year_max = _int_or_none(G.get('year_max'))

    if year_min is not None:

        qs = qs.filter(year__gte=year_min)

    if year_max is not None:

        qs = qs.filter(year__lte=year_max)



    p_min = _int_or_none(G.get('power_min'))

    p_max = _int_or_none(G.get('power_max'))

    if p_min is not None:

        qs = qs.filter(power__gte=p_min)

    if p_max is not None:

        qs = qs.filter(power__lte=p_max)



    price_min = _int_or_none(G.get('price_min'))

    price_max = _int_or_none(G.get('price_max'))

    if price_min is not None:

        qs = qs.filter(price__gte=price_min)

    if price_max is not None:

        qs = qs.filter(price__lte=price_max)



    country = G.get('country_filter', '')

    if country:

        qs = qs.filter(country=country)

    state = G.get('state_filter', '')

    if state:

        qs = qs.filter(state=state)

    city = (G.get('city', '') or '').strip()

    if city:

        qs = qs.filter(city__icontains=city)



    posted = _int_or_none(G.get('posted_within'))

    if posted:

        qs = qs.filter(created_at__gte=timezone.now() - timedelta(days=posted))



    q = (G.get('part_query', '') or '').strip()

    if q:

        qs = qs.filter(Q(title__icontains=q) | Q(oem_code__icontains=q))



    qs = qs.order_by('-created_at')



    part_groups, total_pt = _truck_part_groups()

    current_year = timezone.now().year



    context = {

        'listings': qs,

        'total_count': qs.count(),

        'truck_brands': TruckBrand.objects.all().order_by('name'),

        'truck_type_choices': Listing._meta.get_field('truck_type').choices,

        'fuel_types': FuelType.objects.all().order_by('name'),

        'condition_choices': Listing.CONDITION_CHOICES,

        'part_groups': part_groups,

        'part_types_total': total_pt,

        'country_choices': _truck_country_choices(),

        'us_states': Listing.US_STATE_CHOICES,

        'years': list(range(current_year + 1, 1949, -1)),

        'sel_part_types': [str(x) for x in part_types],

        'sel_conditions': conditions,

        'sel_truck_types': truck_types,

    }

    return render(request, 'listings/truck_parts_browse.html', context)





def truck_parts_advanced_search(request):

    from django.utils import timezone

    G = request.GET

    part_groups, total_pt = _truck_part_groups()

    current_year = timezone.now().year

    context = {

        'truck_brands': TruckBrand.objects.all().order_by('name'),

        'truck_type_choices': Listing._meta.get_field('truck_type').choices,

        'fuel_types': FuelType.objects.all().order_by('name'),

        'condition_choices': Listing.CONDITION_CHOICES,

        'part_groups': part_groups,

        'part_types_total': total_pt,

        'country_choices': _truck_country_choices(),

        'us_states': Listing.US_STATE_CHOICES,

        'years': list(range(current_year + 1, 1949, -1)),

        'sel_part_types': [v for v in G.getlist('part_types') if v],

        'sel_conditions': [v for v in G.getlist('condition') if v],

        'sel_truck_types': [v for v in G.getlist('truck_type') if v],

    }

    return render(request, 'listings/truck_parts_advanced.html', context)

