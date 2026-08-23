# Serverio būklė

Sugeneruota: 2026-08-23 10:36:23 CEST

## Kodas

```
sukasi:      a8dc5ec fix(create): Pirmos registracijos data — viena antraštė, Metai ir Mėnuo vienoje eilėje
origin/master: a8dc5ec fix(create): Pirmos registracijos data — viena antraštė, Metai ir Mėnuo vienoje eilėje
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/listings/translatable_db.py
   M locale/en/LC_MESSAGES/django.mo
   M locale/en/LC_MESSAGES/django.po
   M locale/lt/LC_MESSAGES/django.mo
   M locale/lt/LC_MESSAGES/django.po
   M templates/listings/listing_create_cars_quick.html
   M templates/listings/listing_detail.html
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
HTTP 301, 0.002196s
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
  aktyvūs, baigsis per 7 d.: 2
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
Aug 23 10:27:26 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 10:27:26 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 10:27:26 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.051s CPU time.
Aug 23 10:28:54 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 10:28:55 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 10:28:55 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 10:30:10 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 10:30:12 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 10:30:12 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 10:30:12 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.021s CPU time.
Aug 23 10:31:14 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 10:31:16 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 10:31:16 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 10:31:16 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.086s CPU time.
Aug 23 10:32:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 10:32:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 10:32:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 10:33:54 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 10:33:55 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 10:33:55 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 10:33:55 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.035s CPU time.
Aug 23 10:35:14 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 10:35:15 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 10:35:15 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 10:36:23 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
