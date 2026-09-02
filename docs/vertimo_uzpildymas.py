# -*- coding: utf-8 -*-
"""
VIENKARTINIS tuščių msgstr užpildymas Google Translate'u.

Keturios apsaugos, dėl kurių susitarta:

  1. Liečiam TIK tuščias eilutes. Eilutė, kuri jau turi vertimą,
     nepaliečiama — nė tada, kai ji pažymėta fuzzy. docs/terminai.md
     visada viršesnis: jo terminai praleidžiami net jei tušti.
  2. Kintamieji (%(n)s, %s, {vardas}) ir HTML žymės po vertimo
     tikrinami. Nesutampa — msgstr lieka TUŠČIAS, o eilutė patenka į
     sąrašą žmogui (docs/vertimo_uzpildymas_ataskaita.txt).
  3. Daugiskaitos eilutės (msgid_plural) neverčiamos visai: rusiškai
     šitas katalogas reikalauja KETURIŲ formų, mašina duoda vieną.
     Surašomos atskirai.
  4. Pabaigoje msgfmt --check. Failas įrašomas tik jei patikra švari;
     kitaip niekas nekeičiama ir rodoma klaida.

Visos naujos eilutės pažymimos `#, fuzzy` — taip jos NEPATENKA į .mo ir
vartotojui nerodomos, kol žmogus neperžiūrėjo. Tokia ir buvo mintis.

Raktas: GOOGLE_TRANSLATE_API_KEY (arba GOOGLE_MAPS_API_KEY) aplinkoje.

    python docs/vertimo_uzpildymas.py --bandymas       # kiek ir ko yra
    python docs/vertimo_uzpildymas.py ru en            # užpildo
"""
import os
import re
import subprocess
import sys
import tempfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, 'docs'))

API_URL = 'https://translation.googleapis.com/language/translate/v2'
PORCIJA = 64          # kiek eilučių vienam kreipiniui (Google leidžia 128)
LAIKAS = 30

try:
    import polib
except ImportError:
    sys.exit('Reikia polib: pip install polib')

import kintamuju_patikra as kp
import terminai_taikyti as tt

# Kintamieji, kuriuos prieš vertimą paslepiam už neutralaus ženklo.
SAUGOMI = re.compile(r'%\([^)]*\)[a-zA-Z]|%[a-zA-Z%]|\{[^{}]*\}')


def raktas():
    for vardas in ('GOOGLE_TRANSLATE_API_KEY', 'GOOGLE_MAPS_API_KEY'):
        v = (os.environ.get(vardas) or '').strip()
        if v:
            return v
    return ''


def paslepk(tekstas):
    """„Rasta %(n)s" → („Rasta ⟦0⟧", ['%(n)s'])."""
    dalys = []

    def keisk(m):
        dalys.append(m.group(0))
        return '⟦%d⟧' % (len(dalys) - 1)

    return SAUGOMI.sub(keisk, tekstas), dalys


def atskleisk(tekstas, dalys):
    for i, d in enumerate(dalys):
        # Google kartais įterpia tarpų aplink ženklą arba pakeičia
        # skliaustų kryptį — priimam abu pavidalus.
        tekstas = re.sub(r'⟦\s*%d\s*⟧' % i, lambda _m, d=d: d, tekstas)
    return tekstas


def versk(tekstai, kalba, api):
    """[str] → [str] per Google v2. Skirsto porcijomis."""
    import requests
    isversta = []
    for i in range(0, len(tekstai), PORCIJA):
        porcija = tekstai[i:i + PORCIJA]
        r = requests.post(API_URL, params={'key': api}, timeout=LAIKAS, data=[
            ('q', t) for t in porcija
        ] + [('target', kalba), ('source', 'en'), ('format', 'text')])
        if r.status_code != 200:
            raise SystemExit('Google atsakė %s: %s' % (r.status_code, r.text[:300]))
        isversta += [d['translatedText'] for d in r.json()['data']['translations']]
        print('   … %d/%d' % (min(i + PORCIJA, len(tekstai)), len(tekstai)))
    return isversta


