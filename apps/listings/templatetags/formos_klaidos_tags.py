# -*- coding: utf-8 -*-
"""Formos klaidų surinkimas šablonui — žr. apps/listings/formos_klaidos.py."""
import json

from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from apps.listings import formos_klaidos

register = template.Library()


@register.simple_tag(takes_context=True)
def formos_klaidos_kontekstas(context):
    """Klaidos iš view'o konteksto arba, jei jo nėra — iš `messages`.

    Naujuose view'uose užtenka paduoti error_fields/error_messages
    (formos_klaidos.kontekstas()). Seni view'ai klaidas siunčia per
    messages.error() — tada jas atpažįstam pagal tekstą, kad nereikėtų
    perrašyti visų 28 formų iš karto.
    """
    laukai = context.get('error_fields')
    zinutes = context.get('error_messages')
    eilutes = context.get('form_errors')

    if not laukai and not eilutes:
        # Aktyvavimas rado neužpildytą skelbimą ir nukreipė čia
        # (views.listing_select_plan): konkretūs trūkstami laukai
        # atkeliauja per sesiją — kontekstas po nukreipimo dingsta.
        laukai, zinutes = _trukstami_is_sesijos(context.get('request'))

    if laukai and not eilutes:
        # View'as padavė tik laukus — dėžutės eilutes pasidarom patys
        eilutes = [{'laukas': l, 'tekstas': (zinutes or {}).get(l)
                                            or formos_klaidos.tekstas_laukui(l)}
                   for l in laukai]

    if not laukai and not eilutes:
        # `messages` iteruojasi kelis kartus tame pačiame atvaizdavime,
        # tad senas šablono blokas (jei toks dar yra) nenukenčia.
        #
        # TIK KLAIDOS. Anksčiau čia patekdavo visos žinutės, tad po
        # sėkmingo išsaugojimo žmogus matydavo „Ištaisykite šias
        # klaidas: Listing updated successfully." — sėkmė raudonoje
        # dėžutėje. Sėkmę, informaciją ir įspėjimus rodo base.html
        # (kiekvieną savo spalva), o čia lieka tik tai, ką reikia
        # taisyti.
        tekstai = formos_klaidos.tik_klaidu_tekstai(context.get('messages'))
        surinkta = formos_klaidos.kontekstas(tekstai)
        laukai = surinkta['error_fields']
        zinutes = surinkta['error_messages']
        eilutes = surinkta['form_errors']

    return {
        'laukai': laukai or [],
        'zinutes': zinutes or {},
        'eilutes': eilutes or [],
    }


def _formos_skelbimo_pk(request):
    """Kurio skelbimo forma atidaryta: /<pk>/edit-…/ arba ?edit= / ?draft_id=."""
    atitikmuo = getattr(request, 'resolver_match', None)
    pk = (atitikmuo.kwargs.get('pk') if atitikmuo else None) \
        or request.GET.get('edit') or request.GET.get('draft_id')
    return str(pk) if pk else ''


def _trukstami_is_sesijos(request):
    """Trūkstami laukai iš sesijos — TIK tam pačiam skelbimui ir vieną kartą."""
    if request is None or not hasattr(request, 'session'):
        return None, None
    irasas = request.session.get(formos_klaidos.SESIJOS_RAKTAS)
    if not irasas or str(irasas.get('pk')) != _formos_skelbimo_pk(request):
        return None, None
    request.session.pop(formos_klaidos.SESIJOS_RAKTAS, None)
    laukai = list(irasas.get('laukai') or [])
    return laukai, formos_klaidos.trukstamu_zinutes(laukai)


@register.simple_tag(takes_context=True)
def formos_klaidos_json(context, laukai, zinutes):
    """JSON blokas, kurį perskaito static/js/form_validation.js."""
    return mark_safe(json.dumps({
        'laukai': list(laukai or []),
        'zinutes': {k: str(v) for k, v in (zinutes or {}).items()},
        'tekstai': {
            'privalomas': _(formos_klaidos.PRIVALOMAS),
            'taisykles': _(formos_klaidos.TAISYKLES),
            'netinkamas': _('Netinkama reikšmė'),
        },
    }, ensure_ascii=False))
