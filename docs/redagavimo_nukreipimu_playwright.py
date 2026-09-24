# -*- coding: utf-8 -*-
"""
SKELBIMO REDAGAVIMAS: ar išsaugojus nukreipia į patį skelbimą.

Klaida: visos formos (išskyrus trucks ir ratus) po sėkmingo išsaugojimo
grįždavo į `listing_edit_hub`, o tas tą patį skelbimą permeta atgal į
/create/…/?edit=<pk>. Vartotojas likdavo toje pačioje formoje ir
nematydavo jokio patvirtinimo. Moto dalis dar blogiau: išsaugojus mesdavo
į /dashboard/announcements/, o /NNN/edit/ jos išvis neatidarydavo.

Kiekvienai kategorijai darom tą patį, ką ir žmogus:
  1. atidarom /NNN/edit/,
  2. pakeičiam aprašymą,
  3. išsaugom,
  4. tikrinam, kad adresas tapo /NNN/ (arba /wheels/NN/)
     IR kad naujas aprašymas matosi skelbime.

Paleidimas:
    PATIKRA_DB=<...> python docs/redagavimo_nukreipimu_playwright.py
(reikia vietinio serverio 127.0.0.1:8899 su TA PAČIA duomenų baze)
"""
import os
import re
import sys
import time

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sqlite_settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'patikra'))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

import formu_seed                                   # noqa: E402
from playwright.sync_api import sync_playwright     # noqa: E402

ADRESAS = os.environ.get('ADRESAS', 'http://127.0.0.1:8899')
NARSYKLE = os.environ.get('CHROMIUM',
                          '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')

gerai = blogai = 0
nesekmes = []


def tikrink(salyga, tekstas, papildomai=''):
    global gerai, blogai
    if salyga:
        gerai += 1
        print(f'  OK   {tekstas}')
    else:
        blogai += 1
        nesekmes.append(tekstas)
        print(f'  BLOGAI {tekstas}' + (f'\n         {papildomai}' if papildomai else ''))


def prisijunk(p):
    p.goto(f'{ADRESAS}/accounts/login/', wait_until='domcontentloaded')
    p.fill('input[name="email"]', formu_seed.PASTAS)
    p.fill('input[name="password"]', formu_seed.SLAPTAZODIS)
    # Puslapyje daug submit mygtukų (kalbos perjungiklis ir kt.) —
    # spaudžiam būtent prisijungimo formos.
    p.click('form:has(input[name="password"]) button[type="submit"]')
    p.wait_for_load_state('domcontentloaded')


def klaidos_tekstas(p):
    """Ką forma parodė, jei neišsaugojo — kad ataskaita būtų naudinga."""
    gabalai = []
    for sel in ('[id$="form-errors"] li', '[id$="form-error-list"] li',
                '.messages li', '[role="alert"]'):
        try:
            tekstai = p.locator(sel).all_inner_texts()[:4]
        except Exception:      # dar vyksta nukreipimas — konteksto nebėra
            continue
        for t in tekstai:
            t = ' '.join(t.split())
            if t and t not in gabalai:
                gabalai.append(t)
    return ' | '.join(gabalai)[:400] or f'liko {p.url}'


def be_kalbos(url):
    """/en/852/ → /852/ — i18n_patterns prideda kalbos priešdėlį."""
    kelias = url.split(ADRESAS)[-1].split('?')[0].split('#')[0]
    return re.sub(r'^/[a-z]{2}(-[a-z]{2})?/', '/', kelias)


def uzpildyk_tuscius(p, aprasymo_sel):
    """Užpildo TIK tuščius privalomus formos laukus.

    Bandomieji skelbimai sėjami minimaliai (modelio privalomi laukai), o
    kiekviena forma dar turi savų privalomų laukų (tipas, gamintojas,
    telefonas). Nepaliestų laukų neperrašinėjam — kitaip patikra
    nebeparodytų, ar forma užsipildo iš DB (tą tikrinam atskirai).
    """
    return p.evaluate("""(sel) => {
        const form = document.querySelector(sel).closest('form');
        if (!form) { return 0; }
        let n = 0;
        form.querySelectorAll('input, select, textarea').forEach(el => {
            if (el.type === 'file' || el.type === 'hidden') { return; }
            if (el.name === 'description') { return; }
            if (el.type === 'checkbox') {
                if (/agree|terms|sutink/i.test(el.name) && !el.checked) { el.checked = true; n++; }
                return;
            }
            if (el.type === 'radio' || el.disabled) { return; }
            if (el.value) { return; }
            if (el.tagName === 'SELECT') {
                const o = Array.from(el.options).find(x => x.value);
                if (o) { el.value = o.value; n++; }
            } else if (/phone|tel/i.test(el.name)) { el.value = '+37060000000'; n++; }
            else if (el.type === 'email') { el.value = 'patikra@autoleft.lt'; n++; }
            else if (el.type === 'number') { el.value = '1'; n++; }
            else if (el.type === 'date') { el.value = '2020-01-01'; n++; }
            else if (el.type === 'text' || el.type === '' || el.tagName === 'TEXTAREA') {
                el.value = 'Patikra'; n++;
            }
            el.dispatchEvent(new Event('input', {bubbles: true}));
            el.dispatchEvent(new Event('change', {bubbles: true}));
        });
        return n;
    }""", aprasymo_sel)


