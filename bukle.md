# Serverio būklė

Sugeneruota: 2026-09-06 15:22:03 CEST

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
HTTP 301, 0.001574s
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
Sep 06 15:14:49 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 15:14:51 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 15:14:51 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 15:14:51 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.457s CPU time.
Sep 06 15:16:03 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 15:16:05 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 15:16:05 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 15:16:05 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.669s CPU time.
Sep 06 15:17:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 15:17:40 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 15:17:40 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 15:17:40 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 3.510s CPU time.
Sep 06 15:18:39 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 15:18:41 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 15:18:41 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 15:18:41 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.544s CPU time.
Sep 06 15:19:45 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 15:19:47 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 15:19:47 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 15:19:47 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.461s CPU time.
Sep 06 15:20:59 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 15:21:01 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 15:21:01 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 15:21:01 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.592s CPU time.
Sep 06 15:22:03 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
