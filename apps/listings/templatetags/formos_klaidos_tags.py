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

    if laukai and not eilutes:
        # View'as padavė tik laukus — dėžutės eilutes pasidarom patys
        eilutes = [{'laukas': l, 'tekstas': (zinutes or {}).get(l)
                                            or formos_klaidos.tekstas_laukui(l)}
                   for l in laukai]

    if not laukai and not eilutes:
        # `messages` iteruojasi kelis kartus tame pačiame atvaizdavime,
        # tad senas šablono blokas (jei toks dar yra) nenukenčia.
        tekstai = [str(m) for m in (context.get('messages') or [])]
        surinkta = formos_klaidos.kontekstas(tekstai)
        laukai = surinkta['error_fields']
        zinutes = surinkta['error_messages']
        eilutes = surinkta['form_errors']

    return {
        'laukai': laukai or [],
        'zinutes': zinutes or {},
        'eilutes': eilutes or [],
    }


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
