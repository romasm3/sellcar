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

## 6. NAUJA DEPLOY PATIKRA — PIRMA ATSKIRAI, TIK PASKUI Į GRANDINĘ

> Įrašyta 2026-09-01, po to, kai nauja statinių patikra kas minutę
> atsukdavo visiškai sveiką kodą.

Kiekviena nauja patikra `deploy-agent.sh` arba `deploy-from-git.sh`
pridedama TRIMIS žingsniais, ir ne kitokia tvarka:

**1. Paleidžiama ATSKIRAI, nieko neveikdama.** Tik loguoja, ką būtų
nusprendusi. Bent viena sėkminga ir viena nesėkminga eiga tikroje
aplinkoje. `bash -n` čia negalioja — jis tikrina sintaksę, ne elgesį.

**2. Turi savo testą, kuris ją PALEIDŽIA**, o ne skaito. Skriptas sukasi
su `set -euo pipefail`, kur elgesys nėra akivaizdus iš teksto:

* `grep` be atitikmens grąžina 1 → `pipefail` → `set -e` išmeta iš
  skripto (taip deploy'as nutrūkdavo dar prieš prasidedant);
* `curl` per gunicorn soketą be `X-Forwarded-Proto: https` gauna 301
  tuščiu kūnu, nes `SECURE_SSL_REDIRECT` įjungtas — patikra „nemato" HTML;
* `[[ ]] && komanda` paskutinėje eilutėje grąžina 1.

Pavyzdžiai: `docs/deploy_statiniu_test.sh`, `docs/deploy_atsukimo_test.sh`.

**3. Tik tada įjungiama — ir NIEKADA į grandinę, kuri atsuka kodą.**
Gyvybės klausimas yra vienas: `health_check`, t. y. ar puslapis
atsidaro. Visa kita — pageidavimai:

| Patikra | Kas nutinka, kai krenta |
|---|---|
| `health_check` | atsukam kodą (ir sutvarkom git) |
| statinių maišas, versijos žymė, bet kas kita | **tik įspėjimas žurnale** |

Blogai: `if health_check && mano_patikra; then` — viena smulkmena
nusveria veikiantį puslapį.

**Po atsukimo darbinis katalogas privalo likti švarus.** `rsync` grąžina
senus failus, bet git HEAD lieka rodyti į naują commit'ą; tada kitas
`git pull` nulūžta ir taimeris tyliai nustoja veikti. Tvarko
`sutvarkyti_po_atsukimo`: pataisa į atsargą, `git reset --hard` į
`last_good/VERSIJA` sha, ir patikrinimas, kad `git status` tuščias.

---

## 7. VIENA ŠALIS VISAI SVETAINEI

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

## 8. Tos pačios taisyklės — įmonėms ir meistrams

Vieta pirma. Paslaugos ir kainos — kortelėje. Viskas kita — įmonės
puslapyje.

---

## 9. FILTRAS TIK RENKA REIKŠMĘ — PUSLAPIS KRAUNAMAS VIENĄ KARTĄ

Kiekvienas paieškos laukas — šoninėje juostoje, panelėje ir detalioje
paieškoje — laikosi tos pačios taisyklės:

* pasirinkimas keičia TIK vietinę būseną ir lauko užrašą;
* puslapis NEPERSIKRAUNA ir adresas NESIKEIČIA;
* skaičius ant „Filtruoti" atsinaujina gyvai (count endpoint);
* adresą atnaujina tik „Filtruoti" — vienu kartu, su visais pasirinkimais;
* „Išvalyti" valo tik paspaustas;
* naršyklės „atgal" grąžina ankstesnį filtrų rinkinį.

Išimčių nėra: šalis, kuras, markė, modelis ir visa kita elgiasi vienodai.
Šalies punktai formos viduje (`_salis.html` su `formoje=1`) yra laukas, ne
nuoroda; be formos (/imones/, /map/) jie lieka nuorodos.

Ką tikrinti kode:

* juostos šablonuose neturi likti nė vieno `form.submit()`,
  `@change="$el.form.submit()"` ar `onchange="this.form.submit()"`
  (vienintelė išimtis — sekcijos jungiklis, kuris keičia patį laukų
  rinkinį);
* laukas, kurio reikšmę valdo Alpine, valomas per įvykį
  (`data-isvalomas` + `@isvalyk`), o ne rašant tiesiai į `input.value` —
  Alpine tokį įrašą perrašo;
* `form.submit()` NEKELIA „submit" įvykio, tad visos apsaugos
  (`static/js/vienas_variantas.js`) praleidžiamos; jei reikia siųsti iš
  JS — `form.requestSubmit()`;
* nematomo paviršiaus ir suskleistos markės/modelio eilutės laukai
  siunčiami neturi — kitaip adrese lieka `?brand=&brand=` ir juosta
  atsistato su daugiau eilučių, nei buvo;
* `<input type="number">` pasiūlymų sąraše (`<datalist>`) reikšmė turi
  būti SKAIČIUS, o žmogui matomas užrašas — per `label`; tekstinės
  reikšmės („74 kW (100 AG)") laukas nepriima ir lieka tuščias.

Patikra: `docs/juostos_elgsena_playwright.js` — pasirenka šalį, kurą ir
markę (adresas nejuda, skaičius keičiasi tris kartus), paspaudžia
„Filtruoti" (adresas atnaujinamas vienu kartu su visais trimis).

---

## 10. SĄRAŠŲ TEKSTAS VISADA KAIRĖJE

Kiekvienoje sąrašo eilutėje — iškrentančiame lauke, šalių sąraše,
telefono eilutėse, /pasirinkti/ puslapyje — tekstas prasideda kairėje:

    justify-content: flex-start;  text-align: left;
    pavadinimo span: flex: 1; min-width: 0; text-align: left;
    skaičius (jei yra): margin-left: auto;

`justify-content: space-between` sąrašo eilutėje NEBENAUDOJAMAS: jis
eilutės turinį stumdo pagal tekstų ilgį. Antraštėms (`.sp-items-header`,
`.sp-picker-hdr`) tai netaikoma — jos ne sąrašo eilutės.

Viena išimtis, kuri stipresnė: šalies vardas NEIŠTEMPIAMAS iki viso
pločio (`flex: 0 1 auto`), nes vėliava turi likti prilipusi prie
pavadinimo (taisyklė 5). Skaičius į dešinę nueina per `margin-left:auto`.

Patikra: `docs/sarasu_lygiuote_playwright.js` — matuoja tikrą atstumą
nuo eilutės krašto iki teksto; riba 38 px (14 px vidus + 16 px langelis
+ 10 px tarpas). `GYVAI=1` — matuoja gyvoje svetainėje.

---

## 11. SĄRAŠŲ UŽRAŠŲ IR REIKŠMIŲ NEKEISTI

Filtrų laukų pavadinimai ir jų reikšmės NEVERČIAMI, NEPERVADINAMI ir
NETRUMPINAMI savo nuožiūra — niekada, nebent žmogus aiškiai paprašo tą
patį lauką pervadinti. Reikšmės imamos iš modelio arba konfigūracijos
TOKIOS, KOKIOS YRA.

Jei sąrašas tuščias, tvarkoma tik JUNGTIS (pvz. laukas nebuvo įrašytas į
`CHOICES_BY_DB_FIELD`), o ne kuriamas naujas reikšmių sąrašas.

„Pagražinimas" be prašymo — irgi keitimas. Prieš bet kokį išvaizdos
darbą:

1. užfiksuok, kaip veikia dabar (`docs/sonines_juostos_sarasas.py`
   išrašas arba lygiavertis), ir įrašyk failą;
2. padaryk darbą;
3. po darbo tą patį išrašą pakartok ir ĮRODYK, kad elgsena ir turinys
   nepasikeitė — skirtumas turi būti tuščias arba paaiškintas eilutė po
   eilutės.

Be to įrodymo darbas neatiduodamas.

---

## 12. JOKIO AUTOMATINIO PERSIKROVIMO PASIRINKUS FILTRĄ

Žr. 9. Pasirinkimas kaupiamas, adresą keičia tik „Filtruoti". Šablonuose
neturi likti nė vieno `form.submit()`, `@change="$el.form.submit()"` ar
`onchange="this.form.submit()"` filtro lauke.

---

## 13. KALBOS PERJUNGIKLIS MATOMAS VISADA

Antraštės kalbos perjungiklis nėra slepiamas jokiame plotyje. Ties
≤360 px jis buvo dingęs, o 360 CSS px (720 fizinių taškų, DPR 2) yra
dažniausias Android plotis — kalbos nematydavo didelė dalis žmonių.

Pavidalas telefone (etalonas `docs/demo/mob-antraste-demo.html`):
vėliavėlė 20×15, kalbos kodas DIDŽIOSIOMIS (13 px, svoris 700, tarpas
tarp raidžių 0,3 px — per `text-transform`, pati reikšmė lieka „lt") ir
11 px rodyklė. ~56 px pločio, 36 px aukščio, be fono ir be rėmelio;
telpa ir 320 px ekrane.

Kai antraštėje trūksta vietos, trumpinama „Įkelti" (≤340 px lieka tik
„+"), o NE kalba.

Šalies juosta — VIENA 52 px eilutė, kuri nesilaužo: trumpinamas tik
pavadinimas (`ellipsis`), o vėliava, skaičius ir „Keisti" yra
`flex: 0 0 auto`; „Keisti" nustumiamas per `margin-left: auto`.

Nuorodų juosta po antrašte slenka į šoną (`overflow-x: auto`,
`white-space: nowrap`, slankiklis paslėptas) ir puslapio neišplečia.

Patikra: `docs/kalbos_perjungiklis_playwright.js` ir
`docs/mob_antrastes_playwright.js` — 320, 360, 390, 414 ir 768 px:
perjungiklis matomas, antraštė vienoje eilutėje be persidengimo, šalies
juosta ne aukštesnė kaip 52 px, `scrollWidth <= innerWidth`, lakštas
kaip etalone. `GYVAI=1` — tikrina gyvoje svetainėje.

---

## 14. ŽINUTĖSE — VARDAS, NIEKADA EL. PAŠTAS

Pokalbių sąraše ir pokalbyje žmogus vadinamas vardu. El. paštas
nerodomas nė vienoje vietoje — nei kaip pavadinimas, nei avataro raidėje.

Vardą duoda VIENA vieta —
`apps/conversations/templatetags/pokalbiu_tags.vardas`:
`Profile.display_name` → vardas ir pavardė → „Naudotojas #42". Adresą
atpažįstam iš „@" ir atmetam: registruojantis `username` prilyginamas el.
paštui (accounts/forms.py), tad `display_name` atsarginis kelias be šito
grąžintų būtent adresą.

Savo paskyroje (antraštės meniu, /accounts/…) adresas lieka — ten žmogus
mato save patį.

Patikra: `docs/zinutes_test.py` (serveris) ir
`docs/zinutes_playwright.js` (naršyklė) — abu krenta, jei pokalbių
srityje randa el. pašto pavidalo tekstą.

---

## 15. SERVERYJE GYVENANTYS FAILAI — DEPLOY JŲ NELIEČIA

`.env` ir `google-translate-key.json` yra tik serveryje; git'e jų nėra.
`restore_code` naudoja `rsync --delete`, todėl failas, atsiradęs PO
paskutinio snapshot'o, atsukimo metu buvo TRINAMAS. Būtent taip 2026-09
dingo vertimo raktas ir pokalbių vertimas ėmė grąžinti originalą.

Sąrašas — VIENAS, `deploy-agent.sh` `SAUGOMI_FAILAI`. Iš jo daromi ir
rsync išskyrimai, ir patikra. Naują serverio failą pridedi TEN, ne
dviejose vietose.

Po kiekvieno deploy'o ir po kiekvieno atsukimo `tikrinti_raktus` patikrina,
ar failai vietoje; jei ne — žurnale 🔴 eilutės ir ataskaitos antraštėje
„TRŪKSTA SERVERIO FAILŲ".

## 16. ATSARGINĖS KOPIJOS NEGALI UŽPILDYTI DISKO

* `pg_dump | gzip` — nespaustas dumpas buvo ~2,8 GB, po kiekvieno
  deploy'o dar vienas; gzip mažina ~10 kartų (išmatuota: 332 kartus
  tekstiniam SQL).
* Laikom paskutines **5** (`KEEP_DB_DUMPS`), senesnes trinam.
* PRIEŠ kopiją ir prieš bet kokį kodo keitimą — laisvos vietos patikra.
  Mažiau nei **20 %** → deploy nutrūksta (`exit 2`) su aiškiu pranešimu,
  kodas nepaliestas.
* Patikra negali tapti gedimu: jei `df` atsako netikėtai, ji TYLI ir
  praleidžia, o ne stabdo deploy'ą amžinai.
* Žurnale — kopijos dydis, kopijų skaičius ir likusi vieta.

Senas kopijas saugiai ištrinti paliekant dvi naujausias:

    ls -1t /root/autoleft_backups/db_* | tail -n +3 | xargs -r rm -f

Patikra: `docs/deploy_kopiju_test.sh` — paleidžia pačią logiką (failų
išlikimą po `--delete`, vietos ribą abiem kryptim, valymą, gzip).

---

## 17. TERMINAI — VIENAS ŠALTINIS, PATVIRTINTI VERTIMAI

`docs/terminai.md` — filtrų laukų, reikšmių, kategorijų ir sąsajos
terminai lietuvių, rusų ir anglų kalbomis. Vertimai **patvirtinti**: jų
neverčiam iš naujo ir nekeičiam savo nuožiūra. Abejojant dėl termino
etalonas — `autogidas.lt/ru/`, o ne naujas vertimas.

Naujas terminas pridedamas **į docs/terminai.md**, ne į .po. Tada:

    python docs/terminai_taikyti.py --bandymas   # parodo, ką keis
    python docs/terminai_taikyti.py              # įrašo .po ir .mo

Patvirtintas vertimas **negali likti `#, fuzzy`** — tokia eilutė
nekompiliuojama į .mo ir vartotojui nerodoma, t. y. vertimas neveiktų.
Fuzzy lieka tik neperžiūrėtoms mašinos eilutėms, kad matytųsi, jog jos
dar netikrintos.

Dalis tekstų į .po per `makemessages` nepatenka niekada: filtrų užrašai
ateina per `_(f['label'])`, o reikšmės — iš DB, ir xgettext kintamojo
nemato. Tokie tekstai registruojami `apps/listings/translatable_db.py`
(ten yra `TERMINAI_LT`, sutampantis su terminai.md).

`.mo` failai NEBELAIKOMI git'e (2026-09-06): binariniai, todėl kas kartą
kėlė merge konfliktus. Juos gamina deploy'as — `deploy-agent.sh` po
`collectstatic` paleidžia `compilemessages`. Į repo keliauja tik `.po`.

Iš to plaukia taisyklė: **kas išima `compilemessages` iš deploy'o,
išjungia visus vertimus.** `.po` be `.mo` nerodo nieko.

Patikra: `docs/terminai_test.py` — per tikrą gettext tikrina, ką pamato
rusas ir anglas, ar patvirtinti terminai nepažymėti fuzzy ir ar .mo ne
senesnis už .po.

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
- [ ] Nauja deploy patikra: paleista atskirai, turi savo testą, neatsuka kodo
- [ ] Šalis — viena reikšmė: pakeitus vienur, pasikeitė visur
- [ ] Šalies keitimas nenumetė markės, kainos, metų
- [ ] Skelbimo šalis paimta iš kontaktų bloko, ne iš paieškos
- [ ] Įmonėms ir meistrams — tos pačios taisyklės
- [ ] Filtro pasirinkimas neperkrauna puslapio ir nekeičia adreso
- [ ] „Filtruoti" atnaujina adresą vienu kartu su visais pasirinkimais
- [ ] Markės/modelio × ištrina eilutę ir nepalieka `?brand=` adrese
- [ ] Skaičiaus laukų `<datalist>` reikšmės skaitinės
- [ ] Sąrašų tekstas kairėje (offsetLeft <= 38 px visuose paviršiuose)
- [ ] Nė vienas užrašas ar reikšmė nepervadinti be prašymo
- [ ] Prieš/po išrašas sutampa arba skirtumas paaiškintas
- [ ] Kalbos perjungiklis matomas 320, 360, 390, 414 ir 768 px
- [ ] Pokalbiuose nerodomas nė vienas el. paštas
- [ ] Naujos žinutės atsiranda be puslapio perkrovimo, tekstas nedingsta
- [ ] Serverio failai (.env, raktai) išskirti iš snapshot/restore
- [ ] Kopijos suspaustos, laikom 5, vietos patikra prieš deploy'ą
- [ ] Nauji terminai — docs/terminai.md, ne tiesiai .po
- [ ] Po vertimų keitimo perrašytas ir sukommitintas .mo
