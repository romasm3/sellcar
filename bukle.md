# Serverio būklė

Sugeneruota: 2026-08-27 13:11:20 CEST

## Kodas

```
sukasi:      0736ac3 feat(žemėlapis): kainų žymekliai, kortelė virš žymeklio ir apatinis lapas
origin/master: 0736ac3 feat(žemėlapis): kainų žymekliai, kortelė virš žymeklio ir apatinis lapas
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/listings/brand_api.py
   M apps/listings/context_processors.py
   M apps/listings/geokodavimas.py
   M apps/listings/views.py
   M config/settings.py
   M templates/base.html
   M templates/listings/listing_list.html
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
HTTP 301, 0.001959s
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
Aug 27 13:04:16 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 13:04:18 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 13:04:18 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 13:04:18 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.164s CPU time.
Aug 27 13:05:23 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 13:05:25 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 13:05:25 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 13:05:25 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.034s CPU time.
Aug 27 13:06:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 13:06:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 13:06:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 13:06:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.258s CPU time.
Aug 27 13:07:43 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 13:07:45 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 13:07:45 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 13:07:45 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.075s CPU time.
Aug 27 13:08:54 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 13:08:55 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 13:08:55 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 13:08:55 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.148s CPU time.
Aug 27 13:10:07 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 13:10:09 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 13:10:09 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 13:10:09 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.170s CPU time.
Aug 27 13:11:19 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
