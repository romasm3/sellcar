# Serverio būklė

Sugeneruota: 2026-08-23 13:10:14 CEST

## Kodas

```
sukasi:      81b9d4b feat(i18n): panelių dropdown reikšmės verčiamos (motogear, padangos, priekabos)
origin/master: 81b9d4b feat(i18n): panelių dropdown reikšmės verčiamos (motogear, padangos, priekabos)
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/listings/translatable_db.py
   M locale/en/LC_MESSAGES/django.mo
   M locale/en/LC_MESSAGES/django.po
   M locale/lt/LC_MESSAGES/django.po
   M templates/listings/advanced_generic.html
   M templates/listings/contact.html
   M templates/listings/partials/panel_generic.html
   M templates/listings/partials/sidebar_generic.html
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
HTTP 301, 0.002087s
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
Aug 23 13:02:05 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 13:02:07 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 13:02:07 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 13:02:07 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.115s CPU time.
Aug 23 13:03:11 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 13:03:12 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 13:03:12 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 13:04:14 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 13:04:16 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 13:04:16 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 13:04:16 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.002s CPU time.
Aug 23 13:05:25 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 13:05:27 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 13:05:27 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 13:05:27 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.056s CPU time.
Aug 23 13:06:33 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 13:06:34 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 13:06:34 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 13:07:40 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 13:07:42 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 13:07:42 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 13:08:48 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 13:08:50 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 13:08:50 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 13:10:14 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
