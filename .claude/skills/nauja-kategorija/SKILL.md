---
name: nauja-kategorija
description: Pilna skelbimų kategorijos vertikalė AutoLeft projekte — create forma, greitoji paieškos panelė, išplėstinė paieška, naršymo kortelės ir detalės puslapis. Naudok, kai reikia įgyvendinti naują VehicleType kategoriją (žemės ūkis, statybinė technika, nuoma, paslaugos ir pan.) arba užbaigti pusiau padarytą.
---

# Nauja kategorija — pilna vertikalė

Tikslas: **sukurti · rasti · peržiūrėti**. Kategorija nelaikoma padaryta, kol
veikia visi penki sluoksniai: create forma, greitoji panelė, išplėstinė
paieška, naršymo kortelės ir detalės puslapis.

Etalonai, iš kurių paimtas šis procesas: `trailers` (0f84e02, 50b75a2) ir
`agriculture` (431842c).

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

**SPĄSTAS: tie patys pavadinimai kartojasi tarp kategorijų.** `ABS` ir
`Hidraulika` egzistuoja ir priekaboms (`trailer_safety`, `trailer_body`), ir
žemės ūkiui (`agri_other`). Ieškant vien pagal `name`, paimama svetima
eilutė — išplėstinė paieška rodė 2 ypatumus iš 9. Todėl **visada ribok pagal
kategorijos prefiksą** (`panels.py` → `EQUIPMENT_PREFIX`).

### Kontaktai

TIK `{% include 'listings/partials/contact_block.html' %}`. Savo telefono /
el. pašto / miesto laukų nekurk. `country_choices` iš view'o neperduok —
jie ateina iš `contact_block_tags`.

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
- **Jei testuodamas sukūrei skelbimų** — pasakyk `pk` ir pasiūlyk išvalyti;
  trynimo be leidimo nedaryk
