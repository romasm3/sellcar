from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Listing, ListingImage, SavedListing, Brand, Model
from .forms import ListingCreateForm, ListingImageForm, ListingSearchForm
from .filters import ListingFilter


def home(request):
    """Pagrindinis puslapis"""
    listings = Listing.objects.filter(status="active").order_by("-created_at")[:8]

    context = {
        "listings": listings,
    }
    return render(request, "listings/home.html", context)


def listing_list(request):
    """Skelbimų sąrašas su paieška ir filtravimu"""
    listings = Listing.objects.filter(status="active")

    # Paieška
    search_query = request.GET.get("search", "")
    if search_query:
        listings = listings.filter(
            Q(title__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(brand__name__icontains=search_query)
            | Q(model__name__icontains=search_query)
        )

    # Filtravimas
    listing_filter = ListingFilter(request.GET, queryset=listings)
    listings = listing_filter.qs

    # Rūšiavimas
    ordering = request.GET.get("ordering", "-created_at")
    listings = listings.order_by(ordering)

    # Paginacija
    paginator = Paginator(listings, 12)  # 12 skelbimų per puslapį
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "filter": listing_filter,
        "search_query": search_query,
        "total_count": listings.count(),
    }
    return render(request, "listings/listing_list.html", context)


def listing_detail(request, slug):
    """Skelbimo detalus vaizdas"""
    listing = get_object_or_404(Listing, slug=slug)

    # Padidinti peržiūrų skaičių
    listing.views += 1
    listing.save(update_fields=["views"])

    # Panašūs skelbimai
    similar_listings = Listing.objects.filter(
        brand=listing.brand, status="active"
    ).exclude(id=listing.id)[:4]

    # Ar vartotojas išsaugojo šį skelbimą?
    is_saved = False
    if request.user.is_authenticated:
        is_saved = SavedListing.objects.filter(
            user=request.user, listing=listing
        ).exists()

    context = {
        "listing": listing,
        "similar_listings": similar_listings,
        "is_saved": is_saved,
    }
    return render(request, "listings/listing_detail.html", context)


@login_required
def listing_create(request):
    """Naujo skelbimo kūrimas"""
    if request.method == "POST":
        form = ListingCreateForm(request.POST)
        images = request.FILES.getlist("images")

        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.save()

            # Išsaugoti nuotraukas
            for idx, image in enumerate(images):
                ListingImage.objects.create(
                    listing=listing,
                    image=image,
                    is_main=(idx == 0),  # Pirmą nuotrauką padaryti pagrindine
                )

            messages.success(request, "Skelbimas sėkmingai sukurtas!")
            return redirect("listings:listing_detail", slug=listing.slug)
    else:
        form = ListingCreateForm()

    context = {
        "form": form,
    }
    return render(request, "listings/listing_create.html", context)


@login_required
def listing_edit(request, slug):
    """Skelbimo redagavimas"""
    listing = get_object_or_404(Listing, slug=slug, seller=request.user)

    if request.method == "POST":
        form = ListingCreateForm(request.POST, instance=listing)
        images = request.FILES.getlist("images")

        if form.is_valid():
            form.save()

            # Pridėti naujas nuotraukas
            for image in images:
                ListingImage.objects.create(listing=listing, image=image)

            messages.success(request, "Skelbimas atnaujintas!")
            return redirect("listings:listing_detail", slug=listing.slug)
    else:
        form = ListingCreateForm(instance=listing)

    context = {
        "form": form,
        "listing": listing,
    }
    return render(request, "listings/listing_edit.html", context)


@login_required
def listing_delete(request, slug):
    """Skelbimo ištrynimas"""
    listing = get_object_or_404(Listing, slug=slug, seller=request.user)

    if request.method == "POST":
        listing.delete()
        messages.success(request, "Skelbimas ištrintas!")
        return redirect("accounts:profile")

    context = {
        "listing": listing,
    }
    return render(request, "listings/listing_delete.html", context)


@login_required
def image_delete(request, pk):
    """Nuotraukos ištrynimas"""
    image = get_object_or_404(ListingImage, pk=pk, listing__seller=request.user)
    listing_slug = image.listing.slug

    if request.method == "POST":
        image.delete()
        messages.success(request, "Nuotrauka ištrinta!")

    return redirect("listings:listing_edit", slug=listing_slug)


@login_required
def save_listing(request, slug):
    """Išsaugoti skelbimą (pridėti į favorites)"""
    listing = get_object_or_404(Listing, slug=slug)

    saved, created = SavedListing.objects.get_or_create(
        user=request.user, listing=listing
    )

    if created:
        messages.success(request, "Skelbimas išsaugotas!")
    else:
        saved.delete()
        messages.success(request, "Skelbimas pašalintas iš išsaugotų!")

    return redirect("listings:listing_detail", slug=slug)


@login_required
def saved_listings(request):
    """Vartotojo išsaugoti skelbimai"""
    saved = SavedListing.objects.filter(user=request.user).select_related("listing")

    context = {
        "saved_listings": saved,
    }
    return render(request, "listings/saved_listings.html", context)


def search_map(request):
    """Paieška su žemėlapiu"""
    listings = Listing.objects.filter(
        status="active", latitude__isnull=False, longitude__isnull=False
    )

    # Filtravimas
    listing_filter = ListingFilter(request.GET, queryset=listings)
    listings = listing_filter.qs

    # Konvertuoti į JSON formatą žemėlapiui
    listings_data = []
    for listing in listings:
        listings_data.append(
            {
                "id": listing.id,
                "title": listing.title,
                "price": float(listing.price),
                "lat": float(listing.latitude),
                "lng": float(listing.longitude),
                "url": listing.slug,
                "image": listing.get_main_image(),
                "year": listing.year,
                "mileage": listing.mileage,
            }
        )

    context = {
        "listings_data": listings_data,
        "filter": listing_filter,
    }
    return render(request, "listings/search_map.html", context)


def get_models_by_brand(request):
    """AJAX: Gauti modelius pagal markę"""
    brand_id = request.GET.get("brand_id")
    models = Model.objects.filter(brand_id=brand_id).values("id", "name")
    return JsonResponse(list(models), safe=False)
