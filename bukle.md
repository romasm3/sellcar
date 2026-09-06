# Serverio būklė

Sugeneruota: 2026-09-06 15:05:27 CEST

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
HTTP 301, 0.001689s
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
Sep 06 14:58:29 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 14:58:30 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 14:58:30 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 14:58:30 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.391s CPU time.
Sep 06 14:59:32 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 14:59:34 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 14:59:34 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 14:59:34 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.323s CPU time.
Sep 06 15:00:36 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 15:00:38 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 15:00:38 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 15:00:38 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.572s CPU time.
Sep 06 15:01:49 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 15:01:51 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 15:01:51 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 15:01:51 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.520s CPU time.
Sep 06 15:02:59 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 15:03:01 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 15:03:01 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 15:03:01 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.504s CPU time.
Sep 06 15:04:15 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 15:04:17 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 15:04:17 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 15:04:17 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.402s CPU time.
Sep 06 15:05:27 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
