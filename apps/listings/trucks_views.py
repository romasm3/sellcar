from .search_params import sanitize as sanitize_search_params
"""
trucks_views.py — Trucks & Commercial vehicle listings
Architecture: Variant A — uses existing Listing table with truck-specific fields.
"""
from django.utils.translation import gettext_lazy as _
import json
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.http import require_POST
from django.utils import timezone
from .search_config import panels as panel_config
from django.db.models import Count, Q, Case, When, IntegerField, Value
from django.db.models.functions import Greatest, Coalesce
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation

from .image_validation import ImageValidationError, validate_images
from .models import (
    Listing,
    ListingImage,
    ListingEquipment,
    Equipment,
    VehicleType,
    SubCategory,
    TruckBrand,
    FuelType,
    Transmission,
    SavedListing,
)

logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════
TRUCKS_DRAFT_SESSION_KEY = 'active_trucks_draft_id'
# Kiek dienų skelbimas laikomas nauju — vienas šaltinis modelyje
# (models.NAUJO_SKELBIMO_DIENOS, ten pat ir Listing.yra_naujas).
from apps.listings.models import NAUJO_SKELBIMO_DIENOS
NEW_LISTING_DAYS = NAUJO_SKELBIMO_DIENOS

CITY_COORDINATES = {
    'vilnius': (54.6872, 25.2797), 'kaunas': (54.8985, 23.9036),
    'klaipeda': (55.7033, 21.1443), 'siauliai': (55.9349, 23.3137),
}
COUNTRY_COORDINATES = {
    'US': (37.0902, -95.7129), 'LT': (55.1694, 23.8813),
    'LV': (56.8796, 24.6032), 'EE': (58.5953, 25.0136),
    'PL': (51.9194, 19.1451), 'DE': (51.1657, 10.4515),
}

CURRENCY_CHOICES = [
    ('USD', '$'), ('EUR', '€'), ('GBP', '£'),
]

# Šalys — vienas sąrašas visai svetainei (apps/listings/salys.py).
# Čia buvo savas aštuonių šalių sąrašas.
from apps.listings import salys as _salys
COUNTRY_CHOICES = _salys.plokscias()

MONTHS = [
    ('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'),
    ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'),
    ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'),
]


def _get_coordinates(city, country_code):
    if city:
        cl = city.lower().strip()
        if cl in CITY_COORDINATES:
            return CITY_COORDINATES[cl]
    if country_code and country_code in COUNTRY_COORDINATES:
        return COUNTRY_COORDINATES[country_code]
    return (54.8985, 23.9036)


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


def _decimal_or_none(v):
    if v in (None, ''):
        return None
    try:
        return Decimal(str(v))
    except (InvalidOperation, ValueError, TypeError):
        return None


# ═══════════════════════════════════════════════════════════
# DRAFT MGMT (create flow)
# ═══════════════════════════════════════════════════════════
def _is_draft_empty(draft):
    """Check if draft has no meaningful content (used by ?new=1 cleanup)."""
    if not draft:
        return True
    return (
        not draft.truck_brand_id
        and not draft.truck_model_text
        and not draft.images.exists()
        and not draft.description
        and (not draft.price or draft.price == 0)
    )


def _resolve_trucks_subcategory(slug):
    """Pikerio ?subcategory= slug → trucks SubCategory (fallback 'trucks').

    Anksčiau subkategorija buvo hardcodinta į 'trucks', o ?subcategory=
    ignoruojamas — visi Vilkikai / Autotraukiniai / Autobusai /
    Komunalinis transportas patekdavo į „Sunkvežimius“.
    """
    trucks_vt = VehicleType.objects.filter(slug='trucks').first()
    if not trucks_vt:
        return None
    sub = None
    if slug:
        sub = SubCategory.objects.filter(
            vehicle_type=trucks_vt, slug=slug, parent__isnull=True
        ).first()
    return sub or SubCategory.objects.filter(
        vehicle_type=trucks_vt, slug='trucks'
    ).first()


def _get_trucks_draft(request, force_new=False):
    """Sesijos draft'as, jei jis JAU yra. Nekuria naujo.

    GET užklausa eilutės DB nebekuria — anksčiau vien atidarius formą
    atsirasdavo „Untitled truck draft". Draft'as sukuriamas tik tada, kai
    vartotojas ką nors realiai padaro: autosave (įvedė lauką), nuotraukos
    įkėlimas arba formos pateikimas.
    """
    if force_new:
        _drop_empty_trucks_draft(request)
    draft_id = request.session.get(TRUCKS_DRAFT_SESSION_KEY)
    if not draft_id:
        return None
    try:
        return Listing.objects.get(
            pk=draft_id, seller=request.user, status='draft')
    except Listing.DoesNotExist:
        request.session[TRUCKS_DRAFT_SESSION_KEY] = None
        return None


