# Mobilus vaizdas — etalono specifikacija

Šaltinis: 10 tikrų telefono puslapių, išsaugotų iš Chrome (Android), `body class="is-mobile"`.
Ne ekrano nuotraukos, ne emuliacija — tikras serverio atiduotas HTML + CSS.

Autogidas mobilią versiją atiduoda **iš serverio** pagal User-Agent, ne per CSS lūžio taškus.
Todėl tai atskiras šablonas, o ne suspaustas darbalaukio tinklelis.

---

## 1. Greitoji paieškos panelė

### Struktūra

```html
<form action="/skelbimai/<kategorija>/" method="get" id="form-search" class="form-search-ads">
  <div class="search-form">
    <div class="selects-container" id="selects-container">

      <!-- laukas su drill-in -->
      <div class="select search-select-1">
        <div id="search-field-1"></div>      <!-- paslėpti input'ai -->
        <div id="search-field-14"></div>
        <a href="/select/?type=concatenation&step=1&group1=1&group2=14&section=01&return=<b64>">
          <div class="title">
            <span>Markė, modelis</span>
            <img src="/static/images/chevron-right.svg" class="arrow-right">
          </div>
        </a>
      </div>

      <!-- tekstinė paieška — NE drill-in, įprastas input vietoje -->
      <div class="select text search-select-inline search-select-376">
        <div class="input">
          <input class="form-control form-control-search" type="text" placeholder="Ieškoti" name="f_376">
        </div>
      </div>

      <!-- žymimieji langeliai -->
      <div class="checkboxes-container quick-search-addons">
        <div class="checkbox-container">
          <input id="ac_4" class="checkbox" name="ac_4" type="checkbox" value="1">
          <label class="checkbox-label" for="ac_4">Tik Lietuvoje</label>
        </div>
        <div class="checkbox-container">
          <input id="ac_3" class="checkbox" name="ac_3" type="checkbox" value="1">
          <label class="checkbox-label" for="ac_3">Skelbimas su VIN</label>
        </div>
      </div>
    </div>

    <!-- lipnus apačios blokas -->
    <div class="form-bottom-sticky" id="btnSticky">
      <div class="buttons-container">
        <div class="form-bottom-containter">
          <a href="/paieska/<kategorija>/?#selects-target" class="detail-search btn-info is-full">
            <svg>#filter</svg> Detali paieška
          </a>
          <button class="search-button btn-brand-primary is-full" type="submit">
            <svg>#search</svg> Pasiūlymai <span id="count" class="js-animate-count">28622</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</form>
```

### Matmenys (iš CSS)

| Elementas | Reikšmė |
|---|---|
| `.select` | `font-size: 17px; position: relative; overflow: hidden` |
| `.select .title` | `padding: 16px 24px; width: 100%; text-align: left; color: #000` |
| `.select .title span` | `line-height: 16px; display: inline-block; vertical-align: middle` |
| `.arrow-right` | `position: absolute; right: 8%; top: 50%; transform: translateY(-50%); width: 8px; height: 14px` |
| `.selects-container` | `padding-top: 4px; background: #fff; border-left/right: 1px solid #e7e7e7` |
| `.select.text` | be rodyklės (`.arrow { display: none }`), `padding-top: 1px` |
| `.selects-container .select .input` | `padding: 24px 16px` |
| `.checkboxes-container` | `display: flex; flex-direction: column; padding: 0 16px 24px; gap: 12px` |
| `.form-bottom-sticky .buttons-container` | `background: #fff; border: 0 1px 1px solid #e7e7e7; padding: 0 12px 12px` |
| `.form-bottom-containter` | `display: flex; flex-direction: column-reverse; align-items: center; gap: 8px; width: 100%` |
| `.btn-brand-primary.is-full` | `width: 100%` |
| `.detail-search` | `color: #686868; font-weight: 500; text-decoration: none` |

**Svarbu:** apačios blokas telefone yra `column-reverse` — mygtukas „Pasiūlymai N" **viršuje**, „Detali paieška" **po juo**. Abu per visą plotį.

