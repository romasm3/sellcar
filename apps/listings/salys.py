# -*- coding: utf-8 -*-
"""
ŠALYS — vienas sąrašas visai svetainei.

Iki šito failo šalių sąrašas gulėjo bent dvylikoje vietų: dviejuose
modeliuose (Listing, WheelListing) ir maždaug dešimtyje kategorijų
vaizdų, kur kiekvienas turėjo savo `_country_choices()` su JAV priekyje.
Kopijos jau buvo prasilenkusios. Dabar visi — kūrimo forma, filtrai,
detali paieška ir žemėlapio paieška — ima iš čia.

TVARKA: dažniausios viršuje, tada abėcėlė. Grupės renderinamos kaip
`<optgroup>`, todėl sąraše matosi skirtukai.

RIKIAVIMAS: pagal lietuvišką abėcėlę (Č po C, Š po S, Ž po Z) —
`raktas()`. Grupių viduje rūšiuojama programiškai, todėl rankinės
tvarkos klaidos neįmanomos.

VALSTIJOS: laukas „Valstija" prasmingas tik toms šalims, kurios jas
turi. `VALSTIJOS` yra vienintelis to sąrašas — nauja šalis su
valstijomis pridedama viena eilute, ir laukas pats atsiras.
"""

from django.utils.translation import gettext_lazy as _

# ── Lietuviška abėcėlė rikiavimui ──────────────────────────────────
ABECELE = 'aąbcčdeęėfghiįyjklmnoprsštuųūvzž'
_SVORIS = {r: i for i, r in enumerate(ABECELE)}


def raktas(tekstas):
    """Rikiavimo raktas pagal lietuvišką abėcėlę."""
    return [_SVORIS.get(r, len(ABECELE) + ord(r)) for r in tekstas.lower()]


# ── Grupės ─────────────────────────────────────────────────────────
# (grupės vardas, [(kodas, vardas)]) — vardas rodomas kaip <optgroup>.
# Pirmos dvi grupės tvarkos nekeičia (dažniausios), likusios
# rikiuojamos pagal lietuvišką abėcėlę.

_NAMAI = [('LT', _('Lietuva'))]

_KAIMYNAI = [
    ('LV', _('Latvija')), ('EE', _('Estija')),
    ('PL', _('Lenkija')), ('DE', _('Vokietija')),
]

_EUROPA = [
    ('IE', _('Airija')), ('AT', _('Austrija')), ('BE', _('Belgija')),
    ('BG', _('Bulgarija')), ('CZ', _('Čekija')), ('DK', _('Danija')),
    ('GR', _('Graikija')), ('IS', _('Islandija')), ('ES', _('Ispanija')),
    ('IT', _('Italija')), ('CY', _('Kipras')), ('HR', _('Kroatija')),
    ('LI', _('Lichtenšteinas')), ('LU', _('Liuksemburgas')),
    ('MT', _('Malta')), ('NO', _('Norvegija')), ('NL', _('Nyderlandai')),
    ('PT', _('Portugalija')), ('FR', _('Prancūzija')),
    ('RO', _('Rumunija')), ('SK', _('Slovakija')), ('SI', _('Slovėnija')),
    ('FI', _('Suomija')), ('SE', _('Švedija')), ('CH', _('Šveicarija')),
    ('HU', _('Vengrija')),
]

_RYTAI = [
    ('BY', _('Baltarusija')), ('MD', _('Moldova')),
    ('RU', _('Rusija')), ('UA', _('Ukraina')),
]

# Dažniausios importo kryptys — todėl verta jas turėti sąraše
_IMPORTAS = [
    ('GB', _('Didžioji Britanija')), ('GE', _('Gruzija')),
    ('JP', _('Japonija')), ('US', _('Jungtinės Valstijos')),
    ('AE', _('Jungtiniai Arabų Emyratai')), ('KZ', _('Kazachstanas')),
    ('TR', _('Turkija')),
    # Valstijas turinčios šalys — kad laukas „Valstija" turėtų kur atsirasti
    ('CA', _('Kanada')), ('AU', _('Australija')),
]


def _rikiuok(porų_sąrašas):
    return sorted(porų_sąrašas, key=lambda p: raktas(str(p[1])))


GRUPES = [
    ('', _NAMAI),
    (str(_('Kaimyninės šalys')), _KAIMYNAI),
    (str(_('Europa')), _rikiuok(_EUROPA)),
    (str(_('Rytų kaimynai')), _rikiuok(_RYTAI)),
    (str(_('Importo kryptys')), _rikiuok(_IMPORTAS)),
]