def _drop_empty_trucks_draft(request):
    """?new=1 — senas tuščias draft'as išmetamas (ANTI-ZOMBIE-DRAFT)."""
    old_id = request.session.get(TRUCKS_DRAFT_SESSION_KEY)
    if old_id:
        try:
            old = Listing.objects.get(
                pk=old_id, seller=request.user, status='draft')
            if _is_draft_empty(old):
                logger.info(f"[trucks] Deleting empty draft #{old.pk}")
                old.delete()
        except Listing.DoesNotExist:
            pass
        request.session[TRUCKS_DRAFT_SESSION_KEY] = None
        request.session.modified = True


def _get_or_create_trucks_draft(request, force_new=False):
    """
    Get existing trucks draft from session, or create new one.

    If force_new=True (e.g. ?new=1), deletes any empty existing draft
    and creates fresh. This is the ANTI-ZOMBIE-DRAFT logic.
    """
    if force_new:
        _drop_empty_trucks_draft(request)

    # Try existing
    draft_id = request.session.get(TRUCKS_DRAFT_SESSION_KEY)
    if draft_id:
        try:
            return Listing.objects.get(
                pk=draft_id,
                seller=request.user,
                status='draft',
            )
        except Listing.DoesNotExist:
            request.session[TRUCKS_DRAFT_SESSION_KEY] = None

    # Create new
    trucks_vt = VehicleType.objects.filter(slug='trucks').first()
    if not trucks_vt:
        return None

    trucks_subcat = _resolve_trucks_subcategory(request.GET.get('subcategory'))

    draft = Listing.objects.create(
        seller=request.user,
        vehicle_type=trucks_vt,
        subcategory=trucks_subcat,
        title='Untitled truck draft',
        year=date.today().year,
        mileage=0,
        price=0,
        country='US',
        city='—',
        status='draft',
        condition='',
        defects='',
    )
    request.session[TRUCKS_DRAFT_SESSION_KEY] = draft.pk
    request.session.modified = True
    return draft


# ═══════════════════════════════════════════════════════════
# CHOICES (single source for create + edit + filters)
# ═══════════════════════════════════════════════════════════
def _truck_type_choices():
    if hasattr(Listing, 'TRUCK_TYPE_CHOICES'):
        return Listing.TRUCK_TYPE_CHOICES
    return [
        ('curtain_side', 'Curtain-Side'),
        ('refrigerator', 'Refrigerator'),
        ('isothermal', 'Isothermal'),
        ('tipper', 'Tipper'),
        ('flatbed', 'Flatbed'),
        ('container', 'Container'),
        ('tanker', 'Tanker'),
        ('box', 'Box'),
        ('chassis', 'Chassis'),
        ('crane', 'Crane'),
        ('other', 'Other'),
    ]


def _wheel_formula_choices():
    if hasattr(Listing, 'WHEEL_FORMULA_CHOICES'):
        return Listing.WHEEL_FORMULA_CHOICES
    return [
        ('4x2', '4x2'), ('4x4', '4x4'),
        ('6x2', '6x2'), ('6x4', '6x4'), ('6x6', '6x6'),
        ('8x2', '8x2'), ('8x4', '8x4'), ('8x6', '8x6'), ('8x8', '8x8'),
    ]


def _mass_interval_choices():
    if hasattr(Listing, 'MASS_INTERVAL_CHOICES'):
        return Listing.MASS_INTERVAL_CHOICES
    return [
        ('to_3500', 'Up to 3.5 t'),
        ('3500_7500', '3.5 – 7.5 t'),
        ('7500_12000', '7.5 – 12 t'),
        ('12000_18000', '12 – 18 t'),
        ('over_18000', 'Over 18 t'),
    ]


def _suspension_choices():
    if hasattr(Listing, 'TRUCK_SUSPENSION_CHOICES'):
        return Listing.TRUCK_SUSPENSION_CHOICES
    return [
        ('air', 'Air'),
        ('spring', 'Spring'),
        ('air_spring', 'Air + Spring'),
        ('hydraulic', 'Hydraulic'),
    ]


def _euro_standard_choices():
    if hasattr(Listing, 'EURO_STANDARD_CHOICES'):
        return Listing.EURO_STANDARD_CHOICES
    return []


def _condition_choices():
    if hasattr(Listing, 'CONDITION_CHOICES'):
        return Listing.CONDITION_CHOICES
    return [('new', 'New'), ('used', 'Used')]


def _defect_choices():
    if hasattr(Listing, 'DEFECT_CHOICES'):
        return Listing.DEFECT_CHOICES
    return [('none', 'No defects'), ('minor', 'Minor'), ('major', 'Major')]


def _steering_choices():
    if hasattr(Listing, 'STEERING_CHOICES'):
        return Listing.STEERING_CHOICES
    return [('left', 'Left'), ('right', 'Right')]


def _color_choices():
    if hasattr(Listing, 'COLOR_CHOICES'):
        return Listing.COLOR_CHOICES
    return []


def _us_states():
    if hasattr(Listing, 'US_STATE_CHOICES'):
        return Listing.US_STATE_CHOICES
    return []


def _years_list():
    return list(range(date.today().year + 1, 1949, -1))


