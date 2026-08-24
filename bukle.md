# Serverio būklė

Sugeneruota: 2026-08-24 19:24:14 CEST

## Kodas

```
sukasi:      7448ced fix(paštas): laiškai nebesiunčiami į negyvus domenus
origin/master: 7448ced fix(paštas): laiškai nebesiunčiami į negyvus domenus
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/listings/templatetags/listing_filters.py
   M templates/listings/listing_list.html
   M templates/listings/partials/_adv_rail_ico.html
   M templates/listings/partials/category_icon.html
   M templates/listings/partials/search_panel.html
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
HTTP 301, 0.001270s
```

## Skelbimų būsenos

```

Listing — iš viso 35
  active        23   MATOMAS
  draft          9   nematomas
  expired        3   nematomas
  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─
  nematomi dėl būsenos:      12
  iš jų pasibaigę (expires_at praeityje): 3
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
/dev/sda1       291G   15G  277G   5% /
```

## Paskutinis auto-deploy

```
Aug 24 19:16:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.168s CPU time.
Aug 24 19:17:41 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 19:17:44 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 19:17:44 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 19:17:44 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.525s CPU time.
Aug 24 19:18:49 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 19:18:51 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 19:18:51 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 19:18:51 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.060s CPU time.
Aug 24 19:20:00 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 19:20:02 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 19:20:02 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 19:20:02 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.504s CPU time.
Aug 24 19:21:08 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 19:21:10 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 19:21:10 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 19:21:10 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.147s CPU time.
Aug 24 19:22:09 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 19:22:11 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 19:22:11 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 19:22:11 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.095s CPU time.
Aug 24 19:23:12 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 19:23:13 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 19:23:13 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 19:24:14 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