### Drill-in — atskiras puslapis, ne sluoksnis

Kiekviena eilutė yra `<a href>` į `/select/` su parametrais:

| `type=` | Ką reiškia | Pavyzdys |
|---|---|---|
| `concatenation` | susietas markė+modelis, žingsniai | `?type=concatenation&step=1&group1=1&group2=14` |
| `ddvaluedouble` | diapazonas Nuo–Iki | `?type=ddvaluedouble&group1=41&group2=42` (Metai) |
| `multiple` | kelių reikšmių pasirinkimas | `?type=multiple&group=2` (Kuro tipas) |
| `checkbox` | vienas žymimasis langelis | `?type=checkbox&group=453` |

`return=` — base64 užkoduotas grįžimo kelias su parametrais.
Tai svarbu: **naršyklės „atgal" mygtukas veikia natūraliai**, nes tai tikras puslapis su savo URL.

### Sąlyginiai laukai

Nereikšmingi kategorijai laukai lieka HTML'e su `style="display: none;"` ir įjungiami JS'u.
Pvz. automobiliams „Rida su vienu įkrovimu, km", „Baterijos talpa, kWh", „Yra greitojo įkrovimo jungtis"
rodomi tik pasirinkus elektrą.

---

## 2. Detali paieška telefone

**Tas pats principas** — 28 `.select` eilutės su `/select/` nuorodomis, ta pati forma
`action="/skelbimai/automobiliai/"`, ta pati tekstinė paieška inline.
Skiriasi tik laukų kiekis. Jokio tinklelio, jokių dropdown'ų.

---

## 3. Rezultatų puslapis

### Viršus

```
[‹ atgal] [logotipas] [+ Įkelti] [žymos +N] [☰]
🏠 › Skelbimai › Automobiliai
<h1> SEO antraštė, nukirpta „…"          [filtrų ikona]
2 eilutės aprašymo + „Skaityti daugiau"
[Volkswagen] [BMW] [Audi] [Mercedes-Ben…]   ← horizontaliai slenkamos markių nuorodos
```

Markių juosta — tai `<a href="/skelbimai/automobiliai/<marke>/">` nuorodos, ne filtrai.

### Pranešimų juosta

```html
<div class="items-notifications-header">
  <div class="notifications-label icon ico-bell">Nepraleiskite naujų skelbimų</div>
  <button class="toggle-push-notifications"><span>Gauti ekrane</span></button>
  <button class="btn-subscribe-email-notifications"><span>Gauti el. paštu</span></button>
</div>
```

### Rezultatų antraštė

```html
<div class="items-header">
  <div class="filter-count"><div class="ads-count">Rasta: <span>28617</span></div></div>
  <div class="filter-controls">
    <div class="list-type js-listing-type">
      <span class="icon ico-list-thumb active" data-type="thumb"></span>
      <span class="icon ico-list-line" data-type="line"></span>
    </div>
    <div class="sorting">
      <div class="current-option icon ico-up-arrow"><span>Nauji ir atnaujinti</span></div>
      <select id="sorting-select">
        <option>Nauji ir atnaujinti viršuje</option>
        <option>Pigiausi viršuje</option>
        <option>Brangiausi viršuje</option>
      </select>
    </div>
  </div>
</div>
```

### Skelbimo kortelė