# ═══════════════════════════════════════════════════════════
# EQUIPMENT — TRUCK-SPECIFIC (autoplius.lt style, EN translation)
# Hardcoded list, separate from cars/moto Equipment.
# Stored as Equipment rows with category prefix 'truck_*' so they don't mix with cars.
# ═══════════════════════════════════════════════════════════
TRUCK_EQUIPMENT_DEFINITION = [
    # (category_key, EN label shown in UI, [list of item names])
    ('truck_body', 'Body & Equipment', [
        'Aluminum floor',
        'Aluminum side panels',
        'Hydraulics',
        'Rear doors',
        'Side doors',
        'Air suspension',
        'Central lubrication',
        'Two-way tipper',
        'Three-way tipper',
        'Lift axle',
        'For bulk cargo',
        'Spare wheel',
        'Additional fuel tank',
        'Refrigeration unit',
        'Alarm',
        'Tail lift',
        'Springs',
        'Hook / winch',
        'Crane / manipulator',
        'Bucket / grapple',
    ]),
    ('truck_cabin', 'Cabin', [
        'Sunroof',
        'Heated seat',
        'Air conditioning',
        'Double cabin',
        'Mini kitchen',
        'Tilt cabin',
        'Personal lighting',
        'Low cabin',
        'Personal ventilation',
        'Power steering',
    ]),
    ('truck_other', 'Other features', [
        'Metallic paint',
        'Trailer hitch',
        'Not used in Lithuania',
        'Open to trade',
        'For sale on lease',
        'Service book',
    ]),
    ('truck_audio_video', 'Audio / Video', [
        'Audio system',
        'Video system',
    ]),
    ('truck_electronics', 'Electronics', [
        'Cruise control',
        'Electric mirrors',
        'Navigation / GPS',
        'Auxiliary heater',
        'Tachograph',
        'Electric steering adjustment',
        'Electric windows',
        'Onboard computer',
        'Climate control',
    ]),
    ('truck_safety', 'Safety', [
        'ABS',
        'ADR (hazmat)',
        'Cargo straps',
        'Airbags',
        'EBS',
        'Engine brake / retarder',
        'Locking differential',
        'ESP',
        'Trailer brake',
        'Hill-start assist',
    ]),
]


def _get_truck_equipment():
    """
    Returns truck-specific equipment grouped by category, ready for template.
    Each item is auto-created in Equipment table with 'truck_*' category prefix
    on first call (idempotent via get_or_create), so item.id stays stable.

    Cars/moto equipment is NOT touched — only truck_* categories belong here.
    """
    grouped = []
    for cat_key, cat_label, item_names in TRUCK_EQUIPMENT_DEFINITION:
        items = []
        for name in item_names:
            obj, _ = Equipment.objects.get_or_create(
                category=cat_key,
                name=name,
            )
            items.append(obj)
        grouped.append({
            'key': cat_key,
            'label': cat_label,
            'items': items,
        })
    return grouped


def _ordered_truck_brands():
    """Return TruckBrand list with 'Other' pinned to the top, rest alphabetical."""
    others = list(TruckBrand.objects.filter(name__iexact='Other'))
    rest = list(TruckBrand.objects.exclude(name__iexact='Other').order_by('name'))
    return others + rest


# ═══════════════════════════════════════════════════════════
# DATA EXTRACT — DB → form-data dict (used by both create & edit)
# ═══════════════════════════════════════════════════════════
def _listing_to_form_data(listing):
    """Extract form-bindable dict from existing Listing."""
    if not listing:
        return {}

    eq_ids = list(listing.equipment_items.values_list('equipment_id', flat=True))

    return {
        'truck_brand': str(listing.truck_brand_id) if listing.truck_brand_id else '',
        'truck_model_text': listing.truck_model_text or '',
        'truck_type': listing.truck_type or '',
        'year': listing.year or '',
        'first_registration_month': (
            f'{listing.first_registration.month:02d}'
            if listing.first_registration else ''
        ),
        'gross_weight_kg': listing.gross_weight_kg or '',
        'curb_weight': listing.curb_weight or '',
        'power': listing.power or '',
        'mileage': listing.mileage or '',
        'fuel_type': str(listing.fuel_type_id) if listing.fuel_type_id else '',
        'wheel_formula': listing.wheel_formula or '',
        'truck_length_mm': listing.truck_length_mm or '',
        'truck_width_mm': listing.truck_width_mm or '',
        'euro_standard': listing.euro_standard or '',
        'mass_interval': listing.mass_interval or '',
        'truck_height_mm': listing.truck_height_mm or '',
        'truck_volume_m3': listing.truck_volume_m3 or '',
        'defects': listing.defects or '',
        'condition': listing.condition or '',
        'payload_kg': listing.payload_kg or '',
        'fuel_tank_capacity_l': listing.fuel_tank_capacity_l or '',
        'technical_inspection_year': listing.technical_inspection_year or '',
        'technical_inspection_month': (
            f'{listing.technical_inspection_month:02d}'
            if listing.technical_inspection_month else ''
        ),
        'steering': listing.steering or '',
        'transmission': str(listing.transmission_id) if listing.transmission_id else '',
        'sleeping_seats': listing.sleeping_seats or '',
        'front_suspension': listing.front_suspension or '',
        'rear_suspension': listing.rear_suspension or '',
        'sdk_number': listing.sdk_number or '',
        'engine_capacity': listing.engine_capacity or '',
        'color': listing.color or '',
        'vin': listing.vin or '',
        'description': listing.description or '',
        'video_url': listing.video_url or '',
        'price': listing.price or '',
        'currency': listing.currency or 'USD',
        'negotiable': listing.negotiable,
        'country': listing.country or 'US',
        'state': listing.state or '',
        'city': listing.city if listing.city != '—' else '',
        'postal_code': listing.postal_code or '',
        'address': listing.address or '',
        'equipment': [str(eid) for eid in eq_ids],
    }


