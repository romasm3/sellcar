from django.urls import path
from . import views


app_name = 'payments'


urlpatterns = [
    path('wallet/topup/', views.create_wallet_topup_checkout, name='wallet_topup'),
    path('wallet/topup/success/', views.topup_success, name='topup_success'),
    path('wallet/topup/cancel/', views.topup_cancel, name='topup_cancel'),
    path('webhook/', views.stripe_webhook, name='webhook'),
]