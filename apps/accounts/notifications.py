# -*- coding: utf-8 -*-
"""
LAIŠKŲ NUSTATYMAI — VIENA PATIKRA VISIEMS SIUNTIMAMS.

    galima_siusti(user, 'tipas') -> bool

Ją kviečia KIEKVIENA laiško siuntimo vieta: apps/listings/emails/sender.py
(send_scenario — dauguma laiškų) ir siusk() žemiau (tiesioginiai
siuntimai valdymo komandose). Naujas laiškas = naujas scenarijaus kodas
SCENARIJU_TIPAS žodyne arba siusk(..., tipas=...) — kitaip jis nepraeis
pro nustatymus ir niekada netaps „sisteminiu" netyčia.

Tipai:
  sistema        — slaptažodžio atkūrimas, el. pašto patvirtinimas,
                   mokėjimai, administratoriui: siunčiama VISADA
  aktyvavimas    — priminimai aktyvuoti juodraštį („Activate my listing")
  galiojimas     — skelbimo galiojimo pabaiga / pasibaigęs
  susidomejimas  — peržiūros, išsaugojimai, populiarumas, savaitės statistika
  skelbimai      — kiti apie MANO skelbimą (paskelbtas, parduotas…)
  zinutes        — pirkėjų žinutės ir užklausos
  paieskos       — išsaugotos paieškos, įsiminti skelbimai, sekami pardavėjai
  rinkodara      — akcijos, TOP, panašūs skelbimai

„Nesiųsti man jokių laiškų apie mano skelbimus" (Profile.
email_apie_skelbimus_isjungta) blokuoja visus MANO_SKELBIMU tipus.

Atsisakymo nuoroda kiekvieno ne sisteminio laiško apačioje —
pasirašyta (TimestampSigner), išjungia TĄ VIENĄ tipą be prisijungimo.
"""
import logging

from django.conf import settings
from django.core import signing
from django.urls import reverse
from django.utils import translation
from django.utils.html import escape
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy

logger = logging.getLogger(__name__)

SISTEMA = 'sistema'
MANO_SKELBIMU = frozenset({'aktyvavimas', 'galiojimas', 'susidomejimas', 'skelbimai'})

# tipas → Profile laukas (None — tik pagrindinis jungiklis)
TIPO_LAUKAS = {
    'aktyvavimas': 'email_aktyvavimo_priminimai',
    'galiojimas': 'email_galiojimas',
    'susidomejimas': 'email_susidomejimas',
    'skelbimai': None,
    'zinutes': 'email_messages',
    'paieskos': 'email_notifications',
    'rinkodara': 'marketing_emails',
}

TIPO_PAVADINIMAS = {
    'aktyvavimas': gettext_lazy('Priminimai aktyvuoti neaktyvuotą skelbimą'),
    'galiojimas': gettext_lazy('Pranešimai apie skelbimo galiojimo pabaigą'),
    'susidomejimas': gettext_lazy('Pranešimai apie skelbimo peržiūras ir susidomėjimą'),
    'skelbimai': gettext_lazy('Laiškai apie mano skelbimus'),
    'zinutes': gettext_lazy('Žinutės iš kitų naudotojų'),
    'paieskos': gettext_lazy('Nauji skelbimai pagal išsaugotas paieškas'),
    'rinkodara': gettext_lazy('Akcijos ir naujienos'),
}

SCENARIJU_TIPAS = {
    'draft_reminder_first': 'aktyvavimas',
    'draft_reminder_24h': 'aktyvavimas',
    'draft_reminder_daily': 'aktyvavimas',
    'listing_expiring_soon': 'galiojimas',
    'listing_expired': 'galiojimas',
    'listing_expired_reminder': 'galiojimas',
    'listing_auto_renew_reminder': 'galiojimas',
    'listing_first_views': 'susidomejimas',
    'listing_views_milestone': 'susidomejimas',
    'listing_popular': 'susidomejimas',
    'listing_saved_by_users': 'susidomejimas',
    'listing_weekly_stats': 'susidomejimas',
    'listing_no_sale_reminder': 'susidomejimas',
    'listing_similar_sold': 'susidomejimas',
    'listing_photo_quality_tips': 'susidomejimas',
    'listing_published': 'skelbimai',
    'listing_sold_confirmation': 'skelbimai',
    'listing_reported': 'skelbimai',
    'contact_seller': 'zinutes',
    'contact_seller_reply': 'zinutes',
    'contact_seller_unanswered': 'zinutes',
    'new_message_notification': 'zinutes',
    'saved_listing_price_drop': 'paieskos',
    'saved_listing_sold': 'paieskos',
    'saved_listing_updated': 'paieskos',
    'saved_listings_list': SISTEMA,      # žmogus pats paprašė sąrašo
    'saved_search_first_results': 'paieskos',
    'saved_search_new_results': 'paieskos',
    'saved_search_price_drops': 'paieskos',
    'followed_seller_new_listing': 'paieskos',
}


