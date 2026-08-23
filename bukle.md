# Serverio būklė

Sugeneruota: 2026-08-23 18:51:58 CEST

## Kodas

```
sukasi:      383d13e fix(paieska): panelėje be vidinio perjungiklio, detalioje paieškoje — juosta visur
origin/master: 383d13e fix(paieska): panelėje be vidinio perjungiklio, detalioje paieškoje — juosta visur
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/listings/search_config/panels.py
   M apps/listings/views.py
   M apps/listings/wheels_views.py
   M locale/en/LC_MESSAGES/django.mo
   M locale/en/LC_MESSAGES/django.po
   M templates/listings/moto_parts_advanced.html
   M templates/listings/motogear_advanced.html
   M templates/listings/partials/_adv_rail.html
   M templates/listings/truck_parts_advanced.html
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
HTTP 301, 0.001844s
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
/dev/sda1       291G   15G  277G   5% /
```

## Paskutinis auto-deploy

```
Aug 23 18:44:08 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 18:44:08 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 18:45:15 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 18:45:16 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 18:45:16 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 18:45:16 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.113s CPU time.
Aug 23 18:46:24 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 18:46:26 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 18:46:26 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 18:46:26 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.062s CPU time.
Aug 23 18:47:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 18:47:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 18:47:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 18:48:31 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 18:48:33 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 18:48:33 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 18:49:41 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 18:49:43 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 18:49:43 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 18:49:43 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.048s CPU time.
Aug 23 18:50:47 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 18:50:48 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 18:50:48 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 18:50:48 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.056s CPU time.
Aug 23 18:51:58 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
