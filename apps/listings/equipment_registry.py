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


# ─── Turistiniai nameliai ───
# Savi 52 su 'camp_' prefiksu, NE automobilių eilutės: automobilių
# ypatumai suvesti angliškai (Cruise control, Airbags), o šie —
# lietuviškai, tad sutampa tik akronimas „ESP". Be prefikso
# build_advanced() paimtų automobilių ESP eilutę, o nameliai turėtų
# savo — filtras grąžintų 0 rezultatų.
CAMP_EQUIPMENT_DEFINITION = [
    ('camp_electronics', 'Elektronika', [
        '360° vaizdo kamera',
        'Audio grotuvas',
        'Automatinio parkavimo sistema',
        'Kelio ženklų atpažinimo sistema',
        'Kritulių jutiklis',
        'Laisvų rankų įranga',
        'Navigacija / GPS',
        'Nuovargio įspėjimo sistema',
        'Start-Stop sistema',
        'Atstumo jutiklių sistema',
        'Beraktė užvedimo sistema',
        'Galinio vaizdo kamera',
        'Kruizo kontrolė',
    ]),
    ('camp_assist', 'Pagalbos sistemos', [
        'ASR',
        'Borto kompiuteris',
        'Centrinis užraktas',
        'ESP',
        'Vairo stiprintuvas',
    ]),
    ('camp_safety', 'Saugumas ir apsauga', [
        'Aklosios zonos stebėjimo sistema',
        'Atstumo palaikymo sistema',
        'Avarinio stabdymo sistema',
        'Juostos palaikymo sistema',
        'Traukos kontrolės sistema',
        'Oro pagalvės',
        'Signalizacija / Imobilaizeris',
        'Stabilumo kontrolės sistema',
    ]),
    ('camp_interior', 'Salonas', [
        'Autonominis šildymas (webasto)',
        'CD grotuvas',
        'Dujinė viryklė',
        'Dušas',
        'El. langai',
        'El. sėdynės',
        'El. veidrodėliai',
        'Elektroninė klimato kontrolė',
        'Garso aparatūra',
        'Gido mikrofonas',
        'Karštas vanduo',
        'Kavos aparatas',
        'Oro kondicionierius',
        'Šildomas priekinis stiklas',
        'Šildomos sėdynės',
        'Tamsinti stiklai',
        'Tualetas',
        'Video įranga',
    ]),
    ('camp_other', 'Kiti privalumai', [
        'Aukštas',
        'CD keitiklis',
        'Dviračių laikikliai',
        'Geros būklės',
        'Lauko baldai',
        'Skaidraus stiklo priekiniai žibintai',
        'Su prieangiu',
        'Tentas',
    ]),
]


# vehicle_type slug → definicijų sąrašas
# ═══════════════════════════════════════════════════════════
# TRANSPORTO NUOMA — 3 ypatumai, bendri keturioms subkategorijoms
# (motociklų nuoma etalone ypatumų neturi).
#
# Prefiksas 'rent_' privalomas: „Kaina su vairuotoju" ir kiti nuomos
# sąlygų punktai kitose kategorijose neegzistuoja, bet prefiksas laiko
# juos izoliuotus ir ateičiai — žr. panels.EQUIPMENT_PREFIX.
# ═══════════════════════════════════════════════════════════
RENT_EQUIPMENT_DEFINITION = [
    ('rent_terms', 'Nuomos sąlygos', [
        'Kaina su vairuotoju',
        'Nuolaidos ilgesniam laikotarpiui',
        'Nuomojamas tik su vairuotoju',
    ]),
]


# ═══════════════════════════════════════════════════════════
# PASLAUGOS — 18 varnelių iš etalono „Papildomi duomenys" bloko.
#
# Etalono paieškoje jų nėra (sec 18 filtruoja tik tipą, miestą ir tekstą),
# bet skelbime jos rodomos, todėl saugom kaip Equipment eilutes.
# Prefiksas 'svc_' — „Ratų remontas" ir „Kita" pavadinimai lengvai
# susikirstų su kitomis kategorijomis (žr. panels.EQUIPMENT_PREFIX).
# ═══════════════════════════════════════════════════════════
SVC_EQUIPMENT_DEFINITION = [
    ('svc_repair', 'Remontas ir diagnostika', [
        'Bamperių remontas',
        'Dažymo paslaugos',
        'Duslintuvų remontas',
        'Elektronikos diagnostika',
        'Hidraulikos diagnostika',
        'Kėbulo remontas',
        'Pavarų dėžių remontas',
        'Turbinų diagnostika',
        'Ratų remontas',
        'Salono remontas',
        'Starterių, generatorių remontas',
        'Ratų montavimas, balansavimas',
        'Variklių diagnostika',
        'Važiuoklės remontas',
        'Autobusų, sunkvežimių remontas',
        'Motociklų, motorolerių remontas',
    ]),
    ('svc_other', 'Kita', [
        'Vežame į užsienį',
        'Kita',
    ]),
]


# ═══════════════════════════════════════════════════════════
# VIDEO, AUDIO, NAVIGACIJOS — 16 ypatumų (etalonas sec 15).
#
# Prefiksas 'elec_'. Automobilių ypatumų kategorija vadinasi
# 'electronics' — be pabraukimo prefikse ji irgi pakliūtų į
# startswith() filtrą, todėl pabraukimas čia būtinas.
# ═══════════════════════════════════════════════════════════
ELEC_EQUIPMENT_DEFINITION = [
    ('elec_features', 'Ypatumai', [
        '“Subwoofer” valdymas',
        'AUX jungtis',
        'Ekvalaizeris',
        'Galinė dalis',
        'Korteliu skaitytuvas',
        'LCD ekranas',
        'Liečiamas ekranas',
        'Linijiniai išėjimai',
        'Multifunkcinis valdymas nuo vairo',
        'Neveikiantis',
        'Nuotolinio valdymo pultas',
        'Priekinis skydelis',
        'Spalvotas ekranas',
        'USB jungtis',
        'Valdymas ratuku',
        'Vidinė atmintis',
    ]),
]


CATEGORY_EQUIPMENT = {
    'trailers': TRAILER_EQUIPMENT_DEFINITION,
    'agriculture': AGRI_EQUIPMENT_DEFINITION,
    'loading-equipment': LOAD_EQUIPMENT_DEFINITION,
    'camping-houses': CAMP_EQUIPMENT_DEFINITION,
    'rental': RENT_EQUIPMENT_DEFINITION,
    'services': SVC_EQUIPMENT_DEFINITION,
    'electronics': ELEC_EQUIPMENT_DEFINITION,
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
