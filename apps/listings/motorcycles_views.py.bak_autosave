"""
Motorcycle listing creation - single-page flow with AUTOSAVE (like autoplius.lt).

Note: 'Other' brand and 'Other' model are always sorted FIRST in all dropdowns,
so users can easily find the catch-all option when their specific brand/model
is not in the list.
"""
import os
import json
from itertools import groupby
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.db.models import Count, Q, Case, When, IntegerField, Value
from django.db.models.functions import Greatest, Coalesce, Lower
from datetime import date, timedelta

from .models import (
    Listing,
    ListingImage,
    ListingEquipment,
    Equipment,
    VehicleType,
    SubCategory,
    MotorcycleBrand,
    MotorcycleModel,
    FuelType,
    Transmission,
    SavedListing,
)


# ═══════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════

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


def _build_listing_title(brand, model, year):
    parts = []
    if brand:
        parts.append(brand.name)
    if model:
        parts.append(model.name)
    if year:
        parts.append(str(year))
    title = ' '.join(parts).strip()
    return title or 'Untitled draft'


def _moto_brands_qs():
    """All motorcycle brands ordered with 'Other' first, then alphabetical."""
    return MotorcycleBrand.objects.annotate(
        is_other=Case(
            When(name='Other', then=0),
            default=1,
            output_field=IntegerField(),
        )
    ).order_by('is_other', Lower('name'))


def _moto_models_qs(brand_id=None):
    """Motorcycle models for a brand, ordered with 'Other' first."""
    qs = MotorcycleModel.objects.all()
    if brand_id:
        qs = qs.filter(brand_id=brand_id)
    return qs.annotate(
        is_other=Case(
            When(name='Other', then=0),
            default=1,
            output_field=IntegerField(),
        )
    ).order_by('is_other', Lower('name'))


# ═══════════════════════════════════════════════════════════
# AJAX
# ═══════════════════════════════════════════════════════════

def get_motorcycle_brands_ajax(request):
    """Returns all motorcycle brands. 'Other' is always first."""
    brands = _moto_brands_qs().values('id', 'name')
    return JsonResponse(list(brands), safe=False)


def get_motorcycle_models_ajax(request):
    """Returns models for a brand. 'Other' is always first."""
    brand_id = request.GET.get('brand_id')
    if not brand_id:
        return JsonResponse([], safe=False)
    models = _moto_models_qs(brand_id=brand_id).values('id', 'name')
    return JsonResponse(list(models), safe=False)


# ═══════════════════════════════════════════════════════════
# CONTEXT BUILDER (CREATE FORM)
# ═══════════════════════════════════════════════════════════

def _build_context(request, submitted=None, errors=None, draft_id=None):
    try:
        motorcycle_type_choices = Listing.MOTORCYCLE_TYPE_CHOICES
    except AttributeError:
        motorcycle_type_choices = []
    try:
        cooling_type_choices = Listing.COOLING_TYPE_CHOICES
    except AttributeError:
        cooling_type_choices = []
    try:
        moto_engine_type_choices = Listing.MOTO_ENGINE_TYPE_CHOICES
    except AttributeError:
        moto_engine_type_choices = []
    try:
        condition_choices = Listing.CONDITION_CHOICES
    except AttributeError:
        condition_choices = [('new', 'New'), ('used', 'Used')]
    try:
        color_choices = Listing.COLOR_CHOICES
    except AttributeError:
        color_choices = []
    try:
        defect_choices = Listing.DEFECT_CHOICES
    except AttributeError:
        defect_choices = [('none', 'No defects')]
    try:
        euro_standard_choices = Listing.EURO_STANDARD_CHOICES
    except AttributeError:
        euro_standard_choices = []
    try:
        country_choices = Listing.COUNTRY_CHOICES
    except AttributeError:
        country_choices = [('US', 'United States')]
    try:
        us_states = Listing.US_STATE_CHOICES
    except AttributeError:
        us_states = []

    return {
        'motorcycle_brands': _moto_brands_qs(),
        'fuel_types': FuelType.objects.all().order_by('name'),
        'transmissions': Transmission.objects.all().order_by('name'),
        'years': list(range(2026, 1949, -1)),
        'months': list(range(1, 13)),
        'motorcycle_type_choices': motorcycle_type_choices,
        'cooling_type_choices': cooling_type_choices,
        'moto_engine_type_choices': moto_engine_type_choices,
        'condition_choices': condition_choices,
        'color_choices': color_choices,
        'defect_choices': defect_choices,
        'euro_standard_choices': euro_standard_choices,
        'country_choices': country_choices,
        'us_states': us_states,
        'submitted': submitted or {},
        'errors': errors or [],
        'draft_id': draft_id,
    }


