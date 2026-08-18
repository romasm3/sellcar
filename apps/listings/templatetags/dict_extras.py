from django import template
register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, '')

@register.filter
def get_param(querydict, key):
    """GET reikšmė pagal kintamą raktą — generinei paieškos panelei.

    Šablone {{ request.GET.foo }} neveikia, kai rakto vardas ateina iš
    konfigūracijos, todėl reikia filtro.
    """
    if not key:
        return ''
    return querydict.get(key, '')


@register.filter
def get_list(querydict, key):
    """GET sąrašas pagal kintamą raktą (multiselect laukams)."""
    if not key:
        return []
    if hasattr(querydict, 'getlist'):
        return querydict.getlist(key)
    val = querydict.get(key)
    return [val] if val else []
