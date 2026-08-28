# Serverio būklė

Sugeneruota: 2026-08-28 12:29:08 CEST

## Kodas

```
sukasi:      e3859b0 feat(pradžia): paieškos juosta su sugrupuotu iškrentančiu sąrašu
origin/master: e3859b0 feat(pradžia): paieškos juosta su sugrupuotu iškrentančiu sąrašu
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/imones/views.py
  RM static/js/hero_paieska.js -> static/js/paieskos_juosta.js
   M templates/imones/_stiliai.html
   M templates/imones/sarasas.html
   M templates/listings/listing_list.html
  RM templates/listings/partials/_hero_paieska.html -> templates/partials/_paieskos_juosta.html
  R  templates/listings/partials/_hero_stiliai.html -> templates/partials/_paieskos_juosta_stiliai.html
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
HTTP 301, 0.001210s
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
Aug 28 12:22:05 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 28 12:22:07 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 28 12:22:07 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 28 12:22:07 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.372s CPU time.
Aug 28 12:23:17 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 28 12:23:18 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 28 12:23:18 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 28 12:23:18 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.308s CPU time.
Aug 28 12:24:25 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 28 12:24:27 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 28 12:24:27 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 28 12:24:27 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.173s CPU time.
Aug 28 12:25:52 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 28 12:25:54 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 28 12:25:54 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 28 12:25:54 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.375s CPU time.
Aug 28 12:26:58 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 28 12:26:59 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 28 12:26:59 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 28 12:26:59 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.224s CPU time.
Aug 28 12:28:05 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 28 12:28:07 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 28 12:28:07 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 28 12:28:07 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.451s CPU time.
Aug 28 12:29:08 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
