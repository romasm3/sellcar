# Padangų forma: AutoLeft vs Autogidas

Autogido etalonas: `autogidas.lt/v2/naujas-skelbimas` → Ratlankiai / padangos → Padangos
Mūsų: `autoleft.com/create/tyres/`
Nuskaityta 2026-09-15 iš abiejų gyvų formų.

---

## 1. Ką Autogidas turi, o mes NE

| Laukas | Autogidas | AutoLeft | Trūkumas |
|---|---|---|---|
| **Paskirtis** | 6: Lengviesiems · Motociklams · **Keturračiams** · Mikroautobusams · Sunkvežimiams ir autobusams · Traktoriams ir spec technikai | 6: Lengvieji · Visureigiams · Komerciniams/mikroautobusams · Sunkvežimiai · Motociklai · Pramoniniai | nėra **Keturračiams (ATV)**; mūsų „Visureigiams" Autogidas neturi (mūsų pranašumas — palikti) |
| **Skersmuo** | **57** reikšmės: R4–R63, tarp jų R10C, R12C, R13C, R14C, R15C, R15.3, R15.5, R16C, R16.5, R17C, R17.5, R19.5, R22.5, R24.5, R26.5 | **15**: R10–R24 | trūksta **42 reikšmių** — visų C tipo, visų .5 ir viso žemės ūkio diapazono |
| **Plotis** | **80** reikšmių: 5.50, 6.00, 6.50, 7.00, 10.5, 11.5, 12.5, 13.5, 14, 20, 32, 33, 38, 80, 85, **90–130**, 135–355, 365, 385, 425–1050 | **24**: 125–355 žingsniu 10 | trūksta **moto (80–130)**, colinių (5.50–14) ir žemės ūkio (365–1050) |
| **Aukštis (profilis)** | **29**: 12.5, 14, 14.5, 20, 25, 30, 31, 32, 33, 35, 37, 40–85, 88, **90, 95, 100, 105, 110, 115, 120** | **14**: 20–85 žingsniu 5 | trūksta moto ir sunkiojo profilių nuo 88 iki 120 ir smulkiųjų 12.5–14.5 |
| **Būklė** | Naudotos · Naujos · **Restauruotos** | Naudotas · Naujas | nėra **Restauruotos** (atnaujinto protektoriaus padangos — sunkiajam transportui įprasta) |
| **Sezoniškumas** | Vasarinės · Universalios · Žieminės · **Kitas** | Vasarinės · Žieminės · Universalios | nėra **Kitas** |
| **Protektoriaus gylis mm** | **27**: 1, 1.5, 2, 2.5, 3, 3.5, 4, 5–20, 25, 30, 35, 40 | **10**: 1–10 | naujos sunkiojo ir žemės ūkio padangos turi 14–25 mm — įvesti neįmanoma |
| **Padangų likutis %** | **20**: 5–100 žingsniu **5** | **10**: 10–100 žingsniu **10** | 95%, 85%, 75% ir t. t. įvesti neįmanoma (realiai naudojama dažnai) |
| **Kaina** | etiketė **„Vieneto kaina"** | etiketė „Kaina" | neaišku, ar už vienetą, ar už komplektą (`TYRE-16`) |
| **Miestas** | sąrašas: Vilnius, Kaunas, … + „Kitas miestas" | laisvas tekstas | be sąrašo filtruoti sunku (mūsų laisvas tekstas tinka užsieniui — reikia autocomplete, ne uždaryto sąrašo) |
| **El. paštas** | privalomas, su pastaba „Portalo lankytojams nematomas" | neprivalomas, be pastabos | — |
| **Nuotraukos** | parašyta: iki **36**, max **24 MB**, JPG/GIF/PNG | limitas niekur neparodytas | vartotojas nežino ribų |
| **Pardavėjas** | rodo „Privatus asmuo" + **„Tapatybė patvirtinta"** | tik privatus | žr. `CAR-06` |

## 2. Ką mes turime, o Autogidas NE (pranašumas — palikti)

- Greičio indeksas (J–Z)
- Apkrovos indeksas
- Pagaminimo metai (DOT) — Autogidas turi, bet mūsų iki 2026
- Šalis su 30+ valstybių ir laisvas miestas (Autogidas — praktiškai tik Lietuva)
- „Ypatumai" varnelės — abu turi tas pačias 8

## 3. Kas sulaužyta mūsų pusėje (žr. PADANGOS.md)

- `TYRE-01` / `RIM-01` — formos pateikti **neįmanoma** (`id_contact_phone` vs `id_phone`)
- `TYRE-02` — validacijos pranešimai rodo ne tą lauką
- `TYRE-05`, `TYRE-06` — „summer", „Specifications", „Remaining", „Production year"
- `TYRE-07`, `TYRE-08`, `TYRE-09` — katalogo antraštė, „Nerasta jokių skelbimų 6", „Redaguoti profilį"

## 4. Realūs įrodymai iš šios sesijos

| Mūsų skelbimas | Autogido originalas | Ką teko iškraipyti |
|---|---|---|
| `/wheels/32/` Sava 215/60 R16 | Sava Eskimo Ice, likutis **95%** | likutis įvestas **90%** — 95 sąraše nėra |
| `/wheels/33/` Bridgestone 205/65 16 | Bridgestone Duravis **R16C** | įvesta **R16** — C tipo skersmens nėra |
| `/wheels/29/` Barum 295/70 21 | reali sunkvežimio žyma **315/70 R22.5** | nei R22.5, nei tokio pločio nėra |
| `/wheels/30/` Michelin 185/50 17 | reali moto žyma **120/70 ZR17 + 180/55 ZR17** | nei 120, nei 180 pločio nėra |
