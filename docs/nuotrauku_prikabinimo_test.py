# -*- coding: utf-8 -*-
"""
NUOTRAUKŲ PRIKABINIMAS IŠ URL — manage.py prikabink_nuotraukas.

Testas nuo interneto nepriklauso: paleidžiamas vietinis HTTP serveris,
kuris atiduoda du JPEG, vieną HTML ir vieną per didelį „paveikslėlį".

Tikrinam:
  • 2 URL → 2 nuotraukos; tvarka kaip URL eilė; pirma — pagrindinė;
    miniatiūros pagamintos (tas pats kelias kaip formos įkėlimas)
  • pakartojus tuos pačius → 0 naujų (SHA-256 dublikatai)
  • tas pats URL du kartus tame pačiame paleidime → vienas
  • ne paveikslėlio URL (text/html) → praleista, komanda nekrenta
  • per didelis (≥ 20 MB) → praleista
  • --dry-run → DB nepakitusi
  • --pakeisti → esamos ištrinamos, lieka tik naujos (pirma — pagrindinė);
    visi URL blogi → esamos NELIEČIAMOS; su --dry-run → DB nepakitusi

Paleidimas (TIK su laikina sqlite baze, NE prieš produkcijos DB):
    PATIKRA_DB=<laikinas failas> python docs/nuotrauku_prikabinimo_test.py
Failai rašomi į laikiną MEDIA_ROOT.
"""
import os
import sys
import tempfile

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sqlite_settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'patikra'))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

import io                                            # noqa: E402
import threading                                     # noqa: E402
from decimal import Decimal                          # noqa: E402
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer  # noqa: E402

from django.core.management import call_command      # noqa: E402
from django.test import override_settings            # noqa: E402
from PIL import Image                                # noqa: E402

import formu_seed                                    # noqa: E402
from apps.listings.models import Listing, VehicleType  # noqa: E402

MEDIA = tempfile.mkdtemp(prefix='prikabinimo_media_')

gerai = blogai = 0


def tikrink(salyga, tekstas, papildomai=''):
    global gerai, blogai
    if salyga:
        gerai += 1
        print(f'  OK   {tekstas}')
    else:
        blogai += 1
        print(f'  BLOGAI {tekstas}' + (f'\n         {papildomai}' if papildomai else ''))


def jpeg(spalva, dydis=(320, 240)):
    b = io.BytesIO()
    Image.new('RGB', dydis, spalva).save(b, 'JPEG')
    return b.getvalue()


ATSAKYMAI = {
    '/a.jpg': ('image/jpeg', jpeg('red')),
    '/b.jpg': ('image/jpeg', jpeg('blue')),
    '/puslapis': ('text/html; charset=utf-8', b'<html>ne paveikslelis</html>'),
    '/didelis.jpg': ('image/jpeg', b'\xff\xd8' + b'0' * (20 * 1024 * 1024)),
}


class Tvarkykle(BaseHTTPRequestHandler):
    def do_GET(self):
        tipas, kunas = ATSAKYMAI.get(self.path, ('text/plain', b'nera'))
        self.send_response(200 if self.path in ATSAKYMAI else 404)
        self.send_header('Content-Type', tipas)
        self.send_header('Content-Length', str(len(kunas)))
        self.end_headers()
        try:
            self.wfile.write(kunas)
        except (BrokenPipeError, ConnectionResetError):
            pass       # komanda nutraukia per didelio failo siuntimą — taip ir turi būti

    def log_message(self, *a):
        pass


def paleisk(listing, *keliai, dry=False, pakeisti=False):
    out = io.StringIO()
    argumentai = [str(listing.pk)]
    for k in keliai:
        argumentai += ['--url', f'{BAZE}{k}']
    if dry:
        argumentai.append('--dry-run')
    if pakeisti:
        argumentai.append('--pakeisti')
    call_command('prikabink_nuotraukas', *argumentai, stdout=out)
    return out.getvalue()


