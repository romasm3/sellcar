# Serverio būklė

Sugeneruota: 2026-09-06 17:51:24 CEST

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
HTTP 301, 0.001467s
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
Sep 06 17:44:07 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 17:44:09 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 17:44:09 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 17:44:09 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.536s CPU time.
Sep 06 17:45:16 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 17:45:18 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 17:45:18 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 17:45:18 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.846s CPU time.
Sep 06 17:46:24 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 17:46:26 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 17:46:26 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 17:46:26 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.499s CPU time.
Sep 06 17:47:59 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 17:48:01 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 17:48:01 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 17:48:01 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.509s CPU time.
Sep 06 17:49:04 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 17:49:06 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 17:49:06 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 17:49:06 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.500s CPU time.
Sep 06 17:50:16 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 17:50:18 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 17:50:18 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 17:50:18 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.529s CPU time.
Sep 06 17:51:24 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
