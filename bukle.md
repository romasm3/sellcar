# Serverio būklė

Sugeneruota: 2026-08-27 16:08:08 CEST

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
HTTP 301, 0.001761s
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
/dev/sda1       291G   18G  273G   7% /
```

## Paskutinis auto-deploy

```
Aug 27 15:59:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 15:59:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.024s CPU time.
Aug 27 16:01:11 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 16:01:12 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 16:01:12 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 16:01:12 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.056s CPU time.
Aug 27 16:02:23 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 16:02:25 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 16:02:25 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 16:02:25 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.155s CPU time.
Aug 27 16:03:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 16:03:31 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 16:03:31 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 16:04:41 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 16:04:43 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 16:04:43 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 16:04:43 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.086s CPU time.
Aug 27 16:05:52 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 16:05:53 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 16:05:53 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 16:07:00 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 16:07:02 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 16:07:02 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 16:07:02 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.295s CPU time.
Aug 27 16:08:08 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