NUMATYTA = 'LT'


def pasirinkimai():
    """Django `choices` su <optgroup> — kūrimo formai ir modeliams."""
    return [(grupe, poros) if grupe else poros[0] for grupe, poros in GRUPES]


def plokscias():
    """[(kodas, vardas)] be grupių — ten, kur optgroup netinka."""
    return [pora for _grupe, poros in GRUPES for pora in poros]


VARDAI = {kodas: vardas for kodas, vardas in plokscias()}


def vardas(kodas):
    return VARDAI.get(kodas, kodas)


# ── Angliški pavadinimai — NEVERČIAMI ──────────────────────────────
# Šalies juostoje virš paieškos panelės vardai rodomi angliškai ir
# nekeičiami pagal sąsajos kalbą: tai tarptautinis sąrašas, kurį skaito
# ir tas, kuris svetainės kalbos nemoka. Todėl čia paprastos eilutės, o
# ne gettext — kitaip vertėjas juos „pataisytų" į lietuviškus.
VARDAI_EN = {
    'LT': 'Lithuania', 'LV': 'Latvia', 'EE': 'Estonia', 'PL': 'Poland',
    'DE': 'Germany', 'IE': 'Ireland', 'AT': 'Austria', 'BE': 'Belgium',
    'BG': 'Bulgaria', 'CZ': 'Czechia', 'DK': 'Denmark', 'GR': 'Greece',
    'IS': 'Iceland', 'ES': 'Spain', 'IT': 'Italy', 'CY': 'Cyprus',
    'HR': 'Croatia', 'LI': 'Liechtenstein', 'LU': 'Luxembourg',
    'MT': 'Malta', 'NO': 'Norway', 'NL': 'Netherlands', 'PT': 'Portugal',
    'FR': 'France', 'RO': 'Romania', 'SK': 'Slovakia', 'SI': 'Slovenia',
    'FI': 'Finland', 'SE': 'Sweden', 'CH': 'Switzerland', 'HU': 'Hungary',
    'BY': 'Belarus', 'MD': 'Moldova', 'RU': 'Russia', 'UA': 'Ukraine',
    'GB': 'United Kingdom', 'GE': 'Georgia', 'JP': 'Japan',
    'US': 'United States', 'AE': 'United Arab Emirates',
    'KZ': 'Kazakhstan', 'TR': 'Turkey', 'CA': 'Canada', 'AU': 'Australia',
}


def vardas_en(kodas):
    """Angliškas pavadinimas šalies juostai. Nežinomam kodui — pats kodas."""
    return VARDAI_EN.get(str(kodas or '').upper(), str(kodas or '').upper())


def grupes_su(kodai):
    """Tos pačios grupės, paliekant tik nurodytus kodus (filtrams).

    Filtruose rodom tik tas šalis, kurios turi skelbimų — kaip ir su
    markėmis. Tuščios grupės iškrenta.
    """
    kodai = set(kodai)
    isvestis = []
    for grupe, poros in GRUPES:
        liko = [p for p in poros if p[0] in kodai]
        if liko:
            isvestis.append((grupe, liko))
    return isvestis


def su_skelbimais(qs, laukas='country'):
    """[(kodas, vardas)] — tik tos šalys, kurios yra queryset'e."""
    kodai = (qs.exclude(**{laukas: ''}).values_list(laukas, flat=True)
             .distinct())
    return [p for p in plokscias() if p[0] in set(kodai)]


# ── Valstijos ──────────────────────────────────────────────────────
# Laukas „Valstija" rodomas TIK toms šalims, kurios čia yra.

_JAV = [
    ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'),
    ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'),
    ('CT', 'Connecticut'), ('DE', 'Delaware'), ('FL', 'Florida'),
    ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'),
    ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'),
    ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'),
    ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'),
    ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'),
    ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'),
    ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'),
    ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'),
    ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'),
    ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'),
    ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'), ('WY', 'Wyoming'), ('DC', 'Washington, D.C.'),
]

_KANADA = [
    ('AB', 'Alberta'), ('BC', 'British Columbia'), ('MB', 'Manitoba'),
    ('NB', 'New Brunswick'), ('NL', 'Newfoundland and Labrador'),
    ('NS', 'Nova Scotia'), ('NT', 'Northwest Territories'),
    ('NU', 'Nunavut'), ('ON', 'Ontario'), ('PE', 'Prince Edward Island'),
    ('QC', 'Quebec'), ('SK', 'Saskatchewan'), ('YT', 'Yukon'),
]

