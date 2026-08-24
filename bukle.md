# Serverio būklė

Sugeneruota: 2026-08-24 16:46:10 CEST

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
HTTP 301, 0.001024s
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
Aug 24 16:37:30 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 16:38:42 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 16:38:44 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 16:38:44 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 16:39:52 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 16:39:54 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 16:39:54 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 16:39:54 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.023s CPU time.
Aug 24 16:41:17 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 16:41:18 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 16:41:18 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 16:41:18 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.072s CPU time.
Aug 24 16:42:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 16:42:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 16:42:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 16:42:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.026s CPU time.
Aug 24 16:43:36 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 16:43:38 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 16:43:38 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 16:43:38 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.061s CPU time.
Aug 24 16:44:58 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 16:44:59 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 16:44:59 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 16:44:59 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.038s CPU time.
Aug 24 16:46:10 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
