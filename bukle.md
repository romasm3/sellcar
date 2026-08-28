# Serverio būklė

Sugeneruota: 2026-08-28 11:23:23 CEST

## Kodas

```
sukasi:      25d3cbf feat(įmonės): trys bandomosios įmonės su viena komanda
origin/master: 25d3cbf feat(įmonės): trys bandomosios įmonės su viena komanda
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/listings/context_processors.py
   M apps/listings/views.py
   M templates/base.html
   M templates/listings/listing_list.html
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
HTTP 301, 0.002405s
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
/dev/sda1       291G   19G  272G   7% /
```

## Paskutinis auto-deploy

```
Aug 28 11:14:55 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 28 11:14:57 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 28 11:14:57 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 28 11:14:57 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.577s CPU time.
Aug 28 11:16:24 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 28 11:16:26 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 28 11:16:26 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 28 11:16:26 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.449s CPU time.
Aug 28 11:17:58 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 28 11:18:06 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 28 11:18:06 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 28 11:18:06 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 3.076s CPU time.
Aug 28 11:19:15 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 28 11:19:17 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 28 11:19:17 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 28 11:19:17 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.501s CPU time.
Aug 28 11:20:25 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 28 11:20:27 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 28 11:20:27 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 28 11:20:27 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.662s CPU time.
Aug 28 11:21:41 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 28 11:21:43 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 28 11:21:43 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 28 11:21:43 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.674s CPU time.
Aug 28 11:23:22 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