# ═══════════════════════════════════════════════════════════
# CREATE FORM VIEW
# ═══════════════════════════════════════════════════════════

@login_required
def motorcycle_listing_create(request):
    if request.method == 'POST':
        return _handle_post(request)

    draft_id = request.session.get('active_moto_draft_id')
    submitted = {}

    if draft_id:
        try:
            draft = Listing.objects.get(
                pk=draft_id,
                seller=request.user,
                status='draft',
            )
            submitted = _draft_to_submitted(draft)
        except Listing.DoesNotExist:
            del request.session['active_moto_draft_id']
            request.session.modified = True
            draft_id = None

    return render(
        request,
        'listings/motorcycle_create.html',
        _build_context(request, submitted=submitted, draft_id=draft_id),
    )


def _draft_to_submitted(draft):
    return {
        'motorcycle_brand': str(draft.motorcycle_brand_id) if draft.motorcycle_brand_id else '',
        'motorcycle_model': str(draft.motorcycle_model_id) if draft.motorcycle_model_id else '',
        'year': str(draft.year) if draft.year else '',
        'month': str(draft.first_registration.month) if draft.first_registration else '',
        'vin': draft.vin or '',
        'motorcycle_type': draft.motorcycle_type or '',
        'cooling_type': draft.cooling_type or '',
        'moto_engine_type': draft.moto_engine_type or '',
        'engine_capacity_cc': str(draft.engine_capacity_cc) if draft.engine_capacity_cc else '',
        'power': str(draft.power) if draft.power else '',
        'mileage': str(draft.mileage) if draft.mileage else '',
        'condition': draft.condition or '',
        'color': draft.color or '',
        'defects': draft.defects or '',
        'fuel_type': str(draft.fuel_type_id) if draft.fuel_type_id else '',
        'transmission': str(draft.transmission_id) if draft.transmission_id else '',
        'curb_weight': str(draft.curb_weight) if draft.curb_weight else '',
        'euro_standard': draft.euro_standard or '',
        'origin_country': draft.origin_country or '',
        'technical_inspection_month': str(draft.technical_inspection_month) if draft.technical_inspection_month else '',
        'technical_inspection_year': str(draft.technical_inspection_year) if draft.technical_inspection_year else '',
        'price': str(int(draft.price)) if draft.price else '',
        'negotiable': 'on' if draft.negotiable else '',
        'description': draft.description or '',
        'video_url': draft.video_url or '',
        'country': draft.country or 'US',
        'state': draft.state or '',
        'city': draft.city if draft.city and draft.city != '—' else '',
        'postal_code': draft.postal_code or '',
        'address': draft.address or '',
        'hide_exact_address': 'on' if draft.hide_exact_address else '',
    }


