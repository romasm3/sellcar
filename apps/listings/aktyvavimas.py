# -*- coding: utf-8 -*-
"""
AKTYVAVIMAS — viena vieta visiems keliams.

    neaktyvus skelbimas → „Aktyvuoti" (POST) → trūksta ko nors?
        taip → redagavimas (/<id>/edit/) su KONKREČIAIS laukais
        ne   → aktyvuojama nemokamai → „pavyko"

Mokėjimas kol kas IŠJUNGTAS (MOKEJIMAI_IJUNGTI = False): jokio plano,
trukmės ar paslaugų pasirinkimo. Įjungus — tas pats kelias veda į planų
puslapį (listing_select_plan), kuris lieka kode ateičiai.

Būsena keičiama TIK per POST. Anksčiau GET /listings/<id>/select-plan/
ant aktyvaus skelbimo tyliai pratęsdavo galiojimą — perkrovus puslapį
ar naršyklei iš anksto užkrovus nuorodą. Senas /<id>/activation-plans/
POST aktyvuodavo be jokios patikros (taip #869 tapo viešas be nuotraukų).

Šiame modulyje views neimportuojamas modulio lygiu — jį importuoja
kūrimo formų vaizdai, o views importuoja juos.
"""
from django.shortcuts import redirect


def aktyvuok(request, listing):
    """POST veiksmas: aktyvuoja arba nukreipia į redagavimą su trūkumais."""
    from .constants import mokejimai_ijungti
    from . import views

    if mokejimai_ijungti():
        return redirect('listing_select_plan', pk=listing.pk)
    if listing.status == 'sold':
        return redirect('listing_edit_hub', pk=listing.pk)
    laukai = listing.trukstami_laukai()
    if laukai:
        return views._i_redagavima_su_trukstamais(request, listing, laukai)
    return views._publikuok_nemokamai(request, listing)
