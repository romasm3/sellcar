# -*- coding: utf-8 -*-
"""
PAIEŠKOS SKYDELIO POTIPIAI (sp-panel-*) — ar skydelis nelieka tuščias.

Klaida, kurią gaudom: ?sekcija= reikšmė buvo įrašoma į VISŲ kategorijų
potipių laukus (subTab.trucks, subTab.construction, partSub, rentSub,
wheelType), o goTab() grįžtant į pagrindinę kategoriją potipio
neatstatydavo. Rezultatas — „Vilkikai" → „Sunkvežimiai" atidarydavo baltą
langą su antrašte ir be nė vieno lauko.

Tikrinam:
  1. inicijuojant iš URL sekcija patenka TIK į savo kategorijos lauką;
  2. netinkama sekcijos reikšmė virsta numatytąja, o forma matoma;
  3. „…" → potipis → „…" → pagrindinė kategorija: laukai matomi
     (vilkikai, statybinė technika, nuoma — trys vartotojo nurodyti keliai);
  4. „Automobilių supirkimas" (paslaugų sekcija) — ar sekcija ne dingsta.

Paleidimas (reikia vietinio serverio 127.0.0.1:8899):
    python docs/skydelio_potipiu_playwright.py
"""
import os
import sys

from playwright.sync_api import sync_playwright

ADRESAS = os.environ.get('ADRESAS', 'http://127.0.0.1:8899')
NARSYKLE = os.environ.get('CHROMIUM',
                          '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')

gerai = blogai = 0


def tikrink(salyga, tekstas, papildomai=''):
    global gerai, blogai
    if salyga:
        gerai += 1
        print(f'  OK   {tekstas}')
    else:
        blogai += 1
        print(f'  BLOGAI {tekstas}' + (f'\n         {papildomai}' if papildomai else ''))


def eik(p, kelias_):
    """Atidarom puslapį ir laukiam, kol Alpine iš tikrųjų pasileis.
    Be šito x-show dar nepritaikytas ir „matoma" reiškia bet ką."""
    paskutine = None
    for _ in range(3):
        p.goto(f'{ADRESAS}{kelias_}', wait_until='networkidle')
        try:
            p.wait_for_function(
                '() => window.Alpine && window.Alpine.$data && '
                '!document.querySelector("[x-cloak]")', timeout=8000)
            p.wait_for_timeout(300)
            return
        except Exception as e:          # Alpine ateina iš CDN — pasitaiko
            paskutine = e
    raise RuntimeError(f'Alpine nepasileido: {paskutine}')


def busena(p):
    """Gyva Alpine spPanel() būsena."""
    return p.evaluate("""() => {
        const el = document.querySelector('[x-data*="spPanel"]');
        const d = window.Alpine.$data(el);
        return {tab: d.tab, subTab: JSON.parse(JSON.stringify(d.subTab)),
                partSub: d.partSub, rentSub: d.rentSub, wheelType: d.wheelType};
    }""")


def matomu_lauku(p, key):
    """Kiek matomų įvesties laukų turi tos kategorijos skydelis."""
    return p.evaluate("""(key) => {
        const pan = document.getElementById('sp-panel-' + key);
        if (!pan) { return -1; }
        let n = 0;
        pan.querySelectorAll('form.sp-search-form').forEach(f => {
            if (!(f.offsetWidth || f.offsetHeight)) { return; }
            f.querySelectorAll('input, select, button, .sp-fld').forEach(x => {
                if (x.type === 'hidden') { return; }
                if (x.offsetWidth || x.offsetHeight) { n++; }
            });
        });
        return n;
    }""", key)


def atidaryk_daugiau(p):
    """„…" sąrašas stalinėje versijoje atsidaro užvedus pelę.
    Paspaudimas čia netinka: @mouseenter jį jau atidaro, o @click
    perjungia atgal į uždarytą."""
    p.hover('.sp-rail-fixed button.sp-rail-btn2')
    p.wait_for_timeout(250)


def spausk_punkta(p, pavadinimas):
    # Spaudžiam ne per vidurį: pirmas sąrašo punktas guli prie pat „…"
    # mygtuko ir kartais jo kampas perima paspaudimą.
    p.click(f'.sp-rail-fixed a:has-text("{pavadinimas}")',
            position={'x': 220, 'y': 12})
    p.wait_for_timeout(800)


