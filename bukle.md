# Serverio būklė

Sugeneruota: 2026-08-27 13:02:01 CEST

## Kodas

```
sukasi:      0736ac3 feat(žemėlapis): kainų žymekliai, kortelė virš žymeklio ir apatinis lapas
origin/master: 0736ac3 feat(žemėlapis): kainų žymekliai, kortelė virš žymeklio ir apatinis lapas
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/listings/brand_api.py
   M apps/listings/context_processors.py
   M config/settings.py
   M templates/base.html
   M templates/listings/search_map.html
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
HTTP 301, 0.001597s
```

## Skelbimų būsenos

```

Listing — iš viso 35
  active        22   MATOMAS
  draft          9   nematomas
  expired        4   nematomas
  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─
  nematomi dėl būsenos:      13
  iš jų pasibaigę (expires_at praeityje): 4
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
/dev/sda1       291G   18G  274G   6% /
```

## Paskutinis auto-deploy

```
Aug 27 12:53:40 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 12:53:40 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 12:54:52 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 12:54:54 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 12:54:54 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 12:56:02 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 12:56:04 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 12:56:04 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 12:56:04 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.218s CPU time.
Aug 27 12:57:08 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 12:57:10 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 12:57:10 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 12:57:10 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.058s CPU time.
Aug 27 12:58:23 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 12:58:25 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 12:58:25 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 12:58:25 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.099s CPU time.
Aug 27 12:59:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 12:59:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 12:59:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 13:00:44 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 13:00:46 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 13:00:46 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 13:00:46 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.319s CPU time.
Aug 27 13:02:01 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
