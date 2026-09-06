# Serverio būklė

Sugeneruota: 2026-09-06 10:34:29 CEST

## Kodas

```
sukasi:      7a71bd0 vertimai: uzpildyti, sugadinti pazymeti fuzzy
origin/master: 2907582 fix(vertimai): fuzzy eilučių tvarkymas de/fr/vi/ar + .mo iš repo į deploy'ą
šaka:        master
darbo katalogas: švarus
```

## Servisai

```
gunicorn                 active
nginx                    active
postgresql               active
autoleft-deploy.timer    active
```

## Ar svetainė atsako

```
HTTP 301, 0.001200s
```

## Skelbimų būsenos

```

Listing — iš viso 35
  active        16   MATOMAS
  expired       10   nematomas
  draft          9   nematomas
  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─
  nematomi dėl būsenos:      19
  iš jų pasibaigę (expires_at praeityje): 10
  aktyvūs, baigsis per 7 d.: 5
  aktyvūs be pabaigos datos: 8 (pvz. testiniai)
Truck: skelbimų nėra.
WheelListing: skelbimų nėra.

Viešame sąraše matomi tik status="active" (+ neseniai parduoti).
Jei tavo seni skelbimai yra "expired" — juos reikia aktyvuoti iš naujo,
o ne taisyti kode.
```

## Vietos diske

```
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       291G   28G  264G  10% /
```

## Paskutinis auto-deploy

```
Sep 06 10:34:16 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 10:34:17 vmi3306453 autoleft-deploy[92923]: [2026-09-06 10:34:17] === Naujų commit'ų rasta: 7a71bd0 → 2907582 ===
Sep 06 10:34:17 vmi3306453 autoleft-deploy[92944]:     2907582 fix(vertimai): fuzzy eilučių tvarkymas de/fr/vi/ar + .mo iš repo į deploy'ą
Sep 06 10:34:17 vmi3306453 autoleft-deploy[92944]:     c493ddc test(patikra): bendros Playwright dalys perkeltos iš /tmp į repo
Sep 06 10:34:17 vmi3306453 autoleft-deploy[92923]: [2026-09-06 10:34:17] Kodas atnaujintas iki 2907582
Sep 06 10:34:29 vmi3306453 autoleft-deploy[93143]:     [email] praleisti negyvi adresai (1): testai@example.com
Sep 06 10:34:29 vmi3306453 autoleft-deploy[93143]:     .[email] praleisti negyvi adresai (1): testai@example.com
Sep 06 10:34:29 vmi3306453 autoleft-deploy[93143]:     ..s....
Sep 06 10:34:29 vmi3306453 autoleft-deploy[93143]:     ----------------------------------------------------------------------
Sep 06 10:34:29 vmi3306453 autoleft-deploy[93143]:     Ran 11 tests in 6.768s
Sep 06 10:34:29 vmi3306453 autoleft-deploy[93143]:     
Sep 06 10:34:29 vmi3306453 autoleft-deploy[93143]:     OK (skipped=1)
Sep 06 10:34:29 vmi3306453 autoleft-deploy[93143]:     ── 3/3  Vertimai: /en/ be lietuvių kalbos, šablonai apvynioti
Sep 06 10:34:29 vmi3306453 autoleft-deploy[93143]:       /en/imones/paieska/: Šalis
Sep 06 10:34:29 vmi3306453 autoleft-deploy[93143]:       /en/imones/paieska/: šalys
Sep 06 10:34:29 vmi3306453 autoleft-deploy[93143]:       /en/imones/paieska/: šioje
Sep 06 10:34:29 vmi3306453 autoleft-deploy[93143]:       /en/imones/paieska/: Žemėlapio
Sep 06 10:34:29 vmi3306453 autoleft-deploy[93143]:       /en/imones/paieska/: žemėlapio
Sep 06 10:34:29 vmi3306453 autoleft-deploy[93143]:     
Sep 06 10:34:29 vmi3306453 autoleft-deploy[93143]:     ----------------------------------------------------------------------
Sep 06 10:34:29 vmi3306453 autoleft-deploy[93143]:     Ran 4 tests in 0.436s
Sep 06 10:34:29 vmi3306453 autoleft-deploy[93143]:     
Sep 06 10:34:29 vmi3306453 autoleft-deploy[93143]:     FAILED (failures=1)
Sep 06 10:34:29 vmi3306453 autoleft-deploy[93143]:     
Sep 06 10:34:29 vmi3306453 autoleft-deploy[93143]:     PATIKRA NEPRAĖJO — nediegti.
```
