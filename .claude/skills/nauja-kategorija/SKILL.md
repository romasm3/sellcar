---
name: nauja-kategorija
description: Pilna skelbimų kategorijos vertikalė AutoLeft projekte — create forma, greitoji paieškos panelė, išplėstinė paieška, naršymo kortelės ir detalės puslapis. Naudok, kai reikia įgyvendinti naują VehicleType kategoriją (žemės ūkis, statybinė technika, nuoma, paslaugos ir pan.) arba užbaigti pusiau padarytą.
---

# Nauja kategorija — pilna vertikalė

Tikslas: **sukurti · rasti · peržiūrėti**. Kategorija nelaikoma padaryta, kol
veikia visi penki sluoksniai: create forma, greitoji panelė, išplėstinė
paieška, naršymo kortelės ir detalės puslapis.

Etalonai, iš kurių paimtas šis procesas: `trailers` (0f84e02, 50b75a2),
`agriculture` (431842c), `construction` (40a5ed7), `loading-equipment`
(be266df) ir `forestry` (208486a).

Greitas orientyras, kurį etaloną kopijuoti:

| Kategorija panaši į… | Imk bazę |
|---|---|
| viena forma, subkategorijos, ypatumai | `trailers` / `agriculture` |
| viena forma, BE subkategorijų | `loading-equipment` |
| viena forma, BE ypatumų ir BE mėnesio | `forestry` |
| DVI formos vienam VT | `construction` |

---

## 0. Prieš rašant kodą — visada

### Sek `boats` patterną, NE `trucks`

| | `boats_views.py` ✅ | `trucks_views.py` ❌ |
|---|---|---|
| Srautas | vienas view, create+edit per vieną POST | draft session (`TRUCKS_DRAFT_SESSION_KEY`), autosave |
| Sudėtingumas | ~360 eil. | ~1150 eil. |
| Žinomos klaidos | nėra | hardcodino `subcategory='trucks'`, `?subcategory=` ignoruotas |

`trailers_views.py` ir `agriculture_views.py` — tiesioginės `boats` kopijos
su pakeistais laukais. Imk artimiausią jau padarytą kategoriją kaip bazę.

### Padaryk laukų auditą PRIEŠ migraciją

Daugumą laukų jau turi `Listing`. `agriculture` atveju: **perpanaudota 14,
naujų prireikė tik 6**.

```bash
venv/bin/python -c "
import django,os,sys; sys.path.insert(0,'/root/autoleft')
os.environ.setdefault('DJANGO_SETTINGS_MODULE','config.settings'); django.setup()
from apps.listings.models import Listing
for f in Listing._meta.get_fields():
    if hasattr(f,'get_internal_type'): print(f.name, f.get_internal_type())"
```

Dažniausiai perpanaudojama:

| Specifikacija | `Listing` laukas |
|---|---|
| Pavadinimas · Komentarai | `title` · `description` |
| Būklė | `condition` |
| Metai · Mėnuo | `year` · `first_registration` (diena=1) |
| Kaina · eksportui · + Mokesčiai | `price` · `export_price` · `taxes_extra` |
| SDK · VIN | `sdk_number` · `vin` |
| Galia kW | `power` (IntegerField) |
| Masės | `curb_weight` · `gross_weight_kg` · `payload_kg` |
| Matmenys · Tūris | `truck_length_mm/width/height` · `truck_volume_m3` |
| Euro · TA · Spalva | `euro_standard` · `technical_inspection_year/month` · `color` |

**Diapazoniniai filtrai reikalauja skaitinių laukų.** Jei specifikacija sako
„Galia, kW" ir tam yra `power` (Integer) — puiku. Jei naujas laukas bus
filtruojamas diapazonu, kurk jį `IntegerField`/`DecimalField`, ne `CharField`.

### Klausimai, kuriuos užduoti prieš kodą

1. **Migracija ir jos paleidimas.** Vos pakeitus `models.py`, produkcija
   tampa traši: gunicorn sukasi ant seno kodo, bet bet koks jo perkrovimas
   prieš `migrate` mes 500 visame puslapyje. Klausk iš karto:
   generuoti+paleisti dabar (rekomenduojama, additive `ADD COLUMN` yra
   metadata-only, be prastovos) ar palikti nepaleistą.
