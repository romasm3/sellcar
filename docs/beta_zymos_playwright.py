# -*- coding: utf-8 -*-
"""
„BETA" ŽENKLIUKAS PRIE LOGOTIPO.

Tikrinam tai, ko akimis nepamatysi patikimai:

  1. ženkliukas yra ir matomas (antraštėje ir porėje);
  2. jis NEUŽLIPA ant mobilaus meniu mygtuko (dėl to ir dedamas
     absoliučiai — kad iš eilutės nieko nestumtų);
  3. antraštės aukštis nepasikeitė, palyginus su puslapiu be ženkliuko;
  4. neatsirado horizontalaus slinkimo siauruose telefonuose;
  5. stilius toks, kokio prašyta (dydis, storis, apvalumas, gradientas);
  6. ekrano skaitytuvui jis nematomas (aria-hidden).

Paleidimas (reikia vietinio serverio 127.0.0.1:8899):
    python docs/beta_zymos_playwright.py
"""
import os
import sys

from playwright.sync_api import sync_playwright

ADRESAS = os.environ.get('ADRESAS', 'http://127.0.0.1:8899')
NARSYKLE = os.environ.get('CHROMIUM',
                          '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')

# Mobilus plotis — siauriausias, kurį antraštė dar turi atlaikyti.
PLOCIAI = (('stalinis', 1280, 900), ('mobilus', 390, 844), ('siauras', 360, 780))

gerai = blogai = 0


def tikrink(pav, ok, papild=''):
    global gerai, blogai
    print(('  OK     ' if ok else '  BLOGAI ') + pav
          + ('   %s' % (papild,) if papild else ''))
    if ok:
        gerai += 1
    else:
        blogai += 1


ZYMA = """
() => {
    const z = [...document.querySelectorAll('.beta-zyma')]
        .find(e => e.getBoundingClientRect().width > 0);
    if (!z) return null;
    const r = z.getBoundingClientRect();
    const s = getComputedStyle(z);
    const a = z.closest('.site-logo');
    const ar = a ? a.getBoundingClientRect() : null;
    return {
        tekstas: z.textContent.trim(),
        ariaHidden: z.getAttribute('aria-hidden'),
        x: r.left, y: r.top, w: r.width, h: r.height, desine: r.right,
        apacia: r.bottom,
        logoDesine: ar ? ar.right : null, logoApacia: ar ? ar.bottom : null,
        logoVirsus: ar ? ar.top : null,
        logoPos: a ? getComputedStyle(a).position : null,
        fontSize: s.fontSize, fontWeight: s.fontWeight,
        letterSpacing: s.letterSpacing, transform: s.textTransform,
        radius: s.borderRadius, spalva: s.color,
        fonas: s.backgroundImage, pozicija: s.position,
    };
}
"""

# Mygtukai, ant kurių ženkliukas neturi užlipti.
KLIUTYS = """
() => [...document.querySelectorAll('button, a')]
    .filter(e => {
        const r = e.getBoundingClientRect();
        if (!r.width || !r.height) return false;
        if (r.top > 120) return false;            // tik antraštės eilutė
        return !e.closest('.site-logo');
    })
    .map(e => {
        const r = e.getBoundingClientRect();
        return {kas: (e.className || '').toString().slice(0, 40) ||
                     e.tagName, x: r.left, y: r.top,
                desine: r.right, apacia: r.bottom};
    })
"""

