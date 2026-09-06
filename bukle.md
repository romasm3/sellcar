# Serverio būklė

Sugeneruota: 2026-09-06 17:37:08 CEST

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
HTTP 301, 0.001993s
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
Sep 06 17:29:37 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 17:29:39 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 17:29:39 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 17:29:39 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.398s CPU time.
Sep 06 17:31:11 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 17:31:13 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 17:31:13 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 17:31:13 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.398s CPU time.
Sep 06 17:32:14 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 17:32:16 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 17:32:16 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 17:32:16 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.402s CPU time.
Sep 06 17:33:16 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 17:33:18 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 17:33:18 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 17:33:18 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.415s CPU time.
Sep 06 17:34:17 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 17:34:19 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 17:34:19 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 17:34:19 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.467s CPU time.
Sep 06 17:35:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 17:35:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 17:35:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 17:35:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.521s CPU time.
Sep 06 17:37:07 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
