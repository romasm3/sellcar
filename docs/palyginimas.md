# Elementų palyginimas su etalonu

Metodika: Playwright nuskaito puslapį (darbalaukis 1440 px, telefonas
390 px), nuslenka iki apačios, tada surenka **visų matomų elementų**
sąrašą iš viršaus į apačią — pozicija, aukštis, tekstas. Ta pati funkcija
abiem pusėms (`skanuoti.py`), todėl sąrašai palyginami tiesiogiai.

Nuskaityta **2026-08-21**. Etalonas: autogidas.lt.

Būsenos: **sutampa** · **skiriasi** · **trūksta** (yra pas juos, nėra pas
mus) · **perteklinis** (yra pas mus, nėra pas juos).

---

## 1. Pagrindinis puslapis

### 1.1 Darbalaukis (1440 px)

Etalone 61 matomas blokas, pas mus 38.

| # | Elementas | Etalone | Pas mus | Būsena |
|---|---|---|---|---|
| 1 | Antraštė | logotipas, „Įkelti skelbimą 0", 6 nuorodos (Finansavimas, Pasiūlymai verslui, KET testai, Autokatalogas, Straipsniai, Pagalba) | logotipas, kalba, „Įkelti", Prisijungti, Registruotis, 2 nuorodos | **skiriasi** — jų 6 turinio nuorodos, mūsų 2 |
| 2 | Reklamos juosta po antrašte | 3 partnerių baneriai, 173 px | nėra | **trūksta** (sąmoningai) |
| 3 | Paieškos panelė | y 295, aukštis 414 px, kairėje kategorijų ikonos | y 141, aukštis 449 px, ta pati struktūra | **sutampa** |
| 4 | Rezultatų skaičius virš panelės | nėra | „Rasti 7 skelbimai" (y 89) | **perteklinis** |
| 5 | „Mano paieškos" blokas | y 733, 136 px, tuščios būsenos tekstas | nėra | **trūksta** |
| 6 | Automobilio vertinimo blokas | y 893, 212 px („Kiek vertas tavo automobilis") | nėra | **trūksta** (sąmoningai — paslaugos nėra) |
| 7 | „Populiarios paieškos" | y 1129, 295 px, 6 temos | nėra | **trūksta** |
| 8 | „Partnerių pasiūlymai" | y 1448, 539 px | nėra | **trūksta** (sąmoningai) |
| 9 | Skelbimų skirtukai | „Naršyk skelbimus": Pasiūlymai / Naujausi / Su garantija / Partnerių, y 2011, 2502 px | „Pasiūlymai / Dienos pasiūlymai / Naujausias / Populiariausi / Brangiausias", y 679, 814 px | **skiriasi** — 4 vs 5 skirtukai, skirtingi pjūviai |
| 10 | Naujienų blokas | y 4536, 804 px, 1 straipsnis + „Skaityti daugiau" | nėra | **trūksta** |
| 11 | „Populiariausi automobiliai" (markių sąrašas) | y 5341, 783 px | nėra | **trūksta** |
| 12 | Poraštė | ~940 px, keturios skiltys + įmonės rekvizitai | 395 px, trys skiltys | **skiriasi** — trumpesnė |
| 13 | Slapukų sutikimas | 334 px modalas | nėra | **trūksta** (teisinis, ne dizaino) |

**Bendra:** puslapio aukštis etalone ~6 100 px, pas mus ~1 900 px.
Trūksta šešių turinio blokų; nė vienas iš jų nėra paieškos ar rezultatų
dalis — tai turinio ir partnerių sekcijos.

### 1.2 Telefonas (390 px)

Etalone 51 blokas, pas mus 36.

| # | Elementas | Etalone | Pas mus | Būsena |
|---|---|---|---|---|
| 1 | Antraštė | „Įkelti" + ☰, 70 px | „AL · Įkelti · žymė · ☰", 64 px | **sutampa** |
| 2 | Baneriai | 203 px, trys | nėra | **trūksta** (sąmoningai) |
| 3 | „Mano paieškos" | 103 px | nėra | **trūksta** |
| 4 | Paieškos panelė | „Automobilių skelbimų paieška", 705 px; eilutės: Markė+modelis, Metai, Kaina, Kuro tipas, Kėbulo tipas, Tik Lietuvoje | 657 px; tos pačios eilutės | **sutampa** |
| 5 | Vertinimo blokas | 223 px | nėra | **trūksta** |
| 6 | „Populiarios paieškos" | 274 px | nėra | **trūksta** |
| 7 | Partnerių pasiūlymai | 855 px | nėra | **trūksta** |
| 8 | Skelbimų skirtukai | 4 547 px (daug kortelių) | 2 028 px | **skiriasi** — mažiau kortelių |
| 9 | Naujienos, populiariausi automobiliai | 460 + 1 369 px | nėra | **trūksta** |
| 10 | Poraštė | 942 + 280 + 149 px | 697 px | **skiriasi** |

---

## 2. Rezultatų puslapis

### 2.1 Darbalaukis (1440 px)

| # | Elementas | Etalone | Pas mus | Būsena |
|---|---|---|---|---|
| 1 | Trupinių takas | „Skelbimai › Automobiliai › Volkswagen…" | nėra | **trūksta** |
| 2 | Kategorijos aprašas | 139 px („Automobiliai (28703) — Autogide parduodami…") | nėra | **trūksta** |
| 3 | Šoninė filtrų juosta | balta kortelė 230 px, „Daugiau filtrų" viršuje, 2 749 px turinio | balta kortelė 230 px, „Daugiau filtrų" viršuje, 900 px | **sutampa** (kortelė pataisyta 2026-08-21) |
| 4 | Tarpas juosta ↔ rezultatai | 16 px | 16 px | **sutampa** |
| 5 | Rezultatų antraštė | „Rasta skelbimų: 28703", rūšiavimas | „Rasti 7 skelbimai", „Išvalyti filtrus", „Išplėstinis", „Žemėlapis", rūšiavimas | **skiriasi** — pas mus 3 papildomi mygtukai |
| 6 | Kortelė | nuotrauka + 3 miniatiūros, pavadinimas, 6 parametrai su ikonomis, kaina, pardavėjas | nuotrauka + 3 miniatiūros, pavadinimas, kaina, parametrai, pardavėjo eilutė | **sutampa** (miniatiūros ir pardavėjas pridėti 2026-08-21) |
| 7 | Tekstas po rezultatais (SEO) | 512 px | nėra | **trūksta** |
| 8 | Skelbimų skirtukai po rezultatais | nėra | „Pasiūlymai / Dienos…" 814 px | **perteklinis** |
| 9 | Poraštė | 426 + 73 px | 395 px | **skiriasi** |

### 2.2 Telefonas (390 px)

| # | Elementas | Etalone | Pas mus | Būsena |
|---|---|---|---|---|
| 1 | Šoninė juosta | **nėra** | **nėra** | **sutampa** |
| 2 | Filtrų ikona antraštėje | „Keisti paiešką" → detali paieška | „Keisti paiešką" → `/paieska/<kat>/` | **sutampa** |
| 3 | Kategorijos aprašas | 186 px | nėra | **trūksta** |
| 4 | Kortelė | 508–664 px: nuotrauka su žymomis, pavadinimas, **6 parametrai trimis stulpeliais**, kaina | 429 px: nuotrauka, pavadinimas, kaina, 6 parametrai trimis stulpeliais | **sutampa** (pataisyta 2026-08-21) |
| 5 | Reklamos tarp kortelių | „Nelik plikas paėmęs paskolą" 383 px kas ~4 korteles | nėra | **trūksta** (sąmoningai) |
| 6 | Kortelių kiekis puslapyje | ~20 | 7 (visi turimi) | duomenų skirtumas, ne struktūros |

---

## 3. Detali paieška

Nuskaityta 2026-08-21: etalonas `/paieska/automobiliai/`, mūsų `/paieska/cars/`.

### 3.1 Darbalaukis

| # | Elementas | Etalone | Pas mus | Būsena |
|---|---|---|---|---|
| 1 | Puslapio antraštė | „Skelbimų paieška · Automobiliai", 52 px | „Detali paieška: Automobiliai", 62 px | **sutampa** |
| 2 | Kategorijų juosta po antrašte | **yra** — Auto, Motociklai, Ratai, Dalys, Ž. ūkio, Sunkusis tr., Priekabos, Nuoma… | nėra | **trūksta** |
| 3 | Laukų sritis | 2 976 px (visi laukai + ypatybių sąrašas) | 418 px | **skiriasi** — pas mus gerokai mažiau laukų |
| 4 | Veiksmų mygtukai | apačioje | „Išvalyti" + „Ieškoti N" | **sutampa** |
| 5 | Poraštė | 426 + 73 px | 395 px | **skiriasi** |

Puslapio aukštis: etalone ~3 500 px, pas mus ~1 400 px. Pagrindinis
skirtumas — ypatybių (equipment) sąrašas ir kategorijų juosta.

### 3.2 Telefonas

| # | Elementas | Etalone | Pas mus | Būsena |
|---|---|---|---|---|
| 1 | Laukai eilutėmis su „›" | taip | taip | **sutampa** |
| 2 | Kategorijų juosta | yra | nėra | **trūksta** |
| 3 | Apatinė veiksmų juosta | „Rodyti N" prilipusi apačioje | „Skelbimai N" prilipusi apačioje | **sutampa** |

---

## 4. Skelbimo puslapis

Etalonas: `volvo-s60-…0139757312`. Mūsų: `/725/` (testinis).

### 4.1 Darbalaukis

| # | Elementas | Etalone | Pas mus | Būsena |
|---|---|---|---|---|
| 1 | Trupinių takas | „Atgal · Skelbimai · Automobiliai · Volvo · S60", 60 px | „Naršyti automobilius" (viena nuoroda) | **skiriasi** |
| 2 | Nuotraukų galerija su žymomis | „PRIEŠ 1 D.", „+10" ant nuotraukos | žymės yra (New, VIN, ⭐) | **sutampa** |
| 3 | Nuotraukų peržiūra | sluoksnis su miniatiūromis | sluoksnis su miniatiūromis | **sutampa** (2026-08-21) |
| 4 | Kaina | 950 € + „Mėnesio įmoka nuo 15 €/mėn." | $15 900 | **skiriasi** — nėra finansavimo eilutės (sąmoningai) |
| 5 | Pagrindinė informacija | Metai, Kuro tipas, Rida, Pavarų dėžė, Variklis + „Tech. detalės" blokas | Metai, Rida, Kuras, … | **sutampa** |
| 6 | Kontaktai | pardavėjas, sutrumpintas telefonas, „Rašyti" | pardavėjas, sutrumpintas telefonas, „Siųsti žinutę" | **sutampa** (2026-08-21) |
| 7 | Draudimo / finansavimo blokai | 2 partnerių blokai turinyje | nėra | **trūksta** (sąmoningai) |
| 8 | „Panašūs skelbimai" | 411 px, 3–4 kortelės | **nėra** | **trūksta** |
| 9 | Poraštė | 474 + 73 px | 395 px | **skiriasi** |

### 4.2 Telefonas

| # | Elementas | Etalone | Pas mus | Būsena |
|---|---|---|---|---|
| 1 | Turinio aukštis | 4 197 px | 2 063 px | **skiriasi** — trūksta panašių skelbimų ir partnerių blokų |
| 2 | Prilipęs kontaktų blokas apačioje | **taip** — „Rašyti +370 653…" 78 px visada matomas | nėra — kontaktai tik puslapio viduje | **trūksta** |

---

## 5. Skelbimo kūrimo forma

| # | Elementas | Etalone | Pas mus | Būsena |
|---|---|---|---|---|
| 1 | Ar reikia prisijungti | **taip** — svečiui rodomas „Mano gidas" prisijungimo puslapis | taip — nukreipia į prisijungimą | **sutampa** |
| 2 | Prisijungimas + registracija viename | taip (du skirtukai) | ne — atskiri puslapiai | **skiriasi** |
| 3 | „Redaguoti skelbimą su redagavimo kodu" | **yra** (493 px kortelė) — leidžia tvarkyti skelbimą be paskyros | nėra | **trūksta** |
| 4 | Grįžimas po prisijungimo | į skelbimo kūrimą | į skelbimo kūrimą (`?next=/create/`) | **sutampa** (2026-08-21) |

---

## 6. Prisijungimas / registracija

| # | Elementas | Etalone | Pas mus | Būsena |
|---|---|---|---|---|
| 1 | Puslapio pavadinimas | „Mano gidas" | „Sveiki sugrįžę" | **skiriasi** |
| 2 | Prisijungimas ir registracija | vienas puslapis, du skirtukai | du atskiri puslapiai | **skiriasi** |
| 3 | Laukai | el. paštas, slaptažodis, „Prisiminti mane", „Priminti slaptažodį" | tie patys keturi | **sutampa** |
| 4 | Prekės ženklas puslapyje | Autogidas | **„SellCar" ir „SC" logotipas** | **defektas** — likutis nuo pervadinimo |
| 5 | Poraštė | 426 px | 395 px | **skiriasi** |

**Rastas defektas:** prisijungimo ir registracijos puslapiuose (ir dar 114
vietų šablonuose) likęs senas pavadinimas **SellCar**, o prisijungimo
kortelėje — „SC" logotipas vietoj „AL". Iš viso `SellCar` minimas
**116 kartų** 91 šablone.

---

## 7. Rasti ir jau ištaisyti defektai (2026-08-21)

| # | Kas buvo | Būsena |
|---|---|---|
| 1 | Šoninė juosta be baltos kortelės | ✅ `a03e59b` |
| 2 | „Žemės ūkio, spec. dalys" ir „Aksesuarai, Tuning" panelės tuščios | ✅ `f565808` |
| 3 | Oranžinis mygtukas dalių panelėje | ✅ `f565808` |
| 4 | Panelės antraštė „Paieška" vietoj kategorijos | ✅ `f565808` |
| 5 | „Automobilių supirkimas" metė į rezultatus | ✅ `f565808` |
| 6 | Statybinės technikos priedų panelė nepasiekiama | ✅ `f565808` |
| 7 | Kontaktai skelbime už prisijungimo | ✅ `e8c39e9` |
| 8 | Nuotrauka atidarydavo failą, ne peržiūrą | ✅ `9d88053` |
| 9 | Penkios konkuruojančios spalvos viename ekrane | ✅ `4fef8ab` |
| 10 | Rezultatų kortelė telefone be turinio | ✅ `81763c0` |
| 11 | Kortelėje darbalaukyje nebuvo miniatiūrų ir pardavėjo | ✅ `b5105e1` |

---

## 8. Suvestinė: kas skiriasi labiausiai

| Sritis | Trūkstamų blokų | Iš jų sąmoningai praleista |
|---|---|---|
| Pagrindinis | 6 | 3 (baneriai, partnerių pasiūlymai, vertinimas) |
| Rezultatai | 3 | 1 (reklamos tarp kortelių) |
| Detali paieška | 2 | 0 |
| Skelbimo puslapis | 4 | 2 (draudimas, finansavimas) |
| Kūrimo forma | 2 | 0 |
| Prisijungimas | 2 + 1 defektas | 0 |

**Nesąmoningi skirtumai, kuriuos verta spręsti** (eilės tvarka pagal
poveikį vartotojui):

1. Skelbimo puslapyje nėra **prilipusio kontaktų bloko telefone** — etalone
   „Rašyti / telefonas" matomas visą laiką slenkant.
2. Nėra **„Panašūs skelbimai"** bloko — praranda perėjimus tarp skelbimų.
3. Detalioje paieškoje nėra **kategorijų juostos** ir trūksta ypatybių
   laukų (2 976 px vs 418 px).
4. Prisijungimo puslapiuose likęs **SellCar** pavadinimas (116 vietų).
5. Skelbimo puslapyje nėra **trupinių tako** (Skelbimai › Automobiliai › BMW).
6. Registracija ir prisijungimas atskiruose puslapiuose, o ne viename.

---

## 9. Įrankis

`docs/palyginimas-skaneris.py` — funkcija `run()` priima sąrašą
(pavadinimas, url, ar telefonas, ar praleisti TLS klaidas) ir surašo
visus matomus elementus į JSON. Ta pati funkcija naudota abiem pusėms,
todėl skaičiai palyginami tiesiogiai.
