# -*- coding: utf-8 -*-
"""
„IŠTRINTI PASKYRĄ" IR „ATSISIŲSTI MANO DUOMENIS".

Klaida: trynimas niekada neveikė — modalo patvirtinimo laukas neturėjo
name, slaptažodis buvo paslėptas tuščias laukas, check_password('') →
False, o klaidos atveju — peradresavimas į neegzistuojantį šabloną.

Tikrinam (tik testiniai naudotojai, laikina sqlite bazė):
  • modale tikri laukai: password (type=password, required) ir
    patvirtinimas (required); nėra tuščio paslėpto password
  • neteisingas slaptažodis → paskyra NEPALIESTA, „Neteisingas slaptažodis"
  • be „DELETE" → paskyra NEPALIESTA, klaida
  • teisingas slaptažodis + DELETE → „Paskyra ištrinta", atjungta,
    prisijungti nebegalima (ir per prisijungimo formą)
  • po trynimo jo skelbimai anonimui 404
  • asmens duomenys anonimizuoti (vardas, el. paštas, telefonai, adresas,
    skelbimo kontaktai), žinutės kitam dalyviui išliko
  • laiškas „Jūsų paskyra ištrinta" išsiųstas, nors laiškai išjungti
  • „Atsisiųsti mano duomenis" → JSON su TO naudotojo profiliu,
    skelbimais ir žinutėmis (be svetimų skelbimų)
  • svetimos paskyros ištrinti negalima (POST su kito id trina tik save;
    neprisijungęs → prisijungimas)

Paleidimas (TIK su laikina sqlite baze, NE prieš produkcijos DB):
    PATIKRA_DB=<laikinas failas> python docs/paskyros_trynimo_test.py
"""
import os
import sys

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sqlite_settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'patikra'))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

import json                                          # noqa: E402
import re                                            # noqa: E402
from decimal import Decimal                          # noqa: E402

from django.conf import settings                     # noqa: E402
from django.contrib.auth import get_user_model       # noqa: E402
from django.core import mail                         # noqa: E402
from django.test import Client, override_settings    # noqa: E402
from django.test.utils import setup_test_environment  # noqa: E402

from apps.accounts.models import Profile             # noqa: E402
from apps.conversations.models import Conversation, Message  # noqa: E402
from apps.listings.models import Listing, VehicleType  # noqa: E402

SLAPTAZODIS = 'Patikra-Trynimas-123'
TRINTI = '/accounts/settings/delete-account/'
DUOMENYS = '/accounts/settings/mano-duomenys/'
gerai = blogai = 0


def tikrink(salyga, tekstas, papildomai=''):
    global gerai, blogai
    if salyga:
        gerai += 1
        print(f'  OK   {tekstas}')
    else:
        blogai += 1
        print(f'  BLOGAI {tekstas}' + (f'\n         {papildomai}' if papildomai else ''))


def naujas(vardas):
    """Šviežias testinis naudotojas su profiliu ir aktyviu skelbimu."""
    U = get_user_model()
    el = f'{vardas}@trynimo-patikra.lt'
    U.objects.filter(email=el).delete()
    u = U.objects.create_user(username=vardas, email=el, password=SLAPTAZODIS,
                              first_name='Jonas', last_name='Testauskas')
    Profile.objects.filter(user=u).update(
        phone_number='+37061111111', phone_number_secondary='+37062222222',
        street='Laisvės al.', house_number='7', city='Kaunas', bio='Apie mane',
        language='lt', email_messages=False, marketing_emails=False,
        email_notifications=False, email_apie_skelbimus_isjungta=True)
    vt, _ = VehicleType.objects.get_or_create(slug='parts', defaults={'name': 'Parts'})
    l = Listing.objects.create(seller=u, vehicle_type=vt, title=f'Trynimo patikra {vardas}',
                               status='active', price=Decimal('100'), city='Kaunas',
                               country='LT', year=2020, mileage=0,
                               contact_phone='+37063333333', contact_email=el,
                               address='Laisvės al. 7')
    return U.objects.get(pk=u.pk), l


def klientas(u=None):
    c = Client()
    c.cookies[settings.LANGUAGE_COOKIE_NAME] = 'lt'
    if u is not None:
        c.force_login(u)
    return c


