# -*- coding: utf-8 -*-
"""
SUNKIOJO TRANSPORTO SUBKATEGORIJOS — KURIE LAUKAI KURIAI RODOMI.

Penkios subkategorijos yra ne viena bendra forma, o penkios formos su
savais laukų rinkiniais (etalonas: docs/autogidas-sunkusis-laukai.md).
Iki šiol visos rodė tą patį rinkinį, todėl vilkikas prašė „Tipo" iš
sunkvežimių antstatų sąrašo, o ašių skaičiaus — kur jis tikrai
reikalingas — nebuvo iš viso.

Slug'ai — tie patys, kuriuos naudoja pikeris ir paieškos panelė
(apps/listings/views.py PICKER_SUBCATEGORIES['trucks'],
apps/listings/context_processors.py SECTIONS['trucks']).

Kaip skaityti lentelę:

    SLEPIAMI  — laukai, kurių ta subkategorija NErodo;
    RODOMI    — laukai, kuriuos rodo TIK ji.

Ko lentelėje nėra, tas rodomas visoms — taip forma lieka tokia pati,
kokia buvo, o skiriasi tik įvardyti laukai. Naujam etalono punktui
užtenka vienos eilutės čia; šablonas ir vaizdas nekeičiami.
"""
from django.utils.translation import gettext_lazy as _

# Subkategorijų slug'ai (SubCategory.slug po „trucks" kategorija)
SUNKVEZIMIAI = 'trucks'
VILKIKAI = 'semi-trucks-tractors'
AUTOTRAUKINIAI = 'vehicle-transporters'
AUTOBUSAI = 'buses'
KOMUNALINIS = 'municipal-transport'

VISOS = (SUNKVEZIMIAI, VILKIKAI, AUTOTRAUKINIAI, AUTOBUSAI, KOMUNALINIS)

# Trumpas vardas antraštei („MAN 18.510 4x2 2022 m Vilkikas").
# Vienaskaita — antraštėje kalbama apie vieną skelbimą.
ANTRASTES_VARDAS = {
    SUNKVEZIMIAI: _('Sunkvežimis'),
    VILKIKAI: _('Vilkikas'),
    AUTOTRAUKINIAI: _('Autovežis'),
    AUTOBUSAI: _('Autobusas'),
    KOMUNALINIS: _('Komunalinio ūkio transportas'),
}

# ── Kas kuriai subkategorijai rodoma ────────────────────────────────
#
# VILKIKAI: „Tipas" yra sunkvežimių antstatų sąrašas (savivartis,
# cisterna, refrižeratorius…), vilkikui jis beprasmis — etalone jo ten
# nėra. Užtat yra ašių skaičius, o miegamų vietų laukas jau buvo.
SLEPIAMI = {
    VILKIKAI: ('truck_type',),
}

RODOMI = {
    VILKIKAI: ('axle_count',),
}


def normalizuok(slug):
    """Bet koks slug'as → viena iš penkių arba „trucks"."""
    slug = (slug or '').strip()
    return slug if slug in VISOS else SUNKVEZIMIAI


def rodyti(slug, laukas):
    """Ar laukas rodomas šiai subkategorijai."""
    slug = normalizuok(slug)
    if laukas in SLEPIAMI.get(slug, ()):
        return False
    # Laukas, priskirtas TIK kitai subkategorijai, čia nerodomas
    for kita, laukai in RODOMI.items():
        if laukas in laukai:
            return kita == slug
    return True


def laukai(slug):
    """Žodynas šablonui: {lauko vardas: rodyti?}.

    Šablone tada `{% if rodomi.truck_type %}` — be jokios logikos
    pačiame šablone.
    """
    slug = normalizuok(slug)
    vardai = set()
    for reiksmes in list(SLEPIAMI.values()) + list(RODOMI.values()):
        vardai.update(reiksmes)
    return {v: rodyti(slug, v) for v in vardai}


def antrastes_vardas(slug):
    return ANTRASTES_VARDAS.get(normalizuok(slug), '')
