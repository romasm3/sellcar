# AutoLeft — klaidos: MOTOCIKLŲ PADANGOS

Atskiro kūrimo kelio **nėra**. Motociklų padangos dedamos per tą pačią
`/create/tyres/` formą, pasirinkus „Paskirtis = Motociklai" (`purpose=moto`).
Katalogas: `/browse/tyres/?purpose=moto`.

Testinis skelbimas: `/wheels/30/` — Michelin Pilot Power 3, FR, 260 €, 2 vnt.

Etalonas — **autogidas.lt**. Valiuta — tik EUR. Dizaino nekeisti.

---

## PAVELDIMOS KLAIDOS

Viskas iš `PADANGOS.md` galioja ir čia. Svarbiausios:

| Kodas | Trumpai |
|---|---|
| `TYRE-01` | Formos pateikti neįmanoma (`id_contact_phone` vs `id_phone`) |
| `TYRE-02` | Validacijos pranešimai rodo ne tą lauką |
| `TYRE-05` | Skelbime „Sezoniškumas: summer" |
| `TYRE-06` | „Specifications", „Remaining", „Production year" neišversti |
| `TYRE-08` | „Nerasta jokių skelbimų 1" virš matomos kortelės |
| `TYRE-09` | Kortelėje „Redaguoti profilį 50" |

---

## SAVOS KLAIDOS — moto dydžiai neįvedami

| Kodas | Problema | Būsena |
|---|---|---|
| `MTYRE-01` | **Motociklų pločių sąraše nėra.** Plotis prasideda nuo **125** ir eina žingsniu 10 iki 355 — tai lengvųjų automobilių eilė. Motociklams reikia **90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 240**. Būtent **120** (priekinė, 120/70 ZR17) ir **180/190/200** (galinė) — dažniausi dydžiai pasaulyje — sąraše jų nėra. Rezultatas: nė vieno tikro moto skelbimo įvesti negalima; testiniame #30 teko rašyti 185/50 vietoj 120/70 ir 180/55. | NAUJA |
| `MTYRE-02` | **Profilio sąraše nėra moto reikšmių.** Yra `20–85` žingsniu 5; motociklams reikia dar **90, 95, 100** (pvz. 110/90-19, 130/90-16 — enduro ir čioperiams). | NAUJA |
| `MTYRE-03` | **Nėra colinių / senų žymėjimų.** Moto naudoja ir `3.00-18`, `4.10-18`, `MT90-16`. Dabartinė forma priima tik `plotis/profilis Rskersmuo`. | NAUJA |
| `MTYRE-04` | **Skersmenų sąraše nėra R23 ir mažesnių moto dydžių** — yra R10–R24, tad čia daugmaž tvarkoje, bet trūksta **R16.5** ir colinių `21"` priekinių enduro padangų žymėjimo. Žemas prioritetas. | NAUJA |

---

## SAVOS KLAIDOS — trūksta moto laukų

| Kodas | Ko trūksta | Būsena |
|---|---|---|
| `MTYRE-05` | **Priekinė / galinė.** Moto padanga visada yra arba priekinė, arba galinė — tai svarbiausias moto padangos požymis. Formoje tokio lauko nėra. Vienintelis apėjimas — varnelė „Parduodama po vieną". Reikia `moto_position`: Priekinė / Galinė / Pora. | NAUJA |
| `MTYRE-06` | **Padangos tipas.** Nėra: Sportinė / Turistinė / Enduro / Cross / Čioperiams / Skuteriams / Žieminė dygliuota moto. Yra tik bendra varnelė „Sportinės padangos", skirta automobiliams. Autogidas moto padangas skirsto. | NAUJA |
| `MTYRE-07` | **Su kamera / be kameros (tube / tubeless).** Moto padangoms privalomas skirtumas, formoje nėra. | NAUJA |
| `MTYRE-08` | **Greičio ir apkrovos indeksas moto formatu.** Moto rašoma `58W`, `73W`, `M/C`. Apkrovos laukas — laisvas tekstas be patikros (`TYRE-14`), greičio sąrašas — automobilių. Trūksta `M/C` žymos. | NAUJA |
| `MTYRE-09` | **Filtre „Motociklams" nėra nė vieno moto specifinio filtro** — tik tie patys plotis / profilis / skersmuo / sezoniškumas kaip automobiliams. Pasirinkus „Motociklams" filtrų rinkinys turėtų persijungti. | NAUJA |

---

## SIŪLOMA EILĖ

1. Kartu su `TYRE-01` (bendras blokatorius)
2. `MTYRE-01` + `MTYRE-02` — be pločių kategorija neturi prasmės
3. `MTYRE-05` — priekinė / galinė
4. `MTYRE-07`, `MTYRE-06` — tipas ir kamera
5. `MTYRE-09` — filtrų persijungimas
6. `MTYRE-03`, `MTYRE-04`, `MTYRE-08` — smulkmenos
