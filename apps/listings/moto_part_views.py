from .search_params import sanitize as sanitize_search_params
"""
Single moto part srautas — autogidas.lt "Motociklų dalys" 1:1 forma.
URL: /create/moto-part/
"""

from django.utils.translation import gettext_lazy as _
from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q

from apps.listings.image_validation import split_valid_images
from apps.listings.models import (
    Listing, ListingImage, VehicleType, SubCategory,
    MotorcycleBrand, MotorcycleModel, Equipment, ListingEquipment,
)

# ─── "Dalies tipas" grupės (Equipment kategorijos) — rodymo tvarka + label ───
MOTO_PART_CATEGORIES = [
    ('moto_trim', _('Trim / Body parts')),
    ('moto_electrical', _('Electrical system parts')),
    ('moto_cooling', _('Engine cooling parts')),
    ('moto_engine', _('Engine parts')),
    ('moto_chassis', _('Chassis & transmission parts')),
]

CONDITION_CHOICES = [
    ('new', _('New')),
    ('used', _('Used')),
    ('refurbished', _('Refurbished')),
    ('damaged', _('Damaged')),
]


def _int_or_none(v):
    if v in (None, ''):
        return None
    try:
        return int(v)
    except (ValueError, TypeError):
        return None


def _float_or_none(v):
    if v in (None, ''):
        return None
    try:
        return float(v)
    except (ValueError, TypeError):
        return None


@login_required
def moto_part_create(request):

    from django.shortcuts import get_object_or_404

    edit_pk = _int_or_none(request.GET.get('edit') or request.POST.get('edit'))

    edit_listing = get_object_or_404(Listing, pk=edit_pk, seller=request.user) if edit_pk else None
    if request.method == 'POST':
        return _handle_post(request, edit_listing)
    return _render_form(request, listing=edit_listing)