def tekstas(a):
    return a.content.decode('utf-8', 'replace')


def nepaliesta(u):
    x = get_user_model().objects.get(pk=u.pk)
    return (x.is_active and x.email == u.email and x.check_password(SLAPTAZODIS)
            and Listing.objects.filter(seller=u, status='active').exists())


@override_settings(LANGUAGE_CODE='lt', PASTAS_FONE=False,
                   EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
def main():
    setup_test_environment()
    u, l = naujas('trynimas_a')
    kitas, kito_l = naujas('trynimas_b')

    print('\n— Modalas nustatymuose')
    h = tekstas(klientas(u).get('/accounts/settings/', follow=True))
    forma = re.search(r'<form[^>]*data-trynimo-forma.*?</form>', h, re.S)
    f = forma.group(0) if forma else ''
    tikrink(re.search(r'<input type="password" name="password"[^>]*required', f) is not None,
            'yra <input type="password" name="password" required>')
    tikrink(re.search(r'<input type="text" name="patvirtinimas"[^>]*required', f) is not None,
            'yra <input type="text" name="patvirtinimas" required>')
    tikrink('type="hidden" name="password"' not in h, 'nėra paslėpto tuščio password')
    tikrink('Dabartinis slaptažodis' in f and 'Įrašykite DELETE' in f,
            'etiketės „Dabartinis slaptažodis", „Įrašykite DELETE"')
    tikrink(re.search(r'id="confirmDelete" disabled', f) is not None, '„Ištrinti" iš pradžių neaktyvus')
    tikrink('data-mano-duomenys' in h and 'Atsisiųsti mano duomenis' in h,
            'šalia — „Atsisiųsti mano duomenis"')

    print('\n— Neteisingas slaptažodis')
    c = klientas(u)
    a = c.post(TRINTI, {'password': 'neteisingas', 'patvirtinimas': 'DELETE'}, follow=True)
    tikrink(a.status_code == 200 and 'Neteisingas slaptažodis' in tekstas(a),
            f'rodoma „Neteisingas slaptažodis" ({a.status_code})')
    tikrink(nepaliesta(u), 'paskyra ir skelbimas NEPALIESTI')

    print('\n— Be „DELETE"')
    a = c.post(TRINTI, {'password': SLAPTAZODIS, 'patvirtinimas': 'delete'}, follow=True)
    tikrink('Įrašykite DELETE' in tekstas(a), 'rodoma klaida „Įrašykite DELETE…"')
    a = c.post(TRINTI, {'password': SLAPTAZODIS}, follow=True)
    tikrink('Įrašykite DELETE' in tekstas(a), 'be lauko — irgi klaida')
    tikrink(nepaliesta(u), 'paskyra NEPALIESTA')
    a = c.get(TRINTI, follow=True)
    tikrink(a.status_code == 200 and nepaliesta(u), f'GET → nustatymai, ne 500 ({a.status_code})')

    print('\n— Atsisiųsti mano duomenis')
    Conversation.objects.filter(participants=u).delete()
    conv = Conversation.objects.create(listing=kito_l)
    conv.participants.add(u, kitas)
    Message.objects.create(conversation=conv, sender=u, content='Ar dar parduodate?')
    Message.objects.create(conversation=conv, sender=kitas, content='Taip, parduodu.')
    a = c.get(DUOMENYS)
    tikrink(a.status_code == 200 and a['Content-Type'].startswith('application/json')
            and 'attachment' in a.get('Content-Disposition', ''),
            f'200, application/json, atsisiuntimas ({a.status_code}, {a.get("Content-Type")})')
    try:
        d = json.loads(a.content)
    except ValueError:
        d = {}
    tikrink(d.get('naudotojas', {}).get('email') == u.email
            and d.get('profilis', {}).get('phone_number') == '+37061111111',
            'JSON — to naudotojo el. paštas ir telefonas')
    ids = [x['id'] for x in d.get('skelbimai', {}).get('Listing', [])]
    tikrink(l.pk in ids and kito_l.pk not in ids, f'JSON — jo skelbimai, be svetimų ({ids})')
    zin = [z['tekstas'] for p in d.get('pokalbiai', []) for z in p['zinutes']]
    tikrink('Ar dar parduodate?' in zin and 'Taip, parduodu.' in zin, 'JSON — žinutės')
    tikrink(klientas().get(DUOMENYS).status_code == 302, 'neprisijungus → peradresavimas, ne duomenys')

    print('\n— Svetimos paskyros ištrinti negalima')
    a = klientas().post(TRINTI, {'password': SLAPTAZODIS, 'patvirtinimas': 'DELETE'})
    tikrink(a.status_code == 302 and '/login' in a['Location'] and nepaliesta(u),
            'neprisijungęs POST → prisijungimas, niekas nepaliesta')
    a = klientas(kitas).post(TRINTI, {'password': SLAPTAZODIS, 'patvirtinimas': 'DELETE',
                                      'user_id': u.pk, 'pk': u.pk, 'id': u.pk}, follow=True)
    tikrink(nepaliesta(u), 'POST su kito naudotojo id — svetima paskyra NEPALIESTA')
    tikrink(not get_user_model().objects.get(pk=kitas.pk).is_active,
            'ištrinta tik paties prisijungusiojo (kito) paskyra')

    print('\n— Teisingas slaptažodis + DELETE')
    mail.outbox = []
    sena_el = u.email
    a = c.post(TRINTI, {'password': SLAPTAZODIS, 'patvirtinimas': 'DELETE'}, follow=True)
    tikrink('Paskyra ištrinta' in tekstas(a) and a.redirect_chain and a.redirect_chain[0][0] == '/',
            f'„Paskyra ištrinta", į pradinį ({a.redirect_chain[:1]})')
    tikrink('_auth_user_id' not in c.session, 'atjungta')
    x = get_user_model().objects.get(pk=u.pk)
    tikrink(not x.is_active and not x.has_usable_password(), 'is_active=False, slaptažodis nenaudojamas')
    tikrink(not Client().login(username=x.username, password=SLAPTAZODIS)
            and not Client().login(username='trynimas_a', password=SLAPTAZODIS),
            'prisijungti nebegalima')
    a = klientas().post('/accounts/login/', {'email': sena_el, 'password': SLAPTAZODIS}, follow=True)
    tikrink('_auth_user_id' not in a.client.session, 'prisijungimo forma su senu el. paštu — neprisileidžia')

    print('\n— Asmens duomenys')
    p = Profile.objects.get(user=x)
    tikrink(x.first_name == '' and x.last_name == '' and sena_el not in x.email
            and x.email.endswith('@istrinta.invalid') and x.username.startswith('istrintas-'),
            f'vardas, pavardė, el. paštas anonimizuoti ({x.username}, {x.email})')
    tikrink(not any([p.phone_number, p.phone_number_secondary, p.street, p.house_number,
                     p.city, p.bio, p.profile_picture]),
            'telefonai, adresas, aprašymas, nuotrauka išvalyti')
    tikrink(not get_user_model().objects.filter(email=sena_el).exists(), 'senas el. paštas DB nebeegzistuoja')
    l.refresh_from_db()
    tikrink(l.status == 'archived' and not l.contact_phone and not l.contact_email and not l.address,
            f'skelbimas archived, kontaktai išvalyti ({l.status})')
    tikrink(Message.objects.filter(conversation=conv).count() == 2,
            'žinutės kitam pokalbio dalyviui išliko')

    print('\n— Skelbimai anonimui')
    a = klientas().get(f'/{l.pk}/', follow=True)
    tikrink(a.status_code == 404, f'GET /{l.pk}/ anonimui → 404 ({a.status_code})')
    a = klientas().get(f'/accounts/seller/{x.pk}/', follow=True)
    tikrink(a.status_code == 404, f'pardavėjo puslapis /accounts/seller/{x.pk}/ → 404 ({a.status_code})')

    print('\n— Laiškas „Jūsų paskyra ištrinta"')
    laiskai = [m for m in mail.outbox if sena_el in m.to]
    tikrink(len(laiskai) == 1 and 'Jūsų paskyra ištrinta' in laiskai[0].subject,
            f'1 laiškas į {sena_el}, nors visi laiškai buvo išjungti',
            str([(m.to, m.subject) for m in mail.outbox]))

    print(f'\n════ {gerai} gerai / {blogai} blogai ════')
    return 1 if blogai else 0


if __name__ == '__main__':
    sys.exit(main())
