# Serverio būklė

Sugeneruota: 2026-09-06 16:51:24 CEST

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
HTTP 301, 0.002241s
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
  aktyvūs, baigsis per 7 d.: 6
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
Sep 06 16:43:29 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 16:43:31 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 16:43:31 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 16:43:31 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.392s CPU time.
Sep 06 16:44:37 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 16:44:39 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 16:44:39 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 16:44:39 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.427s CPU time.
Sep 06 16:46:02 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 16:46:04 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 16:46:04 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 16:46:04 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.965s CPU time.
Sep 06 16:47:16 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 16:47:18 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 16:47:18 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 16:47:18 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.434s CPU time.
Sep 06 16:48:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 16:48:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 16:48:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 16:48:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.472s CPU time.
Sep 06 16:50:13 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 16:50:16 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 16:50:16 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 16:50:16 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.713s CPU time.
Sep 06 16:51:24 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
