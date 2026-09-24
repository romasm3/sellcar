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

    for paskirtis, kiek in (('moto', 2), ('quad', 1)):
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

    print('\n— Formatas')
    skliaustuose = re.findall(r'text-gray-400">\((\d+)\)</span>', turinys)
    tikrink(not skliaustuose, 'niekur nebeliko skaičiaus skliausteliuose',
            f'rasta: {skliaustuose[:5]}')
    nuliai = [v['vardas'] for v in rasta.values() if v['n'] == '0']
    tikrink(bool(nuliai), 'nuliai rodomi, o ne slepiami',
            'nė vienas punktas nerodo 0 — patikra neinformatyvi')
    tuscias = [v['vardas'] for v in rasta.values() if not v['n']]
    tikrink(not tuscias, 'nė vienas skaičius nėra tuščias', f'{tuscias[:5]}')

    print(f'\n════ {gerai} gerai / {blogai} blogai ════')
    return 1 if blogai else 0


if __name__ == '__main__':
    sys.exit(main())
