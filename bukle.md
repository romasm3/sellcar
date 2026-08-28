# Serverio būklė

Sugeneruota: 2026-08-28 10:59:25 CEST

## Kodas

```
sukasi:      7d409de feat(žemėlapis): rezultatai persikrauna patys judinant žemėlapį
origin/master: 7d409de feat(žemėlapis): rezultatai persikrauna patys judinant žemėlapį
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M config/settings.py
   M config/urls.py
   M static/js/zemelapio_paieska.js
   M templates/listings/listing_list.html
   M templates/listings/partials/_zemelapio_stiliai.html
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
HTTP 301, 0.002298s
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
/dev/sda1       291G   19G  272G   7% /
```

## Paskutinis auto-deploy

```
Aug 28 10:51:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 28 10:51:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 28 10:51:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 28 10:51:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.386s CPU time.
Aug 28 10:53:16 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 28 10:53:18 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 28 10:53:18 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 28 10:53:18 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.541s CPU time.
Aug 28 10:54:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 28 10:54:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 28 10:54:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 28 10:54:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.259s CPU time.
Aug 28 10:55:40 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 28 10:55:42 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 28 10:55:42 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 28 10:55:42 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.492s CPU time.
Aug 28 10:56:54 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 28 10:56:56 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 28 10:56:56 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 28 10:56:56 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.384s CPU time.
Aug 28 10:58:19 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 28 10:58:21 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 28 10:58:21 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 28 10:58:21 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.283s CPU time.
Aug 28 10:59:25 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
