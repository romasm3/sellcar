# -*- coding: utf-8 -*-
"""
VIENKARTINIS tuščių msgstr užpildymas Google Translate'u.

AUTENTIKACIJA — tokia pati kaip apps/conversations/translate_service.py:
paslaugos paskyra per GOOGLE_APPLICATION_CREDENTIALS (numatytai
<projektas>/google-translate-key.json) ir `translate_v2.Client()` be
jokių papildomų parametrų. API raktu čia nesinaudojam: Maps raktas
apribotas HTTP referrer'iais, tad iš serverio grąžina
403 „Requests from referer <empty> are blocked".

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

Paketas — 100 eilučių, tarp paketų 200 ms. Kritęs paketas praleidžiamas
ir darbas tęsiamas; kurie krito, surašoma ataskaitos gale.

    cd /root/autoleft && source venv/bin/activate
    python docs/vertimo_uzpildymas.py ru en
    python docs/vertimo_uzpildymas.py --bandymas    # kiek ko yra, be API
"""
import os
import re
import subprocess
import sys
import tempfile
import time

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, 'docs'))

PAKETAS = 100         # eilučių viename kreipinyje
PAUZE = 0.2           # s tarp paketų

# Katalogo aplankas ne visada sutampa su Google kalbos kodu:
# Django rašo `zh_Hans`, Google laukia `zh-CN`.
GOOGLE_KODAS = {
    'zh_Hans': 'zh-CN', 'zh-hans': 'zh-CN', 'zh_Hant': 'zh-TW',
    'pt_BR': 'pt', 'nb': 'no',
}


def visos_kalbos(su_saltiniu=False):
    """Visi locale/ katalogai — kad naujos kalbos nereikėtų įrašinėti.

    `lt` praleidžiam: tai šaltinio kalba, jos msgid'ai jau lietuviški, ir
    tuščias msgstr vartotojui rodo būtent juos. Vertimas iš lietuvių į
    lietuvių tik sugadintų patvirtintą tekstą. Reikia — nurodyk ją vardu.
    """
    saknis = os.path.join(BASE, 'locale')
    visos = sorted(k for k in os.listdir(saknis)
                   if os.path.exists(os.path.join(saknis, k,
                                                  'LC_MESSAGES', 'django.po')))
    if su_saltiniu:
        return visos
    return [k for k in visos if k != 'lt']

try:
    import polib
except ImportError:
    sys.exit('Reikia polib: pip install polib')

import kintamuju_patikra as kp
import terminai_taikyti as tt

# Kintamieji, kuriuos prieš vertimą paslepiam už neutralaus ženklo.
SAUGOMI = re.compile(r'%\([^)]*\)[a-zA-Z]|%[a-zA-Z%]|\{[^{}]*\}')


def rakto_failas():
    """Tas pats kelias, kurį skaito config/settings.py."""
    kelias = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    if not kelias:
        try:
            from decouple import config
            kelias = config('GOOGLE_APPLICATION_CREDENTIALS', default='')
        except Exception:
            kelias = ''
    kelias = kelias or os.path.join(BASE, 'google-translate-key.json')
    if os.path.isfile(kelias):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = kelias
        return kelias
    return ''


def klientas():
    """translate_v2.Client() be parametrų — kaip translate_service.py."""
    from google.cloud import translate_v2 as translate
    return translate.Client()


def paslepk(tekstas):
    """„Rasta %(n)s" → („Rasta ⟦0⟧", ['%(n)s'])."""
    dalys = []

    def keisk(m):
        dalys.append(m.group(0))
        return '⟦%d⟧' % (len(dalys) - 1)

    return SAUGOMI.sub(keisk, tekstas), dalys


def atskleisk(tekstas, dalys):
    for i, d in enumerate(dalys):
        # Google kartais įterpia tarpų aplink ženklą — priimam ir tokį.
        tekstas = re.sub(r'⟦\s*%d\s*⟧' % i, lambda _m, d=d: d, tekstas)
    return tekstas


def versk_paketais(tekstai, kalba, cli):
    """[str] → ([str|None], [(nuo, iki, klaida)]).

    Kritęs paketas neužverčia viso darbo: jo eilutės grįžta kaip None,
    o klaida įrašoma į ataskaitą.
    """
    isversta = [None] * len(tekstai)
    kritę = []
    viso = len(tekstai)
    for i in range(0, viso, PAKETAS):
        porcija = tekstai[i:i + PAKETAS]
        try:
            # Šaltinio kalbos NENURODOM: msgid'ai mišrūs — dalis angliški,
            # dalis lietuviški. Google atpažįsta pati.
            atsakymas = cli.translate(
                porcija, target_language=GOOGLE_KODAS.get(kalba, kalba),
                format_='text')
            if isinstance(atsakymas, dict):
                atsakymas = [atsakymas]
            for j, t in enumerate(atsakymas):
                isversta[i + j] = t.get('translatedText', '')
        except Exception as e:
            kritę.append((i, min(i + PAKETAS, viso), '%s: %s'
                          % (type(e).__name__, str(e)[:200])))
            print('   %d–%d KRITO (%s), tęsiam'
                  % (i + 1, min(i + PAKETAS, viso), type(e).__name__))
        print('   %d/%d' % (min(i + PAKETAS, viso), viso))
        time.sleep(PAUZE)
    return isversta, kritę


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
    polib.pofile(kelias).save_as_mofile(kelias[:-3] + '.mo')
    return True, '\n'.join(klaidos)


def main():
    bandymas = '--bandymas' in sys.argv
    kalbos = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not kalbos or kalbos == ['visos']:
        kalbos = visos_kalbos()

    cli = None
    if not bandymas:
        failas = rakto_failas()
        if not failas:
            sys.exit('Nėra paslaugos paskyros rakto. Ieškota: '
                     'GOOGLE_APPLICATION_CREDENTIALS ir %s.\n'
                     'Serveryje jis yra — paleisk ten, iš /root/autoleft.'
                     % os.path.join(BASE, 'google-translate-key.json'))
        print('Raktas: %s' % failas)
        try:
            cli = klientas()
        except Exception as e:
            sys.exit('Nepavyko sukurti kliento: %s: %s' % (type(e).__name__, e))

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
        gauta, kritę = versk_paketais(list(paslepti), kalba, cli)

        sulauzyti = []
        uzpildyta = 0
        for e, d, v in zip(pildom, dalys, gauta):
            if v is None:
                continue                   # paketas krito — paliekam tuščią
            v = atskleisk(v, d)
            if (kp.procentai(v) != kp.procentai(e.msgid)
                    or kp.zymes(v) != kp.zymes(e.msgid)):
                sulauzyti.append((e.msgid, v))
                continue                   # 2 apsauga: paliekam tuščią
            e.msgstr = v
            if 'fuzzy' not in e.flags:
                e.flags.append('fuzzy')    # dar neperžiūrėta
            uzpildyta += 1
        print('   užpildyta %d, sulaužytų kintamųjų %d, kritusių paketų %d'
              % (uzpildyta, len(sulauzyti), len(kritę)))

        ataskaita.append('\n=== %s — kintamieji sulūžo (%d), verčia žmogus ==='
                         % (kalba, len(sulauzyti)))
        for mid, blogas in sulauzyti:
            ataskaita.append('  msgid : %s\n  mašina: %s' % (mid, blogas))
        ataskaita.append('\n=== %s — kritę paketai (%d) ===' % (kalba, len(kritę)))
        for nuo, iki, klaida in kritę:
            ataskaita.append('  eilutės %d–%d: %s' % (nuo + 1, iki, klaida))

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