2. **Bendrų `choices` plėtimas.** Jei kategorijos reikšmių sąrašas platesnis
   už esamą bendrą (pvz. Spalva 15 vs mūsų 11), klausk: plėsti visoms
   kategorijoms ar naudoti esamą. Plėtimas paliečia automobilius,
   motociklus ir kt.
3. **Subkategorijų mapping'as**, jei kuri nors DB subkategorija lieka be
   atitikmens — pasakyk ir pasiūlyk palikti tuščią, o ne priskirti klaidingai.

---

## 1. Modelis ir migracija

Laukų vardai su kategorijos prefiksu: `agri_type`, `trailer_kind`. Visi
`blank=True` / `null=True` — additive migracija, esamoms eilutėms poveikio nėra.

```bash
venv/bin/python manage.py makemigrations listings --name <kategorija>_fields
venv/bin/python manage.py sqlmigrate listings 00XX   # parodyk vartotojui
# tik po patvirtinimo:
venv/bin/python manage.py migrate listings && systemctl restart gunicorn
```

---

## 2. Create forma

Failai: `apps/listings/<kategorija>_views.py` +
`templates/listings/<kategorija>_listing_create.html`.

### Subkategorijos: pirma nustatyk, KURIS iš trijų atvejų

```bash
venv/bin/python -c "
import django,os,sys; sys.path.insert(0,'/root/autoleft')
os.environ.setdefault('DJANGO_SETTINGS_MODULE','config.settings'); django.setup()
from apps.listings.models import SubCategory
print(list(SubCategory.objects.filter(vehicle_type__slug='<slug>').values_list('slug',flat=True)))"
```

| Atvejis | Ką daryti | Pavyzdys |
|---|---|---|
| **Turi subkategorijų** | mapping iš formos lauko, redirect per `<KAT>_SUBCATEGORY_SLUGS` | `trailers`, `agriculture` |
| **NETURI nė vienos** | `subcategory` lieka `NULL`, mapping'o logikos NĖRA, pikeris veda tiesiai į formą per **`CREATE_URL_BY_VEHICLE_TYPE`** | `loading-equipment`, `forestry` |
| **Dvi formos vienam VT** | žr. „Kategorija su dviem formomis" žemiau | `construction` |

**SPĄSTAS: kategorijai be subkategorijų `<KAT>_SUBCATEGORY_SLUGS` redirect
neveiks** — `_route_category_pick()` gauna tuščią `subcategory_slug` ir
nukris į išjungtą 7 žingsnių srautą. Reikia įrašo `CREATE_URL_BY_VEHICLE_TYPE`:

```python
CREATE_URL_BY_VEHICLE_TYPE = {
    ...
    '<slug>': '/create/<slug>/?new=1',
}
```

Nekurk subkategorijų vien tam, kad būtų — jei etaloniniame medyje
kategorija plokščia, subkategorijos pridėtų nereikalingą drill-in žingsnį
pikeryje. Ir atvirkščiai: tuščios subkategorijos, likusios be atitikmens
(`construction/forklifts`, `agriculture/forestry-machines`), paliekamos
kaip yra — 0 skelbimų, pikeryje nerodomos, trynimas CASCADE ir neatstatomas.

### Subkategorija — iš FORMOS, ne iš URL

Tai dažniausia klaida projekte (buvo `trucks` ir `parts`).

```python
AGRI_TYPE_TO_SUBCATEGORY = {'traktorius': 'tractors', 'kombainas': 'combines', ...}
AGRI_DEFAULT_SUBCATEGORY = 'other-agricultural'

def _subcategory_for(agri_type):
    """Tipas → subkategorija. Persiskaičiuoja KAS IŠSAUGOJIMĄ."""
    slug = AGRI_TYPE_TO_SUBCATEGORY.get(agri_type, AGRI_DEFAULT_SUBCATEGORY)
    return _resolve_subcategory(slug)

def _type_for_subcategory(slug):
    """Atvirkštinis — iš URL TIK preselekcijai. Grąžina '' kai
    subkategorija dengia kelis tipus (vartotojas renkasi pats)."""
```

POST šakoje:
```python
target.subcategory = _subcategory_for(agri_type) or selected_sub
```

**Testas, kuris tai gaudo:** URL sako `tractors`, formoje pasirenki „Kombainas"
→ turi išsisaugoti `combines`, ne `tractors`.

### Ypatumai — `Equipment` su kategorijos prefiksu

Migracijos nereikia: `Equipment` eilutės kuriamos `get_or_create` metu.
`Equipment.CATEGORY_CHOICES` neriboja — Django choices nėra DB apribojimas.

