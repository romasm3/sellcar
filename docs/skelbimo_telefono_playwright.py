# -*- coding: utf-8 -*-
"""
SKELBIMO TELEFONAS: rodomas skelbimo, o ne paskyros numeris.

Klaida: skelbimo puslapyje (pardavėjo blokas) numeris buvo imamas iš
PASKYROS (`p.phone_number`), o `Listing.kontaktinis_telefonas` tuščią
skelbimo lauką irgi pakeisdavo paskyros numeriu. Todėl skelbimai, kuriuos
kuriant žmogus įvedė +49 171 39200xx, rodė savininko asmeninį
+370 671 12478 (#833, #841, #844, #847).

Tikrinam:
  1. skelbimas su savo numeriu rodo SAVO, o ne paskyros;
  2. /NNN/telefonas/ (pilnas numeris) grąžina tą patį skelbimo numerį;
  3. skelbimas BE numerio nerodo nieko — paskyros numeris neatsiranda;
  4. redagavimo forma užsipildo skelbimo numeriu;
  5. naujo skelbimo formoje paskyros numeris lieka numatytąja reikšme.

Paleidimas (reikia vietinio serverio 127.0.0.1:8899 su TA PAČIA DB):
    PATIKRA_DB=<...> python docs/skelbimo_telefono_playwright.py
"""
import os
import sys

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sqlite_settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'patikra'))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

from playwright.sync_api import sync_playwright        # noqa: E402

import formu_seed                                      # noqa: E402

ADRESAS = os.environ.get('ADRESAS', 'http://127.0.0.1:8899')
NARSYKLE = os.environ.get('CHROMIUM',
                          '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')

PASKYROS = '+370 671 12478'      # asmeninis, kurio skelbime būti neturi
SKELBIMO = '+49 171 3920011'     # įvestas kuriant skelbimą

gerai = blogai = 0


def tikrink(salyga, tekstas, papildomai=''):
    global gerai, blogai
    if salyga:
        gerai += 1
        print(f'  OK   {tekstas}')
    else:
        blogai += 1
        print(f'  BLOGAI {tekstas}' + (f'\n         {papildomai}' if papildomai else ''))


def pasejk():
    """Du skelbimai: vienas su savo numeriu, kitas be jokio."""
    from decimal import Decimal

    from apps.listings.models import Listing, VehicleType

    u = formu_seed.vartotojas()
    profilis = u.profile
    profilis.phone_number = PASKYROS
    profilis.show_phone = True
    profilis.save()

    vt, _ = VehicleType.objects.get_or_create(slug='cars',
                                              defaults={'name': 'Cars'})
    isvestis = {}
    for raktas, antraste, numeris in (('savas', 'Telefonas savas', SKELBIMO),
                                      ('tuscias', 'Telefonas tuscias', '')):
        l = Listing.objects.filter(seller=u, title=antraste).first() or Listing(
            seller=u, title=antraste)
        l.vehicle_type = vt
        l.year, l.mileage, l.price = 2019, 1000, Decimal('1000')
        l.city, l.country, l.status = 'Vilnius', 'LT', 'active'
        l.contact_phone = numeris
        l.save()
        isvestis[raktas] = l
    return isvestis


def main():
    s = pasejk()

    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=NARSYKLE)
        ctx = b.new_context(viewport={'width': 1440, 'height': 950},
                            ignore_https_errors=True)
        p = ctx.new_page()

        # ── 1. Skelbimas su savo numeriu ─────────────────────────────
        print('\n— Skelbimas su savo numeriu')
        p.goto(f"{ADRESAS}/{s['savas'].pk}/", wait_until='domcontentloaded')
        p.wait_for_timeout(500)
        html = p.content()
        tikrink(SKELBIMO[:8] in html, f'puslapyje matosi skelbimo numeris ({SKELBIMO[:8]}…)')
        tikrink(PASKYROS[:8] not in html,
                'paskyros numerio puslapyje NĖRA',
                f'rastas {PASKYROS[:8]}… — vėl rodomas paskyros numeris')

        # ── 2. Pilnas numeris per /NNN/telefonas/ ────────────────────
        atsakas = p.request.get(f"{ADRESAS}/{s['savas'].pk}/telefonas/")
        duomenys = atsakas.json() if atsakas.ok else {}
        tikrink(duomenys.get('telefonas') == SKELBIMO,
                '/NNN/telefonas/ grąžina skelbimo numerį',
                f'grąžino {duomenys.get("telefonas")!r}')

        # ── 3. Skelbimas be numerio ──────────────────────────────────
        print('\n— Skelbimas be numerio')
        p.goto(f"{ADRESAS}/{s['tuscias'].pk}/", wait_until='domcontentloaded')
        p.wait_for_timeout(500)
        html = p.content()
        tikrink(PASKYROS[:8] not in html,
                'paskyros numeris NEatsiranda vietoj tuščio',
                f'rastas {PASKYROS[:8]}…')
        atsakas = p.request.get(f"{ADRESAS}/{s['tuscias'].pk}/telefonas/")
        tikrink(atsakas.status == 404,
                '/NNN/telefonas/ tuščiam grąžina 404, ne paskyros numerį',
                f'status={atsakas.status} body={atsakas.text()[:120]}')

        # ── 4-5. Formos ──────────────────────────────────────────────
        print('\n— Redagavimo ir kūrimo formos')
        p.goto(f'{ADRESAS}/accounts/login/', wait_until='domcontentloaded')
        p.fill('input[name="email"]', formu_seed.PASTAS)
        p.fill('input[name="password"]', formu_seed.SLAPTAZODIS)
        p.click('form:has(input[name="password"]) button[type="submit"]')
        p.wait_for_load_state('domcontentloaded')

        p.goto(f"{ADRESAS}/{s['savas'].pk}/edit/", wait_until='domcontentloaded')
        p.wait_for_timeout(600)
        reiksme = p.locator('[name="phone"]').first.input_value()
        tikrink(reiksme.strip() == SKELBIMO,
                'redagavimo forma rodo SKELBIMO numerį', f'rodo {reiksme!r}')

        # Tuščiam skelbimui paskyros numeris tik SIŪLOMAS — placeholder'iu.
        # Įrašytas į `value` jis išsisaugodavo žmogui nieko nepakeitus, ir
        # taip paskyros savininko numeris atsidurdavo svetimame skelbime.
        p.goto(f"{ADRESAS}/{s['tuscias'].pk}/edit/", wait_until='domcontentloaded')
        p.wait_for_timeout(600)
        laukas = p.locator('[name="phone"]').first
        reiksme = laukas.input_value()
        uzuomina = laukas.get_attribute('placeholder') or ''
        tikrink(reiksme.strip() == '',
                'tuščiam skelbimui laukas TUŠČIAS (paskyros numeris neįrašomas)',
                f'rodo {reiksme!r} — vėl išsisaugotų savaime')
        tikrink(uzuomina.strip() == PASKYROS,
                'paskyros numeris matomas kaip užuomina (placeholder)',
                f'placeholder={uzuomina!r}')

        ctx.close()
        b.close()

    print(f'\n════ {gerai} gerai / {blogai} blogai ════')
    return 1 if blogai else 0


if __name__ == '__main__':
    sys.exit(main())
