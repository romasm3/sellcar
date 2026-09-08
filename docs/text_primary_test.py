# -*- coding: utf-8 -*-
"""`.text-primary` spalva — kad kaina ir ikonos neatrodytų išjungtos.

Klasė buvo perrašyta į --accent-grad-from (#9ca3af) — šviesiausią
gradiento tašką, skirtą fonams. Tekstui jis sutampa su --text-disabled,
todėl skelbimo kaina atrodė pilka kaip neaktyvus laukas.

Tikrinam: klasė ima --accent, gradiento kintamųjų reikšmės nepaliestos,
kontrastas ant balto fono pakankamas, ir kad tekstinės taisyklės
nebenaudoja gradiento kintamųjų.

Paleidimas:  python docs/text_primary_test.py
"""
import io, os, re, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSS = io.open(os.path.join(BASE, 'static/css/style.css'), encoding='utf-8').read()
BASE_HTML = io.open(os.path.join(BASE, 'templates/base.html'), encoding='utf-8').read()

KLAIDOS = []


def tikrinu(pav, salyga, papild=''):
    if salyga:
        print(u'  ✓ %s' % pav)
    else:
        print(u'  ✗ %s %s' % (pav, papild))
        KLAIDOS.append(pav)


def taisykle(selektorius):
    """Paskutinė (laiminti) selektoriaus taisyklė iš style.css."""
    rasta = re.findall(re.escape(selektorius) + r'\s*(?:,[^{]*)?\{([^}]*)\}', CSS)
    return rasta[-1] if rasta else ''


def spalva(kintamasis):
    m = re.search(re.escape(kintamasis) + r':\s*([^;]+);', BASE_HTML)
    return m.group(1).strip() if m else ''


def hex2rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def santykis(fg, bg):
    """WCAG kontrasto santykis."""
    def L(c):
        s = []
        for v in c:
            v = v / 255.0
            s.append(v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4)
        return 0.2126 * s[0] + 0.7152 * s[1] + 0.0722 * s[2]
    a, b = L(fg), L(bg)
    if a < b:
        a, b = b, a
    return (a + 0.05) / (b + 0.05)


print(u'\n== 1. Klasė ima teisingą kintamąjį ==')
t = taisykle('.text-primary')
tikrinu(u'.text-primary → var(--accent)', 'var(--accent)' in t, t.strip())
tikrinu(u'nebeima --accent-grad-from', 'accent-grad-from' not in t, t.strip())
h = taisykle(r'.hover\:text-primary:hover')
tikrinu(u'hover → var(--accent-hover)', 'var(--accent-hover)' in h, h.strip())
tikrinu(u'hover nebeima --accent-grad-to', 'accent-grad-to' not in h, h.strip())

print(u'\n== 2. Gradiento kintamųjų reikšmės NEPALIESTOS ==')
tikrinu(u'--accent-grad-from = #9ca3af', spalva('--accent-grad-from') == '#9ca3af',
        spalva('--accent-grad-from'))
tikrinu(u'--accent-grad-to = #6b7280', spalva('--accent-grad-to') == '#6b7280',
        spalva('--accent-grad-to'))
tikrinu(u'gradientai fonams tebenaudoja --accent-grad-from',
        'linear-gradient(135deg, var(--accent-grad-from)' in CSS)

print(u'\n== 3. Spalva nebesutampa su „išjungta" ==')
akcentas = '#374151'          # --accent-rgb: 55 65 81
isjungta = spalva('--text-disabled')
tikrinu(u'--accent (#374151) ≠ --text-disabled (%s)' % isjungta,
        akcentas.lower() != isjungta.lower())
tikrinu(u'senoji spalva sutapdavo su --text-disabled',
        spalva('--accent-grad-from').lower() == isjungta.lower(),
        u'jei nesutampa — klaidos aprašymas paseno')

print(u'\n== 4. Kontrastas ant balto fono ==')
naujas = santykis(hex2rgb(akcentas), (255, 255, 255))
senas = santykis(hex2rgb('#9ca3af'), (255, 255, 255))
tikrinu(u'naujas ≥ 4.5 (WCAG AA tekstui): %.2f' % naujas, naujas >= 4.5)
tikrinu(u'senasis buvo per silpnas: %.2f' % senas, senas < 4.5)

print(u'\n== 5. Gradientams atskiros klasės neprireikė ==')
sablonai = []
for saknis, _, failai in os.walk(os.path.join(BASE, 'templates')):
    for f in failai:
        if f.endswith('.html'):
            sablonai.append(io.open(os.path.join(saknis, f), encoding='utf-8').read())
visi = '\n'.join(sablonai)
tikrinu(u'niekur nėra gradientinio teksto (bg-clip-text)', 'bg-clip-text' not in visi)
tikrinu(u'niekur nėra text-transparent', 'text-transparent' not in visi)

print('')
if KLAIDOS:
    print(u'NEPRAĖJO: %d' % len(KLAIDOS))
    sys.exit(1)
print(u'VISI TESTAI PRAĖJO')
