# Serverio būklė

Sugeneruota: 2026-08-24 14:23:10 CEST

## Kodas

```
sukasi:      2531ff1 feat(prekės ženklas): naujas logotipas „Autoleft." ir ikona vietoj AL kvadrato
origin/master: 2531ff1 feat(prekės ženklas): naujas logotipas „Autoleft." ir ikona vietoj AL kvadrato
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/listings/urls.py
   M templates/base.html
   M templates/listings/listing_list.html
   M templates/partials/secondary_nav.html
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
HTTP 301, 0.202964s
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
Aug 24 14:14:51 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 14:15:58 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 14:15:59 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 14:15:59 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 14:17:19 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 14:17:21 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 14:17:21 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 14:17:21 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.245s CPU time.
Aug 24 14:18:27 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 14:18:28 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 14:18:28 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 14:18:28 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.084s CPU time.
Aug 24 14:19:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 14:19:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 14:19:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 14:19:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.180s CPU time.
Aug 24 14:20:46 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 14:20:48 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 14:20:48 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 14:20:48 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.049s CPU time.
Aug 24 14:21:49 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 14:21:51 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 14:21:51 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 14:21:51 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.019s CPU time.
Aug 24 14:23:10 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
