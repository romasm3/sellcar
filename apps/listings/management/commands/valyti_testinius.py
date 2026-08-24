# -*- coding: utf-8 -*-
"""
Management command: valyti_testinius

Testinių skelbimų inventorius ir valymas — Listing, Truck, WheelListing.

KODĖL ATSKIRA KOMANDA. Testiniai skelbimai atsirado iš dviejų vietų
(`testiniai_skelbimai` ir `seed_fake_listings`), abi turi savo --trinti,
bet nė viena nemato kitos, nedaro atsarginės kopijos ir nepašalina
nuotraukų nuo disko. Django `on_delete=CASCADE` išvalo tik DB eilutes —
JPEG'ai lieka media kataloge amžiams.

SAUGIKLIAI
    · numatytoji veiksena — TIK SĄRAŠAS, nieko nekeičia
    · trinti galima tik su --trinti --tikrai (abu kartu)
    · prieš trynimą privaloma pg_dump kopija; nepavyko — nutraukiam
    · trinami tik TIKRAI testiniai (žr. žemiau); „klaustukai" NIEKADA
      netrinami automatiškai — jie surašomi patvirtinimui
    · viskas vienoje transakcijoje; failai nuo disko šalinami TIK po to,
      kai transakcija sėkmingai užsidaro

KAS LAIKOMA TIKRAI TESTINIU (mašininė žymė, be spėlionių)
    · aprašymas prasideda „TESTINIS SKELBIMAS"   (testiniai_skelbimai)
    · aprašyme yra „__SEEDED_FAKE__"             (seed_fake_listings)
    · savininkas testai@autoleft.local
    · pavadinime „[TEST]"

KAS PATENKA Į „KLAUSTUKUS" (rodoma, bet netrinama)
    · pavadinimas tipo „test", „aaa", „asd", „qwe", „bandymas", „123"
    · kaina ≤ 1 IR nė vienos nuotraukos
    · nė vienos nuotraukos IR aprašymas trumpesnis nei 20 simbolių
    · savininkas romasm333@gmail.com (testinė pirkėjo paskyra, bet joje
      gali būti ir tikrų skelbimų)

NAUDOJIMAS
    python manage.py valyti_testinius                  # visų skelbimų lentelė
    python manage.py valyti_testinius --tik-testiniai  # tik kandidatai
    python manage.py valyti_testinius --csv /tmp/skelbimai.csv
    python manage.py valyti_testinius --trinti --tikrai
    python manage.py valyti_testinius --trinti --tikrai --id 12,15,18
"""
import os
import re
import subprocess
from datetime import date

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

TESTINIO_APRASO_PRADZIA = 'TESTINIS SKELBIMAS'
SEED_ZYMA = '__SEEDED_FAKE__'
TESTINIS_PASTAS = 'testai@autoleft.local'
ITARTINA_PASKYRA = 'romasm333@gmail.com'

# Pavadinimai, kurie beveik visada reiškia bandymą. Tikrinama VISAS
# pavadinimas, ne dalis: „Testarossa" ar „Assist" neturi pakliūti.
ITARTINI_PAVADINIMAI = re.compile(
    r'^\s*(test|testas|testinis|tests?\d*|a{2,}|s{2,}|asd\w*|qwe\w*|zxc\w*'
    r'|x{2,}|\d{1,4}|bandymas|bandau|nauja|naujas|xxx|ffff?)\s*$',
    re.IGNORECASE)

ATSARGINIU_KATALOGAS = '/root/backups'


def _modeliai():
    """(modelis, vardas, nuotraukų laukai) — importuojama vėlai, kad
    komanda būtų įkeliama ir be paruoštos DB."""
    from apps.listings.models import Listing, Truck, WheelListing
    return [
        (Listing, 'Listing', ('image', 'image_lg', 'image_lg_webp',
                              'image_sm', 'image_sm_webp')),
        (Truck, 'Truck', ('image',)),
        (WheelListing, 'WheelListing', ('image',)),
    ]