```html
<article class="list-item" id="ann_NNN">
  <a class="item-link">
    <div class="item-description">
      <div class="image has-thumbs">
        <div class="image-wrapper">
          <div class="badge" data-badge="Prieš 7 val."></div>
          <div class="badge viewed-badge" data-badge="Žiūrėjote"></div>
          <div class="badge vin-badge"></div>
          <picture>
            <source media="(max-width:668px)" srcset="…4_15_…">   <!-- mobili nuotrauka -->
            <source media="(min-width:669px)" srcset="…4_16_…">
            <img src="…">
          </picture>
        </div>
        <div class="thumbs js-images">
          <img width="88" height="66" …>   ← 3 miniatiūros
        </div>
      </div>
      <div class="content">
        <h2 class="title"><span class="icon item-level">12</span> Volvo XC90</h2>
        <div class="params param-icon params-grid">
          <div class="icon param-year">    <svg>#icon-param-year</svg>    <div><i>Metai</i><b>2003-01</b></div></div>
          <div class="icon param-fuel-type"><svg>…</svg><div><i>Kuro tipas</i><b>Benzinas/Dujos</b></div></div>
          <div class="icon param-mileage"> <svg>…</svg><div><i>Rida</i><b>247 100 km</b></div></div>
          <div class="icon param-gearbox"> <svg>…</svg><div><i>Pavarų dėžė</i><b>Automatinė</b></div></div>
          <div class="icon param-engine">  <svg>…</svg><div><i>Variklis</i><b>2.5 L, 154 kW</b></div></div>
          <div class="icon param-location"><svg>…</svg><div><i>Miestas</i><b>Radviliškis, Lietuva</b></div></div>
        </div>
      </div>
    </div>
    <div class="seller-item">…Pardavėjas, logotipas, „Visi pardavėjo skelbimai"…</div>
    <div class="item-footer">
      <div class="price-item">
        <div class="price">1 650 €</div>
        <div class="gf-monthly-link"><span class="financing-price">27 €/mėn.</span></div>
      </div>
      <div class="item-action">[dalintis] [įsiminti]</div>
    </div>
  </a>
</article>
```

**Parametrų tinklelis:**
```css
.params-grid.params { display: flex; flex-wrap: wrap; gap: 8px; font-size: 14px; color: #000 }
.params-grid.params .icon { display: flex; align-items: center; gap: 8px; width: calc(33.3333% - 10.6667px) }
```
Telefone — **trys stulpeliai**, ne du. Kiekvienas elementas: ikona 24×24, po jos
`<i>` etiketė ir `<b>` reikšmė vienas po kitu.

**Nuotraukos:** atskiras `srcset` mobiliam (`max-width: 668px`) ir darbalaukiui — mažesnis
failas telefone. Miniatiūros fiksuoto dydžio 88×66.

---

## 4. Hamburger meniu (☰)

Neprisijungusiam:
```
[logotipas]                              [×]
[+ Įkelti skelbimą]        ← tamsiai mėlynas, per visą plotį
[Registruotis | Prisijungti] ← baltas su rėmeliu
♡ Įsiminti skelbimai (0)
🔖 Mano paieškos (0)
👁 Žiūrėti skelbimai
PRO pardavimas  [NAUJA]
Finansavimas / Pasiūlymai verslui / Naujienos / Auto katalogas
[LT] RU EN
```

Prisijungusiam papildomai: avataras + el. paštas viršuje, „Mano Autogidas" antraštė,
Mano skelbimai (N), Žinutės, Piniginė, Nustatymai, App Store / Google Play mygtukai, Atsijungti.

---

## 5. Ką tai reiškia mums

