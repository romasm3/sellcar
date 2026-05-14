from django.urls import path
from django.views.generic import RedirectView
from . import views
app_name = 'accounts'
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # Profile puslapiai pašalinti — redirect'inam į My Listings
    path('profile/', RedirectView.as_view(pattern_name='my_listings', permanent=False), name='profile'),
    path('profile/edit/', RedirectView.as_view(pattern_name='my_listings', permanent=False), name='profile_edit'),
    # Settings
    path('settings/', views.settings, name='settings'),
    path('settings/inline-update/', views.inline_update, name='inline_update'),
    path('settings/update-picture/', views.update_profile_picture, name='update_profile_picture'),
    path('settings/delete-picture/', views.delete_profile_picture, name='delete_profile_picture'),
    path('settings/notifications/', views.update_notifications, name='update_notifications'),
    path('settings/privacy/', views.update_privacy, name='update_privacy'),
    path('settings/delete-account/', views.delete_account, name='delete_account'),
    # Password reset
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # Password change
    path('password-change/', views.password_change, name='password_change'),
    path('boost/', views.boost_listings, name='boost_listings'),
    # Seller profile — PUBLIC pardavėjo puslapis (kiti vartotojai mato)
    path('seller/<int:pk>/', views.seller_profile, name='seller_profile'),
    path('seller/<int:seller_pk>/review/', views.leave_review, name='leave_review'),
    path('settings/business/', views.update_business_profile, name='update_business_profile'),
    path('wallet/', views.wallet, name='wallet'),
    path('wallet/top-up/', views.wallet_top_up, name='wallet_top_up'),
    path('wallet/top-up-test/', views.wallet_top_up_test, name='wallet_top_up_test'),
    path('wallet/stripe-webhook/', views.stripe_webhook, name='wallet_stripe_webhook'),
    path('become-dealer/', views.become_dealer, name='become_dealer'),
    # Dealer area
    path('dealer/setup/', views.dealer_setup, name='dealer_setup'),
    path('dealer/dashboard/', views.dealer_dashboard, name='dealer_dashboard'),
    path('admin/dealers/', views.admin_dealers_list, name='admin_dealers_list'),
    path('admin/dealers/<int:user_id>/', views.admin_dealer_detail, name='admin_dealer_detail'),
    path('admin/dealers/<int:user_id>/toggle-active/', views.admin_dealer_toggle_active, name='admin_dealer_toggle_active'),
    path('dealer/<str:username>/', views.dealer_public_page, name='dealer_public_page'),
]