# ═══════════════════════════════════════════════════════════
# SAVE FORM → Listing (shared by create + edit)
# ═══════════════════════════════════════════════════════════
def _save_form_to_listing(post, listing):
    """Apply POST data to existing Listing instance and save."""
    # Truck-specific
    tb_id = _int_or_none(post.get('truck_brand'))
    if tb_id:
        try:
            listing.truck_brand = TruckBrand.objects.get(pk=tb_id)
        except TruckBrand.DoesNotExist:
            pass
    elif post.get('truck_brand') == '':
        listing.truck_brand = None

    listing.truck_model_text = (post.get('truck_model_text') or '').strip()
    listing.truck_type = post.get('truck_type', '')
    listing.wheel_formula = post.get('wheel_formula', '')
    listing.mass_interval = post.get('mass_interval', '')
    listing.front_suspension = post.get('front_suspension', '')
    listing.rear_suspension = post.get('rear_suspension', '')
    listing.sdk_number = (post.get('sdk_number') or '').strip()

    listing.truck_length_mm = _int_or_none(post.get('truck_length_mm'))
    listing.truck_width_mm = _int_or_none(post.get('truck_width_mm'))
    listing.truck_height_mm = _int_or_none(post.get('truck_height_mm'))
    listing.truck_volume_m3 = _decimal_or_none(post.get('truck_volume_m3'))
    listing.gross_weight_kg = _int_or_none(post.get('gross_weight_kg'))
    listing.payload_kg = _int_or_none(post.get('payload_kg'))
    listing.fuel_tank_capacity_l = _int_or_none(post.get('fuel_tank_capacity_l'))
    listing.sleeping_seats = _int_or_none(post.get('sleeping_seats'))

    # Common fields
    year = _int_or_none(post.get('year'))
    if year:
        listing.year = year

    month = _int_or_none(post.get('first_registration_month'))
    if year and month:
        try:
            listing.first_registration = date(year=year, month=month, day=1)
        except (ValueError, TypeError):
            pass

    ft_id = _int_or_none(post.get('fuel_type'))
    if ft_id:
        try:
            listing.fuel_type = FuelType.objects.get(pk=ft_id)
        except FuelType.DoesNotExist:
            pass

    tr_id = _int_or_none(post.get('transmission'))
    if tr_id:
        try:
            listing.transmission = Transmission.objects.get(pk=tr_id)
        except Transmission.DoesNotExist:
            pass
    elif post.get('transmission') == '':
        listing.transmission = None

    mileage = _int_or_none(post.get('mileage'))
    if mileage is not None:
        listing.mileage = mileage

    listing.engine_capacity = _decimal_or_none(post.get('engine_capacity'))
    listing.power = _int_or_none(post.get('power'))
    listing.condition = post.get('condition', '')
    listing.defects = post.get('defects', '')
    listing.steering = post.get('steering', '')
    listing.color = post.get('color', '')
    listing.curb_weight = _int_or_none(post.get('curb_weight'))
    listing.euro_standard = post.get('euro_standard', '')
    listing.technical_inspection_month = _int_or_none(post.get('technical_inspection_month'))
    listing.technical_inspection_year = _int_or_none(post.get('technical_inspection_year'))

    listing.vin = (post.get('vin', '') or '').strip().upper()
    listing.description = post.get('description', '')
    listing.video_url = post.get('video_url', '')

    # Price
    price = _decimal_or_none(post.get('price'))
    if price is not None:
        listing.price = price
    listing.currency = post.get('currency', 'USD')
    listing.negotiable = post.get('negotiable') in ('on', 'true', '1', True)

    # Location
    listing.country = post.get('country', 'US')
    if listing.country == 'US':
        listing.state = post.get('state', '')
    else:
        listing.state = ''
    listing.city = (post.get('city', '') or '').strip() or '—'
    listing.postal_code = post.get('postal_code', '').strip()
    listing.address = post.get('address', '').strip()

    # Phone lives on the profile, not the listing — same as every other form.
    phone_val = (post.get('phone', '') or '').strip()
    if phone_val and hasattr(listing.seller, 'profile'):
        listing.seller.profile.phone_number = phone_val
        listing.seller.profile.save(update_fields=['phone_number'])

    # Coords
    lat, lng = _get_coordinates(listing.city, listing.country)
    listing.latitude = Decimal(str(lat))
    listing.longitude = Decimal(str(lng))

    # Title
    title_parts = []
    if listing.truck_brand:
        title_parts.append(listing.truck_brand.name)
    if listing.truck_model_text:
        title_parts.append(listing.truck_model_text)
    if listing.year:
        title_parts.append(str(listing.year))
    if title_parts:
        listing.title = ' '.join(title_parts)

    listing.save()

    # Equipment (M2M-like via ListingEquipment)
    eq_ids = post.getlist('equipment')
    ListingEquipment.objects.filter(listing=listing).delete()
    for eid in eq_ids:
        try:
            ListingEquipment.objects.create(
                listing=listing,
                equipment_id=int(eid),
            )
        except (ValueError, TypeError):
            continue

    return listing


