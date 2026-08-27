# Serverio būklė

Sugeneruota: 2026-08-27 17:08:59 CEST

## Kodas

```
sukasi:      9b42948 feat(žemėlapis): kategorijos iš juostos šaltinio, su skaičiais, kartu ir ratai
origin/master: 9b42948 feat(žemėlapis): kategorijos iš juostos šaltinio, su skaičiais, kartu ir ratai
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/listings/zemelapio_views.py
   M static/js/zemelapio_paieska.js
   M templates/listings/partials/_skelbimo_kortele.html
   M templates/listings/partials/_zemelapio_aikstele.html
   M templates/listings/partials/_zemelapio_burbulas.html
   M templates/listings/partials/_zemelapio_sarasas.html
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
HTTP 301, 0.001318s
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
Aug 27 17:01:23 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 17:01:23 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.062s CPU time.
Aug 27 17:02:28 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 17:02:30 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 17:02:30 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 17:02:30 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.182s CPU time.
Aug 27 17:03:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 17:03:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 17:03:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 17:03:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.044s CPU time.
Aug 27 17:04:38 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 17:04:40 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 17:04:40 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 17:05:43 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 17:05:45 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 17:05:45 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 17:05:45 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.076s CPU time.
Aug 27 17:06:44 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 17:06:46 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 17:06:46 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 17:07:54 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 17:07:56 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 17:07:56 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 17:07:56 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.014s CPU time.
Aug 27 17:08:59 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
