# -*- coding: utf-8 -*-
"""Kainos vieta ir dydis skelbimo šoninėje juostoje.

Kaina buvo įstrigusi tarp galios ir vietos, nors tai antra pagal svarbą
informacija. Nauja tvarka: metai → pavadinimas → KAINA → vieta →
skiriamoji linija → kuras/rida/galia → telefonas → veiksmai → statistika.

Tikrinam ir eiliškumą šablone, ir tikrą dydį naršyklėje (38 px
darbalaukyje, 30 px siaurame ekrane) — pastarąjį per Chromium, tad
matuojamas apskaičiuotas stilius, ne CSS tekstas.

Paleidimas:  python docs/kainos_sonine_test.py
"""
import io, os, re, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAB = io.open(os.path.join(BASE, 'templates/listings/listing_detail.html'),
              encoding='utf-8').read()

KLAIDOS = []


def tikrinu(pav, salyga, papild=''):
    if salyga:
        print(u'  ✓ %s' % pav)
    else:
        print(u'  ✗ %s %s' % (pav, papild))
        KLAIDOS.append(pav)


# Šoninė juosta — nuo „Sidebar" komentaro iki statistikos
i = SAB.index('<!-- Sidebar (same for all categories')
SONINE = SAB[i:i + 14000]


def vieta(zyme):
    return SONINE.find(zyme)


print(u'\n== 1. Eiliškumas šoninėje juostoje ==')
metai = vieta('{{ listing.year }}')
pavad = vieta('<h2 class="text-xl font-bold text-gray-900')
kaina = vieta('<p class="ap-kaina">')
miestas = vieta('{{ listing.city|vietovardis }}')
linija = vieta('<hr class="ap-skirtukas">')
kuras = vieta('{{ listing.fuel_type.name|tdb }}')
rida = vieta('data-unit-show="mileage"')
galia = vieta('data-unit-show="power"')
telefonas = vieta('class="ap-phone"')
veiksmai = vieta('shareModal')
statistika = vieta('{% trans "Listing ID" %}')

for pav, p in ((u'metai', metai), (u'pavadinimas', pavad), (u'kaina', kaina),
               (u'vieta', miestas), (u'linija', linija), (u'kuras', kuras),
               (u'rida', rida), (u'galia', galia), (u'telefonas', telefonas),
               (u'veiksmai', veiksmai), (u'statistika', statistika)):
    if p < 0:
        tikrinu(u'rasta: %s' % pav, False, u'NERASTA')

eile = [metai, pavad, kaina, miestas, linija, kuras, rida, galia,
        telefonas, veiksmai, statistika]
tikrinu(u'metai → pavadinimas → KAINA → vieta → linija → '
        u'kuras → rida → galia → telefonas → veiksmai → statistika',
        all(a >= 0 and a < b for a, b in zip(eile, eile[1:])), eile)
tikrinu(u'kaina PRIEŠ kurą (buvo po galios)', 0 <= kaina < kuras)
tikrinu(u'kaina iškart po pavadinimo', 0 <= pavad < kaina)

print(u'\n== 2. Viena skiriamoji linija, po vietos ==')
tikrinu(u'linija po vietos', 0 <= miestas < linija)
tikrinu(u'linija prieš specifikacijas', 0 <= linija < kuras)
tikrinu(u'šoninėje tik viena <hr>', SONINE.count('<hr') == 1,
        u'rasta %d' % SONINE.count('<hr'))
tikrinu(u'linija 1px var(--border)',
        re.search(r'\.ap-skirtukas\s*\{[^}]*border-top:\s*1px solid var\(--border\)', SAB)
        is not None)

print(u'\n== 3. Kainos stilius ==')
st = re.search(r'\.ap-kaina\s*\{([^}]*)\}', SAB)
st = st.group(1) if st else ''
tikrinu(u'font-weight 700', 'font-weight: 700' in st, st.strip())
tikrinu(u'color var(--text)', 'color: var(--text)' in st, st.strip())
tikrinu(u'letter-spacing -0.02em', 'letter-spacing: -0.02em' in st, st.strip())
tikrinu(u'nebenaudoja .text-primary',
        'text-3xl font-bold text-primary' not in SONINE)

print(u'\n== 4. Kiti šoninės juostos elementai nepaliesti ==')
tikrinu(u'telefono mygtukas .ap-phone vietoje', telefonas > 0)
tikrinu(u'Bendrinti · Išsaugoti · Pranešti vietoje',
        'shareModal' in SONINE and 'save_listing' in SONINE and 'reportModal' in SONINE)
tikrinu(u'statistika (#numeris, išsaugota, peržiūros) vietoje',
        'Listing ID' in SONINE and 'Views' in SONINE)
tikrinu(u'specifikacijų turinys nepakeistos',
        'data-unit-show="mileage"' in SONINE and 'data-unit-show="power"' in SONINE
        and 'get_body_type_display' in SONINE)
tikrinu(u'eksporto kaina ir „derinama" liko kainos bloke',
        'export_price' in SONINE and 'Kaina derinama' in SONINE)

print(u'\n== 5. Tikras dydis naršyklėje ==')
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print(u'  – playwright neįdiegtas, matavimas praleistas')
else:
    stilius = re.search(r'\.ap-kaina\s*\{[^}]*\}', SAB).group(0)
    media = re.search(r'@media \(min-width: 1024px\) \{ \.ap-kaina[^}]*\} \}', SAB).group(0)
    puslapis = (u'<style>:root{--text:#111827}body{margin:0}%s %s</style>'
                u'<p class="ap-kaina">18 450 €</p>' % (stilius, media))
    with sync_playwright() as pw:
        # Konteineryje Chromium guli /opt/pw-browsers (PLAYWRIGHT_BROWSERS_PATH),
        # o pip versija gali tiketis kito numerio — nurodom keliu.
        kelias = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
        nars = (pw.chromium.launch(executable_path=kelias)
                if os.path.exists(kelias) else pw.chromium.launch())
        for pav, plotis, laukiama in ((u'darbalaukis 1280px', 1280, 38),
                                      (u'planšetė 1024px', 1024, 38),
                                      (u'telefonas 360px', 360, 30)):
            psl = nars.new_page(viewport={'width': plotis, 'height': 800})
            psl.set_content(puslapis)
            dydis = psl.evaluate(
                "getComputedStyle(document.querySelector('.ap-kaina')).fontSize")
            svoris = psl.evaluate(
                "getComputedStyle(document.querySelector('.ap-kaina')).fontWeight")
            spalva = psl.evaluate(
                "getComputedStyle(document.querySelector('.ap-kaina')).color")
            plotis_tekst = psl.evaluate(
                "document.querySelector('.ap-kaina').getBoundingClientRect().width")
            tikrinu(u'%s: %d px' % (pav, laukiama), dydis == '%dpx' % laukiama, dydis)
            if plotis == 360:
                tikrinu(u'telefone kaina telpa į 360 px',
                        plotis_tekst <= 360, u'%.0f px' % plotis_tekst)
                tikrinu(u'svoris 700', svoris == '700', svoris)
                tikrinu(u'spalva var(--text) = #111827',
                        spalva == 'rgb(17, 24, 39)', spalva)
            psl.close()
        nars.close()

print('')
if KLAIDOS:
    print(u'NEPRAĖJO: %d' % len(KLAIDOS))
    sys.exit(1)
print(u'VISI TESTAI PRAĖJO')
