import json
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .forms import (
    Step1BasicInfoForm,
    Step2MediaForm,
    Step3VehicleDataForm,
    Step4EquipmentForm,
    Step5PriceForm,
    Step6DescriptionForm,
    Step7ContactForm,
)
from .models import (
    Listing,
    ListingImage,
    Model,
    Equipment,
    ListingEquipment,
    VehicleType,
    Brand,
    FuelType,
    Transmission,
)
from datetime import date


# ============================================
# LISTING LIST (Browse Cars)
# ============================================
def listing_list(request):
    """List all active listings with filters"""
    listings = Listing.objects.filter(status='active').select_related(
        'brand', 'model', 'fuel_type', 'transmission'
    ).order_by('-created_at')
    
    # Get all data for dropdowns
    brands = Brand.objects.all().order_by('name')
    years = list(range(2025, 1989, -1))
    fuel_types = FuelType.objects.all().order_by('name')
    transmissions = Transmission.objects.all().order_by('name')
    
    # Apply filters from GET parameters
    brand_filter = request.GET.get('brand')
    model_filter = request.GET.get('model')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    year_min = request.GET.get('year_min')
    year_max = request.GET.get('year_max')
    fuel_type_filter = request.GET.get('fuel_type')
    transmission_filter = request.GET.get('transmission')
    search_query = request.GET.get('search', '')
    
    if search_query:
        listings = listings.filter(title__icontains=search_query)
    
    if brand_filter:
        listings = listings.filter(brand_id=brand_filter)
    
    if model_filter:
        listings = listings.filter(model_id=model_filter)
    
    if price_min:
        listings = listings.filter(price__gte=price_min)
    
    if price_max:
        listings = listings.filter(price__lte=price_max)
    
    if year_min:
        listings = listings.filter(year__gte=year_min)
    
    if year_max:
        listings = listings.filter(year__lte=year_max)
    
    if fuel_type_filter:
        listings = listings.filter(fuel_type_id=fuel_type_filter)
    
    if transmission_filter:
        listings = listings.filter(transmission_id=transmission_filter)
    
    # Get models for selected brand (for AJAX)
    models = []
    if brand_filter:
        models = Model.objects.filter(brand_id=brand_filter).order_by('name')
    
    context = {
        'listings': listings,
        'brands': brands,
        'models': models,
        'years': years,
        'fuel_types': fuel_types,
        'transmissions': transmissions,
        'search_query': search_query,
        'total_count': listings.count(),
    }
    return render(request, 'listings/listing_list.html', context)


# ============================================
# LISTING DETAIL
# ============================================
def listing_detail(request, pk):
    """Listing detail view"""
    listing = get_object_or_404(Listing, pk=pk)

    # Increment views count
    listing.views_count += 1
    listing.save(update_fields=['views_count'])

    context = {
        'listing': listing,
        'GOOGLE_MAPS_API_KEY': getattr(settings, 'GOOGLE_MAPS_API_KEY', ''),
    }
    return render(request, 'listings/listing_detail.html', context)


