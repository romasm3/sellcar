# Serverio būklė

Sugeneruota: 2026-08-29 12:17:31 CEST

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
HTTP 301, 0.001236s
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
Aug 29 12:10:26 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 29 12:10:28 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 29 12:10:28 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 29 12:10:28 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.324s CPU time.
Aug 29 12:11:37 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 29 12:11:39 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 29 12:11:39 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 29 12:11:39 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.163s CPU time.
Aug 29 12:12:59 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 29 12:13:02 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 29 12:13:02 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 29 12:13:02 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.526s CPU time.
Aug 29 12:14:12 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 29 12:14:13 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 29 12:14:13 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 29 12:14:13 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.192s CPU time.
Aug 29 12:15:18 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 29 12:15:20 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 29 12:15:20 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 29 12:15:20 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.327s CPU time.
Aug 29 12:16:24 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 29 12:16:25 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 29 12:16:25 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 29 12:16:25 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.239s CPU time.
Aug 29 12:17:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
