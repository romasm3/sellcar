# Serverio būklė

Sugeneruota: 2026-08-24 18:16:47 CEST

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
HTTP 301, 0.001107s
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
Aug 24 18:08:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.181s CPU time.
Aug 24 18:09:36 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 18:09:38 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 18:09:38 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 18:09:38 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.130s CPU time.
Aug 24 18:10:40 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 18:10:41 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 18:10:41 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 18:10:41 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.104s CPU time.
Aug 24 18:11:59 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 18:12:01 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 18:12:01 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 18:12:01 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.168s CPU time.
Aug 24 18:13:04 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 18:13:05 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 18:13:05 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 18:13:05 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.196s CPU time.
Aug 24 18:14:08 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 18:14:10 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 18:14:10 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 18:15:28 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 18:15:30 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 18:15:30 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 18:15:30 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.230s CPU time.
Aug 24 18:16:47 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
