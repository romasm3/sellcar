# AutoLeft — klaidos: DALYS

Formos: `/create/parts/form/?sub=<slug>` · `/create/car-for-parts/`
Etalonas — **autogidas.lt** (dalių medžio Autogidas neturi — mūsų 294 lapų medis yra pranašumas, tik neišverstas).
Valiuta — tik EUR. Dizaino nekeisti.

---

## BLOKUOJANČIOS

| Kodas | Problema | Būsena |
|---|---|---|
| `PARTS-01` | `/create/car-for-parts/` pateikus grąžina **500**. Atkūrimas: POST su vien `price=33` → 500; su `price=0`, tuščiu arba `abc` → 200. Krenta tik gavus galiojančią netuščią skaitinę reikšmę, t. y. išsaugojimo kelyje. Skelbimo sukurti neįmanoma. | NAUJA |

---

## DUOMENŲ PRARADIMAS (nauja 2026-09-15)

| Kodas | Problema | Būsena |
|---|---|---|
| `PARTS-02` | **Po validacijos klaidos vartotojo įvestas pavadinimas dingsta ir pakeičiamas kategorijos pavadinimu.** Atkūrimas: `/create/parts/form/?sub=doors-door-parts-door-front-left`, įvesti „Honda Civic VIII 2006 priekinės kairės durys, pilkos", nepažymėti taisyklių varnelės, pateikti → grįžta forma, o `title` lauke jau **„Door Front Left"**. Visi kiti laukai (OEM, markė, modelis, metai, spalva, kaina, aprašymas, telefonas, šalis, miestas) išliko teisingi — sulaužytas tik `title`. | NAUJA |
| `PARTS-03` | **Po validacijos klaidos dingsta VISOS įkeltos nuotraukos.** Tame pačiame atkūrime: prieš pateikimą `input.files.length` = 6, po grąžinimo = **0**, jokio įspėjimo. Vartotojas turi kelti iš naujo, nesuprasdamas, kad jų nebėra. | NAUJA |
| `PARTS-04` | `agree_terms` neturi `required` — naršyklė praleidžia, serveris atmeta, ir kartu nusinešami `PARTS-02` + `PARTS-03`. Užtenka pridėti `required`, kad abu duomenų praradimai nebeįvyktų kasdieniu atveju. | NAUJA |

---

## FORMOS STRUKTŪRA

| Kodas | Problema | Būsena |
|---|---|---|
| `PARTS-05` | **Klaidų blokas atvaizduojamas du kartus ir dviem kalbomis.** Puslapyje vienu metu: „Please fix the following: Turite sutikti su taisyklėmis" ir „Ištaisykite šias klaidas: Turite sutikti su taisyklėmis". Tas pats tekstas 4 kartus DOM'e. | NAUJA |
| `PARTS-06` | **Visoms 294 dalių rūšims naudojama viena bendra automobilio specifikacijų forma.** Nesvarbu, kas parduodama, klausiama: kuro tipas, variklio tūris, galia, pavarų dėžė, kėbulo tipas, durų skaičius, pavara. Trūksta pačios dalies parametrų: ratlankiams — **skersmuo, plotis, PCD, ET, centrinė skylė**; stabdžių diskams — **skersmuo, storis, ventiliuojamas/pilnas**; žibintams — **pusė (kairė/dešinė), tipas (halogen/xenon/LED)**; durims — **pusė ir spalvos kodas** (spalvos kodas yra, pusė – tik per kategoriją). Patikrinta `wheels-tyres-wheels-alloy-wheel` — ratlankio dydžio įvesti nėra kur, teko rašyti į „Versija" laisvu tekstu. | NAUJA |
| `PARTS-07` | **Mišri kalba tame pačiame išskleidžiamajame sąraše.** `condition` reikšmės angliškos (New / Used / Refurbished / Damaged), o `fuel_type` ir `transmission` tame pačiame puslapyje lietuviškos (Benzinas / Mechaninė). `body_type` — „Hatchback" (angliškai), `drive_type` — „Front (FWD)", `country` — „Ispanija" (lietuviškai). Žr. ir `LANG-07`. | NAUJA |

---

## VERTIMAI

| Kodas | Problema | Būsena |
|---|---|---|
| `LANG-05` | **Visas dalių medis angliškas:** 19 grupių, 294 galinės dalys, 3 lygiai. Lighting · Engine · Brakes · Exhaust System ir t. t. Formos antraštė „Car, van parts". Didžiausias vertimų darbas svetainėje. **Slug'ų NEKEISTI** — jie URL raktai. | NAUJA |
| `LANG-07` | Dalių forma pusiau išversta. Angliškai: „Part Name *", „Part Code", „Condition *", „Brand", „Modification", „Year", „Fuel Type", „Engine Size", „Power", „Gearbox", „Body Type", „Price (€)", mygtukas „Continue to Plan Selection →". Lietuviškai toje pačioje formoje: „Modelis", „Telefonas*", „El. paštas", „Šalis*", „Valstija*". | NAUJA |

---

## KITA

| Kodas | Problema | Būsena |
|---|---|---|
| `GEO-01` | **„Valstija" sąrašas rodo AUSTRALIJOS ir JAV valstijas, nors šalis — Lietuva.** `country=LT`, o `state` išskleidžia 73 variantus: „Australian Capital Territory", „New South Wales", „Queensland", „Tasmania"… Lietuviškų apskričių nė vienos. Sąrašas nefiltruojamas pagal šalį. Galioja ir kitoms formoms. | NAUJA |
| ~~`PHOTO-01`~~ | ~~Dalių forma įkelia tik 1 nuotrauką iš 3~~ — **ATŠAUKTA**. Paneigta: forma laiko failus `input`'e ir įkelia visus pateikimo metu. Patikrinta #811 (5 nuotr.), #812 (10 nuotr.), #813–#815. | ATŠAUKTA |

---

## SIŪLOMA EILĖ

1. `PARTS-01` — kategorija neveikia visai
2. `PARTS-04` (viena eilutė) → automatiškai nuima kasdienį `PARTS-02` ir `PARTS-03` poveikį
3. `PARTS-02` + `PARTS-03` — serverinis pataisymas
4. `PARTS-05` — dvigubas klaidų blokas
5. `GEO-01`
6. `PARTS-06` — kategorijai specifiniai laukai (didelis darbas)
7. `LANG-07`, tada `LANG-05` (didysis medžio vertimas)

---

## TESTINIAI SKELBIMAI

| ID | Kas | Kategorija | Šalis |
|---|---|---|---|
| #810 | BMW N47D20C variklis, 850 € | `engine-engine-block-engine-assembly` | — |
| #811 | BMW F30 328i galinis žibintas, 120 €, 5 nuotr. | `lighting-rear-lights-rear-light` | — |
| #812 | VW Golf VII 1.6 TDI mech. pavarų dėžė, 320 €, 10 nuotr. | `gearbox-...-manual-gearbox` | — |
| #813 | Audi A3 8V priekiniai stabdžių diskai, 65 €, 6 nuotr. | `brakes-brake-parts-brake-disc` | — |
| #814 | Honda Civic VIII priekinės kairės durys, 120 €, 6 nuotr. | `doors-door-parts-door-front-left` | ES |
| #815 | Audi R15 5x112 ET45 ratlankiai, 180 €, 5 nuotr. | `wheels-tyres-wheels-alloy-wheel` | AT |
