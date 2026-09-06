# Serverio būklė

Sugeneruota: 2026-09-06 15:41:09 CEST

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
HTTP 301, 0.001763s
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
Sep 06 15:33:40 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 15:33:42 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 15:33:42 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 15:33:42 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.399s CPU time.
Sep 06 15:34:46 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 15:34:47 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 15:34:47 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 15:34:47 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.357s CPU time.
Sep 06 15:35:55 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 15:35:57 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 15:35:57 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 15:35:57 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.432s CPU time.
Sep 06 15:37:09 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 15:37:11 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 15:37:11 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 15:37:11 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.510s CPU time.
Sep 06 15:38:18 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 15:38:20 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 15:38:20 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 15:38:20 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.752s CPU time.
Sep 06 15:39:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 15:39:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 15:39:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 15:39:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.439s CPU time.
Sep 06 15:41:09 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
