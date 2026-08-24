# Serverio būklė

Sugeneruota: 2026-08-24 17:47:15 CEST

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
HTTP 301, 0.001277s
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
Aug 24 17:39:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 17:39:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 17:39:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 17:39:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.179s CPU time.
Aug 24 17:40:39 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 17:40:42 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 17:40:42 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 17:40:42 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.551s CPU time.
Aug 24 17:41:59 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 17:42:00 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 17:42:00 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 17:42:00 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.141s CPU time.
Aug 24 17:43:27 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 17:43:29 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 17:43:29 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 17:43:29 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.127s CPU time.
Aug 24 17:44:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 17:44:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 17:44:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 17:44:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.101s CPU time.
Aug 24 17:45:47 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 17:45:49 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 17:45:49 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 17:45:49 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.132s CPU time.
Aug 24 17:47:15 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
