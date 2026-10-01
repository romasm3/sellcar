# -*- coding: utf-8 -*-
"""
„AKTYVUOTI" TIESIOG AKTYVUOJA (žmogaus sprendimas 2026-10-01).

    [Aktyvuoti] = POST /listings/<id>/activate/ (CSRF, tik savininkas) →
    aktyvus → atgal į /dashboard/announcements/ su „Skelbimas aktyvuotas"
    + nuoroda į /<id>/.
Vienintelis stabdys — nėra nuotraukos: tada NEaktyvuojam, o vedam į
redagavimą su „Įkelkite bent vieną nuotrauką ir išsaugokite – skelbimas
aktyvuosis"; įkėlus ir išsaugojus — aktyvuojasi pats. Jokio plano,
paketo, kainos ar apmokėjimo. Aktyviame — [Deaktyvuoti] [Redaguoti].

Tikrinam (tikras HTML ir DB):
  • juodraštis su 1 foto → POST activate → 302 į skydelį, žinutė su
    nuoroda; anoniminis GET /<id>/ → 200
  • juodraštis be kainos/miesto, bet su foto → vis tiek aktyvuojamas
  • juodraštis be foto → 302 į redagavimą, lieka juodraštis; žinutė yra,
    klaidų sąrašas NE tuščias
  • įkėlus foto ir išsaugojus redagavimą → aktyvus be antro paspaudimo
  • ne savininkas → 403/404, būsena nepakinta
  • GET activate ir GET select-plan būsenos nekeičia
  • aktyvaus skelbimo redagavimo išsaugojimas → lieka aktyvus (anonimui 200)
  • [Deaktyvuoti] → nebeviešas; skydelyje aktyviam yra [Deaktyvuoti]
  • niekur nėra plano / apmokėjimo žingsnio

Paleidimas (TIK su laikina sqlite baze, NE prieš produkcijos DB):
    PATIKRA_DB=<laikinas failas> python docs/aktyvavimo_test.py
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import daliu_redagavimo_pavadinimo_test as forma_testas  # noqa: E402  (django.setup())

import io                                            # noqa: E402
import json                                          # noqa: E402
import re                                            # noqa: E402
from decimal import Decimal                          # noqa: E402

from django.conf import settings                     # noqa: E402
from django.contrib.auth import get_user_model       # noqa: E402
from django.core.files.base import ContentFile       # noqa: E402
from django.test import Client, override_settings    # noqa: E402
from django.test.utils import setup_test_environment  # noqa: E402
from PIL import Image                                # noqa: E402

import formu_seed                                    # noqa: E402
from apps.listings.models import Listing, ListingImage  # noqa: E402

MEDIA = tempfile.mkdtemp(prefix='aktyvavimo_media_')
DRAUDZIAMI = ('Mokėjimas', 'Paslaugų pasirinkimas', 'Skelbimo trukmė', 'Pasirinkite planą',
              'Apmokėti', 'Stripe', 'Continue to Plan Selection')

gerai = blogai = 0


def tikrink(salyga, tekstas, papildomai=''):
    global gerai, blogai
    if salyga:
        gerai += 1
        print(f'  OK   {tekstas}')
    else:
        blogai += 1
        print(f'  BLOGAI {tekstas}' + (f'\n         {papildomai}' if papildomai else ''))


def nuotrauka(l):
    b = io.BytesIO()
    Image.new('RGB', (40, 30), 'gray').save(b, 'JPEG')
    img = ListingImage(listing=l, is_main=True)
    img.image.save('aktyvavimas.jpg', ContentFile(b.getvalue()), save=False)
    img.save()


def juodrastis(u, pav, foto=True, kaina='900', miestas='Kaunas'):
    """Dalies juodraštis (turi part_category — kad veiktų redagavimo forma)."""
    l = forma_testas.pasejk(u)                       # bazinis dalies skelbimas
    l.pk = None
    l.id = None
    l.title, l.status = pav, 'draft'
    l.price, l.city = Decimal(kaina), miestas
    l.oem_code = ''
    l.save()
    if foto:
        nuotrauka(l)
    l.refresh_from_db()
    return l


def html(a):
    return a.content.decode('utf-8', 'replace')


def be_mokejimo(h, kur):
    t = re.sub(r'<script.*?</script>|<!--.*?-->', '', h, flags=re.S)
    rasta = [z for z in DRAUDZIAMI if z in t]
    tikrink(not rasta, f'{kur}: jokio plano / apmokėjimo', f'rasta {rasta}')


@override_settings(LANGUAGE_CODE='lt', MOKEJIMAI_IJUNGTI=False, PAYMENTS_ENABLED=False)
def main():
    setup_test_environment()
    u = formu_seed.vartotojas()
    c = Client()
    c.cookies[settings.LANGUAGE_COOKIE_NAME] = 'lt'
    c.force_login(u)
    anonimas = Client()

    print('\n— Juodraštis su 1 foto → POST /listings/<id>/activate/')
    l = juodrastis(u, 'Patikra aktyvavimas su foto')
    tikrink(anonimas.get(f'/{l.pk}/').status_code == 404, 'prieš: anonimui 404 (juodraštis)')
    a = c.post(f'/listings/{l.pk}/activate/')
    tikrink(a.status_code == 302 and a.get('Location') == '/dashboard/announcements/',
            f'302 → /dashboard/announcements/ (gauta {a.status_code} {a.get("Location")})')
    l.refresh_from_db()
    tikrink(l.status == 'active', f'statusas active ({l.status})')
    h = html(c.get('/dashboard/announcements/'))
    tikrink('Skelbimas aktyvuotas' in h and f'href="/{l.pk}/"' in h,
            'žinutė „Skelbimas aktyvuotas" su nuoroda į /<id>/')
    tikrink(anonimas.get(f'/{l.pk}/').status_code == 200, 'anoniminis GET /<id>/ → 200')
    be_mokejimo(h, '   skydelis')

    print('\n— Juodraštis be kainos ir miesto, bet su foto → vis tiek aktyvuojamas')
    m = juodrastis(u, 'Patikra be kainos su foto', kaina='0', miestas='—')
    c.post(f'/listings/{m.pk}/activate/')
    m.refresh_from_db()
    tikrink(m.status == 'active', f'aktyvus be kainos/miesto ({m.status})')

    print('\n— Juodraštis be foto → redagavimas, lieka juodraštis')
    n = juodrastis(u, 'Patikra be foto', foto=False)
    a = c.post(f'/listings/{n.pk}/activate/', follow=True)
    galas = a.redirect_chain[-1][0] if a.redirect_chain else ''
    n.refresh_from_db()
    tikrink(a.redirect_chain and a.redirect_chain[0][0] == f'/{n.pk}/edit/',
            f'302 → /{n.pk}/edit/ (grandinė {[x[0] for x in a.redirect_chain]})')
    tikrink(n.status == 'draft', 'liko juodraštis')
    h = html(a)
    tikrink('Įkelkite bent vieną nuotrauką ir išsaugokite – skelbimas aktyvuosis' in h,
            'žinutė „Įkelkite bent vieną nuotrauką ir išsaugokite…"')
    k = re.search(r'id="serverio-klaidos">(.*?)</script>', h, re.S)
    k = json.loads(k.group(1)) if k else {}
    tikrink(k.get('laukai') == ['images'], f'klaidų sąrašas ne tuščias: {k.get("laukai")}')
    tikrink('form-error-box' not in h or 'Įkelkite bent vieną nuotrauką' in h,
            'nėra tuščios klaidų dėžutės')
    be_mokejimo(h, '   redagavimo forma')

    print('\n— Įkėlus foto ir išsaugojus redagavimą → aktyvus pats')
    nuotrauka(n)
    url = galas
    postas = {}
    for raktas, reiksme in forma_testas.forma(html(c.get(url))).laukai:
        postas.setdefault(raktas, []).append(reiksme)
    a = c.post(url, postas)
    n.refresh_from_db()
    tikrink(n.status == 'active', f'po išsaugojimo aktyvus ({n.status}; POST {a.status_code})')
    tikrink(anonimas.get(f'/{n.pk}/').status_code == 200, '   anonimui 200')

    print('\n— Ne savininkas')
    kitas = get_user_model().objects.filter(email='kitas@autoleft.lt').first() or \
        get_user_model().objects.create_user(username='kitas_patikra', email='kitas@autoleft.lt',
                                             password='Patikra123!')
    sv = juodrastis(u, 'Patikra svetimas', foto=True)
    k2 = Client()
    k2.force_login(kitas)
    a = k2.post(f'/listings/{sv.pk}/activate/')
    sv.refresh_from_db()
    tikrink(a.status_code in (403, 404), f'ne savininkas → {a.status_code}')
    tikrink(sv.status == 'draft', 'būsena nepakito')

    print('\n— GET būsenos nekeičia')
    for kelias in (f'/listings/{sv.pk}/activate/', f'/listings/{sv.pk}/select-plan/'):
        c.get(kelias, follow=True)
        sv.refresh_from_db()
        tikrink(sv.status == 'draft', f'GET {kelias} → liko juodraštis')
    a = c.get(f'/listings/{sv.pk}/select-plan/')
    tikrink(a.status_code == 302 and a.get('Location') == f'/listings/{sv.pk}/activate/',
            f'select-plan → 302 /listings/<id>/activate/ ({a.get("Location")})')
    be_mokejimo(html(c.get(f'/listings/{sv.pk}/activate/')), '   GET activate puslapis')

    print('\n— Aktyvaus skelbimo redagavimas → lieka aktyvus')
    url = f'/create/parts/form/?edit={l.pk}'
    postas = {}
    for raktas, reiksme in forma_testas.forma(html(c.get(url))).laukai:
        postas.setdefault(raktas, []).append(reiksme)
    postas['title'] = ['Patikra aktyvavimas su foto (redaguota)']
    a = c.post(url, postas)
    l.refresh_from_db()
    tikrink(l.status == 'active' and 'redaguota' in l.title,
            f'išsaugota ir aktyvus ({l.status}, POST {a.status_code})')
    tikrink(anonimas.get(f'/{l.pk}/').status_code == 200, '   anonimui 200')

    print('\n— [Deaktyvuoti] [Redaguoti] aktyviame')
    h = html(c.get('/dashboard/announcements/?status=active'))
    tikrink(f'action="/listings/{l.pk}/deactivate/"' in h and f'href="/{l.pk}/edit/"' in h,
            'skydelyje aktyviam — [Deaktyvuoti] ir [Redaguoti]')
    h = html(c.get('/dashboard/announcements/?status=inactive'))
    tikrink(f'action="/listings/{sv.pk}/activate/"' in h and f'href="/{sv.pk}/edit/"' in h,
            'skydelyje juodraščiui — [Aktyvuoti] (POST /activate/) ir [Redaguoti]')
    c.post(f'/listings/{l.pk}/deactivate/')
    l.refresh_from_db()
    tikrink(l.status != 'active' and anonimas.get(f'/{l.pk}/').status_code == 404,
            f'deaktyvuotas → anonimui 404 ({l.status})')

    print(f'\n════ {gerai} gerai / {blogai} blogai ════')
    return 1 if blogai else 0


if __name__ == '__main__':
    with override_settings(MEDIA_ROOT=MEDIA):
        kodas = main()
    sys.exit(kodas)
