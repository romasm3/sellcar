# Padangos ir ratlankiai — klaidų būsenos

Kategorija: `/create/tyres/`, `/create/rims/`, `/browse/tyres/`,
`/browse/rims/`, `/wheels/<id>/`.

Etalonas — autogidas.lt → Naujas skelbimas → Ratlankiai / padangos.

Patikra: `python docs/padangu_formos_test.py` (93 patikros). Be pataisų
jis krenta ties kiekviena žemiau išvardyta klaida.

| Nr. | Klaida | Būsena | Commit |
|-----|--------|--------|--------|
| TYRE-01 | Padangų formos pateikti neįmanoma: telefono ieškota per `getElementById('id_contact_phone')`, tokio id nėra | IŠTAISYTA | `33b2a8836ab3` |
| RIM-01 | Ta pati klaida ratlankių formoje | IŠTAISYTA | `33b2a8836ab3` |
| TYRE-02 | Validacijos pranešimai rodė ne tą lauką („Būtina nurodyti valstiją" vietoj „gamintoją") | IŠTAISYTA | `33b2a8836ab3` |
| TYRE-03 | Per trumpi sąrašai: skersmuo, plotis, profilis | IŠTAISYTA | `33b2a8836ab3` |
| TYRE-04 | Per trumpi sąrašai: protektoriaus gylis, likutis, būklė, sezoniškumas, paskirtis | IŠTAISYTA | `33b2a8836ab3` |
| TYRE-05 | Skelbimo puslapyje „Sezoniškumas: summer" — žalia DB reikšmė | IŠTAISYTA | `33b2a8836ab3` |
| TYRE-06 | Lentelėje angliški „Specifications", „Remaining", „Production year" | IŠTAISYTA | `33b2a8836ab3` |
| TYRE-07 | `/browse/tyres/` `<title>` — „Naršyti sunkvežimius" | IŠTAISYTA | `33b2a8836ab3` |
| TYRE-08 | Virš rezultatų „Nerasta jokių skelbimų 6" | IŠTAISYTA | `33b2a8836ab3` |
| TYRE-09 | Kortelėje žyma „Redaguoti profilį 50" | IŠTAISYTA | `33b2a8836ab3` |
| TYRE-10 | „Paskirtis" skirtinga formoje ir filtre; filtras naudojo kitas reikšmes | IŠTAISYTA | `33b2a8836ab3` |
| TYRE-12 | Automatinis pavadinimas be „R": „Bridgestone 225/45 18" | IŠTAISYTA | `33b2a8836ab3` |
| TYRE-13 | `agree_terms` be `required` | IŠTAISYTA | `33b2a8836ab3` |
| TYRE-16 | Kainos etiketė, komplekto suma, nuotraukų ribos | IŠTAISYTA | `33b2a8836ab3` |
| TYRE-17 | Kortelėje vienu metu „Naujas" (įkėlimo žyma) ir „Naudotas" (būklė) | IŠTAISYTA | `33b2a8836ab3` |

## Ką reiškė kiekviena pataisa

**TYRE-01 / RIM-01.** `handleTyresSubmit()` ir `handleRimsSubmit()` telefono
lauko ieškojo pagal `id_contact_phone`. Kontaktų blokas
(`partials/contact_block.html`) `name` gauna parametru — padangoms ir
ratlankiams tai `contact_phone` — bet `id` jame visada `id_phone`. Tad
paieška visada grąžindavo `null`, klaida įsirašydavo net užpildžius
telefoną, ir funkcija baigdavosi `return`: forma niekada nebūdavo išsiųsta.
Dabar ieškoma pagal `[name="contact_phone"]`.

Ta pati klaida buvo ir `wheels_create.html` (bendra forma). Kitur jos nėra
— patikrinti visi šablonai, testas šitą prižiūri nuolat.

**TYRE-02.** Šablono `msgid`'ai buvo teisingi („Manufacturer is required"
ir kt.) — klydo LIETUVIŠKAS vertimas penkiose eilutėse. Kitos 12 kalbų
buvo išverstos teisingai.

**TYRE-03 / TYRE-04.** Sąrašai papildyti pagal etaloną; senos reikšmės
paliktos. Skersmuo 15 → 57, plotis 24 → 82, profilis 14 → 29, gylis
10 → 27, likutis 10 → 20 (žingsnis 5), būklė 2 → 3 (`refurbished`),
sezoniškumas 3 → 4 (`other`), paskirtis 6 → 7 (`atv`).

`condition` stulpelis praplėstas iki 20 simbolių: `refurbished` yra 11.

**TYRE-10.** Paieškos panelė turėjo SAVO, ranka surašytus sąrašus ir net
kitas reikšmes: `car`, `van`, `agro`, `quad` vietoj
`passenger`/`commercial`/`industrial`/`atv`. Toks filtras nerasdavo nieko,
nes skelbimuose guli kitos reikšmės. Dabar abi vietos ima tą patį sąrašą iš
`models.py` (šablonams — per `templatetags/ratu_tags.py`), o senos nuorodos
perrašomos (`wheels_views.SENOS_PASKIRTYS`), kad išsaugotos paieškos
veiktų.

**TYRE-07 / 08 / 09.** Irgi lietuviško vertimo klaidos: „Browse Tyres" →
„Naršyti sunkvežimius", „Browse Rims" → „Naršyti automobilius",
„Listings found:" → „Nerasta jokių skelbimų", „Profile" → „Redaguoti
profilį". Papildomai eilutė virš rezultatų dabar rodo „Nerasta jokių
skelbimų" tik tada, kai rezultatų tikrai 0.

**TYRE-17.** Įkėlimo žyma pervadinta „Naujas" → „Naujiena". Ji yra
bendrame `partials/_laiko_zyma.html`, tad pasikeitė visose kategorijose;
esami 12 kalbų vertimai perkelti prie naujo `msgid`.

## Likę atviri

| Nr. | Klaida | Būsena |
|-----|--------|--------|
| TYRE-11 | — (nebuvo aprašyta užduotyje) | NEŽINOMA |
| TYRE-14 | — (nebuvo aprašyta užduotyje) | NEŽINOMA |
| TYRE-15 | — (nebuvo aprašyta užduotyje) | NEŽINOMA |

## Patikrinti tikri skelbimai

Abu anksčiau buvo neįvedami:

```
Bridgestone Duravis · Mikroautobusams · R16C · 205/65 · Vasarinės
  Naudotos · 2 vnt. · 50 € · likutis 100% · gylis 10 mm · 2024 · Marijampolė
  → #1 „Bridgestone 205/65 R16C", būsena active

Michelin Pilot Power 3 · Motociklams · R17 · 120/70 · Vasarinės
  1 vnt. · 130 € · Vilnius
  → #2 „Michelin 120/70 R17", būsena active
```
