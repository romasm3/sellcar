# -*- coding: utf-8 -*-
"""
AKTYVŪS SKELBIMAI BE NUOTRAUKŲ — suradimas, atkūrimas, šalinimas.

Kortelė be nuotraukos tituliniame atrodo kaip klaida, o pirkėjui ji
bevertė. Skelbimas be nuotraukos atsiranda dviem keliais: nuotraukų
apskritai nebuvo įkelta, arba DB eilutė yra, o failo diske nebėra
(perkeltas media/, nepavykęs rsync, ištrintas rankomis).

Skelbimai gyvena TRIJOSE lentelėse, tad apeinam visas:
    Listing      + ListingImage   -> /<id>/
    Truck        + TruckImage     -> /sunkvezimiai/<id>/
    WheelListing + WheelImage     -> /wheels/<id>/

KO ŠITAS DARBAS PADARYTI NEGALI. Atkurti nuotraukų iš skelbimo šaltinio
(mobile.de ir pan.) neįmanoma: modeliuose tokio lauko NĖRA — nei
source_url, nei importo nuorodos, tik `video_url`. Tad vienintelis
atkūrimo kelias yra failas, gulintis diske kitu keliu; jo ieškom pagal
bylos vardą po MEDIA_ROOT.

SAUGIKLIAI
  * numatytoji veiksena — TIK PARODO, nieko nekeičia;
  * trynimas vyksta tik su --trinti IR tik po sėkmingo pg_dump;
  * svetimi skelbimai niekada netrinami — jie tik išvardijami.
    Savus nurodai per --savininkai (numatyta: dvi tavo paskyros).

Paleidimas:
    python manage.py nuotrauku_auditas                     # tik sąrašas
    python manage.py nuotrauku_auditas --atkurti           # + prisega rastus failus
    python manage.py nuotrauku_auditas --atkurti --trinti  # + ištrina likusius
"""
import os
import subprocess
from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connection

# Kieno skelbimus apskritai leidžiama trinti.
SAVI = ('romasm3@gmail.com', 'romasm333@gmail.com')
ATSARGU_KATALOGAS = '/root/autoleft_backups'


def _lenteles():
    """[(vardas, modelis, nuotraukų related_name, adreso funkcija)]"""
    from apps.listings.models import Listing, Truck, WheelListing
    return [
        ('Listing', Listing, 'images'),
        ('Truck', Truck, 'images'),
        ('WheelListing', WheelListing, 'images'),
    ]


def _failas_yra(nuotrauka):
    """Ar DB eilutės failas tikrai guli diske."""
    laukas = getattr(nuotrauka, 'image', None)
    if not laukas or not getattr(laukas, 'name', ''):
        return False
    try:
        return os.path.exists(laukas.path)
    except (ValueError, NotImplementedError, OSError):
        return False


def _diske_kitur(vardas, atmintine):
    """Failas tuo pačiu vardu kitoje media/ vietoje, arba None."""
    return atmintine.get(os.path.basename(vardas))


def _media_zemelapis():
    """{bylos vardas: pilnas kelias} — vienas MEDIA_ROOT perėjimas."""
    zemelapis = {}
    saknis = str(getattr(settings, 'MEDIA_ROOT', '') or '')
    if not saknis or not os.path.isdir(saknis):
        return zemelapis
    for kelias, _kat, bylos in os.walk(saknis):
        for b in bylos:
            # Pirmas radinys lieka: gilesnės kopijos dažniausiai yra
            # miniatiūros, o ne originalas.
            zemelapis.setdefault(b, os.path.join(kelias, b))
    return zemelapis


def surink(atmintine=None):
    """Aktyvūs skelbimai be naudojamos nuotraukos.

    Grąžina sąrašą žodynų: lentelė, id, pavadinimas, kategorija,
    savininkas, sukurta, bukle, nuotrauku, dingusiu, atkuriamu.
    """
    if atmintine is None:
        atmintine = _media_zemelapis()

    radiniai = []
    for vardas, modelis, rel in _lenteles():
        qs = modelis.objects.filter(status='active')
        if hasattr(modelis, 'is_shadow_banned'):
            qs = qs.filter(is_shadow_banned=False)
        for o in qs.select_related('seller').prefetch_related(rel):
            nuotraukos = list(getattr(o, rel).all())
            dingę = [n for n in nuotraukos if not _failas_yra(n)]
            if nuotraukos and not dingę:
                continue                      # viskas tvarkoje

            atkuriami = [n for n in dingę
                         if n.image and n.image.name
                         and _diske_kitur(n.image.name, atmintine)]
            radiniai.append({
                'lentele': vardas,
                'id': o.pk,
                'pavadinimas': (getattr(o, 'title', '') or '')[:60],
                'kategorija': _kategorija(o),
                'savininkas': getattr(getattr(o, 'seller', None), 'email', '') or '—',
                'sukurta': getattr(o, 'created_at', None),
                'bukle': 'be nuotraukų' if not nuotraukos else 'failai dingę',
                'nuotrauku': len(nuotraukos),
                'dingusiu': len(dingę),
                'atkuriamu': len(atkuriami),
                'objektas': o,
                'dinge': dingę,
            })
    return radiniai


