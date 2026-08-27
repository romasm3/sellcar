# Serverio būklė

Sugeneruota: 2026-08-27 11:43:26 CEST

## Kodas

```
sukasi:      056083b feat(formos): vieningas privalomų laukų klaidų žymėjimas visose /create/
origin/master: 056083b feat(formos): vieningas privalomų laukų klaidų žymėjimas visose /create/
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/listings/agriculture_views.py
   M apps/listings/bicycles_views.py
   M apps/listings/boats_views.py
   M apps/listings/camping_views.py
   M apps/listings/construction_views.py
   M apps/listings/electronics_views.py
   M apps/listings/forestry_views.py
   M apps/listings/listing_helpers.py
   M apps/listings/loading_views.py
   M apps/listings/models.py
   M apps/listings/motogear_views.py
   M apps/listings/motorcycles_views.py
   M apps/listings/rental_views.py
   M apps/listings/services_views.py
   M apps/listings/trailers_views.py
   M apps/listings/urls.py
   M apps/listings/views.py
   M templates/listings/listing_detail.html
   M templates/listings/partials/contact_block.html
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
HTTP 301, 0.001425s
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
/dev/sda1       291G   17G  274G   6% /
```

## Paskutinis auto-deploy

```
Aug 27 11:34:55 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 11:34:55 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 11:34:55 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.166s CPU time.
Aug 27 11:36:05 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 11:36:07 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 11:36:07 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 11:37:22 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 11:37:23 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 11:37:23 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 11:38:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 11:38:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 11:38:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 11:38:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.062s CPU time.
Aug 27 11:39:42 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 11:39:44 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 11:39:44 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 11:40:53 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 11:40:55 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 11:40:55 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 11:40:55 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.196s CPU time.
Aug 27 11:42:10 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 11:42:12 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 11:42:12 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 11:42:12 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.009s CPU time.
Aug 27 11:43:25 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
