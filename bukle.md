# Serverio būklė

Sugeneruota: 2026-08-28 12:51:24 CEST

## Kodas

```
sukasi:      4cda8fa feat(įmonės): puslapis tik įmonėms — savas žemėlapis, paslaugų siūlymai
origin/master: 4cda8fa feat(įmonės): puslapis tik įmonėms — savas žemėlapis, paslaugų siūlymai
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/imones/models.py
   M apps/imones/views.py
   M apps/listings/paieskos_siulymai.py
   M static/js/paieskos_juosta.js
   M templates/imones/_stiliai.html
   M templates/imones/sarasas.html
   M templates/partials/_paieskos_juosta.html
   M templates/partials/_paieskos_juosta_stiliai.html
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
HTTP 301, 0.008847s
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
Aug 28 12:43:29 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 28 12:43:30 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 28 12:43:30 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 28 12:43:30 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.275s CPU time.
Aug 28 12:44:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 28 12:44:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 28 12:44:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 28 12:44:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.360s CPU time.
Aug 28 12:46:16 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 28 12:46:18 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 28 12:46:18 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 28 12:46:18 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.380s CPU time.
Aug 28 12:47:25 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 28 12:47:27 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 28 12:47:27 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 28 12:47:27 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.583s CPU time.
Aug 28 12:48:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 28 12:48:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 28 12:48:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 28 12:48:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.443s CPU time.
Aug 28 12:49:55 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 28 12:49:57 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 28 12:49:57 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 28 12:49:57 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.307s CPU time.
Aug 28 12:51:24 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
