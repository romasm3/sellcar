from django.urls import path
from . import views
from . import views_help
from . import motorcycles_views
from . import motogear_views
from . import trucks_views
from . import car_for_parts_views
from . import moto_for_parts_views
from . import parts_views
from . import moto_part_views
from . import truck_for_parts_views
from apps.listings import boats_views
from . import trailers_views
from . import agriculture_views
from . import construction_views
from . import loading_views
from . import select_views
from . import forestry_views
from . import camping_views
from . import rental_views
from . import services_views
from . import electronics_views
from . import bicycles_views
from . import wheels_views

urlpatterns = [
    path('upgrade/', views.listing_upgrade, name='listing_upgrade'),
    path('listings/<int:pk>/select-plan/', views.listing_select_plan, name='listing_select_plan'),
    path('listings/<int:pk>/pay-plan/<str:plan_code>/', views.listing_pay_plan, name='listing_pay_plan'),
    path('ajax/validate-promo-code/', views.validate_promo_code_ajax, name='validate_promo_code_ajax'),
    # ─── Browse ───
    path("", views.listing_list, name="listing_list"),
    path("", views.home, name="home"),
    path('browse/', views.listing_list, name='browse_listings'),
    path('v2/', views.listing_list_v2, name='listing_list_v2'),
    path("map/", views.search_map, name="search_map"),

    # ─── Create ───
    path("create/", views.listing_create, name="listing_create"),
    path("create/cars/quick/", views.listing_create_cars_quick, name="listing_create_cars_quick"),
    path("create/motorcycle/", motorcycles_views.motorcycle_listing_create, name="motorcycle_listing_create"),
    path("create/trucks/", trucks_views.trucks_listing_create, name="trucks_listing_create"),
    path("create/boats/", boats_views.boats_listing_create, name="boats_listing_create"),
    path("create/trailers/", trailers_views.trailers_listing_create, name="trailers_listing_create"),
    path("create/agriculture/", agriculture_views.agriculture_listing_create, name="agriculture_listing_create"),
    path("create/construction/", construction_views.construction_listing_create, name="construction_listing_create"),
    path("create/construction/attachment/", construction_views.construction_attachment_create, name="construction_attachment_create"),
    path("create/loading-equipment/", loading_views.loading_listing_create, name="loading_listing_create"),
    path("create/forestry/", forestry_views.forestry_listing_create, name="forestry_listing_create"),
    path("create/camping-houses/", camping_views.camping_listing_create, name="camping_listing_create"),
    path("create/rental/car/", rental_views.rental_car_create, name="rental_car_create"),
    path("create/rental/moto/", rental_views.rental_moto_create, name="rental_moto_create"),
    path("create/rental/minibus/", rental_views.rental_minibus_create, name="rental_minibus_create"),
    path("create/rental/heavy/", rental_views.rental_heavy_create, name="rental_heavy_create"),
    path("create/services/", services_views.services_listing_create, name="services_listing_create"),
    path("create/electronics/", electronics_views.electronics_listing_create, name="electronics_listing_create"),
    path("create/bicycles/", bicycles_views.bicycles_listing_create, name="bicycles_listing_create"),
    path("create/minibuses/", views.minibus_category_choice, name="minibus_category_choice"),
    path("create/wheels/", wheels_views.wheels_create, name="wheels_create"),
    path("create/tyres/", wheels_views.tyres_create, name="tyres_create"),
    path("create/rims/", wheels_views.rims_create, name="rims_create"),
    path("browse/wheels/", wheels_views.wheels_list, name="wheels_list"),
    path("search/wheels/advanced/", wheels_views.wheels_advanced_search, name="wheels_advanced_search"),
    path("ajax/wheels-search-count/", wheels_views.wheels_search_count_ajax, name="wheels_search_count_ajax"),
    path("wheels/<int:pk>/save/", wheels_views.wheels_save_toggle, name="wheels_save_toggle"),
    path("wheels/<int:pk>/edit/", wheels_views.wheels_edit, name="wheels_edit"),
    path("wheels/<int:pk>/delete/", wheels_views.wheels_delete, name="wheels_delete"),
    path("wheels/<int:pk>/activate/", wheels_views.wheels_activate, name="wheels_activate"),
    path("wheels/<int:pk>/", wheels_views.wheels_detail, name="wheels_detail"),

    # ─── PARTS (Single part / parts kit) ───
    path("create/moto-part/", moto_part_views.moto_part_create, name="moto_part_create"),
    path("create/parts/", parts_views.parts_category_select, name="parts_category_select"),
    path("create/parts/form/", parts_views.parts_listing_create, name="parts_listing_create"),
    path("ajax/parts-subtree/", parts_views.parts_subtree_ajax, name="parts_subtree_ajax"),
    path("ajax/parts-search/", parts_views.parts_search_ajax, name="parts_search_ajax"),
    path("browse/moto-parts/", moto_part_views.moto_parts_browse, name="moto_parts_browse"),

    # ─── Misc ───
    path("contact/", views.contact, name="contact"),
    path("faq/", views.faq, name="faq"),
    path("saved/", views.saved_listings, name="saved_listings"),
    path('searches/', views.saved_searches_list, name='saved_searches_list'),

    # ─── HELP CENTER ───
    path('help/', views_help.help_center, name='help_center'),
    path('help/whats-new/', views_help.whats_new, name='whats_new'),
    path('help/market-trends/', views_help.market_trends, name='market_trends'),
    path('help/tips/', views_help.tips_guides, name='tips_guides'),
    path('help/pricing/', views_help.pricing, name='pricing'),
    path('help/valuation/', views_help.valuation, name='valuation'),
    path('help/advertise/', views_help.advertise, name='advertise'),
    path('help/about/', views_help.about_us, name='about_us'),
    path('help/contact/', views_help.contact_page, name='contact_page'),
    path('help/terms/', views_help.terms, name='terms'),
    path('help/privacy/', views_help.privacy, name='privacy'),
    path('help/cookies/', views_help.cookies, name='cookies'),

    # ─── AJAX (cars) ───
    path("api/models/", views.get_models_by_brand, name="get_models_by_brand"),
    path('ajax/get-models/', views.get_models_ajax, name='get_models_ajax'),
    path('ajax/get-subcategories/', views.get_subcategories_ajax, name='get_subcategories_ajax'),
    path('ajax/get-submodels/', views.get_submodels_ajax, name='get_submodels'),
    path('ajax/save-step3-data/', views.save_step3_data, name='save_step3_data'),
    path('ajax/save-cars-draft/', views.save_cars_draft_ajax, name='save_cars_draft_ajax'),
    path('ajax/upload-draft-images/', views.upload_draft_images_ajax, name='upload_draft_images_ajax'),
    path('ajax/upload-listing-images/<int:pk>/', views.upload_listing_images_ajax, name='upload_listing_images_ajax'),
    path('ajax/reorder-listing-images/<int:pk>/', views.reorder_listing_images_ajax, name='reorder_listing_images_ajax'),
    path('ajax/rotate-listing-image/<int:pk>/', views.rotate_listing_image_ajax, name='rotate_listing_image_ajax'),
    path('ajax/delete-draft-image/<int:pk>/', views.delete_draft_image_ajax, name='delete_draft_image_ajax'),
    path('ajax/reorder-draft-images/', views.reorder_draft_images_ajax, name='reorder_draft_images_ajax'),

    # ─── AJAX (motorcycles) ───
    path('ajax/get-motorcycle-brands/', motorcycles_views.get_motorcycle_brands_ajax, name='get_motorcycle_brands_ajax'),
    path('ajax/get-motorcycle-models/', motorcycles_views.get_motorcycle_models_ajax, name='get_motorcycle_models_ajax'),
    path('ajax/save-motorcycle-draft/', motorcycles_views.save_motorcycle_draft_ajax, name='save_motorcycle_draft_ajax'),
    path('ajax/upload-moto-draft-images/', motorcycles_views.upload_moto_draft_images_ajax, name='upload_moto_draft_images'),
    path('ajax/reorder-moto-draft-images/', motorcycles_views.reorder_moto_draft_images_ajax, name='reorder_moto_draft_images'),
    path('ajax/delete-moto-listing-image/<int:pk>/', motorcycles_views.delete_listing_image_ajax, name='delete_moto_listing_image'),
    path('ajax/delete-draft/<int:pk>/', motorcycles_views.delete_draft_ajax, name='delete_draft_ajax'),

    # ─── AJAX (trucks) ───
    path('ajax/save-trucks-draft/', trucks_views.save_trucks_draft_ajax, name='save_trucks_draft_ajax'),
    path('ajax/upload-trucks-image/', trucks_views.upload_trucks_image_ajax, name='upload_trucks_image_ajax'),
    path('ajax/delete-trucks-image/<int:pk>/', trucks_views.delete_trucks_image_ajax, name='delete_trucks_image_ajax'),
    path('ajax/reorder-trucks-images/', trucks_views.reorder_trucks_images_ajax, name='reorder_trucks_images_ajax'),

    # ─── CAR FOR PARTS (WIP — tik staff'ui) ───
    path('create/car-for-parts/', car_for_parts_views.car_for_parts_create, name='car_for_parts_create'),
    path('create/moto-for-parts/', moto_for_parts_views.moto_for_parts_create, name='moto_for_parts_create'),
    path('<int:pk>/edit-moto-for-parts/', moto_for_parts_views.moto_for_parts_edit, name='moto_for_parts_edit'),
    path('ajax/upload-moto-for-parts-image/', moto_for_parts_views.upload_moto_for_parts_image, name='upload_moto_for_parts_image'),
    path('ajax/delete-moto-for-parts-image/<int:pk>/', moto_for_parts_views.delete_moto_for_parts_image, name='delete_moto_for_parts_image'),
    path('ajax/reorder-moto-for-parts-images/', moto_for_parts_views.reorder_moto_for_parts_images, name='reorder_moto_for_parts_images'),
    path('ajax/upload-moto-for-parts-edit-image/<int:pk>/', moto_for_parts_views.upload_moto_for_parts_edit_image, name='upload_moto_for_parts_edit_image'),
    path('ajax/reorder-moto-for-parts-edit-images/<int:pk>/', moto_for_parts_views.reorder_moto_for_parts_edit_images, name='reorder_moto_for_parts_edit_images'),
    path('<int:pk>/edit-car-for-parts/', car_for_parts_views.car_for_parts_edit, name='car_for_parts_edit'),
    path('ajax/upload-car-for-parts-image/', car_for_parts_views.upload_car_for_parts_image, name='upload_car_for_parts_image'),
    path('ajax/delete-car-for-parts-image/<int:pk>/', car_for_parts_views.delete_car_for_parts_image, name='delete_car_for_parts_image'),
    path('ajax/reorder-car-for-parts-images/', car_for_parts_views.reorder_car_for_parts_images, name='reorder_car_for_parts_images'),
    path('ajax/upload-car-for-parts-edit-image/<int:pk>/', car_for_parts_views.upload_car_for_parts_edit_image, name='upload_car_for_parts_edit_image'),
    path('ajax/reorder-car-for-parts-edit-images/<int:pk>/', car_for_parts_views.reorder_car_for_parts_edit_images, name='reorder_car_for_parts_edit_images'),

    # ─── Search ───
    path('search/advanced/', views.advanced_search, name='advanced_search'),
    path('ajax/advanced-search-count/', views.advanced_search_count_ajax, name='advanced_search_count_ajax'),
    path('paieska/count/<str:category>/', views.search_panel_count, name='search_panel_count'),
    path('paieska/<str:category>/', views.advanced_search_generic, name='advanced_search_generic'),
    # Telefono drill-in: reikšmės pasirinkimas atskirame puslapyje
    path('pasirinkti/', select_views.select_value, name='select_value'),
    path('search/advanced/motorcycles/', motorcycles_views.motorcycles_advanced_search, name='motorcycles_advanced_search'),
    path('search/advanced/moto-parts/', moto_part_views.moto_parts_advanced_search, name='moto_parts_advanced_search'),
    path('search/advanced/trucks/', trucks_views.trucks_advanced_search, name='trucks_advanced_search'),
    path('search/save/', views.save_search, name='save_search'),
    path('search/delete/<int:pk>/', views.delete_search, name='delete_search'),
    path('search/toggle/<int:pk>/', views.toggle_search_notify, name='toggle_search_notify'),
    path('search/duplicate/<int:pk>/', views.duplicate_search, name='duplicate_search'),
    path('search/<int:pk>/viewed/', views.mark_search_viewed, name='mark_search_viewed'),

    # ─── Image ───
    path("image/<int:pk>/delete/", views.image_delete, name="image_delete"),
    path("image/<int:pk>/set-main/", views.image_set_main, name="image_set_main"),

    # ─── Dashboard ───
    path('dashboard/announcements/', views.my_listings, name='my_listings'),
    path('dashboard/announcements/boost-all/', views.listing_boost_all, name='listing_boost_all'),

    # ─── Admin moderation ───
    path('admin-moderate/', views.admin_users_list, name='admin_users_list'),
    path('admin-moderate/user/<int:user_id>/', views.admin_moderate_user, name='admin_moderate_user'),
    path('admin-moderate/listing/<int:pk>/toggle-shadow-ban/', views.admin_toggle_shadow_ban, name='admin_toggle_shadow_ban'),
    path('admin-moderate/sales-stats/', views.admin_sales_stats, name='admin_sales_stats'),

    # ─── MOTO GEAR ───
    path('create/motogear/', motogear_views.motogear_listing_create, name='motogear_listing_create'),
    path('ajax/save-motogear-draft/', motogear_views.save_motogear_draft_ajax, name='save_motogear_draft_ajax'),
    path('ajax/get-gear-equipment/', motogear_views.get_gear_equipment_ajax, name='get_gear_equipment_ajax'),
    path('ajax/get-gear-subtypes/', motogear_views.get_gear_subtypes_ajax, name='get_gear_subtypes_ajax'),
    path('ajax/upload-motogear-draft-images/', motogear_views.upload_motogear_draft_images_ajax, name='upload_motogear_draft_images_ajax'),
    path('ajax/delete-motogear-draft-image/<int:pk>/', motogear_views.delete_motogear_draft_image_ajax, name='delete_motogear_draft_image_ajax'),
    path('ajax/reorder-motogear-draft-images/', motogear_views.reorder_motogear_draft_images_ajax, name='reorder_motogear_draft_images_ajax'),
    path('browse/motogear/', motogear_views.motogear_list, name='motogear_list'),
    path('search/motogear/advanced/', motogear_views.motogear_advanced_search, name='motogear_advanced_search'),
    path('ajax/motogear-count/', motogear_views.motogear_count_ajax, name='motogear_count_ajax'),

    # ─── Listing detail + edit + lifecycle ───
    path("<int:pk>/", views.listing_detail, name="listing_detail"),
    path("<int:pk>/success/", views.listing_success, name="listing_success"),
    path("<int:pk>/stats/", views.listing_stats, name="listing_stats"),
    path("<int:pk>/edit/", views.listing_edit_hub, name="listing_edit_hub"),
    path("<int:pk>/edit-trucks/", trucks_views.trucks_listing_edit, name="trucks_listing_edit"),
    path("<int:pk>/edit/section/<str:section>/", views.listing_edit_section, name="listing_edit_section"),
    path("<int:pk>/edit/step/<int:step>/", views.listing_edit_step, name="listing_edit_step"),
    path("<int:pk>/edit-legacy/", views.listing_edit, name="listing_edit"),
    path("<int:pk>/activation-plans/", views.listing_activation_plans, name="listing_activation_plans"),

    # ─── Extra services purchase (papildomai žvaigždutės/highlight/featured) ───
    path("<int:pk>/services/", views.listing_services_order, name="listing_services_order"),
    path("<int:pk>/services/checkout/", views.listing_services_checkout, name="listing_services_checkout"),
    path("<int:pk>/activate/", views.listing_activate, name="listing_activate"),
    path("<int:pk>/reserve/", views.listing_reserve_toggle, name="listing_reserve_toggle"),
    path("<int:pk>/vin-update/", views.listing_vin_update, name="listing_vin_update"),
    path("<int:pk>/delete/", views.listing_delete, name="listing_delete"),
    path("<int:pk>/save/", views.save_listing, name="save_listing"),
    path("<int:pk>/contact/", views.contact_seller, name="contact_seller"),
    path("<int:pk>/report/", views.report_listing, name="report_listing"),

    path("create/truck-for-parts/", truck_for_parts_views.truck_for_parts_create, name="truck_for_parts_create"),
    path('browse/truck-parts/', truck_for_parts_views.truck_parts_browse, name='truck_parts_browse'),
    path('search/advanced/truck-parts/', truck_for_parts_views.truck_parts_advanced_search, name='truck_parts_advanced_search'),
    path("<int:pk>/edit-truck-for-parts/", truck_for_parts_views.truck_for_parts_edit, name="truck_for_parts_edit"),
    path('ajax/upload-truck-for-parts-image/', truck_for_parts_views.upload_truck_for_parts_image, name='upload_truck_for_parts_image'),
    path('ajax/delete-truck-for-parts-image/<int:pk>/', truck_for_parts_views.delete_truck_for_parts_image, name='delete_truck_for_parts_image'),
    path('ajax/reorder-truck-for-parts-images/', truck_for_parts_views.reorder_truck_for_parts_images, name='reorder_truck_for_parts_images'),
    path('ajax/upload-truck-for-parts-edit-image/<int:pk>/', truck_for_parts_views.upload_truck_for_parts_edit_image, name='upload_truck_for_parts_edit_image'),
    path('ajax/reorder-truck-for-parts-edit-images/<int:pk>/', truck_for_parts_views.reorder_truck_for_parts_edit_images, name='reorder_truck_for_parts_edit_images'),
]