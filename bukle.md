# Serverio būklė

Sugeneruota: 2026-08-24 11:17:16 CEST

## Kodas

```
sukasi:      5eae698 fix(skelbimas): matmenų perskaičiavimas rodomas vieną kartą
origin/master: 5eae698 fix(skelbimas): matmenų perskaičiavimas rodomas vieną kartą
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/listings/views.py
   M locale/en/LC_MESSAGES/django.mo
   M locale/en/LC_MESSAGES/django.po
   M templates/listings/listing_list.html
   M templates/listings/motorcycles_list.html
   M templates/listings/partials/sidebar_generic.html
   M templates/listings/wheels_list.html
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
HTTP 301, 0.001067s
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
Aug 24 11:08:48 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.040s CPU time.
Aug 24 11:09:55 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 11:09:57 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 11:09:57 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 11:09:57 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.077s CPU time.
Aug 24 11:11:16 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 11:11:18 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 11:11:18 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 11:11:18 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.078s CPU time.
Aug 24 11:12:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 11:12:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 11:12:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 11:12:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.172s CPU time.
Aug 24 11:13:39 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 11:13:41 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 11:13:41 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 11:13:41 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.088s CPU time.
Aug 24 11:14:46 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 11:14:47 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 11:14:47 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 11:15:46 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 11:15:48 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 11:15:48 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 11:15:48 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.118s CPU time.
Aug 24 11:17:16 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
