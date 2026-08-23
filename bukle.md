# Serverio būklė

Sugeneruota: 2026-08-23 13:20:54 CEST

## Kodas

```
sukasi:      38067e8 feat(i18n): ETAPAS 1 — vieši puslapiai angliškai
origin/master: 38067e8 feat(i18n): ETAPAS 1 — vieši puslapiai angliškai
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/listings/translatable_db.py
   M locale/en/LC_MESSAGES/django.mo
   M locale/en/LC_MESSAGES/django.po
   M locale/lt/LC_MESSAGES/django.po
   M templates/listings/agriculture_listing_create.html
   M templates/listings/bicycles_listing_create.html
   M templates/listings/camping_listing_create.html
   M templates/listings/electronics_listing_create.html
   M templates/listings/loading_equipment_create.html
   M templates/listings/moto_part_create.html
   M templates/listings/motogear_create.html
   M templates/listings/rental_car_create.html
   M templates/listings/rental_heavy_create.html
   M templates/listings/rental_minibus_create.html
   M templates/listings/services_listing_create.html
   M templates/listings/trailers_listing_create.html
   M templates/listings/truck_for_parts_create.html
   M templates/listings/trucks_listing_create.html
   M templates/listings/wheels_create.html
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
HTTP 301, 0.001231s
```

## Skelbimų būsenos

```

Listing — iš viso 47
  active        33   MATOMAS
  draft         11   nematomas
  expired        3   nematomas
  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─
  nematomi dėl būsenos:      14
  iš jų pasibaigę (expires_at praeityje): 3
  aktyvūs, baigsis per 7 d.: 3
  aktyvūs be pabaigos datos: 16 (pvz. testiniai)
Truck: skelbimų nėra.
WheelListing: skelbimų nėra.

Viešame sąraše matomi tik status="active" (+ neseniai parduoti).
Jei tavo seni skelbimai yra "expired" — juos reikia aktyvuoti iš naujo,
o ne taisyti kode.
```

## Vietos diske

```
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       291G   14G  277G   5% /
```

## Paskutinis auto-deploy

```
Aug 23 13:11:25 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 13:11:25 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 13:12:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 13:12:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 13:12:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 13:13:41 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 13:13:42 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 13:13:42 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 13:14:50 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 13:14:52 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 13:14:52 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 13:16:12 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 13:16:14 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 13:16:14 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 13:17:14 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 13:17:16 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 13:17:16 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 13:17:16 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.209s CPU time.
Aug 23 13:18:20 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 13:18:22 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 13:18:22 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 13:19:29 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 13:19:30 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 13:19:30 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 13:20:54 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
