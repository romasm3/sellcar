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


@register.filter
def drop_param(querydict, key):
    """GET parametrai be vieno lauko — telefono žymos × nuorodai.

    × šalina TIK tą filtrą: likę parametrai (kategorija, kiti filtrai,
    rūšiavimas) lieka URL'e.
    """
    params = querydict.copy()
    params.pop(key, None)
    return params.urlencode()


@register.filter
def get_list_param(querydict, key):
    """Visos to paties parametro reikšmės — kelioms markėms ar modeliams."""
    try:
        return querydict.getlist(key)
    except AttributeError:
        return []


@register.simple_tag
def drop_value(querydict, key, value):
    """GET parametrai be VIENOS to lauko reikšmės.

    × ant vienos poros šalina tik ją: kitos poros lieka, o kadangi
    reikšmės kaupiamos tuo pačiu vardu (ne brand_2, brand_3), numeracijos
    nėra ir jai nėra kaip sugriūti.
    """
    params = querydict.copy()
    values = [v for v in params.getlist(key) if str(v) != str(value)]
    if values:
        params.setlist(key, values)
    else:
        params.pop(key, None)
    return params.urlencode()


@register.filter
def option_label(field, value):
    """Reikšmės pavadinimas žymai (markė → „Audi", ne „95")."""
    value = str(value)
    for key in ('brands_top', 'brands_rest'):
        for row in field.get(key) or []:
            if str(row.get('value')) == value:
                return row.get('name')
    for opt_value, label in field.get('options') or []:
        if str(opt_value) == value:
            return label
    return value


@register.filter
def model_name(value):
    """Modelio pavadinimas pagal id — žymai telefone.

    Modelio laukas reikšmių sąrašo neturi (jos ateina kaskada), todėl
    pavadinimas paimamas tiesiai iš lentelės.
    """
    from apps.listings.models import Model

    try:
        return Model.objects.filter(pk=int(value)).values_list('name', flat=True).first() or value
    except (TypeError, ValueError):
        return value


@register.filter
def brand_label(value, item):
    """Pasirinktos markės pavadinimas iš kešuoto sąrašo.

    FK markėms request.GET turi id ('961'), o mygtuke reikia „BMW".
    Sąrašas jau kešuotas brand_api.brand_items(), todėl tai nekainuoja
    papildomos užklausos.
    """
    if not value:
        return ''
    try:
        from apps.listings.brand_api import brand_name
        return brand_name(item.get('brand_vt'), value, item.get('brand_sub') or None) or value
    except Exception:
        return value


@register.filter
def img_sm(image):
    """Kortelės dydžio nuotrauka (668 px) su atsarga.

    Jei objektas neturi perdirbtų versijų (kitas modelis arba dar
    neperdirbta), grąžinam originalą — puslapis nesugriūva.
    """
    if not image:
        return ''
    url = getattr(image, 'url_sm', None)
    if url:
        return url
    try:
        return image.image.url
    except Exception:
        return ''
