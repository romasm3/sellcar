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

1. kontaktų bloke skelbimo puslapyje, prieš miestą
2. skelbimo kortelėje sąraše, vietos eilutėje
3. žemėlapio žymeklio burbule
4. išsaugotose paieškose ir peržiūrėtuose skelbimuose

**Formatas visur vienodas:**

    [vėliava] Vilnius, Lietuva

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
  visose keturiose vietose. Jokių kopijų.
- Vėliavų rinkinys — **visos** šalys iš `salys.py`. Vienas šaltinis, ne
  po failą kaskart.

**Šalis nenurodyta** — vėliavos nerodom, rodom tik miestą. Klaidų
nemetam, tuščio kvadrato nepaliekam.

**Patikra:** `grep -rc "flags/" templates/ | grep -v _veliava` turi
grąžinti tuščią — vėliavos kelias minimas tik vienoje dalyje.

---

## 6. Tos pačios taisyklės — įmonėms ir meistrams

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
- [ ] Vėliavėlė visose keturiose vietose, per `_veliava.html`
- [ ] Vėliavėlė — SVG, 16×12, su rėmeliu; šalies vardas pilnas ir išverstas
- [ ] Be šalies — tik miestas, be tuščio kvadrato
- [ ] Įmonėms ir meistrams — tos pačios taisyklės
