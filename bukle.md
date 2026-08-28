# Serverio būklė

Sugeneruota: 2026-08-28 13:07:46 CEST

## Kodas

```
sukasi:      51f5346 feat(įmonės): trečias juostos laukas „Kada" pagal darbo laiką
origin/master: 51f5346 feat(įmonės): trečias juostos laukas „Kada" pagal darbo laiką
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/imones/admin.py
   M apps/imones/models.py
   M apps/listings/paieskos_siulymai.py
   M static/js/paieskos_juosta.js
   M templates/partials/_paieskos_juosta.html
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
HTTP 301, 0.001202s
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
Aug 28 12:59:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 28 12:59:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 28 12:59:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 28 12:59:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.339s CPU time.
Aug 28 13:00:55 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 28 13:00:57 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 28 13:00:57 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 28 13:00:57 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.434s CPU time.
Aug 28 13:02:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 28 13:02:31 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 28 13:02:31 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 28 13:02:31 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.389s CPU time.
Aug 28 13:03:54 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 28 13:03:55 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 28 13:03:55 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 28 13:03:55 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.368s CPU time.
Aug 28 13:05:25 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 28 13:05:27 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 28 13:05:27 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 28 13:05:27 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.210s CPU time.
Aug 28 13:06:33 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 28 13:06:35 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 28 13:06:35 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 28 13:06:35 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.237s CPU time.
Aug 28 13:07:46 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
