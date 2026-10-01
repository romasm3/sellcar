# -*- coding: utf-8 -*-
"""
AKTYVAVIMAS — „Aktyvuoti" tiesiog aktyvuoja (žmogaus sprendimas 2026-10-01).

    [Aktyvuoti] (POST /listings/<id>/activate/) → skelbimas aktyvus →
    atgal į /dashboard/announcements/ su „Skelbimas aktyvuotas" + nuoroda.

VIENINTELIS stabdys — nėra nė vienos nuotraukos: tada NEaktyvuojam, o
vedam į redagavimą su „Įkelkite bent vieną nuotrauką ir išsaugokite –
skelbimas aktyvuosis". Skelbimas įsimenamas sesijoje (LAUKIA_RAKTAS), ir
kai tik jis turi nuotrauką (išsaugota forma ar AJAX įkėlimas),
AktyvavimoLaukimoMiddleware jį aktyvuoja — antrą kartą spausti nereikia.

Kiti trūkumai (kaina, miestas…) aktyvavimo NEstabdo: savininkas juos
pataiso „Redaguoti" jau aktyviame skelbime. Jokio plano, paketo, kainos
ar apmokėjimo žingsnio (MOKEJIMAI_IJUNGTI = False; planų puslapis lieka
kode ateičiai ir rodomas tik įjungus mokėjimus).

Būsena keičiama TIK per POST. Šis modulis views neimportuoja modulio
lygiu — jį importuoja kūrimo formų vaizdai.
"""
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext as _

LAUKIA_RAKTAS = 'laukia_aktyvavimo'
BE_NUOTRAUKOS = 'Įkelkite bent vieną nuotrauką ir išsaugokite – skelbimas aktyvuosis'


def _paskelbk(listing, user):
    """Aktyvuoja ir (juodraščiui) išsiunčia „paskelbta" laišką. True — pavyko."""
    buvo = listing.status
    if not listing.activate():
        return False
    if buvo == 'draft':
        try:
            from .views import _send_listing_published_email
            _send_listing_published_email(listing, user)
        except Exception:                            # laiškas — ne priežastis lūžti
            pass
    return True


def _laukti_nuotraukos(request, listing):
    """Be nuotraukos — į redagavimą; įsimenam, kad išsaugojus aktyvuotume."""
    from . import formos_klaidos
    laukia = [p for p in request.session.get(LAUKIA_RAKTAS, []) if p != listing.pk]
    request.session[LAUKIA_RAKTAS] = laukia + [listing.pk]
    request.session[formos_klaidos.SESIJOS_RAKTAS] = {'pk': listing.pk, 'laukai': ['images']}
    request.session.modified = True
    messages.warning(request, _(BE_NUOTRAUKOS))
    return redirect(listing.get_edit_url())


def aktyvuok(request, listing, grizti='sekme'):
    """POST veiksmas.

    grizti='sekme'    — kūrimo formos: į „pavyko" puslapį (kaip buvo);
    grizti='skydelis' — mygtukas „Aktyvuoti": atgal į skydelį su žinute.
    """
    from .constants import mokejimai_ijungti

    if mokejimai_ijungti():
        return redirect('listing_select_plan', pk=listing.pk)
    if listing.status == 'sold':
        return redirect('listing_edit_hub', pk=listing.pk)
    if not listing.turi_nuotrauku():
        return _laukti_nuotraukos(request, listing)

    buvo = listing.status
    _paskelbk(listing, request.user)

    if grizti == 'skydelis':
        messages.success(request, format_html(
            '{} <a href="{}" class="underline font-semibold">{}</a>',
            _('Skelbimas aktyvuotas.'), reverse('listing_detail', args=[listing.pk]),
            _('Peržiūrėti')))
        return redirect('my_listings')
    veiksmas = {'draft': 'published', 'expired': 'reactivated'}.get(buvo, 'extended')
    return redirect(reverse('listing_success', kwargs={'pk': listing.pk}) + f'?action={veiksmas}')


class AktyvavimoLaukimoMiddleware:
    """Skelbimas, kurio aktyvavimą stabdė nuotraukų nebuvimas, aktyvuojasi,
    kai tik jis jų turi — po redagavimo formos ar AJAX įkėlimo (POST).

    Žiūrima TIK į to naudotojo sesijoje įsimintus skelbimus, todėl
    kiti užklausų keliai nieko nekainuoja.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        try:
            self._tikrink(request)
        except Exception:                            # niekada nelaužom atsakymo
            pass
        return response

    @staticmethod
    def _tikrink(request):
        if request.method != 'POST' or not hasattr(request, 'session'):
            return
        laukia = request.session.get(LAUKIA_RAKTAS)
        if not laukia or not getattr(request, 'user', None) or not request.user.is_authenticated:
            return
        from .models import Listing
        liko = []
        for listing in Listing.objects.filter(pk__in=laukia, seller=request.user):
            if listing.status in ('draft', 'expired') and listing.turi_nuotrauku():
                if _paskelbk(listing, request.user):
                    messages.success(request, format_html(
                        '{} <a href="{}" class="underline font-semibold">{}</a>',
                        _('Skelbimas aktyvuotas.'),
                        reverse('listing_detail', args=[listing.pk]), _('Peržiūrėti')))
                    continue
            if listing.status in ('draft', 'expired'):
                liko.append(listing.pk)
        request.session[LAUKIA_RAKTAS] = liko
        request.session.modified = True
