# -*- coding: utf-8 -*-
"""
FUZZY EILUČIŲ TVARKYMAS — ką priimti, o ką grąžinti vertimui.

Fuzzy eilutė gali būti dviejų visiškai skirtingų rūšių, ir iš pažiūros
jos vienodos:

  A. msgmerge PERRAŠYMAS. msgid pasikeitė tik rašyba („Private seller" →
     „Private Seller"), vertimas liko teisingas. Tokią galima priimti.

  B. msgmerge PRISKYRIMAS SVETIMAM msgid'ui. Vertimas atkeliavo nuo
     KITOS eilutės:
         Rating              → „Auflistung"   (buvo „Listing")
         Rating Count        → „Herkunftsland" (buvo „Origin Country")
         Email Notifications → „Änderung"     (buvo „Modification")
     Tokios priimti NEGALIMA: į svetainę pateks matomai klaidingas
     tekstas. Būtent dėl šitų 2026-08-20 audite rasta 57 klaidos, ir
     būtent dėl jų projekto makemessages leidžia msgmerge su
     `--no-fuzzy-matching`.

Kintamųjų sutapimas (%(vardas)s, {n}) yra BŪTINA, bet NEPAKANKAMA
sąlyga: „Rating" ir „Listing" abu be kintamųjų, o vertimas vis tiek
svetimas. Todėl žiūrim ir į `#| msgid` (ankstesnį msgid), kurį msgmerge
palieka pats.

    python docs/fuzzy_tvarkymas.py --ataskaita          # tik suskaičiuoja
    python docs/fuzzy_tvarkymas.py --priimk de fr vi ar # nuima fuzzy nuo A
    python docs/fuzzy_tvarkymas.py --isvalyk de fr ...  # B ištuština

`--isvalyk` niekam nekenkia: tuščias msgstr rodo msgid — lygiai tą patį,
ką vartotojas mato ir dabar (fuzzy į .mo nepatenka). Užtat tokią eilutę
docs/vertimo_uzpildymas.py vėl paims ir išvers tvarkingai.
"""
import os
import re
import sys
import unicodedata

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

try:
    import polib
except ImportError:
    sys.exit('Reikia polib: pip install polib')

PROC = re.compile(r'%\([^)]*\)[a-zA-Z]?|%[a-zA-Z%]')
SKLIAUSTAI = re.compile(r'\{[^{}]*\}')


def kintamieji(tekstas):
    return (sorted(PROC.findall(tekstas or ''))
            + sorted(SKLIAUSTAI.findall(tekstas or '')))


def pagrindas(tekstas):
    """Tekstas be rašybos skirtumų — didžiųjų, skyrybos, tarpų, kirčių."""
    t = unicodedata.normalize('NFKD', (tekstas or '').lower())
    t = ''.join(z for z in t if not unicodedata.combining(z))
    return re.sub(r'[^a-z0-9%(){}]+', '', t)


def po_kelias(kalba):
    return os.path.join(BASE, 'locale', kalba, 'LC_MESSAGES', 'django.po')


def kalbos():
    saknis = os.path.join(BASE, 'locale')
    return sorted(k for k in os.listdir(saknis) if os.path.exists(po_kelias(k)))


def rusiuok(po):
    """(priimtini, svetimi, sulauzyti, neperziureti) — fuzzy pagal rūšį.

    „Neperžiūrėti" yra atskira rūšis ir jos NIEKADA nepriimam: tai
    mašininio užpildymo eilutės, kurias docs/vertimo_uzpildymas.py
    sąmoningai pažymi fuzzy, kad žmogus pirma peržiūrėtų. Jos neturi
    `#| msgid` — msgmerge jų neliečia. Anksčiau jos pakliūdavo į
    „priimtinus" ir vienu paleidimu būtų atsidūrusios svetainėje
    neperžiūrėtos.
    """
    priimtini, svetimi, sulauzyti, neperziureti = [], [], [], []
    for e in po:
        if e.obsolete or 'fuzzy' not in e.flags:
            continue
        if not e.msgstr and not e.msgstr_plural:
            continue                      # tuščia fuzzy — nieko netaisom
        if kintamieji(e.msgid) != kintamieji(e.msgstr):
            sulauzyti.append(e)           # kintamieji nesutampa
        elif not e.previous_msgid:
            neperziureti.append(e)        # mašinos darbas, laukia žmogaus
        elif pagrindas(e.previous_msgid) != pagrindas(e.msgid):
            svetimi.append(e)             # vertimas nuo kitos eilutės
        else:
            priimtini.append(e)
    return priimtini, svetimi, sulauzyti, neperziureti


def main():
    veiksmas = ('--priimk' if '--priimk' in sys.argv else
                '--isvalyk' if '--isvalyk' in sys.argv else '--ataskaita')
    nurodytos = [a for a in sys.argv[1:] if not a.startswith('--')]
    sarasas = nurodytos or kalbos()

    print('%-8s %6s %10s %9s %11s %13s'
          % ('kalba', 'fuzzy', 'priimtini', 'svetimi', 'kintamieji',
             'neperžiūrėti'))
    pavyzdziai = []
    for kalba in sarasas:
        kelias = po_kelias(kalba)
        if not os.path.exists(kelias):
            print('%-8s — nėra katalogo' % kalba)
            continue
        po = polib.pofile(kelias)
        priimtini, svetimi, sulauzyti, neperziureti = rusiuok(po)
        print('%-8s %6d %10d %9d %11d %13d'
              % (kalba, len(priimtini) + len(svetimi) + len(sulauzyti)
                 + len(neperziureti),
                 len(priimtini), len(svetimi), len(sulauzyti),
                 len(neperziureti)))

        if not pavyzdziai:
            for e in svetimi[:5]:
                pavyzdziai.append('  %-30s ← buvo %-24s vertimas: %s'
                                  % (e.msgid[:30], (e.previous_msgid or '')[:24],
                                     (e.msgstr or '')[:24]))

        if veiksmas == '--ataskaita':
            continue

        if veiksmas == '--priimk':
            for e in priimtini:
                e.flags = [f for f in e.flags if f != 'fuzzy']
                e.previous_msgid = None
            pakeista = len(priimtini)
        else:                              # --isvalyk
            for e in svetimi + sulauzyti:
                e.msgstr = ''
                if e.msgstr_plural:
                    e.msgstr_plural = {i: '' for i in e.msgstr_plural}
                e.flags = [f for f in e.flags if f != 'fuzzy']
                e.previous_msgid = None
            pakeista = len(svetimi) + len(sulauzyti)
        po.save(kelias)
        po.save_as_mofile(kelias[:-3] + '.mo')
        print('         → pakeista %d, įrašyta' % pakeista)

    if pavyzdziai:
        print('\nKodėl „svetimi" nepriimami (pavyzdžiai):')
        print('\n'.join(pavyzdziai))
    return 0


if __name__ == '__main__':
    sys.exit(main())