def _kategorija(o):
    if o.__class__.__name__ == 'WheelListing':
        return 'Ratlankiai' if o.product_type == 'rim' else 'Padangos'
    if o.__class__.__name__ == 'Truck':
        return 'Sunkvežimiai'
    vt = getattr(o, 'vehicle_type', None)
    return getattr(vt, 'name', '') or '—'


def atkurk(radinys, atmintine):
    """Prisega diske rastus failus. Grąžina, kiek atkurta."""
    atkurta = 0
    for n in radinys['dinge']:
        if not (n.image and n.image.name):
            continue
        rastas = _diske_kitur(n.image.name, atmintine)
        if not rastas:
            continue
        # Kelias rašomas santykinis MEDIA_ROOT atžvilgiu — toks, kokio
        # laukia ImageField.
        naujas = os.path.relpath(rastas, str(settings.MEDIA_ROOT))
        if naujas != n.image.name:
            n.image.name = naujas
            n.save(update_fields=['image'])
        atkurta += 1
    return atkurta


def uzmigdyk(radinys):
    """Aktyvų skelbimą perjungia į „Neaktyvus" (expired).

    Ne trynimas: skelbimas dingsta iš paieškos ir titulinio (visi sąrašai
    filtruoja status='active'), bet lieka savininko paskyroje ir duomenų
    bazėje. Savininkas gali įkelti nuotraukas ir paskelbti iš naujo.

    Naudojam 'expired', nes jis yra VISUOSE trijuose modeliuose ir jau
    reiškia „neaktyvus" (Listing.STATUS_CHOICES: 'expired' -> Neaktyvus).
    """
    o = radinys['objektas']
    o.status = 'expired'
    o.save(update_fields=['status'])
    return True


def atsargine_kopija():
    """pg_dump į ATSARGU_KATALOGAS. Grąžina kelią arba kelia klaidą.

    Be jos netrinam NIEKO: prarasti skelbimą dėl klaidos scenarijuje
    galima, atkurti — ne.
    """
    variklis = connection.settings_dict.get('ENGINE', '')
    if 'postgresql' not in variklis:
        raise RuntimeError('Trynimas leidžiamas tik su PostgreSQL '
                           '(dabar %s) — pg_dump kitaip neturi prasmės.' % variklis)

    os.makedirs(ATSARGU_KATALOGAS, exist_ok=True)
    d = connection.settings_dict
    kelias = os.path.join(
        ATSARGU_KATALOGAS,
        'autoleft_%s.sql' % datetime.now().strftime('%Y-%m-%d_%H%M%S'))
    aplinka = dict(os.environ)
    if d.get('PASSWORD'):
        aplinka['PGPASSWORD'] = d['PASSWORD']
    komanda = ['pg_dump', '-d', d['NAME']]
    if d.get('USER'):
        komanda += ['-U', d['USER']]
    if d.get('HOST'):
        komanda += ['-h', d['HOST']]
    if d.get('PORT'):
        komanda += ['-p', str(d['PORT'])]
    with open(kelias, 'wb') as f:
        subprocess.check_call(komanda, stdout=f, env=aplinka, timeout=3600)
    if os.path.getsize(kelias) < 1024:
        raise RuntimeError('pg_dump sukūrė įtartinai mažą failą: %s' % kelias)
    return kelias