def _handle_post(request, edit_listing=None):
    errors = []

    title = (request.POST.get('title', '') or '').strip()
    if not title:
        errors.append('Part name is required')

    condition = request.POST.get('condition', '')
    if condition not in ('new', 'used', 'refurbished', 'damaged'):
        errors.append('Condition is required')

    brand_id = _int_or_none(request.POST.get('motorcycle_brand'))
    if not brand_id:
        errors.append('Brand is required')

    price = _float_or_none(request.POST.get('price'))
    if price is None or price <= 0:
        errors.append('Price is required')

    country = request.POST.get('country', 'US')
    state = request.POST.get('state', '') if country == 'US' else ''
    city = (request.POST.get('city', '') or '').strip()
    if country == 'US' and not state:
        errors.append('State is required for US')
    if country != 'US' and not city:
        errors.append('City is required')

    phone = (request.POST.get('phone', '') or '').strip()
    if not phone:
        errors.append('Phone is required')

    if not edit_listing and not request.POST.get('agree_terms'):
        errors.append('You must agree to the terms')

    if errors:
        for e in errors:
            messages.error(request, e)
        return _render_form(request, listing=edit_listing, errors=errors)

    try:
        parts_vt = VehicleType.objects.get(slug='parts')
    except VehicleType.DoesNotExist:
        messages.error(request, 'Parts vehicle type not configured.')
        return _render_form(request, errors=['Parts vehicle type not configured.'])

    if edit_listing:

        listing = edit_listing

        listing.title = title[:200]

        listing.oem_code = (request.POST.get('oem_code', '') or '').strip()[:50]

        listing.condition = condition

        listing.price = price

        listing.negotiable = request.POST.get('negotiable') == 'on'

        listing.description = request.POST.get('description', '') or ''

        listing.country = country

        listing.state = state

        listing.city = city or '—'

        listing.postal_code = request.POST.get('postal_code', '') or ''

        listing.address = request.POST.get('address', '') or ''

        _yr = _int_or_none(request.POST.get('year'))

        if _yr:

            listing.year = _yr

        try:

            listing.motorcycle_brand = MotorcycleBrand.objects.get(pk=brand_id)

        except MotorcycleBrand.DoesNotExist:

            pass

        _mid = _int_or_none(request.POST.get('motorcycle_model'))

        if _mid:

            try:

                listing.motorcycle_model = MotorcycleModel.objects.get(pk=_mid)

            except MotorcycleModel.DoesNotExist:

                pass

        listing.motorcycle_type = request.POST.get('motorcycle_type', '') or ''

        _cc = _float_or_none(request.POST.get('engine_capacity'))

        if _cc:

            listing.engine_capacity = _cc

        if hasattr(request.user, 'profile'):

            request.user.profile.phone_number = phone

            request.user.profile.save(update_fields=['phone_number'])

        listing.save()

        ListingEquipment.objects.filter(listing=listing).delete()

        for eid in request.POST.getlist('part_types'):

            try:

                ListingEquipment.objects.create(listing=listing, equipment_id=int(eid))

            except (ValueError, TypeError):

                pass

        _existing = listing.images.count()

        _images, _image_errors = split_valid_images(request.FILES.getlist('images')[:36])

        for _err in _image_errors:

            messages.error(request, _err)

        for i, image in enumerate(_images):

            try:

                ListingImage.objects.create(listing=listing, image=image, is_main=(_existing == 0 and i == 0), order=_existing + i)

            except Exception as e:

                print(f"[moto_part] image upload failed: {e}")

        messages.success(request, 'Listing updated successfully.')

        return redirect('my_listings')



    sub = SubCategory.objects.filter(slug='single-moto-part').first()

    listing = Listing(
        seller=request.user,
        vehicle_type=parts_vt,
        subcategory=sub,
        title=title[:200],
        oem_code=(request.POST.get('oem_code', '') or '').strip()[:50],
        condition=condition,
        price=price,
        negotiable=request.POST.get('negotiable') == 'on',
        description=request.POST.get('description', '') or '',
        country=country,
        city=city or '—',
        postal_code=request.POST.get('postal_code', '') or '',
        address=request.POST.get('address', '') or '',
        year=_int_or_none(request.POST.get('year')) or date.today().year,
        mileage=0,
        status='draft',
    )
    listing.state = state

    # ─── Moto brand / model / type ───
    try:
        listing.motorcycle_brand = MotorcycleBrand.objects.get(pk=brand_id)
    except MotorcycleBrand.DoesNotExist:
        pass

    model_id = _int_or_none(request.POST.get('motorcycle_model'))
    if model_id:
        try:
            listing.motorcycle_model = MotorcycleModel.objects.get(pk=model_id)
        except MotorcycleModel.DoesNotExist:
            pass

    listing.motorcycle_type = request.POST.get('motorcycle_type', '') or ''

    # Darbinis tūris cm³ → engine_capacity (saugom cm³ reikšmę, pvz. 1300)
    cc = _float_or_none(request.POST.get('engine_capacity'))
    if cc:
        listing.engine_capacity = cc

    # Telefonas → user.profile
    if hasattr(request.user, 'profile'):
        request.user.profile.phone_number = phone
        request.user.profile.save(update_fields=['phone_number'])

    try:
        listing.save()
    except Exception as e:
        messages.error(request, f'Save failed: {str(e)[:200]}')
        return _render_form(request, errors=[str(e)])

    # ─── "Dalies tipas" checkbox'ai → ListingEquipment ───
    for eid in request.POST.getlist('part_types'):
        try:
            ListingEquipment.objects.create(listing=listing, equipment_id=int(eid))
        except (ValueError, TypeError):
            pass

    # ─── Nuotraukos (sinchroniškai su POST) ───
    images, _image_errors = split_valid_images(request.FILES.getlist('images'))
    for _err in _image_errors:
        messages.error(request, _err)
    for i, image in enumerate(images[:36]):
        try:
            ListingImage.objects.create(
                listing=listing,
                image=image,
                is_main=(i == 0),
                order=i,
            )
        except Exception as e:
            print(f"[moto_part] image upload failed: {e}")

    # Single part flow → planų puslapis
    return redirect('listing_select_plan', pk=listing.pk)


