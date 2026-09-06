# Serverio būklė

Sugeneruota: 2026-09-06 16:16:08 CEST

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
HTTP 301, 0.001136s
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
Sep 06 16:08:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 16:08:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 16:08:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 16:08:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.491s CPU time.
Sep 06 16:09:46 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 16:09:48 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 16:09:48 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 16:09:48 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.641s CPU time.
Sep 06 16:11:11 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 16:11:13 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 16:11:13 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 16:11:13 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.523s CPU time.
Sep 06 16:12:28 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 16:12:30 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 16:12:30 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 16:12:30 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.507s CPU time.
Sep 06 16:13:29 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 16:13:31 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 16:13:31 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 16:13:31 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.478s CPU time.
Sep 06 16:14:59 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 16:15:01 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 16:15:01 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 16:15:01 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.521s CPU time.
Sep 06 16:16:07 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
