
"""

Single part / parts kit srautas.



Du puslapiai:

  1) parts_category_select  — autogidas.lt-style kategorijų grid + search

  2) parts_listing_create   — galutinė create form'a (po subcategorijos pasirinkimo)

"""



from datetime import date

from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404, redirect

from django.utils.translation import gettext_lazy as _

from django.utils import timezone

from apps.listings import brands as brand_source

from django.contrib import messages

from django.http import JsonResponse

from django.db.models import Q

from django.urls import reverse



from apps.listings.image_validation import split_valid_images
from apps.listings.models import (

    PartCategory, Listing, ListingImage,

    VehicleType, SubCategory, Brand, Model as VehicleModel,

    FuelType, Transmission,

)





# „Dalys“ subkategorijos, kurias aptarnauja ši viena forma. Ji sukasi apie
# PartCategory medį (19 kategorijų / 294 subkategorijos), o ne apie
# SubCategory, todėl tinka visoms trims. Turi sutapti su
# views.PARTS_GENERIC_FORM_SLUGS (ten — pikerio maršrutizavimas).
PARTS_SUBCATEGORY_SLUGS = {
    'single-part-or-kit',
    'single-truck-part',
    'agri-special-parts',
    'accessories-tuning',
}

# Puslapio antraštė pagal pasirinktą šaką — anksčiau visoms buvo
# užrašyta „Car, van parts", nors formą dalinasi keturios.
PARTS_PAGE_TITLES = {
    'single-part-or-kit': _('Car, van parts'),
    'single-truck-part': _('Sunkiojo transporto dalys'),
    'agri-special-parts': _('Žemės ūkio, spec. dalys'),
    'accessories-tuning': _('Aksesuarai, Tuning'),
}

DEFAULT_PARTS_SUBCATEGORY = 'single-part-or-kit'


# Kuri markių šeima kuriai dalių šakai. Autogide dalių sąrašas sutampa su
# transporto priemonės sąrašu, todėl šeima imama iš brand_registry.
# Šeimoms be modelių kaskados modelis rašomas į laisvo teksto lauką.
MODEL_TEXT_FIELD_BY_SCOPE = {
    'trucks': 'truck_model_text',
    'agriculture': 'agri_model_text',
}


def _parts_scope(request, part_subcategory=None, listing=None):
    """Šeimos raktas pagal pasirinktą „Dalys" šaką."""
    sub_slug = (
        request.POST.get('for', '') or request.GET.get('for', '')
    ).strip()
    if sub_slug not in PARTS_SUBCATEGORY_SLUGS and listing is not None:
        sub_slug = getattr(listing.subcategory, 'slug', '') or ''
    if sub_slug not in PARTS_SUBCATEGORY_SLUGS:
        sub_slug = DEFAULT_PARTS_SUBCATEGORY
    return brand_source.scope_for(subcategory_slug=sub_slug) or 'cars'



@login_required

def parts_category_select(request):

    """Step 1: Kategorijų grid (Lighting, Engine, Brakes, ...)."""

    categories = PartCategory.objects.filter(

        level=PartCategory.LEVEL_CATEGORY,

        is_active=True,

    ).order_by('order', 'name_en')



    # ?for=<subcategory slug> — kuri „Dalys“ subkategorija buvo pasirinkta
    # pikeryje. Perduodama toliau į formą, kad skelbimas neatsidurtų
    # „Atskira dalis / komplektas“, kai iš tikrųjų rinktasi „Aksesuarai, Tuning“.
    for_sub = (request.GET.get('for', '') or '').strip()

    context = {

        'categories': categories,

        'page_title': PARTS_PAGE_TITLES.get(
            for_sub if for_sub in PARTS_SUBCATEGORY_SLUGS else DEFAULT_PARTS_SUBCATEGORY,
            _("Car, van parts"),
        ),

        'for_sub': for_sub if for_sub in PARTS_SUBCATEGORY_SLUGS else '',

    }

    return render(request, 'listings/parts_category_select.html', context)





