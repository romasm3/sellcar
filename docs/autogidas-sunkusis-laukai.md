# Autogidas — sunkiojo transporto struktūra (etalonas AutoLeft'ui)

Nuskaityta gyvai iš autogidas.lt 2026-09-07.
Naudojimas: tas pats principas kaip `docs/autogidas-laukai.md` — Claude Code
kopijuoja struktūrą 1:1, nekurdamas savo variantų.

---

## 1. Pagrindinė išvada

**Autogidas neturi „Vilkikas" tipo `Tipas` sąraše. Vilkikams `Tipas` laukas
apskritai NERODOMAS.**

Priežastis paprasta: `Tipas` aprašo **antstatą** — ką mašina veža (cisterna,
savivartis, furgonas). Vilkikas antstato neturi, jis tempia puspriekabę.
Todėl vilkikams tas laukas beprasmis ir jo tiesiog nėra.

AutoLeft dabar daro atvirkščiai: rodo vilkikui svetimą antstatų sąrašą, iš kurio
tenka rinktis „Kita".

---

## 2. Kategorijų medis

Sunkusis transportas Autogidas'e — **penkios atskiros lygiavertės kategorijos**,
ne viena su subkategorijomis:

| Kategorija | URL |
|---|---|
| Sunkvežimiai | `/skelbimai/sunkvezimiai/` |
| Vilkikai | `/skelbimai/vilkikai/` |
| Autotraukiniai, autovežiai | `/skelbimai/autotraukiniai-autoveziai/` |
| Autobusai | `/skelbimai/autobusai/` |
| Komunalinio ūkio transportas | `/skelbimai/komunalinio-ukio-transportas/` |

Kiekviena turi **savo laukų rinkinį**. Tai ne viena forma su filtru — tai
skirtingos formos.

AutoLeft pasirinkimo ekranas (`/create/?step=1&vt=trucks`) šias penkias
kategorijas jau rodo teisingai, bet visos penkios veda į tą pačią formą
`/create/trucks/`, o `?subcategory=` parametras niekur nenaudojamas ir
neišsaugomas.

---

## 3. VILKIKAI — laukų rinkinys

Filtrai (= laukai, kuriuos Autogidas laiko svarbiais):

| Laukas | Tipas | Reikšmės |
|---|---|---|
| Markė | select | markių sąrašas |
| Modelis | tekstas | laisvas |
| Kaina | nuo–iki | € |
| Metai | nuo–iki | 1925–2026 |
| **Ratų formulė** | select | 4x2, 4x4, 6x2, 6x2/4, 6x4, 6x4/2, 6x6, 8x2/4, 8x4, 8x6, 8x8, 10x4, 10x6, 10x8 |
| **Ašių skaičius** | select | 1 ašis, 2 ašys, 3 ašys, >3 ašių, Kitas |
| Rida | nuo–iki | km |
| **Euro standartas** | select | Euro 1…Euro 6, Kitas |
| **Galia, kW** | nuo–iki | rodoma „210 kW (282 AG)" formatu |
| **Daužtas** | select | Visi / Ne / Taip |
| **Miegamų vietų skaičius** | select | 1, 2, 3 |
| Pavarų dėžė | select | Semi-automatinė, Mechaninė, Automatinė |
| Būklė | select | Naudotas, Naujas |
| Šalis | select | Lietuva, Lenkija, Latvija, Estija, Airija… |
| Miestas | select | Vilnius, Kaunas, Klaipėda… |
| Skelbimo amžius | select | Vienos dienos, Trijų dienų, Savaitės… |
| Pardavėjo tipas | select | Privatus, Verslas |

**Tipo lauko NĖRA.**

Skelbimo puslapyje vilkikui rodoma:
`Markė · Modelis · Metai (YYYY-MM) · Daužtas · Euro standartas · Ratų formulė`

Antraštės formatas: `MAN Tgx 2012 m Vilkikas`
(markė + modelis + metai + „m" + kategorija)

---

## 4. SUNKVEŽIMIAI — laukų rinkinys

Skiriasi nuo vilkikų:

| Laukas | Yra vilkikuose? |
|---|---|
| **Tipas** (antstatas) | ❌ tik sunkvežimiuose |
| **Bendroji masė kg** (2800 / 3500 / 7500 / 12000 / 20000) | ❌ tik sunkvežimiuose |
| Pavarų dėžė | ✅ abiejose |
| Euro standartas | ✅ abiejose |
| Rida | ✅ abiejose |
| Ratų formulė | ✅ abiejose |
| Miegamų vietų skaičius | ✅ tik vilkikuose |
| Ašių skaičius | ✅ tik vilkikuose |

---

## 5. Ką keisti AutoLeft'e

1. `?subcategory=` turi būti **išsaugomas skelbime** ir rodomas skelbimo
   puslapyje bei kortelėje. Dabar dingsta.
2. Laukų rinkinys turi **priklausyti nuo subkategorijos**:
   - Vilkikai → BE `Tipas`; pridėti `Ašių skaičius` ir `Miegamų vietų skaičius`
     (AutoLeft turi `sleeping_seats`, bet neturi ašių skaičiaus)
   - Sunkvežimiai → su `Tipas` (dabartinis antstatų sąrašas) ir `Bendroji masė`
   - Autobusai / Komunalinis / Autotraukiniai → savi rinkiniai
3. Antraštė turi apimti kategoriją: `MAN 18.510 4x2 2022 m Vilkikas`,
   ne `MAN 18.510 4x2 LL SA (TGX GX) 2022`.
4. Pašalinti dubliuotą tuščią `— Pasirinkite —` (dabar 25 opcijos: 2 tuščios).
5. Backfill: #749, #754, #762 → subkategorija „Vilkikai", `Tipas` išvalyti.

---

## 6. Trūkstami laukai (yra Autogidas'e, nėra AutoLeft'e)

- **Ašių skaičius** (1 / 2 / 3 / >3 / Kitas) — vilkikams privalomas
- **Daužtas** (Taip / Ne) — AutoLeft turi `defects`, bet ne tą patį
- **Galia kW su AG konversija** rodoma pačiame filtre
- **Bendroji masė kg** kaip filtruojamas intervalas (2800/3500/7500/12000/20000)
