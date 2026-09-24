# -*- coding: utf-8 -*-
"""
KATEGORIJŲ MENIU SKAITLIUKAI: ar meniu rodo tą patį, ką turi DB.

Tikrinam tris dalykus:
  1. septyni punktai, kurie skaičiaus neturėjo visai, dabar jį turi
     (Motociklai, Apranga, Padangos motociklams, Padangos keturračiams,
     Vilkikai, Autotraukiniai, Komunalinis);
  2. formatas vienodas — atskiras pilkas skaičius dešinėje, be
     skliaustelių varde, ir nulis rodomas kaip 0, o ne slepiamas;
  3. skaičius sutampa su tuo, ką duoda apps/listings/meniu_kiekiai.py,
     o tą patį atskirai perskaičiuoja `manage.py tikrinti_meniu`.

Paleidimas (reikia vietinio serverio 127.0.0.1:8899 su TA PAČIA DB):
    PATIKRA_DB=<...> python docs/meniu_skaitliuku_playwright.py
"""
import os
import re
import sys

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sqlite_settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'patikra'))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

from playwright.sync_api import sync_playwright        # noqa: E402

import formu_seed                                      # noqa: E402
from apps.listings.meniu_kiekiai import kiekiai        # noqa: E402
from apps.listings.sekciju_uzklausos import kiek as sekciju_kiek  # noqa: E402

ADRESAS = os.environ.get('ADRESAS', 'http://127.0.0.1:8899')
NARSYKLE = os.environ.get('CHROMIUM',
                          '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')

gerai = blogai = 0


def tikrink(salyga, tekstas, papildomai=''):
    global gerai, blogai
    if salyga:
        gerai += 1
        print(f'  OK   {tekstas}')
    else:
        blogai += 1
        print(f'  BLOGAI {tekstas}' + (f'\n         {papildomai}' if papildomai else ''))


def pasejk():
    """Skelbimai kaip tik tose vietose, kurios anksčiau rodė tuštumą."""
    from decimal import Decimal

    from apps.listings.models import Listing, SubCategory, VehicleType, WheelListing

    formu_seed.zinynai()
    u = formu_seed.vartotojas()

    def vt(slug):
        v, _ = VehicleType.objects.get_or_create(slug=slug,
                                                 defaults={'name': slug.title()})
        return v

    def sub(v, slug):
        s, _ = SubCategory.objects.get_or_create(
            vehicle_type=v, slug=slug,
            defaults={'name': slug.replace('-', ' ').title()})
        return s

    # (vehicle_type, subcategory, kiek)
    planas = [
        ('trucks', 'semi-trucks-tractors', 3),
        ('trucks', 'vehicle-transporters', 2),
        ('trucks', 'municipal-transport', 1),
        ('trucks', None, 2),                 # „main" sekcija
        ('motorcycles', None, 4),
        ('motorcycles', 'helmets', 2),       # apranga
    ]
    for vt_slug, sub_slug, kiek in planas:
        v = vt(vt_slug)
        s = sub(v, sub_slug) if sub_slug else None
        esama = Listing.objects.filter(seller=u, vehicle_type=v, subcategory=s,
                                       title__startswith='Meniu ').count()
        for i in range(max(0, kiek - esama)):
            Listing.objects.create(
                seller=u, vehicle_type=v, subcategory=s,
                title=f'Meniu {vt_slug}-{sub_slug}-{esama + i}',
                year=2019, mileage=1000, price=Decimal('1000'),
                city='Vilnius', country='LT', status='active')

    for paskirtis, kiek in (('moto', 2), ('atv', 1)):
        esami = WheelListing.objects.filter(seller=u, product_type='tyre',
                                            purpose=paskirtis).count()
        for i in range(max(0, kiek - esami)):
            WheelListing.objects.create(
                seller=u, product_type='tyre', purpose=paskirtis,
                brand_name='Meniu', model_name=f'M{i}', diameter='R17',
                condition='used', quantity=4, price=Decimal('50'),
                city='Vilnius', country='LT', status='active',
                title=f'Meniu {paskirtis} {i}')


def meniu_skaiciai(p):
    """{href arba vardas: skaičius} — kaip realiai atiduota puslapyje."""
    return p.evaluate("""() => {
        const isv = {};
        document.querySelectorAll('.sp-rail a, .sp-rail-fixed a').forEach(a => {
            const spans = a.querySelectorAll('span');
            if (!spans.length) { return; }
            const pask = spans[spans.length - 1];
            if (!/text-gray-400/.test(pask.className)) { return; }
            const vardas = (a.innerText || '').split('\\n')[0].trim();
            isv[a.getAttribute('href')] = {n: pask.textContent.trim(), vardas: vardas};
        });
        return isv;
    }""")