def parts_subtree_ajax(request):

    """AJAX endpoint — grąžina grupių + subcategorijų medį."""

    cat_slug = request.GET.get('category_slug', '').strip()

    if not cat_slug:

        return JsonResponse({'error': 'category_slug required'}, status=400)



    try:

        category = PartCategory.objects.get(

            slug=cat_slug,

            level=PartCategory.LEVEL_CATEGORY,

        )

    except PartCategory.DoesNotExist:

        return JsonResponse({'error': 'Category not found'}, status=404)



    groups = PartCategory.objects.filter(

        parent=category,

        level=PartCategory.LEVEL_GROUP,

        is_active=True,

    ).prefetch_related('children').order_by('order', 'name_en')



    data = []

    for group in groups:

        subs = group.children.filter(

            level=PartCategory.LEVEL_SUBCATEGORY,

            is_active=True,

        ).order_by('order', 'name_en')

        data.append({

            'name': group.name_en,

            'slug': group.slug,

            'children': [

                {'name': sub.name_en, 'slug': sub.slug}

                for sub in subs

            ],

        })



    return JsonResponse({'groups': data, 'category_name': category.name_en})





def parts_search_ajax(request):

    """AJAX endpoint — search bar'as."""

    query = request.GET.get('q', '').strip()

    if len(query) < 2:

        return JsonResponse({'results': []})



    subs = PartCategory.objects.filter(

        level=PartCategory.LEVEL_SUBCATEGORY,

        is_active=True,

    ).filter(

        Q(name_en__icontains=query) | Q(name_lt__icontains=query)

    ).select_related('parent', 'parent__parent')[:20]



    results = []

    for sub in subs:

        breadcrumb = sub.breadcrumb_text(separator=" › ")

        results.append({

            'name': sub.name_en,

            'slug': sub.slug,

            'breadcrumb': breadcrumb,

        })



    return JsonResponse({'results': results})





def _int_or_none(value):

    if value in (None, ''):

        return None

    try:

        return int(value)

    except (ValueError, TypeError):

        return None





def _float_or_none(value):

    if value in (None, ''):

        return None

    try:

        return float(value)

    except (ValueError, TypeError):

        return None





