# -*- coding: utf-8 -*-
"""
FORMŲ KLAIDOS — viena vieta visoms /create/ formoms.

Kodėl. Klaidos gimė 28 skirtingose vietose ir 28 skirtingais pavidalais:
dalis view'ų kaupia `errors` sąrašą angliškai, dalis lietuviškai, vienas
(trucks) — žodyną pagal lauką. Šablonai jas išpylė vienu `messages`
sąrašu, tad žmogus matydavo „Phone is required", bet ne KURIS laukas
raudonas — o telefone forma ilga ir tas laukas dažnai už ekrano ribų.

Čia klaidos suvedamos į vieną pavidalą:

    error_fields    — laukų vardai (name=""), kuriuos reikia pažymėti
    error_messages  — {lauko vardas: lietuviškas tekstas}
    form_errors     — [{'laukas': ..., 'tekstas': ...}] viršutinei dėžutei

Tekstas → laukas atpažįstamas pagal ŽODYNĄ žemiau, todėl esamų
`errors.append('Phone is required')` perrašinėti nereikia: senas tekstas
randamas, paverčiamas lietuvišku ir susiejamas su lauku. Naujose vietose
geriau iškart rašyti porą ('phone', _('Telefonas yra privalomas')).
"""
from django.utils.translation import gettext as _

PRIVALOMAS = 'Privalomas laukas'
TAISYKLES = 'Turite sutikti su taisyklėmis'


def _t(tekstas):
    """Vertimas paieškai — msgid'ai .po faile yra lietuviški."""
    return _(tekstas)


# ── Tekstas → laukas ────────────────────────────────────────────────
# Raktas sunormalintas: mažosiomis, be galinio taško. Sąrašas surinktas
# iš visų create view'ų (grep errors.append), todėl padengia ir senus
# angliškus, ir jau išverstus lietuviškus variantus.
TEKSTAS_I_LAUKA = {
    # sutikimas
    'you must agree to the terms': 'agree_terms',
    'you must agree to terms and conditions': 'agree_terms',
    'agree_terms: you must agree to the terms': 'agree_terms',
    'turite sutikti su taisyklėmis': 'agree_terms',
    # būklė
    'condition is required': 'condition',
    'būklė yra privaloma': 'condition',
    # metai / mėnuo
    'year is required': 'year',
    'metai yra privalomi': 'year',
    'month is required': 'first_registration_month',
    'mėnuo yra privalomas': 'first_registration_month',
    'invalid month/year combination': 'first_registration_month',
    # kaina
    'price is required': 'price',
    'valid price is required': 'price',
    'kaina yra privaloma': 'price',
    'nuomos kaina parai yra privaloma': 'price',
    # kontaktai
    'phone is required': 'phone',
    'phone: this field is required': 'phone',
    'telefonas yra privalomas': 'phone',
    'city is required': 'city',
    'miestas yra privalomas': 'city',
    'state is required': 'state',
    'state is required for us': 'state',
    'state is required for us listings': 'state',
    'valstija yra privaloma': 'state',
    # markė / modelis
    'brand is required': 'brand',
    'brand not found': 'brand',
    'markė yra privaloma': 'brand',
    'gamintojas yra privalomas': 'brand',
    'model is required': 'model',
    'model not found': 'model',
    'modelis yra privalomas': 'model',
    # techniniai
    'fuel type is required': 'fuel_type',
    'fuel type not found': 'fuel_type',
    'transmission is required': 'transmission',
    'transmission not found': 'transmission',
    'mileage is required': 'mileage',
    'doors is required': 'doors',
    'defects is required': 'defects',
    'body type is required': 'body_type',
    'kėbulo tipas yra privalomas': 'body_type',
    'sėdimų vietų skaičius yra privalomas': 'seats',
    # tipai ir pavadinimai
    'type is required': 'type',
    'tipas yra privalomas': 'type',
    'category is required': 'category',
    'size is required': 'size',
    'material is required': 'material',
    'gender is required': 'gender',
    'part name is required': 'title',
    'pavadinimas yra privalomas': 'title',
    'paslaugos tipas yra privalomas': 'service_type',
    'motociklo tipas yra privalomas': 'motorcycle_type',
    'paskirtis yra privaloma': 'purpose',
    'padargas / savaeigė yra privalomas': 'machine_kind',
    'galingumas w yra privalomas garsiakalbiams': 'power_watts',
}

