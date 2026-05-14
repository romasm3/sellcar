"""
Custom template filters for listings app.

Usage in templates:
    {% load listing_filters %}
    {% for y in "2024 2025 2026"|split:" " %}
        {{ y }}
    {% endfor %}
"""
from django import template

register = template.Library()


@register.filter(name='split')
def split_filter(value, delimiter=' '):
    """Split a string by delimiter. Default delimiter is space.

    Example:
        {{ "a,b,c"|split:"," }}  -> ['a', 'b', 'c']
        {{ "a b c"|split }}      -> ['a', 'b', 'c']
    """
    if value is None:
        return []
    return str(value).split(delimiter)


@register.filter(name='get_item')
def get_item(dictionary, key):
    """Get an item from a dict by key.

    Example:
        {{ my_dict|get_item:"somekey" }}
    """
    if dictionary is None:
        return None
    return dictionary.get(key) if hasattr(dictionary, 'get') else None


@register.filter(name='star_badge')
def star_badge(listing):
    """Return star emoji based on effective star level.

    Example:
        {{ listing|star_badge }}
    """
    if not hasattr(listing, 'get_effective_star_level'):
        return ''
    level = listing.get_effective_star_level()
    if level == 2:
        return '⭐⭐'
    if level == 1:
        return '⭐'
    return ''