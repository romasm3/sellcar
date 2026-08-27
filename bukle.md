# Serverio būklė

Sugeneruota: 2026-08-27 12:28:45 CEST

## Kodas

```
sukasi:      678d8b8 fix(žemėlapis): ratukas be Ctrl, OSM nuoroda tik prie OSM, miestai iš didžiosios
origin/master: 678d8b8 fix(žemėlapis): ratukas be Ctrl, OSM nuoroda tik prie OSM, miestai iš didžiosios
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/listings/urls.py
   M apps/listings/zemelapio_views.py
   M static/js/zemelapio_paieska.js
   M templates/listings/partials/_zemelapio_stiliai.html
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
HTTP 301, 0.001051s
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
/dev/sda1       291G   18G  274G   6% /
```

## Paskutinis auto-deploy

```
Aug 27 12:20:21 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 12:21:27 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 12:21:29 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 12:21:29 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 12:21:29 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.138s CPU time.
Aug 27 12:22:36 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 12:22:38 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 12:22:38 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 12:22:38 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.079s CPU time.
Aug 27 12:23:40 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 12:23:42 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 12:23:42 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 12:23:42 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.036s CPU time.
Aug 27 12:24:47 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 12:24:48 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 12:24:48 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 12:24:48 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.114s CPU time.
Aug 27 12:26:09 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 12:26:11 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 12:26:11 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 12:27:29 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 12:27:31 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 12:27:31 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 12:27:31 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.067s CPU time.
Aug 27 12:28:45 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
