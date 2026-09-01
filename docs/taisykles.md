# Nuolatinės taisyklės

Galioja **visiems paieškos paviršiams ir visiems būsimiems darbams**.
Kiekvienas naujas filtras, kortelė ar puslapis tikrinamas pagal šitą
sąrašą **prieš atiduodant darbą** — ne po to.

Trumpinys skiltyje „Patikra" prie kiekvienos taisyklės sako, kaip
įsitikinti, kad ji laikoma; ten, kur būklė šiandien dar neatitinka,
parašyta atvirai.

---

## 1. VIETA YRA SVARBIAUSIAS FILTRAS

Vieta **pirma ir visada matoma** kiekviename filtrų paviršiuje:

| Paviršius | Kur |
|---|---|
| Greitoji paieškos panelė | pirmoji eilutė |
| Šoninė juosta rezultatuose | pirmoji eilutė |
| Išplėstinė paieška | pirmoji eilutė |
| Mobilus rodinys | pirmoji eilutė |

**Tvarka visada: šalis → miestas → spindulys.**

Niekada neslepiama po „Daugiau filtrų". Niekada nenustumiama žemiau
markės ar kainos.

**Patikra:** atidaryk kiekvieną paviršių ir pažiūrėk, kas yra pirmas
laukas. Jei ne šalis — taisyklė laužoma.

**Būklė 2026-09-01:** padaryta tik dalis — virš greitosios panelės yra
šalies juosta (`templates/partials/_salis.html`). Pačių panelių
konfigūracijoje vieta tebėra apačioje arba jos nėra visai:
`cars` — `brand, model, year, price, fuel_type, body_type, __text__,
country` (vieta 8-a); `motorcycles` — vietos lauko nėra.
Sutvarkyti reikia `paneles-config.json` ir `isplestine-config.json`
laukų tvarką.

---

## 2. KORTELĖ rodo tik tai, ko reikia apsispręsti

Kortelė sąraše atsako į vienintelį klausimą: **verta atidaryti ar ne.**

Rodoma:
- nuotrauka
- pavadinimas
- metai
- kaina
- pagrindiniai **trys** parametrai
- **vieta**

**Nerodoma:** komplektacija, įranga, VIN, aprašymas, istorija. Visa
techninė informacija — tik skelbimo viduje.

**Patikra:** suskaičiuok kortelės elementus. Jei ten yra kas nors, ko
nereikia sprendimui „atidaryti / neatidaryti" — išimk.

---

## 3. SKELBIMO PUSLAPYJE kontaktų blokas yra pagrindinis elementas

Ne priedas šone. Jame **visada**:

- pardavėjo tipas
- telefonas
- žinutė
- **tiksli vieta** — miestas, adresas (jei nurodytas), žemėlapis su
  žymekliu ir „Kaip nuvažiuoti"

Klientas turi iškart matyti, **kur važiuoti apžiūrėti automobilio**.
Blokas matomas be slinkimo iki galo.

**Patikra:** atidaryk skelbimą 390 px pločio ekrane. Jei kontaktams
rasti reikia slinkti žemiau pusės puslapio — taisyklė laužoma.

---

## 4. Kontaktai — viena dalis visai svetainei

Visi kontaktai eina per `templates/listings/partials/contact_block.html`.
Jokių kopijų kituose šablonuose. Kategorijų skirtumai — per include
parametrus (`show_postal`, `phone_name`, `css_style`…), niekada ne antra
kopija. Pridedant ar išimant kontaktų lauką redaguojamas tas vienas
failas.

Šalių ir valstijų sąrašai — iš `contact_block_tags`. `country_choices` iš
view'o **neperduodamas** (keli view'ai netyčia buvo susiaurinę jį iki JAV).

**Patikra:** `grep -rl "contact_block.html" templates/ | wc -l` prieš
`grep -rn "name=\"phone\"" templates/ | wc -l` — antras skaičius neturi
būti didesnis.

---

## 5. ŠALIES VĖLIAVĖLĖ prie vietos

> Papildyta 2026-09-01. Ankstesnė redakcija sakė rodyti vėliavą tik tada,
> kai skelbimo šalis skiriasi nuo pasirinktos paieškoje. Dabar galioja
> platesnė taisyklė: vėliavėlė rodoma **visur, kur rodoma vieta**.

**Šaltinis — kontaktų blokas.** Vieta, kurią pardavėjas nurodė
įkeldamas skelbimą (šalis → miestas), yra **vienintelis** šaltinis.
Jokio spėliojimo pagal pardavėjo paskyrą ar IP.

**Kur dedama** — visur, kur rodoma skelbimo vieta:

1. kontaktų bloke skelbimo puslapyje
2. skelbimo kortelėje sąraše, vietos eilutėje
3. žemėlapio žymeklio burbule
4. išsaugotose paieškose ir peržiūrėtuose skelbimuose
5. šalies sąrašuose — juostoje virš panelės ir šoninėje juostoje

