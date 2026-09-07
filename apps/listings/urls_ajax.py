# -*- coding: utf-8 -*-
"""
AJAX MARŠRUTAI BE KALBOS PRIEŠDĖLIO.

Kodėl atskirai
──────────────
`config/urls.py` visą `apps.listings.urls` laiko
`i18n_patterns(prefix_default_language=False)` viduje: lietuviški adresai
be priešdėlio, kiti su (`/ru/…`). Puslapiams to ir reikia.

Bet frontend'as AJAX adresus rašo KIETAI, be priešdėlio:

    xhr.open('POST', '/ajax/upload-listing-images/' + listingId + '/')

Tokių vietų šablonuose ~50. Kai aktyvi kalba ne lietuvių,
`LocalePrefixPattern` reikalauja „/ru/ajax/…", o „/ajax/…" nebeatitinka
NĖ VIENO maršruto — POST'as gauna 404. Vartotojui tai atrodo kaip
„Upload failed (404)" ties 100 % progreso. GET'ą tokiu atveju išgelbsti
`KalbosKelioMiddleware` (302 į priešdėlį), bet POST'o jis sąmoningai
neliečia: 302 nuneštų failo kūną.

Ką darom
────────
Tuos pačius maršrutus prijungiam DAR KARTĄ — už `i18n_patterns` ribų.
Sąrašas imamas iš to paties `urls.py`, tad antro šaltinio nėra ir naujas
`ajax/` maršrutas čia atsiranda savaime.

Seni adresai su priešdėliu („/ru/ajax/…") toliau veikia: jie ir liko
`i18n_patterns` viduje.

Kalba AJAX atsakymuose ateina iš slapuko ir profilio (`LocaleMiddleware`
+ `UserLanguageMiddleware`), o ne iš kelio, tad klaidų tekstai lieka
vartotojo kalba.
"""
from apps.listings import urls as _puslapiai

# Ne visi frontend'o kviečiami keliai prasideda „ajax/". Šitie irgi
# užrašyti kietai (fetch('/image/12/set-main/') ir pan.), tad jiems
# reikia to paties bepriešdėlio varianto. Sąrašas trumpas ir aiškus:
# įrašom tik tai, ką JS tikrai kviečia.
PRIESAGOS = (
    'ajax/',            # visi AJAX galiniai taškai
    'image/',           # nuotraukos trynimas ir „padaryti pagrindine"
    'paieska/count/',   # „Filtruoti · N" skaitiklis
    'search/save/',     # išsaugota paieška
    'search/toggle-save/',
    'perziureti/id/',   # peržiūrėtų skelbimų žymėjimas
    'map/duomenys/',    # žemėlapio duomenys
    'map/pardavejas/',
)


def _ajax_marsrutai():
    """Frontend'o kviečiami keliai iš pagrindinio urls.py."""
    return [m for m in _puslapiai.urlpatterns
            if str(getattr(m, 'pattern', '')).startswith(PRIESAGOS)]


urlpatterns = _ajax_marsrutai()
