# -*- coding: utf-8 -*-
"""
Paskyros trynimas ir duomenų eksportas (GDPR).

KODĖL ANONIMIZUOJAM, O NE TRINAM EILUTĘ. `user.delete()` per CASCADE
ištrintų ir tai, kas priklauso ne tik jam: jo žinutes kito žmogaus
pokalbiuose (conversations.Message.sender — CASCADE), piniginės ir
mokėjimų įrašus (WalletTransaction, StripeCheckoutSession), atsiliepimus.
Todėl User eilutė lieka, bet:

  • prisijungti nebegalima: is_active=False, slaptažodis nenaudojamas,
    el. paštas pakeistas į istrintas-<id>@istrinta.invalid (negyvas
    domenas — laiškai nebesiunčiami), kitos sesijos nebegalioja
    (ModelBackend neaktyvaus naudotojo nebeatpažįsta);
  • asmens duomenys išvalyti: vardas, pavardė, telefonai, adresas,
    įmonės ir prekiautojo kontaktai, aprašymai, registracijos IP,
    profilio / logotipo / reklaminio paveikslėlio failai ištrinti;
  • skelbimai (Listing, Truck, WheelListing) → 'archived' (anonimui 404),
    jų kontaktinis telefonas, el. paštas, adresas ir pašto kodas išvalyti;
  • asmeniniai sąrašai (išsaugotos paieškos ir skelbimai, peržiūrų
    istorija) ištrinti — iš jų eidavo laiškai;
  • žinutės lieka kitam pokalbio dalyviui, siuntėjas rodomas kaip
    „istrintas-<id>".
"""
import datetime
import decimal
import uuid

from django.db import models, transaction
from django.db.models.fields.files import FieldFile

ISTRINTA_DOMENAS = 'istrinta.invalid'

PROFILIO_ISVALYTI = {
    'bio': '', 'location': '', 'phone_number': '', 'phone_number_secondary': '',
    'street': '', 'house_number': '', 'city': '', 'country': '',
    'company_name': '', 'working_hours': '', 'contact_person': '',
    'company_description': '', 'website': '',
    'dealer_company_name': '', 'dealer_address': '', 'dealer_phone': '',
    'dealer_description': '', 'dealer_working_hours': {},
    'signup_ip': None, 'signup_user_agent': '',
    'public_profile': False, 'show_email': False, 'show_phone': False,
    'email_notifications': False, 'email_messages': False, 'marketing_emails': False,
    'sms_notifications': False, 'price_drop_email': False, 'price_drop_onsite': False,
    'email_apie_skelbimus_isjungta': True,
    'dealer_subscription_active': False, 'private_subscription_active': False,
}
PROFILIO_FAILAI = ('profile_picture', 'company_logo', 'banner_image', 'dealer_logo')
SKELBIMO_KONTAKTAI = ('contact_phone', 'contact_email', 'address', 'postal_code')


def istrinta(user):
    return (user.email or '').endswith('@' + ISTRINTA_DOMENAS)


def _skelbimu_modeliai():
    from apps.listings.models import Listing, Truck, WheelListing
    return (Listing, Truck, WheelListing)


@transaction.atomic
def anonimizuok(user):
    """Ištrina paskyrą (anonimizuoja). Grąžina paslėptų skelbimų skaičių."""
    pk = user.pk
    paslepta = 0
    for M in _skelbimu_modeliai():
        laukai = {f.name for f in M._meta.concrete_fields}
        isvalyti = {k: '' for k in SKELBIMO_KONTAKTAI if k in laukai}
        qs = M.objects.filter(seller=user)
        paslepta += qs.exclude(status='archived').count()
        qs.update(status='archived', **isvalyti)          # .update — be save() šalutinių

    profilis = getattr(user, 'profile', None)
    if profilis is not None:
        for laukas in PROFILIO_FAILAI:
            failas = getattr(profilis, laukas, None)
            if failas:
                try:
                    failas.delete(save=False)
                except Exception:                          # noqa: BLE001 — failo jau nėra
                    setattr(profilis, laukas, None)
        for k, v in PROFILIO_ISVALYTI.items():
            setattr(profilis, k, v)
        profilis.save()

    from apps.listings import models as lm
    for vardas in ('SavedSearch', 'SavedListing', 'SavedListingNotification', 'SavedTruck',
                   'SavedTruckNotification', 'SavedWheelListing', 'PerziuretasSkelbimas'):
        M = getattr(lm, vardas, None)
        if M is not None:
            M.objects.filter(user=user).delete()

    user.username = f'istrintas-{pk}'
    user.email = f'istrintas-{pk}@{ISTRINTA_DOMENAS}'
    user.first_name = ''
    user.last_name = ''
    user.is_active = False
    user.is_staff = False
    user.set_unusable_password()
    user.save()
    return paslepta


# ── Eksportas ─────────────────────────────────────────────────────────
def _reiksme(v):
    if isinstance(v, (datetime.datetime, datetime.date, datetime.time)):
        return v.isoformat()
    if isinstance(v, decimal.Decimal):
        return str(v)
    if isinstance(v, uuid.UUID):
        return str(v)
    if isinstance(v, FieldFile):                           # tuščiam .url kelia klaidą
        return v.name or None
    return v


def _eilute(obj, praleisti=()):
    d = {}
    for f in obj._meta.concrete_fields:
        if f.name in praleisti:
            continue
        if isinstance(f, models.ForeignKey):
            d[f.name] = getattr(obj, f.attname)
        else:
            d[f.name] = _reiksme(getattr(obj, f.name))
    return d


def duomenu_eksportas(user):
    """Viskas, ką saugom apie naudotoją: profilis, skelbimai, žinutės…"""
    from apps.conversations.models import Conversation
    from apps.listings.models import SavedSearch

    profilis = getattr(user, 'profile', None)
    skelbimai = {}
    for M in _skelbimu_modeliai():
        skelbimai[M.__name__] = [_eilute(o) for o in M.objects.filter(seller=user).order_by('pk')]

    pokalbiai = []
    for conv in (Conversation.objects.filter(participants=user)
                 .prefetch_related('participants').order_by('pk')):
        pokalbiai.append({
            'id': conv.pk,
            'skelbimas': conv.listing_id,
            'sukurta': _reiksme(conv.created_at),
            'dalyviai': [p.username for p in conv.participants.all()],
            'zinutes': [{
                'id': m.pk,
                'siuntejas': 'as' if m.sender_id == user.pk else m.sender.username,
                'tekstas': m.content,
                'paveikslelis': _reiksme(m.image),
                'issiusta': _reiksme(m.created_at),
            } for m in conv.messages.select_related('sender').order_by('created_at', 'pk')],
        })

    return {
        'eksportuota': _reiksme(datetime.datetime.now(datetime.timezone.utc)),
        'naudotojas': {
            'id': user.pk, 'username': user.username, 'email': user.email,
            'first_name': user.first_name, 'last_name': user.last_name,
            'date_joined': _reiksme(user.date_joined), 'last_login': _reiksme(user.last_login),
        },
        'profilis': _eilute(profilis, praleisti=('id', 'user')) if profilis else None,
        'skelbimai': skelbimai,
        'pokalbiai': pokalbiai,
        'issaugotos_paieskos': [_eilute(s, praleisti=('user',))
                                for s in SavedSearch.objects.filter(user=user).order_by('pk')],
    }