@login_required
def parts_listing_create(request):
    """
    Step 2: Galutinė parts create/edit form'a.
    URL CREATE: /create/parts/form/?sub=<slug>
    URL EDIT:   /create/parts/form/?edit=<pk>
    """
    edit_pk_str = request.GET.get('edit', '').strip() or request.POST.get('edit', '').strip()
    edit_pk = _int_or_none(edit_pk_str)
    is_edit_mode = bool(edit_pk)

    listing = None
    part_subcategory = None

    if is_edit_mode:
        listing = get_object_or_404(Listing, pk=edit_pk, seller=request.user)
        if not listing.vehicle_type or listing.vehicle_type.slug != 'parts':
            messages.error(request, 'Parts edit is only available for parts listings.')
            return redirect('listing_edit_hub', pk=edit_pk)
        part_subcategory = listing.part_category
        if part_subcategory is None:
            messages.error(request, 'Part category missing on this listing.')
            return redirect('my_listings')
    else:
        sub_slug = request.GET.get('sub', '').strip() or request.POST.get('sub', '').strip()
        if not sub_slug:
            return redirect('parts_category_select')
        try:
            part_subcategory = PartCategory.objects.get(
                slug=sub_slug,
                level=PartCategory.LEVEL_SUBCATEGORY,
            )
        except PartCategory.DoesNotExist:
            return redirect('parts_category_select')

    if request.method == 'POST':
        errors = []

        title = (request.POST.get('title', '') or '').strip()
        if not title:
            title = part_subcategory.name_en

        condition = request.POST.get('condition', '')
        if condition not in ('new', 'used', 'refurbished', 'damaged'):
            errors.append('Condition is required')

        price = _float_or_none(request.POST.get('price'))
        if price is None or price <= 0:
            errors.append('Price is required')

        brand_id = _int_or_none(request.POST.get('brand'))
        model_id = _int_or_none(request.POST.get('model'))

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

        if not is_edit_mode and not request.POST.get('agree_terms'):
            errors.append('You must agree to the terms')

        if errors:
            for e in errors:
                messages.error(request, e)
            return _render_parts_form(request, part_subcategory, errors=errors,
                                      listing=listing, is_edit_mode=is_edit_mode)

        if is_edit_mode:
            target = listing
        else:
            try:
                parts_vt = VehicleType.objects.get(slug='parts')
            except VehicleType.DoesNotExist:
                messages.error(request, 'Parts vehicle type not configured.')
                return redirect('parts_category_select')

            # Kuri „Dalys“ subkategorija buvo pasirinkta pikeryje. Anksčiau
            # čia buvo hardcodinta 'single-part-or-kit', todėl „Žemės ūkio,
            # spec. dalys“ ir „Aksesuarai, Tuning“ būtų sukritusios į vieną
            # (ta pati klaida kaip trucks_views subcategory).
            for_slug = (
                request.POST.get('for', '') or request.GET.get('for', '')
            ).strip()
            if for_slug not in PARTS_SUBCATEGORY_SLUGS:
                for_slug = DEFAULT_PARTS_SUBCATEGORY
            single_part_sub = SubCategory.objects.filter(
                vehicle_type=parts_vt, slug=for_slug,
            ).first()

            target = Listing(
                seller=request.user,
                vehicle_type=parts_vt,
                subcategory=single_part_sub,
                part_category=part_subcategory,
                year=date.today().year,
                mileage=0,
                status='draft',
            )

        target.title = title[:200]
        target.oem_code = (request.POST.get('oem_code', '') or '').strip()[:50]
        target.condition = condition
        target.price = price
        target.negotiable = request.POST.get('negotiable') == 'on'
        target.description = request.POST.get('description', '') or ''
        target.country = country
        if hasattr(Listing, 'state'):
            target.state = state
        target.city = city or '—'
        target.postal_code = request.POST.get('postal_code', '') or ''
        target.address = request.POST.get('address', '') or ''

        if brand_id:
            try:
                target.brand = Brand.objects.get(pk=brand_id)
            except Brand.DoesNotExist:
                pass

        post_scope = _parts_scope(request, part_subcategory, listing)
        text_field = MODEL_TEXT_FIELD_BY_SCOPE.get(post_scope)
        if text_field:
            # Autogide šioms šeimoms modelis yra laisvas tekstas — kaskados
            # duomenų nėra nei pas juos, nei pas mus.
            setattr(target, text_field,
                    (request.POST.get('model_text', '') or '').strip()[:100])
        elif model_id:
            try:
                target.model = VehicleModel.objects.get(pk=model_id)
            except VehicleModel.DoesNotExist:
                pass

        year_from = _int_or_none(request.POST.get('year_from'))
        if year_from:
            target.year = year_from

        fuel_id = _int_or_none(request.POST.get('fuel_type'))
        if fuel_id:
            try:
                target.fuel_type = FuelType.objects.get(pk=fuel_id)
            except FuelType.DoesNotExist:
                pass

        trans_id = _int_or_none(request.POST.get('transmission'))
        if trans_id:
            try:
                target.transmission = Transmission.objects.get(pk=trans_id)
            except Transmission.DoesNotExist:
                pass

        engine_cap = _float_or_none(request.POST.get('engine_capacity'))
        if engine_cap:
            target.engine_capacity = engine_cap

        power = _int_or_none(request.POST.get('power'))
        if power:
            target.power = power

        target.body_type = request.POST.get('body_type', '') or ''
        target.doors = request.POST.get('doors', '') or ''
        target.drive_type = request.POST.get('drive_type', '') or ''
        target.color = request.POST.get('color', '') or ''
        target.modification = (request.POST.get('modification', '') or '').strip()[:100]
        target.version = (request.POST.get('version', '') or '').strip()[:100]
        target.color_code = (request.POST.get('color_code', '') or '').strip()[:30]
        target.engine_code = (request.POST.get('engine_code', '') or '').strip()[:30]
        target.gearbox_code = (request.POST.get('transmission_code', '') or '').strip()[:30]

        if hasattr(request.user, 'profile'):
            request.user.profile.phone_number = phone
            request.user.profile.save(update_fields=['phone_number'])

        try:
            target.save()
        except Exception as e:
            messages.error(request, f'Save failed: {str(e)[:200]}')
            return _render_parts_form(request, part_subcategory, errors=[str(e)],
                                      listing=listing, is_edit_mode=is_edit_mode)

        images, _image_errors = split_valid_images(request.FILES.getlist('images'))
        for _err in _image_errors:
            messages.error(request, _err)
        if is_edit_mode:
            existing_images = target.images.all()
            max_order = existing_images.aggregate(Max('order'))['order__max'] or -1
            for i, image in enumerate(images[:10]):
                try:
                    ListingImage.objects.create(
                        listing=target,
                        image=image,
                        is_main=False,
                        order=max_order + i + 1,
                    )
                except Exception as e:
                    print(f"[parts_edit] image upload failed: {e}")
            messages.success(request, 'Listing updated successfully.')
            return redirect('listing_edit_hub', pk=target.pk)
        else:
            for i, image in enumerate(images[:10]):
                try:
                    ListingImage.objects.create(
                        listing=target,
                        image=image,
                        is_main=(i == 0),
                        order=i,
                    )
                except Exception as e:
                    print(f"[parts_create] image upload failed: {e}")
            return redirect('listing_select_plan', pk=target.pk)

    return _render_parts_form(request, part_subcategory, listing=listing, is_edit_mode=is_edit_mode)


