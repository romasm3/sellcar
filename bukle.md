# Serverio būklė

Sugeneruota: 2026-08-24 12:40:41 CEST

## Kodas

```
sukasi:      3f85319 refactor(naujumas): pašalintas nebenaudojamas new_listing_ids, dienų riba iš modelio
origin/master: 3f85319 refactor(naujumas): pašalintas nebenaudojamas new_listing_ids, dienų riba iš modelio
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M templates/listings/advanced_search.html
   M templates/listings/listing_list.html
   M templates/listings/moto_parts_browse.html
   M templates/listings/motorcycles_list.html
   M templates/listings/truck_parts_browse.html
   M templates/listings/trucks_list.html
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
HTTP 301, 0.001268s
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
Aug 24 12:36:09 vmi3306453 autoleft-deploy[164298]:      M templates/listings/listing_list.html
Aug 24 12:36:09 vmi3306453 autoleft-deploy[164298]:      M templates/listings/listing_list_v2.html
Aug 24 12:36:09 vmi3306453 autoleft-deploy[164298]:      M templates/listings/moto_parts_browse.html
Aug 24 12:36:09 vmi3306453 autoleft-deploy[164298]:      M templates/listings/motorcycles_advanced_search.html
Aug 24 12:36:09 vmi3306453 autoleft-deploy[164298]:      M templates/listings/motorcycles_list.html
Aug 24 12:36:09 vmi3306453 autoleft-deploy[164298]:      M templates/listings/my_listings.html
Aug 24 12:36:09 vmi3306453 autoleft-deploy[164298]:      M templates/listings/trucks_advanced_search.html
Aug 24 12:36:09 vmi3306453 autoleft-deploy[164298]:      M templates/listings/trucks_list.html
Aug 24 12:36:09 vmi3306453 autoleft-deploy[164281]: [2026-08-24 12:36:09] ❌ Darbo katalogas nešvarus — deploy'as sustabdytas. Sutvarkyk ranka.
Aug 24 12:36:09 vmi3306453 systemd[1]: autoleft-deploy.service: Main process exited, code=exited, status=1/FAILURE
Aug 24 12:36:09 vmi3306453 systemd[1]: autoleft-deploy.service: Failed with result 'exit-code'.
Aug 24 12:36:09 vmi3306453 systemd[1]: Failed to start AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 12:37:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 12:37:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 12:37:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 12:37:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.236s CPU time.
Aug 24 12:38:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 12:38:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 12:38:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 12:38:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.020s CPU time.
Aug 24 12:39:36 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 12:39:38 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 12:39:38 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 12:39:38 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.033s CPU time.
Aug 24 12:40:40 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