class Command(BaseCommand):
    help = ('Suranda aktyvius skelbimus be nuotraukų, bando prisegti diske '
            'rastus failus, o likusius (tik savus) ištrina.')

    def add_arguments(self, parser):
        parser.add_argument('--atkurti', action='store_true',
                            help='prisegti diske rastus failus')
        parser.add_argument('--uzmigdyk', action='store_true',
                            help='perjungti į „Neaktyvus" (dingsta iš paieškos, '
                                 'lieka savininkui ir DB)')
        parser.add_argument('--trinti', action='store_true',
                            help='IŠTRINTI tuos, kurių atkurti nepavyko (tik savus). '
                                 'Beveik visada geriau --uzmigdyk.')
        parser.add_argument('--savininkai', default=','.join(SAVI),
                            help='kieno skelbimus leidžiama trinti (kableliais)')

    def handle(self, *args, **n):
        savi = {e.strip().lower() for e in n['savininkai'].split(',') if e.strip()}
        atmintine = _media_zemelapis()
        self.stdout.write('media/ failų indeksas: %d' % len(atmintine))

        radiniai = surink(atmintine)
        if not radiniai:
            self.stdout.write(self.style.SUCCESS(
                'Aktyvių skelbimų be nuotraukų nėra.'))
            return

        # ── a. Sąrašas ──────────────────────────────────────────────
        self.stdout.write('\n%-13s %6s  %-30s %-14s %-26s %-10s %s' % (
            'LENTELĖ', 'ID', 'PAVADINIMAS', 'KATEGORIJA', 'SAVININKAS',
            'SUKURTA', 'BŪKLĖ'))
        for r in radiniai:
            self.stdout.write('%-13s %6s  %-30s %-14s %-26s %-10s %s (%d/%d)' % (
                r['lentele'], r['id'], r['pavadinimas'][:30], r['kategorija'][:14],
                r['savininkas'][:26],
                r['sukurta'].strftime('%Y-%m-%d') if r['sukurta'] else '—',
                r['bukle'], r['dingusiu'], r['nuotrauku']))

        # ── b. Atkūrimas ────────────────────────────────────────────
        atkurti, liko = [], []
        for r in radiniai:
            kiek = 0
            if n['atkurti'] and r['atkuriamu']:
                kiek = atkurk(r, atmintine)
            elif r['atkuriamu']:
                kiek = r['atkuriamu']           # tik parodom, ką atkurtume
            if kiek and kiek == r['dingusiu']:
                r['atkurta'] = kiek
                atkurti.append(r)
            else:
                liko.append(r)

        # ── Kieno jie? Savininkų pjūvis rodomas VISADA ───────────────
        mano = [r for r in radiniai if r['savininkas'].lower() in savi]
        kitu = [r for r in radiniai if r['savininkas'].lower() not in savi]
        self.stdout.write('\nIš viso %d: mano paskyrų %d, kitų vartotojų %d'
                          % (len(radiniai), len(mano), len(kitu)))
        if kitu:
            pagal = {}
            for r in kitu:
                pagal[r['savininkas']] = pagal.get(r['savininkas'], 0) + 1
            for adresas, kiek in sorted(pagal.items(), key=lambda p: -p[1]):
                self.stdout.write('    %-34s %d' % (adresas, kiek))

        if not n['atkurti']:
            self.stdout.write(self.style.WARNING(
                '\nTik peržiūra. Atkurtų: %d, liktų: %d. '
                'Veiksmui pridėk --atkurti [--uzmigdyk|--trinti].'
                % (len(atkurti), len(liko))))
            self._santrauka(atkurti, liko, savi, [], [], [])
            return

        # ── c. Užmigdymas arba trynimas ─────────────────────────────
        # Užmigdymas yra numatytas kelias: skelbimas dingsta iš paieškos,
        # bet lieka savininkui. Trynimas — tik jei to paprašyta atskirai.
        veikiami = [r for r in liko if r['savininkas'].lower() in savi]
        svetimi = [r for r in liko if r['savininkas'].lower() not in savi]
        uzmigdyti, istrinti = [], []

        if n['uzmigdyk'] and veikiami:
            for r in veikiami:
                uzmigdyk(r)
                uzmigdyti.append(r)
        elif n['trinti'] and veikiami:
            kelias = atsargine_kopija()
            self.stdout.write(self.style.SUCCESS(
                'Atsarginė kopija: %s (%d B)' % (kelias, os.path.getsize(kelias))))
            for r in veikiami:
                r['objektas'].delete()
                istrinti.append(r)

        self._santrauka(atkurti, liko, savi, istrinti, svetimi, uzmigdyti)

    def _santrauka(self, atkurti, liko, savi, istrinti, svetimi, uzmigdyti=()):
        self.stdout.write('\n%-13s %6s  %-34s %s' % ('LENTELĖ', 'ID', 'PAVADINIMAS', 'KAS PADARYTA'))
        for r in atkurti:
            self.stdout.write('%-13s %6s  %-34s nuotraukos pridėtos (%d)'
                              % (r['lentele'], r['id'], r['pavadinimas'][:34],
                                 r.get('atkurta', r['atkuriamu'])))
        for r in uzmigdyti:
            self.stdout.write('%-13s %6s  %-34s UŽMIGDYTAS -> Neaktyvus (liko savininkui)'
                              % (r['lentele'], r['id'], r['pavadinimas'][:34]))
        for r in istrinti:
            self.stdout.write('%-13s %6s  %-34s IŠTRINTAS (nuotraukų atkurti nepavyko)'
                              % (r['lentele'], r['id'], r['pavadinimas'][:34]))
        for r in svetimi:
            self.stdout.write('%-13s %6s  %-34s paliktas — svetimas (%s)'
                              % (r['lentele'], r['id'], r['pavadinimas'][:34],
                                 r['savininkas']))
        neistrinti = [r for r in liko if r not in istrinti
                      and r not in svetimi and r not in uzmigdyti]
        for r in neistrinti:
            self.stdout.write('%-13s %6s  %-34s paliktas — trynimas neįjungtas (--trinti)'
                              % (r['lentele'], r['id'], r['pavadinimas'][:34]))
        self.stdout.write('\nIš viso: pridėta %d, užmigdyta %d, ištrinta %d, palikta %d'
                          % (len(atkurti), len(uzmigdyti), len(istrinti),
                             len(svetimi) + len(neistrinti)))