| Klausimas | Etalonas | Ką darom |
|---|---|---|
| Kaip pasiekiamas mobilus vaizdas | Serveris pagal User-Agent | Nuspręsti: serverio šablonas ar CSS lūžio taškas |
| Drill-in | Atskiras puslapis `/select/` su savo URL | Atskiras URL — kad „atgal" veiktų |
| Laukų sąrašas | Tas pats kaip darbalaukyje | Ta pati konfigūracija, kitas šablonas |
| Tekstinė paieška | Inline, ne drill-in | Taip pat |
| Žymimieji langeliai | Atskirai, po laukais | Taip pat |
| Mygtukas | Viršuje, per visą plotį, su skaičiumi | Taip pat („Skelbimai N") |
| „Detali paieška" | Po mygtuku, per visą plotį | Taip pat |
| Kortelės parametrai | 3 stulpeliai, ikona + etiketė + reikšmė | Taip pat |
| Nuotraukos | Atskiras srcset telefonui | Įsivesti |


---

## 7. Taisyklė: mobiliame vaizde nėra horizontalaus slinkimo

Viskas telpa į ekrano plotį. Jokių slenkamų juostų, nukirptų elementų ar
pastumtų sričių. Netelpa — mažinam, laužom į eilutes arba slepiam po
mygtuku, bet nestumiam į šoną.

Patikrinimas prie 360, 390 ir 768 px:

```javascript
document.documentElement.scrollWidth === document.documentElement.clientWidth
```

Ir abiejų pusių patikra — `scrollWidth` kairėn išsikišusio turinio nemato:

```javascript
[...document.querySelectorAll('*')].filter(e => { const r = e.getBoundingClientRect();
  return r.left < -1 || r.right > window.innerWidth + 1; })
```

Tai galioja ir etalonui: jų mobiliame puslapyje `scrollWidth` visada lygus
`innerWidth`. Vienintelė slenkama sritis pas juos — markių nuorodų juosta
rezultatų puslapyje, ir ji yra turinys, ne valdymas.

### Išimtis: sąmoninga karuselė

Taisyklė kalba apie IŠDĖSTYMĄ — kai elementas netyčia išlipa už ekrano.
Sąmoningai slenkama juosta (kortelių karuselė, kaip etalono „Mano
paieškos" ir „Populiarios paieškos") yra išimtis, jei tenkina tris
sąlygas:

1. slinkimas vyksta juostos konteineryje (`overflow-x: auto`), o puslapio
   `scrollWidth` lieka lygus `innerWidth`;
2. `scroll-snap-type: x mandatory` — kortelė sustoja vietoje, ne pusiau;
3. rodyklės rodomos tik kai yra ką slinkti, o telefone jų nėra — stumiama
   pirštu.

Pas mus taip veikia tik skirtukų pavadinimų juosta (`.home-tabs-header`
šablone `listings/listing_list.html`): telefone ji lieka vienoje eilutėje
ir stumiama pirštu, o paspaustas skirtukas prisitraukia į vidurį
(`scrollIntoView({ inline: 'center' })`). SKELBIMŲ kortelės NIEKUR
neslankioja į šoną — jos dedamos į tinklelį ir keliauja žemyn
(vartotojo sprendimas 2026-08-20).

**Pavyzdys (2026-08-20).** Antraštės dešinė pusė buvo 340 px ir plėtė visą
puslapį iki 396 px. Atrodė kaip trys atskiros klaidos — „slenkanti" ikonų
juosta, nukirptas kategorijų pikeris ir nematomas rūšiavimas — bet
priežastis buvo viena. Sutvarkyta paslepiant telefone tai, kas etalone
irgi paslėpta: kalbų jungiklį, paieškos ir žinučių ikonas.

---

## 6. Žinomi defektai

| Defektas | Kur | Būsena |
|---|---|---|
| Skelbimo kortelė telefone išsikiša už ekrano — 465 px vietoj 390 (`.ap-price` ir kainos elementai) | rezultatų puslapis, visos kategorijos | Taisoma kartu su rezultatų puslapiu ir `mobile_results_header` bloku po kaskados |


---

## 8. Vary: User-Agent ir CDN (2026-08-21)

Rezultatų puslapis (`listing_list`) serveryje sprendžia, ar renderinti
šoninę filtrų juostą (`context_processors.device_kind`), todėl atsakymas
siunčiamas su `Vary: User-Agent`.

Šiandien tai nekenkia: prieš Django nėra jokio bendro kešo — nginx
`proxy_cache` nekonfigūruotas, CDN nėra, HTML neturi `Cache-Control:
public`.

**Kai dėsim Cloudflare:** CF `Vary` ignoruoja (išskyrus `Accept-Encoding`),
todėl įjungus HTML kešavimą telefonas gali gauti darbalaukio variantą su
juosta. Tam maršrutui reikės **Cache Level: bypass** (arba Cache Rule,
kuri HTML nekešuoja). Alternatyva — grįžti prie CSS sprendimo ir atsisakyti
serverio šakos.
