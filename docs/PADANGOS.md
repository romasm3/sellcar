# AutoLeft — klaidos: PADANGOS (Ratlankiai / padangos)

Forma: `/create/tyres/` · Skelbimas: `/wheels/<id>/` · Katalogas: `/browse/tyres/`
Etalonas — **autogidas.lt**. Valiuta — tik EUR. Dizaino nekeisti.
Būsenos: `NAUJA` · `TAISOMA` · `IŠTAISYTA` · `ATŠAUKTA`

Patikrinta 2026-09-15, sukurti 6 skelbimai — po vieną į kiekvieną „Paskirtis" reikšmę.

---

## BLOKUOJANČIOS — kategorija neveikia be apėjimo

| Kodas | Problema | Būsena |
|---|---|---|
| `TYRE-01` | **Padangų skelbimo pateikti NEĮMANOMA.** `handleTyresSubmit()` tikrina `document.getElementById('id_contact_phone')`, bet tikrasis telefono lauko id yra **`id_phone`** (`name="contact_phone"`). Todėl `phone` visada `null` → visada įrašoma klaida „Būtinas telefono numeris" → `return`, forma niekada nesiunčiama. Nesvarbu, kad telefonas jau užpildytas serverio (`+370 601 00000`). **Atkūrimas:** atidaryti `/create/tyres/`, užpildyti viską, spausti „Pateikti skelbimą" — puslapis lieka vietoje, viršuje „Būtinas telefono numeris". **Taisymas:** `getElementById('id_phone')` (arba `querySelector('[name="contact_phone"]')`). | NAUJA |
| `RIM-01` | **Ta pati klaida ratlankių formoje** `/create/rims/`. `handleRimsSubmit()` taip pat ieško `id_contact_phone`, o tokio id puslapyje nėra (patikrinta: `id_brand_name`, `id_diameter`, `id_price`, `id_rim_material`, `id_rim_bolt_count`, `id_rim_pcd`, `id_rim_width`, `id_country`, `id_state`, `id_city`, `id_agree_terms` — visi OK, tik `id_contact_phone` MISSING). Ratlankių skelbimo irgi paskelbti neįmanoma. Taisyti kartu su `TYRE-01`. | NAUJA |

