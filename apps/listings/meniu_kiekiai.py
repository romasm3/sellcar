# -*- coding: utf-8 -*-
"""
KATEGORIJŲ MENIU SKAITLIUKAI — VIENA VIETA.

Iki šiol kiekvienas meniu skaičiavo savaip: „…" sąrašas iš `_vt_counts`,
ratų iškrentantis sąrašas iš `titulinis.ratu_kiekiai()`, dalių — iš
`parts_panel_context()`, o motociklų sąrašas ir sunkiojo transporto
sekcijos neturėjo skaitliukų išvis (vilkikų slug'as „tractor-units" nėra
VehicleType, todėl `_vt_counts` jam visada grąžindavo 0).

Dabar visi skaičiai ateina iš čia, o `tikrinti_meniu` komanda tą patį
perskaičiuoja atskirai ir palygina — jei kur nors vėl atsirastų antras
skaičiavimo būdas, komanda tai parodys.

Raktai plokšti:
    'cars', 'motorcycles', 'motogear', 'moto-tyres', 'quad-tyres', …
    '<kategorija>:<sekcija>'  →  'trucks:semi-trucks-tractors',
                                 'wheels:tyre', 'parts:moto'
"""
from django.db.models import Count

# Sunkiojo transporto sekcijos: adreso ?sekcija= reikšmė → subkategorijos
# slug'as. Sutampa (žr. context_processors.SECTIONS), bet vardijam
# aiškiai, kad meniu ir DB ryšys nesiremtų sutapimu.
TRUCK_SEKCIJOS = {
    'semi-trucks-tractors': 'semi-trucks-tractors',
    'buses': 'buses',
    'vehicle-transporters': 'vehicle-transporters',
    'municipal-transport': 'municipal-transport',
}

RENTAL_SEKCIJOS = {
    'car-rental': 'car-rental',
    'limo-wedding-rental': 'limo-wedding-rental',
    'motorcycle-rental': 'motorcycle-rental',
    'minibus-touring-water-rental': 'minibus-touring-water-rental',
    'heavy-trailer-rental': 'heavy-trailer-rental',
}


def kiekiai(user=None):
    """Visi meniu skaitliukai viename žodyne.

    Importai viduje: modulis kviečiamas iš `views.py`, o jame gyvena
    `_public_listings_qs`, tad viršuje būtų ciklinis importas.
    """
    from .models import WheelListing
    from .views import _public_listings_qs
    from . import motogear_views
    from .search_panel import parts_panel_context

    vieši = _public_listings_qs(user)
    k = {}

    # ─── Kategorijos (VehicleType) ───
    for eil in vieši.values('vehicle_type__slug').annotate(c=Count('id')):
        if eil['vehicle_type__slug']:
            k[eil['vehicle_type__slug']] = eil['c']

    # ─── Motociklai be aprangos ───
    # Apranga gyvena po „motorcycles" tipu, bet meniu yra atskiras
    # punktas, todėl iš motociklų ją atimam — kitaip tas pats skelbimas
    # būtų suskaičiuotas dukart.
    k['motogear'] = motogear_views._moto_gear_public_qs(user).count()
    k['motorcycles'] = max(0, k.get('motorcycles', 0) - k['motogear'])

    # ─── Ratai (atskira lentelė) ───
    ratai = WheelListing.objects.filter(is_shadow_banned=False, status='active')
    pagal_tipa = dict(ratai.values_list('product_type').annotate(n=Count('id')))
    k['wheels:tyre'] = pagal_tipa.get('tyre', 0)
    k['wheels:rim'] = pagal_tipa.get('rim', 0)
    k['wheels'] = k['wheels:tyre'] + k['wheels:rim']

    pagal_paskirti = dict(
        ratai.filter(product_type='tyre').values_list('purpose').annotate(n=Count('id')))
    k['moto-tyres'] = pagal_paskirti.get('moto', 0)
    k['quad-tyres'] = pagal_paskirti.get('quad', 0)

    # ─── Sekcijos pagal subkategoriją (sunkusis, nuoma, statybinė) ───
    pagal_sub = {
        eil['subcategory__slug']: eil['c']
        for eil in (vieši.filter(subcategory__isnull=False)
                    .values('subcategory__slug').annotate(c=Count('id')))
    }
    for sekcija, slug in TRUCK_SEKCIJOS.items():
        k['trucks:' + sekcija] = pagal_sub.get(slug, 0)
    for sekcija, slug in RENTAL_SEKCIJOS.items():
        k['rental:' + sekcija] = pagal_sub.get(slug, 0)
    k['construction:construction-attachments'] = pagal_sub.get(
        'construction-attachments', 0)

    # „Pagrindinė" sunkiojo sekcija — visa, kas nepriklauso nė vienai
    # įvardytai sekcijai.
    k['trucks:main'] = max(0, k.get('trucks', 0)
                           - sum(k['trucks:' + s] for s in TRUCK_SEKCIJOS))

    # ─── Paslaugos: automobilių supirkimas ───
    k['services:car-buying'] = vieši.filter(
        vehicle_type__slug='services', service_type='car_buying').count()

    # ─── Dalys: tos pačios penkios subkategorijos kaip panelėje ───
    try:
        for sub in parts_panel_context(user)['parts_subs']:
            k['parts:' + sub['key']] = sub['count']
    except Exception:          # skaičius neturi griauti puslapio
        pass

    return k
