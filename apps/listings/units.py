# -*- coding: utf-8 -*-
"""
MATAVIMO VIENETAI — VIENA VIETA SERVERIO PUSEI.

Kliento pusėje jungiklius valdo `static/js/unit_toggle.js`. Iki šiol
jungiklis gyveno TIK naršyklėje: serveris gaudavo „10837" ir nežinojo,
ar tai litrai, ar kubiniai centimetrai. Litrais toks skaičius netelpa į
stulpelį (DecimalField 5,1 → 9999,9), tad vietoj žinutės žmogus gaudavo
500, o kartu pakibdavo juodraštis su jau įkeltomis nuotraukomis.

Dabar kiekvienas jungiklis kartu su reikšme siunčia paslėptą lauką:

    engine_capacity      12.0        ← reikšmė
    engine_capacity_unit L           ← KURIO VIENETO ta reikšmė

Sutartis viena ir be dviprasmybių: `<laukas>_unit` visada nurodo
SIUNČIAMOS reikšmės vienetą. Naršyklė perskaičiuoja į saugojimo vienetą
pati (taip veikia ir paieškos filtrai bei juodraščių autosave), tad
įprastai atkeliauja kanoninis vienetas; be JavaScript'o — tas, kuriuo
forma buvo atvaizduota. Serveris normalizuoja bet kurį atvejį, tad
dvigubo vertimo būti negali.

Čia — TIK GRYNOS FUNKCIJOS: jokio `request`, jokio POST perrašymo.
Normalizuoja pati forma (žr. `UnitNormalizationMixin`) arba vaizdas,
paimdamas reikšmę per `reiksme(post, laukas)`. Bendro middleware
sąmoningai NĖRA: jis perrašinėtų POST visoje svetainėje — ir ten, kur
apie vienetus niekas nieko nežino (admin, API, svetimos formos).

Saugojimo vienetai nesikeičia: litrai, kilometrai, kilogramai.

Ribos (RIBOS) — dalykinės, ne stulpelio talpos: variklis iki 30 l, o ne
iki 9999,9. Stulpelio talpą atskirai tikrina apps/listings/skaiciai.py.
"""
from decimal import Decimal, InvalidOperation

from django.utils.translation import gettext as _

# laukas → (saugojimo vienetas, {vienetas: kiek to vieneto telpa
#           viename saugojimo vienete})
#
# Vardai sutampa su static/js/unit_toggle.js SPECS — jei ten atsiranda
# naujas jungiklis, jo eilutė reikalinga ir čia.
VIENETAI = {
    'engine_capacity': ('L', {'L': Decimal('1'), 'cm3': Decimal('1000')}),
    'mileage': ('km', {'km': Decimal('1'), 'mi': Decimal('0.62137')}),
    'mileage_km': ('km', {'km': Decimal('1'), 'mi': Decimal('0.62137')}),
    'range_km': ('km', {'km': Decimal('1'), 'mi': Decimal('0.62137')}),
    'curb_weight': ('kg', {'kg': Decimal('1'), 'lb': Decimal('2.20462')}),
    'gross_weight_kg': ('kg', {'kg': Decimal('1'), 'lb': Decimal('2.20462')}),
    'payload_kg': ('kg', {'kg': Decimal('1'), 'lb': Decimal('2.20462')}),
    'power': ('kW', {'kW': Decimal('1'), 'HP': Decimal('1.34102')}),
    'fuel_tank_capacity_l': ('L', {'L': Decimal('1'), 'gal': Decimal('0.264172')}),
    'engine_capacity_cc': ('cm3', {'cm3': Decimal('1'), 'ci': Decimal('0.0610237')}),
}

# Kiek skaitmenų po kablelio saugom. Turi atitikti modelio lauką:
# IntegerField → 0, DecimalField → decimal_places. Be šito 100 mi
# virstų „160.9347087886…", o `int()` tokio nebepriimtų.
TIKSLUMAS = {
    'engine_capacity': 1, 'engine_capacity_cc': 0,
    'mileage': 0, 'mileage_km': 0, 'range_km': 0,
    'curb_weight': 0, 'gross_weight_kg': 0, 'payload_kg': 0,
    'power': 0, 'fuel_tank_capacity_l': 0,
}

# Sinonimai — naršyklė rodo „cm³", POST'e patogiau „cm3".
SINONIMAI = {
    'cm³': 'cm3', 'CM3': 'cm3', 'l': 'L', 'ltr': 'L',
    'lbs': 'lb', 'LB': 'lb', 'hp': 'HP', 'kw': 'kW',
    'KM': 'km', 'MI': 'mi', 'KG': 'kg',
}

# Dalykinės ribos saugojimo vienetais. Stulpelis priimtų ir 9999,9 l, bet
# tokio variklio nebūna — o 10837 beveik visada reiškia cm³.
RIBOS = {
    'engine_capacity': Decimal('30'),      # l
}

# Ką pasiūlyti, kai reikšmė netelpa: laukas → kitas tos šeimos vienetas.
PASIULYMAS = {
    'engine_capacity': 'cm3',
}


