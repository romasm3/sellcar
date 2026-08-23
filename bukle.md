# Serverio būklė

Sugeneruota: 2026-08-23 18:40:48 CEST

## Kodas

```
sukasi:      71312da fix(paieska): „Daugiau" sąrašas nebeužsidaro vedant pelę žemyn
origin/master: 71312da fix(paieska): „Daugiau" sąrašas nebeužsidaro vedant pelę žemyn
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/listings/wheels_views.py
   M locale/en/LC_MESSAGES/django.mo
   M locale/en/LC_MESSAGES/django.po
   M templates/listings/advanced_generic.html
   M templates/listings/partials/_adv_rail.html
   M templates/listings/partials/_panel_bodies.html
   M templates/listings/partials/_sp_field_styles.html
   M templates/listings/wheels_advanced_search.html
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
HTTP 301, 0.000997s
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
Aug 23 18:32:59 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 18:32:59 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 18:32:59 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.034s CPU time.
Aug 23 18:34:04 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 18:34:05 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 18:34:05 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 18:34:05 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.040s CPU time.
Aug 23 18:35:12 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 18:35:14 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 18:35:14 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 18:35:14 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.286s CPU time.
Aug 23 18:36:20 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 18:36:22 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 18:36:22 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 18:37:22 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 18:37:24 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 18:37:24 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 18:37:24 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.084s CPU time.
Aug 23 18:38:28 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 18:38:29 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 18:38:29 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 18:39:41 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 18:39:42 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 18:39:42 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 18:40:47 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
