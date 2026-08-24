# Serverio būklė

Sugeneruota: 2026-08-24 16:22:49 CEST

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
HTTP 301, 0.001407s
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
Aug 24 16:14:18 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.025s CPU time.
Aug 24 16:15:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 16:15:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 16:15:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 16:15:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.130s CPU time.
Aug 24 16:16:48 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 16:16:51 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 16:16:51 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 16:16:51 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.021s CPU time.
Aug 24 16:17:59 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 16:18:02 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 16:18:02 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 16:18:02 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.557s CPU time.
Aug 24 16:19:14 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 16:19:15 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 16:19:15 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 16:20:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 16:20:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 16:20:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 16:20:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.048s CPU time.
Aug 24 16:21:33 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 16:21:35 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 16:21:35 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 16:21:35 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.002s CPU time.
Aug 24 16:22:48 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