def _moto_part_form_data(request, listing):

    if request.method == 'POST':

        return request.POST

    if not listing:

        return {}

    _phone = ''

    if hasattr(request.user, 'profile') and request.user.profile.phone_number:

        _phone = request.user.profile.phone_number

    return {

        'title': listing.title or '',

        'oem_code': listing.oem_code or '',

        'condition': listing.condition or '',

        'price': str(int(listing.price)) if listing.price else '',

        'negotiable': 'on' if listing.negotiable else '',

        'description': listing.description or '',

        'country': listing.country or 'US',

        'state': getattr(listing, 'state', '') or '',

        'city': '' if listing.city == '—' else (listing.city or ''),

        'postal_code': listing.postal_code or '',

        'address': listing.address or '',

        'year': str(listing.year) if listing.year else '',

        'motorcycle_brand': str(listing.motorcycle_brand_id) if listing.motorcycle_brand_id else '',

        'motorcycle_model': str(listing.motorcycle_model_id) if listing.motorcycle_model_id else '',

        'motorcycle_type': listing.motorcycle_type or '',

        'engine_capacity': str(listing.engine_capacity) if listing.engine_capacity else '',

        'phone': _phone,

    }





def _render_form(request, listing=None, errors=None):
    user_phone = ''
    if hasattr(request.user, 'profile') and request.user.profile.phone_number:
        user_phone = request.user.profile.phone_number

    moto_brands = MotorcycleBrand.objects.all().order_by('name')

    current_year = timezone.now().year
    years = list(range(current_year + 1, 1949, -1))

    # ─── Dalies tipas grupės su items ───
    part_groups = []
    for cat_key, cat_label in MOTO_PART_CATEGORIES:
        items = list(Equipment.objects.filter(category=cat_key).order_by('name'))
        if items:
            part_groups.append({'key': cat_key, 'label': cat_label, 'items': items})

    # ─── Country choices su vėliavėlėmis (US pirmas, paskui EU pagal pavadinimą) ───
    from apps.listings.views import COUNTRY_FLAGS as _flag
    all_c = list(Listing.COUNTRY_CHOICES)
    us = [c for c in all_c if c[0] == 'US']
    rest = sorted([c for c in all_c if c[0] != 'US'], key=lambda x: x[1])
    country_choices = [
        (code, f"{_flag.get(code, '🌍')} {name}")
        for code, name in (us + rest)
    ]

    context = {
        'moto_brands': moto_brands,
        'motorcycle_type_choices': Listing._meta.get_field('motorcycle_type').choices,
        'condition_choices': CONDITION_CHOICES,
        'years': years,
        'part_groups': part_groups,
        'country_choices': country_choices,
        'us_states': Listing.US_STATE_CHOICES,
        'user_phone': user_phone,
        'user_email': request.user.email,
        'form_data': _moto_part_form_data(request, listing),

        'selected_part_types': ([str(i) for i in listing.equipment_items.values_list('equipment_id', flat=True)] if listing else []),

        'listing': listing,
        'is_edit_mode': bool(listing),

        'edit_listing_id': listing.pk if listing else '',
        'errors': errors or [],
    }
    return render(request, 'listings/moto_part_create.html', context)


# ═══════════════════ BROWSE + ADVANCED (/browse/moto-parts/) ═══════════════════