# ── Ką tikrinam: (href, meniu_kiekiai raktas, žmogiškas vardas) ──────
PUNKTAI = [
    ('/?section=motorcycles',                          'motorcycles',  'Motociklai'),
    ('/?section=motogear',                             'motogear',     'Apranga, šalmai, aksesuarai'),
    ('/?section=moto-tyres',                           'moto-tyres',   'Padangos motociklams'),
    ('/?section=quad-tyres',                           'quad-tyres',   'Padangos keturračiams'),
    ('/?section=wheels&sekcija=tyre',                  'wheels:tyre',  'Padangos'),
    ('/?section=wheels&sekcija=rim',                   'wheels:rim',   'Ratlankiai'),
]

# „…" sąrašo punktai atpažįstami pagal url (jame yra ?sekcija=)
SEKCIJU_PUNKTAI = [
    ('sekcija=semi-trucks-tractors',  'trucks:semi-trucks-tractors',  'Vilkikai'),
    ('sekcija=vehicle-transporters',  'trucks:vehicle-transporters',  'Autotraukiniai, autovežiai'),
    ('sekcija=municipal-transport',   'trucks:municipal-transport',   'Komunalinio ūkio transportas'),
]


# Sekcija → jos naršymo puslapis (tas pats, į kurį veda panelės mygtukas)
# sekcija → (naršymo puslapis, panelės adresas, panelės id)
# „tires"/„rims" panelė yra bendra — #sp-panel-wheels, tik su kita forma.
BROWSE = {
    'motogear':    ('/browse/motogear/',            '/?section=motogear',              'motogear'),
    'moto-tyres':  ('/browse/tyres/?purpose=moto',  '/?section=moto-tyres',            'moto-tyres'),
    'quad-tyres':  ('/browse/tyres/?purpose=atv',   '/?section=quad-tyres',            'quad-tyres'),
    'tires':       ('/browse/tyres/',               '/?section=wheels&sekcija=tyre',   'wheels'),
    'rims':        ('/browse/rims/',                '/?section=wheels&sekcija=rim',    'wheels'),
    'motorcycles': ('/browse/?category=motorcycles', '/?section=motorcycles',          'motorcycles'),
    'trucks':      ('/browse/?category=trucks',     '/?section=trucks',                'trucks'),
    'boats':       ('/browse/?category=boats',      '/?section=boats',                 'boats'),
}


_instrumentuota = False


def browse_kiekis(kelias):
    """Kiek skelbimų randa TIKRASIS naršymo puslapis.

    `response.context` užpildomas tik kai testų aplinka instrumentuota —
    be `setup_test_environment()` jis visada None.
    """
    global _instrumentuota
    from django.test import Client
    from django.test.utils import setup_test_environment
    if not _instrumentuota:
        setup_test_environment()
        _instrumentuota = True
    a = Client().get(kelias, follow=True)
    if a.status_code != 200 or not a.context:
        return None
    try:
        return a.context['total_count']
    except (KeyError, TypeError):
        return None


def mygtuko_skaicius(p, adresas, panele):
    """„Skelbimai N" panelės mygtuke."""
    p.goto(f'{ADRESAS}{adresas}', wait_until='domcontentloaded')
    try:
        p.wait_for_function(
            "(s) => { const e = document.querySelector('#sp-panel-' + s);"
            " return e && /Skelbimai\\s*\\d/.test(e.innerText); }",
            arg=panele, timeout=10000)
    except Exception:
        pass
    # Skaičius subėga nuo 0 (animateCount), todėl skaitom tik tada, kai
    # dvi iš eilės reikšmės sutampa — kitaip pagautume tarpinę.
    pries = None
    for _ in range(20):
        p.wait_for_timeout(250)
        try:
            t = p.locator(f'#sp-panel-{panele}').inner_text(timeout=5000)
        except Exception:
            return None
        m = re.search(r'Skelbimai\s*(\d+)', t)
        dabar = int(m.group(1)) if m else None
        if dabar is not None and dabar == pries:
            return dabar
        pries = dabar
    return pries