def _build_fields_from_post(request, POST):
    brand_id = _int_or_none(POST.get('motorcycle_brand'))
    model_id = _int_or_none(POST.get('motorcycle_model'))
    year = _int_or_none(POST.get('year'))
    month = _int_or_none(POST.get('month'))
    price = _float_or_none(POST.get('price'))

    brand = None
    if brand_id:
        try:
            brand = MotorcycleBrand.objects.get(id=brand_id)
        except MotorcycleBrand.DoesNotExist:
            pass

    model = None
    if model_id:
        try:
            model = MotorcycleModel.objects.get(id=model_id)
        except MotorcycleModel.DoesNotExist:
            pass

    fuel_type_obj = None
    fuel_type_id = _int_or_none(POST.get('fuel_type'))
    if fuel_type_id:
        try:
            fuel_type_obj = FuelType.objects.get(id=fuel_type_id)
        except FuelType.DoesNotExist:
            pass

    transmission_obj = None
    transmission_id = _int_or_none(POST.get('transmission'))
    if transmission_id:
        try:
            transmission_obj = Transmission.objects.get(id=transmission_id)
        except Transmission.DoesNotExist:
            pass

    vehicle_type = VehicleType.objects.filter(slug='motorcycles').first()
    if not vehicle_type:
        return None

    first_registration = None
    if year and month:
        try:
            first_registration = date(year=year, month=month, day=1)
        except (ValueError, TypeError):
            pass

    country = POST.get('country', 'US')[:2]
    state = (POST.get('state', '') if country == 'US' else '')[:2]
    city = POST.get('city', '')

    from .views import get_coordinates_for_location
    if country == 'US' and state:
        state_label_dict = dict(getattr(Listing, 'US_STATE_CHOICES', []))
        state_label = state_label_dict.get(state, state)
        city_for_display = city if city else state_label
    else:
        city_for_display = city

    if not city_for_display:
        city_for_display = '—'

    lat, lng = get_coordinates_for_location(city_for_display, country)

    title = _build_listing_title(brand, model, year)

    fields = {
        'vehicle_type': vehicle_type,
        'motorcycle_brand': brand,
        'motorcycle_model': model,
        'title': title,
        'year': year or 2024,
        'first_registration': first_registration,
        'vin': POST.get('vin', ''),
        'video_url': POST.get('video_url', ''),
        'motorcycle_type': POST.get('motorcycle_type', ''),
        'cooling_type': POST.get('cooling_type', ''),
        'moto_engine_type': POST.get('moto_engine_type', ''),
        'engine_capacity_cc': _int_or_none(POST.get('engine_capacity_cc')),
        'power': _int_or_none(POST.get('power')),
        'mileage': _int_or_none(POST.get('mileage')) or 0,
        'condition': POST.get('condition') or 'used',
        'color': POST.get('color', ''),
        'defects': POST.get('defects') or 'none',
        'fuel_type': fuel_type_obj,
        'transmission': transmission_obj,
        'curb_weight': _int_or_none(POST.get('curb_weight')),
        'euro_standard': POST.get('euro_standard', ''),
        'origin_country': POST.get('origin_country', '')[:2],
        'technical_inspection_month': _int_or_none(POST.get('technical_inspection_month')),
        'technical_inspection_year': _int_or_none(POST.get('technical_inspection_year')),
        'price': price if price else 0,
        'negotiable': POST.get('negotiable') == 'on',
        'description': POST.get('description', ''),
        'country': country,
        'city': city_for_display,
        'postal_code': POST.get('postal_code', ''),
        'address': POST.get('address', ''),
        'hide_exact_address': POST.get('hide_exact_address') == 'on',
        'latitude': lat,
        'longitude': lng,
        'status': 'draft',
    }

    if hasattr(Listing, 'state'):
        fields['state'] = state

    return fields


def _save_draft_fields(request, POST, draft_id):
    fields = _build_fields_from_post(request, POST)
    if not fields:
        return None

    listing = None
    if draft_id:
        try:
            listing = Listing.objects.get(
                pk=draft_id,
                seller=request.user,
                status='draft',
            )
            for key, value in fields.items():
                setattr(listing, key, value)
            listing.save()
        except Listing.DoesNotExist:
            listing = None

    if listing is None:
        fields['seller'] = request.user
        listing = Listing.objects.create(**fields)

    return listing


