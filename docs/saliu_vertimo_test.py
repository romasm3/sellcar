# -*- coding: utf-8 -*-
"""
ŠALIŲ PAVADINIMAI — IŠVERSTI TEN, KUR TEKSTAS SKIRTAS ŽMOGUI.

Klaida: /accounts/settings/ LT kalba rodė „Lithuania". Profile.country
istoriškai laisvas tekstas (numatytoji „Lithuania"), o šablonas jį rodė
tiesiogiai. Dabar — filtras salies_vardas (apps/listings/salys.vardas_is)
atpažįsta ir kodą, ir pavadinimą ir rodo sąsajos kalba; redaguojant —
sąrašas su kodais (tas pats kaip skelbimuose).

Pagal docs/taisykles.md kortelės vietos eilutė ir šalies juosta /
šalies laukas paieškoje lieka ANGLIŠKI (tarptautinis sąrašas) — jų šis
testas netikrina.

Tikrinam (tikras HTML):
  • LT /accounts/settings/ → yra „Lietuva", nėra „Lithuania"
  • EN /accounts/settings/ → yra „Lithuania"
  • išsaugojus kitą šalį (sąrašas, kodas) → rodoma „Vokietija"
  • skelbimo puslapyje LT → „Lietuva"
  • pardavėjo profilyje LT → „Lietuva", ne „Lithuania"
  • kūrimo formos šalies sąraše LT → „Lietuva"

Paleidimas (TIK su laikina sqlite baze, NE prieš produkcijos DB):
    PATIKRA_DB=<laikinas failas> python docs/saliu_vertimo_test.py
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
from django.test import Client, override_settings    # noqa: E402
from django.test.utils import setup_test_environment  # noqa: E402

import formu_seed                                    # noqa: E402
from apps.accounts.models import Profile             # noqa: E402
from apps.listings.models import Listing             # noqa: E402

gerai = blogai = 0


def tikrink(salyga, tekstas, papildomai=''):
    global gerai, blogai
    if salyga:
        gerai += 1
        print(f'  OK   {tekstas}')
    else:
        blogai += 1
        print(f'  BLOGAI {tekstas}' + (f'\n         {papildomai}' if papildomai else ''))


def klientas(u, kalba):
    c = Client()
    c.cookies[settings.LANGUAGE_COOKIE_NAME] = kalba
    c.force_login(u)
    Profile.objects.filter(user=u).update(language=kalba)
    return c


def tekstas(a):
    h = a.content.decode('utf-8', 'replace')
    return re.sub(r'<script.*?</script>|<!--.*?-->', '', h, flags=re.S)


def kontekstas(t, zodis):
    m = re.search(r'.{60}' + re.escape(zodis) + r'.{20}', t, re.S)
    return re.sub(r'\s+', ' ', m.group(0)) if m else ''


@override_settings(LANGUAGE_CODE='lt')
def main():
    setup_test_environment()
    u = formu_seed.vartotojas()
    Profile.objects.filter(user=u).update(country='Lithuania', city='Kaunas', street='Laisvės al.')

    print('\n— /accounts/settings/')
    t = tekstas(klientas(u, 'lt').get('/accounts/settings/', follow=True))
    tikrink('Lietuva' in t, 'LT: yra „Lietuva"')
    tikrink('Lithuania' not in t, 'LT: nėra „Lithuania"', kontekstas(t, 'Lithuania'))
    t = tekstas(klientas(u, 'en').get('/en/accounts/settings/', follow=True))
    tikrink('Lithuania' in t, 'EN: yra „Lithuania"')

    print('\n— Šalies keitimas nustatymuose (sąrašas, kodas)')
    c = klientas(u, 'lt')
    t = tekstas(c.get('/accounts/settings/', follow=True))
    tikrink(re.search(r'<select name="country"', t) and re.search(r'<option value="LT"\s+selected', t),
            'redaguojant — šalių sąrašas, pažymėta LT (iš „Lithuania")')
    c.post('/accounts/settings/inline-update/', {'country': 'DE'})
    t = tekstas(c.get('/accounts/settings/', follow=True))
    tikrink(Profile.objects.get(user=u).country == 'DE' and 'Vokietija' in t,
            'išsaugota DE → rodoma „Vokietija"')
    Profile.objects.filter(user=u).update(country='Lithuania')

    print('\n— Skelbimo puslapis')
    l = Listing.objects.filter(status='active', country='LT').first()
    if l is None:
        l = Listing.objects.filter(status='active').first()
        Listing.objects.filter(pk=l.pk).update(country='LT')
    t = tekstas(klientas(u, 'lt').get(f'/{l.pk}/', follow=True))
    tikrink('Lietuva' in t, f'LT /{l.pk}/: yra „Lietuva"')

    print('\n— Pardavėjo profilis')
    t = tekstas(klientas(u, 'lt').get(f'/accounts/seller/{u.pk}/', follow=True))
    tikrink('Lietuva' in t and 'Lithuania' not in t, 'LT: „Lietuva", ne „Lithuania"',
            kontekstas(t, 'Lithuania'))

    print('\n— Kūrimo formos šalies sąrašas')
    t = tekstas(klientas(u, 'lt').get('/create/parts/form/?sub=lighting-front-lights-headlight',
                                      follow=True))
    tikrink(re.search(r'<option value="LT"[^>]*>\s*Lietuva\s*<', t) is not None,
            'LT: <option value="LT">Lietuva')

    Profile.objects.filter(user=u).update(language='lt')
    print(f'\n════ {gerai} gerai / {blogai} blogai ════')
    return 1 if blogai else 0


if __name__ == '__main__':
    sys.exit(main())
