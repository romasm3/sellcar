# Serverio būklė

Sugeneruota: 2026-09-06 15:49:47 CEST

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
HTTP 301, 0.001827s
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
Sep 06 15:42:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 15:42:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 15:42:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 15:42:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.485s CPU time.
Sep 06 15:43:38 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 15:43:40 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 15:43:40 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 15:43:40 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.459s CPU time.
Sep 06 15:44:47 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 15:44:50 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 15:44:50 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 15:44:50 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.483s CPU time.
Sep 06 15:45:59 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 15:46:01 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 15:46:01 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 15:46:01 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.736s CPU time.
Sep 06 15:47:24 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 15:47:26 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 15:47:26 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 15:47:26 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.315s CPU time.
Sep 06 15:48:45 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 15:48:47 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 15:48:47 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 15:48:47 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.557s CPU time.
Sep 06 15:49:47 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
