# Serverio būklė

Sugeneruota: 2026-08-30 21:32:31 CEST

## Kodas

```
sukasi:      8dd8851 feat(vertimai): lt/en per i18n_patterns, įmonių puslapiai išversti, sargybos testai
origin/master: 8dd8851 feat(vertimai): lt/en per i18n_patterns, įmonių puslapiai išversti, sargybos testai
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/imones/tests.py
   M apps/imones/views.py
   M apps/listings/geokodavimas.py
   M apps/listings/paieskos_siulymai.py
   M config/settings.py
   M locale/en/LC_MESSAGES/django.mo
   M locale/en/LC_MESSAGES/django.po
   M static/js/imones_fresha.js
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
HTTP 301, 0.001509s
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
/dev/sda1       291G   23G  268G   8% /
```

## Paskutinis auto-deploy

```
Aug 30 21:25:29 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 30 21:25:31 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 30 21:25:31 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 30 21:25:31 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.291s CPU time.
Aug 30 21:26:36 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 30 21:26:38 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 30 21:26:38 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 30 21:26:38 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.338s CPU time.
Aug 30 21:27:38 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 30 21:27:40 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 30 21:27:40 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 30 21:27:40 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.260s CPU time.
Aug 30 21:28:54 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 30 21:28:56 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 30 21:28:56 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 30 21:28:56 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.227s CPU time.
Aug 30 21:30:11 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 30 21:30:14 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 30 21:30:14 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 30 21:30:14 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.591s CPU time.
Aug 30 21:31:22 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 30 21:31:24 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 30 21:31:24 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 30 21:31:24 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.650s CPU time.
Aug 30 21:32:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
