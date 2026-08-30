# Serverio būklė

Sugeneruota: 2026-08-30 15:08:52 CEST

## Kodas

```
sukasi:      4e81a10 feat(įmonės): /imones/ perdarytas 1:1 pagal Fresha etaloną
origin/master: 4e81a10 feat(įmonės): /imones/ perdarytas 1:1 pagal Fresha etaloną
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/imones/views.py
   M config/settings.py
   M static/js/imones_fresha.js
   M templates/imones/_fresha_stiliai.html
   M templates/imones/imone.html
   M templates/imones/sarasas.html
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
HTTP 301, 0.001532s
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
/dev/sda1       291G   21G  270G   8% /
```

## Paskutinis auto-deploy

```
Aug 30 15:02:01 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 30 15:02:04 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 30 15:02:04 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 30 15:02:04 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.817s CPU time.
Aug 30 15:03:05 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 30 15:03:07 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 30 15:03:07 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 30 15:03:07 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.686s CPU time.
Aug 30 15:04:21 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 30 15:04:24 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 30 15:04:24 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 30 15:04:24 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.299s CPU time.
Aug 30 15:05:26 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 30 15:05:29 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 30 15:05:29 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 30 15:05:29 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.379s CPU time.
Aug 30 15:06:39 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 30 15:06:41 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 30 15:06:41 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 30 15:06:41 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.400s CPU time.
Aug 30 15:07:46 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 30 15:07:48 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 30 15:07:48 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 30 15:07:48 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.266s CPU time.
Aug 30 15:08:52 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
