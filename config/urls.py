from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.listings import views as listing_views
from apps.accounts.views import set_language

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rosetta/', include('rosetta.urls')),
    path('i18n/setlang/', set_language, name='set_language'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('accounts/', include('apps.accounts.urls')),
    path('conversations/', include('apps.conversations.urls')),
    # Home alias — palieku, kad {% url 'home' %} toliau veiktų
    path('', listing_views.listing_list, name='home'),
    # Listings — visi URL'ai iš apps/listings/urls.py (BE /listings/ prefikso)
    path('', include('apps.listings.urls')),
    path('payments/', include('apps.payments.urls', namespace='payments')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)