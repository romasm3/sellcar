# -*- coding: utf-8 -*-
"""
AKTYVAVIMAS — „Aktyvuoti" aktyvuoja VISADA (žmogaus sprendimai 2026-10-01).

    [Aktyvuoti] (POST /listings/<id>/activate/) → skelbimas aktyvus →
    atgal į /dashboard/announcements/ su „Skelbimas aktyvuotas" + nuoroda.

Jokių patikrų: ir be nuotraukų (rodomas placeholder), ir be kainos ar
miesto. Vienintelis atsisakymas — ne savininkas (404). Trūkumus savininkas
pataiso „Redaguoti" jau aktyviame skelbime. Jokio plano, paketo, kainos ar
apmokėjimo (MOKEJIMAI_IJUNGTI = False; planų puslapis lieka kode ateičiai).

LAIŠKO NUORODA: GET /listings/<id>/activate/?t=<tokenas> aktyvuoja vienu
paspaudimu, net neprisijungus — tokenas pasirašytas (TimestampSigner,
galioja 30 d.) ir susietas su skelbimu IR jo savininku. Blogas ar
pasenęs tokenas → 403, būsena nekeičiama. Be tokeno GET būsenos nekeičia
(puslapis su POST mygtuku).

Šis modulis views neimportuoja modulio lygiu — jį importuoja kūrimo formų
vaizdai.
"""
from django.contrib import messages
from django.core import signing
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext as _

TOKENO_DRUSKA = 'autoleft.aktyvavimas'
TOKENO_GALIOJIMAS = 60 * 60 * 24 * 30          # 30 dienų


def _zenklas():
    return signing.TimestampSigner(salt=TOKENO_DRUSKA)


def aktyvavimo_tokenas(listing):
    """Pasirašytas tokenas laiško nuorodai (skelbimas + savininkas)."""
    return _zenklas().sign(f'{listing.pk}:{listing.seller_id}')


def aktyvavimo_nuoroda(listing, site_url=''):
    """Pilna vieno paspaudimo nuoroda laiškui."""
    from urllib.parse import urlencode
    return (f"{site_url}{reverse('listing_aktyvuoti', args=[listing.pk])}"
            f"?{urlencode({'t': aktyvavimo_tokenas(listing)})}")


def tokenas_tinka(listing, tokenas):
    """Ar tokenas pasirašytas šiam skelbimui ir jo savininkui ir nepasenęs."""
    try:
        reiksme = _zenklas().unsign(tokenas or '', max_age=TOKENO_GALIOJIMAS)
    except signing.BadSignature:                  # apima SignatureExpired
        return False
    return reiksme == f'{listing.pk}:{listing.seller_id}'


def _paskelbk(listing, user):
    """Aktyvuoja ir (juodraščiui) išsiunčia „paskelbta" laišką."""
    buvo = listing.status
    listing.activate()
    if buvo == 'draft':
        try:
            from .views import _send_listing_published_email
            _send_listing_published_email(listing, user)
        except Exception:                            # laiškas — ne priežastis lūžti
            pass


def _aktyvuota_zinute(request, listing):
    messages.success(request, format_html(
        '{} <a href="{}" class="underline font-semibold">{}</a>',
        _('Skelbimas aktyvuotas.'), reverse('listing_detail', args=[listing.pk]),
        _('Peržiūrėti')))


def aktyvuok(request, listing, grizti='sekme'):
    """POST veiksmas — aktyvuoja visada.

    grizti='sekme'    — kūrimo formos: į „pavyko" puslapį (kaip buvo);
    grizti='skydelis' — mygtukas „Aktyvuoti": atgal į skydelį su žinute.
    """
    from .constants import mokejimai_ijungti

    if mokejimai_ijungti():
        return redirect('listing_select_plan', pk=listing.pk)
    if listing.status == 'sold':
        return redirect('listing_edit_hub', pk=listing.pk)

    buvo = listing.status
    _paskelbk(listing, request.user)

    if grizti == 'skydelis':
        _aktyvuota_zinute(request, listing)
        return redirect('my_listings')
    veiksmas = {'draft': 'published', 'expired': 'reactivated'}.get(buvo, 'extended')
    return redirect(reverse('listing_success', kwargs={'pk': listing.pk}) + f'?action={veiksmas}')


def aktyvuok_pagal_tokena(request, listing):
    """Laiško nuoroda: aktyvuoja ir veda į /<id>/ su žinute (be prisijungimo)."""
    if listing.status != 'sold':
        _paskelbk(listing, listing.seller)
    _aktyvuota_zinute(request, listing)
    return redirect('listing_detail', pk=listing.pk)
