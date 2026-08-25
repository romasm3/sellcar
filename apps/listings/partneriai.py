# -*- coding: utf-8 -*-
"""
PARTNERIAI IR REKLAMA — /partneriai/

Partnerių sąrašas laikomas čia, vienoje vietoje: naujas partneris = viena
eilutė. Pirmas laukas — ar rodyti; kol sutartis nepasirašyta, paliekam
False, kad puslapyje neatsirastų ryšys, kurio dar nėra.

    (rodyti, vardas, kategorija, aprašymas, adresas, logotipas)

`logotipas` — failo vardas kataloge static/partneriai/ (nebūtina; be jo
rodoma vardo pirmoji raidė).
"""

from django.utils.translation import gettext_lazy as _

PARTNERIAI = [
    (False, 'Carfax', _('Istorijos ataskaitos'),
     _('Transporto priemonės istorijos ataskaita pagal VIN: eismo įvykiai, '
       'ridos įrašai, savininkų skaičius.'),
     'https://carfaxreport.eu/', 'carfax.svg'),

    (False, 'Soft Power', _('Programinė įranga'),
     _('Sprendimai prekiautojams: skelbimų valdymas, klientų užklausos, '
       'ataskaitos.'),
     '', 'soft-power.svg'),
]


def _logo_yra(failas):
    """Ar logotipo failas tikrai įkeltas į static/partneriai/."""
    if not failas:
        return False
    from django.contrib.staticfiles import finders
    return bool(finders.find('partneriai/%s' % failas))


def matomi_partneriai():
    """Tik įjungti partneriai — tokia tvarka, kokia surašyti.

    Jei logotipo failo dar nėra, jį praleidžiam — kortelėje lieka vardo
    raidė, o ne sugadinto paveikslėlio ženklas.
    """
    return [
        {'vardas': v, 'kategorija': k, 'aprasymas': a, 'url': u,
         'logo': lg if _logo_yra(lg) else ''}
        for rodyti, v, k, a, u, lg in PARTNERIAI if rodyti
    ]
