"""Kategorijų medžio suvienodinimas su etaloniniu (autogidas) sąrašu.

Grynai DUOMENŲ migracija — schema nekeičiama, slug'ai nekeičiami, todėl
redirect'ų nereikia.

Ką daro:
  1. VehicleType.order  → etaloninė 1–18 tvarka (planes/planes-parts 19–20,
     į Sunkųjį transportą sugerti tractor-units/car-carriers/municipal → 90+).
  2. Sukuria 7 trūkstamas subkategorijas (Autobusai, Komunalinio ūkio
     transportas, 2× Dalys, 2× Nuoma, Statybinė technika).
  3. Perkelia 'buses' iš vans VT į trucks VT (0 skelbimų).
  4. Sunumeruoja subkategorijų order — anksčiau beveik visur buvo 0, todėl
     jos rikiavosi abėcėle.

Skelbimai NEJUDINAMI: visos paliestos subkategorijos turi 0 skelbimų
(patikrinta prieš rašant), o esamos su skelbimais (trucks=12, car-parts
šaka=26) tik gauna order reikšmę.

reverse_code palieka duomenis (naujos subkategorijos nešalinamos) — jos
tuščios ir nekenkia, o trynimas būtų CASCADE.
"""
from django.db import migrations


# slug → order (etaloninė tvarka)
VEHICLE_TYPE_ORDER = {
    'cars': 1,
    'motorcycles': 2,
    'tires': 3,
    'parts': 4,
    'agriculture': 5,
    'vans': 6,
    'trucks': 7,
    'trailers': 8,
    'rental': 9,
    'electronics': 10,
    'services': 11,
    'car-buying': 12,
    'loading-equipment': 13,
    'construction': 14,
    'forestry': 15,
    'camping-houses': 16,
    'boats': 17,
    'bicycles': 18,
    # Etalone nėra, bet paliekamos matomos su „Netrukus“
    'planes': 19,
    'planes-parts': 20,
    # Sugerti į „Sunkusis transportas“ subkategorijomis — nebepublikuojami
    'tractor-units': 90,
    'car-carriers': 91,
    'municipal': 92,
}

# (vehicle_type_slug, subcategory_slug, name, order)
# name = msgid; vertimai gyvena locale/<lang>/LC_MESSAGES/django.po
NEW_SUBCATEGORIES = [
    ('trucks', 'municipal-transport', 'Komunalinio ūkio transportas', 5),
    ('parts',  'agri-special-parts',  'Žemės ūkio, spec. dalys',      4),
    ('parts',  'accessories-tuning',  'Aksesuarai, Tuning',           5),
    ('rental', 'car-rental',          'Automobilių nuoma',            1),
    ('rental', 'minibus-touring-water-rental',
     'Mikroautobusų, turistinio, vandens tr. nuoma',                  4),
    ('construction', 'construction-machinery', 'Statybinė technika',  1),
]

# (vehicle_type_slug, subcategory_slug, order)
SUBCATEGORY_ORDER = [
    ('motorcycles', 'motorcycles', 1),
    ('motorcycles', 'moto-gear', 2),
    ('tires', 'tyres', 1),
    ('tires', 'rims', 2),
    ('parts', 'car-parts', 1),
    ('parts', 'moto-parts', 2),
    ('parts', 'truck-parts', 3),
    ('trucks', 'trucks', 1),
    ('trucks', 'semi-trucks-tractors', 2),
    ('trucks', 'vehicle-transporters', 3),
    ('trucks', 'buses', 4),
    ('rental', 'limo-wedding-rental', 2),
    ('rental', 'motorcycle-rental', 3),
    ('rental', 'heavy-trailer-rental', 5),
    ('construction', 'construction-attachments', 2),
]


def apply_tree(apps, schema_editor):
    VehicleType = apps.get_model('listings', 'VehicleType')
    SubCategory = apps.get_model('listings', 'SubCategory')

    for slug, order in VEHICLE_TYPE_ORDER.items():
        VehicleType.objects.filter(slug=slug).update(order=order)

    # ─── 'buses' iš vans → trucks (Autobusai tampa Sunkiojo transporto šaka) ───
    trucks_vt = VehicleType.objects.filter(slug='trucks').first()
    vans_vt = VehicleType.objects.filter(slug='vans').first()
    if trucks_vt and vans_vt:
        buses = SubCategory.objects.filter(
            vehicle_type=vans_vt, slug='buses'
        ).first()
        # Nekeliam, jei trucks jau turi 'buses' (idempotencija)
        already = SubCategory.objects.filter(
            vehicle_type=trucks_vt, slug='buses'
        ).exists()
        if buses and not already:
            buses.vehicle_type = trucks_vt
            buses.order = 4
            buses.save(update_fields=['vehicle_type', 'order'])

    for vt_slug, sub_slug, name, order in NEW_SUBCATEGORIES:
        vt = VehicleType.objects.filter(slug=vt_slug).first()
        if not vt:
            continue
        SubCategory.objects.update_or_create(
            vehicle_type=vt, slug=sub_slug,
            defaults={'name': name, 'order': order, 'parent': None},
        )

    for vt_slug, sub_slug, order in SUBCATEGORY_ORDER:
        SubCategory.objects.filter(
            vehicle_type__slug=vt_slug, slug=sub_slug
        ).update(order=order)


def noop_reverse(apps, schema_editor):
    """Atbulinis žingsnis duomenų neliečia.

    order reikšmės ir naujos (tuščios) subkategorijos nekenkia, o jų
    trynimas būtų CASCADE. Jei tikrai reikia atsukti — daroma rankiniu būdu.
    """
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0057_euro_standard_other'),
    ]

    operations = [
        migrations.RunPython(apply_tree, noop_reverse),
    ]
