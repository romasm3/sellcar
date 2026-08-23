# Serverio būklė

Sugeneruota: 2026-08-23 20:01:49 CEST

## Kodas

```
sukasi:      17ea135 fix(paieska): kelių markių mygtukas — tik detalioje paieškoje ir šoninėje juostoje
origin/master: 17ea135 fix(paieska): kelių markių mygtukas — tik detalioje paieškoje ir šoninėje juostoje
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/listings/search_config/panels.py
   M templates/listings/advanced_generic.html
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
HTTP 301, 0.002118s
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
  aktyvūs, baigsis per 7 d.: 4
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
/dev/sda1       291G   15G  277G   5% /
```

## Paskutinis auto-deploy

```
Aug 23 19:53:12 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 19:53:12 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.068s CPU time.
Aug 23 19:54:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 19:54:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 19:54:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 19:55:40 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 19:55:42 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 19:55:42 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 19:55:42 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.080s CPU time.
Aug 23 19:57:13 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 19:57:14 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 19:57:14 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 19:57:14 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.107s CPU time.
Aug 23 19:58:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 19:58:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 19:58:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 19:58:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.096s CPU time.
Aug 23 19:59:35 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 19:59:36 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 19:59:36 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 20:00:40 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 20:00:42 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 20:00:42 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 20:00:42 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.081s CPU time.
Aug 23 20:01:49 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