def _validate_required(post, require_terms=False):
    """Returns dict of {field: error_msg} for any missing required fields."""
    errors = {}
    if not post.get('truck_type'):
        errors['truck_type'] = _('Tipas yra privalomas')
    if not _int_or_none(post.get('truck_brand')):
        errors['truck_brand'] = _('Markė yra privaloma')
    if not (post.get('truck_model_text') or '').strip():
        errors['truck_model_text'] = _('Modelis yra privalomas')
    if not _int_or_none(post.get('year')):
        errors['year'] = _('Metai yra privalomi')
    if not _int_or_none(post.get('first_registration_month')):
        errors['first_registration_month'] = _('Mėnuo yra privalomas')
    if not _int_or_none(post.get('fuel_type')):
        errors['fuel_type'] = _('Kuro tipas yra privalomas')
    if not post.get('defects'):
        errors['defects'] = _('Defektai yra privalomi')
    if not post.get('condition'):
        errors['condition'] = _('Būklė yra privaloma')
    if not _decimal_or_none(post.get('price')):
        errors['price'] = _('Kaina yra privaloma')
    if post.get('country', 'US') == 'US' and not post.get('state'):
        errors['state'] = _('Valstija yra privaloma')
    if not (post.get('city') or '').strip():
        errors['city'] = _('Miestas yra privalomas')
    if not (post.get('phone') or '').strip():
        errors['phone'] = _('Telefonas yra privalomas')
    if require_terms and not post.get('agree_terms'):
        errors['agree_terms'] = _('Turite sutikti su taisyklėmis')
    return errors


# ═══════════════════════════════════════════════════════════
# CREATE VIEW
# ═══════════════════════════════════════════════════════════
@login_required
def trucks_listing_create(request):
    force_new = request.GET.get('new') == '1'
    draft = _get_trucks_draft(request, force_new=force_new)

    if request.method == 'POST':
        if draft is None:
            draft = _get_or_create_trucks_draft(request, force_new=False)
        if not draft:
            return redirect('/')

        errors = _validate_required(request.POST, require_terms=True)
        if errors:
            data = dict(request.POST)
            data['equipment'] = request.POST.getlist('equipment')
            # flatten single-value lists
            for k, v in list(data.items()):
                if isinstance(v, list) and k != 'equipment' and len(v) == 1:
                    data[k] = v[0]
            return render(request, 'listings/trucks_listing_create.html',
                          _build_context(request, draft, data=data, errors=errors,
                                         is_edit=False))

        # Save and activate
        _save_form_to_listing(request.POST, draft)

        # Clear session
        request.session[TRUCKS_DRAFT_SESSION_KEY] = None
        request.session.modified = True

        # ═══ Pirmi 3 nemokami (bendrai per visas kategorijas) ═══
        from .constants import can_create_free_listing, FREE_LISTING_DAYS
        is_free, _, _ = can_create_free_listing(request.user)

        if is_free:
            try:
                draft.activate(days=FREE_LISTING_DAYS)
            except AttributeError:
                draft.status = 'active'
                draft.activated_at = timezone.now()
                draft.expires_at = timezone.now() + timedelta(days=FREE_LISTING_DAYS)
                draft.save()

            try:
                from .views import _send_listing_published_email
                _send_listing_published_email(draft, request.user)
            except Exception as e:
                logger.error(f"[trucks] published email failed: {e}")

            return redirect(
                reverse('listing_success', kwargs={'pk': draft.pk}) + '?action=published'
            )
        else:
            return redirect('listing_select_plan', pk=draft.pk)

    # GET — render form
    data = _listing_to_form_data(draft)
    return render(request, 'listings/trucks_listing_create.html',
                  _build_context(request, draft, data=data, errors={}, is_edit=False))