_AUSTRALIJA = [
    ('ACT', 'Australian Capital Territory'), ('NSW', 'New South Wales'),
    ('NT', 'Northern Territory'), ('QLD', 'Queensland'),
    ('SA', 'South Australia'), ('TAS', 'Tasmania'),
    ('VIC', 'Victoria'), ('WA', 'Western Australia'),
]

VALSTIJOS = {'US': _JAV, 'CA': _KANADA, 'AU': _AUSTRALIJA}

# Ilgiausias valstijos kodas („ACT", „NSW") — modelio lauko ilgiui
VALSTIJOS_ILGIS = 8


def valstiju_salys():
    return sorted(VALSTIJOS)


def valstijos(kodas):
    return VALSTIJOS.get(kodas, [])


def visos_valstijos():
    """Django `choices` laukui `state` — visos šalys, sugrupuotos."""
    return [(vardas(kodas), VALSTIJOS[kodas]) for kodas in valstiju_salys()]


def filtro_salys(qs=None, laukas='country'):
    """[{code, name, fi_code}] filtrams.

    Su queryset'u rodom TIK tas šalis, kurios turi skelbimų — kaip ir su
    markėmis; be jo (kūrimo formos) — visas.
    """
    poros = su_skelbimais(qs, laukas) if qs is not None else plokscias()
    return [{'code': k, 'name': v, 'fi_code': k.lower()} for k, v in poros]


# ── Vietininkas: „Vokietijoje" ─────────────────────────────────────
# Reikalingas vienai eilutei skelbimo puslapyje („Šis skelbimas yra
# Vokietijoje"). Lietuvių kalboje vietininko iš vardininko taisyklingai
# neišvesi (Lietuva→Lietuvoje, bet Kipras→Kipre), tad sąrašas.
VIETININKAI = {
    'LT': 'Lietuvoje', 'LV': 'Latvijoje', 'EE': 'Estijoje', 'PL': 'Lenkijoje',
    'DE': 'Vokietijoje', 'IE': 'Airijoje', 'AT': 'Austrijoje', 'BE': 'Belgijoje',
    'BG': 'Bulgarijoje', 'CZ': 'Čekijoje', 'DK': 'Danijoje', 'GR': 'Graikijoje',
    'IS': 'Islandijoje', 'ES': 'Ispanijoje', 'IT': 'Italijoje', 'CY': 'Kipre',
    'HR': 'Kroatijoje', 'LI': 'Lichtenšteine', 'LU': 'Liuksemburge',
    'MT': 'Maltoje', 'NO': 'Norvegijoje', 'NL': 'Nyderlanduose',
    'PT': 'Portugalijoje', 'FR': 'Prancūzijoje', 'RO': 'Rumunijoje',
    'SK': 'Slovakijoje', 'SI': 'Slovėnijoje', 'FI': 'Suomijoje',
    'SE': 'Švedijoje', 'CH': 'Šveicarijoje', 'HU': 'Vengrijoje',
    'BY': 'Baltarusijoje', 'MD': 'Moldovoje', 'RU': 'Rusijoje',
    'UA': 'Ukrainoje', 'GB': 'Didžiojoje Britanijoje', 'GE': 'Gruzijoje',
    'JP': 'Japonijoje', 'US': 'Jungtinėse Valstijose',
    'AE': 'Jungtiniuose Arabų Emyratuose', 'KZ': 'Kazachstane',
    'TR': 'Turkijoje', 'CA': 'Kanadoje', 'AU': 'Australijoje',
}


def vietininkas(kodas):
    """'DE' → „Vokietijoje" — eilutei „Šis skelbimas yra …".

    Vietininkas yra lietuvių kalbos linksnis, todėl jį duodam TIK
    lietuviškoje sąsajoje. Kitomis kalbomis sakinys sudėtas iš prielinksnio
    vertime („This listing is in %(salis)s"), tad ten reikia paprasto
    pavadinimo — kitaip anglas skaitytų „is in Vokietijoje".
    """
    from django.utils.translation import get_language
    kodas = str(kodas or '').upper()
    if (get_language() or '').split('-')[0] != 'lt':
        return vardas(kodas)
    return VIETININKAI.get(kodas) or vardas(kodas)
