# Serverio būklė

Sugeneruota: 2026-08-23 18:59:30 CEST

## Kodas

```
sukasi:      4d67933 feat(paieska): juostos punktams su keliomis paieškomis — iškrentantys sąrašai
origin/master: 4d67933 feat(paieska): juostos punktams su keliomis paieškomis — iškrentantys sąrašai
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/listings/search_config/panels.py
   M apps/listings/views.py
   M apps/listings/wheels_views.py
   M locale/en/LC_MESSAGES/django.mo
   M locale/en/LC_MESSAGES/django.po
   M templates/listings/partials/_adv_rail_ico.html
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
HTTP 301, 0.002498s
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
  aktyvūs, baigsis per 7 d.: 3
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
Aug 23 18:52:00 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 18:52:00 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 18:52:59 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 18:53:01 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 18:53:01 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 18:53:01 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.206s CPU time.
Aug 23 18:54:09 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 18:54:11 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 18:54:11 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 18:55:11 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 18:55:12 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 18:55:12 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 18:55:12 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.118s CPU time.
Aug 23 18:56:17 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 18:56:18 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 18:56:18 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 18:56:18 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.127s CPU time.
Aug 23 18:57:27 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 18:57:28 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 18:57:28 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 18:58:29 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 18:58:31 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 18:58:31 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 18:58:31 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.051s CPU time.
Aug 23 18:59:29 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
