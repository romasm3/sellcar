# PWA — planuojama, bet kodas rašomas jau dabar

**Būsena: DAR NEDAROMA.** Manifesto, service worker'io ir ikonų projekte
nėra ir šiuo metu jų nekuriam. Bet AutoLeft **taps įdiegiama programėle**
(PWA), todėl kiekvienas naujas gabalas kodo rašomas taip, kad tada
užtektų pridėti manifestą, service worker'į ir ikonas — be perrašymų.

Šis dokumentas yra taisyklių sąrašas kasdieniam darbui ir esamos būklės
inventorius. Trumpa versija gyvena
`.claude/skills/nauja-kategorija/SKILL.md` (skyrius „PWA").

---

## Šešios taisyklės

### 1. Statiniai failai versijuojami (hash pavadinime)

Service worker'is gali saugiai kešuoti tik tokį failą, kurio pavadinimas
keičiasi pasikeitus turiniui (`isiminti.a1b2c3.js`). Tai reikalinga ir
dabar — be to naršyklė laiko seną `style.css` po diegimo.

Praktikoje: statiniai failai jungiami tik per `{% static %}`, niekada
`/static/js/foo.js` ranka. Tada įjungus maišos saugyklą (Django
`ManifestStaticFilesStorage`) visi adresai persitvarko savaime.

### 2. Jokių įrašytų absoliučių adresų su domenu

Standalone režime programėlė gyvena savo lange; adresas su `https://autoleft.com`
išmuša vartotoją į naršyklę. Visur — `{% url %}` arba santykinis kelias.

Vienintelė leistina išimtis: `og:` ir `twitter:` meta žymos. Jos skirtos
Facebook/Telegram robotams, ne naršymui, ir absoliutaus adreso reikalauja
pagal specifikaciją.

### 3. Puslapis turi elgtis padoriai be interneto

Kiekviena `fetch()` užklausa turi turėti `.catch()` su **matoma** klaidos
būsena: „Nepavyko įkelti. Bandykite dar kartą" ir mygtukas pakartoti —
ne tuščias ekranas ir ne amžinas „Kraunama…".

Taisyklė paprasta: jei rodai „Kraunama…", privalai turėti ir „Nepavyko".

### 4. Nuotraukos ir ikonos — vienoje vietoje

Programėlės ikonos (192 ir 512 px) turi atsirasti pridedant failus į vieną
katalogą, o ne medžiojant logotipą po šablonus. Logotipas ir ženklai
laikomi `static/img/`, šablonuose jungiami per `{% static %}`.

Naujų ikonų nekuriam kiekviename šablone atskirai — dedam į `static/img/`
ir naudojam iš ten.

### 5. Naršymas turi veikti be naršyklės mygtukų

Standalone režime nėra „atgal" juostos. Todėl kiekvienas ekranas, į kurį
galima „nueiti gilyn", turi savo kelią atgal:

* drill-in ekranai (`/pasirinkti/`, filtrų sluoksniai) — „atgal" nuoroda
  arba × su `grizti` parametru;
* vidiniai puslapiai — trupinių takas (`Pagrindinis › … › dabartinis`);
* formos su žingsniais — mygtukas „Atgal", ne tik naršyklės rodyklė.

### 6. Nieko, kas remiasi pilnu adresu arba iššoka iš programėlės

* `window.location.href = 'https://…'` — ne; santykinis kelias arba
  `{% url %}` reikšmė iš `data-` atributo.
* `target="_blank"` — tik tikrai išoriniams adresams (Facebook, WhatsApp,
  pardavėjo svetainė). Vidinei nuorodai — niekada: programėlėje ji
  atsidarytų naršyklėje ir vartotojas iš jos nebegrįžtų.

---

## Esama būklė (patikrinta 2026-08-24)

| Taisyklė | Būklė | Pastaba |
|---|---|---|
| 1. Statiniai versijuojami | ❌ dar ne | `settings.py` neturi `STATICFILES_STORAGE` su maiša; failai jungiami per `{% static %}`, tad įjungimas bus vienos eilutės darbas |
| 2. Absoliutūs adresai | ✅ švaru | 4 vietos, visos — `og:`/`twitter:` meta (leistina išimtis) |
| 3. Klaidų būsenos | ⚠️ dalinai | 189 `fetch()` iškvietimai, iš jų su `.catch()` — 79 |
| 4. Ikonos vienoje vietoje | ❌ dar ne | programėlės ikonų nėra; logotipas — CSS blokas su „AL" tekstu, ne failas |
| 5. „Atgal" gilyn einančiuose ekranuose | ✅ iš esmės | `/pasirinkti/` turi `grizti`, detalioje paieškoje ir `/perziureti/` — trupinių takas |
| 6. `target="_blank"` vidinėms nuorodoms | ⚠️ 6 vietos | `listing_detail` ×3 ir `dealer_public_page` ×3; likę 25 — išoriniai (soc. tinklai, WhatsApp, Viber) |

Ženklas ⚠️ nereiškia, kad reikia mesti darbus ir taisyti — reiškia, kad
liesdamas tą vietą sutvarkai ją pakeliui.

---

## Ko prireiks, kai PWA darysim

Sąrašas trumpas būtent todėl, kad kasdien laikomės taisyklių aukščiau:

1. `static/manifest.webmanifest` — pavadinimas, `start_url` (santykinis),
   `display: standalone`, temos spalvos iš `docs/dizaino-sistema.md`.
2. Ikonos `static/img/ikona-192.png` ir `ikona-512.png` (+ `maskable`).
3. `static/js/sw.js` — app shell kešas, tinklo-pirma strategija HTML'ui,
   kešo-pirma versijuotiems statiniams failams, atsarginis „nėra ryšio"
   puslapis.
4. `<link rel="manifest">` ir registracija `base.html`.
5. `ManifestStaticFilesStorage` įjungimas + `collectstatic`.

Nė vienas iš šių žingsnių nereikalauja liesti šablonų logikos — jei
taisyklių laikomasi.