@login_required
@require_POST
def save_motorcycle_draft_ajax(request):
    POST = request.POST
    draft_id = _int_or_none(POST.get('draft_id'))

    vehicle_type = VehicleType.objects.filter(slug='motorcycles').first()
    if not vehicle_type:
        return JsonResponse({
            'success': False,
            'error': 'Motorcycles category not configured in database.',
        }, status=400)

    try:
        listing = _save_draft_fields(request, POST, draft_id)
    except Exception as e:
        print(f"[autosave] error: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e),
        }, status=500)

    if not listing:
        return JsonResponse({
            'success': False,
            'error': 'Failed to save draft.',
        }, status=500)

    request.session['active_moto_draft_id'] = listing.pk
    request.session.modified = True

    return JsonResponse({
        'success': True,
        'listing_id': listing.pk,
        'saved_at': timezone.now().isoformat(),
    })


@login_required
@require_POST
def delete_draft_ajax(request, pk):
    try:
        listing = Listing.objects.get(
            pk=pk,
            seller=request.user,
            status='draft',
        )
        listing_id = listing.pk
        listing.delete()

        if request.session.get('active_moto_draft_id') == listing_id:
            del request.session['active_moto_draft_id']
            request.session.modified = True

        return JsonResponse({'success': True})
    except Listing.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Draft not found'
        }, status=404)


def _handle_post(request):
    POST = request.POST
    FILES = request.FILES

    draft_id = _int_or_none(POST.get('draft_id'))

    submitted = {
        'motorcycle_brand': POST.get('motorcycle_brand', ''),
        'motorcycle_model': POST.get('motorcycle_model', ''),
        'year': POST.get('year', ''),
        'month': POST.get('month', ''),
        'vin': POST.get('vin', ''),
        'motorcycle_type': POST.get('motorcycle_type', ''),
        'cooling_type': POST.get('cooling_type', ''),
        'moto_engine_type': POST.get('moto_engine_type', ''),
        'engine_capacity_cc': POST.get('engine_capacity_cc', ''),
        'power': POST.get('power', ''),
        'mileage': POST.get('mileage', ''),
        'condition': POST.get('condition', ''),
        'color': POST.get('color', ''),
        'defects': POST.get('defects', ''),
        'fuel_type': POST.get('fuel_type', ''),
        'transmission': POST.get('transmission', ''),
        'curb_weight': POST.get('curb_weight', ''),
        'euro_standard': POST.get('euro_standard', ''),
        'origin_country': POST.get('origin_country', ''),
        'technical_inspection_month': POST.get('technical_inspection_month', ''),
        'technical_inspection_year': POST.get('technical_inspection_year', ''),
        'price': POST.get('price', ''),
        'negotiable': POST.get('negotiable', ''),
        'description': POST.get('description', ''),
        'video_url': POST.get('video_url', ''),
        'country': POST.get('country', ''),
        'state': POST.get('state', ''),
        'city': POST.get('city', ''),
        'postal_code': POST.get('postal_code', ''),
        'address': POST.get('address', ''),
        'hide_exact_address': POST.get('hide_exact_address', ''),
    }

    errors = []
    brand_id = _int_or_none(POST.get('motorcycle_brand'))
    year = _int_or_none(POST.get('year'))
    price = _float_or_none(POST.get('price'))

    if not brand_id:
        errors.append('Brand is required.')
    if not year:
        errors.append('Year is required.')
    if not price or price <= 0:
        errors.append('Valid price is required.')

    if errors:
        return render(
            request,
            'listings/motorcycle_create.html',
            _build_context(request, submitted=submitted, errors=errors, draft_id=draft_id),
        )

    try:
        listing = _save_draft_fields(request, POST, draft_id)
    except Exception as e:
        errors.append(f'Failed to save listing: {e}')
        return render(
            request,
            'listings/motorcycle_create.html',
            _build_context(request, submitted=submitted, errors=errors, draft_id=draft_id),
        )

    if not listing:
        errors.append('Failed to save listing.')
        return render(
            request,
            'listings/motorcycle_create.html',
            _build_context(request, submitted=submitted, errors=errors, draft_id=draft_id),
        )

    images = FILES.getlist('images')
    existing_count = listing.images.count()
    for i, image in enumerate(images[:40]):
        try:
            ListingImage.objects.create(
                listing=listing,
                image=image,
                is_main=(existing_count == 0 and i == 0),
                order=existing_count + i,
            )
        except Exception as e:
            print(f"[motorcycle] image upload failed: {e}")

    if 'active_moto_draft_id' in request.session:
        del request.session['active_moto_draft_id']
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


