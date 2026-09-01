# -*- coding: utf-8 -*-
"""Vertimų sargyba: angliškas puslapis turi būti angliškas, o lietuviški
tekstai — apvynioti.

Kodėl testai, o ne taisyklė: „nepamiršk {% trans %}" veikia tik tada, kai
kas nors ją prisimena. Testas neprisimena — jis krenta. Du atskiri kampai:

1. STATIŠKAI — šablone nelikę neapvynioto lietuviško teksto (nei tarp žymių,
   nei placeholder/title/aria-label/alt atributuose), o JS faile nelikę
   lietuviškų eilučių (tekstai keliauja per json_script).
2. GYVAI — atidarom /en/… puslapius ir tikrinam, kad juose nebūtų lietuviškų
   raidžių. Vartotojų duomenys (įmonių, meistrų, paslaugų, miestų pavadinimai)
   neverčiami, todėl jie iš patikros išimami.

Paleidimas:
    venv/bin/python manage.py test apps.imones \
        --testrunner=config.test_runner.BeDuombazes
"""
import re
from pathlib import Path

from django.conf import settings
from django.test import Client, SimpleTestCase

LT_RAIDES = 'ąčęėįšųūžĄČĘĖĮŠŲŪŽ'

SABLONAI = Path(settings.BASE_DIR) / 'templates' / 'imones'
JS = Path(settings.BASE_DIR) / 'static' / 'js' / 'imones_fresha.js'

# Ne sąsajos tekstas: prekės ženklas, technikos vardai.
LEISTA = {
    'Autoleft', 'AutoLeft', 'Auto', 'Left', 'Google', 'Maps', 'OpenStreetMap',
    'Leaflet', 'div', 'span', 'svg', 'px', 'rem', 'href', 'src', 'nbsp',
    'amp', 'true', 'false', 'null', 'utf', 'https', 'http', 'www', 'com',
}

# Šalinam tai, kas nėra verčiamas tekstas
_BLOKTRANS = re.compile(
    r'\{%\s*blocktrans(?:late)?\b.*?\{%\s*endblocktrans(?:late)?\s*%\}', re.S)
_KOMENT_DJ = re.compile(r'\{%\s*comment\s*%\}.*?\{%\s*endcomment\s*%\}', re.S)
_ZYME = re.compile(r'\{%.*?%\}|\{\{.*?\}\}|\{#.*?#\}', re.S)
_SKRIPTAI = re.compile(r'<(script|style)\b[^>]*>.*?</\1>', re.S | re.I)
_KOMENT_HTML = re.compile(r'<!--.*?-->', re.S)
_ATRIBUTAI = re.compile(
    r'(:?)\b(placeholder|title|aria-label|alt)\s*=\s*(["\'])(.*?)\3', re.S)
# Bet kokia atributo reikšmė — išmetam ją prieš šalindami žymes, kad
# „>" Alpine išraiškoje (x-show="a > 2") nesuskaldytų žymės per pusę.
_ATRIB_REIKSME = re.compile(r'=\s*(["\'])(?:(?!\1).)*\1', re.S)
# Eilutės konstanta Alpine išraiškoje (:placeholder="a || 'tekstas'")
_EILUTE = re.compile(r'''(["\'])(.*?)\1''', re.S)
_ZODIS = re.compile(r'[A-Za-z' + LT_RAIDES + r']{3,}')


def _be_komentaru(tekstas):
    """Išmeta Django ir HTML komentarus bei jau išverstus blocktrans blokus."""
    tuscia = lambda m: '\n' * m.group(0).count('\n')
    return _BLOKTRANS.sub(tuscia, _KOMENT_DJ.sub(tuscia, tekstas))


class NeapvyniotasTekstasTestas(SimpleTestCase):
    """Statinė patikra: šablone nelikę teksto be {% trans %}."""

    def _radiniai(self, kelias):
        s = _be_komentaru(kelias.read_text(encoding='utf-8'))
        radiniai = []
        # 1. verčiami atributai. Alpine sąsajoje (:placeholder="…") tikrinam
        #    tik eilutės konstantas — kintamųjų vardai nėra tekstas.
        be_zymiu = _ZYME.sub(' ', _SKRIPTAI.sub(' ', s))
        for m in _ATRIBUTAI.finditer(be_zymiu):
            reiksme = m.group(4).strip()
            tikrinam = ([e for _c, e in _EILUTE.findall(reiksme)] if m.group(1)
                        else [reiksme])
            zodziai = [z for dalis in tikrinam for z in _ZODIS.findall(dalis)]
            if zodziai and not all(z in LEISTA for z in zodziai):
                eil = s[:m.start()].count('\n') + 1
                radiniai.append(f'{kelias.name}:{eil}: {m.group(2)}="{reiksme[:60]}"')
        # 2. tekstas tarp žymių
        b = _KOMENT_HTML.sub(' ', _SKRIPTAI.sub(' ', s))
        b = _ATRIB_REIKSME.sub('=""', _ZYME.sub(' ', b))
        b = re.sub(r'<[^>]*>', ' ', b)
        for eil, linija in enumerate(b.splitlines(), 1):
            for z in _ZODIS.findall(linija):
                if z not in LEISTA:
                    radiniai.append(f'{kelias.name}:{eil}: {z}')
        return radiniai

    def test_imoniu_sablonuose_viskas_apvyniota(self):
        radiniai = []
        for kelias in sorted(SABLONAI.glob('*.html')):
            radiniai += self._radiniai(kelias)
        self.assertEqual(
            radiniai, [],
            'Tekstas be {% trans %} / {% blocktrans %}:\n  ' + '\n  '.join(radiniai))

    def test_js_faile_nera_lietuvisku_eiluciu(self):
        """Tekstai naršyklei ateina per json_script, o ne eilutėmis JS'e."""
        radiniai = []
        for nr, eilute in enumerate(JS.read_text(encoding='utf-8').splitlines(), 1):
            # komentarų netikrinam — jie skirti mums, ne vartotojui
            be_koment = re.sub(r'/\*.*?\*/', '', eilute)
            be_koment = re.sub(r'(^|\s)(//|\*).*$', '', be_koment)
            for eilutes_tekstas in re.findall(r"'[^']*'|\"[^\"]*\"|`[^`]*`", be_koment):
                if set(eilutes_tekstas) & set(LT_RAIDES):
                    radiniai.append(f'{JS.name}:{nr}: {eilutes_tekstas[:60]}')
        self.assertEqual(
            radiniai, [],
            'Lietuviška eilutė JS faile (naudok json_script):\n  ' + '\n  '.join(radiniai))


