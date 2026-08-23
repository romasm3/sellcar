# Serverio būklė

Sugeneruota: 2026-08-23 19:10:52 CEST

## Kodas

```
sukasi:      b74cbb4 feat(paieska): „Motociklai" sąraše — ir padangos motociklams bei keturračiams
origin/master: b74cbb4 feat(paieska): „Motociklai" sąraše — ir padangos motociklams bei keturračiams
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/listings/search_config/panels.py
   M apps/listings/views.py
   M templates/listings/advanced_generic.html
   M templates/listings/partials/_sp_field_styles.html
   M templates/listings/partials/fields/_model.html
   M templates/listings/partials/panel_generic.html
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
HTTP 301, 0.219014s
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
Aug 23 19:03:49 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 19:03:51 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 19:03:51 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 19:03:51 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.170s CPU time.
Aug 23 19:04:58 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 19:05:00 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 19:05:00 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 19:05:00 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.000s CPU time.
Aug 23 19:06:09 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 19:06:11 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 19:06:11 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 19:06:11 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.121s CPU time.
Aug 23 19:07:20 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 19:07:21 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 19:07:21 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 19:07:21 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.318s CPU time.
Aug 23 19:08:27 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 19:08:29 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 19:08:29 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 19:08:29 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.251s CPU time.
Aug 23 19:09:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 19:09:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 19:09:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 19:09:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.185s CPU time.
Aug 23 19:10:52 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
