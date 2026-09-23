# -*- coding: utf-8 -*-
"""
„ŽIŪRĖTI VISUS" — CENTRUOTAS PO KORTELIŲ TINKLELIU.

Kas buvo. Mygtukas gulėjo prispaustas prie kairio krašto visose titulinio
sekcijose. CSS atrodė teisingai:

    .home-tab-visi { max-width: 320px; margin: var(--sp-5) auto 0; ... }

bet `--sp-5` niekur neapibrėžtas (skalėje yra --sp-1..4, 6, 8, 10, 16).
Neapibrėžtas `var()` padaro VISĄ `margin` trumpinį netinkamą skaičiavimo
metu, tad `margin` krenta į pradinę reikšmę 0 — kartu su `auto`. Mygtukas
lieka kairėje ir be viršutinio tarpo.

Matuojam TIKRĄ atstumą naršyklėje: mygtuko vidurys prieš jo konteinerio
vidurį. Tikrinam visus skirtukus ir stalinį bei mobilų plotį.

Paleidimas (reikia vietinio serverio 127.0.0.1:8899):
    python docs/ziureti_visus_centras_playwright.py
    ADRESAS=https://autoleft.com python docs/ziureti_visus_centras_playwright.py
"""
import os
import sys

from playwright.sync_api import sync_playwright

ADRESAS = os.environ.get('ADRESAS', 'http://127.0.0.1:8899')
NARSYKLE = os.environ.get('CHROMIUM', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')

# Kiek pikselių nuokrypio nuo vidurio dar laikom centru. Nelyginis
# konteinerio plotis duoda pusę pikselio, tad nulio reikalauti negalima.
RIBA = 2.0

SKIRTUKAI = ('offers', 'daily', 'newest', 'popular', 'expensive')
PLOCIAI = (('stalinis', 1280, 900), ('mobilus', 390, 844))

# Atskaita — TĖVINIO elemento turinio dėžė: būtent joje `margin-inline:
# auto` ir centruoja. Matuoti pagal `closest([x-show])` nepatikima: tą patį
# atributą turi keli lygiai, ir atskaitos plotis šokinėja.
MATUOK = """
(tab) => {
    const a = [...document.querySelectorAll('a.home-tab-visi')].find(el => {
        const sek = el.closest('[x-show]');
        return sek && sek.getAttribute('x-show').includes(`'${tab}'`);
    });
    if (!a) return null;
    const m = a.getBoundingClientRect();
    if (!m.width) return null;

    const t = a.parentElement;
    const tr = t.getBoundingClientRect();
    const ts = getComputedStyle(t);
    const kaire = tr.left + parseFloat(ts.paddingLeft || 0);
    const desine = tr.right - parseFloat(ts.paddingRight || 0);

    const st = getComputedStyle(a);
    return {
        mygtukoVidurys: m.left + m.width / 2,
        konteinerioVidurys: (kaire + desine) / 2,
        plotis: m.width,
        konteinerioPlotis: desine - kaire,
        marginLeft: st.marginLeft,
        marginRight: st.marginRight,
        marginTop: st.marginTop,
    };
}
"""

# Alpine skirtuką perjungia `tab` kintamasis; spaudžiam tikrą mygtuką,
# kad elgtumės taip pat, kaip žmogus.
RODYK = """
(tab) => {
    const m = [...document.querySelectorAll('.home-tab-btn')].find(b =>
        (b.getAttribute('@click') || b.getAttribute('x-on:click') || '')
            .includes(`'${tab}'`));
    if (!m) return false;
    m.click();
    return true;
}
"""

gerai = blogai = 0


def tikrink(pav, ok, papild=''):
    global gerai, blogai
    print(('  OK   ' if ok else '  BLOGAI ') + pav + ('   %s' % (papild,) if papild else ''))
    if ok:
        gerai += 1
    else:
        blogai += 1


with sync_playwright() as p:
    narsykle = p.chromium.launch(executable_path=NARSYKLE)
    for vardas, w, h in PLOCIAI:
        # ignore_https_errors — konteinerio proxy pakeičia CDN sertifikatą,
        # ir be šito Alpine.js neįsikrauna, o skirtukai lieka paslėpti.
        ktx = narsykle.new_context(viewport={'width': w, 'height': h},
                                   ignore_https_errors=True)
        psl = ktx.new_page()
        psl.goto(ADRESAS + '/', wait_until='domcontentloaded')
        # Skirtukus rodo Alpine; kol jis neįsikrovė, x-cloak laiko viską
        # paslėpta ir paspaudimas nieko nedaro. Laukiam jo, ne fiksuoto laiko.
        try:
            psl.wait_for_function('() => window.Alpine && document.querySelector('
                                  '"a.home-tab-visi") && '
                                  'document.querySelector("a.home-tab-visi")'
                                  '.closest("[x-show]") !== null', timeout=15000)
            psl.wait_for_function('() => [...document.querySelectorAll('
                                  '"a.home-tab-visi")].some(a => '
                                  'a.getBoundingClientRect().width > 0)',
                                  timeout=15000)
        except Exception as e:
            print('  !!   Alpine neįsikrovė: %s' % str(e)[:80])
        psl.wait_for_timeout(300)
        print('\n== %s (%dx%d) ==' % (vardas, w, h))
        for tab in SKIRTUKAI:
            # Paslėpto skirtuko matuoti negalima: x-show duoda display:none,
            # o tada visi matmenys yra nuliai ir patikra praeitų tuščiai.
            if not psl.evaluate(RODYK, tab):
                print('  --   %-10s skirtuko nėra (praleidžiam)' % tab)
                continue
            d = None
            for _ in range(20):
                psl.wait_for_timeout(100)
                d = psl.evaluate(MATUOK, tab)
                if d and d['plotis']:
                    break
            if d is None or not d['plotis']:
                tikrink('%-10s matomas' % tab, False, 'mygtukas nematomas')
                continue
            nuokrypis = d['mygtukoVidurys'] - d['konteinerioVidurys']
            tikrink('%-10s centruotas' % tab, abs(nuokrypis) <= RIBA,
                    'nuokrypis %+.1f px (mygtukas %.0f px, konteineris %.0f px, '
                    'margin %s / %s)' % (nuokrypis, d['plotis'],
                                         d['konteinerioPlotis'],
                                         d['marginLeft'], d['marginRight']))
            # Viršutinis tarpas irgi krito kartu su `auto` — be jo mygtukas
            # limpa prie kortelių.
            tikrink('%-10s turi viršutinį tarpą' % tab,
                    float(d['marginTop'].replace('px', '') or 0) > 0,
                    'margin-top %s' % d['marginTop'])
        psl.close()
        ktx.close()
    narsykle.close()

print('\n' + '=' * 60)
print('gerai: %d, nepavyko: %d' % (gerai, blogai))
sys.exit(1 if blogai else 0)
