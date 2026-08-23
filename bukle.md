# Serverio būklė

Sugeneruota: 2026-08-23 21:07:46 CEST

## Kodas

```
sukasi:      29c0b79 fix(skelbimas): nuotraukų juosta nebešokinėja perjungiant
origin/master: 29c0b79 fix(skelbimas): nuotraukų juosta nebešokinėja perjungiant
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
HTTP 301, 0.002087s
```

## Skelbimų būsenos

```

Listing — iš viso 47
  active        33   MATOMAS
  draft         11   nematomas
  expired        3   nematomas
  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─
  nematomi dėl būsenos:      14
  iš jų pasibaigę (expires_at praeityje): 3
  aktyvūs, baigsis per 7 d.: 4
  aktyvūs be pabaigos datos: 16 (pvz. testiniai)
Truck: skelbimų nėra.
WheelListing: skelbimų nėra.

Viešame sąraše matomi tik status="active" (+ neseniai parduoti).
Jei tavo seni skelbimai yra "expired" — juos reikia aktyvuoti iš naujo,
o ne taisyti kode.
```

## Vietos diske

```
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       291G   15G  277G   5% /
```

## Paskutinis auto-deploy

```
Aug 23 20:59:10 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 20:59:10 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 21:00:19 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 21:00:21 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 21:00:21 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 21:00:21 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.274s CPU time.
Aug 23 21:01:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 21:01:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 21:01:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 21:02:44 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 21:02:46 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 21:02:46 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 21:02:46 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.228s CPU time.
Aug 23 21:03:54 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 21:03:55 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 21:03:55 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 21:05:04 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 21:05:06 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 21:05:06 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 21:05:06 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.315s CPU time.
Aug 23 21:06:24 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 21:06:25 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 21:06:25 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 21:06:25 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.031s CPU time.
Aug 23 21:07:46 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
