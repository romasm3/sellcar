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
    # Markių sąrašo lauke nebėra (kraunamas per /ajax/markes/), todėl
    # pavadinimą imam iš to paties kešuoto šaltinio.
    if field.get('widget') == 'brand':
        try:
            from apps.listings.brand_api import brand_name
            return brand_name(field.get('brand_vt'), value,
                              field.get('brand_sub') or None) or value
        except Exception:
            return value
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


@register.filter
def model_label(value, item):
    """Pasirinkto modelio pavadinimas iš to paties kešuoto šaltinio."""
    if not value:
        return ''
    try:
        from apps.listings.brand_api import model_items
        vt = item.get('model_vt')
        brand = None
        from django.http import QueryDict   # markė ateina iš to paties GET
        items = None
        # modelio pavadinimą randam nepriklausomai nuo markės — per lentelę
        from apps.listings import models as m
        cls = m.Model if vt == 'cars' else m.MotorcycleModel
        obj = cls.objects.filter(pk=value).first()
        return obj.name if obj else value
    except Exception:
        return value


@register.filter
def split_csv(value):
    """„lt,ru,en" → ['lt', 'ru', 'en'] — kad tvarka būtų šablone, ne atsitiktinė."""
    return [x.strip() for x in str(value).split(',') if x.strip()]


@register.filter
def skyrikliai(tekstas):
    """„A | B" → „A <span class=\"sep\">|</span> B".

    Santrauka lieka paprastu tekstu (jį naudoja title patarimas), o
    brūkšnys šablone gauna savo spalvą — šviesesnę už tekstą, kad
    neblaškytų (docs/dizaino-sistema.md).
    """
    from django.utils.html import escape
    from django.utils.safestring import mark_safe

    # Tarpai aplink brūkšnį lieka tikri — kad tekstas galėtų lūžti prie jų,
    # o ne tik ties kableliais.
    dalys = [escape(d) for d in str(tekstas).split(' | ')]
    return mark_safe(' <span class="sep">|</span> '.join(dalys))


# Ilgi kategorijų pavadinimai telefono pikeryje netelpa į vieną eilutę.
# Trumpiname TIK rodymui — pilnas tekstas lieka title patarime.
TRUMPINIAI = {
    'Limuzinų, vestuvių transporto nuoma': 'Limuzinų nuoma',
    'Mikroautobusų, turistinio, vandens tr. nuoma': 'Mikroautobusų nuoma',
    'Sunkiojo transporto, priekabų nuoma': 'Sunkiojo transp. nuoma',
    'Automobilių, mikroautobusų dalys': 'Automobilių dalys',
    'Sunkiojo transporto dalys': 'Sunkiojo transp. dalys',
    'Žemės ūkio, spec. dalys': 'Žemės ūkio dalys',
    'Žemės ūkio technika, padargai': 'Žemės ūkio technika',
    'Krovimo ir sandėliavimo technika': 'Krovimo technika',
    'Komunalinio ūkio transportas': 'Komunalinis transp.',
    'Autotraukiniai, autovežiai': 'Autovežiai',
    'Priekabos / Puspriekabės': 'Priekabos',
    'Apranga, šalmai, aksesuarai': 'Moto apranga',
    'Aksesuarai, Tuning': 'Aksesuarai, tuning',
    'Video, audio, navigacijos': 'Video, audio, navi',
    'El. paspirtukai, riedžiai, dviračiai': 'Paspirtukai, dviračiai',
    'Turistiniai nameliai': 'Turistiniai nameliai',
    'Miško ūkio technika': 'Miško technika',
    'Ratlankiai / padangos': 'Ratlankiai',
    'Motociklai, apranga': 'Motociklai',
    'Statybinės technikos priedai': 'Statybos priedai',
    'Vandens transportas': 'Vandens transp.',
    'Automobilių supirkimas': 'Auto supirkimas',
    'Mikroautobusų, turistinio, vandens tr. nuoma': 'Mikroautob. nuoma',
    'Sunkiojo transporto, priekabų nuoma': 'Sunkiojo nuoma',
    'El. paspirtukai, riedžiai, dviračiai': 'Paspirtukai',
    'Žemės ūkio technika, padargai': 'Žemės ūkio techn.',
}


@register.filter
def trumpas(vardas):
    """Ilgą kategorijos pavadinimą sutrumpina telefono pikeriui."""
    tekstas = str(vardas).strip()
    return TRUMPINIAI.get(tekstas, tekstas)


@register.filter
def skelbimu(kiek):
    """Lietuviška daugiskaita: 1 skelbimas · 2–9 skelbimai · 0, 10–20 skelbimų.

    Django `pluralize` moka tik dvi formas, o lietuvių kalboje jų trys,
    todėl skaičiuojam patys (kaip ir kitur sąrašuose).
    """
    try:
        n = int(kiek)
    except (TypeError, ValueError):
        return 'skelbimų'
    šimtai = n % 100
    vienetai = n % 10
    if vienetai == 1 and šimtai != 11:
        return 'skelbimas'
    if 2 <= vienetai <= 9 and not 11 <= šimtai <= 19:
        return 'skelbimai'
    return 'skelbimų'
