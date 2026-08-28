# Serverio būklė

Sugeneruota: 2026-08-28 12:41:00 CEST

## Kodas

```
sukasi:      78cc64e feat(įmonės): paieškos juosta įmonių puslapyje, filtrai — į atskirą langą
origin/master: 78cc64e feat(įmonės): paieškos juosta įmonių puslapyje, filtrai — į atskirą langą
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/imones/admin.py
   M apps/imones/management/commands/imones_testines.py
   M apps/imones/models.py
   M apps/imones/views.py
   M apps/listings/paieskos_siulymai.py
   M static/js/paieskos_juosta.js
   M static/js/zemelapio_paieska.js
   M templates/imones/_stiliai.html
   M templates/imones/sarasas.html
   M templates/listings/partials/_zemelapio_stiliai.html
   M templates/listings/search_map.html
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
HTTP 301, 0.001429s
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
Aug 28 12:33:50 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 28 12:33:52 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 28 12:33:52 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 28 12:33:52 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.280s CPU time.
Aug 28 12:35:00 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 28 12:35:03 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 28 12:35:03 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 28 12:35:03 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.432s CPU time.
Aug 28 12:36:24 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 28 12:36:25 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 28 12:36:25 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 28 12:36:25 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.121s CPU time.
Aug 28 12:37:42 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 28 12:37:44 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 28 12:37:44 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 28 12:37:44 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.254s CPU time.
Aug 28 12:38:45 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 28 12:38:46 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 28 12:38:46 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 28 12:38:46 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.223s CPU time.
Aug 28 12:39:54 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 28 12:39:56 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 28 12:39:56 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 28 12:39:56 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.355s CPU time.
Aug 28 12:41:00 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