def _kategorija(obj, modelio_vardas):
    vt = getattr(obj, 'vehicle_type', None)
    if vt is not None:
        return getattr(vt, 'slug', None) or str(vt)
    if modelio_vardas == 'Truck':
        return 'trucks'
    if modelio_vardas == 'WheelListing':
        return getattr(obj, 'wheel_type', None) or 'wheels'
    return '—'


def _savininkas(obj):
    s = getattr(obj, 'seller', None)
    if s is None:
        return '(nėra)'
    return getattr(s, 'email', None) or getattr(s, 'username', None) or str(s.pk)


def ivertinti(obj, modelio_vardas, nuotrauku):
    """Grąžina ('testinis'|'klaustukas'|'tikras', priežastis)."""
    aprasymas = (getattr(obj, 'description', '') or '')
    pavadinimas = (getattr(obj, 'title', '') or '')
    pastas = _savininkas(obj)

    if aprasymas.lstrip().startswith(TESTINIO_APRASO_PRADZIA):
        return 'testinis', 'aprašymas „TESTINIS SKELBIMAS"'
    if SEED_ZYMA in aprasymas:
        return 'testinis', 'seed žymė __SEEDED_FAKE__'
    if pastas.lower() == TESTINIS_PASTAS:
        return 'testinis', 'savininkas ' + TESTINIS_PASTAS
    if '[TEST]' in pavadinimas.upper():
        return 'testinis', 'pavadinime [TEST]'

    if ITARTINI_PAVADINIMAI.match(pavadinimas):
        return 'klaustukas', 'įtartinas pavadinimas „%s"' % pavadinimas.strip()

    try:
        kaina = float(getattr(obj, 'price', 0) or 0)
    except (TypeError, ValueError):
        kaina = 0.0
    if nuotrauku == 0 and kaina <= 1:
        return 'klaustukas', 'be nuotraukų, kaina %g' % kaina
    if nuotrauku == 0 and len(aprasymas.strip()) < 20:
        return 'klaustukas', 'be nuotraukų, aprašymas %d simb.' % len(aprasymas.strip())
    if pastas.lower() == ITARTINA_PASKYRA:
        return 'klaustukas', 'savininkas ' + ITARTINA_PASKYRA

    return 'tikras', ''


def _failu_keliai(obj, nuotrauku_laukai):
    """Visi šio skelbimo nuotraukų failai diske."""
    keliai = []
    for img in obj.images.all():
        for laukas in nuotrauku_laukai:
            f = getattr(img, laukas, None)
            if not f:
                continue
            try:
                keliai.append(f.path)
            except (ValueError, NotImplementedError):
                pass
    return keliai


