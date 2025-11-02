from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .forms import (
    Step1BasicInfoForm,
    Step2MediaForm,
    Step3VehicleDataForm,
    Step4EquipmentForm,
    Step5PriceForm,
    Step6DescriptionForm,
    Step7ContactForm,
)
from .models import Listing, ListingImage, Model, Equipment, ListingEquipment, VehicleType, Brand, FuelType, Transmission
from datetime import date


@login_required
def listing_create(request):
    """Multi-step listing creation view"""

    # Get step from GET parameter or start from 1
    step = int(request.GET.get('step', 1))

    # Session data keys
    SESSION_KEY = 'listing_create_data'

    # Initialize session data
    if SESSION_KEY not in request.session:
        request.session[SESSION_KEY] = {}

    listing_data = request.session[SESSION_KEY]

    # POST request handling
    if request.method == 'POST':

        # STEP 1
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
                return redirect(f'/listings/create/?step=2')

        # STEP 2
        elif step == 2:
            form = Step2MediaForm(request.POST)
            if form.is_valid():
                listing_data['step2'] = {
                    'video_url': form.cleaned_data.get('video_url', ''),
                }
                request.session[SESSION_KEY] = listing_data

                # Handle image uploads
                if request.FILES.getlist('images'):
                    # Temporarily store images in session
                    # Actual upload will happen after full listing creation
                    pass

                return redirect(f'/listings/create/?step=3')

        # STEP 3
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
                return redirect(f'/listings/create/?step=4')

        # STEP 4
        elif step == 4:
            form = Step4EquipmentForm(request.POST)
            if form.is_valid():
                listing_data['step4'] = {
                    'equipment': [eq.id for eq in form.cleaned_data.get('equipment', [])]
                }
                request.session[SESSION_KEY] = listing_data
                return redirect(f'/listings/create/?step=5')

        # STEP 5
        elif step == 5:
            form = Step5PriceForm(request.POST)
            if form.is_valid():
                listing_data['step5'] = {
                    'price': float(form.cleaned_data['price']),
                    'negotiable': form.cleaned_data.get('negotiable', False),
                }
                request.session[SESSION_KEY] = listing_data
                return redirect(f'/listings/create/?step=6')

        # STEP 6
        elif step == 6:
            form = Step6DescriptionForm(request.POST)
            if form.is_valid():
                listing_data['step6'] = {
                    'description': form.cleaned_data.get('description', ''),
                }
                request.session[SESSION_KEY] = listing_data
                return redirect(f'/listings/create/?step=7')

        # STEP 7 - Final
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

                # Create listing
                listing = create_listing_from_session(request.user, listing_data)

                # Clear session
                del request.session[SESSION_KEY]

                messages.success(request, 'Listing created successfully!')
                return redirect('listings:listing_detail', pk=listing.pk)

    # GET requests - display form
    else:
        if step == 1:
            initial_data = listing_data.get('step1', {})
            # Convert IDs back to objects
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

    context = {
        'form': form,
        'step': step,
        'total_steps': 7,
        'listing_data': listing_data,
    }

    return render(request, 'listings/listing_create.html', context)


def create_listing_from_session(user, listing_data):
    """Create listing from session data"""

    # Combine all data
    step1 = listing_data.get('step1', {})
    step2 = listing_data.get('step2', {})
    step3 = listing_data.get('step3', {})
    step4 = listing_data.get('step4', {})
    step5 = listing_data.get('step5', {})
    step6 = listing_data.get('step6', {})
    step7 = listing_data.get('step7', {})

    # Create first_registration date
    first_registration = None
    if 'year' in step1 and 'first_registration_month' in step1:
        first_registration = date(
            year=step1['year'],
            month=step1['first_registration_month'],
            day=1
        )

    # Get foreign key objects
    vehicle_type = VehicleType.objects.get(id=step1['vehicle_type'])
    brand = Brand.objects.get(id=step1['brand'])
    model = Model.objects.get(id=step1['model'])
    fuel_type = FuelType.objects.get(id=step3['fuel_type']) if step3.get('fuel_type') else None
    transmission = Transmission.objects.get(id=step3['transmission']) if step3.get('transmission') else None

    # Create title
    title = f"{brand.name} {model.name} {step1['year']}"

    # Create listing
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

    return listing


# AJAX endpoint for getting models
def get_models_ajax(request):
    """AJAX endpoint to get models by brand"""
    brand_id = request.GET.get('brand_id')
    models = Model.objects.filter(brand_id=brand_id).values('id', 'name')
    return JsonResponse(list(models), safe=False)


# Simple listing detail view
def listing_detail(request, pk):
    """Listing detail view"""
    listing = get_object_or_404(Listing, pk=pk)

    # Increment views count
    listing.views_count += 1
    listing.save(update_fields=['views_count'])

    context = {
        'listing': listing,
    }
    return render(request, 'listings/listing_detail.html', context)


# Additional views - NOTE: These are at module level, NOT indented inside listing_detail
def listing_list(request):
    """List all active listings"""
    listings = Listing.objects.filter(status='active').order_by('-created_at')
    context = {'listings': listings}
    return render(request, 'listings/listing_list.html', context)


@login_required
def listing_edit(request, pk):
    """Edit listing"""
    listing = get_object_or_404(Listing, pk=pk, seller=request.user)

    if request.method == 'POST':
        messages.success(request, 'Listing updated successfully!')
        return redirect('listings:listing_detail', pk=listing.pk)

    context = {'listing': listing}
    return render(request, 'listings/listing_edit.html', context)


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


def search_map(request):
    """Map view of listings"""
    listings = Listing.objects.filter(status='active')
    context = {'listings': listings}
    return render(request, 'listings/search_map.html', context)


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


def get_models_by_brand(request):
    """API endpoint to get models by brand"""
    brand_id = request.GET.get('brand_id')
    models = Model.objects.filter(brand_id=brand_id).values('id', 'name')
    return JsonResponse(list(models), safe=False)