def issaugok(p, aprasymo_sel):
    """Spaudžiam tikrą mygtuką: vienos formos turi <button type=submit>,
    kitos — <button type=button onclick=handle…Submit()>."""
    return p.evaluate("""(sel) => {
        const form = document.querySelector(sel).closest('form');
        if (!form) { return false; }
        const tiesiogiai = form.querySelector('button[type="submit"], input[type="submit"]');
        if (tiesiogiai) { tiesiogiai.click(); return true; }
        const visi = Array.from(document.querySelectorAll('button[onclick]'));
        const m = visi.find(b => /handle\\w*Submit\\s*\\(/.test(b.getAttribute('onclick') || ''));
        if (m) { m.click(); return true; }
        form.submit();
        return true;
    }""", aprasymo_sel)


def redaguok(p, pavadinimas, edit_url, laukiamas_url, aprasymo_sel='[name="description"]'):
    """Atidaro redagavimą, pakeičia aprašymą, išsaugo ir tikrina."""
    print(f'\n— {pavadinimas}')
    zyme = f'PATIKRA-{int(time.time() * 1000) % 10 ** 7}'

    p.goto(f'{ADRESAS}{edit_url}', wait_until='domcontentloaded')
    p.wait_for_timeout(400)

    # 1) ar redagavimo forma apskritai atsidarė
    if p.locator(aprasymo_sel).count() == 0:
        tikrink(False, f'{pavadinimas}: redagavimo forma atsidarė',
                f'vietoj jos {p.url}')
        return
    tikrink(True, f'{pavadinimas}: redagavimo forma atsidarė ({be_kalbos(p.url)})')

    # 2) privalomi laukai užpildyti IŠ ANKSTO (kaina!)
    kaina = p.locator('[name="price"]')
    if kaina.count():
        v = kaina.first.input_value()
        tikrink(bool(v.strip()), f'{pavadinimas}: kainos laukas užpildytas', f'value={v!r}')
    dia = p.locator('[name="rim_dia"]')
    if dia.count():
        v = dia.first.input_value()
        tikrink(bool(v.strip()), f'{pavadinimas}: DIA laukas užpildytas', f'value={v!r}')

    uzpildyk_tuscius(p, aprasymo_sel)
    p.fill(aprasymo_sel, f'Pakeista {zyme}')
    if not issaugok(p, aprasymo_sel):
        tikrink(False, f'{pavadinimas}: rastas išsaugojimo mygtukas')
        return
    # Klaidinga elgsena būdavo nukreipimų grandinė (hub → /create/…/?edit=),
    # todėl laukiam, kol naršyklė nurims, o ne vieno įvykio.
    for _ in range(3):
        try:
            p.wait_for_load_state('networkidle', timeout=8000)
            break
        except Exception:
            pass
    p.wait_for_timeout(500)

    kelias = be_kalbos(p.url)
    tikrink(kelias == laukiamas_url,
            f'{pavadinimas}: nukreipė į {laukiamas_url}',
            f'nukreipė į {kelias} — {klaidos_tekstas(p)}')
    if kelias == laukiamas_url:
        tikrink(zyme in p.content(), f'{pavadinimas}: pakeitimas matosi skelbime')


def main():
    s = formu_seed.skelbimai()
    r = formu_seed.ratai()

    uzduotys = [
        ('Automobilis (quickForm)',  s['cars']),
        ('Valtis (boatForm)',        s['boats']),
        ('Priekaba (trailerForm)',   s['trailers']),
        ('Žemės ūkis (agriForm)',    s['agriculture']),
        ('Statybinė (constrForm)',   s['construction']),
        ('Priedas (attachForm)',     s['attachment']),
        ('Elektronika (elecForm)',   s['electronics']),
        ('Paslaugos (svcForm)',      s['services']),
        ('Dviratis (bikeForm)',      s['bicycles']),
        ('Nuoma (rentCarForm)',      s['rental']),
        ('Moto apranga (mainForm)',  s['motogear']),
        ('Moto dalis',               s['motopart']),
    ]

    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=NARSYKLE)
        ctx = b.new_context(viewport={'width': 1440, 'height': 950},
                            ignore_https_errors=True)
        p = ctx.new_page()
        prisijunk(p)

        for pavadinimas, l in uzduotys:
            redaguok(p, pavadinimas, f'/{l.pk}/edit/', f'/{l.pk}/')

        for tipas, pav in (('tyre', 'Padangos'), ('rim', 'Ratlankiai')):
            w = r[tipas]
            redaguok(p, f'{pav} (/wheels/{w.pk}/edit/)',
                     f'/wheels/{w.pk}/edit/', f'/wheels/{w.pk}/')

        ctx.close()
        b.close()

    print(f'\n════ {gerai} gerai / {blogai} blogai ════')
    for n in nesekmes:
        print('   ·', n)
    return 1 if blogai else 0


if __name__ == '__main__':
    sys.exit(main())
