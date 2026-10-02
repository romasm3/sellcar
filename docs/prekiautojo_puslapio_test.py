# -*- coding: utf-8 -*-
"""
„TAPKITE PREKIAUTOJU" — /accounts/become-dealer/ TIKRAS PUSLAPIS.

Klaida: nustatymuose „Tapkite prekiautoju → Sužinoti daugiau" vedė į
/accounts/become-dealer/, o tas, kol mokėjimai išjungti, tyliai permesdavo
atgal į /accounts/settings/.

Tikrinam (tikras HTML, mokėjimai išjungti — kaip produkcijoje):
  • neprisijungęs GET → 200, ne peradresavimas; yra nauda, kaina (100 €),
    mygtukas „Noriu tapti prekiautoju" (veda į prisijungimą)
  • prisijungęs paprastas naudotojas GET → 200, NE į nustatymus; forma
  • POST → laiškas administratoriui (ADMIN_EMAIL) su įmone ir el. paštu;
    profilyje dealer_status='pending'; puslapis — „Susisieksime per 1 d. d."
  • pakartotinis POST → antro laiško nėra
  • prisijungęs prekiautojas → plano būsena (aktyvus, galioja iki,
    skelbimai N / 30), NE pardavimo tekstas ir ne mygtukas
  • prekiautojas, kurio planas baigėsi → „Nebegalioja"
  • administracijos prekiautojų sąraše — „Užklausa"

Paleidimas (TIK su laikina sqlite baze, NE prieš produkcijos DB):
    PATIKRA_DB=<laikinas failas> python docs/prekiautojo_puslapio_test.py
"""
import os
import sys

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sqlite_settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'patikra'))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

import re                                            # noqa: E402
from datetime import timedelta                       # noqa: E402

from django.conf import settings                     # noqa: E402
from django.contrib.auth import get_user_model       # noqa: E402
from django.core import mail                         # noqa: E402
from django.test import Client, override_settings    # noqa: E402
from django.test.utils import setup_test_environment  # noqa: E402
from django.utils import timezone                    # noqa: E402

import formu_seed                                    # noqa: E402
from apps.accounts.models import Profile             # noqa: E402
from apps.listings.email_settings import ADMIN_EMAIL  # noqa: E402

URL = '/accounts/become-dealer/'
gerai = blogai = 0


def tikrink(salyga, tekstas, papildomai=''):
    global gerai, blogai
    if salyga:
        gerai += 1
        print(f'  OK   {tekstas}')
    else:
        blogai += 1
        print(f'  BLOGAI {tekstas}' + (f'\n         {papildomai}' if papildomai else ''))


def klientas(u=None):
    c = Client()
    c.cookies[settings.LANGUAGE_COOKIE_NAME] = 'lt'
    if u is not None:
        c.force_login(u)
    return c


def gauk(c):
    a = c.get(URL, follow=True)
    kelias = a.redirect_chain[-1][0] if a.redirect_chain else URL
    return a, kelias, a.content.decode('utf-8', 'replace')


def naudotojas(el_pastas, **profilis):
    U = get_user_model()
    u = U.objects.filter(email=el_pastas).first() or U.objects.create_user(
        username=el_pastas.split('@')[0], email=el_pastas, password='x-Patikra-123')
    laukai = dict(account_type='private', dealer_status='none', dealer_subscription_active=False,
                  dealer_subscription_expires=None, dealer_applied_at=None, dealer_company_name='',
                  dealer_phone='')
    laukai.update(profilis)
    Profile.objects.filter(user=u).update(**laukai)
    return u


