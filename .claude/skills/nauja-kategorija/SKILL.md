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

### NUOLATINĖS TAISYKLĖS — galioja kiekvienam paviršiui

Pilnas tekstas ir patikros būdai: **`docs/taisykles.md`**. Santrauka, be
kurios darbo neatiduodam:

**1. Vieta yra svarbiausias filtras.** Kiekviename filtrų paviršiuje —
greitojoje panelėje, šoninėje juostoje, išplėstinėje paieškoje ir
mobiliame rodinyje — vieta yra PIRMA ir visada matoma. Niekada
neslepiama po „Daugiau filtrų", niekada nenustumiama žemiau markės ar
kainos. Tvarka visada: **šalis → miestas → spindulys**.

**2. Kortelė rodo tik tai, ko reikia apsispręsti, ar verta atidaryti:**
nuotrauka, pavadinimas, metai, kaina, pagrindiniai trys parametrai ir
VIETA. Komplektacija, įranga, VIN, aprašymas, istorija — kortelėje
NErodoma, tik skelbimo viduje.

**3. Skelbimo puslapyje kontaktų blokas yra pagrindinis elementas**, ne
priedas: pardavėjo tipas, telefonas, žinutė ir TIKSLI VIETA — miestas,
adresas, žemėlapis su žymekliu ir „Kaip nuvažiuoti". Matomas be slinkimo
iki galo.

**4. Kontaktai visada per `contact_block.html`** — viena dalis visai
svetainei, jokių kopijų.

**5. Šalies vėliavėlė rodoma visur, kur rodoma vieta:** kontaktų bloke,
kortelėje, žemėlapio burbule, išsaugotuose skelbimuose, šalies
sąrašuose. Vėliava eina **IŠKART PO šalies pavadinimo** — `📍 Kaunas,
Lithuania [vėliava]`, sąrašo eilutėje `○ Lithuania [vėliava]      4 821`
(prilipusi prie pavadinimo, skaičius — dešiniame krašte). Ne prieš, ne
eilutės gale. Eilutė nesilaužo: `flex-wrap:nowrap`, tekstui daugtaškis,
vėliavai `flex:0 0 auto`. Kortelėse vietos eilutę duoda viena dalis
`listings/partials/_kort_vieta.html`. Vardas kortelėje ir šalies
sąrašuose — angliškas (`|salies_vardas_en`), kontaktų bloke — išverstas.
Šaltinis — skelbimo šalis iš kontaktų bloko, jokio spėliojimo pagal
paskyrą ar IP. SVG (`static/flags/<kodas>.svg`), 16×12 px, viena dalis
`templates/partials/_veliava.html`. Be šalies — tik miestas, be tuščio
kvadrato.

> Kontaktų bloke vardas IŠVERSTAS (`salys.vardas`) — tekstas žmogui.
> Kortelėje ir šalies sąrašuose — angliškas ir neverčiamas
> (`salys.VARDAI_EN`): sąrašas tarptautinis.

**6. KIEKVIENAS INLINE SVG PRIVALO TURĖTI `width` IR `height` ATRIBUTUS**
žymėje, ne tik CSS:

```html
<svg class="pin" width="11" height="11" viewBox="0 0 24 24">…</svg>
```

Be jų SVG išsitempia iki 100 % konteinerio pločio visur, kur stiliai
nepasiekia: pasenęs naršyklės kešas, kitas puslapis, laiškas, fragmentas
per AJAX. Taip jau tris kartus sulūžo kortelės vietos eilutė —
smeigtukas išsipūtė per visą kortelę, o vėliava nukrito į antrą eilutę.

Iš to plaukia antra dalis: **bendro elemento stilius gyvena bendrame
faile** (`static/css/…`), niekada `<style>` bloke viename šablone —
kitaip kiti paviršiai jo negauna. Ir **testas turi matuoti tikrus
matmenis naršyklėje**, o ne tik tikrinti, ar CSS eilutė yra faile;
`docs/kort_vieta_playwright.js` matuoja ir su stiliais, ir juos išjungęs.

Patikra prieš atiduodant:

```bash
grep -o '<svg[^>]*>' <failas> | grep -v 'width='     # turi būti tuščia
curl -s <adresas> | grep -c 'class="vieta"'          # visuose paviršiuose > 0
```

**7. LAIŠKAS NIEKADA NESIUNČIAMAS UŽKLAUSOS METU.** `send_scenario`
sinchroniškai jungiasi prie smtp.gmail.com; kol vyksta TLS, prisijungimas
ir siuntimas, laukia ir gunicorn darbininkas, ir lankytojas. Skelbimo
puslapyje tai buvo tikra klaida: peržiūrų skaičiui peržengus 10 ar 100,
eilinis lankytojas laukdavo pašto serverio, o be `EMAIL_TIMEOUT` —
laukdavo be galo. Todėl:

* šalutiniai pranešimai (peržiūrų slenkstis, išsaugoto skelbimo
  pokyčiai, žinutė, pasisveikinimas, pranešimas administracijai) —
  per `apps/listings/emails/fone.py`
  (`send_scenario_fone`, `send_admin_scenario_fone`, `send_mail_fone`);
