# Serverio būklė

Sugeneruota: 2026-08-30 20:38:53 CEST

## Kodas

```
sukasi:      c853bdf feat(įmonės): meistrai (Specialistai) — naujas tipas ir veikiantis perjungiklis
origin/master: c853bdf feat(įmonės): meistrai (Specialistai) — naujas tipas ir veikiantis perjungiklis
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/accounts/middleware.py
   M apps/imones/models.py
   M apps/imones/views.py
   M apps/listings/formatai.py
   M config/settings.py
   M config/urls.py
   M static/js/imones_fresha.js
   M templates/base.html
   M templates/imones/_fresha_stiliai.html
   M templates/imones/sarasas.html
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
HTTP 301, 0.001630s
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
  aktyvūs, baigsis per 7 d.: 3
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
/dev/sda1       291G   22G  270G   8% /
```

## Paskutinis auto-deploy

```
Aug 30 20:31:24 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 30 20:31:26 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 30 20:31:26 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 30 20:31:26 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.332s CPU time.
Aug 30 20:32:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 30 20:32:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 30 20:32:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 30 20:32:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.276s CPU time.
Aug 30 20:33:47 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 30 20:33:49 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 30 20:33:49 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 30 20:33:49 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.476s CPU time.
Aug 30 20:34:53 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 30 20:34:55 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 30 20:34:55 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 30 20:34:55 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.281s CPU time.
Aug 30 20:36:05 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 30 20:36:06 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 30 20:36:06 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 30 20:36:06 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.381s CPU time.
Aug 30 20:37:29 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 30 20:37:31 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 30 20:37:31 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 30 20:37:31 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.407s CPU time.
Aug 30 20:38:53 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
