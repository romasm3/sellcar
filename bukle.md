# Serverio būklė

Sugeneruota: 2026-08-25 17:26:24 CEST

## Kodas

```
sukasi:      459ed58 fix(pikeris): tinklelis iš grid pakeistas į flex
origin/master: 459ed58 fix(pikeris): tinklelis iš grid pakeistas į flex
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/listings/urls.py
   M apps/listings/views_help.py
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
HTTP 301, 0.001481s
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
/dev/sda1       291G   16G  276G   6% /
```

## Paskutinis auto-deploy

```
Aug 25 17:19:29 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 25 17:19:31 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 25 17:19:31 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 25 17:19:31 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.185s CPU time.
Aug 25 17:20:40 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 25 17:20:44 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 25 17:20:44 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 25 17:20:44 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.339s CPU time.
Aug 25 17:21:49 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 25 17:21:51 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 25 17:21:51 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 25 17:21:51 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.137s CPU time.
Aug 25 17:22:56 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 25 17:22:58 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 25 17:22:58 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 25 17:22:58 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.053s CPU time.
Aug 25 17:24:06 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 25 17:24:08 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 25 17:24:08 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 25 17:24:08 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.209s CPU time.
Aug 25 17:25:15 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 25 17:25:17 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 25 17:25:17 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 25 17:25:17 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.438s CPU time.
Aug 25 17:26:24 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