# ── Laukas → lietuviškas tekstas ────────────────────────────────────
LAUKO_TEKSTAS = {
    'agree_terms': TAISYKLES,
    'condition': 'Būklė yra privaloma',
    'year': 'Metai yra privalomi',
    'first_registration_month': 'Mėnuo yra privalomas',
    'price': 'Kaina yra privaloma',
    'phone': 'Telefonas yra privalomas',
    'city': 'Miestas yra privalomas',
    'state': 'Valstija yra privaloma',
    'brand': 'Markė yra privaloma',
    'model': 'Modelis yra privalomas',
    'fuel_type': 'Kuro tipas yra privalomas',
    'transmission': 'Pavarų dėžė yra privaloma',
    'mileage': 'Rida yra privaloma',
    'doors': 'Durų skaičius yra privalomas',
    'defects': 'Defektai yra privalomi',
    'body_type': 'Kėbulo tipas yra privalomas',
    'seats': 'Sėdimų vietų skaičius yra privalomas',
    'type': 'Tipas yra privalomas',
    'category': 'Kategorija yra privaloma',
    'size': 'Dydis yra privalomas',
    'material': 'Medžiaga yra privaloma',
    'gender': 'Lytis yra privaloma',
    'title': 'Pavadinimas yra privalomas',
    'service_type': 'Paslaugos tipas yra privalomas',
    'motorcycle_type': 'Motociklo tipas yra privalomas',
    'purpose': 'Paskirtis yra privaloma',
    'machine_kind': 'Padargas / savaeigė yra privalomas',
    'power_watts': 'Galingumas W yra privalomas garsiakalbiams',
}

# Laukai, kurių įvedimo elementas turi kitą name= nei klaidos raktas.
# (trucks turi savo markės/modelio lenteles, žr. CLAUDE.md)
LAUKO_ALIASAI = {
    'truck_brand': 'truck_brand',
    'truck_model_text': 'truck_model_text',
    'truck_type': 'truck_type',
}


def _normalizuoti(tekstas):
    return str(tekstas or '').strip().rstrip('.').strip().lower()


def laukas_pagal_teksta(tekstas):
    """Kurio lauko ši klaida. None — nežinom (rodom tik dėžutėje)."""
    svarus = _normalizuoti(tekstas)
    if svarus in TEKSTAS_I_LAUKA:
        return TEKSTAS_I_LAUKA[svarus]
    # „laukas: tekstas" pavidalas (views.py ir trucks_views.py)
    if ':' in svarus:
        galimas = svarus.split(':', 1)[0].strip()
        if galimas in LAUKO_TEKSTAS or galimas in LAUKO_ALIASAI:
            return galimas
        likutis = svarus.split(':', 1)[1].strip()
        if likutis in TEKSTAS_I_LAUKA:
            return TEKSTAS_I_LAUKA[likutis]
    return None


def tekstas_laukui(laukas, atsarginis=''):
    """Lietuviškas tekstas laukui."""
    if laukas in LAUKO_TEKSTAS:
        return _t(LAUKO_TEKSTAS[laukas])
    return atsarginis or _t(PRIVALOMAS)


def kontekstas(klaidos):
    """Iš bet kokio klaidų sąrašo — kontekstas šablonui.

    `klaidos` gali būti:
      · tekstų sąrašas            ['Phone is required', ...]
      · porų sąrašas              [('phone', 'Telefonas yra privalomas')]
      · žodynas                   {'phone': 'Telefonas yra privalomas'}
    Maišyti galima — taip veikia ir seni view'ai, ir nauji.
    """
    if hasattr(klaidos, 'items'):
        klaidos = list(klaidos.items())

    laukai, zinutes, eilutes = [], {}, []
    for irasas in (klaidos or []):
        if isinstance(irasas, (tuple, list)) and len(irasas) == 2:
            laukas, tekstas = irasas[0], irasas[1]
        else:
            laukas, tekstas = laukas_pagal_teksta(irasas), irasas

        if laukas:
            tekstas = tekstas_laukui(laukas)
        else:
            tekstas = str(tekstas)

        if laukas and laukas in zinutes:
            continue                      # tas pats laukas du kartus — užtenka vieno
        if laukas:
            laukai.append(laukas)
            zinutes[laukas] = tekstas
        eilutes.append({'laukas': laukas or '', 'tekstas': tekstas})

    return {
        'error_fields': laukai,
        'error_messages': zinutes,
        'form_errors': eilutes,
    }