@override_settings(LANGUAGE_CODE='lt', MOKEJIMAI_IJUNGTI=False, PAYMENTS_ENABLED=False,
                   PASTAS_FONE=False,
                   EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
def main():
    setup_test_environment()
    formu_seed.vartotojas()

    print('\n— Neprisijungęs')
    a, kelias, h = gauk(klientas())
    tikrink(a.status_code == 200 and not a.redirect_chain,
            f'GET {URL} → 200, be peradresavimo ({a.status_code}, {a.redirect_chain})')
    tikrink('data-prekiautojo-nauda' in h and 'Firminis puslapis' in h and 'Iki 30 aktyvių skelbimų' in h,
            'yra „Ką gauna prekiautojas": firminis puslapis, iki 30 skelbimų')
    tikrink('data-prekiautojo-kaina' in h and re.search(r'100\s*€', h) and 'Kaina apima' in h,
            'yra kaina 100 € ir „Kaina apima"')
    tikrink('Noriu tapti prekiautoju' in h and '/accounts/login/?next=' in h and 'data-prekiautojo-forma' not in h,
            'mygtukas „Noriu tapti prekiautoju" → prisijungimas')

    print('\n— Prisijungęs paprastas naudotojas')
    u = naudotojas('prekiautojo.patikra@autoleft.lt')
    c = klientas(u)
    a, kelias, h = gauk(c)
    tikrink(a.status_code == 200 and '/accounts/settings/' not in kelias,
            f'GET → 200, NE peradresavimas į nustatymus (galutinis: {kelias})')
    tikrink('data-prekiautojo-forma' in h and 'Noriu tapti prekiautoju' in h and 'data-plano-busena' not in h,
            'pardavimo puslapis su forma, be plano būsenos')

    print('\n— Užklausa (POST)')
    mail.outbox = []
    a = c.post(URL, {'imone': 'UAB Patikros Autocentras', 'telefonas': '+37060000000',
                     'komentaras': 'Turime 25 automobilius'}, follow=True)
    h = a.content.decode('utf-8', 'replace')
    pr = Profile.objects.get(user=u)
    tikrink(pr.dealer_status == 'pending' and pr.dealer_applied_at is not None,
            f'profilyje dealer_status=pending ({pr.dealer_status})')
    laiskai = [m for m in mail.outbox if ADMIN_EMAIL in m.to]
    tikrink(len(laiskai) == 1, f'1 laiškas administratoriui {ADMIN_EMAIL} (yra {len(laiskai)})',
            str([(m.to, m.subject) for m in mail.outbox]))
    if laiskai:
        tikrink('UAB Patikros Autocentras' in laiskai[0].body and u.email in laiskai[0].body
                and '+37060000000' in laiskai[0].body,
                'laiške — įmonė, el. paštas, telefonas')
    tikrink('Susisieksime per 1 d. d.' in h and 'data-plano-busena="laukia"' in h,
            'po POST — „Susisieksime per 1 d. d."')
    c.post(URL, {'imone': 'UAB Patikros Autocentras'})
    tikrink(len([m for m in mail.outbox if ADMIN_EMAIL in m.to]) == 1,
            'pakartotinis POST — antro laiško nėra')

    print('\n— Administracijos prekiautojų sąrašas')
    adm = get_user_model().objects.filter(is_superuser=True).first()
    if adm is None:
        adm = get_user_model().objects.create_superuser('patikra_admin', 'patikra.admin@autoleft.lt', 'x-Patikra-123')
    h = klientas(adm).get('/accounts/admin/dealers/', follow=True).content.decode('utf-8', 'replace')
    tikrink(u.email in h and 'Užklausa' in h, 'užklausą pateikęs matomas su žyma „Užklausa"')

    print('\n— Prekiautojas (aktyvus planas)')
    p = naudotojas('prekiautojas.patikra@autoleft.lt', account_type='dealer', dealer_status='approved',
                   dealer_subscription_active=True,
                   dealer_subscription_expires=timezone.now() + timedelta(days=12),
                   dealer_company_name='UAB Aktyvus Prekiautojas')
    a, kelias, h = gauk(klientas(p))
    tikrink(a.status_code == 200 and '/accounts/settings/' not in kelias, f'GET → 200 ({kelias})')
    tikrink('data-plano-busena="aktyvus"' in h and 'UAB Aktyvus Prekiautojas' in h,
            'rodoma plano būsena „aktyvus" su įmone')
    tikrink(re.search(r'data-skelbimu-riba>\s*\d+ / 30', h) is not None, 'skelbimai N / 30')
    galioja = (timezone.now() + timedelta(days=12)).strftime('%Y-%m-%d')
    tikrink(galioja in h, f'galioja iki {galioja}')
    tikrink('data-prekiautojo-nauda' not in h and 'Noriu tapti prekiautoju' not in h,
            'NĖRA pardavimo teksto ir mygtuko')

    print('\n— Prekiautojas (planas baigėsi)')
    Profile.objects.filter(user=p).update(dealer_subscription_active=False,
                                          dealer_subscription_expires=timezone.now() - timedelta(days=3))
    a, kelias, h = gauk(klientas(p))
    tikrink('data-plano-busena="baigesi"' in h and 'Nebegalioja' in h and 'Noriu tapti prekiautoju' not in h,
            'rodoma „Nebegalioja", ne pardavimo tekstas')

    print(f'\n════ {gerai} gerai / {blogai} blogai ════')
    return 1 if blogai else 0


if __name__ == '__main__':
    sys.exit(main())
