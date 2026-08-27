# Serverio būklė

Sugeneruota: 2026-08-27 13:37:40 CEST

## Kodas

```
sukasi:      ba229ad chore(antraštė): kompaktiška paieška išjungiama vienu jungikliu
origin/master: ba229ad chore(antraštė): kompaktiška paieška išjungiama vienu jungikliu
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/listings/views.py
   M apps/listings/zemelapio_views.py
   M static/js/zemelapio_paieska.js
   M templates/listings/partials/_zemelapio_filtrai.html
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
HTTP 301, 0.001088s
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
/dev/sda1       291G   18G  273G   7% /
```

## Paskutinis auto-deploy

```
Aug 27 13:31:03 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 13:31:06 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 13:31:06 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 13:31:06 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.115s CPU time.
Aug 27 13:32:11 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 13:32:12 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 13:32:12 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 13:32:12 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.171s CPU time.
Aug 27 13:33:20 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 13:33:22 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 13:33:22 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 13:33:22 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.085s CPU time.
Aug 27 13:34:26 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 13:34:28 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 13:34:28 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 13:34:28 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.051s CPU time.
Aug 27 13:35:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 13:35:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 13:35:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 13:35:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.073s CPU time.
Aug 27 13:36:31 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 13:36:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 13:36:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 13:36:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.021s CPU time.
Aug 27 13:37:40 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
