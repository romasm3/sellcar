# Ratlankiai ir Padangos — etalonas (autogidas.lt)

Nuskaityta iš autogidas.lt. Dvi ATSKIROS kategorijos, ne vieno puslapio
„Tipas: ratlankiai / padangos" perjungiklis. Spalvos — mūsų (antracitas),
ne etalono oranžinė. Create forma pagal šį dokumentą NEKEIČIAMA — čia tik
naršymas ir paieška.

Įgyvendinimas: `/browse/rims/` ir `/browse/tyres/`
(`apps/listings/wheels_filters.py` — laukai ir reikšmių sąrašai,
`apps/listings/wheels_views.py` — `rims_list` / `tyres_list`).

---

## RATLANKIAI (LT: Ratlankiai / EN: Rims)

Šoninės juostos filtrai eilės tvarka:

| # | LT | EN | Parametras | Reikšmės |
|---|----|----|------------|----------|
| 1 | Tipas | Type | `rim_material` | Visi, Priedai, Lengvojo lydinio, Plieniniai štampuoti, Kalti, Atsarginis ratas, Ratų gaubtai, Ratlankių dangteliai |
| 2 | Skersmuo | Diameter | `diameter` | Visi, R4–R42 (R4…R13, R14, R15, R16, R16.5, R17, R17.5, R18, R19, R19.5, R20, R21, R22, R22.5, R23, R24, R24.5, R26, R26.5, R28, R29, R30, R32, R34, R38, R42) |
| 3 | Tvirtinimo taškai | Bolt count | `rim_bolt_count` | Visi, 1, 3, 4, 5, 6, 8, 10, 12 |
| 4 | Tarpai tarp skylių (mm) | PCD (mm) | `rim_pcd_mm` | 92.25–222.25 standartinės reikšmės (98.00, 100.00, 105.00, 108.00, 110.00, 112.00, 114.30, 115.00, 118.00, 120.00, 120.65, 125.00, 127.00, 130.00, 139.70 ir kt.) |
| 5 | Centr. skylės diametras | Centre bore | `rim_dia` | 43.0–161.0 (56.5, 57.1, 58.1, 63.4, 65.1, 66.5, 66.6, 67.1, 70.0, 71.5, 72.5, 73.1, 74.1 ir kt.) |
| 6 | Plotis (coliais) | Width (inches) | `rim_width` | Visi, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 11, >11 |
| 7 | Gamintojas | Manufacturer | `brand` | Ratlankių gamintojai (BBS, Borbet, Dezent, Dotz, Enkei, OZ Racing, Ronal, Vossen…) + auto markės + „Kitas" |
| 8 | Tr. priem. markė | Vehicle brand | `fits_brand` | Automobilių markės (populiariausios su skaičiais + visos) |
| 9 | Tr. priem. modelis | Vehicle model | — | **Neįgyvendinta:** DB nėra lauko modeliui (`WheelListing.fits_brands` saugo tik markes) |
| 10 | Kaina | Price | `price_from` / `price_to` | 5, 10, 15, 20, 25, 30, 35, 40, 50, 60, 70, 80, 90, 100, 125, 150, 175, 200, 300, 400, 500, 600, 700, 800, 900, 1000 |
| 11 | Kiekis | Quantity | `quantity` | Visi, 1–9 |
| 12 | Naudoti/Nauji | Condition | `condition` | Visi, Naudoti, Nauji |
| 13 | Šalis | Country | `country_filter` | Visi, Lietuva, Lenkija, Latvija, Estija… |
| 14 | Miestas | City | `city` | LT miestai |
| 15 | Rodyti ne senesnius nei | Show not older than | `age` | Visi, Vienos dienos, Vienos dienos (tik nauji), Trijų dienų, Savaitės, Dviejų savaičių |
| 16 | Pardavėjo tipas | Seller type | `seller_type` | Visi, Privatus, Verslas |
| 17 | Tekstinė paieška | Text search | `q` | + mygtukas „Ieškoti" |

Žymimieji langeliai juostos apačioje:

| LT | EN | Laukas |
|----|----|--------|
| Parduodu po vieną | Sold individually | `feat_sold_single` |
| Su padangom | With tyres | `rim_feat_with_tyres` |
| Originalūs ratlankiai | Original rims | `rim_feat_original` |
| Chromuoti | Chrome | `rim_feat_chromed` |
| Aplankstyti ratlankiai | Bent rims | `rim_feat_bent` |