def tipas_pagal_scenariju(code):
    """Scenarijaus kodas → tipas. Nežinomas NIEKADA netampa „sisteminiu"."""
    if code in SCENARIJU_TIPAS:
        return SCENARIJU_TIPAS[code]
    if code.startswith(('account_', 'admin_', 'payment_')):
        return SISTEMA
    if code.startswith('marketing_'):
        return 'rinkodara'
    if code.startswith('listing_') or code.startswith('draft_'):
        return 'skelbimai'
    return 'paieskos'


def galima_siusti(user, tipas):
    """Ar šiam naudotojui galima siųsti šio tipo laišką."""
    if tipas == SISTEMA or user is None:
        return True
    profilis = getattr(user, 'profile', None)
    if profilis is None:
        return True
    if tipas in MANO_SKELBIMU and getattr(profilis, 'email_apie_skelbimus_isjungta', False):
        return False
    laukas = TIPO_LAUKAS.get(tipas)
    return True if laukas is None else bool(getattr(profilis, laukas, True))


def gavejas_pagal_pasta(pastas):
    """Naudotojas pagal el. paštą (kai siuntėjas jo neperdavė)."""
    from django.contrib.auth import get_user_model
    if not pastas:
        return None
    return get_user_model().objects.filter(email__iexact=pastas).select_related('profile').first()


def gavejo_kalba(user):
    """Laiško kalba — iš profilio; tuščia → settings.LANGUAGE_CODE."""
    profilis = getattr(user, 'profile', None) if user else None
    kalba = (getattr(profilis, 'language', '') or '').strip()
    galimos = {k for k, _v in settings.LANGUAGES}
    return kalba if kalba in galimos else settings.LANGUAGE_CODE


# ── Atsisakymas be prisijungimo ─────────────────────────────────────
ATSISAKYMO_DRUSKA = 'autoleft.atsisakymas'
ATSISAKYMO_GALIOJIMAS = 60 * 60 * 24 * 365      # metai


def atsisakymo_tokenas(user, tipas):
    return signing.TimestampSigner(salt=ATSISAKYMO_DRUSKA).sign(f'{user.pk}:{tipas}')


def atsisakymo_nuoroda(user, tipas):
    from urllib.parse import urlencode
    return (f"{settings.SITE_URL}{reverse('accounts:atsisakyti')}"
            f"?{urlencode({'t': atsisakymo_tokenas(user, tipas)})}")


def tokeno_turinys(tokenas):
    """(user_id, tipas) arba None, jei tokenas blogas / pasenęs."""
    try:
        reiksme = signing.TimestampSigner(salt=ATSISAKYMO_DRUSKA).unsign(
            tokenas or '', max_age=ATSISAKYMO_GALIOJIMAS)
        uid, tipas = reiksme.split(':', 1)
        return int(uid), tipas
    except (signing.BadSignature, ValueError):
        return None


def isjunk(user, tipas):
    """Išjungia vieną tipą (atsisakymo nuoroda)."""
    profilis = user.profile
    laukas = TIPO_LAUKAS.get(tipas)
    if laukas:
        setattr(profilis, laukas, False)
        profilis.save(update_fields=[laukas])
    elif tipas in MANO_SKELBIMU:
        profilis.email_apie_skelbimus_isjungta = True
        profilis.save(update_fields=['email_apie_skelbimus_isjungta'])


def prijunk_atsisakyma(user, tipas, tekstas, html=None):
    """Prideda „Atsisakyti šių pranešimų" prie laiško (ne sisteminiams)."""
    if user is None or tipas == SISTEMA or tipas not in TIPO_LAUKAS:
        return tekstas, html
    nuoroda = atsisakymo_nuoroda(user, tipas)
    with translation.override(gavejo_kalba(user)):
        uzrasas = _('Atsisakyti šių pranešimų')
    tekstas = f'{tekstas.rstrip()}\n\n--\n{uzrasas}: {nuoroda}\n'
    if html:
        blokas = (f'<p style="text-align:center;font-size:12px;color:#9ca3af;margin:16px 0 0;">'
                  f'<a href="{escape(nuoroda)}" style="color:#9ca3af;">{escape(uzrasas)}</a></p>')
        html = html.replace('</body>', blokas + '</body>', 1) if '</body>' in html else html + blokas
    return tekstas, html


def siusk(user, tipas, tema, tekstas, html=None, to_email=None, from_email=None):
    """Tiesioginis siuntimas: patikra → atsisakymo nuoroda → laiškas.

    Grąžina True, jei išsiųsta; False — jei nustatymai to neleidžia.
    """
    from django.core.mail import EmailMultiAlternatives
    pastas = to_email or getattr(user, 'email', '')
    if not galima_siusti(user, tipas):
        logger.info('[pranešimai] nesiunčiama %s (%s): išjungta nustatymuose', pastas, tipas)
        return False
    tekstas, html = prijunk_atsisakyma(user, tipas, tekstas, html)
    laiskas = EmailMultiAlternatives(subject=tema, body=tekstas,
                                     from_email=from_email or settings.DEFAULT_FROM_EMAIL,
                                     to=[pastas])
    if html:
        laiskas.attach_alternative(html, 'text/html')
    laiskas.send()
    return True
