from django.urls import path
from . import views

app_name = "listings"

urlpatterns = [
    path("", views.home, name="home"),
    path("listings/", views.listing_list, name="listing_list"),
    path("listings/create/", views.listing_create, name="listing_create"),
    path("listings/saved/", views.saved_listings, name="saved_listings"),
    path("listings/map/", views.search_map, name="search_map"),
    path("listings/<slug:slug>/", views.listing_detail, name="listing_detail"),
    path("listings/<slug:slug>/edit/", views.listing_edit, name="listing_edit"),
    path("listings/<slug:slug>/delete/", views.listing_delete, name="listing_delete"),
    path("listings/<slug:slug>/save/", views.save_listing, name="save_listing"),
    path("image/<int:pk>/delete/", views.image_delete, name="image_delete"),
    path("api/models/", views.get_models_by_brand, name="get_models_by_brand"),
]