def _render_parts_form(request, part_subcategory, errors=None, listing=None, is_edit_mode=False):
    """Helper to render the parts create/edit form with context."""
    user_phone = ''
    if hasattr(request.user, 'profile') and request.user.profile.phone_number:
        user_phone = request.user.profile.phone_number

    # Markės — iš bendro šaltinio pagal šeimą. Anksčiau čia visada buvo
    # automobilių markės, todėl „Sunkiojo transporto dalis", „Žemės ūkio,
    # spec. dalys" ir „Aksesuarai, Tuning" rodė 200 automobilių markių.
    scope = _parts_scope(request, part_subcategory, listing)
    brands = brand_source.brands_qs(scope)
    scope_has_models = brand_source.has_models(scope)

    fuel_types = FuelType.objects.all().order_by('name')
    transmissions = Transmission.objects.all().order_by('name')

    current_year = timezone.now().year
    years = list(range(current_year + 1, 1949, -1))

    if request.method == 'POST':
        form_data = request.POST
    elif is_edit_mode and listing is not None:
        form_data = {
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
            'brand': str(listing.brand_id) if listing.brand_id else '',
            'model': str(listing.model_id) if listing.model_id else '',
            'model_text': getattr(
                listing, MODEL_TEXT_FIELD_BY_SCOPE.get(scope, ''), '') or '',
            'year_from': str(listing.year) if listing.year else '',
            'fuel_type': str(listing.fuel_type_id) if listing.fuel_type_id else '',
            'transmission': str(listing.transmission_id) if listing.transmission_id else '',
            'engine_capacity': str(listing.engine_capacity) if listing.engine_capacity else '',
            'power': str(listing.power) if listing.power else '',
            'body_type': listing.body_type or '',
            'doors': listing.doors or '',
            'drive_type': listing.drive_type or '',
            'color': listing.color or '',
            'modification': getattr(listing, 'modification', '') or '',
            'version': getattr(listing, 'version', '') or '',
            'color_code': getattr(listing, 'color_code', '') or '',
            'engine_code': getattr(listing, 'engine_code', '') or '',
            'transmission_code': getattr(listing, 'gearbox_code', '') or '',
            'phone': user_phone,
        }
    else:
        form_data = {}

    context = {
        'subcategory': part_subcategory,
        'breadcrumb': part_subcategory.breadcrumb_text(separator=" › "),
        'category_name': part_subcategory.parent.parent.name_en if part_subcategory.parent and part_subcategory.parent.parent else '',
        'group_name': part_subcategory.parent.name_en if part_subcategory.parent else '',
        'sub_name': part_subcategory.name_en,
        'sub_slug': part_subcategory.slug,
        'for_sub': (
            request.POST.get('for', '') or request.GET.get('for', '')
        ).strip(),
        'brands': brands,
        'brand_scope': scope,
        'scope_has_models': scope_has_models,
        'fuel_types': fuel_types,
        'transmissions': transmissions,
        'years': years,
        'user_phone': user_phone,
        'user_email': request.user.email,
        'form_data': form_data,
        'errors': errors or [],
        'is_edit_mode': is_edit_mode,
        'edit_listing_id': listing.pk if listing else None,
        'existing_images': listing.images.all() if (is_edit_mode and listing) else [],
        'condition_choices': [
            ('new', 'New'),
            ('used', 'Used'),
            ('refurbished', 'Refurbished'),
            ('damaged', 'Damaged'),
        ],
        'country_choices': [
            ('US', 'United States'),
            ('LT', 'Lithuania'),
        ],
        'us_states': Listing.US_STATE_CHOICES if hasattr(Listing, 'US_STATE_CHOICES') else [],
    }

    return render(request, 'listings/parts_listing_create.html', context)