class Command(BaseCommand):
    help = 'Išvardina visus skelbimus ir (su --trinti --tikrai) pašalina testinius.'

    def add_arguments(self, p):
        p.add_argument('--trinti', action='store_true',
                       help='Trinti testinius (reikia ir --tikrai)')
        p.add_argument('--tikrai', action='store_true',
                       help='Patvirtinimas: be jo --trinti nieko nedaro')
        p.add_argument('--id', default='',
                       help='Papildomi ID, kuriuos leidžiama trinti, pvz. '
                            '"Listing:12,Truck:3" arba tiesiog "12,15" (Listing)')
        p.add_argument('--tik-testiniai', action='store_true',
                       help='Lentelėje rodyti tik testinius ir klaustukus')
        p.add_argument('--csv', default='', help='Įrašyti visą sąrašą į CSV')
        p.add_argument('--be-kopijos', action='store_true',
                       help='Praleisti pg_dump. NENAUDOTI be labai geros priežasties.')

    # ── Duomenys ─────────────────────────────────────────────────────
    def _surinkti(self):
        eilutes = []
        for modelis, vardas, laukai in _modeliai():
            qs = modelis.objects.all().select_related('seller').prefetch_related('images')
            if hasattr(modelis, 'vehicle_type'):
                qs = qs.select_related('vehicle_type')
            for obj in qs.order_by('pk'):
                n = obj.images.count()
                verdiktas, priezastis = ivertinti(obj, vardas, n)
                eilutes.append({
                    'modelis': vardas, 'obj': obj, 'laukai': laukai,
                    'id': obj.pk,
                    'kategorija': _kategorija(obj, vardas),
                    'pavadinimas': (getattr(obj, 'title', '') or '').strip(),
                    'savininkas': _savininkas(obj),
                    'statusas': getattr(obj, 'status', '') or '',
                    'sukurta': getattr(obj, 'created_at', None),
                    'kaina': getattr(obj, 'price', None),
                    'nuotrauku': n,
                    'verdiktas': verdiktas,
                    'priezastis': priezastis,
                })
        return eilutes

    def _lentele(self, eilutes):
        antraste = ('%-12s %-6s %-18s %-38s %-28s %-9s %-16s %-4s %s'
                    % ('MODELIS', 'ID', 'KATEGORIJA', 'PAVADINIMAS', 'SAVININKAS',
                       'STATUSAS', 'SUKURTA', 'NUO', 'VERDIKTAS'))
        self.stdout.write(antraste)
        self.stdout.write('─' * len(antraste))
        for e in eilutes:
            data = e['sukurta'].strftime('%Y-%m-%d %H:%M') if e['sukurta'] else '—'
            self.stdout.write('%-12s %-6s %-18s %-38s %-28s %-9s %-16s %-4s %s'
                              % (e['modelis'], e['id'], e['kategorija'][:18],
                                 e['pavadinimas'][:38], e['savininkas'][:28],
                                 e['statusas'][:9], data, e['nuotrauku'],
                                 e['verdiktas'] + (' — ' + e['priezastis'] if e['priezastis'] else '')))

    def _csv(self, eilutes, kelias):
        import csv
        with open(kelias, 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            w.writerow(['modelis', 'id', 'kategorija', 'pavadinimas', 'savininkas',
                        'statusas', 'sukurta', 'kaina', 'nuotrauku', 'verdiktas',
                        'priezastis'])
            for e in eilutes:
                w.writerow([e['modelis'], e['id'], e['kategorija'], e['pavadinimas'],
                            e['savininkas'], e['statusas'],
                            e['sukurta'].isoformat() if e['sukurta'] else '',
                            e['kaina'], e['nuotrauku'], e['verdiktas'], e['priezastis']])
        self.stdout.write(self.style.SUCCESS('CSV: ' + kelias))

    # ── Atsarginė kopija ─────────────────────────────────────────────
    def _kopija(self):
        db = settings.DATABASES['default']
        if 'postgresql' not in db['ENGINE']:
            raise CommandError('pg_dump tinka tik PostgreSQL, o čia %s. '
                               'Naudok --be-kopijos tik jei kopiją padarei ranka.'
                               % db['ENGINE'])
        os.makedirs(ATSARGINIU_KATALOGAS, exist_ok=True)
        kelias = os.path.join(ATSARGINIU_KATALOGAS,
                              'pries-testiniu-trynima-%s.sql.gz' % date.today().isoformat())
        aplinka = dict(os.environ)
        if db.get('PASSWORD'):
            aplinka['PGPASSWORD'] = str(db['PASSWORD'])
        komanda = ['pg_dump', '--no-owner', '--dbname', db['NAME']]
        if db.get('USER'):
            komanda += ['--username', str(db['USER'])]
        if db.get('HOST'):
            komanda += ['--host', str(db['HOST'])]
        if db.get('PORT'):
            komanda += ['--port', str(db['PORT'])]

        self.stdout.write('Kopija: ' + kelias)
        with open(kelias, 'wb') as isvestis:
            dump = subprocess.Popen(komanda, stdout=subprocess.PIPE, env=aplinka)
            gzip_p = subprocess.Popen(['gzip', '-c'], stdin=dump.stdout, stdout=isvestis)
            dump.stdout.close()
            gzip_p.communicate()
            dump.wait()
        if dump.returncode != 0 or gzip_p.returncode != 0 or os.path.getsize(kelias) < 1024:
            raise CommandError('pg_dump NEPAVYKO (%s). Nieko netrinu.' % kelias)
        self.stdout.write(self.style.SUCCESS(
            '  ✓ %.1f MB' % (os.path.getsize(kelias) / 1048576.0)))
        return kelias

    # ── Leisti trinti ────────────────────────────────────────────────
    def _papildomi(self, tekstas):
        leidziami = set()
        for dalis in filter(None, (t.strip() for t in tekstas.split(','))):
            if ':' in dalis:
                modelis, pk = dalis.split(':', 1)
                leidziami.add((modelis.strip(), int(pk)))
            else:
                leidziami.add(('Listing', int(dalis)))
        return leidziami

    def handle(self, *args, **o):
        eilutes = self._surinkti()
        if not eilutes:
            self.stdout.write('Skelbimų nėra.')
            return

        rodomos = ([e for e in eilutes if e['verdiktas'] != 'tikras']
                   if o['tik_testiniai'] else eilutes)
        self._lentele(rodomos)
        if o['csv']:
            self._csv(eilutes, o['csv'])

        testiniai = [e for e in eilutes if e['verdiktas'] == 'testinis']
        klaustukai = [e for e in eilutes if e['verdiktas'] == 'klaustukas']
        tikri = [e for e in eilutes if e['verdiktas'] == 'tikras']

        self.stdout.write('')
        self.stdout.write('Iš viso %d · testiniai %d · klaustukai %d · tikri %d'
                          % (len(eilutes), len(testiniai), len(klaustukai), len(tikri)))

        if klaustukai:
            self.stdout.write('')
            self.stdout.write(self.style.WARNING('KLAUSTUKAI — NETRINAMI be tavo žodžio:'))
            for e in klaustukai:
                self.stdout.write('  %s:%s  %-38s %-26s  %s'
                                  % (e['modelis'], e['id'], e['pavadinimas'][:38],
                                     e['savininkas'][:26], e['priezastis']))
            self.stdout.write('  Patvirtinus: --trinti --tikrai --id "%s"'
                              % ','.join('%s:%s' % (e['modelis'], e['id']) for e in klaustukai))

        if not o['trinti']:
            self.stdout.write('')
            self.stdout.write('Tik sąrašas. Trynimui: --trinti --tikrai')
            return

        if not o['tikrai']:
            raise CommandError('--trinti be --tikrai nieko nedaro. Abu kartu.')

        leidziami = self._papildomi(o['id'])
        trinsim = list(testiniai) + [e for e in klaustukai
                                     if (e['modelis'], e['id']) in leidziami]
        # --id gali nurodyti ir „tikrą" skelbimą — leidžiam tik aiškiai įvardytą
        trinsim += [e for e in tikri if (e['modelis'], e['id']) in leidziami]
        if not trinsim:
            self.stdout.write('Trinti nėra ko.')
            return

        if not o['be_kopijos']:
            self._kopija()
        else:
            self.stdout.write(self.style.WARNING('--be-kopijos: pg_dump praleistas'))

        # Failų keliai surenkami PRIEŠ trynimą — po delete() jų nebeliks
        failai = []
        for e in trinsim:
            failai += _failu_keliai(e['obj'], e['laukai'])

        with transaction.atomic():
            for e in trinsim:
                e['obj'].delete()

        # Failai — tik po sėkmingos transakcijos: jei DB atsuktų atgal,
        # skelbimai liktų be nuotraukų.
        pasalinta = nerasta = 0
        for kelias in failai:
            try:
                os.remove(kelias)
                pasalinta += 1
            except FileNotFoundError:
                nerasta += 1
            except OSError as klaida:
                self.stdout.write(self.style.WARNING('  failas liko: %s (%s)'
                                                     % (kelias, klaida)))

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('IŠTRINTA %d skelbimų:' % len(trinsim)))
        for e in trinsim:
            self.stdout.write('  %s:%s  %-38s  %s'
                              % (e['modelis'], e['id'], e['pavadinimas'][:38],
                                 e['priezastis'] or 'nurodyta per --id'))
        self.stdout.write('Nuotraukų failų: pašalinta %d, nerasta diske %d'
                          % (pasalinta, nerasta))
        self.stdout.write('Palikta: %d' % (len(eilutes) - len(trinsim)))