def main():
    pasejk()
    laukiami = kiekiai(None)

    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=NARSYKLE)
        ctx = b.new_context(viewport={'width': 1440, 'height': 950},
                            ignore_https_errors=True)
        p = ctx.new_page()
        p.goto(f'{ADRESAS}/', wait_until='domcontentloaded')
        p.wait_for_timeout(700)
        rasta = meniu_skaiciai(p)
        be_skaiciaus = p.evaluate("""() => {
            const be = [];
            document.querySelectorAll('.sp-rail a.w-full, .sp-rail-fixed a.w-full')
              .forEach(a => {
                const spans = [...a.querySelectorAll('span')];
                const pask = spans[spans.length - 1];
                if (!(pask && /text-gray-400/.test(pask.className))) {
                    be.push((a.innerText || '').split('\\n')[0].trim());
                }
            });
            return be;
        }""")
        turinys = p.content()
        ctx.close()
        b.close()

    print('\n— Septyni punktai, kurie skaičiaus neturėjo')
    for href, raktas, vardas in PUNKTAI:
        įrašas = rasta.get(href)
        tikrink(įrašas is not None, f'{vardas}: skaičius yra',
                f'href={href} sąraše nerastas')
        if įrašas is None:
            continue
        tikrink(įrašas['n'] == str(laukiami.get(raktas, 0)),
                f'{vardas}: rodo {laukiami.get(raktas, 0)}',
                f"rodo {įrašas['n']!r}")

    print('\n— Sunkiojo transporto sekcijos „…" sąraše')
    for fragmentas, raktas, vardas in SEKCIJU_PUNKTAI:
        įrašas = None
        for href, v in rasta.items():
            if href and fragmentas in href:
                įrašas = v
                break
        tikrink(įrašas is not None, f'{vardas}: skaičius yra', f'{fragmentas} nerastas')
        if įrašas is None:
            continue
        tikrink(įrašas['n'] == str(laukiami.get(raktas, 0)),
                f'{vardas}: rodo {laukiami.get(raktas, 0)}',
                f"rodo {įrašas['n']!r}")

    print('\n— Mygtukas, skaitliukas ir naršymo puslapis turi sutapti')
    # DB skaičius imam PRIEŠ naršyklę: Playwright kontekste Django ORM
    # laiko giją asinchronine ir meta SynchronousOnlyOperation.
    is_db = {sek: (sekciju_kiek(sek), browse_kiekis(v[0]))
             for sek, v in BROWSE.items()}

    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=NARSYKLE)
        ctx = b.new_context(viewport={'width': 1440, 'height': 950},
                            ignore_https_errors=True)
        p2 = ctx.new_page()
        mygtukai = {sek: mygtuko_skaicius(p2, v[1], v[2])
                    for sek, v in BROWSE.items()}
        ctx.close()
        b.close()

    for sekcija in BROWSE:
        bendra, narsymas = is_db[sekcija]
        mygtukas = mygtukai[sekcija]
        tikrink(narsymas is not None, f'{sekcija}: naršymo puslapis atsidaro')
        tikrink(bendra == narsymas,
                f'{sekcija}: bendra užklausa = naršymo puslapis ({narsymas})',
                f'bendra {bendra}, naršymas {narsymas}')
        tikrink(mygtukas == narsymas,
                f'{sekcija}: panelės mygtukas = naršymo puslapis ({narsymas})',
                f'mygtukas {mygtukas}, naršymas {narsymas}')

    print('\n— Formatas')
    skliaustuose = re.findall(r'text-gray-400">\((\d+)\)</span>', turinys)
    tikrink(not skliaustuose, 'niekur nebeliko skaičiaus skliausteliuose',
            f'rasta: {skliaustuose[:5]}')
    nuliai = [v['vardas'] for v in rasta.values() if v['n'] == '0']
    tikrink(bool(nuliai), 'nuliai rodomi, o ne slepiami',
            'nė vienas punktas nerodo 0 — patikra neinformatyvi')
    tuscias = [v['vardas'] for v in rasta.values() if not v['n']]
    tikrink(not tuscias, 'nė vienas skaičius nėra tuščias', f'{tuscias[:5]}')
    tikrink(not be_skaiciaus, 'nė vienas meniu punktas neliko be skaičiaus',
            f'{be_skaiciaus[:8]}')

    print(f'\n════ {gerai} gerai / {blogai} blogai ════')
    return 1 if blogai else 0


if __name__ == '__main__':
    sys.exit(main())
