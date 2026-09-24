# -*- coding: utf-8 -*-
"""Bandomieji skelbimai redagavimo formų patikrai (docs/redagavimo_*).

Kuriama po vieną kiekvienos kategorijos, kurios redagavimo formą
tikrinam. Idempotentiška: paleidus antrą kartą tie patys skelbimai
randami pagal `title`, o ne dubliuojami.
"""
from decimal import Decimal

from django.contrib.auth import get_user_model

from apps.listings.models import (FuelType, Listing, MotorcycleBrand,
                                  SubCategory, Transmission, VehicleType,
                                  WheelListing)

SLAPTAZODIS = 'Patikra123!'
PASTAS = 'patikra@autoleft.lt'

# (raktas, VehicleType slug, SubCategory slug arba None, antraštė)
KATEGORIJOS = [
    ('cars',        'cars',         None,                          'Patikra automobilis'),
    ('boats',       'boats',        None,                          'Patikra valtis'),
    ('trailers',    'trailers',     None,                          'Patikra priekaba'),
    ('agriculture', 'agriculture',  None,                          'Patikra traktorius'),
    ('construction', 'construction', 'excavators',                 'Patikra ekskavatorius'),
    ('attachment',  'construction', 'construction-attachments',    'Patikra kaušas'),
    ('electronics', 'electronics',  None,                          'Patikra navigacija'),
    ('services',    'services',     None,                          'Patikra paslauga'),
    ('bicycles',    'bicycles',     None,                          'Patikra dviratis'),
    ('rental',      'rental',       'car-rental',                  'Patikra nuomos auto'),
    ('motogear',    'motorcycles',  'helmets',                     'Patikra šalmas'),
    ('motopart',    'parts',        'single-moto-part',            'Patikra moto dalis'),
]


def _vt(slug):
    vt, _ = VehicleType.objects.get_or_create(
        slug=slug, defaults={'name': slug.title()})
    return vt


def _sub(vt, slug):
    if not slug:
        return None
    sub, _ = SubCategory.objects.get_or_create(
        vehicle_type=vt, slug=slug, defaults={'name': slug.replace('-', ' ').title()})
    return sub


def zinynai():
    """Sąrašai, be kurių formos neišsisaugo (tušti select'ai = privalomas
    laukas be nė vienos pasirinkimo galimybės)."""
    FuelType.objects.get_or_create(name='Dyzelinas')
    Transmission.objects.get_or_create(name='Mechaninė')
    MotorcycleBrand.objects.get_or_create(slug='honda', defaults={'name': 'Honda'})


def vartotojas():
    U = get_user_model()
    u = U.objects.filter(email=PASTAS).first()
    if not u:
        u = U.objects.create_user(username='patikra', email=PASTAS,
                                  password=SLAPTAZODIS)
    u.set_password(SLAPTAZODIS)
    u.is_active = True
    u.save()
    return u


def skelbimai():
    """Grąžina {raktas: Listing}."""
    zinynai()
    u = vartotojas()
    isvestis = {}
    for raktas, vt_slug, sub_slug, antraste in KATEGORIJOS:
        vt = _vt(vt_slug)
        sub = _sub(vt, sub_slug)
        # Ne pagal title: formos po išsaugojimo jį persirenka iš markės ir
        # modelio, todėl antrą kartą nebesusirastų ir sėtų vis naujus.
        # (vehicle_type, subcategory) šiame rinkinyje yra unikalu.
        l = Listing.objects.filter(seller=u, vehicle_type=vt,
                                   subcategory=sub).first()
        if not l:
            l = Listing(seller=u)
        l.title = l.title or antraste
        l.vehicle_type = vt
        l.subcategory = sub
        l.year = 2019
        l.mileage = 120000
        l.price = Decimal('4300.00')
        l.city = 'Vilnius'
        l.country = 'LT'
        l.condition = 'used'
        l.description = 'Pradinis aprašymas.'
        l.status = 'active'
        l.seller_name = 'Patikra'
        l.seller_phone = '+37060000000'
        l.seller_email = PASTAS
        l.save()
        isvestis[raktas] = l
    return isvestis


def ratai():
    """Grąžina {'tyre': WheelListing, 'rim': WheelListing}."""
    u = vartotojas()
    isvestis = {}
    for tipas, antraste in (('tyre', 'Patikra padanga'), ('rim', 'Patikra ratlankis')):
        # Ne pagal title: wheels_edit po išsaugojimo perrašo jį
        # build_title() rezultatu, todėl antrą kartą nebesusirastų ir
        # sėtų naujus skelbimus be galo.
        w = WheelListing.objects.filter(
            seller=u, product_type=tipas, model_name='Hakka').first()
        if not w:
            w = WheelListing(seller=u, title=antraste)
        w.product_type = tipas
        w.brand_name = 'Nokian' if tipas == 'tyre' else 'BBS'
        w.model_name = 'Hakka'
        w.purpose = 'car'
        w.diameter = 'R17'
        w.condition = 'used'
        w.quantity = 4
        w.price = Decimal('120.00')
        w.description = 'Pradinis aprašymas.'
        w.city = 'Vilnius'
        w.country = 'LT'
        w.status = 'active'
        if tipas == 'tyre':
            w.tyre_width, w.tyre_profile, w.tyre_season = '205', '55', 'summer'
        else:
            w.rim_width, w.rim_pcd, w.rim_bolt_count = '7.5', '5x112', '5'
            w.rim_et = 35
            w.rim_dia = Decimal('66.6')
            w.rim_material = 'alloy'
        w.title = antraste
        w.save()
        isvestis[tipas] = w
    return isvestis
