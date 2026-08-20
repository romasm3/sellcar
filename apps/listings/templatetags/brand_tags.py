# apps/listings/templatetags/brand_tags.py
"""Markių widget'ų jungikliai šablonams."""
from django import template

from apps.listings.brands import TOP_BRANDS_ENABLED

register = template.Library()


@register.simple_tag
def top_brands_enabled():
    """Ar rodyti „Top markės" grupę ir „Rodyti visus" jungiklį.

    Kol skelbimų nėra, viršus lieka tuščias, o „tik su skelbimais"
    filtras paslepia visą sąrašą — todėl išjungta. Žr.
    brands.TOP_BRANDS_ENABLED.
    """
    return TOP_BRANDS_ENABLED