class AngliskasPuslapisTestas(SimpleTestCase):
    """Gyva patikra: /en/… puslapiuose nelieka lietuviškų raidžių.

    TIK SKAITOM — nieko nekuriam ir nekeičiam.
    """

    databases = {'default'}

    def setUp(self):
        priimtinas = [h for h in settings.ALLOWED_HOSTS if h not in ('*',)]
        self.c = Client(SERVER_NAME=priimtinas[0] if priimtinas else 'testserver',
                        HTTP_X_FORWARDED_PROTO='https')

    def _puslapiai(self):
        from .models import Imone
        adresai = ['/en/imones/', '/en/imones/paieska/', '/en/imones/?tipas=meistrai']
        imone = Imone.objects.filter(patvirtinta=True).first() or Imone.objects.first()
        if imone:
            adresai.append(f'/en/imone/{imone.slug}/')
        return adresai

    def _duomenu_zodziai(self):
        """Vartotojų įvesti tekstai — jų neverčiam, todėl iš patikros išimam."""
        from .models import Imone, ImonesPaslauga, VeiklosSritis
        zodziai = set()
        laukai = ('pavadinimas', 'meistras_vardas', 'specializacija', 'miestas',
                  'adresas', 'rajonas', 'aprasymas')
        for i in Imone.objects.all():
            for laukas in laukai:
                zodziai |= set(_ZODIS.findall(getattr(i, laukas, '') or ''))
        for v in VeiklosSritis.objects.all():
            zodziai |= set(_ZODIS.findall(v.pavadinimas or ''))
        # Vietovardžiai („Klaipėda", „Visa Lietuva") — irgi duomenys:
        # jie lieka lietuviški ir angliškame puslapyje.
        from .views import POPULIARIOS_VIETOS
        for v in POPULIARIOS_VIETOS:
            zodziai |= set(_ZODIS.findall(str(v['vardas'])))
        for p in ImonesPaslauga.objects.all():
            zodziai |= set(_ZODIS.findall((p.pavadinimas or '') + ' ' + (p.aprasymas or '')))
        # Kalbų pavadinimai perjungiklyje — „Lietuvių", „Latviešu", „Русский".
        # Jie tyčia rašomi gimtąja kalba ir NEVERČIAMI: žmogus sąraše ieško
        # savo kalbos tokios, kokią ją vadina pats, o ne išverstos į tą, kurios
        # nemoka. Perjungiklis yra kiekviename puslapyje, tad be šios išimties
        # patikra kristų būtent dėl teisingo elgesio.
        from apps.listings.templatetags.kalbu_tags import PAVADINIMAI
        for vardas in PAVADINIMAI.values():
            zodziai |= set(_ZODIS.findall(vardas))
        return zodziai

    @staticmethod
    def _matomas(html):
        b = _KOMENT_HTML.sub(' ', _SKRIPTAI.sub(' ', html))
        dalys = [m.group(3) for m in _ATRIBUTAI.finditer(b)]
        dalys.append(re.sub(r'<[^>]*>', ' ', b))
        return ' '.join(dalys)

    def test_angliskuose_puslapiuose_nera_lietuviu_kalbos(self):
        duomenys = self._duomenu_zodziai()
        radiniai = []
        for adresas in self._puslapiai():
            atsakymas = self.c.get(adresas)
            self.assertEqual(atsakymas.status_code, 200, f'{adresas} negrįžo 200')
            tekstas = self._matomas(atsakymas.content.decode())
            for zodis in set(_ZODIS.findall(tekstas)):
                if set(zodis) & set(LT_RAIDES) and zodis not in duomenys:
                    radiniai.append(f'{adresas}: {zodis}')
        self.assertEqual(
            sorted(radiniai), [],
            'Angliškame puslapyje liko lietuviškas tekstas '
            '(neapvyniotas arba neišverstas .po faile):\n  ' + '\n  '.join(sorted(radiniai)))

    def test_lietuviskas_adresas_be_priesdelio(self):
        """/imones/ lieka be /lt/ — priešdėlį gauna tik anglų kalba."""
        self.assertEqual(self.c.get('/imones/').status_code, 200)
        self.assertEqual(self.c.get('/lt/imones/').status_code, 404)