* sinchroniškai lieka tik tai, ko rezultatą puslapis TIKRAI rodo
  („Sąrašas išsiųstas į…", slaptažodžio atkūrimas) ir management
  komandos, kurioms reikia tikro rezultato ataskaitai;
* `EMAIL_TIMEOUT` privalo būti nustatytas — be jo Django laukia amžinai.

Patikra: `docs/pasto_fone_test.py` pakiša lėtą (2 s) pašto backend'ą ir
tikrina, kad skelbimo puslapis vis tiek atiduodamas greičiau.

**8. VIZUALINIS DARBAS TIKRINAMAS GYVOJE SVETAINĖJE, NE TIK 127.0.0.1.**

Playwright nuotrauka iš vietinio serverio talpyklos klaidų NEPAGAUNA IŠ
PRINCIPO: ten nėra nei nginx, nei naršyklės keše kabančio seno failo.
Būtent todėl ataskaitos buvo žalios, o žmogus matė sulaužytą puslapį ir
turėjo spausti Ctrl+Shift+R.

Po kiekvieno vizualinio darbo, KAI JIS JAU IŠKELTAS:

```bash
# 1. Ar HTML rodo į naują (sumaišytą) failą
curl -s https://autoleft.com/ | grep -o 'style\.[a-z0-9]*\.css'

# 2. Ar statiniai turi ilgą galiojimą, o HTML — ne
curl -sI https://autoleft.com/static/css/style.<maišas>.css | grep -i cache
#   → Cache-Control: public, max-age=31536000, immutable
curl -sI https://autoleft.com/ | grep -i cache
#   → Cache-Control: no-cache, must-revalidate

# 3. Nuotrauka iš GYVOS svetainės, ne iš vietinio serverio
```

Jei CSS vardas nepasikeitė, o šablonai keitėsi — darbas dar nepasiekė
lankytojo. Deploy tai tikrina pats (`deploy-agent.sh`,
`tikrinti_statinius`), bet nuotrauka iš gyvos svetainės yra paskutinis
įrodymas, ir be jos darbas neatiduodamas.

Susiję: statinių vardai turi turinio maišą (`STORAGES` nustatymuose),
nginx taisyklės — `deploy/nginx-statiniai.conf`, patikra —
`docs/statiniu_kesas_test.py`.

**9. VIENA ŠALIS VISAI SVETAINEI.** Šalis nėra atskiras kiekvieno
puslapio filtras — tai viena bendra reikšmė. Pakeitus bet kur (juostoje
virš panelės, šoninėje juostoje, `/imones/`), ji galioja visur. Viena
šablono dalis `templates/partials/_salis.html` (stiliai `juosta`,
`sonine`, `lakstas`), vienas kontekstinis procesorius
`context_processors.salis`, viena kiekių funkcija
`salies_juosta.kiekiai()`. Reikšmės sluoksniai: `?salis=` → slapukas →
paskyros profilis → `lt`; adresas laimi visada. Šalies keitimas
neišvalo markės, kainos, metų — tik miestą ir spindulį. Skelbimo šalis
imama TIK iš kontaktų bloko; jei skiriasi nuo pasirinktos — tyli eilutė
„Šis skelbimas yra Vokietijoje" su nuoroda. Naujam paviršiui
nekuriam antro sąrašo — įtraukiam tą pačią dalį.
> Tai skirtingi paviršiai, nesupainiok.

**10. Tos pačios taisyklės — įmonėms ir meistrams:** vieta pirma,
paslaugos ir kainos kortelėje, viskas kita — įmonės puslapyje.


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

### PWA yra planuose — rašom su tuo omenyje

AutoLeft taps įdiegiama programėle. Dar nedaroma, bet naujas kodas privalo
būti suderinamas, kad vėliau užtektų pridėti manifestą, service worker'į ir
ikonas — be perrašymų. Šešios taisyklės ir esamos būklės inventorius:
`docs/pwa-pasiruosimas.md`. Santrauka — šio dokumento skyriuje „9. PWA".

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
venv/bin/python manage.py migrate listings && systemctl restart gunicorn
```

### Kada klausti leidimo

**Additive migracijos ir gunicorn perkrovimas — leidimo neklausiama.**
Daroma iškart, o padaryta pranešama darbo pabaigoje. Laukimas čia tik
kenkia: kodas jau pakeistas, o gunicorn sukasi ant seno — kuo ilgiau taip
stovi, tuo didesnis neatitikimas tarp to, ką matai naršyklėje, ir to, kas
yra faile.

**Klausiama TIK prieš trynimą** — DB įrašų, stulpelių, `.txt` failų,
markių, skelbimų. Tada pirma parodomas tikslus sąrašas (kas ir kiek),
palaukiama atsakymo, ir tik tada trinama. `DROP`, `DELETE` be `WHERE`,
`flush` — niekada be atskiro patvirtinimo.

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

### Markė — vienas šaltinis, viena būsena

**Kiekviena markė projekte egzistuoja VIENĄ kartą** — vienoje lentelėje,
susieta su kategorijomis per M2M. Iš tos pačios eilutės ima visos keturios
vietos:

1. Create forma
2. Greitoji paieškos panelė
3. Rezultatų šoninė filtrų juosta
4. Išplėstinė paieška

„Yamaha" yra viena eilutė, susieta su motociklais ir motociklų nuoma. Prie
jos kabo jos modeliai. Vartotojas ją mato vienodai visose keturiose vietose,
o pridėjus naują markę admin'e ji atsiranda visur iš karto — be deploy'o.

**Būsena taip pat viena.** Pasirinkta markė laikoma URL parametruose ir
išlieka pereinant tarp ekranų: pasirinkus panelėje, šoninėje juostoje ji jau
pažymėta, o modelių sąrašas susiaurėja iki tos markės modelių. Nekurk
atskiros būsenos kiekvienam ekranui — vienas parametras, viena tiesa.

**Tas pats galioja modeliams:** modelis kabo prie markės, ne prie
kategorijos, ir kaskada visur veikia vienodai.

> **DRAUDŽIAMA:** kurti atskirą markių sąrašą kategorijai, jei tos pačios
> markės jau egzistuoja kitoje. Vietoj to — **pridėti kategoriją prie esamos
> markės**. Naujas `.txt` failas ar `BRANDS = [...]` konstanta view'e yra
> ženklas, kad taisyklė laužoma.

**Kodėl tai taisyklė.** 2026-08-20 audite rasta 19 atskirų markių šaltinių:
4 FK lentelės, 3 Python konstantos ir 11 `.txt` failų — **5076 įrašai, iš
kurių tik 3140 unikalūs (37 % dublikatai)**. 1149 markės kartojosi 2+
kategorijose („Mercedes-Benz" — 12 sąrašų), o 81 pavadinimas turėjo skirtingą
rašybą skirtinguose failuose (`SKODA` / `Skoda` / `Škoda`). Iš 19 kategorijų
tik 3 markes buvo galima pridėti per admin — likusios reikalavo deploy'o.

**Kaip tai atrodo kode** (įgyvendinta 2026-08-20):

- `Brand` + `BrandScope` (M2M) — viena lentelė, 12 šeimų;
  `apps/listings/brand_registry.py` sako, kuri kategorija, subkategorija ar
  nuomos tipas kuriai šeimai priklauso;
- **visi paviršiai kviečia tik `apps/listings/brands.py`** —
  `brands_qs(scope)`, `brand_rows`, `find`, `posted_brand`. Jokių
  `Brand.objects.filter(vehicle_type=...)` create formose ir jokių
  `X_BRANDS` konstantų;
- `has_models` šeimoje sako, ar rodoma modelių kaskada. Autogide kaskada
  yra tik ten, kur yra modelių duomenų (automobiliai, motociklai); kitur
  modelis — laisvas tekstas. Nekurk kaskados ten, kur duomenų nėra;
- **dalys ir nuoma sąrašo NEturi** — jos ima transporto priemonės šeimą.
  Patikrinta autogide: sec 10 = sec 01, sec 27 = sec 02, sec 23 = sec 04,
  sec 28 = sec 22 (identiška iki baito);
- markių pavadinimai **nekeičiami ir nejungiami** — kaip šaltinyje. Rašybos
  skirtumus sprendžia paieška (`brands.normalize`), o ne pervadinimas;
- `*_brand_text` stulpelis lieka laisvam tekstui („Kita"), o ne kaip antras
  markių šaltinis. „Kita" įvedimai keliauja į `BrandSuggestion` ir admin'e
  vienu veiksmu virsta tikra marke — taip sąrašas pildosi pagal realų
  poreikį, o ne pagal spėjimus.

**Naujai kategorijai** nereikia nieko sėti: pridedi šeimą į `SCOPES`
(arba prijungi kategoriją prie esamos) ir forma su filtru markes gauna
automatiškai.

### Duomenų perkėlimas — VIENA vieta

Jei tą patį darbą gali padaryti ir management komanda, ir migracija —
**pasirink vieną**. Dvi vietos vienu metu yra klaida iš principo, ne
neatidumas: kiekviena atskirai teisinga, o kartu jos padaro darbą du kartus.

Taisyklė paprasta:

- **Perkėlimą daro migracija** — ji paleidžiama automatiškai, vieną kartą,
  ir turi savo įrašą `django_migrations` lentelėje.
- **Komanda lieka tik patikrinimui** (`--plan`) arba pakartotiniam
  sėjimui ten, kur migracija jau pritaikyta be duomenų. Jos docstring'e
  turi būti parašyta, kad perkėlimą daro migracija.

Nesvarbu, kuri vieta pasirinkta — **abi turi būti idempotentiškos** ir
sutapimą tikrinti pagal tą patį raktą kaip bazės apribojimas.

**Pavyzdys (2026-08-20).** `MotorcycleModel` → `Model` perkėlimas buvo
parašytas ir kaip `unify_models` komanda, ir kaip `0080` migracija. Paleisti
abu — `Model` lentelėje atsirado 3732 dublikatai. Blogiau: komanda
sutapimą tikrino pagal `(brand, slug)`, todėl esamam pavadinimui tiesiog
sugeneruodavo `slug-2` ir kurdavo antrą įrašą — dublikatas atrodė kaip
naujas modelis.

Tvarkant pridėtas ir bazės apribojimas:

```python
unique_together = [['brand', 'slug'], ['brand', 'name']]
```

Tai pigiausias saugiklis: nesvarbu, kiek kartų kas paleis komandą ar
migraciją, antras toks pat įrašas paprasčiausiai nepraeis.

### Mobiliame vaizde nėra horizontalaus slinkimo

**Viskas telpa į ekrano plotį.** Jokių slenkamų juostų, jokių nukirptų
elementų, jokių „pastumtų" sričių. Jei kažkas netelpa — mažinam, laužom į
eilutes arba slepiam po mygtuku, bet **nestumiam į šoną**.

**Taisyklė galioja IŠDĖSTYMUI, ne sąmoningam komponentui.** Skiriasi du
dalykai:

| | Draudžiama | Leidžiama |
|---|---|---|
| Kas | netyčinė persipilda — elementas išlipa už ekrano | sąmoninga slenkama juosta (karuselė) savo konteineryje |
| Požymis | `body.scrollWidth > innerWidth` arba `left < -1` | konteineris su `overflow-x: auto` + `scroll-snap-type` |
| Pavyzdys | per plati antraštė, `justify-end` eilutė | skirtukų pavadinimų juosta (`.home-tabs-header`) |

Karuselė teisinga tik tada, kai slinkimas gyvena JOS viduje: puslapis
nejuda, `document.documentElement.scrollWidth` lieka lygus `innerWidth`,
o pati juosta turi `scroll-snap-type: x mandatory` (kad kortelė sustotų
vietoje) ir rodykles, kurios rodomos tik kai yra ką slinkti. Persipildymo
patikroje tokio konteinerio vidus praleidžiamas:

```javascript
if (el.closest('.home-tabs-header')) return;   // sąmoninga juosta — ne persipilda
```

**Turinys į šoną neslankioja.** Slenkama juosta tinka trumpiems
pavadinimams (skirtukai, žymos), bet ne skelbimų kortelėms: jos dedamos
į tinklelį ir keliauja žemyn. 2026-08-20 kortelių karuselė buvo padaryta
ir tą pačią dieną atmesta — vartotojas nori matyti viską iš karto.

Patikrinimas — vienas skaičius:

```javascript
document.documentElement.scrollWidth === document.documentElement.clientWidth
```

Turi galioti prie 360, 390 ir 768 px. Jei `scrollWidth` didesnis — klaida.

**Bet šito NEUŽTENKA.** Elementas gali išsikišti į KAIRĘ — tada `left`
neigiamas, o `scrollWidth` nepasikeičia, nes naršyklė kairėn išsikišusio
turinio į slinkimo plotį neįskaičiuoja. Todėl tikrinamos ABI pusės:

```javascript
[...document.querySelectorAll('*')]
  .filter(e => { const r = e.getBoundingClientRect();
                 return r.left < -1 || r.right > window.innerWidth + 1; })
  .map(e => [e.className, Math.round(e.getBoundingClientRect().left),
                          Math.round(e.getBoundingClientRect().right)]);
```

**Neigiamas `left` beveik visada reiškia vieną iš trijų:**

1. `position: absolute` su `right: 0` tėve, kuris siauresnis už elementą;
2. neigiamas `margin-left` arba `transform: translateX(-…)`;
3. **flex konteineris su `justify-content: flex-end` ir per plačiu turiniu** —
   perteklius eina į kairę, ne į dešinę.

**Pavyzdys (2026-08-20).** „Rūšiuoti pagal" eilutė buvo
`flex justify-end`, turinys 368 px, konteineris 344 px — elementas
atsidūrė ties `left: −24`. Vienpusis patikrinimas (`right > innerWidth`)
jo nerado, ir po dviejų taisymo bandymų vartotojas vis dar nematė
rūšiavimo telefone. `scrollWidth` visą laiką rodė „viskas gerai".

```python
# Playwright, visiems puslapiams iš karto
PROBE = "() => ({s: document.documentElement.scrollWidth, c: document.documentElement.clientWidth})"
```

**Kodėl to neužtenka tikrinti akimis.** Vienas netelpantis elementas
išplečia VISĄ puslapį, o naršyklė jį sumažina — atrodo, kad tiesiog
„šriftas mažesnis". 2026-08-20 antraštės dešinė pusė (kalbų jungiklis,
paieškos ir žinučių ikonos, meniu) buvo 340 px pločio ir plėtė puslapį iki
396 px. Pasekmės atrodė kaip trys atskiros klaidos: ikonų juosta „slinko",
kategorijų pikeris buvo „nukirptas", o rūšiavimas telefone „nesimatė".
Priežastis buvo viena.

**Todėl ieškant kaltininko tikrinama ne akimis, o taip:** surenkam visus
elementus, kurių `getBoundingClientRect().right > clientWidth`, ir
atmetam tuos, kurių tėvas turi `overflow-x: auto/scroll/hidden`.

### Laukų CSS turi pasiekti KIEKVIENĄ paviršių

**Klasė ant elemento ≠ stilius puslapyje.** `sp-fld`, `sp-sel`, `sp-dd*`
apibrėžti `partials/_sp_field_styles.html`. Kiekvienas naujas paviršius,
kuris renderina paieškos laukus, privalo jį įtraukti:

```django
{% include 'listings/partials/_sp_field_styles.html' %}
```

Patikrinimas — vienas curl. Turi grąžinti **1**, ne 0:

```bash
curl -s https://autoleft.com/paieska/camping-houses/ | grep -c 'sp-fld {'
```

Nuliui reiškia, kad laukai puslapyje bus be baltos dėžutės, be rėmelio ir
be apvalintų kampų, o „Nuo/Iki" poros kabos ore.

**Kodėl tai pasitaikė du kartus.** Iš pradžių stiliai gyveno `<style>`
bloke pačiame `search_panel.html`. Kol egzistavo tik greitoji panelė, viskas
veikė. Detali paieška to partial'o neįtraukė — laukai be rėmelių (1 kartas).
Iškėlus stilius į atskirą partial'ą, ta pati klaida pasikartojo su
rezultatų puslapio šonine juosta, nes ir jis įtraukimo neturėjo (2 kartas).

Klaida klastinga tuo, kad HTML atrodo teisingai: klasės vietoje, markup'as
toks pat kaip veikiančiame puslapyje. Todėl tikrinama ne akimis, o šitaip:

```bash
for u in "/" "/paieska/camping-houses/" "/?category=camping-houses&sidebar=1"; do
  printf "%-46s %s\n" "$u" "$(curl -s "https://autoleft.com$u" | grep -c 'sp-fld {')"
done
```

Visose eilutėse turi būti 1. Tą patį principą taikyk bet kuriam bendram
`<style>` ar `<script>`: naujas paviršius — patikrink, ar jis jį gauna.

### DIEGIMAS: „ĮDIEK"

Kai Thomas parašo **„ĮDIEK"** — paleidi

```bash
./deploy.sh
```

ir parodai **tik jo išvestį**. Nieko neaiškini, nekartoji, nekomentuoji.

Jei krenta — pasakai, **kuriame žingsnyje** (Kodas / Priklausomybės /
Migracijos / Statika / Patikra / Perkrovimas / Smoke) ir **ką siūlai**.
Nieko netaisai savavališkai, kol jis neatsako.

`deploy.sh` pats: parsisiunčia kodą (o dirbant šakoje — sulydo ją į
master), įdiegia priklausomybes tik jei pasikeitė `requirements.txt`,
paleidžia migracijas, `collectstatic`, `compilemessages`, patikrina
šablonų nuotėkį ir testus (**krenta — sustoja ir nieko nediegia**),
perkrauna gunicorn, paleidžia smoke testą (`/`, `/?section=cars`,
`/searches/`, naujausio skelbimo puslapis), o jei bent vienas ne 200 —
grąžina ankstesnį commit'ą ir perkrauna atgal.

### PRIVALOMA PATIKRA PRIEŠ KIEKVIENĄ DIEGIMĄ

Rankinis variantas (tą patį daro `deploy.sh` viduje):

```bash
./scripts/patikra.sh
```

Praeina — galima merge'inti į master (o master per 5 min. iškeliauja į
produkciją). Nepraeina — netaisyk „greitai ir taip", pirma sutvarkyk.

Patikra daro du dalykus:

1. **Šablonų skenavimas** — ar nėra `{#` be `#}` toje pačioje eilutėje.
2. **Django testai** (`apps/listings/tests.py`, ~3 s, testinės DB nekuria —
   `config/test_runner.BeDuombazes`, tik skaito):
   - `SablonuKomentaraiTestas` — visi `templates/**/*.html`;
   - `PuslapiuTestas.test_nera_sablono_komentaru_puslapiuose` — atidaro
     `/`, `/?section=cars`, `/?category=cars&sidebar=1`, `/paieska/cars/`,
     `/browse/`, `/searches/` ir skelbimo puslapį; jei atsakyme yra `{#`
     ar `#}`, testas krenta ir parodo puslapį, eilutę ir iškarpą;
   - `PuslapiuTestas.test_tuscios_busenos_ikona_atitinka_kategorija` — visoms
     kategorijoms atidaro tuščią rezultatų būseną ir lygina ikoną su
     `listings/partials/category_icon.html` tos kategorijos ikona (pagauna
     „automobiliams rodomas sunkvežimis").

Be to, `git commit` sustabdo commit'ą, jei į `templates/` patenka daugiaeilis
`{# #}` (`.githooks/pre-commit`, įjungta per `git config core.hooksPath`).

**Naują puslapį ar tuščią būseną pridėjai — įrašyk jį į `_puslapiai()`
sąrašą** `apps/listings/tests.py`. Patikra saugo tik tai, ką mato.

### Komentarai šablonuose

**Kelių eilučių komentarai — TIK `{% comment %}...{% endcomment %}`.**
`{# ... #}` galioja tik vienoje eilutėje.

Django `{# #}` yra vienos eilutės sintaksė. Užrašius jį per kelias eilutes,
teksto niekas neišfiltruoja — jis atsiduria HTML'e ir vartotojas mato
komentarą puslapyje.

```django
{# Gerai: viena eilutė #}

{% comment %}
Gerai: kelios eilutės.
{% endcomment %}

{# BLOGAI: kelios eilutės —
   šis tekstas bus matomas puslapyje #}
```

Klaida pasitaikė PENKIS kartus (`sidebar_moto_parts.html`,
`advanced_generic.html`, `panel_generic.html`, `search_panel.html`,
`fields/_range.html`, `base.html`) — todėl taisyklės nebeužtenka ir ją
pakeitė patikra aukščiau. Taisyklė pasako, kaip rašyti; patikra neleidžia
išleisti, kai parašyta ne taip.

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

**Ne kiekviena pikerio eilutė virsta vertikale.** Etalone pasitaiko
kategorijų, kurios neturi nei savos formos, nei paieškos sekcijos —
mikroautobusai ten yra **nukreipimo puslapis** į automobilius arba sunkųjį
transportą (riba 3,5 t = B kategorija). Prieš kuriant laukus patikrink:
jei `search_config` nė vienoje sekcijoje kategorijos nėra, greičiausiai
etalonas jos taip pat neturi kaip kategorijos. Tada:

- `CREATE_URL_BY_VEHICLE_TYPE['<slug>'] = '/create/<pasirinkimo-puslapis>/'`
- VT lieka DB, bet be formos, be panelės, be konfigūracijos sekcijos
- naršyme `?category=<slug>` **persiadresuoja** ten, kur skelbimai
  iš tikrųjų gyvena; nukreipimas turi būti subkategorijai jautrus, kitaip
  senos nuorodos praranda prasmę

**Patikrink navigacijos eilučių porų nuoseklumą.** `MORE_ITEMS_SPEC`
eilutė yra `(vt_slug, pavadinimas, ikona, subcategory_id)`. Radau eilutę,
kur `vt_slug='vans'`, o `subcategory_id=198` priklausė `trucks` —
tokia nuoroda tyliai grąžina 0 rezultatų, nes filtras reikalauja abiejų.
Pridėdamas eilutę patikrink, kad subkategorija tikrai priklauso tam VT.

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

Nuolatinės taisyklės (`docs/taisykles.md`) — tikrinama KIEKVIENAM darbui,
ne tik naujai kategorijai:

- [ ] Vieta — pirmas filtras visuose keturiuose paviršiuose
      (panelė, šoninė juosta, išplėstinė, mobilus); šalis → miestas → spindulys
- [ ] Kortelėje tik: nuotrauka, pavadinimas, metai, kaina, 3 parametrai, vieta
      (jokios komplektacijos, įrangos, VIN, aprašymo, istorijos)
- [ ] Kontaktų blokas skelbime — su tikslia vieta, žemėlapiu ir
      „Kaip nuvažiuoti"; matomas be slinkimo iki galo
- [ ] Kontaktai tik per `contact_block.html`
- [ ] Šalies vėliavėlė per `partials/_veliava.html` visur, kur rodoma
      vieta; VISUR po pavadinimo; be šalies — tik miestas
- [ ] Šalis — viena reikšmė visai svetainei: pakeitus vienur, pasikeitė
      visur; keitimas nenumetė markės, kainos, metų
- [ ] Kiekvienas naujas inline SVG turi width ir height žymėje
- [ ] Bendro elemento stilius — bendrame CSS faile, ne šablono <style>
- [ ] Testas matuoja tikrus matmenis naršyklėje, ne tik CSS eilutę faile
- [ ] Nė vienas laiškas nesiunčiamas užklausos metu (fone.py), EMAIL_TIMEOUT yra
- [ ] Statiniai per {% static %}; kelias vienoje žymėje; failas egzistuoja
- [ ] Po vizualinio darbo — nuotrauka iš GYVOS autoleft.com, ne tik iš 127.0.0.1
- [ ] Gyvame HTML style.<maišas>.css pasikeitė, jei keitėsi šablonai ar CSS

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

## 7b. Vertimai — kaip atnaujinti nesugadinant

`manage.py makemessages` projekte **perrašyta** (`apps/listings/management/
commands/makemessages.py`): msgmerge visada leidžiamas su
`--no-fuzzy-matching`. Nekeisk to ir nekviesk `msgmerge` ranka be šios
vėliavos.

**Kodėl.** Be jos msgmerge naujam ar pasikeitusiam msgid priskiria
„panašiausio" seno įrašo vertimą. Dalis tokių priskyrimų lieka BE
`#, fuzzy` žymos ir tampa gyvais, klaidingais vertimais. 2026-08-20
audite tokių rasta **57**:

| msgid | ką rodė |
|---|---|
| `Steel` | „Vairavimas" |
| `Fits car brands` | „Diskiniai stabdžiai" |
| `Bolt count` | „Visos šalys" |
| `Polish` | „English" |
| `Subscription active until` | „Techninė apžiūra galioja iki" |

Su `--no-fuzzy-matching` naujas msgid lieka `msgstr ""` — tai matoma iš
karto ir nepadaro žalos.

**Tvarka:**

```bash
venv/bin/python manage.py makemessages -l lt --no-obsolete
# užpildyti TIK lietuviškus msgid; angliškų nepildyti msgid reikšme
venv/bin/python manage.py compilemessages -l lt
```

### Ko NEVERSTI

**Markių ir modelių pavadinimai NIEKADA neverčiami.** Tai tikriniai
pavadinimai, vienodi visomis kalbomis: `Yamaha`, `Mercedes-Benz`,
`Schmitz Cargobull`, `MT-07`, `Sprinter`. Jie:

- neapvyniojami `{% trans %}` ar `_()`,
- nepatenka į `.po` failus,
- neturi vertimo variantų nė vienai kalbai.

**Verčiami tik sąsajos tekstai:** laukų etiketės („Markė", „Modelis"),
mygtukai, pranešimai, kategorijų ir tipų pavadinimai.

**Ta pati taisyklė galioja DB:** markė saugoma originaliu užrašymu, be
lokalizuotų variantų. Viena eilutė — vienas užrašymas.

**Paiešką palengvina normalizavimas, ne vertimas.** Markių paieškos
laukas turi rasti markę nepaisant:

| Kas nepaisoma | Pavyzdys |
|---|---|
| raidžių dydžio | `skoda` = `Skoda` = `SKODA` |
| diakritikos | `skoda` = `Škoda`, `kassbohrer` = `Kässbohrer` |
| tarpų ir brūkšnelių | `alfaromeo` = `Alfa Romeo` = `Alfa-Romeo` |

Rodomas ir saugomas **visada originalus** pavadinimas — normalizuota forma
naudojama tik palyginimui.

> Kodėl tai svarbu: išvertus markę ji taptų nerandama. Vartotojas, ieškantis
> „Mercedes", nerastų „Mercedesas", o filtro reikšmė URL'e skirtųsi
> priklausomai nuo kalbos — ta pati nuoroda dviem vartotojams duotų skirtingus
> rezultatus.

2026-08-20 patikra rado vieną pažeidimą — `{% trans "Toyota" %}` pagalbos
centre; išimta. Kiti 37 sutapimai tarp `.po` ir markių sąrašų pasirodė esą
atsitiktiniai (`Other`, `White`, `Chopper`, `Diesel`, `XXL` — sąsajos
reikšmės, sutampančios su markės vardu). Tikrinant tai kartoti verta:
lygink `.po` msgid su markių ir modelių sąrašais, bet **sprendimą priimk
pagal `#:` nuorodą** — jei ji rodo į `choices` ar šabloną, tai sąsajos
tekstas, ne markė.

**SPĄSTAS: tas pats msgid dviejuose kontekstuose.** `Steel` yra ir laivų
korpuso medžiaga, ir ratlankių tipas — vienas .po įrašas, vienas
vertimas. Jei reikšmės skiriasi, imk ATSKIRĄ msgid (`Stamped steel`), o
ne perrašyk bendrą.

**SPĄSTAS: vienetai dingsta vertime.** `Width (mm)`, `Width (m)` ir
`Width (J)` visi turėjo vertimą „Plotis" — vartotojas nematė, kuo įvesti.
Vienetą palik ir vertime.

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


### Kortelės patikra: ar turinys tikrai matomas

Po BET KOKIO kortelės ar išdėstymo pakeitimo. 2026-08-21 rezultatų kortelė
telefone atrodė tuščia: tekstas buvo, bet informacijos stulpeliui liko
40 px iš 358 (kortelė `display:flex`, nuotrauka fiksuoti 340 px, mobilaus
varianto nebuvo). Nei HTTP kodas, nei DOM mazgų skaičius, nei persipildymo
patikra to nerodo — visi rodikliai buvo „gerai".

```javascript
[...document.querySelectorAll('.h-listing-card *, .home-tab-card *')]
  .filter(e => e.children.length === 0 && e.offsetParent !== null
               && e.textContent.trim().length > 6)
  .map(e => { const r = e.getBoundingClientRect(); const cs = getComputedStyle(e);
      return {t: e.textContent.trim().slice(0, 24),
              w: Math.round(r.width), h: Math.round(r.height),
              kirpta: e.scrollWidth > e.clientWidth + 1 && cs.textOverflow !== 'ellipsis'}; })
  .filter(x => (x.w < 120 && x.h > 40) || x.h < 10 || x.kirpta);   // TUŠČIA = gerai
```

Trys požymiai: **siauras ir aukštas** (tekstas suspaustas į skiltelę),
**beveik nulinio aukščio**, **nukirptas be `ellipsis`**. Filtrai
`offsetParent !== null` ir `length > 6` išmeta paslėptus skirtukus ir
vienženklius skaitiklius — be jų patikra duoda 200+ netikrų pranešimų.

Tikrinti 360 ir 390 px, abiem vaizdo režimais (`?vaizdas=thumb` ir `line`).
Patikra patikrinta atgal: grąžinus seną CSS ji randa 32 suspaustus blokus,
su dabartiniu — 0.


### docs/dizaino-sistema.md — privalomas šaltinis

Bet kokiam išdėstymo ar stiliaus darbui reikšmės imamos IŠ TEN, ne iš
akies ir ne iš etalono CSS tiesiogiai. Tarpai, šriftai, svoriai,
apvalinimas, laukų ir mygtukų aukščiai, spalvų vaidmenys — visi
apibrėžti `base.html` `:root` kaip kintamieji (`--sp-*`, `--fs-*`,
`--fw-*`, `--r-*`, `--field-h`, `--btn-h`, `--text`, `--border`…).
Šablone rašom `var(--sp-4)`, ne `16px`.

Po darbo paleidžiami trys patikrinimai iš dokumento pabaigos:

```javascript
// Bendras filtras: skaičiuojam tik tai, ką vartotojas mato.
const matomas = e => { const r = e.getBoundingClientRect(); const s = getComputedStyle(e);
                       return r.width > 2 && r.height > 2 && s.visibility !== 'hidden'; };

// 1. Šriftai — tik iš skalės. Imam tik lapinius elementus su tekstu:
// kitaip skaičiuojami ir paveldėti dydžiai, ir paslėpti skirtukai
// (be filtro pagrindinis puslapis rodo 390 „klaidų" vietoj 61 tikros).
const skalė = [12, 14, 16, 17, 18, 20, 24];
[...document.querySelectorAll('body *')].filter(matomas)
  .filter(e => e.children.length === 0 && (e.textContent || '').trim())
  .map(e => ({ t: e.textContent.trim().slice(0, 14), fs: parseFloat(getComputedStyle(e).fontSize) }))
  .filter(x => !skalė.includes(x.fs));          // turi būti tuščias

// 2. Laukai — visi 40 px. Be `:not([type=hidden])` ir be `matomas`
// patikra VISADA nurodo klaidą (paslėpti input'ai yra 0 px aukščio) —
// pagrindiniame puslapyje ji „rasdavo" 44 problemas, iš kurių tikrų 0.
[...document.querySelectorAll('input:not([type=hidden]):not([type=checkbox]):not([type=radio]), select, .sp-fld')]
  .filter(matomas)
  .filter(e => Math.round(e.getBoundingClientRect().height) !== 40);   // turi būti tuščias

// 3. Akcento spalva — vienas elementas ekrane.
// Kanalus normalizuojam: --accent yra „rgb(55 65 81)", o computed style
// grąžina „rgb(55, 55, 81)" — tiesioginis lyginimas visada duoda 0.
const norm = c => c.replace(/[^0-9]+/g, ' ').trim();
const acc = norm(getComputedStyle(document.documentElement).getPropertyValue('--accent'));
[...document.querySelectorAll('*')].filter(matomas)
  .filter(e => norm(getComputedStyle(e).backgroundColor) === acc).length;   // 1 (rezultatuose 0)
```

**Visos trys patikros patikrintos atgal** (2026-08-21): sena Nr. 1 rodė 390
„klaidų", sena Nr. 2 — 44, nors tikrų buvo 61 ir 0; sena Nr. 3 visada
grąžindavo 0. Patikra, kuri niekada nesuveikia, yra blogesnė už jokią.

Pirmi du turi grąžinti tuščią sąrašą, trečias — 1 (rezultatų puslapyje 0,
nes ten pagrindinio veiksmo nėra). Jei ne — taisom prieš commit'ą arba
pasakom, kodėl ta vieta yra išimtis.

---

## 9. PWA — planuojama, bet galioja jau dabar

**Dar nedaroma.** Manifesto, service worker'io ir ikonų nėra. Bet AutoLeft
taps įdiegiama programėle, todėl viskas, kas rašoma dabar, turi būti su tuo
suderinama. Pilnas dokumentas su esamos būklės inventoriumi:
`docs/pwa-pasiruosimas.md`.

1. **Statiniai failai versijuojami** (maiša pavadinime) — service worker'is
   gali saugiai kešuoti tik tokį failą. Praktikoje: jungiam TIK per
   `{% static %}`, niekada ranka rašytu `/static/js/foo.js` keliu.
2. **Jokių įrašytų absoliučių adresų su domenu.** Visur santykiniai keliai
   arba `{% url %}` — kitaip standalone režimas išmes vartotoją į naršyklę.
   Vienintelė išimtis:
   `og:` ir `twitter:` meta žymos (jos skirtos robotams).
3. **Veikia be interneto tiek, kiek įmanoma.** Kiekvienas `fetch()` turi
   `.catch()` su matoma klaidos būsena, ne tuščią ekraną. Jei rodai
   „Kraunama…", privalai turėti ir „Nepavyko. Bandykite dar kartą".
4. **Nuotraukos ir ikonos — vienoje vietoje** (`static/img/`), kad
   manifestui užtektų pridėti 192 ir 512 px variantus.
5. **Naršymas veikia be naršyklės mygtukų.** Standalone režime „atgal"
   juostos nėra: drill-in ekranai turi savo „atgal" (arba × su `grizti`),
   vidiniai puslapiai — trupinių taką, žingsninės formos — mygtuką „Atgal".
6. **Nieko, kas iššoka iš programėlės.** `window.location.href` su pilnu
   domenu — ne. `target="_blank"` — tik tikrai išoriniams adresams
   (soc. tinklai, WhatsApp, pardavėjo svetainė); vidinei nuorodai niekada.

Kai PWA darysim, liks: manifestas, ikonos, `sw.js`, `<link rel="manifest">`
ir maišos saugyklos įjungimas. Jokių perrašymų — jei taisyklių laikomasi.

## 10. Demo failas — palyginimas PRIVALOMAS

Kai užduotyje duotas demo failas (`docs/demo/*.html`), darbas **nelaikomas
baigtu**, kol gyvas puslapis nepalygintas su demo greta ir neparodyta
lentelė. „Padariau pagal demo" be palyginimo nepriimama.

Kodėl ši taisyklė atsirado: du kartus iš eilės rezultatas nuo demo
nutolo (blokai be rėmelių, kitokie šriftų dydžiai, kiti tekstai,
atsiradę blokai, kurių demo nebuvo) — nes buvo dirbama „iš atminties",
o ne skaitant demo CSS.

**Tvarka:**

1. **Perskaityk visą demo CSS**, ne peržvelk. Užsirašyk reikšmes:
   šriftų dydžius ir svorius, tarpus, rėmelius, apvalinimą, tinklelius,
   aukščius, spalvas.
2. **Perkelk pažodžiui.** Jei demo rašo `18px/700`, tai ir turi būti
   `18px/700`, o ne „panašiai" ar „iš dizaino sistemos". Klases
   pervadink su savo prefiksu ir šalia komentaru surašyk atitikmenis
   (`demo .block -> .im-block`).
3. **Tekstai irgi pažodžiui**: „Rašyti žinutę", „Įsiminti įmonę",
   „Visos nuotraukos", „Kaip nuvažiuoti", „Paslaugos ir kainos",
   „Darbo laikas".
4. **Nekurk blokų, kurių demo nėra.** Jei atsirado savas blokas —
   išimk arba pagrįsk atskirai.
5. **Nufotografuok abu** per Playwright ties 1440 ir 390 px, sudėk
   greta (PIL) ir parodyk paveikslėlį.
6. **Pateik lentelę** `elementas | demo | pas mus | sutampa`. Visose
   eilutėse turi būti „taip". Jei kur nors „ne" — taisyk ir kartok.
7. **Sąmoningi nukrypimai** (pvz. atsiliepimai atidėti vėlesniam etapui)
   lentelėje rašomi atskira eilute su priežastimi — jie neslepiami.

Reikšmes patogu tikrinti ne akimis, o naršyklėje:

```js
getComputedStyle(document.querySelector('.im-block'))
  // fontSize, fontWeight, padding, borderRadius, gap, gridTemplateColumns…
```

Palygink demo ir gyvo puslapio `getComputedStyle` reikšmes — jos turi
sutapti skaičius į skaičių.
