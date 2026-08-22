"""Šablonų ir puslapių patikros, kurias privaloma paleisti PRIEŠ DIEGIMĄ.

Kodėl testas, o ne taisyklė dokumentacijoje: taisyklė „nerašyk daugiaeilio
{# #}" buvo, bet komentaras į puslapį nutekėjo penkis kartus — ji veikia tik
tada, kai kas nors ją prisimena perskaityti. Testas neprisimena — jis krenta.

Paleidimas:
    venv/bin/python manage.py test apps.listings -v 2
"""
import re
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.test import Client, SimpleTestCase

SABLONU_KATALOGAS = Path(settings.BASE_DIR) / 'templates'

# Netikrinam atsarginių kopijų (.bak…) — jos nerenderinamos
NETIKRINTI = ('.bak', '.orig', '.tmp')


def _sablonai():
    for kelias in SABLONU_KATALOGAS.rglob('*.html'):
        if any(z in kelias.name for z in NETIKRINTI):
            continue
        yield kelias


class SablonuKomentaraiTestas(SimpleTestCase):
    """Statinė patikra: `{# … #}` Django šablone veikia TIK vienoje eilutėje.

    Daugiaeilis `{#` lieka paprastu tekstu ir atsiduria puslapyje.
    Daugiaeiliams komentarams yra `{% comment %}…{% endcomment %}`.
    """

    def test_nera_neuzdaryto_grotelinio_komentaro(self):
        radiniai = []
        for kelias in _sablonai():
            for nr, eilute in enumerate(kelias.read_text(encoding='utf-8').splitlines(), 1):
                if '{#' in eilute and '#}' not in eilute:
                    santykinis = kelias.relative_to(settings.BASE_DIR)
                    radiniai.append(f'{santykinis}:{nr}: {eilute.strip()[:90]}')
        self.assertEqual(
            radiniai, [],
            'Daugiaeilis {# #} komentaras nutekės į puslapį. '
            'Naudok {% comment %}…{% endcomment %}:\n  ' + '\n  '.join(radiniai))


class PuslapiuTestas(SimpleTestCase):
    """Renderinam pagrindinius puslapius ir tikrinam, kas nusėdo HTML'e.

    TIK SKAITOM: naudojam esamus duomenis, nieko nekuriam ir nekeičiam
    (žr. config/test_runner.BeDuombazes — testinė DB nekuriama).
    """

    databases = {'default'}

    def setUp(self):
        from apps.listings.models import Listing, VehicleType

        self.kategorijos = list(
            VehicleType.objects.filter(
                slug__in=['cars', 'motorcycles', 'trucks', 'parts', 'tires',
                          'trailers', 'agriculture', 'boats']
            ).values_list('slug', flat=True))
        self.skelbimas = Listing.objects.filter(
            status='active', is_shadow_banned=False).order_by('-created_at').first()
        self.vartotojas = get_user_model().objects.filter(is_active=True).first()
        priimtinas = [h for h in settings.ALLOWED_HOSTS if h not in ('*',)]
        self.c = Client(SERVER_NAME=priimtinas[0] if priimtinas else 'testserver')

    # ── puslapių sąrašas, kurį tikrinam ──
    def _puslapiai(self):
        puslapiai = [
            ('pagrindinis', '/'),
            ('pagrindinis su sekcija', '/?section=cars'),
            ('rezultatai su juosta', '/?category=cars&sidebar=1'),
            ('detali paieška', '/paieska/cars/'),
            ('naršyti', '/browse/'),
            ('mano paieškos', '/searches/'),
        ]
        if self.skelbimas:
            puslapiai.append(('skelbimas', f'/{self.skelbimas.pk}/'))
        return puslapiai

    def test_nera_sablono_komentaru_puslapiuose(self):
        """Nė viename atsakyme neturi būti „{#" ar „#}"."""
        if self.vartotojas:
            self.c.force_login(self.vartotojas)  # /searches/ reikia prisijungimo
        klaidos = []
        for pavadinimas, adresas in self._puslapiai():
            atsakymas = self.c.get(adresas, secure=True, follow=True)
            self.assertEqual(atsakymas.status_code, 200, f'{pavadinimas} ({adresas})')
            turinys = atsakymas.content.decode('utf-8', 'ignore')
            for zenklas in ('{#', '#}'):
                vieta = turinys.find(zenklas)
                if vieta != -1:
                    eilute = turinys.count('\n', 0, vieta) + 1
                    iskarpa = turinys[max(0, vieta - 60):vieta + 120].replace('\n', ' ')
                    klaidos.append(f'{pavadinimas} ({adresas}), eilutė {eilute}: …{iskarpa}…')
        self.assertEqual(klaidos, [], 'Šablono komentaras nutekėjo į puslapį:\n  '
                                      + '\n  '.join(klaidos))

    def test_tuscios_busenos_ikona_atitinka_kategorija(self):
        """Kai rezultatų nėra, ikona turi būti TOS kategorijos.

        Lyginam su tuo pačiu partial'u, kuris piešia ikonas visur kitur —
        todėl testas pagauna ir „automobiliams rodomas sunkvežimis".
        """
        sablonas = re.compile(
            r'block w-12 h-12 mx-auto mb-4 text-gray-300">\s*(<svg.*?</svg>)', re.S)
        klaidos = []
        for slug in self.kategorijos:
            # price_min didesnis už bet kokią kainą → tuščia būsena
            atsakymas = self.c.get(f'/?category={slug}&sidebar=1&price_min=99999999',
                                   secure=True, follow=True)
            self.assertEqual(atsakymas.status_code, 200, slug)
            turinys = atsakymas.content.decode('utf-8', 'ignore')
            rastas = sablonas.search(turinys)
            if not rastas:
                klaidos.append(f'{slug}: tuščios būsenos ikonos nerasta')
                continue
            puslapyje = re.sub(r'\s+', ' ', rastas.group(1)).strip()
            laukiama = re.sub(
                r'\s+', ' ',
                render_to_string('listings/partials/category_icon.html',
                                 {'slug': slug})).strip()
            if puslapyje != laukiama:
                klaidos.append(f'{slug}: ikona ne tos kategorijos\n'
                               f'      puslapyje: {puslapyje[:110]}\n'
                               f'      laukiama : {laukiama[:110]}')
        self.assertEqual(klaidos, [], 'Tuščios būsenos ikonos:\n  ' + '\n  '.join(klaidos))