# ============================================
# LISTING CREATE (Multi-step)
# ============================================
@login_required
def listing_create(request):
    """Multi-step listing creation view"""

    step = int(request.GET.get('step', 1))
    SESSION_KEY = 'listing_create_data'
    IMAGES_SESSION_KEY = 'listing_temp_images'

    if SESSION_KEY not in request.session:
        request.session[SESSION_KEY] = {}

    if IMAGES_SESSION_KEY not in request.session:
        request.session[IMAGES_SESSION_KEY] = []

    listing_data = request.session[SESSION_KEY]
    temp_images = request.session[IMAGES_SESSION_KEY]

    if request.method == 'POST':

        if step == 1:
            form = Step1BasicInfoForm(request.POST)
            if form.is_valid():
                listing_data['step1'] = {
                    'vehicle_type': form.cleaned_data['vehicle_type'].id,
                    'brand': form.cleaned_data['brand'].id,
                    'model': form.cleaned_data['model'].id,
                    'year': form.cleaned_data['year'],
                    'first_registration_month': form.cleaned_data['first_registration_month'],
                    'vin': form.cleaned_data.get('vin', ''),
                }
                request.session[SESSION_KEY] = listing_data
                request.session.modified = True
                return redirect('/listings/create/?step=2')

        elif step == 2:
            form = Step2MediaForm(request.POST, request.FILES)
            
            # Handle image uploads
            images = request.FILES.getlist('images')
            saved_images = []
            
            for i, image in enumerate(images[:10]):  # Max 10 images
                # Save to temp location
                filename = f"temp/{request.user.id}_{i}_{image.name}"
                path = default_storage.save(filename, ContentFile(image.read()))
                saved_images.append(path)
            
            if saved_images:
                # Clear old temp images
                for old_path in temp_images:
                    try:
                        default_storage.delete(old_path)
                    except:
                        pass
                request.session[IMAGES_SESSION_KEY] = saved_images
            
            if form.is_valid():
                listing_data['step2'] = {
                    'video_url': form.cleaned_data.get('video_url', ''),
                }
                request.session[SESSION_KEY] = listing_data
                request.session.modified = True
                return redirect('/listings/create/?step=3')

        elif step == 3:
            form = Step3VehicleDataForm(request.POST)
            if form.is_valid():
                listing_data['step3'] = {
                    'body_type': form.cleaned_data['body_type'],
                    'fuel_type': form.cleaned_data['fuel_type'].id,
                    'transmission': form.cleaned_data['transmission'].id,
                    'doors': form.cleaned_data['doors'],
                    'condition': form.cleaned_data['condition'],
                    'color': form.cleaned_data.get('color', ''),
                    'mileage': form.cleaned_data['mileage'],
                    'engine_capacity': float(form.cleaned_data['engine_capacity']) if form.cleaned_data.get('engine_capacity') else None,
                    'power': form.cleaned_data.get('power'),
                }
                request.session[SESSION_KEY] = listing_data
                request.session.modified = True
                return redirect('/listings/create/?step=4')

        elif step == 4:
            form = Step4EquipmentForm(request.POST)
            if form.is_valid():
                listing_data['step4'] = {
                    'equipment': [eq.id for eq in form.cleaned_data.get('equipment', [])]
                }
                request.session[SESSION_KEY] = listing_data
                request.session.modified = True
                return redirect('/listings/create/?step=5')

        elif step == 5:
            form = Step5PriceForm(request.POST)
            if form.is_valid():
                listing_data['step5'] = {
                    'price': float(form.cleaned_data['price']),
                    'negotiable': form.cleaned_data.get('negotiable', False),
                }
                request.session[SESSION_KEY] = listing_data
                request.session.modified = True
                return redirect('/listings/create/?step=6')

        elif step == 6:
            form = Step6DescriptionForm(request.POST)
            if form.is_valid():
                listing_data['step6'] = {
                    'description': form.cleaned_data.get('description', ''),
                }
                request.session[SESSION_KEY] = listing_data
                request.session.modified = True
                return redirect('/listings/create/?step=7')

        elif step == 7:
            form = Step7ContactForm(request.POST)
            if form.is_valid():
                listing_data['step7'] = {
                    'country': form.cleaned_data['country'],
                    'city': form.cleaned_data['city'],
                    'phone': form.cleaned_data['phone'],
                    'email': form.cleaned_data['email'],
                    'show_additional_phone': form.cleaned_data.get('show_additional_phone', False),
                    'agree_terms': form.cleaned_data['agree_terms'],
                    'agree_newsletter': form.cleaned_data.get('agree_newsletter', False),
                }

                # Create listing with images
                listing = create_listing_from_session(request.user, listing_data, temp_images)
                
                # Clean up session
                del request.session[SESSION_KEY]
                request.session[IMAGES_SESSION_KEY] = []
                request.session.modified = True

                messages.success(request, 'Listing created successfully!')
                return redirect('listings:listing_detail', pk=listing.pk)

    else:
        if step == 1:
            initial_data = listing_data.get('step1', {})
            if initial_data and 'vehicle_type' in initial_data:
                try:
                    initial_data['vehicle_type'] = VehicleType.objects.get(id=initial_data['vehicle_type'])
                    initial_data['brand'] = Brand.objects.get(id=initial_data['brand'])
                    initial_data['model'] = Model.objects.get(id=initial_data['model'])
                except:
                    pass
            form = Step1BasicInfoForm(initial=initial_data)

        elif step == 2:
            form = Step2MediaForm(initial=listing_data.get('step2', {}))

        elif step == 3:
            initial_data = listing_data.get('step3', {})
            if initial_data and 'fuel_type' in initial_data:
                try:
                    initial_data['fuel_type'] = FuelType.objects.get(id=initial_data['fuel_type'])
                    initial_data['transmission'] = Transmission.objects.get(id=initial_data['transmission'])
                except:
                    pass
            form = Step3VehicleDataForm(initial=initial_data)

        elif step == 4:
            form = Step4EquipmentForm(initial=listing_data.get('step4', {}))

        elif step == 5:
            form = Step5PriceForm(initial=listing_data.get('step5', {}))

        elif step == 6:
            form = Step6DescriptionForm(initial=listing_data.get('step6', {}))

        elif step == 7:
            form = Step7ContactForm(initial=listing_data.get('step7', {}))

        else:
            return redirect('/listings/create/?step=1')

    # Calculate progress percentage
    progress_percent = int((step / 7) * 100)

    context = {
        'form': form,
        'step': step,
        'total_steps': 7,
        'progress_percent': progress_percent,
        'listing_data': listing_data,
        'temp_images_count': len(temp_images),
    }

    return render(request, 'listings/listing_create.html', context)