def _dec(reiksme):
    if reiksme is None or reiksme == '':
        return None
    try:
        return Decimal(str(reiksme).replace(',', '.').replace(' ', '')
                       .replace(' ', ''))
    except (InvalidOperation, ValueError, TypeError):
        return None


def normalizuok_vieneta(vienetas):
    v = (vienetas or '').strip()
    return SINONIMAI.get(v, v)


def saugojimo_vienetas(laukas):
    aprasas = VIENETAI.get(laukas)
    return aprasas[0] if aprasas else None


def vienetas_is_posto(post, laukas):
    """Kurio vieneto reikšmė atkeliavo. Nenurodytas — saugojimo."""
    v = normalizuok_vieneta((post or {}).get('%s_unit' % laukas, ''))
    aprasas = VIENETAI.get(laukas)
    if not aprasas:
        return v or None
    return v if v in aprasas[1] else aprasas[0]


def i_saugojima(laukas, reiksme, vienetas=None):
    """Reikšmė nurodytu vienetu → saugojimo vienetu.

    Nežinomas laukas ar vienetas — reikšmė grąžinama tokia, kokia buvo:
    normalizavimas niekada nepablogina to, kas jau teisinga.
    """
    skaicius = _dec(reiksme)
    if skaicius is None:
        return None
    aprasas = VIENETAI.get(laukas)
    if not aprasas:
        return skaicius
    saugojimo, santykiai = aprasas
    v = normalizuok_vieneta(vienetas) or saugojimo
    daugiklis = santykiai.get(v)
    if not daugiklis or v == saugojimo:
        return skaicius
    return skaicius / daugiklis


def is_saugojimo(laukas, reiksme, vienetas):
    """Saugojimo vienetu → nurodytu vienetu (žinutėms)."""
    skaicius = _dec(reiksme)
    if skaicius is None:
        return None
    aprasas = VIENETAI.get(laukas)
    if not aprasas:
        return skaicius
    saugojimo, santykiai = aprasas
    v = normalizuok_vieneta(vienetas) or saugojimo
    daugiklis = santykiai.get(v)
    if not daugiklis or v == saugojimo:
        return skaicius
    return skaicius * daugiklis


def suapvalink(laukas, reiksme):
    """Reikšmė teksto pavidalu, lauko tikslumu."""
    skaicius = _dec(reiksme)
    if skaicius is None:
        return ''
    po_kablelio = TIKSLUMAS.get(laukas, 2)
    kvantas = Decimal(1) if po_kablelio == 0 else Decimal('1').scaleb(-po_kablelio)
    return format(skaicius.quantize(kvantas), 'f')


def riba(laukas):
    """Dalykinė riba saugojimo vienetais arba None."""
    return RIBOS.get(laukas)


def rodomas(vienetas):
    """POST vardas → tai, ką žmogus mato („cm3" → „cm³")."""
    return {'cm3': 'cm³'}.get(vienetas, vienetas)


def sk(reiksme, po_kablelio=1):
    """Skaičius žinutei: 10837 → „10 837", 10.8 → „10,8"."""
    skaicius = _dec(reiksme)
    if skaicius is None:
        return ''
    suapvalintas = skaicius.quantize(Decimal(1) if skaicius == skaicius.to_integral()
                                     else Decimal('0.1') ** 0)
    try:
        sveikas = int(skaicius)
    except (ValueError, InvalidOperation):
        return str(skaicius)
    if skaicius == sveikas:
        tekstas = '{:,}'.format(sveikas).replace(',', ' ')
    else:
        tekstas = ('{:,.%df}' % po_kablelio).format(float(skaicius))
        tekstas = tekstas.replace(',', ' ').replace('.', ',')
    return tekstas


def per_didele(laukas, kanonine, vienetas=None):
    """Žinutė, kai reikšmė viršija dalykinę ribą. None — jei telpa.

    Tekste įvardijam VIENETĄ ir, jei ta pati reikšmė kitu vienetu tilptų,
    pasiūlom jį — būtent taip 10837 tampa suprantama klaida, o ne 500.
    """
    virsus = RIBOS.get(laukas)
    skaicius = _dec(kanonine)
    if virsus is None or skaicius is None or skaicius <= virsus:
        return None

    saugojimo = saugojimo_vienetas(laukas) or ''
    v = normalizuok_vieneta(vienetas) or saugojimo
    ivesta = is_saugojimo(laukas, skaicius, v)

    tekstas = _('%(laukas)s negali viršyti %(riba)s %(vnt)s '
                '(įvedėte %(ivesta)s %(vnt)s)') % {
        'laukas': _('Variklio darbinis tūris') if laukas == 'engine_capacity'
                  else laukas,
        'riba': sk(is_saugojimo(laukas, virsus, v)),
        'vnt': rodomas(v),
        'ivesta': sk(ivesta),
    }
    kitas = PASIULYMAS.get(laukas)
    if kitas and kitas != v:
        # Ar ta pati reikšmė kitu vienetu tilptų? Tada tai beveik tikrai
        # apsirikimas, o ne per didelis variklis.
        kitu = i_saugojima(laukas, ivesta, kitas)
        if kitu is not None and kitu <= virsus:
            tekstas += ' — ' + (_('gal norėjote %(kitas)s?')
                                % {'kitas': rodomas(kitas)})
    return tekstas


