# Serverio būklė

Sugeneruota: 2026-09-06 15:28:54 CEST

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
HTTP 301, 0.001713s
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
Sep 06 15:22:03 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 15:22:05 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 15:22:05 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 15:22:05 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.637s CPU time.
Sep 06 15:23:04 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 15:23:06 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 15:23:06 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 15:23:06 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.578s CPU time.
Sep 06 15:24:16 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 15:24:19 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 15:24:19 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 15:24:19 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.568s CPU time.
Sep 06 15:25:29 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 15:25:31 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 15:25:31 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 15:25:31 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.648s CPU time.
Sep 06 15:26:39 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 15:26:41 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 15:26:41 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 15:26:41 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.461s CPU time.
Sep 06 15:27:46 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 15:27:48 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 15:27:48 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 15:27:48 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.787s CPU time.
Sep 06 15:28:54 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
