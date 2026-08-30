from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

# Administracijos antraštė — prekės ženklas, ne „Django administration".
# Taškas rašomas tekste: admin šablonas savo HTML čia neleidžia.
admin.site.site_header = 'Autoleft.'
admin.site.site_title = 'Autoleft.'
admin.site.index_title = 'Valdymas'

# Be kalbos priešdėlio: valdymas, kalbos keitimas, robots.txt.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('rosetta/', include('rosetta.urls')),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
]

# Lietuviškas adresas lieka be priešdėlio (/imones/), angliškas gauna /en/.
urlpatterns += i18n_patterns(
    path('accounts/', include('apps.accounts.urls')),
    path('conversations/', include('apps.conversations.urls')),
    path('payments/', include('apps.payments.urls')),
    path('', include('apps.imones.urls')),
    path('', include('apps.listings.urls')),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)