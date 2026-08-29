# Serverio būklė

Sugeneruota: 2026-08-29 12:28:39 CEST

## Kodas

```
sukasi:      0b5e155 fix(žemėlapis): /map/ rodo tik skelbimus — įmonių kodo ten nebeliko
origin/master: 0b5e155 fix(žemėlapis): /map/ rodo tik skelbimus — įmonių kodo ten nebeliko
šaka:        master
darbo katalogas: švarus
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
HTTP 301, 0.001551s
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
  aktyvūs, baigsis per 7 d.: 5
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
Aug 29 12:21:03 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 29 12:21:05 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 29 12:21:05 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 29 12:21:05 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.407s CPU time.
Aug 29 12:22:15 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 29 12:22:17 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 29 12:22:17 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 29 12:22:17 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.343s CPU time.
Aug 29 12:23:26 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 29 12:23:28 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 29 12:23:28 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 29 12:23:28 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.328s CPU time.
Aug 29 12:25:14 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 29 12:25:16 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 29 12:25:16 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 29 12:25:16 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.366s CPU time.
Aug 29 12:26:24 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 29 12:26:26 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 29 12:26:26 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 29 12:26:26 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.474s CPU time.
Aug 29 12:27:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 29 12:27:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 29 12:27:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 29 12:27:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.210s CPU time.
Aug 29 12:28:39 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
