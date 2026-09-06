# Serverio būklė

Sugeneruota: 2026-09-06 16:25:01 CEST

## Kodas

```
sukasi:      28672ee vertimai: uzpildytos visos matomos eilutes
origin/master: 28672ee vertimai: uzpildytos visos matomos eilutes
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
HTTP 301, 0.003585s
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
/dev/sda1       291G   28G  263G  10% /
```

## Paskutinis auto-deploy

```
Sep 06 16:17:16 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 16:17:23 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 16:17:23 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 16:17:23 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 2.472s CPU time.
Sep 06 16:18:23 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 16:18:26 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 16:18:26 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 16:18:26 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.502s CPU time.
Sep 06 16:19:36 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 16:19:38 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 16:19:38 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 16:19:38 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.411s CPU time.
Sep 06 16:20:58 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 16:21:01 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 16:21:01 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 16:21:01 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.486s CPU time.
Sep 06 16:22:16 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 16:22:18 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 16:22:18 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 16:22:18 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.523s CPU time.
Sep 06 16:23:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 16:23:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 16:23:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 16:23:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.536s CPU time.
Sep 06 16:25:01 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
