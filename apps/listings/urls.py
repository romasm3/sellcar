from django.urls import path
from . import views

app_name = "listings"

urlpatterns = [
    path("", views.listing_list, name="listing_list"),
    path("create/", views.listing_create, name="listing_create"),
    path("saved/", views.saved_listings, name="saved_listings"),
    path("map/", views.search_map, name="search_map"),
    path("api/models/", views.get_models_by_brand, name="get_models_by_brand"),
    path('ajax/get-models/', views.get_models_ajax, name='get_models_ajax'),
    path("<int:pk>/", views.listing_detail, name="listing_detail"),
    path("<int:pk>/edit/", views.listing_edit, name="listing_edit"),
    path("<int:pk>/delete/", views.listing_delete, name="listing_delete"),
    path("<int:pk>/save/", views.save_listing, name="save_listing"),
    path("image/<int:pk>/delete/", views.image_delete, name="image_delete"),
]