> Šios sesijos 6 padangų skelbimai (#26–#31) paskelbti tik apėjus klaidą konsolėje
> (`document.getElementById('id_phone').id='id_contact_phone'`). Realus vartotojas to negali.

---

## NETEISINGI PRANEŠIMAI

| Kodas | Problema | Būsena |
|---|---|---|
| `TYRE-02` | **Validacijos žinutės sumaišytos — rodoma ne tai, ko trūksta.** `handleTyresSubmit()`: trūksta gamintojo → „Būtina nurodyti **valstiją**"; trūksta skersmens → „Būtina nurodyti **valstiją**"; trūksta pločio → „Būtina nurodyti **miestą**"; trūksta profilio → „Būtina nurodyti **kainą**"; trūksta sezoniškumo → „Būtina nurodyti **metus**". Vartotojas negali suprasti, ką taisyti. Reikia po vieną teisingą tekstą kiekvienam laukui. | NAUJA |

---

## TRŪKSTAMI DYDŽIAI — dalies padangų įdėti neįmanoma

| Kodas | Problema | Būsena |
|---|---|---|
| `TYRE-03` | **Kūrimo formos skersmenų sąrašas per trumpas ir nesutampa su filtru.** Forma: `R10–R24` (15 reikšmių). Katalogo filtras `/browse/tyres/`: `R4, R5, R6, R8, R9, R10…R13, R13C, R14, R14C, R15, R15C, R16, R16C, R17, R17C, R17.5, R18, R19, R19.5, R20, R21, R22, R22.5, R23, R24, R24.5, R25, R26, R28, R30, R32, R34, R38, R42, R44, R46, R49, R51, R54, R57, R63`. Filtruoti galima pagal R22.5, bet **sukurti tokio skelbimo negalima**. Sunkvežimių (R17.5/R19.5/R22.5), C tipo (R13C–R17C) ir žemės ūkio (R28–R63) padangų kategorijos praktiškai negyvos. | NAUJA |
| `TYRE-04` | **Pločio ir profilio sąrašai nesutampa tarp formos ir filtro.** Plotis formoje `125–355` (žingsnis 10), filtre `135–355` — 125 filtru nerandama. Profilis formoje `20–85`, filtre `25–90` — 20 nerandama, 90 neįvedama. | NAUJA |

---

## ATVAIZDAVIMAS — skelbimo puslapis `/wheels/<id>/`

| Kodas | Problema | Būsena |
|---|---|---|
| `TYRE-05` | **Sezoniškumas rodomas žaliu DB kodu:** „Sezoniškumas: **summer**" vietoj „Vasarinės". Kortelėje kataloge rodoma teisingai („Vasarinės"), sulūžęs tik detalės šablonas. Patikrinti ir `winter`, `all_season`. | NAUJA |
| `TYRE-06` | **Neišversti laukų pavadinimai tarp lietuviškų:** „**Specifications**" (antraštė), „**Remaining**" (turi būti „Likutis"), „**Production year**" (turi būti „Pagaminimo metai (DOT)"). Visi kiti toje pačioje lentelėje lietuviški. | NAUJA |
| `TYRE-12` | **Automatinis pavadinimas be „R":** „Bridgestone 225/45 **18**", nors tos pačios kortelės viduje „Dydis: 225/45 **R18**". Turi būti „Bridgestone 225/45 R18". | NAUJA |
| `TYRE-16` | Kaina pažymėta „**Vieneto kaina**", bet formoje laukas tiesiog „Kaina", o šalia „Kiekis". Neaišku, ar vesti už vieną, ar už komplektą — Autogidas rodo abi eilutes. Reikia arba etiketės formoje („Kaina už vienetą"), arba antros eilutės „Komplektas (4 vnt.): 960 €". | NAUJA |

---

## ATVAIZDAVIMAS — katalogas `/browse/tyres/`

| Kodas | Problema | Būsena |
|---|---|---|
| `TYRE-07` | **Puslapio `<title>` — „Naršyti sunkvežimius - AutoLeft"** padangų kataloge. Nukopijuotas sunkvežimių šablonas. | NAUJA |
| `TYRE-08` | **„Nerasta jokių skelbimų 6"** rodoma virš 6 matomų kortelių. Patikrinta ir su filtru (`?purpose=moto` → „Nerasta jokių skelbimų 1" virš 1 kortelės). Elementas matomas (`display:block`). Turi būti „Rasta skelbimų: 6". | NAUJA |
| `TYRE-09` | **Kortelės žyma „Redaguoti profilį 50"** — panaudota vartotojo profilio vertimo eilutė padangos profiliui. Turi būti „Profilis 50". | NAUJA |
| `TYRE-10` | **„Paskirtis" pavadinimai skiriasi formoje ir filtre.** Forma: Lengvieji automobiliai / Visureigiams / Komerciniams / mikroautobusams / Sunkvežimiai / Motociklai / Pramoniniai. Filtras: Lengviesiems / Visureigiams / Mikroautobusams / Sunkvežimiams ir autobusams / Motociklams / **Traktoriams ir spec technikai**. Reikšmės (`passenger/suv/commercial/truck/moto/industrial`) sutampa, todėl filtras veikia, bet vartotojui atrodo kaip skirtingos kategorijos. Suvienodinti. | NAUJA |
| `TYRE-17` | Kortelėje vienu metu du skirtingi „Naujas": viršuje žyma „Naujas" (= neseniai įkeltas) ir apačioje būklė „Naudotas". Patikrinta #30 — kortelė sako ir „Naujas", ir „Naudotas". Pervadinti įkėlimo žymą („Naujiena" arba tik laiko žyma). | NAUJA |

---

## FORMOS DEFEKTAI

| Kodas | Problema | Būsena |
|---|---|---|
| `TYRE-13` | `agree_terms` neturi `required` — kaip ir `CAR-03`. | NAUJA |
| `TYRE-14` | „Apkrovos indeksas" — laisvas tekstas be jokios patikros. Priimta „75W", „109/107", „104Q". Autogidas turi atskirą sąrašą. Padaryti sąrašą arba bent formato patikrą. | NAUJA |
| `TYRE-15` | **Nuotraukų laukas dvigubas ir painus:** matomas `imageInput` (be `name`) ir paslėptas `photosSubmitInput` (`name="photos"`). Tikrieji failai laikomi JS masyve `selectedFiles`, o `photosSubmitInput.files` perrašomas tik pateikimo metu. Programiškai ar naršyklės autofill'u įkeltos nuotraukos dingsta be klaidos. Susiję su `FILE-01`. | NAUJA |
| `TYRE-18` | Formoje **nėra `currency` lauko iš viso**. Šiuo metu rezultatas teisingas (EUR), bet niekas jo neužfiksuoja — vos tik bus įvesti USD/GBP, ši kategorija liks be valiutos. Pažymėta žinojimui; **dabar nieko nekeisti** (valiutos logikos neliesti). | NAUJA |

---

## SIŪLOMA EILĖ

1. `TYRE-01` + `RIM-01` — vienos eilutės taisymas, atrakina dvi kategorijas
2. `TYRE-02` — klaidingi pranešimai
3. `TYRE-05`, `TYRE-06`, `TYRE-07`, `TYRE-08`, `TYRE-09` — pigūs šablonų taisymai
4. `TYRE-03` + `TYRE-04` — dydžių sąrašai (formą suvienodinti su filtru)
5. `TYRE-10`, `TYRE-12`, `TYRE-16`, `TYRE-17`
6. `TYRE-13`, `TYRE-14`, `TYRE-15`

---

## PALYGINIMAS SU AUTOGIDU

Pilnas laukas-po-lauko palyginimas — `PADANGOS-PALYGINIMAS-SU-AUTOGIDU.md`.
Paruoštas promptas Claude Code'ui — `PROMPT-padangos.md`.

Santrauka, ko trūksta prieš Autogidą:

| Laukas | Autogidas | Mes |
|---|---|---|
| Paskirtis | 6 (su **Keturračiams**) | 6 (be Keturračių) |
| Skersmuo | 57 (R4–R63, C tipo, .5) | 15 (R10–R24) |
| Plotis | 80 (nuo 5.50 iki 1050) | 24 (125–355) |
| Aukštis | 29 (12.5–120) | 14 (20–85) |
| Būklė | 3 (su **Restauruotos**) | 2 |
| Sezoniškumas | 4 (su **Kitas**) | 3 |
| Protektoriaus gylis | 27 (1–40 mm) | 10 (1–10 mm) |
| Padangų likutis | 20 (žingsnis 5) | 10 (žingsnis 10) |
| Nuotraukų limitas | parodytas (36, 24 MB) | neparodytas |

Mūsų pranašumas, kurio Autogidas neturi (palikti): greičio indeksas, apkrovos
indeksas, 30+ šalių, laisvas miestas, „Visureigiams" paskirtis.

---

## TESTINIAI SKELBIMAI

| ID | Paskirtis | Kas | Šalis |
|---|---|---|---|
| `/wheels/26/` | Lengvieji automobiliai | Bridgestone Potenza S001 225/45 R18, 4 vnt, 240 € | DE |
| `/wheels/27/` | Visureigiams | Continental SportContact 6 285/40 R21, 4 vnt, 560 € | IT |
| `/wheels/28/` | Komerciniams / mikroautobusams | Michelin Agilis Alpin 215/65 R16, 4 vnt, 420 € | PL |
| `/wheels/29/` | Sunkvežimiai | Barum 295/70 R21, 6 vnt, 1 080 € — **reali žyma 315/70 R22.5, tokio dydžio nėra** (`TYRE-03`) | NL |
| `/wheels/30/` | Motociklai | Michelin Pilot Power 3 185/50 R17, 2 vnt, 260 € — **reali žyma 120/70 ZR17 + 180/55 ZR17** (žr. MOTO-PADANGOS.md) | FR |
| `/wheels/31/` | Pramoniniai | Barum Multerrain M/T 235/75 R15, 4 vnt, 480 €, naujos | BE |

Nuotraukos — iš Autogido (`img.autogidas.lt`), po 2–4 vnt., visos atsidarė be klaidų.

---

## PAPILDYTA 2026-09-15 — 2 skelbimai tiesiai iš Autogido

| Mūsų | Autogido originalas | Ką teko iškraipyti |
|---|---|---|
| `/wheels/32/` Sava Eskimo Ice 215/60 R16, žieminės, 4 vnt, 138 €/vnt, Kaunas | `122677976` — likutis **95 %**, protektorius 9,0 mm, komplektas 550 € | likutis įvestas **90 %** — 95 sąraše nėra (`TYRE-04`) |
| `/wheels/33/` Bridgestone Duravis 205/65 R16, mikroautobusams, 2 vnt, 50 €/vnt, Marijampolė | `122605000` — skersmuo **R16C**, likutis 100 % | įvesta **R16** — C tipo skersmens nėra (`TYRE-03`) |

Abu paskelbti tik apėjus `TYRE-01` konsolėje.
