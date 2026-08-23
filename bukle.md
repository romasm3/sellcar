# Serverio būklė

Sugeneruota: 2026-08-23 16:59:15 CEST

## Kodas

```
sukasi:      3991e6a fix(paieska): vienodi filtrai LT ir EN — motogear šoninė juosta ir FK reikšmės
origin/master: 3991e6a fix(paieska): vienodi filtrai LT ir EN — motogear šoninė juosta ir FK reikšmės
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/listings/urls.py
   M apps/listings/wheels_views.py
   M locale/en/LC_MESSAGES/django.mo
   M locale/en/LC_MESSAGES/django.po
   M templates/listings/listing_list.html
   M templates/listings/motogear_list.html
   M templates/listings/motorcycles_list.html
   M templates/listings/partials/_panel_bodies.html
   M templates/listings/partials/search_rail.html
   M templates/listings/trucks_list.html
   M templates/listings/wheels_advanced_search.html
   M templates/listings/wheels_detail.html
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
HTTP 301, 0.001279s
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
Aug 23 16:50:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 16:50:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 16:50:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.135s CPU time.
Aug 23 16:51:49 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 16:51:51 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 16:51:51 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 16:51:51 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.107s CPU time.
Aug 23 16:53:15 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 16:53:16 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 16:53:16 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 16:53:16 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.115s CPU time.
Aug 23 16:54:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 16:54:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 16:54:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 16:55:35 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 16:55:36 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 16:55:36 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 16:56:42 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 16:56:44 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 16:56:44 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 16:58:00 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 16:58:02 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 16:58:02 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 16:58:02 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.336s CPU time.
Aug 23 16:59:15 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
