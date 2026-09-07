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
# NORMALIZAVIMAS UŽKLAUSOJE — viena vieta visoms formoms
# ═══════════════════════════════════════════════════════════════════
class VienetuMiddleware:
    """Reikšmes su ne saugojimo vienetu paverčia saugojimo vienetu.

    Kodėl čia, o ne dvidešimtyje vaizdų: laukai su jungikliais yra ir
    įkėlimo formose, ir paieškos filtruose, ir juodraščių autosave —
    visi jie POST'ą skaito tiesiogiai. Sutvarkius vienoje vietoje,
    kiekvienas iš jų gauna litrus, kilometrus ir kilogramus, nieko
    savyje nekeitęs.

    Įprastai tai NIEKO nekeičia: naršyklė (static/js/unit_toggle.js)
    reikšmę į kanoninį vienetą verčia pati, o `<laukas>_unit` tada yra
    saugojimo vienetas. Verčiam tik tada, kai atkeliauja kitoks — be
    JavaScript'o arba iš išorinio kliento. Dvigubo vertimo būti negali:
    sprendžiam pagal patį lauką, ne pagal spėjimą.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST':
            self._normalizuok(request)
        return self.get_response(request)

    @staticmethod
    def _normalizuok(request):
        try:
            post = request.POST
        except Exception:                      # noqa: BLE001 (pvz. sugadintas kūnas)
            return
        keistini = []
        for laukas, (saugojimo, santykiai) in VIENETAI.items():
            if laukas not in post:
                continue
            v = normalizuok_vieneta(post.get('%s_unit' % laukas, ''))
            if not v or v == saugojimo or v not in santykiai:
                continue
            nauja = i_saugojima(laukas, post.get(laukas), v)
            if nauja is not None:
                keistini.append((laukas, nauja, saugojimo))
        if not keistini:
            return
        kopija = post.copy()
        for laukas, reiksme, saugojimo in keistini:
            kopija[laukas] = suapvalink(laukas, reiksme)
            kopija['%s_unit' % laukas] = saugojimo
        kopija._mutable = False
        request.POST = kopija