```python
AGRI_EQUIPMENT_DEFINITION = [
    ('agri_drivetrain', 'Pavaros ir važiuoklė', ['Lėtintos pavaros', ...]),
    ('agri_mount',      'Prikabinimas',         ['Prikabinamas', 'Pakabinamas']),
    ('agri_other',      'Kita',                 ['ABS', 'Hidraulika', 'Kabina']),
]
```

Apibrėžimai gyvena **`apps/listings/equipment_registry.py`**, ne view'e —
juos turi matyti trys vartotojai: kategorijos view'as, `seed_equipment`
komanda ir seed migracija. Registre nėra Django importų, todėl migracija
jį gali saugiai importuoti.

Pridėjus naują kategoriją:

```python
# equipment_registry.py
CATEGORY_EQUIPMENT['<slug>'] = <SLUG>_EQUIPMENT_DEFINITION
```
```bash
venv/bin/python manage.py seed_equipment          # sukuria trūkstamas
venv/bin/python manage.py seed_equipment --check  # tik parodo
```

**SPĄSTAS 1: eilutės privalo egzistuoti PRIEŠ paiešką.** `build_advanced()`
ieško jau esančių `Equipment` eilučių. Jei jos kuriamos tingiai (tik
renderinant create formą), išplėstinė paieška rodo **0 ypatumų**, kol
niekas neatidarė formos — o naujoje aplinkoje ar po DB atstatymo varnelių
nebūtų iš viso. Todėl kiekviena kategorija su ypatumais **privalo** būti
`CATEGORY_EQUIPMENT` registre; migracija juos užsėja automatiškai.

**SPĄSTAS 2: tie patys pavadinimai kartojasi tarp kategorijų.**
„Hidraulika" egzistuoja **trijose** kategorijose (`trailer_body`,
`agri_other`, `load_hydraulics`), „Kabina" — dviejose. Ieškant vien pagal
`name`, paimama svetima eilutė — išplėstinė paieška rodė 2 ypatumus iš 9.
Todėl **visada ribok pagal kategorijos prefiksą** (`panels.py` →
`EQUIPMENT_PREFIX`). Testas, kuris tai gaudo: filtruok pagal SVETIMOS
kategorijos ypatumo ID ir tikrink, kad rezultatų nėra.

### Kontaktai

TIK `{% include 'listings/partials/contact_block.html' %}`. Savo telefono /
el. pašto / miesto laukų nekurk. `country_choices` iš view'o neperduok —
jie ateina iš `contact_block_tags`.

### Matmenų vienetai — NIEKADA nemaišyk viename lauke

Projekte yra **dvi atskiros matmenų aibės**, ir tai sąmoninga:

| Laukai | Vienetai | Kas naudoja |
|---|---|---|
| `length_m` · `width_m` · `height_m` | **metrai** (Decimal) | `construction`, `forestry` |
| `truck_length_mm` · `truck_width_mm` · `truck_height_mm` | **milimetrai** (Integer) | `trailers`, `loading-equipment` |

Etalone matmenys vienoms kategorijoms pateikti metrais, kitoms —
milimetrais. Perpanaudojus tą patį stulpelį abiem, **diapazono filtras
lygintų metrus su milimetrais** ir tyliai grąžintų nesąmonę: „Ilgis nuo 2
iki 5 m" atrinktų ir 3800 mm įrašą. Generinis variklis vienetų neverčia.

Todėl: pažiūrėk, kokiais vienetais etalonas prašo lauko, ir imk atitinkamą
aibę. Jei reikia trečios (pvz. cm) — kurk naujus stulpelius, o ne konvertuok
išsaugant.

Tas pats principas ir kitiems „to paties dalyko" laukams: `payload_kg`
tinka ir „Keliamoji galia", ir „Max keliamoji galia"; `engine_hours` —
visoms motovalandoms; `constr_drive_type` — pavaros tipui statybinėje,
krovimo ir miško technikoje (išplėstas iki 8 reikšmių).

### Kategorija su dviem formomis

Kai vienas VT turi dvi realiai skirtingas formas (`construction`:
technika sec 24 + priedai sec 16):

- **Vienas modulis, DU view'ai, DU šablonai.** Bendra (subkategorijos,
  markės, kontaktai, nuotraukos, išsaugojimo pabaiga) — bendrose
  funkcijose. `wheels_views.py` daro lygiai taip pat su `tyres`/`rims`.
  Vienas šablonas su `{% if %}` aplink pusę laukų būtų neskaitomas.
