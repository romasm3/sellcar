# AutoLeft (sellcar)
Django vehicle marketplace, Lithuanian-first. PRODUCTION server — be careful.

## Environment
PIRMAS ŽINGSNIS — pasitikrink, KUR esi. Nuo to priklauso viskas:

```bash
pwd; ls -d /root/autoleft 2>/dev/null && echo SERVERIS || echo KONTEINERIS
```

**A. Produkcijos serveris** (`/root/autoleft`, yra systemd, nginx,
/run/gunicorn.sock, psycopg): PostgreSQL, gunicorn per soketą, nginx.
- After backend changes: systemctl restart gunicorn
- You may run migrations, collectstatic and systemctl restart gunicorn
  yourself without asking; report what you did at the end

**B. Debesų konteineris** (`/home/user/sellcar`, PID 1 = process_api, nėra
systemd, nginx, psycopg): šviežias git klonas, be produkcijos prieigos.
- Vietinei patikrai: sqlite + runserver (žr. docs/*_test.py antraštes)
- `systemctl`, `journalctl`, `./deploy-agent.sh` čia NEVEIKIA — net
  nebandyk. Automatinis deploy'as IŠJUNGTAS — push į master NIEKO
  NEDIEGIA; diegia žmogus arba serverio sesija su ./idiek.sh
- Gyvą svetainę matai tik per `curl https://autoleft.com/…` — tuo ir
  tikrink, ar darbas pasiekė lankytoją (SKILL.md 8 taisyklė)
- Prieigos prie 66.94.124.183 (produkcijos VPS) NĖRA: nei ssh, nei
  systemctl, nei DB. Kodas į svetainę patenka TIK kai serveryje kas nors
  paleidžia ./idiek.sh (taimeris išjungtas)
- Jei reikia serverio žurnalų ar rankinio deploy'o — paprašyk žmogaus,
  nemeluok, kad „paleidau"

### PO KIEKVIENO DARBO — PATIKRINK, AR JIS GYVAI

Sumerginęs į master, PRIVALAI paleisti:

```bash
curl -s https://autoleft.com/ | grep -o 'name="versija" content="[^"]*"'
git rev-parse --short=12 HEAD
```

ir ataskaitoje VISADA rašyti eilutę:

```
GYVAI: taip (sha)
GYVAI: NE (gyvai <sha>, master <sha>, skirtumas N commit'ų)
```

Jei nesutampa — **pirmoje ataskaitos eilutėje, storai**:
**„DARBAS DAR NEPASIEKĖ SVETAINĖS"**. Ne pabaigoje, o pačioje pradžioje.

Niekada nerašyk „padaryta ir veikia gyvai", jei versijos žymė to
nepatvirtina. Žalias vietinis testas to NEPATVIRTINA.
- Never run destructive DB commands (DROP, DELETE without WHERE, flush) — always ask first
- deploy-agent.sh exists for snapshot deploys (last_good rollback)

## Conventions
- i18n: all templates {% load i18n %} + {% trans %}; views use gettext as _; models use gettext_lazy. Msgids written in Lithuanian (LT is source language). Single quotes inside HTML attributes
- Prices: step=1, |floatformat:0; valiuta VISADA EUR, šalis jos
  nelemia (apps/listings/valiutos.py — `pagal_sali()` bet kuriai šaliai
  grąžina EUR, `Listing.save()` įrašo EUR, static/js/valiuta.js šalies
  lauko neklauso). Sąsaja su šalimi buvo pašalinta, nes keitė tik ŽYMĘ,
  o ne sumą: 43 000 € virsdavo „43 000 zł". Daugiavaliutės (GBP/USD) —
  atskiras darbas kartu su kursais; iki tol EUR niekur nekeičiam.
  Months 01-12; dates m/Y
- Internal links: {% url 'xxx' %}?{{ request.GET.urlencode }} to preserve filters
- Frontend: Alpine.js + Tailwind
- Single Listing table for most categories via ?category= filter; trucks have separate TruckBrand/TruckModel tables
- Search panel partials live in templates/listings/partials/ (search_rail.html, search_panel.html, panel_*.html)
- PWA planuojama (dar nedaroma): statiniai tik per {% static %}, jokių
  absoliučių adresų su domenu (išskyrus og:/twitter: meta), kiekvienas
  fetch() su matoma klaidos būsena, ikonos static/img/, „atgal" nuorodos
  gilyn einančiuose ekranuose, target="_blank" tik išoriniams adresams.
  Taisyklės ir esama būklė: docs/pwa-pasiruosimas.md
- Kontaktai: paskyros numeris ir paštas skelbime NEĮRAŠOMI savaime.
  Formoje jie tik SIŪLOMI — placeholder'iu (`siulomas_telefonas`
  parametras contact_block.html), o placeholder į POST nepatenka.
  Įrašytas į `value` paskyros numeris nugulėdavo skelbime žmogui nieko
  nepakeitus, ir savininko asmeninis numeris atsidurdavo svetimo
  pardavėjo skelbime (#827). Skelbimo puslapis rodo TIK
  `listing.contact_phone`; tuščias — nerodo nieko, o ne paskyros
  numerio (`Listing.kontaktinis_telefonas`).
- Contact block: every create/edit form renders it ONLY via
  {% include 'listings/partials/contact_block.html' %} — never copy the HTML.
  Per-category differences go through include parameters (show_postal,
  phone_name, css_style/cls_* for non-Tailwind skins...), never a second copy.
  Adding/removing a contact field = editing that one partial.
  Country/state lists come from contact_block_tags — do NOT pass country_choices
  from the view; several views used to narrow it to US-only by accident.
  A new category form MUST use this partial and those tags.

## Nuolatinės taisyklės — docs/taisykles.md
- Vieta yra svarbiausias filtras: pirma ir visada matoma kiekviename
  paviršiuje (panelė, šoninė juosta, išplėstinė, mobilus), tvarka
  šalis → miestas → spindulys. Kortelėje tik tai, ko reikia apsispręsti,
  ar verta atidaryti. Kontaktų blokas skelbime — pagrindinis elementas su
  tikslia vieta ir žemėlapiu. Šalies vėliavėlė visur, kur rodoma vieta,
  per `templates/partials/_veliava.html`.
- Pilnas sąrašas ir patikros būdai — `docs/taisykles.md`. Tikrinama
  PRIEŠ atiduodant kiekvieną darbą, ne tik naują kategoriją.

## Workflow

### DIRBAMA TIESIAI PRODUKCIJOJE (/root/autoleft)
GitHub — atsarginė kopija ir atsukimo istorija.

**AUTOMATINIS DEPLOY'AS IŠJUNGTAS SĄMONINGAI** (2026-09-24, žmogaus
sprendimas). `autoleft-deploy.timer` sustabdytas ir išjungtas
(`systemctl is-active` → inactive; unit'o nuoroda pašalinta). Jis po
kiekvienos kritusios patikros darydavo `git reset` ir galėjo ištrinti
serveryje daromus pakeitimus. NEĮJUNGINĖK jo atgal be žmogaus sutikimo.
Push į GitHub NIEKO NEDIEGIA — diegia tik `./idiek.sh` serveryje.

Tvarka kiekvienam pakeitimui:

    redaguoju → ./idiek.sh → git commit → git push (tik kopija)

`./idiek.sh` (viena komanda): nesucommit'intus pakeitimus pats
sucommit'ina (git add -A) PRIEŠ perkrovimą, įrašo VERSIJA, collectstatic,
`systemctl restart gunicorn`, tikrina https://autoleft.com/ iki 10×2 s ir
ar gyva versijos žymė = HEAD. Ne 200, o prieš tai buvo 200 →
`git reset --hard HEAD~1` + perkrovimas, pranešimas DIDELĖMIS raidėmis su
grąžinimo komanda ir įrašas `deploy/idiegimai.log`. Jei svetainė buvo
sulūžusi dar prieš — nieko neatsuka, tik praneša. Nepritaikytų migracijų
nevykdo — sustoja (pirma pg_dump, tada `migrate` ranka).
Po `./idiek.sh` lieka tik `git push` (jei commit'ino jis — commit'as jau yra).

- Kiekvienas pakeitimas — ATSKIRAS commit, kad būtų atsukamas po vieną
  (commit'ink pats su prasmingu pranešimu prieš `./idiek.sh`; jo
  automatinis commit'as — tik atsarga).
- Po kiekvieno pakeitimo PRIVALOMA `./idiek.sh` ir jo „GYVA: <sha>".
- Push atmestas → `git pull --rebase`, `./idiek.sh`, push (ne --force).
  Pull iš GitHub = kodas iš debesų į produkciją: pirma peržiūrėk, ką
  parsineši (`git log HEAD..origin/master`).
- Prieš bet kokį DB ar migracijų keitimą: `pg_dump` į /root/backups/
  su data. Neatsukamos migracijos (pvz. 0107, trinanti contact_phone)
  be kopijos nediegiamos.
- NIEKADA: `rm -rf`, `DROP TABLE`, `TRUNCATE`, `git push --force`.
- Veikiu TIK /root/autoleft viduje.
- Nesakau „padaryta", kol nepatikrinau gyvai per curl.

### Debesų konteinerio sesijos (/home/user/sellcar)
Konteineris prie serverio NEPRIEINA (nėra ssh, raktų, systemd, maršruto
į VPS). Jis gali tik commit'inti ir push'inti į GitHub — o push nuo šiol
NEDIEGIA. Todėl debesų sesija darbo gyvai patikrinti NEGALI ir privalo
tai pasakyti, o ne skelbti „padaryta". Diegia žmogus arba serverio sesija.

### Bendra
- Commit as you go: small logical commits after each meaningful step,
  Conventional Commits format (feat/fix/chore...), then push.
- Niekada necommitinti .env, *.bak, db dump'ų, media/.
- Stop and ask before anything irreversible (destructive DB commands,
  data-losing migrations).
- Versijos žymę (`meta name="versija"`) rašo `./idiek.sh` (ir
  `./deploy-agent.sh`) PRIEŠ perkrovimą; vien `systemctl restart gunicorn`
  jos NEatnaujina. Tikrinama ir pagal tikrą pakeitimą (žymeklį).
- Gyvai tikrinama TIK per `curl`, niekada per naršyklę: naršyklė ir
  tarpinės talpyklos rodo seną puslapį, ir taip jau buvo pranešta apie
  „nepataisytą" klaidą, kuri iš tikrųjų buvo gyva ir veikianti.
- Diegimo tvarka (deploy-agent.sh): `manage.py check` eina PRIEŠ
  migracijas — sulūžęs kodas sustabdomas nepalietus duomenų. Jei
  migracijos jau pritaikytos, o patikra krinta, kodas NEBEATSUKAMAS:
  sena versija liktų su naujesne schema. Tokiu atveju skriptas sustoja
  ir šaukiasi žmogaus, o DB atkuriama iš kopijos.
- Patikros išvestis niekada nemetama į /dev/null — kitaip žurnale lieka
  tik „patikra krito", o priežasties nesimato.
- MATOMAS ŽYMEKLIS prieš kiekvieną darbą. Dar prieš pradėdamas
  pasirink, KĄ konkrečiai matysi per curl, kai darbas bus gyvas:
  tekstą, CSS klasę, elementą ar skaičių. Komentaro eilutės, testų
  failai ir vien modelio savybės patikrai NETINKA — jų iš išorės
  nematyti, ir tada patikra neįmanoma nei patvirtinti, nei paneigti.
  Ataskaitoje rodyk tą žymeklį, o ne vien versijos žymę.
- Test accounts: admin romasm3@gmail.com, buyer romasm333@gmail.com
