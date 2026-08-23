# Serverio būklė

Sugeneruota: 2026-08-23 13:43:09 CEST

## Kodas

```
sukasi:      55cc9dd feat(i18n): ETAPAS 3 - vartotojo zona angliskai
origin/master: 55cc9dd feat(i18n): ETAPAS 3 - vartotojo zona angliskai
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/listings/parts_views.py
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
HTTP 301, 0.001172s
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
  aktyvūs, baigsis per 7 d.: 3
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
/dev/sda1       291G   14G  277G   5% /
```

## Paskutinis auto-deploy

```
Aug 23 13:34:03 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 13:34:05 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 13:34:05 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 13:35:25 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 13:35:27 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 13:35:27 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 13:35:27 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.040s CPU time.
Aug 23 13:36:50 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 13:36:51 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 13:36:51 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 13:38:00 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 13:38:02 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 13:38:02 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 13:38:02 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.392s CPU time.
Aug 23 13:39:14 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 13:39:16 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 13:39:16 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 13:40:29 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 13:40:30 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 13:40:30 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 13:41:55 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 13:41:56 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 13:41:56 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 13:41:57 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.043s CPU time.
Aug 23 13:43:08 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
