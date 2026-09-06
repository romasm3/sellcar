# Serverio būklė

Sugeneruota: 2026-09-06 14:52:48 CEST

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
HTTP 301, 0.002114s
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
Sep 06 14:45:48 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 14:45:50 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 14:45:50 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 14:45:50 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.516s CPU time.
Sep 06 14:47:05 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 14:47:07 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 14:47:07 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 14:47:07 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.550s CPU time.
Sep 06 14:48:13 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 14:48:15 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 14:48:15 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 14:48:15 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.416s CPU time.
Sep 06 14:49:15 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 14:49:18 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 14:49:18 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 14:49:18 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.448s CPU time.
Sep 06 14:50:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 14:50:33 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 14:50:33 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 14:50:33 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.615s CPU time.
Sep 06 14:51:43 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 14:51:45 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 14:51:45 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 14:51:45 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.415s CPU time.
Sep 06 14:52:48 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
