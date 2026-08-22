# Serverio būklė

Sugeneruota: 2026-08-22 23:28:36 CEST

## Kodas

```
sukasi:      1b4e63d feat(laiskai): HTML rėmas svarbiausiems laiškams + trūkę šablonai
origin/master: 1b4e63d feat(laiskai): HTML rėmas svarbiausiems laiškams + trūkę šablonai
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M templates/listings/advanced_generic.html
   M templates/listings/partials/_sp_field_styles.html
   M templates/listings/partials/fields/_brand.html
   M templates/listings/partials/fields/_model.html
   M templates/listings/partials/panel_moto.html
   M templates/listings/select_value.html
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
HTTP 301, 0.001138s
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
  aktyvūs, baigsis per 7 d.: 1
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
/dev/sda1       291G   14G  278G   5% /
```

## Paskutinis auto-deploy

```
Aug 22 23:20:07 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.073s CPU time.
Aug 22 23:21:14 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 22 23:21:16 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 22 23:21:16 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 22 23:21:16 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.019s CPU time.
Aug 22 23:22:15 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 22 23:22:17 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 22 23:22:17 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 22 23:23:22 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 22 23:23:24 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 22 23:23:24 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 22 23:24:25 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 22 23:24:26 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 22 23:24:26 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 22 23:25:26 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 22 23:25:28 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 22 23:25:28 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 22 23:25:28 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.257s CPU time.
Aug 22 23:26:27 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 22 23:26:28 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 22 23:26:28 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 22 23:27:29 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 22 23:27:30 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 22 23:27:30 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 22 23:28:36 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