Virš rezultatų — greitos nuorodos (chip'ai): Lengvojo lydinio, Plieniniai
štampuoti, Atsarginis ratas, Ratų gaubtai, Ratlankių dangteliai, Kalti,
Priedai.

---

## PADANGOS (LT: Padangos / EN: Tyres)

| # | LT | EN | Parametras | Reikšmės |
|---|----|----|------------|----------|
| 1 | Paskirtis | Purpose | `purpose` | Lengviesiems (Cars), Motociklams (Motorcycles), Mikroautobusams (Vans), Sunkvežimiams ir autobusams (Trucks and buses), Traktoriams ir spec technikai (Tractors and machinery), Visureigiams (SUV) |
| 2 | Sezoniškumas | Season | `tyre_season` | Visi, Vasarinės (Summer), Universalios (All-season), Žieminės (Winter) |
| 3 | Naudotas/Naujas | Condition | `condition` | Visi, Naudotos, Naujos |
| 4 | Skersmuo | Diameter | `diameter` | Visi, R4–R63 su C variantais (R13, R13C, R14, R14C, R15, R15C, R16, R16C, R17, R17C, R17.5, R18, R19, R19.5, R20, R21, R22, R22.5 ir kt.) |
| 5 | Plotis | Width | `tyre_width` | 135–355 (155, 165, 175, 185, 195, 205, 215, 225, 235, 245, 255, 265, 275, 285, 295, 305, 315, 325) + spec. technikos reikšmės iš DB |
| 6 | Aukštis (profilis) | Profile | `tyre_profile` | 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90 + reikšmės iš DB |
| 7 | Kaina | Price | `price_from` / `price_to` | 5–3000 |
| 8 | Gamintojas | Manufacturer | `brand` | Padangų gamintojai (Michelin, Continental, Bridgestone, Nokian, Goodyear…) |
| 9 | Protektoriaus gylis mm | Tread depth (mm) | `tread_from` / `tread_to` | 1, 1.5, 2 … 8, 9, 10 … 40 |
| 10 | Kiekis | Quantity | `quantity` | Visi, 1, 2, 3, 4, 5 ir daugiau |
| 11 | Rodyti ne senesnius nei / Pardavėjo tipas / Šalis / Miestas / Tekstinė paieška / Ieškoti | kaip ratlankiuose | `age`, `seller_type`, `country_filter`, `city`, `q` | |

Žymimieji langeliai juostos apačioje:

| LT | EN | Laukas |
|----|----|--------|
| Visureigių padangos | SUV tyres | `feat_suv` |
| Sportinės padangos | Sport tyres | `feat_sport` |
| Sustiprintos | Reinforced | `feat_reinforced` |
| Parduodamos po vieną | Sold individually | `feat_sold_single` |
| Run on flat | Run flat | `feat_run_flat` |
| Atsarginė padanga „plona" | Space-saver spare | `feat_spare_thin` |
| Lietaus padangos | Rain tyres | `feat_rain` |
| Žieminės dygliuotos | Studded winter | `feat_studded` |

---

## Nukrypimai nuo etalono (ir kodėl)

- **Tr. priem. modelis** — nėra DB lauko (`fits_brands` saugo tik markes),
  todėl filtro nėra. Reikėtų naujo lauko create formoje, o forma pagal šią
  užduotį nekeičiama.
- **Padangų „Sezoniškumas → Kitas"** ir **„Paskirtis → Keturračiams"** —
  tokių reikšmių modelyje nėra (`TYRE_SEASON_CHOICES`,
  `WHEEL_PURPOSE_CHOICES`), o jų pridėjimas keistų create formą.
- **PCD (mm)** — DB `rim_pcd` saugo „5x112" pavidalu, todėl filtras lygina
  reikšmę po „x" (98.00 → `…x98`).
- Sena nuoroda `/browse/wheels/` → 301: `?type=rim` į ratlankius,
  `?type=tyre` ir be parametro — pagal etaloną į ratlankius.

## „Make" taisyklė

EN kalboje markė visur **Brand** (Vehicle brand), gamintojas —
**Manufacturer**. Žodis „Make" nenaudojamas niekur.
