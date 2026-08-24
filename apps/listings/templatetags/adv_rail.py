"""Detalios paieškos kategorijų juosta kaip šablono žyma.

Juosta gyvena viename partial'e (`_adv_rail.html`), o punktus sudeda
views._advanced_rail. Kad tos pačios juostos nereikėtų perduoti per
kiekvieno vaizdo kontekstą, senesniems detalios paieškos puslapiams
užtenka:

    {% load adv_rail %}
    {% adv_rail 'motorcycles' %}
"""

from django import template

register = template.Library()


@register.inclusion_tag('listings/partials/_adv_rail.html')
def adv_rail(active_slug=''):
    from apps.listings.views import _advanced_rail
    juosta, daugiau = _advanced_rail(active_slug)
    return {'adv_rail': juosta, 'adv_more': daugiau}
