from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

# Administracijos antraštė — prekės ženklas, ne „Django administration".
# Taškas rašomas tekste: admin šablonas savo HTML čia neleidžia.
admin.site.site_header = 'Autoleft.'
admin.site.site_title = 'Autoleft.'
admin.site.index_title = 'Valdymas'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('rosetta/', include('rosetta.urls')),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),

    path('accounts/', include('apps.accounts.urls')),
    path('conversations/', include('apps.conversations.urls')),
    path('payments/', include('apps.payments.urls')),
    path('', include('apps.listings.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)