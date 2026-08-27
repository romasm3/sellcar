# Serverio būklė

Sugeneruota: 2026-08-27 19:31:54 CEST

## Kodas

```
sukasi:      a0c4726 feat(šalys): vienas šalių sąrašas, numatyta Lietuva, „Valstija" tik kur reikia
origin/master: a0c4726 feat(šalys): vienas šalių sąrašas, numatyta Lietuva, „Valstija" tik kur reikia
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
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
HTTP 301, 0.001054s
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
Aug 27 19:23:59 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 19:24:01 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 19:24:01 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 19:24:01 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.174s CPU time.
Aug 27 19:25:21 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 19:25:23 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 19:25:23 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 19:25:23 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.135s CPU time.
Aug 27 19:26:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 19:26:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 19:26:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 19:26:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.234s CPU time.
Aug 27 19:27:54 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 19:27:55 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 19:27:55 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 19:27:55 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.021s CPU time.
Aug 27 19:29:03 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 19:29:05 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 19:29:05 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 19:29:05 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.223s CPU time.
Aug 27 19:30:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 19:30:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 19:30:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 19:30:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.239s CPU time.
Aug 27 19:31:54 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
