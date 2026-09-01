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

**Formatas visur vienodas — vėliava GALE, po pavadinimo:**

    Vilnius, Lietuva [vėliava]

Sąrašo eilutėje ji prilimpa prie pavadinimo, o skaičius nustumiamas į
dešinį kraštą:

    ○ Lietuva [vėliava]              4 821
    ● Visos šalys [gaublys]         48 320

Niekur ne prieš pavadinimą. Radus seną variantą — taisyti.

Šalies pavadinimas **pilnas ir išverstas** — ne kodas „LT" ar „DE".

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
- Vėliavų rinkinys — **visos** šalys iš `salys.py`. Vienas šaltinis, ne
  po failą kaskart.

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
- [ ] Vėliavėlė — SVG, 16×12, su rėmeliu; šalies vardas pilnas ir išverstas
- [ ] Be šalies — tik miestas, be tuščio kvadrato
- [ ] Šalis — viena reikšmė: pakeitus vienur, pasikeitė visur
- [ ] Šalies keitimas nenumetė markės, kainos, metų
- [ ] Skelbimo šalis paimta iš kontaktų bloko, ne iš paieškos
- [ ] Įmonėms ir meistrams — tos pačios taisyklės