- **Konfigūracijoje** antrajai formai pridėk `"subcategory_slug": "<slug>"` —
  `panels.py` registruoja ją `PANELS_BY_SUB` / `ADVANCED_BY_SUB`, o
  `build_panel` / `build_advanced` / `apply_panel_filters` priima `sub_slug`.
  Be to vienam VT variklis paimtų tik PIRMĄ sekciją.
- **Išplėstinė paieška:** `/paieska/<slug>/?sub=<subcategory-slug>`.
- **Edit dispatch privalo atskirti**, kuri forma: `_guard()` tikrina, ar
  įrašas yra priedas, ir persiadresuoja į teisingą formą.

### Kiti niuansai

- `Listing.mileage` yra NOT NULL — jei kategorija jo nenaudoja: `target.mileage = 0`
- Pavadinimas generuojamas iš markė + modelis + metai, jei vartotojas neįvedė
- Nuotraukos, kompresija, drag&drop — kopijuok iš etalono šablono, nekurk iš naujo

---

## 3. Maršrutai ir pikeris

| Failas | Ką pridėti |
|---|---|
| `urls.py` | importas + `path("create/<kategorija>/", ...)` |
| `views.py` | `IMPLEMENTED_VEHICLE_TYPE_SLUGS` (be jo pikeryje „Netrukus") |
| `views.py` | `<KAT>_SUBCATEGORY_SLUGS` + redirect `_route_category_pick()` viduje |
| `views.py` | **4 edit dispatch taškai** — `listing_edit`, `listing_edit_hub`, `listing_edit_section`, `listing_edit_step` |
| `views.py` | `EQUIPMENT_CATEGORY_LABELS` ir `EQUIPMENT_CATEGORY_ORDER` — **abu blokai dubliuoti dviejose vietose** |
| `partials/category_icon.html` | viena `{% elif %}` eilutė |

---

## 4. Paieška — abi konfigūracijos

Sluoksnis deklaratyvus: `apps/listings/search_config/`.

### Užpildyk `db_field` abiejose

```
paneles-config.json     — greitoji panelė
isplestine-config.json  — /paieska/<kategorija>/
```

Kiekvienam laukui: `db_field`, `param` (arba `param_min`/`param_max`),
`active: true`. Ypatumų checkbox'ams: `db_field: "__equipment__"`,
`param: "equipment"`. Tekstinei paieškai: `db_field: "__text__"`, `param: "q"`.

**Reikšmės imamos iš modelio `choices`, ne iš JSON `options`** — JSON laiko
etalono etiketes, o mūsų `choices` su jomis sutampa 1:1.

**SPĄSTAS: `text` tipo laukas turi DVI reikšmes.**

| `db_field` | Ką daro variklis |
|---|---|
| `"__text__"` | bendra paieška: `Q(title) \| Q(description)`, param `q` |
| tikras stulpelis (pvz. `constr_model_text`) | `<stulpelis>__icontains` TAME lauke |

Anksčiau variklis visus `text` laukus traktavo kaip bendrą paiešką, todėl
priedų „Modelis" filtras negrąžindavo nieko — ieškojo pavadinime, o ne
`constr_model_text`. Rašydamas konfigūraciją įsitikink, kad tekstiniam
laukui su savo stulpeliu `db_field` NĖRA `__text__`.

**SPĄSTAS: tas pats `param` keliuose laukuose.** `select` laukas su viena
reikšme ir kelių reikšmių paieška (`multi: true`) ant to paties param'o
susikerta — vienos reikšmės filtras susiaurina `__in` rezultatą iki
paskutinės. Variklis tai sprendžia (`len(vals) > 1 → __in`), bet jei rašai
savo helperį — **perkėlęs lauką į konfigūraciją, IŠIMK jį iš seno helperio**.

**SPĄSTAS: brūkšnelis slug'e sulaužo `config_panels.<slug>`.** Django
šablone `config_panels.camping-houses` neveikia (brūkšnelis — minusas);
naudok `config_panels|get_item:'camping-houses'`, kaip daro
`loading-equipment` blokas `search_panel.html`.

**SPĄSTAS: markės parametras išplėstinėje buvo hardkodintas.**
`advanced_search_generic` skaitydavo `request.GET.getlist('trailer_brand_text')`,
todėl perkrovus puslapį pažymėtos markės išlikdavo TIK priekaboms. Dabar
param imamas iš konfigūracijos (`TEXT_BRAND_FIELDS` / `FK_BRAND_FIELDS`) —
jei pridedi naują markės lauką, užtenka jį įrašyti į tuos rinkinius.

**Kai vienam VT tenka KELIOS etalono sekcijos** (nuoma — penkios):
pirmoji lieka numatytoji (**be** `subcategory_slug`), nes `is_active()` ir
`build_panel()` krenta į `PANELS[vt_slug]`; visos kitos gauna
`subcategory_slug`. Panelėje daryk subkategorijų perjungiklį pagal `parts`
pavyzdį (`partSub` → `rentSub`): kiekviena forma su `data-rentsub=`,
`hidden name="subcategory"`, o `refreshCount()` pasirenka formą pagal
aktyvią subkategoriją. Count endpoint'as lieka `/paieska/count/<vt>/` —
subkategorija keliauja formos lauku.

**Trys konfigūracijos raktai, atsiradę nuomos vertikalėje:**

| Raktas | Kam |
|---|---|
| `own_options: true` | kategorija turi savas diapazono pakopas, o bendrosios netinka (nuomos kaina prasideda nuo 5, pardavimo — nuo 500). Skaito ir `options`, ir `options_from` |
| `limit_to_options: true` | sekcija rodo tik dalį bendrų `choices` (nuomos „Tipas": sec 33 septynios, sec 34 kitos šešios, o modelyje vienas sąrašas). Filtruoja pagal etiketes, todėl jos turi sutapti 1:1 |
| `FK_CHOICE_FIELDS` | FK laukas kaip select (kuro tipas, pavarų dėžė). Reikšmė yra id, todėl bendra filtro logika tinka; etiketės imamos per `gettext`, nes lentelėse vardai angliški |

**SPĄSTAS: `price` ne visada yra pardavimo kaina.** Nuomoje į jį rašoma
„Nuomos kaina parai" — taip veikia rikiavimas, kainos filtras ir kortelės
be naujo stulpelio. Bet tada kortelėje ir detalėje **privalai parodyti
vienetą** („45 $/parai"), kitaip skelbimas atrodo absurdiškai pigus.

**SPĄSTAS: `?subcategory=` slug'as griaudavo rezultatų puslapį.**
`filter_listings` (skaičiukas) seniai priima ir id, ir slug'ą, o
`listing_list` (rezultatai) priimdavo tik id — panelė su slug'u mesdavo
`ValueError: Field 'id' expected a number`. Dvi filtrų šakos = du taisymai.

**SPĄSTAS: `config_panels` nėra visuose sąrašo puslapiuose.**
`motorcycles_views` ir `trucks_views` renderina tą patį
`listing_list.html`, bet savo kontekstą — deklaratyvios panelės ten buvo
tuščios, o `|get_item` ant `''` metė `AttributeError` ir nugriovė puslapį.
Pridėjus naują panelę patikrink VISUS tris `listing_list.html` render'us.

**Ne visos varnelės privalo tapti filtrais.** Paslaugose etalono forma turi
18 varnelių, bet jo paieška filtruoja tik tipą, miestą ir tekstą. Tokios
varnelės vis tiek eina į `equipment_registry` (jos rodomos skelbime), bet
į `isplestine-config.json` — ne. Konfigūracija = filtrai, registras = duomenys.

**SPĄSTAS: `title`, `year`, `mileage`, `price` yra NOT NULL be default.**
Kategorijoje, kuriai jie neturi prasmės (paslaugos: nei metų, nei ridos,
o kaina neprivaloma), juos vis tiek reikia užpildyti: `year` = einamieji
metai, `mileage` = 0, `price` = 0. Ir tada **šablonuose parodyk, kad tai
ne nulinė kaina** („Sutartinė"), kitaip kortelė rodo „0 $".

**SPĄSTAS: prefiksas be pabraukimo pagautų svetimą kategoriją.**
Automobilių ypatumų kategorija vadinasi `electronics`; naujai video/audio
vertikalei prefiksas `elec_` saugus tik todėl, kad
`'electronics'.startswith('elec_')` yra `False`. Rinkdamas prefiksą
patikrink jį prieš VISUS esamus `Equipment.category` raktus, ne tik prieš
pavadinimus.

**Sąlyginai privalomi laukai.** Etalone pasitaiko, kad laukas privalomas
tik prie tam tikros reikšmės („Galingumas W" — tik kai Tipas =
Garsiakalbis). Tikrink abiejose pusėse: Alpine `x-show` žvaigždutei ir JS
`req()` sąlygoje, IR view'e prieš `save()`. Vien kliento tikrinimo
neužtenka — POST ateina ir be JS.

**Plokščias pikeris ir subkategorija iš formos — suderinama.** Paspirtukų
etalone subkategorijų žingsnio nėra (einam tiesiai į formą per
`CREATE_URL_BY_VEHICLE_TYPE`), bet DB subkategorijos egzistuoja ir yra
prasmingos, todėl `subcategory` išvedama iš formos lauko `bike_type` ir
persiskaičiuoja kas išsaugojimą. Vienas iš trijų tipų („Elektrinis
riedis") atitikmens neturi — jam paliekam `NULL`, o ne kišam į artimiausią.
Testas, kuris tai gaudo: pakeisk tipą redaguodamas ir tikrink, kad
subkategorija pasikeitė kartu.

**Vienodi vienetai — vienas stulpelis.** `power_w` (vatai) aptarnauja ir
video/audio garsiakalbius, ir paspirtukų variklius; `curb_weight` —
„Svoris kg"; `payload_kg` — „Maksimali apkrova kg". Tai NE tas pats, kas
maišyti vienetus: tikrink, ar etalonas prašo to paties mato, ir tik tada
perpanaudok.

### Įjunk variklyje (`panels.py`)

```python
LISTING_BACKED    += {'<kategorija>'}   # be jo is_active() = False
ENGINE_ENABLED    += {'<kategorija>'}   # greitoji panelė
ADVANCED_ENABLED  += {'<kategorija>'}   # /paieska/<kategorija>/
CHOICES_BY_DB_FIELD['<laukas>'] = '<CHOICES_ATTR>'
TEXT_BRAND_FIELDS += {'<kategorija>_brand_text'}   # laisvo teksto markė
FK_BRAND_FIELDS   += {'<laukas>': '<Modelis>'}     # FK markė
EQUIPMENT_PREFIX['<kategorija>'] = '<prefiksas>_'
```

Ir `views.py`: `SEARCH_PANEL_CATEGORIES` — be jo count endpoint'as meta 404.

### `is_active()` tikrina TIK aktyvius laukus

```python
return all(f.get('db_field') for f in cat['fields'] if f.get('active', True))
```

Be `if f.get('active', True)` kategorija su bent vienu `active: false` lauku
niekada neįsijungtų — o `active: false` naudojam ten, kur etalone laukas yra,
bet mūsų panelėje jo dar nerodom.

### Panelė šablone

`search_panel.html`: `<div x-show="tab === '<slug>'" id="sp-panel-<slug>">`
su forma ir `{% include 'listings/partials/panel_generic.html' with panel=config_panels.<slug> %}`.
Alpine tab'ą parenka pats iš `?category=`, jei toks `id` egzistuoja.

---

## 5. Kortelės ir detalės puslapis

- **`listing_list.html` — DU kortelių išdėstymai** (horizontalus ~770 ir
  tinklelio ~910). Pataisius tik vieną, naršymas rodys senus laukus.
  Sąlyga `listing.vehicle_type.slug == '<slug>'`, ne `selected_category`.
- **`paneles-config.json` → `card_fields`** — paantraštės laukai.
- **`listing_detail.html`** — nauja `{% elif %}` šaka **esamoje grandinėje**,
  ne naujas `{% if %}`. Naujas `{% if %}` nesubalansuotų `{% endif %}`.

---

## 6. Patikrinimų checklist

Visus rašymo testus daryk **atšaukiamoje transakcijoje** — tai produkcijos DB:

```python
try:
    with transaction.atomic():
        ...  # testai
        raise RuntimeError('ROLLBACK')
except RuntimeError: pass
```

- [ ] Pikeris veda į `/create/<kategorija>/`, ne atgal į save
- [ ] Visi laukai ir ypatumai formoje; kontaktai per `contact_block.html`
- [ ] **Subkategorija iš formos, ne iš URL** — testas su dviem skirtingom
- [ ] Pilnas išsaugojimas, kiekvienas laukas DB teisingas
- [ ] Redagavimas atidaro tą pačią formą užpildytą; 4 dispatch taškai
- [ ] `/?category=<slug>` rodo panelę su visais laukais
- [ ] `/paieska/<slug>/` rodo išplėstinę + ypatumų skaitiklį
- [ ] Kiekvienas filtras atskirai; diapazonai su viena užpildyta puse
- [ ] Ypatumų IR logika: pažymėjus du, rodomi tik turintys abu
- [ ] Ypatumai užsėti: `manage.py seed_equipment --check` rodo OK visoms
- [ ] Ypatumų prefiksas izoliuoja: filtras pagal SVETIMOS kategorijos
      ypatumo ID grąžina 0 rezultatų
- [ ] Tušti filtrai nesiaurina
- [ ] Mygtuko skaičius = realus rezultatų kiekis
- [ ] Kortelėse kategorijos laukai (abu išdėstymai)
- [ ] Detalės puslapyje visi užpildyti laukai + ypatumai
- [ ] **Kitos kategorijos nepakitusios** — cars, trucks, boats, trailers, parts

### Testų artefaktai, kurie atrodo kaip klaidos

- Skelbimai per formą lieka `draft` (nemokamų kvota) → `_public_listings_qs`
  jų nemato. Testuodamas filtrus kurk su `status='active'` tiesiogiai.
- `boats` panelė yra po `{% if user.is_staff %}` — anoniminis klientas jos nemato.
- `Decimal` renderinasi LT lokale: `86,50 m³`, ne `86.5`.
- Diapazonus (`year`, `price`) tvarko bendras filtrų blokas, ne kategorijos
  helperis — tikrink per `filter_listings`, ne per `apply_<kat>_filters`.
- Trumpi pjūviai (`html[i:i+9000]`) gali nukirsti lauką — pjauk iki kito
  `id="sp-panel-`.

---

## 7. Dvi filtrų implementacijos

`listing_list` (rezultatai) ir `filter_listings` (AJAX skaičiukas) yra
**atskiros filtrų šakos**. Deklaratyvus variklis kviečiamas iš abiejų —
naujų filtrų ranka nerašyk. Jei vis dėlto rašai kategorijos helperį,
kviesk jį abiejose vietose, kitaip mygtuko skaičius nesutaps su sąrašu.

**Perkėlus lauką į konfigūraciją, IŠIMK jį iš seno helperio.** Priešingu
atveju vienos reikšmės filtras susiaurins `__in` rezultatą — taip kelių
markių paieška grąžindavo tik vieną.

**Tekstinė paieška:** bendri `?q` / `?search` taiko tik pavadinimą; variklis
ieško ir aprašyme. `owns_text_search()` bendruosius praleidžia. Nenaudok
`q` savo helperyje — susidėję duotų tik `title` atitikmenis.

---

## 8. Ką visada paminėti kaip neišspręsta

Ataskaitos gale išvardink:

- **Kokios kategorijos subkategorijos liko be atitikmens** ir kodėl
  (pvz. `forestry-machines` — etalono „Tipas" sąraše miško technikos nėra)
- **Vertimai** — užpildyk tik lietuviškus msgid (`[ąčęėįšųūž]` regex);
  angliškų automatiškai NEPILDYK msgid reikšme, nes taip jie būtų pažymėti
  kaip išversti. Pasakyk, kiek liko neišverstų.
- **Kortelių / detalės spragos**, jei kurios nepadarei
- **Bendri `choices`**, kurie liko siauresni už etaloną
- **Pre-existing problemos, pastebėtos pakeliui** — pvz. `ListingImage`
  COUNT N+1 bendrame kortelės šablone (paliečia visas kategorijas),
  `EQUIPMENT_CATEGORY_LABELS` dublikatas, negyvi `panel_*.html` partialai
- **Ar ypatumai užsėti** — jei pridėjai kategoriją į `CATEGORY_EQUIPMENT`,
  bet nepaleidai `seed_equipment` ir nepridėjai seed migracijos, filtruose
  varnelių nebus
- **Laukai, kuriuos palikai `active: false`** ir kodėl (pvz. FK `fuel_type`
  multiselect: etalono etiketės lietuviškos, o `FuelType.name` DB — angliški;
  `range` ant `CharField` choices — leksikografinis palyginimas)
- **Jei testuodamas sukūrei skelbimų** — pasakyk `pk` ir pasiūlyk išvalyti;
  trynimo be leidimo nedaryk
