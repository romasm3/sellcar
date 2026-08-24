# Serverio būklė

Sugeneruota: 2026-08-24 17:16:04 CEST

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
HTTP 301, 0.001239s
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
Aug 24 17:08:27 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.179s CPU time.
Aug 24 17:09:27 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 17:09:29 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 17:09:29 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 17:09:29 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.302s CPU time.
Aug 24 17:10:29 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 17:10:31 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 17:10:31 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 17:10:31 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.101s CPU time.
Aug 24 17:11:36 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 17:11:38 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 17:11:38 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 17:11:38 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.057s CPU time.
Aug 24 17:12:39 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 17:12:41 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 17:12:41 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 17:13:50 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 17:13:51 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 17:13:51 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 17:13:51 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.068s CPU time.
Aug 24 17:14:52 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 17:14:53 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 17:14:53 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 17:14:53 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.001s CPU time.
Aug 24 17:16:03 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
