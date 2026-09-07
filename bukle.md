# Serverio būklė

Sugeneruota: 2026-09-07 12:19:36 CEST

## Kodas

```
sukasi:      acc75a5 fix(ikelimas): nuotraukų įkėlimas neveikė 12 iš 13 kalbų — 404 dėl kalbos priešdėlio
origin/master: acc75a5 fix(ikelimas): nuotraukų įkėlimas neveikė 12 iš 13 kalbų — 404 dėl kalbos priešdėlio
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
HTTP 301, 0.001402s
```

## Skelbimų būsenos

```

Listing — iš viso 37
  active        17   MATOMAS
  draft         10   nematomas
  expired       10   nematomas
  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─
  nematomi dėl būsenos:      20
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
/dev/sda1       291G   29G  262G  10% /
```

## Paskutinis auto-deploy

```
Sep 07 12:13:02 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 07 12:13:05 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 07 12:13:05 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 07 12:13:05 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.897s CPU time.
Sep 07 12:14:05 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 07 12:14:07 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 07 12:14:07 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 07 12:14:07 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.535s CPU time.
Sep 07 12:15:09 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 07 12:15:12 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 07 12:15:12 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 07 12:15:12 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.754s CPU time.
Sep 07 12:16:11 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 07 12:16:14 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 07 12:16:14 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 07 12:16:14 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.561s CPU time.
Sep 07 12:17:24 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 07 12:17:34 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 07 12:17:34 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 07 12:17:34 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 3.090s CPU time.
Sep 07 12:18:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 07 12:18:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 07 12:18:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 07 12:18:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.432s CPU time.
Sep 07 12:19:35 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
