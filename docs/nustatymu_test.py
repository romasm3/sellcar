# -*- coding: utf-8 -*-
"""
NUSTATYMAI /accounts/settings/ — LAIŠKŲ APIE SKELBIMUS VALDYMAS.

Tikrinam (tikras HTML, tikri laiškai locmem dėžutėje):
  • kiekviena varnelė išsisaugo ir matosi perkrovus
  • VISOS varnelės: uždėta = gaunu. Nuėmus pagrindinę „Gauti laiškus apie
    mano skelbimus" — galima_siusti() = False kiekvienam skelbimų tipui;
    atskiros pilkos (ne disabled); uždėjus — grįžta ankstesnės reikšmės
  • nuėmus atskirą varnelę — tas tipas nesiunčiamas, kiti siunčiami
    (ir per send_scenario — tikras laiškas)
  • slaptažodžio atkūrimo laiškas siunčiamas net viską išjungus
  • ne sisteminiame laiške — „Atsisakyti šių pranešimų" nuoroda; ji su geru
    tokenu veikia be prisijungimo (išjungia tik tą tipą), su blogu → 403
  • juodraščio priminime („Activate my listing") — taip pat
  • prisijungus atsisakymas išlieka (User post_save nebeperrašo profilio)
  • GET /dashboard/ → 302 į /dashboard/announcements/
  • LT puslapyje nėra „Account Settings" ir „SMS"

Paleidimas (TIK su laikina sqlite baze, NE prieš produkcijos DB):
    PATIKRA_DB=<laikinas failas> python docs/nustatymu_test.py
(prieš tai: PYTHONPATH=docs/patikra python manage.py migrate --settings=sqlite_settings)
"""
import os
import sys

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sqlite_settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'patikra'))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

import re                                            # noqa: E402

from django.conf import settings                     # noqa: E402
from django.core import mail                         # noqa: E402
from django.test import Client, override_settings    # noqa: E402
from django.test.utils import setup_test_environment  # noqa: E402

import formu_seed                                    # noqa: E402
from apps.accounts import notifications as N         # noqa: E402
from apps.accounts.models import Profile             # noqa: E402

VARNELES = ['email_apie_skelbimus_isjungta', 'email_aktyvavimo_priminimai', 'email_galiojimas',
            'email_susidomejimas', 'email_notifications', 'email_messages', 'marketing_emails']
SKELBIMU = ['aktyvavimas', 'galiojimas', 'susidomejimas', 'skelbimai']

gerai = blogai = 0


def tikrink(salyga, tekstas, papildomai=''):
    global gerai, blogai
    if salyga:
        gerai += 1
        print(f'  OK   {tekstas}')
    else:
        blogai += 1
        print(f'  BLOGAI {tekstas}' + (f'\n         {papildomai}' if papildomai else ''))


def puslapis(c):
    return c.get('/accounts/settings/', follow=True).content.decode('utf-8', 'replace')


def pazymeta(h, vardas):
    m = re.search(rf'<input[^>]*name="{vardas}"[^>]*>', h)
    return bool(m) and ' checked' in m.group(0)


def issaugok(c, **reiksmes):
    """Formos POST. email_apie_skelbimus_isjungta=True — pagrindinė
    „Gauti laiškus…" NUIMTA (jos lauko POST'e nėra), kitaip — uždėta."""
    isjungta = reiksmes.pop('email_apie_skelbimus_isjungta', False)
    duom = {k: 'on' for k, v in reiksmes.items() if v}
    if not isjungta:
        duom['gauti_laiskus_apie_skelbimus'] = 'on'
    return c.post('/accounts/settings/notifications/', duom)


def profilis(u):
    return Profile.objects.get(user=u)


