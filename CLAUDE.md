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
  nebandyk; iškelk pakeitimus į master ir deploy'ą paleis serverio timeris
- Gyvą svetainę matai tik per `curl https://autoleft.com/…` — tuo ir
  tikrink, ar darbas pasiekė lankytoją (SKILL.md 8 taisyklė)
- Prieigos prie 66.94.124.183 (produkcijos VPS) NĖRA: nei ssh, nei
  systemctl, nei DB. Kodas į svetainę patenka TIK per serverio deploy
  taimerį, kai commit'as atsiranda master'yje
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
- Commit as you go: small logical commits after each meaningful step, Conventional Commits format (feat/fix/chore...), then push
- Merge to master yourself when the work is done — do NOT ask each time.
  Before every merge: fetch master, check it hasn't moved under you, check
  your files don't overlap with what another session pushed, and re-run the
  checks ON THE MERGED TREE, not just on the branch. Merge only green work.
  Note that master auto-deploys to production within 5 min (deploy/README.md),
  so a merge is a deploy. Still stop and ask before anything irreversible
  (destructive DB commands, data-losing migrations).
- Po kiekvienos užbaigtos užduoties AUTOMATIŠKAI: git add (tik susiję
  failai) → commit (Conventional Commits) → git push origin master.
  Neklausti leidimo. Niekada necommitinti .env, *.bak, db dump'ų, media/.
- Debesų sesijos DEPLOY'INA push'indamos į master: serveryje sukasi
  autoleft-deploy.timer, kuris kas minutę tikrina origin/master ir,
  radęs naują commit'ą, pats parsisiunčia, migruoja, surenka statinius
  ir perkrauna gunicorn. Push į master = deploy.
- Darbas NĖRA baigtas, kol autoleft.com versijos žymė nesutampa su
  commit'u. Po push'o palauk ~3 min ir patikrink:
      curl -s https://autoleft.com/ | grep -o 'name="versija" content="[^"]*"'
      git rev-parse --short=12 HEAD
  Sutampa — baigta. Nesutampa — darbas dar NEPASIEKĖ svetainės, ir tai
  rašoma pirmoje ataskaitos eilutėje (žr. „PO KIEKVIENO DARBO" aukščiau).
  Deploy žurnalas: /var/log/autoleft-deploy.log, taip pat
  `journalctl -u autoleft-deploy -n 50`.
- MATOMAS ŽYMEKLIS prieš kiekvieną darbą. Dar prieš pradėdamas
  pasirink, KĄ konkrečiai matysi per curl, kai darbas bus gyvas:
  tekstą, CSS klasę, elementą ar skaičių. Komentaro eilutės, testų
  failai ir vien modelio savybės patikrai NETINKA — jų iš išorės
  nematyti, ir tada patikra neįmanoma nei patvirtinti, nei paneigti.
  Ataskaitoje rodyk tą žymeklį, o ne vien versijos žymę.
- Test accounts: admin romasm3@gmail.com, buyer romasm333@gmail.com
