# -*- coding: utf-8 -*-
"""
„AKTYVUOTI" AKTYVUOJA VISADA (žmogaus sprendimai 2026-10-01).

    [Aktyvuoti] = POST /listings/<id>/activate/ (CSRF, tik savininkas) →
    aktyvus → /dashboard/announcements/ su „Skelbimas aktyvuotas" + nuoroda.
Jokių patikrų: ir be nuotraukų (placeholder), ir be kainos/miesto.
Vienintelis atsisakymas — ne savininkas (404). Laiško nuoroda
GET /listings/<id>/activate/?t=<pasirašytas tokenas> aktyvuoja vienu
paspaudimu; blogas / pasenęs tokenas → 403. Laiškas — gavėjo kalba.

Tikrinam (tikras HTML ir DB):
  • juodraštis su foto → POST activate → 302 į skydelį, žinutė su nuoroda;
    anoniminis GET /<id>/ → 200
  • juodraštis BE nuotraukų (ir be kainos/miesto) → POST activate → 302;
    anoniminis GET /<id>/ → 200
  • GET ?t=<geras tokenas> (neprisijungus) → 302 į /<id>/, aktyvus
  • GET ?t=<blogas / pasenęs / kito skelbimo> → 403, būsena ta pati
  • ne savininkas → 403/404, būsena nepakinta
  • GET activate be tokeno ir GET select-plan būsenos nekeičia
  • aktyvaus skelbimo redagavimo išsaugojimas → lieka aktyvus (anonimui 200)
  • [Deaktyvuoti] [Redaguoti] aktyviame; [Aktyvuoti] [Redaguoti] juodraštyje
  • LT gavėjo laiške nėra „Activate my listing", yra „Aktyvuoti skelbimą";
    mygtukas — vieno paspaudimo nuoroda su tokenu; „Redaguoti" → /<id>/edit/
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

    print('\n— Juodraštis BE nuotraukų, kainos ir miesto → vis tiek aktyvuojamas')
    m = juodrastis(u, 'Patikra be nuotrauku', foto=False, kaina='0', miestas='—')
    a = c.post(f'/listings/{m.pk}/activate/')
    m.refresh_from_db()
    tikrink(a.status_code == 302 and a.get('Location') == '/dashboard/announcements/',
            f'302 → skydelis (gauta {a.status_code} {a.get("Location")})')
    tikrink(m.status == 'active' and not m.images.exists(), f'aktyvus be nuotraukų ({m.status})')
    r = anonimas.get(f'/{m.pk}/')
    tikrink(r.status_code == 200, f'anoniminis GET /{m.pk}/ → 200 (gauta {r.status_code})')
    tikrink('Įkelkite bent vieną nuotrauką' not in html(c.get('/dashboard/announcements/')),
            'jokio „Įkelkite bent vieną nuotrauką"')

    print('\n— Laiško nuoroda: GET ?t=<tokenas>')
    from unittest import mock
    import time as _time
    from apps.listings.aktyvavimas import aktyvavimo_tokenas
    t1 = juodrastis(u, 'Patikra tokenas geras', foto=False)
    a = anonimas.get(f'/listings/{t1.pk}/activate/', {'t': aktyvavimo_tokenas(t1)})
    t1.refresh_from_db()
    tikrink(a.status_code == 302 and a.get('Location') == f'/{t1.pk}/',
            f'geras tokenas (neprisijungus) → 302 /{t1.pk}/ (gauta {a.status_code} {a.get("Location")})')
    tikrink(t1.status == 'active', f'   aktyvus ({t1.status})')
    tikrink('Skelbimas aktyvuotas' in html(anonimas.get(f'/{t1.pk}/')), '   žinutė „Skelbimas aktyvuotas"')

    t2 = juodrastis(u, 'Patikra tokenas blogas', foto=False)
    with mock.patch('django.core.signing.time.time', return_value=_time.time() - 31 * 86400):
        pasenes = aktyvavimo_tokenas(t2)
    kito = aktyvavimo_tokenas(t1)                 # galioja, bet kitam skelbimui
    for pav, tok in (('blogas', 'blogas:tokenas'), ('pasenęs (31 d.)', pasenes),
                     ('kito skelbimo', kito), ('tuščias', '')):
        a = anonimas.get(f'/listings/{t2.pk}/activate/', {'t': tok})
        t2.refresh_from_db()
        tikrink(a.status_code == 403 and t2.status == 'draft',
                f'{pav} tokenas → 403, liko juodraštis (gauta {a.status_code}, {t2.status})')
    sv = t2

    print('\n— Ne savininkas')
    kitas = get_user_model().objects.filter(email='kitas@autoleft.lt').first() or \
        get_user_model().objects.create_user(username='kitas_patikra', email='kitas@autoleft.lt',
                                             password='Patikra123!')
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

    print('\n— Priminimo laiškas: gavėjo kalba ir vieno paspaudimo nuoroda')
    from apps.listings.management.commands.send_draft_reminders import priminimo_laiskas
    from apps.accounts.models import Profile
    lj = juodrastis(u, 'Patikra laiskas', foto=False)
    for kalba, turi, neturi in (('lt', 'Aktyvuoti skelbimą', 'Activate my listing'),
                                ('en', 'Activate my listing', 'Aktyvuoti skelbimą')):
        profilis, _sukurtas = Profile.objects.get_or_create(user=u)
        profilis.language = kalba
        profilis.save(update_fields=['language'])
        lj.seller.refresh_from_db()
        tema, tekstas, laiskas = priminimo_laiskas(lj, 'draft_reminder_first', site_url='')
        tikrink(turi in laiskas and neturi not in laiskas,
                f'{kalba.upper()} gavėjui: yra „{turi}", nėra „{neturi}"')
        if kalba == 'lt':
            tikrink('JŪSŲ JUODRAŠTIS' in laiskas.upper() and 'Kodėl verta aktyvuoti dabar?' in laiskas
                    and 'Redaguoti skelbimą' in laiskas and 'Why activate' not in laiskas,
                    '   LT: juodraštis, „Kodėl verta…", „Redaguoti skelbimą"')
            tikrink('Užbaikite' in tema and 'Complete' not in tema, f'   LT tema: „{tema}"')
            _t, _tekstas, kasdienis = priminimo_laiskas(lj, 'draft_reminder_daily', site_url='')
            tikrink('Aktyvuoti skelbimą' in kasdienis and 'Activate' not in kasdienis,
                    '   LT kasdienis laiškas išverstas')
        # Nuorodos — gavėjo kalba (EN: /en/… priešdėlis), kad atsidarytų jo kalba
        nuoroda = re.search(r'href="((?:/[a-z]{2})?/listings/\d+/activate/\?t=[^"]+)"', laiskas)
        tikrink(nuoroda is not None
                and re.search(rf'href="(?:/[a-z]{{2}})?/{lj.pk}/edit/"', laiskas) is not None,
                '   mygtukas — /activate/?t=…, „Redaguoti" — /<id>/edit/ (ne /create/)')
        if kalba == 'lt':
            lt_nuoroda = nuoroda.group(1).replace('&amp;', '&') if nuoroda else ''
    a = anonimas.get(lt_nuoroda, follow=True)
    lj.refresh_from_db()
    tikrink(a.status_code == 200 and lj.status == 'active'
            and a.redirect_chain and a.redirect_chain[-1][0].rstrip('/').endswith(f'/{lj.pk}'),
            f'laiško mygtukas aktyvuoja vienu paspaudimu ir veda į /<id>/ ({lj.status}, '
            f'{[x[0] for x in a.redirect_chain]})')
    Profile.objects.filter(user=u).update(language='lt')

    print(f'\n════ {gerai} gerai / {blogai} blogai ════')
    return 1 if blogai else 0


if __name__ == '__main__':
    with override_settings(MEDIA_ROOT=MEDIA):
        kodas = main()
    sys.exit(kodas)