def moto_parts_browse(request):
    # Sugadintos skaitinės reikšmės (?price_min=abc) tyliai išmetamos.
    request.GET = sanitize_search_params(request.GET)
    def _clean(vs):
        return [v for v in vs if v not in (None, '')]

    qs = (Listing.objects
          .filter(vehicle_type__slug='parts', subcategory__slug='single-moto-part', status='active')
          .select_related('motorcycle_brand', 'motorcycle_model').prefetch_related('images'))
    G = request.GET

    pt = _clean(G.getlist('part_types'))
    if pt:
        qs = qs.filter(equipment_items__equipment_id__in=pt).distinct()

    if _int_or_none(G.get('motorcycle_brand')):
        qs = qs.filter(motorcycle_brand_id=_int_or_none(G.get('motorcycle_brand')))
    if _int_or_none(G.get('motorcycle_model')):
        qs = qs.filter(motorcycle_model_id=_int_or_none(G.get('motorcycle_model')))

    mt = _clean(G.getlist('motorcycle_type'))
    if mt:
        qs = qs.filter(motorcycle_type__in=mt)
    cond = _clean(G.getlist('condition'))
    if cond:
        qs = qs.filter(condition__in=cond)

    if _int_or_none(G.get('year_min')):
        qs = qs.filter(year__gte=_int_or_none(G.get('year_min')))
    if _int_or_none(G.get('year_max')):
        qs = qs.filter(year__lte=_int_or_none(G.get('year_max')))
    if _int_or_none(G.get('engine_min')):
        qs = qs.filter(engine_capacity__gte=_int_or_none(G.get('engine_min')))
    if _int_or_none(G.get('engine_max')):
        qs = qs.filter(engine_capacity__lte=_int_or_none(G.get('engine_max')))
    if _int_or_none(G.get('price_min')):
        qs = qs.filter(price__gte=_int_or_none(G.get('price_min')))
    if _int_or_none(G.get('price_max')):
        qs = qs.filter(price__lte=_int_or_none(G.get('price_max')))

    if G.get('country_filter'):
        qs = qs.filter(country=G.get('country_filter'))
    if G.get('state_filter'):
        qs = qs.filter(state=G.get('state_filter'))
    if G.get('city', '').strip():
        qs = qs.filter(city__icontains=G.get('city').strip())

    pw = _int_or_none(G.get('posted_within'))
    if pw:
        qs = qs.filter(created_at__gte=timezone.now() - timedelta(days=pw))
    if G.get('negotiable') == 'on':
        qs = qs.filter(negotiable=True)

    q = (G.get('part_query', '') or '').strip()
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(oem_code__icontains=q))

    qs = qs.order_by('-created_at')

    part_groups, total_pt = [], 0
    for key, label in MOTO_PART_CATEGORIES:
        items = list(Equipment.objects.filter(category=key).order_by('name'))
        if items:
            part_groups.append({'key': key, 'label': label, 'items': items})
            total_pt += len(items)

    from apps.listings.views import COUNTRY_FLAGS as _flag
    all_c = list(Listing.COUNTRY_CHOICES)
    us = [c for c in all_c if c[0] == 'US']
    rest = sorted([c for c in all_c if c[0] != 'US'], key=lambda x: x[1])
    country_choices = [(code, f"{_flag.get(code, '🌍')} {name}") for code, name in (us + rest)]

    current_year = timezone.now().year

    context = {
        'listings': qs,
        'total_count': qs.count(),
        'moto_brands': MotorcycleBrand.objects.all().order_by('name'),
        'motorcycle_type_choices': Listing._meta.get_field('motorcycle_type').choices,
        'condition_choices': CONDITION_CHOICES,
        'part_groups': part_groups,
        'part_types_total': total_pt,
        'country_choices': country_choices,
        'us_states': Listing.US_STATE_CHOICES,
        'years': list(range(current_year + 1, 1949, -1)),
        'sel_part_types': [str(x) for x in pt],
        'sel_conditions': cond,
        'sel_moto_types': mt,
    }
    return render(request, 'listings/moto_parts_browse.html', context)


def moto_parts_advanced_search(request):
    G = request.GET
    part_groups, total_pt = [], 0
    for key, label in MOTO_PART_CATEGORIES:
        items = list(Equipment.objects.filter(category=key).order_by('name'))
        if items:
            part_groups.append({'key': key, 'label': label, 'items': items})
            total_pt += len(items)

    from apps.listings.views import COUNTRY_FLAGS as _flag
    all_c = list(Listing.COUNTRY_CHOICES)
    us = [c for c in all_c if c[0] == 'US']
    rest = sorted([c for c in all_c if c[0] != 'US'], key=lambda x: x[1])
    country_choices = [(code, f"{_flag.get(code, '🌍')} {name}") for code, name in (us + rest)]

    current_year = timezone.now().year
    context = {
        'moto_brands': MotorcycleBrand.objects.all().order_by('name'),
        'motorcycle_type_choices': Listing._meta.get_field('motorcycle_type').choices,
        'condition_choices': CONDITION_CHOICES,
        'part_groups': part_groups,
        'part_types_total': total_pt,
        'country_choices': country_choices,
        'us_states': Listing.US_STATE_CHOICES,
        'years': list(range(current_year + 1, 1949, -1)),
        'sel_part_types': [v for v in G.getlist('part_types') if v],
        'sel_conditions': [v for v in G.getlist('condition') if v],
        'sel_moto_types': [v for v in G.getlist('motorcycle_type') if v],
    }
    return render(request, 'listings/moto_parts_advanced.html', context)