from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),

    # Settings
    path('settings/', views.settings, name='settings'),
    path('settings/notifications/', views.update_notifications, name='update_notifications'),
    path('settings/privacy/', views.update_privacy, name='update_privacy'),
    path('settings/delete-account/', views.delete_account, name='delete_account'),

    # Password reset - NAUDOK CUSTOM VIEWS
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Password change
    path('password-change/', views.password_change, name='password_change'),
]
