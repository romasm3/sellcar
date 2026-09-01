# -*- coding: utf-8 -*-
"""
KALBŲ ŽYMĖS — vėliavos kodas ir pavadinimas pagal kalbos kodą.

Iki šiol base.html keturiose vietose kartojosi ta pati 13 šakų
{% if %}{% elif %} grandinė (kalbos kodas → vėliavos kodas), o penktoje
— dar viena tokia pati pavadinimams. Pridėjus kalbą reikėdavo nepamiršti
visų penkių. Čia — viena vieta.

Vėliavos kodas ne visada sutampa su kalbos kodu: en→us, et→ee,
zh-hans→cn, vi→vn, ar→sa, ko→kr.
"""
from django import template

register = template.Library()

# Kalbos kodas → šalies kodas flag-icons bibliotekai
VELIAVOS = {
    'en': 'us', 'lt': 'lt', 'lv': 'lv', 'et': 'ee', 'pl': 'pl',
    'de': 'de', 'ru': 'ru', 'fr': 'fr', 'es': 'es', 'zh-hans': 'cn',
    'vi': 'vn', 'ar': 'sa', 'ko': 'kr',
}

# Pavadinimas gimtąja kalba — perjungiklyje NEVERČIAMAS: ruso akis
# sąraše ieško „Русский", ne „Russian", kad ir kokia kalba būtų sąsaja.
# (settings.LANGUAGES pavadinimai eina per gettext ir angliškame puslapyje
# virsta angliškais — ten to ir reikia, o čia, sąraše, — ne.)
PAVADINIMAI = {
    'lt': 'Lietuvių', 'en': 'English', 'lv': 'Latviešu', 'et': 'Eesti',
    'pl': 'Polski', 'de': 'Deutsch', 'ru': 'Русский', 'fr': 'Français',
    'es': 'Español', 'zh-hans': '简体中文', 'vi': 'Tiếng Việt',
    'ar': 'العربية', 'ko': '한국어',
}


@register.filter
def veliavos_kodas(kalbos_kodas):
    """'zh-hans' → 'cn'. Nežinomai kalbai — jos pačios kodas."""
    kodas = str(kalbos_kodas or '').lower()
    return VELIAVOS.get(kodas, kodas[:2] or 'us')


@register.filter
def kalbos_pavadinimas(kalbos_kodas, atsarginis=''):
    """'ru' → 'Русский'. Nežinomai — kas paduota (settings pavadinimas)."""
    kodas = str(kalbos_kodas or '').lower()
    return PAVADINIMAI.get(kodas) or atsarginis or kodas.upper()
