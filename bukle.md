# Serverio būklė

Sugeneruota: 2026-08-24 15:27:31 CEST

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
HTTP 301, 0.001236s
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
Aug 24 15:18:55 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.053s CPU time.
Aug 24 15:19:55 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 15:19:57 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 15:19:57 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 15:21:00 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 15:21:02 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 15:21:02 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 15:21:02 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.198s CPU time.
Aug 24 15:22:10 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 15:22:12 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 15:22:12 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 15:22:12 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.010s CPU time.
Aug 24 15:23:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 15:23:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 15:23:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 15:23:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.072s CPU time.
Aug 24 15:24:40 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 15:24:41 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 15:24:41 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 15:24:41 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.035s CPU time.
Aug 24 15:26:12 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 15:26:15 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 15:26:15 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 15:26:15 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.044s CPU time.
Aug 24 15:27:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
