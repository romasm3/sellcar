# Serverio būklė

Sugeneruota: 2026-08-28 12:02:55 CEST

## Kodas

```
sukasi:      801d553 feat(įmonės): puslapiai pagal demo pažodžiui + pilni testiniai duomenys
origin/master: 801d553 feat(įmonės): puslapiai pagal demo pažodžiui + pilni testiniai duomenys
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/listings/views.py
   M static/js/imone.js
   M static/js/zemelapio_paieska.js
   M templates/listings/listing_list.html
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
HTTP 301, 0.001471s
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
Aug 28 11:56:16 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 28 11:56:18 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 28 11:56:18 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 28 11:56:18 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.392s CPU time.
Aug 28 11:57:23 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 28 11:57:25 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 28 11:57:25 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 28 11:57:25 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.181s CPU time.
Aug 28 11:58:28 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 28 11:58:30 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 28 11:58:30 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 28 11:58:30 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.258s CPU time.
Aug 28 11:59:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 28 11:59:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 28 11:59:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 28 11:59:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.320s CPU time.
Aug 28 12:00:39 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 28 12:00:41 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 28 12:00:41 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 28 12:00:41 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.358s CPU time.
Aug 28 12:01:48 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 28 12:01:50 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 28 12:01:50 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 28 12:01:50 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.653s CPU time.
Aug 28 12:02:55 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
