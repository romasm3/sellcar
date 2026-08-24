# AutoLeft dizaino sistema

Visos reikšmės išmatuotos iš etalono CSS (autogidas.lt, tikras telefono ir
darbalaukio snapshot'as). Spalvos — mūsų, struktūra — etalono.

**Pagrindinė taisyklė:** šablonuose nerašoma nė vienos konkrečios reikšmės.
Viskas ateina iš kintamųjų, apibrėžtų `base.html` `:root` bloke.

---

## 1. Tarpų skalė

Tik šie dydžiai. Kitokių nebūna.

```
--sp-1:  4px    smulkūs tarpai ikonos ir teksto viduje
--sp-2:  8px    tarp susijusių elementų
--sp-3: 12px    tarp laukų eilučių (vertikaliai)
--sp-4: 16px    vidinės kortelių paraštės
--sp-6: 24px    tarp laukų stulpelių (horizontaliai), sekcijų vidus
--sp-8: 32px    tarp blokų
--sp-10: 40px   tarp sekcijų
--sp-16: 64px   tarp didelių puslapio dalių
```

Etalone naudojami dažniausiai: 16 (73×), 8 (71×), 24 (41×), 4 (36×), 32 (12×), 12 (11×).

**Laukų tinklelis:** `gap-y: 12px`, `gap-x: 24px`. Visur, be išimčių.

---

## 2. Tipografijos skalė

Tik šie dydžiai:

```
--fs-xs:  12px   žymos, skaitikliai, smulkus tekstas
--fs-sm:  14px   parametrai kortelėse, pagalbinis tekstas
--fs-base:16px   pagrindinis tekstas, laukai, mygtukai
--fs-md:  17px   mobilių eilučių sąrašas (tik ten)
--fs-lg:  18px   dideli mygtukai
--fs-xl:  20px   sekcijų antraštės
--fs-2xl: 24px   puslapio antraštė
```

Svoriai — tik keturi:

```
--fw-normal:   400   įprastas tekstas
--fw-medium:   500   nuorodos, žymos, antraštės laukams
--fw-semibold: 600   mygtukai, kortelių pavadinimai
--fw-bold:     700   puslapio antraštės, kainos
```

Etalone: 500 (110×), 600 (72×), 400 (73×), 700 (54×). Daugiau nereikia.

---

## 3. Apvalinimas

```
--r-sm:   4px    smulkūs elementai
--r-md:   8px    laukai, mygtukai, kortelės — NUMATYTASIS
--r-lg:  16px    dideli blokai, moduliniai langai
--r-pill: 999px  žymos su ×, skaitikliai
--r-full: 50%    apskritos ikonos, avatarai
```

Etalone 8 px naudojamas 123 kartus — tai numatytoji reikšmė. Jei abejoji, imk 8.

---

## 4. Laukai

Visi įvesties laukai vienodi:

```
aukštis        40px          (etalone 86 taisyklės su height: 40px)
apvalinimas    8px
rėmelis        1px solid var(--border)
fonas          #FFFFFF
vidinė paraštė 0 12px
line-height    38px
perėjimas      border-color .2s
```

Būsenos:

```
:hover              border-color: var(--border-hover)
:focus              border-color: var(--accent), be outline
:disabled           cursor: not-allowed, fonas var(--surface-muted)
.input-error        border-color: var(--danger)
```

Etiketė virš lauko: `--fs-sm`, `--fw-medium`, tarpas iki lauko 4 px.

---

## 5. Mygtukai — trys tipai, ne daugiau

```
aukštis        48px  (mobilus ir darbalaukis vienodai)
mažas          34px  (antraštės mygtukai)
apvalinimas    8px
šriftas        16px / 600
paraštės       6px 16px
tarpas ikona↔tekstas  8px
perėjimas      .2s
```

**Pirminis** (`.btn-primary`) — vienas ekrane. Užpildytas akcento spalva, baltas tekstas.
**Antrinis** (`.btn-outlined`) — baltas fonas, 1 px akcento rėmelis, akcento tekstas.
**Tekstinis** (`.btn-text`) — be fono ir rėmelio, pilkas tekstas, hover — juodas.

Modifikatoriai: `.is-full` (100 % plotis), `.is-big` (46 px, 18 px šriftas).

---

## 6. Spalvos ir jų vaidmenys

Kiekviena spalva turi **vieną** vaidmenį. Jei nežinai, kurį imti — imk pilką.

```
--accent           pagrindinis veiksmas ekrane. TIK VIENAS per ekraną.
--accent-hover     jo hover būsena
--accent-soft      jo švelnus fonas (žymos, pasirinktos eilutės)

--text             #111827   pagrindinis tekstas
--text-muted       #6B7280   antrinis tekstas, etiketės
--text-disabled    #9CA3AF

--border           #E7E7E7   laukų ir kortelių rėmeliai
--border-hover     #B0B0B0

--surface          #FFFFFF   kortelės, panelės
--surface-muted    #F9FAFB   puslapio fonas

--success          #067647   ant fono #ECFDF3, rėmelis #ABEFC6
--danger           #FF5151   klaidos, trynimas
```

### Hierarchijos taisyklė

**Viename ekrane — vienas akcento spalvos elementas.**

Dabar pas mus vienu metu konkuruoja penki: raudonas „Sukurti skelbimą",
pilkas „Skelbimai", žalias skaitiklis, oranžinė aktyvi ikona, mėlynas „Įkelti".

Sutvarkyti taip:

| Ekranas | Pagrindinis veiksmas (akcentas) | Visa kita |
|---|---|---|
| Pagrindinis | „Skelbimai N" paieškos panelėje | „Sukurti skelbimą" — antrinis |
| Rezultatai | — (nėra) | „Sukurti skelbimą" — antrinis |
| Detali paieška | „Ieškoti N" | „Išvalyti" — tekstinis |
| Skelbimo kūrimas | „Publikuoti" | „Išsaugoti juodraštį" — antrinis |
| Skelbimo puslapis | „Rašyti pardavėjui" | „Skambinti" — antrinis |

Skaitikliai antraštėje — ne akcentas. Jie informaciniai: `--fs-xs`, žyma su
`--success` fonu, ne ryški spalva.

Aktyvi kategorijos ikona — akcento spalvos pabraukimas, bet ne užpildyta ikona.

### Prekės ženklo spalva — oranžinė #E8703A

```
--brand-ink   #1A1A1A   logotipo užrašas „Autoleft"
--brand-dot   #E8703A   TIK taškas logotipe ir ikonoje
--brand-font  "EB Garamond", Georgia, "Times New Roman", serif
```

**Oranžinė naudojama tik dviejose vietose: logotipo taške ir programėlės
ikonoje. Daugiau niekur svetainėje jos nėra** — nei mygtukuose, nei žymose,
nei aktyviose būsenose. Akcentas lieka antracitas (`--accent`).

Kodėl taip: viena reta spalva atsimenama geriau nei visur išbarstyta. Kai
oranžinė yra vieninteliame taške, ji tampa ženklu — akis ją suranda iškart
ir susieja su preke. Kai ta pati oranžinė yra ir mygtuke, ir žymoje, ir
kortelės fone, ji nustoja ką nors reikšti ir tampa dar viena spalva triukšme.
Tas pats principas kaip su akcentu: vienas elementas ekrane, ne penki.

Patikra (turi grąžinti tuščią sąrašą — logotipo taškas neskaičiuojamas):

```javascript
[...document.querySelectorAll('body *')]
  .filter(e => !e.classList.contains('logo-dot'))
  .filter(e => { const cs = getComputedStyle(e);
                 return /232,\s*112,\s*58/.test(cs.color + cs.backgroundColor + cs.borderColor); });
```

Logotipo dydis: 32 px darbalaukyje, 24 px telefone. Ant tamsaus fono užrašas
tampa `#F2F0ED`, taškas lieka oranžinis (`.logo-sviesus`).

---

## 7. Kortelės

```
fonas          var(--surface)
apvalinimas    8px
rėmelis        1px solid var(--border)
vidus          16px
šešėlis        nėra (etalone kortelės be šešėlio)
hover          box-shadow: 0 0 8px rgba(0,0,0,.2)
```

---

## 8. Žymos ir skaitikliai

```
apvalinimas    12px
šriftas        12px / 500
paraštės       2px 8px
line-height    1.5
```

Žalia žyma: tekstas `--success`, fonas `#ECFDF3`, rėmelis `#ABEFC6`.

---

## 9. Nuorodos

```
įprasta        var(--text), be pabraukimo
hover          var(--accent) + pabraukimas
```

---

## 10. Perėjimai

Visur `.2s`. Kitokių trukmių nebūna. Animuojami tik `color`, `background-color`,
`border-color`, `opacity`, `transform` — niekada `height`, `width` ar `top`.

---

## Patikrinimas

Po bet kokio išdėstymo darbo paleisti:

```js
// 1. Ar nėra reikšmių už skalės ribų
[...document.querySelectorAll('*')].map(e => getComputedStyle(e))
  .filter(s => s.fontSize && ![12,14,16,17,18,20,24].includes(parseFloat(s.fontSize)))
  .length   // turi būti 0 (be paveldėtų)

// 2. Ar visi laukai 40 px
[...document.querySelectorAll('input,select,.sp-fld')]
  .filter(e => Math.round(e.getBoundingClientRect().height) !== 40)
  // turi būti tuščias

// 3. Kiek akcento spalvos elementų ekrane
[...document.querySelectorAll('*')]
  .filter(e => getComputedStyle(e).backgroundColor === 'rgb(<accent>)')
  .length   // turi būti 1
```
