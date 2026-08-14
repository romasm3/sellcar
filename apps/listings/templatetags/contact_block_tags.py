# apps/listings/templatetags/contact_block_tags.py
# ═══════════════════════════════════════════════════════════
# Choice lists for the shared contact block.
#
# Views used to build these themselves, and the copies had drifted —
# car-for-parts and truck-for-parts offered only the United States, and
# motorcycles offered the full list or only the US depending on a branch.
# The contact block reads them from here instead, so no view can narrow
# the list by accident.
# ═══════════════════════════════════════════════════════════

from django import template

from ..models import Listing

register = template.Library()


@register.simple_tag
def contact_country_choices():
    """Every country a listing may be located in."""
    return list(Listing.COUNTRY_CHOICES)


@register.simple_tag
def contact_state_choices():
    """US states — only meaningful when country == 'US'."""
    return list(Listing.US_STATE_CHOICES)
