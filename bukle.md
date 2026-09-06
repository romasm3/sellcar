# Serverio būklė

Sugeneruota: 2026-09-06 14:59:33 CEST

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
HTTP 301, 0.001153s
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
Sep 06 14:52:48 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 14:52:50 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 14:52:50 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 14:52:50 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.419s CPU time.
Sep 06 14:53:54 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 14:53:56 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 14:53:56 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 14:53:56 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.528s CPU time.
Sep 06 14:55:05 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 14:55:07 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 14:55:07 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 14:55:07 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.592s CPU time.
Sep 06 14:56:14 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 14:56:16 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 14:56:16 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 14:56:16 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.439s CPU time.
Sep 06 14:57:19 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 14:57:21 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 14:57:21 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 14:57:21 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.407s CPU time.
Sep 06 14:58:29 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 14:58:30 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 14:58:30 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 14:58:30 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.391s CPU time.
Sep 06 14:59:32 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