# ═══════════════════════════════════════════════════════════════════
# FORMOMS IR VAIZDAMS
# Lauko nebuvimą skiriam nuo tuščios reikšmės — „nėra" reiškia
# „nekeičiam", o tuščia reikšmė gali reikšti „išvalyk".
_NERA = object()


def reiksme(post, laukas, numatyta=None):
    """Lauko reikšmė SAUGOJIMO vienetu iš bet kokio žodyno.

    `post` — bet kas, kas turi `.get()` (QueryDict, dict, cleaned_data).
    Reikalaujam TIK `.get()`: autosave'as siunčia JSON'ą ir apvynioja jį
    savo klase be `__contains__`, tad `laukas in post` čia lūžtų
    (TypeError → 500 kiekvienam autosave'ui). Nesant lauko, `.get()`
    grąžina `_NERA` ir mes atiduodam numatytąją reikšmę.

    Nieko nekeičia: grąžina naują reikšmę, o šaltinis lieka toks, koks
    buvo.

        listing.engine_capacity = units.reiksme(request.POST,
                                                'engine_capacity')
    """
    if post is None:
        return numatyta
    tekstas = post.get(laukas, _NERA)
    if tekstas is _NERA:
        return numatyta
    if isinstance(tekstas, str):
        tekstas = tekstas.strip()
    if tekstas in (None, ''):
        return numatyta
    rezultatas = i_saugojima(laukas, tekstas, vienetas_is_posto(post, laukas))
    if rezultatas is None:
        return numatyta
    return lauko_tikslumu(laukas, rezultatas)


def lauko_tikslumu(laukas, reiksme):
    """Suapvalina lauko tikslumu.

    Sveikiems laukams (rida, galia, masė) grąžinam `int`: Decimal su
    trupmena būtų arba nukirstas, arba iš viso nepriimtas.
    """
    skaicius = _dec(reiksme)
    if skaicius is None:
        return None
    po_kablelio = TIKSLUMAS.get(laukas)
    if po_kablelio == 0:
        return int(skaicius.quantize(Decimal(1)))
    if po_kablelio:
        return skaicius.quantize(Decimal('1').scaleb(-po_kablelio))
    return skaicius


def normalizuotas(post, laukai=None):
    """NAUJAS žodynas, kuriame vienetų laukai jau saugojimo vienetais.

    Originalas nepaliečiamas. Naudinga vaizdams, kurie POST'ą paduoda
    toliau vienu gabalu (pvz. sunkvežimių `_save_form_to_listing`).
    """
    # QueryDict'ui — jo paties kopija: vaizdai naudoja `getlist()`
    # (įranga, žymimieji laukeliai), o paprastas dict to nemoka.
    if hasattr(post, 'getlist') and hasattr(post, 'copy'):
        kopija = post.copy()
        kopija._mutable = True
    else:
        kopija = dict(post.items()) if hasattr(post, 'items') else dict(post)
    for laukas in (laukai or VIENETAI):
        if laukas not in kopija:
            continue
        saugojimo = saugojimo_vienetas(laukas)
        v = vienetas_is_posto(kopija, laukas)
        if not v or v == saugojimo:
            continue
        nauja = i_saugojima(laukas, kopija.get(laukas), v)
        if nauja is None:
            continue
        kopija[laukas] = suapvalink(laukas, nauja)
        kopija['%s_unit' % laukas] = saugojimo
    return kopija


class UnitNormalizationMixin:
    """Django formoms: `<laukas>_unit` → saugojimo vienetas PRIEŠ validaciją.

    Naudojimas:

        class Step3VehicleDataForm(UnitNormalizationMixin, forms.Form):
            VIENETU_LAUKAI = ('engine_capacity', 'power', 'mileage')

    Be `VIENETU_LAUKAI` imami visi formos laukai, kuriems vienetai
    aprašyti (VIENETAI). Vienetas paimamas iš `self.data`, nes pats
    `<laukas>_unit` paprastai nėra formos laukas.
    """

    VIENETU_LAUKAI = None

    def _vienetu_laukai(self):
        if self.VIENETU_LAUKAI is not None:
            return self.VIENETU_LAUKAI
        return [v for v in getattr(self, 'fields', {}) if v in VIENETAI]

    def clean(self):
        isvalyta = super().clean()
        if not isinstance(isvalyta, dict):
            return isvalyta
        for laukas in self._vienetu_laukai():
            if isvalyta.get(laukas) in (None, ''):
                continue
            v = vienetas_is_posto(getattr(self, 'data', {}) or {}, laukas)
            if not v or v == saugojimo_vienetas(laukas):
                continue
            nauja = i_saugojima(laukas, isvalyta[laukas], v)
            if nauja is not None:
                isvalyta[laukas] = lauko_tikslumu(laukas, nauja)
        return isvalyta
