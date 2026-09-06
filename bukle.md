# Serverio būklė

Sugeneruota: 2026-09-06 18:16:16 CEST

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
HTTP 301, 0.001865s
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
Sep 06 18:09:25 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 18:09:28 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 18:09:28 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 18:09:28 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.504s CPU time.
Sep 06 18:10:40 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 18:10:43 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 18:10:43 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 18:10:43 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.461s CPU time.
Sep 06 18:11:49 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 18:11:52 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 18:11:52 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 18:11:52 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.537s CPU time.
Sep 06 18:12:53 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 18:12:55 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 18:12:55 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 18:12:55 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.542s CPU time.
Sep 06 18:14:04 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 18:14:06 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 18:14:06 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 18:14:06 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.411s CPU time.
Sep 06 18:15:14 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 18:15:16 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 18:15:16 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 18:15:16 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.637s CPU time.
Sep 06 18:16:16 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
