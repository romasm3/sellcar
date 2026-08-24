# Serverio būklė

Sugeneruota: 2026-08-24 13:12:47 CEST

## Kodas

```
sukasi:      6c41a98 feat(antraštė): širdis su įsimintų skelbimų skaitikliu ir telefone
origin/master: 6c41a98 feat(antraštė): širdis su įsimintų skelbimų skaitikliu ir telefone
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M templates/listings/advanced_generic.html
   M templates/listings/partials/_adv_rail.html
   M templates/listings/partials/_sp_field_styles.html
   M templates/listings/partials/fields/_mobile_rows.html
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
HTTP 301, 0.001100s
```

## Skelbimų būsenos

```

Listing — iš viso 35
  active        23   MATOMAS
  draft          9   nematomas
  expired        3   nematomas
  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─
  nematomi dėl būsenos:      12
  iš jų pasibaigę (expires_at praeityje): 3
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
/dev/sda1       291G   15G  277G   5% /
```

## Paskutinis auto-deploy

```
Aug 24 13:04:46 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 13:04:48 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 13:04:48 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 13:05:53 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 13:05:54 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 13:05:54 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 13:07:05 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 13:07:07 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 13:07:07 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 13:08:15 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 13:08:17 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 13:08:17 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 13:08:17 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.004s CPU time.
Aug 24 13:09:24 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 13:09:25 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 13:09:25 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 13:10:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 13:10:31 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 13:10:31 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 13:10:31 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.007s CPU time.
Aug 24 13:11:39 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 13:11:41 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 13:11:41 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 13:11:41 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.068s CPU time.
Aug 24 13:12:46 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
