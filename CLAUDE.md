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
- Jei reikia serverio žurnalų ar rankinio deploy'o — paprašyk žmogaus,
  nemeluok, kad „paleidau".
- Never run destructive DB commands (DROP, DELETE without WHERE, flush) — always ask first
- deploy-agent.sh exists for snapshot deploys (last_good rollback)

## Conventions
- i18n: all templates {% load i18n %} + {% trans %}; views use gettext as _; models use gettext_lazy. Msgids written in Lithuanian (LT is source language). Single quotes inside HTML attributes
- Prices: step=1, |floatformat:0, "$" suffix; months 01-12; dates m/Y
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
- Test accounts: admin romasm3@gmail.com, buyer romasm333@gmail.com
