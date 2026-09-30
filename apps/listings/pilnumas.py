# -*- coding: utf-8 -*-
"""
SKELBIMO PILNUMAS — ko trūksta, kad skelbimas galėtų būti viešas.

Vienas šaltinis visiems: Listing.activate() (neleidžia aktyvuoti),
aktyvavimo puslapis (/listings/<id>/aktyvuoti/ → redagavimas su
konkrečiais laukais), skelbimo puslapis (neišlaikantis — ne viešas) ir
būsenos užrašas „Juodraštis – trūksta: …".

Grąžinami FORMOS laukų vardai (name=""), kad forma juos pažymėtų
(formos_klaidos_tags → static/js/form_validation.js).

Anksčiau buvo trys skirtingos patikros: activate() žiūrėjo tik į
nuotraukas, select-plan — į PAPILDOMI_LAUKAI, o senas
/<id>/activation-plans/ POST nežiūrėjo į nieką (taip #869 tapo aktyvus
be nuotraukų). Be to, PAPILDOMI_LAUKAI reikalavo sunkiasvorio tipo net
toms subkategorijoms, kurių formoje to lauko nėra (vilkikai, #867), ir
ridos naujiems automobiliams.
"""

# Ko dar reikalaujam iš kiekvienos kategorijos — TIK tų laukų, kuriuos jos
# forma iš tikrųjų renka (modelio laukų vardai).
PAPILDOMI_LAUKAI = {
    'cars': ('year', 'brand_id', 'body_type', 'transmission_id', 'doors', 'mileage'),
    'motorcycles': ('year',),
    'trucks': ('year', 'truck_brand_id', 'truck_model_text', 'truck_type'),
    'trailers': ('year',),
    'agriculture': ('year',),
    'construction': ('year',),
    'forestry': ('year',),
    'loading-equipment': ('year',),
    'camping-houses': ('year',),
}

# Modelio laukas → formos name="" (kur skiriasi).
FORMOS_LAUKAS = {'brand_id': 'brand', 'transmission_id': 'transmission',
                 'truck_brand_id': 'truck_brand', 'subcategory_id': 'subcategory'}

# Skaitytojui — ko trūksta (būsenos užrašui „Juodraštis – trūksta: …").
PAVADINIMAS = {
    'price': 'kaina', 'country': 'šalis', 'city': 'miestas', 'images': 'nuotraukos',
    'year': 'metai', 'brand': 'markė', 'body_type': 'kėbulo tipas',
    'transmission': 'pavarų dėžė', 'doors': 'durų skaičius', 'mileage': 'rida',
    'truck_brand': 'markė', 'truck_model_text': 'modelis', 'truck_type': 'tipas',
    'condition': 'būklė', 'subcategory': 'kategorija',
}


def _reikalingas(listing, laukas):
    """Ar kategorijos laukas šiam skelbimui iš tikrųjų renkamas formoje."""
    slug = listing.vehicle_type.slug if listing.vehicle_type_id else ''
    if slug == 'trucks':
        # Sunkiasvorių forma rodo skirtingus laukus pagal subkategoriją
        from apps.listings import sunkusis
        sub = listing.subcategory.slug if listing.subcategory_id else ''
        forma = FORMOS_LAUKAS.get(laukas, laukas)
        return sunkusis.rodyti(sub, forma)
    return True


def _uzpildytas(listing, laukas):
    reiksme = getattr(listing, laukas, None)
    if laukas == 'mileage':
        # Naujam — 0 km teisinga reikšmė; naudotam 0 reiškia „neįvesta"
        if listing.condition == 'new':
            return reiksme is not None
        return bool(reiksme)
    if isinstance(reiksme, str):
        return bool(reiksme.strip())
    return bool(reiksme)


def trukstami_laukai(listing):
    """Formos laukų vardai, kurių trūksta, kad skelbimas būtų viešas."""
    from apps.listings.views import MOTO_GEAR_SLUGS

    laukai = []
    if not (listing.price and listing.price > 0):
        laukai.append('price')
    if not listing.country:
        laukai.append('country')
    if not listing.city or listing.city.strip() in ('—', '-'):
        laukai.append('city')

    sub = listing.subcategory.slug if listing.subcategory_id else ''
    if sub in MOTO_GEAR_SLUGS:
        papildomi = ('subcategory_id', 'condition')
    else:
        slug = listing.vehicle_type.slug if listing.vehicle_type_id else ''
        papildomi = PAPILDOMI_LAUKAI.get(slug, ())
    for laukas in papildomi:
        if _reikalingas(listing, laukas) and not _uzpildytas(listing, laukas):
            laukai.append(FORMOS_LAUKAS.get(laukas, laukas))

    if not listing.turi_nuotrauku():
        laukai.append('images')
    return laukai


def trukstamu_tekstas(laukai):
    """„kaina, miestas, nuotraukos" — skaitytojui."""
    from django.utils.translation import gettext as _
    return ', '.join(_(PAVADINIMAS.get(l, l)) for l in laukai)
