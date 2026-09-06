# Serverio būklė

Sugeneruota: 2026-09-06 17:08:31 CEST

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
HTTP 301, 0.003385s
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
Sep 06 17:01:24 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 17:01:26 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 17:01:26 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 17:01:26 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.424s CPU time.
Sep 06 17:02:45 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 17:02:47 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 17:02:47 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 17:02:47 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.439s CPU time.
Sep 06 17:03:49 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 17:03:51 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 17:03:51 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 17:03:51 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.417s CPU time.
Sep 06 17:05:10 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 17:05:12 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 17:05:12 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 17:05:12 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.547s CPU time.
Sep 06 17:06:16 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 17:06:18 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 17:06:18 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 17:06:18 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.498s CPU time.
Sep 06 17:07:27 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 17:07:29 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 17:07:29 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 17:07:29 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.543s CPU time.
Sep 06 17:08:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
