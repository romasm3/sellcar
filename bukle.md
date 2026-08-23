# Serverio būklė

Sugeneruota: 2026-08-23 11:43:21 CEST

## Kodas

```
sukasi:      d772aef feat(i18n): EN vertimai automobilio formai — Autogidas žodynas, UK rašyba
origin/master: d772aef feat(i18n): EN vertimai automobilio formai — Autogidas žodynas, UK rašyba
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/listings/admin.py
   M apps/listings/models.py
   M apps/listings/urls.py
   M apps/listings/views.py
   M templates/listings/listing_detail.html
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
HTTP 301, 0.003760s
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
  aktyvūs, baigsis per 7 d.: 2
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
/dev/sda1       291G   14G  277G   5% /
```

## Paskutinis auto-deploy

```
Aug 23 11:33:34 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 11:34:57 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 11:34:58 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 11:34:58 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 11:36:08 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 11:36:09 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 11:36:09 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 11:37:28 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 11:37:30 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 11:37:30 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 11:38:32 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 11:38:34 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 11:38:34 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 11:39:48 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 11:39:49 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 11:39:49 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 11:39:49 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.028s CPU time.
Aug 23 11:40:56 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 11:40:58 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 11:40:58 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 11:40:58 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.026s CPU time.
Aug 23 11:42:14 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 11:42:16 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 11:42:16 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 11:43:21 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