# ═══════════════════════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════════════════
# NAUJI VIEW'AI: Browse + Advanced Search MOTOCIKLAMS
# ═══════════════════════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════════════════


NEW_LISTING_DAYS = 3


def _moto_public_listings_qs(request_user=None):
    """Active + recently sold motorcycle listings (admin sees shadow-banned)."""
    now = timezone.now()
    sold_cutoff = now - timedelta(days=Listing.SOLD_DISPLAY_DAYS)

    qs = Listing.objects.filter(
        Q(status='active') |
        Q(status='sold', sold_at__gte=sold_cutoff)
    ).filter(vehicle_type__slug='motorcycles')

    if request_user and request_user.is_authenticated and request_user.is_superuser:
        return qs
    return qs.filter(is_shadow_banned=False)


def _moto_track_impressions(request, listings):
    """Track impressions via existing helper in views.py."""
    from .views import _track_listing_impressions
    _track_listing_impressions(request, listings)


# ─── motorcycles_list — browse page (delegate from views.listing_list) ───

def motorcycles_list(request):
    """
    Motorcycle browse page.
    Called from views.listing_list() when ?category=motorcycles.
    Renders 'listings/motorcycles_list.html' with motorcycle-specific filters.
    """
    _now = timezone.now()
    _three_days_ago = _now - timedelta(days=NEW_LISTING_DAYS)

    listings = _moto_public_listings_qs(request.user).select_related(
        'motorcycle_brand', 'motorcycle_model', 'vehicle_type'
    ).annotate(
        effective_date=Greatest(
            'created_at',
            Coalesce('last_boosted_at', 'created_at'),
        ),
    ).annotate(
        sort_priority=Case(
            When(star_level=2, star_expires_at__gt=_now, then=Value(500)),
            When(star_level=1, star_expires_at__gt=_now, then=Value(400)),
            When(effective_date__gt=_three_days_ago, then=Value(200)),
            default=Value(100),
            output_field=IntegerField(),
        )
    ).order_by('-sort_priority', '-effective_date')

    # Brand counts
    brand_counts = {
        item['motorcycle_brand_id']: item['count']
        for item in _moto_public_listings_qs(request.user)
            .values('motorcycle_brand_id').annotate(count=Count('id'))
    }
    # Brands ordered with 'Other' first, then alphabetical
    brands_qs = _moto_brands_qs()
    motorcycle_brands = [
        {'id': b.id, 'name': b.name, 'count': brand_counts.get(b.id, 0)}
        for b in brands_qs
    ]

    years = list(range(2026, 1949, -1))

    # Filters
    f = request.GET
    motorcycle_brand_filter = f.get('motorcycle_brand')
    motorcycle_model_filter = f.get('motorcycle_model')
    motorcycle_type_filter = [v for v in f.getlist('motorcycle_type') if v]
    cooling_type_filter = [v for v in f.getlist('cooling_type') if v]
    price_min = f.get('price_min')
    price_max = f.get('price_max')
    year_min = f.get('year_min')
    year_max = f.get('year_max')
    engine_cc_min = f.get('engine_cc_min')
    engine_cc_max = f.get('engine_cc_max')
    search_query = f.get('search', '')
    country_filter = f.get('country_filter', '')
    state_filter = f.get('state_filter', '')

    if search_query:
        listings = listings.filter(title__icontains=search_query)
    if motorcycle_brand_filter:
        listings = listings.filter(motorcycle_brand_id=motorcycle_brand_filter)
    if motorcycle_model_filter:
        listings = listings.filter(motorcycle_model_id=motorcycle_model_filter)
    if motorcycle_type_filter:
        listings = listings.filter(motorcycle_type__in=motorcycle_type_filter)
    if cooling_type_filter:
        listings = listings.filter(cooling_type__in=cooling_type_filter)
    if price_min:
        listings = listings.filter(price__gte=price_min)
    if price_max:
        listings = listings.filter(price__lte=price_max)
    if year_min:
        listings = listings.filter(year__gte=year_min)
    if year_max:
        listings = listings.filter(year__lte=year_max)
    if engine_cc_min:
        listings = listings.filter(engine_capacity_cc__gte=engine_cc_min)
    if engine_cc_max:
        listings = listings.filter(engine_capacity_cc__lte=engine_cc_max)
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
    _moto_track_impressions(request, listings_list)

    new_listing_ids = [
        l.id for l in listings_list
        if l.created_at >= timezone.now() - timedelta(days=NEW_LISTING_DAYS)
    ]

    try:
        motorcycle_type_choices = Listing.MOTORCYCLE_TYPE_CHOICES
    except AttributeError:
        motorcycle_type_choices = []
    try:
        cooling_type_choices = Listing.COOLING_TYPE_CHOICES
    except AttributeError:
        cooling_type_choices = []

    context = {
        'listings': listings_list,
        'motorcycle_brands': motorcycle_brands,
        'years': years,
        'motorcycle_type_choices': motorcycle_type_choices,
        'cooling_type_choices': cooling_type_choices,
        'selected_motorcycle_types': motorcycle_type_filter,
        'selected_cooling_types': cooling_type_filter,
        'search_query': search_query,
        'total_count': listings.count(),
        'selected_category': 'motorcycles',
        'saved_ids': saved_ids,
        'new_listing_ids': new_listing_ids,
        'us_states': Listing.US_STATE_CHOICES,
        'selected_country': country_filter,
        'selected_state': state_filter,
    }
    return render(request, 'listings/motorcycles_list.html', context)