# ═══════════════════════════════════════════════════════════
# EDIT VIEW (shared template)
# ═══════════════════════════════════════════════════════════
@login_required
def trucks_listing_edit(request, pk):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user)

    # Defensive: if not a truck somehow, redirect to normal edit
    if not (listing.vehicle_type and listing.vehicle_type.slug == 'trucks'):
        return redirect('listing_edit_hub', pk=pk)

    if request.method == 'POST':
        errors = _validate_required(request.POST)
        if errors:
            data = dict(request.POST)
            data['equipment'] = request.POST.getlist('equipment')
            for k, v in list(data.items()):
                if isinstance(v, list) and k != 'equipment' and len(v) == 1:
                    data[k] = v[0]
            return render(request, 'listings/trucks_listing_create.html',
                          _build_context(request, listing, data=data, errors=errors,
                                         is_edit=True))

        old_price = listing.price
        _save_form_to_listing(request.POST, listing)

        # Email notifications
        try:
            from .views import (
                _send_saved_listing_price_drop_emails,
                _send_saved_listing_updated_emails,
            )
            new_price = float(listing.price)
            old_price_f = float(old_price) if old_price else 0
            if new_price != old_price_f and old_price_f > 0:
                if new_price < old_price_f:
                    _send_saved_listing_price_drop_emails(listing, old_price_f, new_price)
                else:
                    summary = _('Kaina pasikeitė: %(sena)s → %(nauja)s') % {
                        'sena': formatai.kaina(old_price_f, listing.currency_symbol),
                        'nauja': formatai.kaina(new_price, listing.currency_symbol)}
                    _send_saved_listing_updated_emails(listing, summary)
            else:
                _send_saved_listing_updated_emails(listing, 'Listing details updated')
        except Exception as e:
            logger.error(f"[trucks] update email failed: {e}")

        return redirect('listing_detail', pk=listing.pk)

    # GET — render form
    data = _listing_to_form_data(listing)
    return render(request, 'listings/trucks_listing_create.html',
                  _build_context(request, listing, data=data, errors={}, is_edit=True))


# ═══════════════════════════════════════════════════════════
# CONTEXT BUILDER
# ═══════════════════════════════════════════════════════════
def _build_context(request, listing, data, errors, is_edit):
    """Single context builder shared by create + edit."""
    return {
        'is_edit': is_edit,
        'current_draft': listing if not is_edit else None,
        'current_listing': listing if is_edit else None,
        'data': data,
        'errors': errors,
        # Choices
        'truck_type_choices': _truck_type_choices(),
        'wheel_formula_choices': _wheel_formula_choices(),
        'mass_interval_choices': _mass_interval_choices(),
        'truck_suspension_choices': _suspension_choices(),
        'euro_standard_choices': _euro_standard_choices(),
        'condition_choices': _condition_choices(),
        'defect_choices': _defect_choices(),
        'steering_choices': _steering_choices(),
        'color_choices': _color_choices(),
        'currency_choices': CURRENCY_CHOICES,
        'country_choices': COUNTRY_CHOICES,
        'us_states': _us_states(),
        'months': MONTHS,
        'years': _years_list(),
        # Lookups
        'brands': _ordered_truck_brands(),
        'fuel_types': FuelType.objects.all().order_by('name'),
        'transmissions': Transmission.objects.all().order_by('name'),
        'equipment_by_category': _get_truck_equipment(),
    }


