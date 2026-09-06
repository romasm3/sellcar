# Serverio būklė

Sugeneruota: 2026-09-06 16:11:11 CEST

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
HTTP 301, 0.001220s
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
Sep 06 16:02:58 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 16:03:00 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 16:03:00 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 16:03:00 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.599s CPU time.
Sep 06 16:04:22 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 16:04:24 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 16:04:24 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 16:04:24 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.434s CPU time.
Sep 06 16:05:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 16:05:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 16:05:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 16:05:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.398s CPU time.
Sep 06 16:06:46 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 16:06:48 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 16:06:48 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 16:06:48 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.512s CPU time.
Sep 06 16:08:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 16:08:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 16:08:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 16:08:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.491s CPU time.
Sep 06 16:09:46 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 16:09:48 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 16:09:48 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 16:09:48 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.641s CPU time.
Sep 06 16:11:11 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