with sync_playwright() as p:
    narsykle = p.chromium.launch(executable_path=NARSYKLE)
    for vardas, w, h in PLOCIAI:
        ktx = narsykle.new_context(viewport={'width': w, 'height': h},
                                   ignore_https_errors=True)
        psl = ktx.new_page()
        psl.goto(ADRESAS + '/', wait_until='domcontentloaded')
        # Fiksuoto laukimo neužtenka: kol Alpine ir šriftai neįsikrovę,
        # antraštė dar persidėlioja, ir matavimai išeina skirtingi.
        # Laukiam, kol ženkliuko padėtis nustoja keistis.
        psl.wait_for_timeout(600)
        pr = None
        for _ in range(30):
            dab = psl.evaluate(
                '() => { const z = [...document.querySelectorAll(".beta-zyma")]'
                '.find(e => e.getBoundingClientRect().width > 0);'
                ' if (!z) return null; const r = z.getBoundingClientRect();'
                ' return [r.left, r.top].join(","); }')
            if dab is not None and dab == pr:
                break
            pr = dab
            psl.wait_for_timeout(200)
        print('\n== %s (%dx%d) ==' % (vardas, w, h))

        d = psl.evaluate(ZYMA)
        if d is None:
            tikrink('ženkliukas matomas', False, 'nerastas nė vienas')
            psl.close(); ktx.close()
            continue

        tikrink('ženkliukas matomas', d['w'] > 0 and d['h'] > 0,
                '%.0fx%.0f px' % (d['w'], d['h']))
        tikrink('tekstas', d['tekstas'].lower() == 'beta', repr(d['tekstas']))
        tikrink('aria-hidden="true"', d['ariaHidden'] == 'true', d['ariaHidden'])
        tikrink('logotipo konteineris position: relative',
                d['logoPos'] == 'relative', d['logoPos'])
        tikrink('ženkliukas position: absolute',
                d['pozicija'] == 'absolute', d['pozicija'])
        # „Dešinėje apačioje" — dešinysis kraštas už logotipo, o vidurys
        # apatinėje jo pusėje. Kyšoti žemiau NEBŪTINA: ≤400 px
        # sąmoningai laikom ženkliuką dėžės viduje, nes po juo iškart
        # prasideda „Įkelti".
        vidurys = d['y'] + d['h'] / 2.0
        logoVidurys = (d['logoVirsus'] + d['logoApacia']) / 2.0
        tikrink('dešinėje apačioje',
                d['desine'] >= d['logoDesine'] - 1 and vidurys > logoVidurys,
                'dešinė %.0f vs logo %.0f; vidurys %.0f vs %.0f'
                % (d['desine'], d['logoDesine'], vidurys, logoVidurys))

        # ── Kiek ženkliukas kabo žemiau logotipo ────────────────────
        # Tai svarbiausia patikra, ir ji NEPRIKLAUSO nuo to, kas tuo metu
        # jau atsirado eilute žemiau. Prie `bottom: -12px` ženkliukas
        # nusileisdavo 12 px ir užlipdavo: 1280 px ant antrinės
        # navigacijos (tarpas 8 px), 360 px ant „Įkelti", kai antraštė
        # persilaužia (tarpas 0 px). Kabėjimo riba — 7 px.
        kabo = d['apacia'] - d['logoApacia']
        tikrink('kabo ne daugiau kaip 7 px žemiau logotipo', kabo <= 7,
                '%.0f px' % kabo)

        # ── Ar neužlipa ant antraštės mygtukų ────────────────────────
        kliutys = psl.evaluate(KLIUTYS)
        def kertasi(a, b):
            return not (a['desine'] <= b['x'] or b['desine'] <= a['x']
                        or a['apacia'] <= b['y'] or b['apacia'] <= a['y'])
        uzlipo = [k for k in kliutys if kertasi(d, k)]
        tikrink('neužlipa ant antraštės mygtukų', not uzlipo,
                ('žyma [%.0f,%.0f–%.0f,%.0f] kertasi su %s'
                 % (d['x'], d['y'], d['desine'], d['apacia'],
                    [(k['kas'], round(k['x']), round(k['y'])) for k in uzlipo[:2]]))
                if uzlipo else '%d mygtukų patikrinta' % len(kliutys))

        # ── Nepablogina horizontalaus slinkimo ──────────────────────
        # Siauruose telefonuose antraštė ir be ženkliuko išeina ~13 px už
        # krašto (sena bėda, žr. base.html komentarus). Tad tikrinam ne
        # „nulis", o kad ženkliukas NIEKO NEPRIDEDA.
        MAT = ('() => document.documentElement.scrollWidth - '
               'document.documentElement.clientWidth')
        su = psl.evaluate(MAT)
        psl.add_style_tag(content='.beta-zyma { display: none !important; }')
        psl.wait_for_timeout(150)
        be = psl.evaluate(MAT)
        psl.evaluate('() => [...document.querySelectorAll("style")].pop().remove()')
        psl.wait_for_timeout(150)
        tikrink('ženkliukas nepablogina slinkimo', su <= be,
                'su %d px, be %d px' % (su, be))

        if vardas == 'stalinis':
            tikrink('font-size 8.5px', d['fontSize'] == '8.5px', d['fontSize'])
            tikrink('font-weight 700', d['fontWeight'] == '700', d['fontWeight'])
            tikrink('letter-spacing .6px', d['letterSpacing'] == '0.6px',
                    d['letterSpacing'])
            tikrink('DIDŽIOSIOMIS', d['transform'] == 'uppercase', d['transform'])
            tikrink('apvalus (999px)', '999px' in d['radius'], d['radius'])
            tikrink('baltas tekstas', d['spalva'] == 'rgb(255, 255, 255)',
                    d['spalva'])
            tikrink('gradientas raudona→oranžinė',
                    'linear-gradient' in d['fonas']
                    and '239, 68, 68' in d['fonas']
                    and '249, 115, 22' in d['fonas'], d['fonas'][:60])

            # Antraštės aukštis neturi pasikeisti — ženkliukas absoliutus.
            auks = psl.evaluate(
                '() => { const e = document.querySelector(".hdr-eile");'
                ' return e ? e.getBoundingClientRect().height : null; }')
            psl.add_style_tag(content='.beta-zyma { display: none !important; }')
            psl.wait_for_timeout(150)
            be = psl.evaluate(
                '() => { const e = document.querySelector(".hdr-eile");'
                ' return e ? e.getBoundingClientRect().height : null; }')
            tikrink('antraštės aukštis nepakito',
                    auks is None or abs((auks or 0) - (be or 0)) < 0.5,
                    'su %.1f px, be %.1f px' % (auks or 0, be or 0))

        psl.close()
        ktx.close()

    # ── Porė ────────────────────────────────────────────────────────
    print('\n== porė ==')
    ktx = narsykle.new_context(viewport={'width': 1280, 'height': 900},
                               ignore_https_errors=True)
    psl = ktx.new_page()
    psl.goto(ADRESAS + '/', wait_until='domcontentloaded')
    psl.wait_for_timeout(1200)
    kiek = psl.evaluate('() => document.querySelectorAll(".beta-zyma").length')
    tikrink('ženkliukų puslapyje yra ir antraštėje, ir porėje', kiek >= 2, kiek)
    psl.close()
    ktx.close()
    narsykle.close()

print('\n' + '=' * 60)
print('gerai: %d, nepavyko: %d' % (gerai, blogai))
sys.exit(1 if blogai else 0)
