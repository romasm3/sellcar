# Serverio būklė

Sugeneruota: 2026-08-27 16:16:36 CEST

## Kodas

```
sukasi:      6f9e103 fix(žemėlapis): filtrai realiai filtruoja sąrašą ir žymeklius
origin/master: 6f9e103 fix(žemėlapis): filtrai realiai filtruoja sąrašą ir žymeklius
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/listings/brand_api.py
   M apps/listings/context_processors.py
   M apps/listings/views.py
   M apps/listings/zemelapio_views.py
   M static/js/zemelapio_paieska.js
   M templates/listings/partials/_zemelapio_filtrai.html
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
HTTP 301, 0.001135s
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
Aug 27 16:09:12 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 16:09:12 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.015s CPU time.
Aug 27 16:10:11 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 16:10:15 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 16:10:15 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 16:10:15 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.194s CPU time.
Aug 27 16:11:13 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 16:11:15 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 16:11:15 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 16:11:15 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.192s CPU time.
Aug 27 16:12:16 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 16:12:18 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 16:12:18 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 16:13:21 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 16:13:22 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 16:13:22 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 16:13:22 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.031s CPU time.
Aug 27 16:14:23 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 16:14:25 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 16:14:25 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 16:15:34 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 16:15:36 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 16:15:36 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 16:15:36 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.049s CPU time.
Aug 27 16:16:36 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
