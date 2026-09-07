from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

from apps.listings.kalbos_kelias import perjungti_kalba
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
    # Kalbos perjungimas — SAVAS, prieš Django rinkinį: Django
    # `set_language` adreso priešdėlio čia nepersuka (žr.
    # apps/listings/kalbos_kelias.py), tad žmogus grįždavo į /ru/…
    # ir kalba atšokdavo atgal.
    path('i18n/setlang/', perjungti_kalba, name='set_language'),
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

# AJAX maršrutai DAR KARTĄ — be kalbos priešdėlio.
#
# Frontend'as juos rašo kietai („/ajax/upload-listing-images/12/"), tad
# su ne lietuvių kalba jie krisdavo į 404: i18n_patterns tokiu atveju
# laukia „/ru/ajax/…". Nuotraukų įkėlimas neveikė 12 iš 13 kalbų.
# Paaiškinimas — apps/listings/urls_ajax.py.
#
# Dedam PO i18n_patterns, kad `reverse()` grąžintų būtent bepriešdėlį
# variantą: AJAX adresui priešdėlio nereikia niekada.
urlpatterns += [
    path('', include('apps.listings.urls_ajax')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)