# ─── motorcycles_advanced_search — advanced search page ───

def motorcycles_advanced_search(request):
    """Full advanced search for motorcycles."""
    listings = _moto_public_listings_qs(request.user).select_related(
        'motorcycle_brand', 'motorcycle_model', 'vehicle_type'
    )

    years = list(range(2026, 1949, -1))
    # Brands ordered with 'Other' first, then alphabetical
    motorcycle_brands = _moto_brands_qs()

    f = request.GET
    search_query = f.get('search', '')
    price_min = f.get('price_min', '')
    price_max = f.get('price_max', '')
    year_min = f.get('year_min', '')
    year_max = f.get('year_max', '')
    mileage_min = f.get('mileage_min', '')
    mileage_max = f.get('mileage_max', '')
    engine_cc_min = f.get('engine_cc_min', '')
    engine_cc_max = f.get('engine_cc_max', '')
    power_min = f.get('power_min', '')
    power_max = f.get('power_max', '')
    motorcycle_type_filter = f.get('motorcycle_type', '')
    moto_transmission_filter = f.get('moto_transmission', '')
    moto_engine_type_filter = f.get('moto_engine_type', '')
    moto_fuel_type_filter = f.get('moto_fuel_type', '')
    cooling_type_filter = f.get('cooling_type', '')
    registration_type_filter = f.get('registration_type', '')
    euro_standard_filter = f.get('euro_standard', '')
    color_filter = f.get('color', '')
    defects_filter = f.get('defects', '')
    first_reg_country = f.get('first_reg_country', '')
    state_filter = f.get('state_filter', '')
    country_filter = f.get('country_filter', '')
    cond_used = f.get('cond_used', '')
    cond_new = f.get('cond_new', '')
    moto_eq = f.getlist('moto_eq')
    battery_min = f.get('battery_min', '')
    battery_max = f.get('battery_max', '')
    electric_range_min = f.get('electric_range_min', '')
    electric_range_max = f.get('electric_range_max', '')

    if search_query:
        listings = listings.filter(title__icontains=search_query)

    # Brand/model multi-select via 'pair' parameter
    pairs = request.GET.getlist('pair')
    if pairs:
        q = Q()
        for pair in pairs:
            parts = pair.split('|')
            if len(parts) == 4:
                bid, bname, mid, mname = parts
                if mid:
                    q |= Q(motorcycle_brand_id=bid, motorcycle_model_id=mid)
                else:
                    q |= Q(motorcycle_brand_id=bid)
        if q:
            listings = listings.filter(q)

    if price_min:
        listings = listings.filter(price__gte=price_min)
    if price_max:
        listings = listings.filter(price__lte=price_max)
    if year_min:
        listings = listings.filter(year__gte=year_min)
    if year_max:
        listings = listings.filter(year__lte=year_max)
    if mileage_min:
        listings = listings.filter(mileage__gte=mileage_min)
    if mileage_max:
        listings = listings.filter(mileage__lte=mileage_max)
    if engine_cc_min:
        listings = listings.filter(engine_capacity_cc__gte=engine_cc_min)
    if engine_cc_max:
        listings = listings.filter(engine_capacity_cc__lte=engine_cc_max)
    if power_min:
        listings = listings.filter(power__gte=power_min)
    if power_max:
        listings = listings.filter(power__lte=power_max)
    if motorcycle_type_filter:
        listings = listings.filter(motorcycle_type=motorcycle_type_filter)
    if cooling_type_filter:
        listings = listings.filter(cooling_type=cooling_type_filter)
    if moto_engine_type_filter:
        listings = listings.filter(moto_engine_type=moto_engine_type_filter)
    if euro_standard_filter:
        listings = listings.filter(euro_standard=euro_standard_filter)
    if color_filter:
        listings = listings.filter(color=color_filter)
    if defects_filter:
        listings = listings.filter(defects=defects_filter)

    # Optional moto-specific filters (only if model has them)
    if moto_transmission_filter and hasattr(Listing, 'moto_transmission'):
        listings = listings.filter(moto_transmission=moto_transmission_filter)
    if moto_fuel_type_filter and hasattr(Listing, 'moto_fuel_type'):
        listings = listings.filter(moto_fuel_type=moto_fuel_type_filter)
    if registration_type_filter and hasattr(Listing, 'registration_type'):
        listings = listings.filter(registration_type=registration_type_filter)
    if first_reg_country and hasattr(Listing, 'origin_country'):
        listings = listings.filter(origin_country=first_reg_country)
    if battery_min and hasattr(Listing, 'battery_capacity_kwh'):
        listings = listings.filter(battery_capacity_kwh__gte=battery_min)
    if battery_max and hasattr(Listing, 'battery_capacity_kwh'):
        listings = listings.filter(battery_capacity_kwh__lte=battery_max)
    if electric_range_min and hasattr(Listing, 'electric_range_km'):
        listings = listings.filter(electric_range_km__gte=electric_range_min)
    if electric_range_max and hasattr(Listing, 'electric_range_km'):
        listings = listings.filter(electric_range_km__lte=electric_range_max)

    # Condition checkboxes
    if cond_used and not cond_new:
        listings = listings.filter(condition='used')
    elif cond_new and not cond_used:
        listings = listings.filter(condition='new')

    if state_filter:
        listings = listings.filter(country='US', state=state_filter)
    elif country_filter:
        listings = listings.filter(country=country_filter)

    saved_ids = []
    if request.user.is_authenticated:
        saved_ids = list(SavedListing.objects.filter(
            user=request.user
        ).values_list('listing_id', flat=True))

    _now = timezone.now()
    _three_days_ago = _now - timedelta(days=NEW_LISTING_DAYS)

    sorted_listings = listings.annotate(
        effective_date=Greatest(
            'created_at',
            Coalesce('last_boosted_at', 'created_at'),
        ),
    ).annotate(
        sort_priority=Case(
            When(star_level=2, star_expires_at__gt=_now, then=Value(500)),
            When(star_level=1, star_expires_at__gt=_now, then=Value(400)),
            When(effective_date__gt=_three_days_ago, then=Value(200)),
            default=Value(100),
            output_field=IntegerField(),
        )
    ).order_by('-sort_priority', '-effective_date')

    sorted_listings_all = list(sorted_listings[:60])
    _moto_track_impressions(request, sorted_listings_all)

    new_listing_ids = [
        l.id for l in sorted_listings_all
        if l.created_at >= timezone.now() - timedelta(days=NEW_LISTING_DAYS)
    ]

    # Choices
    try:
        motorcycle_type_choices = Listing.MOTORCYCLE_TYPE_CHOICES
    except AttributeError:
        motorcycle_type_choices = []
    try:
        cooling_type_choices = Listing.COOLING_TYPE_CHOICES
    except AttributeError:
        cooling_type_choices = []
    try:
        moto_engine_type_choices = Listing.MOTO_ENGINE_TYPE_CHOICES
    except AttributeError:
        moto_engine_type_choices = []

    moto_transmission_choices = getattr(Listing, 'MOTO_TRANSMISSION_CHOICES', [
        ('manual', 'Manual'),
        ('automatic', 'Automatic'),
        ('semi_auto', 'Semi-Automatic'),
        ('cvt', 'CVT'),
    ])
    moto_fuel_type_choices = getattr(Listing, 'MOTO_FUEL_TYPE_CHOICES', [
        ('petrol', 'Petrol'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
    ])
    registration_type_choices = getattr(Listing, 'REGISTRATION_TYPE_CHOICES', [
        ('regular', 'Regular'),
        ('historic', 'Historic'),
        ('competition', 'Competition / Track-only'),
    ])

    try:
        color_choices = Listing.COLOR_CHOICES
    except AttributeError:
        color_choices = []
    try:
        defect_choices = Listing.DEFECT_CHOICES
    except AttributeError:
        defect_choices = []
    try:
        euro_standard_choices = Listing.EURO_STANDARD_CHOICES
    except AttributeError:
        euro_standard_choices = []
    try:
        country_choices = Listing.COUNTRY_CHOICES
    except AttributeError:
        country_choices = []

    context = {
        'listings': sorted_listings_all,
        'total_count': listings.count(),
        'motorcycle_brands': motorcycle_brands,
        'years': years,
        'motorcycle_type_choices': motorcycle_type_choices,
        'cooling_type_choices': cooling_type_choices,
        'moto_engine_type_choices': moto_engine_type_choices,
        'moto_transmission_choices': moto_transmission_choices,
        'moto_fuel_type_choices': moto_fuel_type_choices,
        'registration_type_choices': registration_type_choices,
        'color_choices': color_choices,
        'defect_choices': defect_choices,
        'euro_standard_choices': euro_standard_choices,
        'country_choices': country_choices,
        'us_states': Listing.US_STATE_CHOICES,
        'saved_ids': saved_ids,
        'new_listing_ids': new_listing_ids,
        'f': request.GET,
        'selected_moto_eq': moto_eq,
    }
    return render(request, 'listings/motorcycles_advanced_search.html', context)