def kelias(p, pradzia, punktas, key, aprasas):
    """Atidarom potipį iš URL, po to per „…" grįžtam į pagrindinę kategoriją."""
    print(f'\n— {aprasas}')
    eik(p, pradzia)
    tikrink(matomu_lauku(p, key) > 0, f'potipis atidarytas, laukai matomi ({pradzia})',
            f'matomų laukų: {matomu_lauku(p, key)}')
    atidaryk_daugiau(p)
    spausk_punkta(p, punktas)
    n = matomu_lauku(p, key)
    tikrink(n > 0, f'grįžus į „{punktas}" laukai matomi', f'matomų laukų: {n}')
    return n


with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=NARSYKLE)
    ctx = b.new_context(viewport={'width': 1440, 'height': 950},
                        ignore_https_errors=True)
    p = ctx.new_page()

    # ── 1. Sekcija neteršia kitų kategorijų laukų ─────────────────────
    print('\n— Sekcija priklauso tik savo kategorijai')
    eik(p, '/?section=trucks&sekcija=semi-trucks-tractors')
    s = busena(p)
    tikrink(s['subTab']['trucks'] == 'semi-trucks-tractors',
            'subTab.trucks = semi-trucks-tractors', str(s))
    tikrink(s['subTab']['construction'] == 'main', 'subTab.construction liko main', str(s))
    tikrink(s['partSub'] == 'car', 'partSub liko car', str(s))
    tikrink(s['rentSub'] == 'car-rental', 'rentSub liko car-rental', str(s))
    tikrink(s['wheelType'] == 'tyre', 'wheelType liko tyre', str(s))

    # ── 2. Netinkama sekcijos reikšmė ─────────────────────────────────
    print('\n— Netinkama ?sekcija= reikšmė')
    eik(p, '/?section=trucks&sekcija=nesamone-123')
    s = busena(p)
    tikrink(s['subTab']['trucks'] == 'main', 'subTab.trucks nukrito į main', str(s))
    tikrink(matomu_lauku(p, 'trucks') > 0, 'skydelis su laukais, ne tuščias',
            f"matomų laukų: {matomu_lauku(p, 'trucks')}")

    # ── 3. Trys vartotojo nurodyti keliai ─────────────────────────────
    kelias(p, '/?section=trucks&sekcija=semi-trucks-tractors', 'Sunkvežimiai',
           'trucks', 'Vilkikai → Sunkvežimiai')
    kelias(p, '/?section=construction&sekcija=construction-attachments',
           'Statybinė technika', 'construction',
           'Statybinės technikos priedai → Statybinė technika')
    kelias(p, '/?section=rental&sekcija=limo-wedding-rental', 'Automobilių nuoma',
           'rental', 'Limuzinų nuoma → Automobilių nuoma')

    # Dalys — ketvirtas vartotojo paminėtas atvejis
    print('\n— Dalys po vilkikų')
    eik(p, '/?section=trucks&sekcija=semi-trucks-tractors')
    p.click('a.sp-rail-btn2[href="/?section=parts"]')
    p.wait_for_timeout(700)
    n = matomu_lauku(p, 'parts')
    tikrink(n > 0, 'dalių skydelyje laukai matomi', f'matomų laukų: {n}')

    # ── 4. Automobilių supirkimas — paslaugų sekcija ──────────────────
    print('\n— Automobilių supirkimas (?section=services&sekcija=car-buying)')
    eik(p, '/?section=services&sekcija=car-buying')
    tekstas = p.inner_text('#sp-panel-services h2')
    tikrink('supirkimas' in tekstas.lower(), 'antraštė rodo sekciją', tekstas)
    tikrink(p.locator('#sp-panel-services input[type="hidden"]'
                      '[name="service_type"][value="car_buying"]').count() == 1,
            'forma paduoda service_type=car_buying (sekcija NEignoruojama)')
    tikrink(matomu_lauku(p, 'services') > 0, 'paslaugų laukai matomi',
            f"matomų laukų: {matomu_lauku(p, 'services')}")

    ctx.close()
    b.close()

print(f'\n════ {gerai} gerai / {blogai} blogai ════')
sys.exit(1 if blogai else 0)
