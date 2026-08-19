from django import template
register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Reikšmė iš žodyno pagal kintamą raktą.

    Kai kintamojo kontekste nėra, Django jį paverčia į '' (string_if_invalid),
    todėl be šio patikrinimo `''|get_item:'x'` mestų AttributeError ir
    nugriautų visą puslapį — taip nutiko nuomos panelėje puslapiuose,
    kurie search_panel.html renderina be config_panels_sub.
    """
    if not hasattr(dictionary, 'get'):
        return ''
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