def main():
    global BAZE
    serveris = ThreadingHTTPServer(('127.0.0.1', 0), Tvarkykle)
    threading.Thread(target=serveris.serve_forever, daemon=True).start()
    BAZE = f'http://127.0.0.1:{serveris.server_address[1]}'

    u = formu_seed.vartotojas()
    vt, _ = VehicleType.objects.get_or_create(slug='parts', defaults={'name': 'Parts'})
    l = Listing.objects.create(seller=u, vehicle_type=vt, title='Patikra prikabinimas',
                               status='draft', price=Decimal('100'), city='Kaunas', country='LT',
                               year=2020, mileage=0)

    print('\n— --dry-run')
    isvestis = paleisk(l, '/a.jpg', '/b.jpg', dry=True)
    tikrink(l.images.count() == 0, f'DB nepakitusi (nuotraukų {l.images.count()})', isvestis)
    tikrink(not os.listdir(MEDIA) or not any(f for _r, _d, f in os.walk(MEDIA)),
            'diske failų neatsirado')

    print('\n— 2 URL → 2 nuotraukos')
    isvestis = paleisk(l, '/a.jpg', '/b.jpg')
    nuotr = list(l.images.order_by('order'))
    tikrink(len(nuotr) == 2, f'2 nuotraukos (yra {len(nuotr)})', isvestis)
    tikrink(len(nuotr) == 2 and nuotr[0].is_main and not nuotr[1].is_main,
            'pirma — pagrindinė, antra — ne')
    tikrink(len(nuotr) == 2 and 'a' in nuotr[0].image.name and 'b' in nuotr[1].image.name,
            'tvarka kaip URL eilė', str([n.image.name for n in nuotr]))
    tikrink(all(n.image_lg and n.image_sm for n in nuotr),
            'miniatiūros pagamintos (image_lg, image_sm)')
    tikrink(all(n.image.name.startswith('listings/') for n in nuotr),
            'tas pats upload_to kaip formos (listings/…)')

    print('\n— Pakartojus tuos pačius → 0 naujų')
    isvestis = paleisk(l, '/a.jpg', '/b.jpg')
    tikrink(l.images.count() == 2 and 'Pridėta: 0' in isvestis and 'dublikatų: 2' in isvestis,
            f'0 naujų, 2 dublikatai (nuotraukų {l.images.count()})', isvestis)

    print('\n— Netinkami URL — praleidžiami, komanda nekrenta')
    try:
        isvestis = paleisk(l, '/puslapis', '/didelis.jpg', '/nera.jpg')
        nukrito = None
    except Exception as e:                           # noqa: BLE001
        isvestis, nukrito = '', e
    tikrink(nukrito is None, 'komanda nenukrito', str(nukrito))
    tikrink('ne paveikslėlis' in isvestis, 'text/html → „ne paveikslėlis"', isvestis)
    tikrink('per didelis' in isvestis, '≥ 20 MB → „per didelis"', isvestis)
    tikrink('praleista: 3' in isvestis and l.images.count() == 2,
            f'praleista 3, nuotraukų liko 2 ({l.images.count()})')

    print('\n— Tas pats URL du kartus viename paleidime')
    l2 = Listing.objects.create(seller=u, vehicle_type=vt, title='Patikra prikabinimas 2',
                                status='draft', price=Decimal('100'), city='Kaunas', country='LT',
                                year=2020, mileage=0)
    isvestis = paleisk(l2, '/a.jpg', '/a.jpg')
    tikrink(l2.images.count() == 1, f'1 nuotrauka (yra {l2.images.count()})', isvestis)

    print('\n— --pakeisti')
    ATSAKYMAI['/c.jpg'] = ('image/jpeg', jpeg('green'))
    pries = sorted(l.images.values_list('pk', flat=True))
    isvestis = paleisk(l, '/c.jpg', dry=True, pakeisti=True)
    tikrink(sorted(l.images.values_list('pk', flat=True)) == pries,
            '--pakeisti --dry-run → DB nepakitusi', isvestis)
    isvestis = paleisk(l, '/puslapis', '/nera.jpg', pakeisti=True)
    tikrink(sorted(l.images.values_list('pk', flat=True)) == pries and 'NELIEČIAMOS' in isvestis,
            'visi URL blogi → esamos neliečiamos', isvestis)
    isvestis = paleisk(l, '/c.jpg', '/a.jpg', pakeisti=True)
    nuotr = list(l.images.order_by('order'))
    tikrink(len(nuotr) == 2 and not set(n.pk for n in nuotr) & set(pries),
            f'esamos 2 ištrintos, liko 2 naujos (yra {len(nuotr)})', isvestis)
    tikrink(len(nuotr) == 2 and 'c' in nuotr[0].image.name and nuotr[0].is_main
            and not nuotr[1].is_main and [n.order for n in nuotr] == [0, 1],
            'tvarka c, a; pirma — pagrindinė; order 0, 1', str([(n.image.name, n.is_main, n.order) for n in nuotr]))
    isvestis = paleisk(l, '/b.jpg')
    tikrink(l.images.count() == 3, f'be --pakeisti — prideda prie esamų (yra {l.images.count()})', isvestis)

    serveris.shutdown()
    print(f'\n════ {gerai} gerai / {blogai} blogai ════')
    return 1 if blogai else 0


if __name__ == '__main__':
    with override_settings(MEDIA_ROOT=MEDIA):
        kodas = main()
    sys.exit(kodas)
