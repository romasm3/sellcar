# Serverio būklė

Sugeneruota: 2026-08-24 19:17:41 CEST

## Kodas

```
sukasi:      7448ced fix(paštas): laiškai nebesiunčiami į negyvus domenus
origin/master: 7448ced fix(paštas): laiškai nebesiunčiami į negyvus domenus
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
HTTP 301, 0.001039s
```

## Skelbimų būsenos

```

Listing — iš viso 35
  active        23   MATOMAS
  draft          9   nematomas
  expired        3   nematomas
  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─
  nematomi dėl būsenos:      12
  iš jų pasibaigę (expires_at praeityje): 3
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
/dev/sda1       291G   15G  277G   5% /
```

## Paskutinis auto-deploy

```
Aug 24 19:09:45 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.011s CPU time.
Aug 24 19:10:53 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 19:10:55 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 19:10:55 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 19:10:55 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.071s CPU time.
Aug 24 19:11:57 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 19:11:59 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 19:11:59 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 19:11:59 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.180s CPU time.
Aug 24 19:13:11 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 19:13:13 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 19:13:13 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 19:13:13 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.203s CPU time.
Aug 24 19:14:18 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 19:14:19 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 19:14:19 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 19:14:19 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.055s CPU time.
Aug 24 19:15:20 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 19:15:22 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 19:15:22 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 19:16:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 19:16:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 19:16:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 19:16:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.168s CPU time.
Aug 24 19:17:41 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