@override_settings(LANGUAGE_CODE='lt',
                   EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
def main():
    setup_test_environment()
    u = formu_seed.vartotojas()
    p, _ = Profile.objects.get_or_create(user=u)
    p.language = 'lt'
    p.save(update_fields=['language'])
    c = Client()
    c.cookies[settings.LANGUAGE_COOKIE_NAME] = 'lt'
    c.force_login(u)

    print('\n— Puslapis LT')
    h = puslapis(c)
    tikrink('Account Settings' not in h, 'nėra „Account Settings"')
    tikrink('Paskyros nustatymai' in h and 'Gauti laiškus apie mano skelbimus' in h
            and 'Nesiųsti man' not in h,
            'yra „Paskyros nustatymai" ir teigiama pagrindinė „Gauti laiškus apie mano skelbimus"')
    tikrink('sms_notifications' not in h and 'SMS' not in h, 'SMS varnelės nėra')
    tikrink('Uždėta varnelė — laiškus gausite.' in h, 'po antrašte: „Uždėta varnelė — laiškus gausite."')
    varneliu_tekstai = re.findall(r'<label class="nst-varnele[^"]*">\s*<span[^>]*>([^<]+)</span>', h)
    tikrink(varneliu_tekstai and not [t for t in varneliu_tekstai if t.strip().startswith('Nesiųsti')],
            f'nėra varnelės, prasidedančios „Nesiųsti" ({len(varneliu_tekstai)} varnelių)',
            f'{varneliu_tekstai}')
    for zodis in ('Profile Picture', 'Login Settings', 'User Data', 'Email Notifications',
                  'Privacy Settings', 'Dealer Account', 'Danger Zone', 'Save Preferences',
                  'Save Privacy Settings', 'Delete Account'):
        tikrink(zodis not in re.sub(r'<script.*?</script>', '', h, flags=re.S),
                f'nėra „{zodis}"')

    print('\n— Kiekviena varnelė išsisaugo ir matosi perkrovus')
    for vardas in VARNELES:
        for reiksme in (True, False):
            visos = {v: True for v in VARNELES if v != 'email_apie_skelbimus_isjungta'}
            visos['email_apie_skelbimus_isjungta'] = False
            visos[vardas] = reiksme
            issaugok(c, **visos)
            h = puslapis(c)
            db = getattr(profilis(u), vardas)
            if vardas == 'email_apie_skelbimus_isjungta':
                # pagrindinė rodoma apversta: „Gauti…" uždėta, kai NEišjungta
                ok = db == reiksme and pazymeta(h, 'gauti_laiskus_apie_skelbimus') == (not reiksme)
                pz = pazymeta(h, 'gauti_laiskus_apie_skelbimus')
            else:
                ok = db == reiksme and pazymeta(h, vardas) == reiksme
                pz = pazymeta(h, vardas)
            tikrink(ok, f'{vardas} = {reiksme}: DB {db}, puslapyje {pz}')

    print('\n— Pagrindinė varnelė')
    issaugok(c, **{v: True for v in VARNELES if v != 'email_apie_skelbimus_isjungta'})
    issaugok(c, email_apie_skelbimus_isjungta=True, email_notifications=True,
             email_messages=True, marketing_emails=True)
    u.refresh_from_db()
    for tipas in SKELBIMU:
        tikrink(not N.galima_siusti(u, tipas), f'galima_siusti({tipas}) = False')
    tikrink(N.galima_siusti(u, 'zinutes') and N.galima_siusti(u, 'paieskos'),
            'kiti (žinutės, paieškos) — siunčiami')
    pr = profilis(u)
    tikrink(pr.email_aktyvavimo_priminimai and pr.email_galiojimas and pr.email_susidomejimas,
            'atskirų varnelių DB reikšmės išliko (nuėmus pagrindinę — grįš)')
    h = puslapis(c)
    for v in ('email_aktyvavimo_priminimai', 'email_galiojimas', 'email_susidomejimas'):
        zyma = re.search(rf'<input[^>]*name="{v}"[^>]*>', h).group(0)
        tikrink(' disabled' not in zyma and pazymeta(h, v),
                f'   {v}: NE disabled ir pažymėta (reikšmė siunčiama su forma)')
    tikrink('nst-grupe is-off' in h, '   grupė pilka (is-off), kol pagrindinė uždėta')

    print('\n— Naršyklės POST: pagrindinė „Gauti…" nuimta, be trijų atskirų')
    issaugok(c, email_aktyvavimo_priminimai=True, email_galiojimas=True, email_susidomejimas=True,
             email_notifications=True, email_messages=True, marketing_emails=True)
    c.post('/accounts/settings/notifications/', {'email_notifications': 'on'})
    pr = profilis(u)
    tikrink(pr.email_apie_skelbimus_isjungta and pr.email_aktyvavimo_priminimai
            and pr.email_galiojimas and pr.email_susidomejimas,
            'POST be „Gauti…" ir be trijų → išjungta, trys atskiros DB lieka True')
    c.post('/accounts/settings/notifications/', {'gauti_laiskus_apie_skelbimus': 'on',
                                                 'email_aktyvavimo_priminimai': 'on',
                                                 'email_galiojimas': 'on',
                                                 'email_susidomejimas': 'on'})
    pr = profilis(u)
    tikrink(not pr.email_apie_skelbimus_isjungta and pr.email_aktyvavimo_priminimai
            and pr.email_galiojimas and pr.email_susidomejimas,
            'POST su „Gauti…" ir trimis „on" → gaunama, visos trys True')
    h = puslapis(c)
    tikrink(pazymeta(h, 'gauti_laiskus_apie_skelbimus') and pazymeta(h, 'email_galiojimas')
            and 'nst-grupe is-off' not in h,
            'gaunant: „Gauti…" pažymėta, grupė aktyvi (uždėta = gaunu visur)')
    issaugok(c, email_aktyvavimo_priminimai=True, email_galiojimas=True, email_susidomejimas=True,
             email_notifications=True, email_messages=True, marketing_emails=True)
    u.refresh_from_db()
    tikrink(all(N.galima_siusti(u, t) for t in SKELBIMU), 'nuėmus pagrindinę — vėl siunčiama')

    print('\n— Atskira varnelė')
    issaugok(c, email_aktyvavimo_priminimai=True, email_galiojimas=False, email_susidomejimas=True,
             email_notifications=True, email_messages=True, marketing_emails=True)
    u.refresh_from_db()
    tikrink(not N.galima_siusti(u, 'galiojimas'), 'galiojimas — nesiunčiamas')
    tikrink(N.galima_siusti(u, 'aktyvavimas') and N.galima_siusti(u, 'susidomejimas'),
            'aktyvavimas ir susidomėjimas — siunčiami')
    from apps.listings.emails.sender import send_scenario
    mail.outbox.clear()
    send_scenario('listing_expiring_soon', to_email=u.email, context={})   # be to_user!
    tikrink(len(mail.outbox) == 0, 'send_scenario(listing_expiring_soon) — neišsiųsta (to_user randamas pagal paštą)')
    send_scenario('listing_first_views', to_email=u.email, context={})
    tikrink(len(mail.outbox) == 1, 'send_scenario(listing_first_views) — išsiųsta')
    laiskas = mail.outbox[-1] if mail.outbox else None
    nuoroda = re.search(r'(/accounts/atsisakyti/\?t=\S+)', laiskas.body) if laiskas else None
    tikrink(laiskas is not None and 'Atsisakyti šių pranešimų' in laiskas.body and nuoroda,
            '   laiško apačioje „Atsisakyti šių pranešimų" su nuoroda')

    print('\n— Slaptažodžio atkūrimas — visada')
    issaugok(c, email_apie_skelbimus_isjungta=True)      # viskas išjungta
    mail.outbox.clear()
    anonimas = Client()
    anonimas.post('/accounts/password-reset/', {'email': u.email})
    tikrink(len(mail.outbox) == 1, f'slaptažodžio atkūrimo laiškas išsiųstas ({len(mail.outbox)})')
    tikrink(mail.outbox and 'atsisakyti' not in mail.outbox[0].body,
            '   be atsisakymo nuorodos (sisteminis)')

    print('\n— Atsisakymo nuoroda be prisijungimo')
    issaugok(c, email_aktyvavimo_priminimai=True, email_galiojimas=True, email_susidomejimas=True,
             email_notifications=True, email_messages=True, marketing_emails=True)
    a = anonimas.get(nuoroda.group(1) if nuoroda else '/accounts/atsisakyti/?t=x')
    pr = profilis(u)
    tikrink(a.status_code == 200 and not pr.email_susidomejimas,
            f'geras tokenas (neprisijungus) → 200, susidomėjimas išjungtas ({a.status_code})')
    tikrink(pr.email_galiojimas and pr.email_aktyvavimo_priminimai and not pr.email_apie_skelbimus_isjungta,
            '   kiti nepaliesti')
    # Prisijungimas (last_login) nebeperrašo profilio pasenusia kopija:
    # u.profile atmintyje dar su email_susidomejimas=True
    tikrink(u.profile.email_susidomejimas is True, '   (atmintyje — sena profilio kopija)')
    Client().force_login(u)
    tikrink(not profilis(u).email_susidomejimas,
            'prisijungus atsisakymas išlieka (signalas nebeperrašo profilio)')
    a = anonimas.get('/accounts/atsisakyti/', {'t': 'blogas:tokenas'})
    tikrink(a.status_code == 403, f'blogas tokenas → 403 ({a.status_code})')
    pries = (profilis(u).email_galiojimas)
    kito = N.atsisakymo_tokenas(u, 'galiojimas')[:-3] + 'abc'
    a = anonimas.get('/accounts/atsisakyti/', {'t': kito})
    tikrink(a.status_code == 403 and profilis(u).email_galiojimas == pries,
            'suklastotas tokenas → 403, niekas nepakito')

    print('\n— Juodraščio priminimas („Activate my listing")')
    from apps.listings.management.commands.send_draft_reminders import priminimo_laiskas
    from apps.listings.models import Listing
    juod = Listing.objects.filter(seller=u).first()
    if juod:
        _tema, tekstas, html = priminimo_laiskas(juod, 'draft_reminder_first', site_url='')
        tikrink('Atsisakyti šių pranešimų' in tekstas and 'Atsisakyti šių pranešimų' in html,
                'priminime — „Atsisakyti šių pranešimų" (tekste ir HTML)')

    print('\n— /dashboard/')
    a = c.get('/dashboard/')
    tikrink(a.status_code == 302 and a.get('Location') == '/dashboard/announcements/',
            f'GET /dashboard/ → 302 /dashboard/announcements/ ({a.status_code} {a.get("Location")})')

    issaugok(c, **{v: True for v in VARNELES if v not in ('email_apie_skelbimus_isjungta',
                                                          'marketing_emails')})
    print(f'\n════ {gerai} gerai / {blogai} blogai ════')
    return 1 if blogai else 0


if __name__ == '__main__':
    sys.exit(main())
