from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView

# Jei turi sitemaps modulį — pataisyk import path pagal savo projektą:
# from apps.listings.sitemaps import ListingSitemap
# sitemaps = {'listings': ListingSitemap}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('rosetta/', include('rosetta.urls')),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    # path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('accounts/', include('apps.accounts.urls')),
    path('', include('apps.listings.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)