def create_listing_from_session(user, listing_data, temp_images=None):
    """Create listing from session data"""

    step1 = listing_data.get('step1', {})
    step2 = listing_data.get('step2', {})
    step3 = listing_data.get('step3', {})
    step4 = listing_data.get('step4', {})
    step5 = listing_data.get('step5', {})
    step6 = listing_data.get('step6', {})
    step7 = listing_data.get('step7', {})

    first_registration = None
    if 'year' in step1 and 'first_registration_month' in step1:
        first_registration = date(
            year=step1['year'],
            month=step1['first_registration_month'],
            day=1
        )

    vehicle_type = VehicleType.objects.get(id=step1['vehicle_type'])
    brand = Brand.objects.get(id=step1['brand'])
    model = Model.objects.get(id=step1['model'])
    fuel_type = FuelType.objects.get(id=step3['fuel_type']) if step3.get('fuel_type') else None
    transmission = Transmission.objects.get(id=step3['transmission']) if step3.get('transmission') else None

    title = f"{brand.name} {model.name} {step1['year']}"

    listing = Listing.objects.create(
        seller=user,
        vehicle_type=vehicle_type,
        brand=brand,
        model=model,
        title=title,
        year=step1['year'],
        first_registration=first_registration,
        vin=step1.get('vin', ''),
        video_url=step2.get('video_url', ''),
        body_type=step3.get('body_type', ''),
        fuel_type=fuel_type,
        transmission=transmission,
        doors=step3.get('doors', ''),
        condition=step3.get('condition', 'used'),
        color=step3.get('color', ''),
        mileage=step3.get('mileage', 0),
        engine_capacity=step3.get('engine_capacity'),
        power=step3.get('power'),
        price=step5.get('price', 0),
        negotiable=step5.get('negotiable', False),
        description=step6.get('description', ''),
        city=step7.get('city', ''),
        status='active',
    )

    # Add equipment
    if 'equipment' in step4:
        for equipment_id in step4['equipment']:
            equipment = Equipment.objects.get(id=equipment_id)
            ListingEquipment.objects.create(listing=listing, equipment=equipment)

    # Move temp images to listing
    if temp_images:
        for i, temp_path in enumerate(temp_images):
            try:
                # Read from temp location
                if default_storage.exists(temp_path):
                    with default_storage.open(temp_path, 'rb') as f:
                        content = f.read()
                    
                    # Create new filename
                    ext = os.path.splitext(temp_path)[1]
                    new_filename = f"listings/{listing.pk}/{i}{ext}"
                    
                    # Save to final location
                    final_path = default_storage.save(new_filename, ContentFile(content))
                    
                    # Create ListingImage
                    ListingImage.objects.create(
                        listing=listing,
                        image=final_path,
                        is_main=(i == 0),
                        order=i
                    )
                    
                    # Delete temp file
                    default_storage.delete(temp_path)
            except Exception as e:
                print(f"Error processing image: {e}")

    return listing


# ============================================
# LISTING EDIT
# ============================================
@login_required
def listing_edit(request, pk):
    """Edit listing"""
    listing = get_object_or_404(Listing, pk=pk, seller=request.user)

    if request.method == 'POST':
        messages.success(request, 'Listing updated successfully!')
        return redirect('listings:listing_detail', pk=listing.pk)

    context = {
        'listing': listing,
        'GOOGLE_MAPS_API_KEY': getattr(settings, 'GOOGLE_MAPS_API_KEY', ''),
    }
    return render(request, 'listings/listing_edit.html', context)


