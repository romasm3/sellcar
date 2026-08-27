# Serverio būklė

Sugeneruota: 2026-08-27 17:01:22 CEST

## Kodas

```
sukasi:      552a28a feat(žemėlapis): kategorijos filtras, markės pagal kategoriją, saikingas priartinimas
origin/master: 552a28a feat(žemėlapis): kategorijos filtras, markės pagal kategoriją, saikingas priartinimas
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/listings/zemelapio_views.py
   M static/js/zemelapio_paieska.js
   M templates/listings/partials/_zemelapio_burbulas.html
   M templates/listings/partials/_zemelapio_filtrai.html
   M templates/listings/search_map.html
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
HTTP 301, 0.001463s
```

## Skelbimų būsenos

```

Listing — iš viso 35
  active        22   MATOMAS
  draft          9   nematomas
  expired        4   nematomas
  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─
  nematomi dėl būsenos:      13
  iš jų pasibaigę (expires_at praeityje): 4
  aktyvūs, baigsis per 7 d.: 4
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
/dev/sda1       291G   19G  273G   7% /
```

## Paskutinis auto-deploy

```
Aug 27 16:53:30 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.111s CPU time.
Aug 27 16:54:38 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 16:54:40 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 16:54:40 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 16:54:40 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.056s CPU time.
Aug 27 16:55:47 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 16:55:49 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 16:55:49 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 16:55:49 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.007s CPU time.
Aug 27 16:56:53 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 16:56:55 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 16:56:55 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 16:56:55 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.207s CPU time.
Aug 27 16:57:57 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 16:57:58 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 16:57:58 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 16:57:58 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.053s CPU time.
Aug 27 16:59:06 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 16:59:08 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 16:59:08 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 17:00:19 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 17:00:20 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 17:00:20 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 17:00:20 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.136s CPU time.
Aug 27 17:01:21 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