**Formatas visur vienodas — vėliava IŠKART PO šalies pavadinimo:**

    📍 Kaunas, Lithuania [vėliava]

Ne prieš, ne eilutės gale. Sąrašo eilutėje ji taip pat prilimpa prie
pavadinimo, o skaičius nustumiamas į dešinį kraštą:

    ○ Lithuania [vėliava]            4 821
    ● Visos šalys [gaublys]         48 320

Radus seną variantą — taisyti.

**Eilutė nesilaužo.** `display:flex; align-items:center; gap:6px;
flex-wrap:nowrap`; tekstui `overflow:hidden; text-overflow:ellipsis;
white-space:nowrap`; vėliavai `flex:0 0 auto`. Ilga vieta
(„Nordrhein-Westfalen, Germany") trumpinama daugtaškiu, bet vėliava
NIEKADA nenukrenta į antrą eilutę.

Šalies pavadinimas **pilnas** — ne kodas „LT" ar „DE".

> **Kur angliškas, kur išverstas.** Kortelės vietos eilutėje (ir
> darbalaukyje, ir telefono „Miestas" langelyje) bei šalies sąrašuose
> (juostoje, šoninėje juostoje) vardas **angliškas ir neverčiamas**
> (`salys.VARDAI_EN`, filtras `|salies_vardas_en`) — tai tarptautinis
> sąrašas, jį skaito ir tas, kuris svetainės kalbos nemoka. Kontaktų
> bloke skelbimo puslapyje vardas lieka **išverstas** (`salys.vardas`) —
> ten tekstas skirtas žmogui, skaitančiam skelbimą savo kalba.

**Vienoje kortelėje vieta rodoma VIENĄ kartą.** Darbalaukyje — žalia
eilutė po parametrais (`.kv-zalia`); telefone ji paslėpta, o vietą rodo
„Miestas" langelis parametrų tinklelyje (`docs/mobilus-etalonas.md`,
`.param-location`). Dvi vietos toje pačioje kortelėje — klaida.

> Nepainioti su šalies juosta virš paieškos panelės: ten sąrašas
> tarptautinis, todėl vardai **angliški ir neverčiami**
> (`salys.VARDAI_EN`). Vietos eilutėje — išversti (`salys.vardas`).

**Techniškai:**

- **SVG**, ne emoji: `static/flags/<kodas>.svg`. Windows vėliavų emoji
  neturi ir vietoj jų rodo dvi raides kvadratėliuose.
- 16×12 px, vertikaliai centruota su tekstu, tarpas 6 px,
  `border-radius: 2px`, `1px rgba(0,0,0,.08)` rėmelis — kad baltos
  vėliavos (JP, PL) nesusilietų su fonu.
- `alt` ir `title` — pilnas šalies pavadinimas.
- **Viena šablono dalis** `templates/partials/_veliava.html`, naudojama
  visur. Jokių kopijų.
- **Kortelės vietos eilutė** — irgi viena dalis:
  `templates/listings/partials/_kort_vieta.html` (smeigtukas, tekstas,
  vėliava). Kortelėse jos HTML nekopijuojam.
- Rėmelis daromas `outline: 1px solid rgba(0,0,0,.10); outline-offset:
  -1px` — border'as 16×12 vėliavą paverstų 18×14, o `box-shadow … inset`
  ant `<img>` nesimato (etalone vėliava yra `<svg>`).
- Vėliavų rinkinys — **visos** šalys iš `salys.py`. Vienas šaltinis, ne
  po failą kaskart.

**Statiniai — visada per `{% static %}`, kelias vienoje žymėje.** Vardai
turi turinio maišą (`ManifestStaticFilesStorage`), todėl pakeitus failą
pasikeičia vardas ir naršyklė gauna naują pati. Ranka rašytas
„/static/…" maišo negauna ir lieka kaboti naršyklės keše; sulipdytas
`{% static 'a/' %}{{ b }}` iš viso lūžta, nes katalogo manifeste nėra.
Išimtis — laiškai: ten adresas absoliutus (`{{ site_url }}/static/…`) ir
nesumaišytas, nes laiškas gyvena ilgiau nei maišas.

> **Vizualinis darbas tikrinamas GYVOJE svetainėje.** Nuotrauka iš
> 127.0.0.1 talpyklos klaidų nepagauna iš principo — ten nėra nei nginx,
> nei seno failo naršyklės keše. Patikra: `docs/statiniu_kesas_test.py`,
> nginx taisyklės — `deploy/nginx-statiniai.conf`.

**Inline SVG — visada su `width` ir `height` žymėje**, ne tik CSS
(`<svg class="pin" width="11" height="11" viewBox="0 0 24 24">`). Be jų
jis išsitempia iki 100 % konteinerio ten, kur stiliai nepasiekia:
pasenęs naršyklės kešas, kitas puslapis, laiškas. Bendro elemento
stilius gyvena bendrame `static/css` faile, ne šablono `<style>` bloke.
Testas turi matuoti tikrus matmenis naršyklėje — ir su stiliais, ir be
jų (`docs/kort_vieta_playwright.js`, 1b dalis).

**Šalis nenurodyta** — vėliavos nerodom, rodom tik miestą. Klaidų
nemetam, tuščio kvadrato nepaliekam.

**Patikra:** `grep -rc "flags/" templates/ | grep -v _veliava` turi
grąžinti tuščią — vėliavos kelias minimas tik vienoje dalyje.

---

## 6. VIENA ŠALIS VISAI SVETAINEI

> Įrašyta 2026-09-01.

Šalis **nėra** atskiras kiekvieno puslapio filtras. Tai **viena bendra
reikšmė**: pakeitus ją bet kurioje vietoje, ji pasikeičia visose.

**Viena vieta kode.** Jokių kopijų, jokių antrų sąrašų:

| Kas | Kur |
|---|---|
| šablonas | `templates/partials/_salis.html` — trys stiliai: `juosta`, `sonine`, `lakstas` |
| reikšmė ir sąrašas | `apps/listings/salies_juosta.py` |
| kiekiai | `salies_juosta.kiekiai()` — ta pati funkcija, kuri duoda skaičių ant panelės mygtuko |
| perdavimas šablonams | `context_processors.salis` |

**Reikšmės sluoksniai** (adresas laimi visada):

    ?salis=de  →  slapukas „salis"  →  paskyros profilis  →  lt

**Kur veikia ta pati reikšmė:** paieškos panelė pradžioje, pradžios
skirtukai („Naujausi", „Populiariausi"), šoninė juosta rezultatuose,
išplėstinė paieška, `/imones/` ir `/imones/paieska/`, žemėlapis.

**Šalies keitimas neišvalo kitų filtrų.** Markė, kaina, metai lieka;
išvalomi tik miestas ir spindulys — jie pririšti prie senos šalies
(`salies_juosta.PRIRISTI_PRIE_SALIES`). Tie patys laukai nuimami ir
skaičiuojant skaičiukus: kitaip „Vilnius + 50 km" prie visų kitų šalių
rodytų 0.

**Skelbimo šalis — TIK iš kontaktų bloko**, niekada iš paieškoje
pasirinktos. Jei jos skiriasi, virš bloko — tyli eilutė:

    Šis skelbimas yra Vokietijoje   Rodyti visus skelbimus Vokietijoje

Vietininkas („Vokietijoje") duodamas tik lietuviškoje sąsajoje —
`salys.vietininkas()` kitomis kalbomis grąžina paprastą pavadinimą,
nes ten prielinksnis yra vertime.

**Patikra:** `docs/viena_salis_test.py` (tikras klientas, tikri adresai)
ir `docs/viena_salis_playwright.js` (naršyklė, nuotraukos 1600 ir 390 px).

---

## 7. Tos pačios taisyklės — įmonėms ir meistrams

Vieta pirma. Paslaugos ir kainos — kortelėje. Viskas kita — įmonės
puslapyje.

---

## Patikros sąrašas prieš atiduodant darbą

- [ ] Vieta pirmas filtras VISUOSE keturiuose paviršiuose
- [ ] Tvarka: šalis → miestas → spindulys
- [ ] Vieta nepaslėpta po „Daugiau filtrų"
- [ ] Kortelėje: nuotrauka, pavadinimas, metai, kaina, 3 parametrai, vieta
- [ ] Kortelėje NĖRA komplektacijos, įrangos, VIN, aprašymo, istorijos
- [ ] Kontaktų bloke: tipas, telefonas, žinutė, miestas, adresas,
      žemėlapis, „Kaip nuvažiuoti"
- [ ] Kontaktų blokas matomas be slinkimo iki galo (390 px)
- [ ] Kontaktai tik per `contact_block.html`
- [ ] Vėliavėlė visur, kur rodoma vieta, per `_veliava.html`
- [ ] Vėliavėlė VISUR po pavadinimo, ne prieš jį
- [ ] Vėliavėlė — SVG, 16×12, su rėmeliu; šalies vardas pilnas
- [ ] Kortelėje ir šalies sąrašuose vardas angliškas, kontaktų bloke — išverstas
- [ ] Vietos eilutė nesilaužo net su ilgu pavadinimu, vėliava nedingsta
- [ ] Kortelėje vieta rodoma vieną kartą (darbalaukyje žalia eilutė,
      telefone „Miestas" langelis)
- [ ] Be šalies — tik miestas, be tuščio kvadrato
- [ ] Šalis — viena reikšmė: pakeitus vienur, pasikeitė visur
- [ ] Šalies keitimas nenumetė markės, kainos, metų
- [ ] Skelbimo šalis paimta iš kontaktų bloko, ne iš paieškos
- [ ] Įmonėms ir meistrams — tos pačios taisyklės
