# Serverio būklė

Sugeneruota: 2026-08-30 21:17:31 CEST

## Kodas

```
sukasi:      8dd8851 feat(vertimai): lt/en per i18n_patterns, įmonių puslapiai išversti, sargybos testai
origin/master: 8dd8851 feat(vertimai): lt/en per i18n_patterns, įmonių puslapiai išversti, sargybos testai
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/imones/views.py
   M apps/listings/geokodavimas.py
   M apps/listings/paieskos_siulymai.py
   M templates/imones/_fresha_stiliai.html
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
HTTP 301, 0.001637s
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
Aug 30 21:09:56 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 30 21:09:58 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 30 21:09:58 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 30 21:09:58 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.308s CPU time.
Aug 30 21:11:05 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 30 21:11:07 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 30 21:11:07 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 30 21:11:07 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.423s CPU time.
Aug 30 21:12:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 30 21:12:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 30 21:12:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 30 21:12:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.310s CPU time.
Aug 30 21:13:35 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 30 21:13:37 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 30 21:13:37 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 30 21:13:37 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.299s CPU time.
Aug 30 21:14:59 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 30 21:15:01 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 30 21:15:01 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 30 21:15:01 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.381s CPU time.
Aug 30 21:16:04 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 30 21:16:06 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 30 21:16:06 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 30 21:16:06 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.320s CPU time.
Aug 30 21:17:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