# ═══════════════════════════════════════════════════════════
# AJAX: SAVE DRAFT (autosave during create)
# ═══════════════════════════════════════════════════════════
@login_required
@require_POST
def save_trucks_draft_ajax(request):
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

    draft = _get_or_create_trucks_draft(request, force_new=False)
    if not draft:
        return JsonResponse({'success': False, 'error': 'Cannot create draft'}, status=400)

    # Treat data as POST-style dict
    class FakePost:
        def __init__(self, d):
            self.d = d
        def get(self, k, default=''):
            v = self.d.get(k, default)
            if isinstance(v, list):
                return v[0] if v else default
            return v if v is not None else default
        def getlist(self, k):
            v = self.d.get(k, [])
            if isinstance(v, list):
                return v
            return [v] if v else []

    try:
        _save_form_to_listing(FakePost(data), draft)
    except Exception as e:
        logger.error(f"[trucks autosave] {e}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

    if _is_draft_empty(draft):
        draft.delete()
        request.session[TRUCKS_DRAFT_SESSION_KEY] = None
        request.session.modified = True
        return JsonResponse({'success': True, 'draft_id': None, 'skipped': 'empty'})

    return JsonResponse({
        'success': True,
        'draft_id': draft.pk,
        'saved_at': timezone.now().isoformat(),
    })


# ═══════════════════════════════════════════════════════════
# AJAX: PHOTO UPLOAD (works for both create draft + edit listing)
# ═══════════════════════════════════════════════════════════
@login_required
@require_POST
def upload_trucks_image_ajax(request):
    """
    Upload to either:
      - existing listing (if listing_id provided in POST — EDIT mode)
      - active session draft (CREATE mode)
    """
    listing_id = _int_or_none(request.POST.get('listing_id'))

    if listing_id:
        try:
            target = Listing.objects.get(
                pk=listing_id,
                seller=request.user,
            )
        except Listing.DoesNotExist:
            return JsonResponse({'success': False, 'error': str(_('Listing not found'))}, status=404)
    else:
        target = _get_or_create_trucks_draft(request, force_new=False)
        if not target:
            return JsonResponse({'success': False, 'error': 'No active draft'}, status=400)

    images = request.FILES.getlist('images')
    if not images:
        return JsonResponse({'success': False, 'error': str(_('No images uploaded'))}, status=400)

    try:
        validate_images(images)
    except ImageValidationError as exc:
        return JsonResponse({'success': False, 'error': str(exc)}, status=400)

    existing_count = target.images.count()
    uploaded = []

    for i, image in enumerate(images[:40]):
        try:
            img = ListingImage.objects.create(
                listing=target,
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
            logger.error(f"[trucks upload] {e}")

    return JsonResponse({
        'success': True,
        'uploaded': uploaded,
        'total_count': target.images.count(),
    })


@login_required
@require_POST
def delete_trucks_image_ajax(request, pk):
    """Delete one image (works for create draft + edit listing)."""
    try:
        img = ListingImage.objects.get(
            pk=pk,
            listing__seller=request.user,
        )
        listing = img.listing
        was_main = img.is_main
        img.delete()

        if was_main:
            first = listing.images.order_by('order').first()
            if first:
                first.is_main = True
                first.save(update_fields=['is_main'])

        return JsonResponse({
            'success': True,
            'remaining_count': listing.images.count(),
        })
    except ListingImage.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Image not found'}, status=404)


@login_required
@require_POST
def reorder_trucks_images_ajax(request):
    """Reorder images (create draft or edit listing)."""
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

    image_ids = data.get('image_ids', [])
    listing_id = _int_or_none(data.get('listing_id'))

    if not image_ids:
        return JsonResponse({'success': False, 'error': 'No image_ids'}, status=400)

    if listing_id:
        target_filter = {'listing_id': listing_id, 'listing__seller': request.user}
    else:
        draft_id = request.session.get(TRUCKS_DRAFT_SESSION_KEY)
        if not draft_id:
            return JsonResponse({'success': False, 'error': 'No active draft'}, status=400)
        target_filter = {'listing_id': draft_id, 'listing__seller': request.user}

    for new_order, img_id in enumerate(image_ids):
        try:
            img = ListingImage.objects.get(pk=img_id, **target_filter)
            img.order = new_order
            img.is_main = (new_order == 0)
            img.save(update_fields=['order', 'is_main'])
        except ListingImage.DoesNotExist:
            continue

    return JsonResponse({'success': True})


# ═══════════════════════════════════════════════════════════
# LIST + ADVANCED SEARCH (Browse Trucks page) — unchanged
# ═══════════════════════════════════════════════════════════
def _public_trucks_qs(request_user=None):
    """All public trucks (active + recently sold)."""
    now = timezone.now()
    sold_cutoff = now - timedelta(days=Listing.SOLD_DISPLAY_DAYS)

    qs = Listing.objects.filter(
        Q(status='active') | Q(status='sold', sold_at__gte=sold_cutoff),
        vehicle_type__slug='trucks',
    )
    if request_user and request_user.is_authenticated and request_user.is_superuser:
        return qs
    return qs.filter(is_shadow_banned=False)


def trucks_list(request):
    """Browse Trucks page."""
    # Sugadintos skaitinės reikšmės (?price_min=abc) tyliai išmetamos.
    request.GET = sanitize_search_params(request.GET)
    listings = _public_trucks_qs(request.user).select_related(
        'truck_brand', 'fuel_type', 'transmission', 'subcategory', 'vehicle_type',
    ).prefetch_related('images')

    # Filters
    selected_subcategory = request.GET.get('subcategory', '')
    if selected_subcategory:
        listings = listings.filter(subcategory__slug=selected_subcategory)

    selected_truck_types = [v for v in request.GET.getlist('truck_type') if v]
    if selected_truck_types:
        listings = listings.filter(truck_type__in=selected_truck_types)

    selected_euro = request.GET.get('euro_standard', '')
    if selected_euro:
        listings = listings.filter(euro_standard=selected_euro)

    selected_drive = request.GET.get('drive_type', '')
    if selected_drive:
        listings = listings.filter(drive_type=selected_drive)

    selected_country = request.GET.get('country_filter', '')
    selected_state = request.GET.get('state_filter', '')
    if selected_state:
        listings = listings.filter(country='US', state=selected_state)
    elif selected_country:
        listings = listings.filter(country=selected_country)

    if request.GET.get('brand'):
        listings = listings.filter(truck_brand_id=request.GET.get('brand'))
    if request.GET.get('price_min'):
        listings = listings.filter(price__gte=request.GET.get('price_min'))
    if request.GET.get('price_max'):
        listings = listings.filter(price__lte=request.GET.get('price_max'))
    if request.GET.get('year_min'):
        listings = listings.filter(year__gte=request.GET.get('year_min'))
    if request.GET.get('year_max'):
        listings = listings.filter(year__lte=request.GET.get('year_max'))
    if request.GET.get('fuel_type'):
        listings = listings.filter(fuel_type_id=request.GET.get('fuel_type'))

    # Sort by recency
    _now = timezone.now()
    _3d = _now - timedelta(days=NEW_LISTING_DAYS)
    listings = listings.annotate(
        eff_date=Greatest(Coalesce('activated_at', 'created_at'), Coalesce('last_boosted_at', 'created_at')),
        sort_priority=Case(
            When(star_level=2, star_expires_at__gt=_now, then=Value(500)),
            When(star_level=1, star_expires_at__gt=_now, then=Value(400)),
            When(eff_date__gt=_3d, then=Value(200)),
            default=Value(100),
            output_field=IntegerField(),
        ),
    ).order_by('-sort_priority', '-eff_date')

    listings_all = list(listings[:60])

    # Subcategories with counts
    trucks_vt = VehicleType.objects.filter(slug='trucks').first()
    subcategories = []
    if trucks_vt:
        for sc in SubCategory.objects.filter(vehicle_type=trucks_vt).order_by('order', 'name'):
            count = _public_trucks_qs(request.user).filter(subcategory=sc).count()
            subcategories.append({
                'slug': sc.slug,
                'name': sc.name,
                'icon': '🚛',
                'count': count,
            })

    # Truck-type counts
    truck_type_counts = dict(
        _public_trucks_qs(request.user).filter(subcategory__slug='trucks')
        .exclude(truck_type='')
        .values('truck_type')
        .annotate(c=Count('id'))
        .values_list('truck_type', 'c')
    )
    truck_type_choices_with_counts = [
        {
            'value': v,
            'label': l,
            'count': truck_type_counts.get(v, 0),
        }
        for v, l in _truck_type_choices()
    ]

    # Brands with counts
    brands = _ordered_truck_brands()
    brand_counts = dict(
        _public_trucks_qs(request.user).values('truck_brand_id')
        .annotate(c=Count('id'))
        .values_list('truck_brand_id', 'c')
    )
    for b in brands:
        b.count = brand_counts.get(b.id, 0)

    saved_ids = []
    if request.user.is_authenticated:
        saved_ids = list(SavedListing.objects.filter(
            user=request.user
        ).values_list('listing_id', flat=True))


    # Tabs
    tabs_base = _public_trucks_qs(request.user).select_related(
        'truck_brand', 'fuel_type', 'transmission'
    )
    _now2 = timezone.now()
    tab_featured = list(tabs_base.filter(
        star_level__gte=1, star_expires_at__gt=_now2,
    ).order_by('-star_level', '-last_boosted_at')[:6])
    if not tab_featured:
        tab_featured = list(tabs_base.filter(
            last_boosted_at__isnull=False
        ).order_by('-last_boosted_at')[:6])
    if not tab_featured:
        tab_featured = list(tabs_base.order_by('-created_at')[:6])
    tab_newest = list(tabs_base.annotate(paskelbta_db=Coalesce('activated_at', 'created_at')).order_by('-paskelbta_db')[:6])
    tab_popular = list(tabs_base.order_by('-views_count')[:6])
    tab_expensive = list(tabs_base.filter(price__gt=0).order_by('-price')[:6])

    context = {
        'listings': listings_all,
        'total_count': listings.count(),
        'brands': brands,
        'fuel_types': FuelType.objects.all().order_by('name'),
        'years': _years_list(),
        'subcategories': subcategories,
        'selected_subcategory': selected_subcategory,
        'selected_truck_types': selected_truck_types,
        'truck_type_choices_with_counts': truck_type_choices_with_counts,
        'euro_standard_choices': _euro_standard_choices(),
        'drive_type_choices': getattr(Listing, 'DRIVE_TYPE_CHOICES', []),
        'selected_euro_standard': selected_euro,
        'selected_drive_type': selected_drive,
        'selected_country': selected_country,
        'selected_state': selected_state,
        'us_states': _us_states(),
        'saved_ids': saved_ids,
        'tab_featured': tab_featured,
        'tab_newest': tab_newest,
        'tab_popular': tab_popular,
        'tab_expensive': tab_expensive,
    }

    # ═══ SIDEBAR režimas → senas trucks template; kitaip → bendras listing_list (rail) ═══
    if request.GET.get('sidebar'):
        return render(request, 'listings/trucks_list.html', context)

    context.update({
        'selected_category': 'trucks',
        'country_choices': _salys.plokscias(),
        # Filtruose — tik tos šalys, kurios turi skelbimų
        'location_countries': _salys.filtro_salys(listings),
        'transmissions': [],
        'body_type_choices': [],
        'selected_body_types': [],
        'equipment_by_category': [],
        'selected_equipment': [],
        # Deklaratyvios panelės (priekabos, žemės ūkis, nuoma...) — rail'as
        # leidžia į jas persijungti ir iš šio puslapio, todėl kontekstas
        # turi būti toks pat kaip listing_list; kitaip panelės būtų tuščios.
        'config_panels': {
            slug: panel_config.build_panel(slug, request.user)
            for slug in panel_config.active_categories()
        },
        'config_panels_sub': {
            sub: panel_config.build_panel(cfg['vt_slug'], request.user, sub_slug=sub)
            for sub, cfg in panel_config.PANELS_BY_SUB.items()
        },
        'selected_subcategory_name': '',
        'search_query': request.GET.get('search', ''),
    })
    return render(request, 'listings/listing_list.html', context)


def trucks_advanced_search(request):
    """Same as trucks_list — advanced search delegates here."""
    return trucks_list(request)