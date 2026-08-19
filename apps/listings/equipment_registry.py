# apps/listings/equipment_registry.py
# ═══════════════════════════════════════════════════════════
# YPATUMŲ (Equipment) REGISTRAS — vienintelis šaltinis.
#
# Kodėl atskiras modulis, o ne views: šiuos apibrėžimus turi matyti
# TRYS vartotojai —
#   • kategorijos view'as (create formos checkbox'ai),
#   • `seed_equipment` management komanda,
#   • duomenų migracija 0063 (kad naujoje aplinkoje eilutės atsirastų
#     pačios, be jokio rankinio žingsnio).
# Migracijos negali importuoti views (jie traukia modelius importo metu),
# todėl čia laikomi GRYNI duomenys — jokių Django importų.
#
# Kategorijos prefiksas ('trailer_', 'agri_', 'load_') yra privalomas:
# tie patys pavadinimai („Hidraulika", „Kabina") kartojasi tarp
# kategorijų, o paieška juos skiria būtent pagal prefiksą
# (search_config.panels.EQUIPMENT_PREFIX).
#
# Nauja kategorija: pridėk įrašą į CATEGORY_EQUIPMENT, paleisk
# `manage.py seed_equipment` ir įrašyk prefiksą į EQUIPMENT_PREFIX.
# ═══════════════════════════════════════════════════════════

TRAILER_EQUIPMENT_DEFINITION = [
    ('trailer_body', 'Kėbulas ir įranga', [
        'EDSCHA stogas',
        'Su kietu stogu',
        'Atitraukiamas stogas',
        'Su palapine',
        'Atitraukiami šonai',
        'Su tentu',
        'Durys gale',
        'Durys šone',
        'Žaliuzės',
        'Liftas gale',
        'Su hidrauliniu kranu',
        'Su gerve',
        'Hidraulika',
        'Įrankių dėžė',
    ]),
    ('trailer_chassis', 'Važiuoklė', [
        'Pakeliama ašis',
        'Pneumatinė pakaba',
        'Diskiniai stabdžiai',
    ]),
    ('trailer_safety', 'Sauga', [
        'ABS',
        'EBS',
        'Priekabos stabdys',
        'Krovinio diržai',
        'TIR',
        'Termografas',
    ]),
    ('trailer_other', 'Kita', [
        'Garantija',
        'Parduodama lizingu',
    ]),
]


AGRI_EQUIPMENT_DEFINITION = [
    ('agri_drivetrain', 'Pavaros ir važiuoklė', [
        'Lėtintos pavaros',
        'Greičio variatorius',
        'Dvigubi ratai',
        'Vikšrinis',
    ]),
    ('agri_mount', 'Prikabinimas', [
        'Prikabinamas',
        'Pakabinamas',
    ]),
    ('agri_other', 'Kita', [
        'ABS',
        'Hidraulika',
        'Kabina',
    ]),
]


LOAD_EQUIPMENT_DEFINITION = [
    ('load_cabin', 'Kabina ir apsauga', [
        'Kabina',
        'Pusiau kabina',
        'Apšildoma kabina',
        'Apsauginis stogelis',
    ]),
    ('load_hydraulics', 'Hidraulika ir mechanizmai', [
        'Hidraulika',
        'Papildomas hidraulikos vožtuvas',
        'Šoninio poslinkio mechanizmas',
        'Pasukamas griebtuvas',
    ]),
    ('load_platform', 'Platforma ir atramos', [
        'Platforma stumiasi į vieną pusę',
        'Platforma stumiasi į abi puses',
        'Sulankstomos atramos',
        'Lingės',
    ]),
    ('load_surface', 'Važiuoklė ir paviršius', [
        'Skirtas tvirtam paviršiui',
        'Skirtas bet kokiam paviršiui',
        'Žemintos pavaros',
    ]),
]


# vehicle_type slug → definicijų sąrašas
CATEGORY_EQUIPMENT = {
    'trailers': TRAILER_EQUIPMENT_DEFINITION,
    'agriculture': AGRI_EQUIPMENT_DEFINITION,
    'loading-equipment': LOAD_EQUIPMENT_DEFINITION,
}


def iter_equipment():
    """(category_key, name) poros visoms kategorijoms."""
    for definition in CATEGORY_EQUIPMENT.values():
        for cat_key, _label, names in definition:
            for name in names:
                yield cat_key, name


def seed(equipment_model):
    """Idempotentiškai sukuria trūkstamas eilutes. Grąžina (sukurta, viso).

    Priima modelio klasę, kad tiktų ir migracijai (apps.get_model), ir
    management komandai (tiesioginis importas).
    """
    created = 0
    total = 0
    for cat_key, name in iter_equipment():
        total += 1
        _obj, was_created = equipment_model.objects.get_or_create(
            category=cat_key, name=name,
        )
        if was_created:
            created += 1
    return created, total
