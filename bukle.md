# Serverio būklė

Sugeneruota: 2026-08-24 12:22:16 CEST

## Kodas

```
sukasi:      cd36a44 merge: master (išsaugotų skelbimų pastabos)
origin/master: cd36a44 merge: master (išsaugotų skelbimų pastabos)
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/listings/models.py
   M apps/listings/motogear_views.py
   M apps/listings/motorcycles_views.py
   M apps/listings/trucks_views.py
   M apps/listings/views.py
   M apps/listings/wheels_views.py
   M templates/base.html
   M templates/listings/listing_list.html
   M templates/listings/moto_parts_browse.html
   M templates/listings/motogear_list.html
   M templates/listings/motorcycles_advanced_search.html
   M templates/listings/motorcycles_list.html
   M templates/listings/truck_parts_browse.html
   M templates/listings/trucks_advanced_search.html
   M templates/listings/trucks_list.html
   M templates/listings/wheels_list.html
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
HTTP 301, 0.001112s
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
Aug 24 12:13:42 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 12:13:42 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 12:14:54 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 12:14:56 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 12:14:56 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 12:14:56 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.177s CPU time.
Aug 24 12:16:24 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 12:16:25 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 12:16:25 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 12:17:40 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 12:17:42 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 12:17:42 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 12:17:42 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.426s CPU time.
Aug 24 12:18:46 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 12:18:48 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 12:18:48 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 12:18:48 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.025s CPU time.
Aug 24 12:19:57 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 12:19:59 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 12:19:59 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 12:21:04 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 12:21:05 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 12:21:05 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 12:21:05 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.061s CPU time.
Aug 24 12:22:16 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
