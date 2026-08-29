# Serverio būklė

Sugeneruota: 2026-08-29 12:48:25 CEST

## Kodas

```
sukasi:      0b5e155 fix(žemėlapis): /map/ rodo tik skelbimus — įmonių kodo ten nebeliko
origin/master: 0b5e155 fix(žemėlapis): /map/ rodo tik skelbimus — įmonių kodo ten nebeliko
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/imones/admin.py
   M apps/imones/management/commands/imones_testines.py
   M apps/imones/models.py
   M apps/imones/views.py
   M templates/base.html
   M templates/imones/sarasas.html
```

## Servisai

```
gunicorn                 deactivating
nginx                    active
postgresql               active
autoleft-deploy.timer    active
```

## Ar svetainė atsako

```
HTTP 301, 0.940994s
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
  aktyvūs, baigsis per 7 d.: 6
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
/dev/sda1       291G   20G  271G   7% /
```

## Paskutinis auto-deploy

```
Aug 29 12:41:32 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 29 12:41:34 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 29 12:41:34 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 29 12:41:34 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.393s CPU time.
Aug 29 12:42:46 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 29 12:42:48 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 29 12:42:48 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 29 12:42:48 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.252s CPU time.
Aug 29 12:43:48 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 29 12:43:50 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 29 12:43:50 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 29 12:43:50 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.286s CPU time.
Aug 29 12:44:56 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 29 12:44:58 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 29 12:44:58 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 29 12:44:58 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.305s CPU time.
Aug 29 12:46:07 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 29 12:46:09 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 29 12:46:09 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 29 12:46:09 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.506s CPU time.
Aug 29 12:47:19 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 29 12:47:21 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 29 12:47:21 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 29 12:47:21 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.486s CPU time.
Aug 29 12:48:25 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