def kandidatai(po, zodynas):
    """Eilutės, kurias VALIA pildyti, ir tos, kurios paliekamos."""
    pildom, daugiskaitos = [], []
    for e in po:
        if e.obsolete:
            continue
        if e.msgid_plural:
            if not any((e.msgstr_plural or {}).values()):
                daugiskaitos.append(e)
            continue
        if e.msgstr:
            continue                       # 1 apsauga: turinčių neliečiam
        if tt.raktas(e.msgid) in zodynas:
            continue                       # terminai.md viršesnis
        if not re.search(r'[A-Za-zĄ-Žą-ž]', e.msgid):
            continue                       # vien skaičiai ar ženklai
        pildom.append(e)
    return pildom, daugiskaitos


def isaugok_jei_svaru(po, kelias):
    """4 apsauga: įrašom tik jei msgfmt --check švarus."""
    laikinas = tempfile.NamedTemporaryFile(suffix='.po', delete=False)
    laikinas.close()
    po.save(laikinas.name)
    r = subprocess.run(['msgfmt', '--check', '-o', os.devnull, laikinas.name],
                       capture_output=True, text=True)
    klaidos = [x for x in r.stderr.splitlines() if 'warning: header field' not in x]
    if r.returncode != 0:
        os.unlink(laikinas.name)
        return False, '\n'.join(klaidos)
    os.replace(laikinas.name, kelias)
    po = polib.pofile(kelias)
    po.save_as_mofile(kelias[:-3] + '.mo')
    return True, '\n'.join(klaidos)


def main():
    bandymas = '--bandymas' in sys.argv
    kalbos = [a for a in sys.argv[1:] if not a.startswith('--')] or ['ru', 'en']
    api = raktas()
    if not api and not bandymas:
        sys.exit('Nėra GOOGLE_TRANSLATE_API_KEY (nei GOOGLE_MAPS_API_KEY) '
                 'aplinkoje. Šitam konteineryje rakto nėra — paleisk '
                 'serveryje arba perduok raktą per aplinkos kintamąjį.')

    zodynas = tt.zodynas()
    ataskaita = []
    for kalba in kalbos:
        kelias = tt.po_kelias(kalba)
        po = polib.pofile(kelias)
        pildom, daugiskaitos = kandidatai(po, zodynas)
        print('\n%s: tuščių verstinų %d, daugiskaitos eilučių %d'
              % (kalba, len(pildom), len(daugiskaitos)))
        ataskaita.append('=== %s — daugiskaitos eilutės (%d), verčia žmogus ==='
                         % (kalba, len(daugiskaitos)))
        for e in daugiskaitos:
            ataskaita.append('  %s | %s' % (e.msgid, e.msgid_plural))
        if bandymas or not pildom:
            continue

        paslepti, dalys = zip(*[paslepk(e.msgid) for e in pildom])
        gauta = versk(list(paslepti), kalba, api)

        sulauzyti = []
        for e, d, v in zip(pildom, dalys, gauta):
            v = atskleisk(v, d)
            if kp.procentai(v) != kp.procentai(e.msgid) or kp.zymes(v) != kp.zymes(e.msgid):
                sulauzyti.append((e.msgid, v))
                continue                   # 2 apsauga: paliekam tuščią
            e.msgstr = v
            if 'fuzzy' not in e.flags:
                e.flags.append('fuzzy')    # dar neperžiūrėta
        print('   užpildyta %d, sulaužytų kintamųjų %d'
              % (len(pildom) - len(sulauzyti), len(sulauzyti)))
        ataskaita.append('\n=== %s — kintamieji sulūžo (%d), verčia žmogus ==='
                         % (kalba, len(sulauzyti)))
        for mid, blogas in sulauzyti:
            ataskaita.append('  msgid: %s\n  mašina: %s' % (mid, blogas))

        gerai, klaida = isaugok_jei_svaru(po, kelias)
        if not gerai:
            print('   NEĮRAŠYTA — msgfmt --check klaidos:\n%s' % klaida)
            return 1
        print('   įrašyta, msgfmt --check švarus')

    kelias = os.path.join(BASE, 'docs', 'vertimo_uzpildymas_ataskaita.txt')
    open(kelias, 'w', encoding='utf-8').write('\n'.join(ataskaita) + '\n')
    print('\nAtaskaita žmogui: %s' % kelias)
    return 0


if __name__ == '__main__':
    sys.exit(main())
