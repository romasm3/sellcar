# Serverio būklė

Sugeneruota: 2026-08-29 12:10:26 CEST

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
HTTP 301, 0.001862s
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
Aug 29 12:03:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 29 12:03:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 29 12:03:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 29 12:03:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.427s CPU time.
Aug 29 12:04:35 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 29 12:04:37 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 29 12:04:37 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 29 12:04:37 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.270s CPU time.
Aug 29 12:05:49 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 29 12:05:51 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 29 12:05:51 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 29 12:05:51 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.303s CPU time.
Aug 29 12:06:57 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 29 12:06:59 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 29 12:06:59 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 29 12:06:59 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.358s CPU time.
Aug 29 12:08:17 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 29 12:08:19 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 29 12:08:19 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 29 12:08:19 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.265s CPU time.
Aug 29 12:09:18 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 29 12:09:20 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 29 12:09:20 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 29 12:09:20 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.169s CPU time.
Aug 29 12:10:26 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