# ============================================
# LISTING DELETE
# ============================================
@login_required
def listing_delete(request, pk):
    """Delete listing"""
    listing = get_object_or_404(Listing, pk=pk, seller=request.user)

    if request.method == 'POST':
        listing.delete()
        messages.success(request, 'Listing deleted successfully!')
        return redirect('listings:listing_list')

    context = {'listing': listing}
    return render(request, 'listings/listing_delete_confirm.html', context)


# ============================================
# SAVED LISTINGS
# ============================================
@login_required
def saved_listings(request):
    """View saved/favorite listings"""
    context = {}
    return render(request, 'listings/saved_listings.html', context)


@login_required
def save_listing(request, pk):
    """Save/unsave a listing"""
    listing = get_object_or_404(Listing, pk=pk)
    messages.success(request, 'Listing saved!')
    return redirect('listings:listing_detail', pk=listing.pk)


# ============================================
# SEARCH MAP
# ============================================
def search_map(request):
    """Map view of listings with Google Maps"""
    listings = Listing.objects.filter(status='active').select_related('brand', 'model')
    
    # Get filter values for dropdowns
    makes = Brand.objects.values_list('name', flat=True).distinct().order_by('name')
    models_list = Model.objects.values_list('name', flat=True).distinct().order_by('name')
    years = list(range(2025, 1989, -1))
    
    # Apply filters
    make = request.GET.get('make')
    model = request.GET.get('model')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    year_min = request.GET.get('year_min')
    year_max = request.GET.get('year_max')
    fuel_type = request.GET.get('fuel_type')
    transmission = request.GET.get('transmission')
    
    if make:
        listings = listings.filter(brand__name=make)
    if model:
        listings = listings.filter(model__name=model)
    if price_min:
        listings = listings.filter(price__gte=price_min)
    if price_max:
        listings = listings.filter(price__lte=price_max)
    if year_min:
        listings = listings.filter(year__gte=year_min)
    if year_max:
        listings = listings.filter(year__lte=year_max)
    if fuel_type:
        listings = listings.filter(fuel_type__name__iexact=fuel_type)
    if transmission:
        listings = listings.filter(transmission__name__iexact=transmission)
    
    # Prepare listings JSON for map markers
    listings_json = []
    for listing in listings:
        main_image = None
        first_image = listing.images.first()
        if first_image:
            main_image = first_image.image.url
        
        # Use coordinates or default to Kaunas
        lat = float(listing.latitude) if listing.latitude else 54.8985
        lng = float(listing.longitude) if listing.longitude else 23.9036
        
        listings_json.append({
            'id': listing.pk,
            'title': listing.title,
            'slug': listing.pk,
            'year': listing.year,
            'mileage': listing.mileage,
            'price': float(listing.price),
            'latitude': lat,
            'longitude': lng,
            'main_image': main_image,
        })
    
    context = {
        'listings': listings,
        'listings_json': json.dumps(listings_json),
        'makes': makes,
        'models': models_list,
        'years': years,
        'GOOGLE_MAPS_API_KEY': getattr(settings, 'GOOGLE_MAPS_API_KEY', ''),
    }
    return render(request, 'listings/search_map.html', context)


# ============================================
# IMAGE DELETE
# ============================================
@login_required
def image_delete(request, pk):
    """Delete listing image"""
    image = get_object_or_404(ListingImage, pk=pk, listing__seller=request.user)
    listing_pk = image.listing.pk

    if request.method == 'POST':
        image.delete()
        messages.success(request, 'Image deleted!')
        return redirect('listings:listing_detail', pk=listing_pk)

    return redirect('listings:listing_detail', pk=listing_pk)


# ============================================
# API ENDPOINTS (AJAX)
# ============================================
def get_models_ajax(request):
    """AJAX endpoint to get models by brand ID"""
    brand_id = request.GET.get('brand_id')
    if brand_id:
        models = Model.objects.filter(brand_id=brand_id).values('id', 'name').order_by('name')
        return JsonResponse(list(models), safe=False)
    return JsonResponse([], safe=False)


def get_models_by_brand(request):
    """API endpoint to get models by brand ID or name"""
    brand_id = request.GET.get('brand_id')
    make = request.GET.get('make')
    
    if brand_id:
        models = Model.objects.filter(brand_id=brand_id).values('id', 'name').order_by('name')
        return JsonResponse(list(models), safe=False)
    elif make:
        models = Model.objects.filter(brand__name=make).values('id', 'name').order_by('name')
        return JsonResponse({'models': list(models)})
    
    return JsonResponse({'models': []})