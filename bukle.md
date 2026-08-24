# Serverio būklė

Sugeneruota: 2026-08-24 11:24:18 CEST

## Kodas

```
sukasi:      df1f877 feat(paieska): filtrai taikomi tik paspaudus „Filtruoti"
origin/master: df1f877 feat(paieska): filtrai taikomi tik paspaudus „Filtruoti"
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/listings/models.py
   M apps/listings/urls.py
   M apps/listings/views.py
   M locale/en/LC_MESSAGES/django.mo
   M locale/en/LC_MESSAGES/django.po
   M templates/listings/saved_listings.html
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
HTTP 301, 0.001217s
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
Aug 24 11:15:48 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.118s CPU time.
Aug 24 11:17:16 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 11:17:18 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 11:17:18 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 11:17:18 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.281s CPU time.
Aug 24 11:18:27 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 11:18:28 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 11:18:28 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 11:18:28 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.022s CPU time.
Aug 24 11:19:29 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 11:19:30 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 11:19:30 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 11:19:30 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.085s CPU time.
Aug 24 11:20:47 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 11:20:49 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 11:20:49 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 11:20:49 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.067s CPU time.
Aug 24 11:22:00 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 11:22:02 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 11:22:02 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 11:22:02 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.400s CPU time.
Aug 24 11:23:16 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 11:23:18 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 11:23:18 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 11:24:18 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
