# Serverio būklė

Sugeneruota: 2026-08-23 20:40:13 CEST

## Kodas

```
sukasi:      c8349dd feat(saugumas): apsauga nuo botų registracijos ir slaptažodžių spėliojimo
origin/master: c8349dd feat(saugumas): apsauga nuo botų registracijos ir slaptažodžių spėliojimo
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M templates/listings/listing_detail.html
   M templates/listings/partials/_lightbox.html
   M templates/listings/wheels_detail.html
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
HTTP 301, 0.001179s
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
Aug 23 20:32:19 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 20:32:21 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 20:32:21 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 20:33:27 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 20:33:28 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 20:33:28 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 20:33:28 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.030s CPU time.
Aug 23 20:34:38 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 20:34:39 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 20:34:39 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 20:35:41 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 20:35:43 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 20:35:43 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 20:35:43 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.061s CPU time.
Aug 23 20:36:48 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 20:36:50 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 20:36:50 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 20:37:56 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 20:37:58 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 20:37:58 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 20:39:03 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 20:39:05 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 20:39:05 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 20:39:05 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.362s CPU time.
Aug 23 20:40:12 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
