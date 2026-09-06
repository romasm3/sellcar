# Serverio būklė

Sugeneruota: 2026-09-06 14:42:16 CEST

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
HTTP 301, 0.001204s
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
Sep 06 14:35:02 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 14:35:05 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 14:35:05 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 14:35:05 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.904s CPU time.
Sep 06 14:36:12 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 14:36:14 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 14:36:14 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 14:36:14 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.364s CPU time.
Sep 06 14:37:16 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 14:37:18 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 14:37:18 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 14:37:18 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.572s CPU time.
Sep 06 14:38:23 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 14:38:25 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 14:38:25 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 14:38:25 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.522s CPU time.
Sep 06 14:39:34 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 14:39:36 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 14:39:36 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 14:39:36 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.527s CPU time.
Sep 06 14:40:55 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 14:40:57 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 14:40:57 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 14:40:57 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.480s CPU time.
Sep 06 14:42:15 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
