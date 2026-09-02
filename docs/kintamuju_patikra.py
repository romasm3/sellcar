# -*- coding: utf-8 -*-
"""
Ar vertimas nesulaužė kintamųjų ir HTML žymių?

Mašininis vertimas mielai išverčia patį kintamojo vardą:
`Found %(count)s listings` → `Найдено %(количество) объявлений`. Django
tokį atvejį pagauna ir grįžta prie angliško originalo, tad vartotojas
vertimo NEMATO, o .po faile jis atrodo esantis. `msgfmt --check` tokį
failą laiko klaidingu.

    python docs/kintamuju_patikra.py            # tik parodo
    python docs/kintamuju_patikra.py --zymek    # sulaužytas pažymi fuzzy
    python docs/kintamuju_patikra.py --sarasas ru > /tmp/taisyti-ru.txt

`--zymek` nieko netrina: fuzzy eilutė nekompiliuojama į .mo, tad
vartotojui rodoma lygiai tas pat, kas ir dabar (angliškas originalas),
tik .po faile matyti, kad eilutė laukia peržiūros.
"""
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KALBOS = ('ru', 'en', 'lt')

try:
    import polib
except ImportError:
    sys.exit('Reikia polib: pip install polib')

# %(vardas)s, %s, %d, %% — Python formatavimas
PROC = re.compile(r'%\([^)]*\)[a-zA-Z]?|%[a-zA-Z%]|%')
# {vardas} — JavaScript pusėje keičiami šablonai
SKLIAUSTAI = re.compile(r'\{[^{}]*\}')
ZYME = re.compile(r'</?([a-zA-Z][a-zA-Z0-9]*)[^>]*>')


def kintamieji(tekstas):
    return sorted(PROC.findall(tekstas or '')) + sorted(SKLIAUSTAI.findall(tekstas or ''))


def procentai(tekstas):
    return sorted(PROC.findall(tekstas or ''))


def zymes(tekstas):
    return sorted(ZYME.findall(tekstas or ''))


def nplurals(po):
    m = re.search(r'nplurals\s*=\s*(\d+)', po.metadata.get('Plural-Forms', ''))
    return int(m.group(1)) if m else 2


def bedos(kelias):
    """[(eilute, msgid, msgstr, priezastis)] — kas neatitinka originalo."""
    po = polib.pofile(kelias)
    n = nplurals(po)
    rasta = []
    for e in po:
        # Fuzzy eilutė į .mo nepatenka — vartotojas jos nemato, tad ir
        # sulaužyti kintamieji joje niekam nekenkia.
        if e.obsolete or 'fuzzy' in e.flags:
            continue
        if e.msgid_plural:
            uzpildytos = [v for v in (e.msgstr_plural or {}).values() if v]
            if not uzpildytos:
                continue
            if len(e.msgstr_plural) != n:
                rasta.append((e, e.msgid, ' | '.join(uzpildytos),
                              'daugiskaita: %d formos vietoj %d' %
                              (len(e.msgstr_plural), n)))
                continue
            laukiami = set(procentai(e.msgid)) | set(procentai(e.msgid_plural))
            for v in uzpildytos:
                svetimi = [p for p in procentai(v) if p not in laukiami]
                if svetimi:
                    rasta.append((e, e.msgid, v,
                                  'kintamieji: originale nėra %s' % svetimi))
                    break
            continue
        if not e.msgstr:
            continue
        # Lūžta tik tada, kai vertime yra direktyva, kurios originale nėra:
        # `%(количество)` be konversijos raidės arba išverstas vardas kelia
        # ValueError/KeyError, ir Django grįžta prie angliško originalo.
        laukiami = set(procentai(e.msgid))
        svetimi = [p for p in procentai(e.msgstr) if p not in laukiami]
        if svetimi:
            rasta.append((e, e.msgid, e.msgstr,
                          'kintamieji: originale nėra %s' % svetimi))
    return po, rasta


def ispejimai(kelias):
    """Ne lūžis, bet vertas akies: dingęs kintamasis ar HTML žymė."""
    po = polib.pofile(kelias)
    rasta = []
    for e in po:
        if e.obsolete or not e.msgstr or 'fuzzy' in e.flags:
            continue
        laukiami = set(procentai(e.msgid))
        if [p for p in procentai(e.msgstr) if p not in laukiami]:
            continue                       # jau suskaičiuota kaip lūžis
        dingę = [p for p in laukiami if p not in procentai(e.msgstr)]
        if dingę:
            rasta.append((e, e.msgid, e.msgstr, 'dingo kintamasis %s' % dingę))
            continue
        za, zb = zymes(e.msgid), zymes(e.msgstr)
        if za != zb:
            rasta.append((e, e.msgid, e.msgstr, 'HTML žymės: %s vs %s' % (za, zb)))
    return rasta


def main():
    zymek = '--zymek' in sys.argv
    sarasas = None
    if '--sarasas' in sys.argv:
        sarasas = sys.argv[sys.argv.index('--sarasas') + 1]

    viso = 0
    for kalba in ([sarasas] if sarasas else KALBOS):
        kelias = os.path.join(BASE, 'locale', kalba, 'LC_MESSAGES', 'django.po')
        if not os.path.exists(kelias):
            continue
        po, rasta = bedos(kelias)
        viso += len(rasta)
        if sarasas:
            print('# %s — %d eilutės su sulaužytais kintamaisiais' % (kalba, len(rasta)))
            print('# Kairėje originalas, dešinėje dabartinis (blogas) variantas.\n')
            for e, mid, mstr, kodel in rasta:
                print('msgid : %s' % mid.replace('\n', '\\n'))
                print('dabar : %s' % mstr.replace('\n', '\\n'))
                print('bėda  : %s' % kodel)
                print('vieta : %s' % ', '.join('%s:%s' % v for v in e.occurrences[:2]))
                print()
            continue
        print('%s: %d sulaužytų iš %d' % (kalba, len(rasta), len(po)))
        for e, mid, mstr, kodel in rasta[:8]:
            print('   %-58s  %s' % (mid[:58].replace('\n', ' '), kodel))
        if len(rasta) > 8:
            print('   … dar %d' % (len(rasta) - 8))
        if zymek and rasta:
            for e, _m, _s, _k in rasta:
                if 'fuzzy' not in e.flags:
                    e.flags.append('fuzzy')
            po.save(kelias)
            po.save_as_mofile(kelias[:-3] + '.mo')
            print('   pažymėta fuzzy: %d (į .mo nebepatenka, rodomas originalas)'
                  % len(rasta))
    return 1 if (viso and not zymek and not sarasas) else 0


if __name__ == '__main__':
    sys.exit(main())
