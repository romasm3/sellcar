# Serverio būklė

Sugeneruota: 2026-08-23 17:59:09 CEST

## Kodas

```
sukasi:      d1902a3 style(paieska): kategorijų juosta ir „Daugiau" sąrašas pagal etaloną
origin/master: d1902a3 style(paieska): kategorijų juosta ir „Daugiau" sąrašas pagal etaloną
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/listings/search_config/isplestine-config.json
   M apps/listings/search_config/panels.py
   M apps/listings/views.py
   M locale/en/LC_MESSAGES/django.mo
   M locale/en/LC_MESSAGES/django.po
   M templates/listings/advanced_generic.html
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
HTTP 301, 0.001043s
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
Aug 23 17:50:46 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 17:51:56 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 17:51:58 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 17:51:58 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 17:51:58 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.027s CPU time.
Aug 23 17:53:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 17:53:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 17:53:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 17:53:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.100s CPU time.
Aug 23 17:54:48 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 17:54:49 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 17:54:49 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 17:55:55 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 17:55:57 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 17:55:57 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 17:55:57 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.217s CPU time.
Aug 23 17:56:58 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 17:56:59 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 17:56:59 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 17:56:59 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.018s CPU time.
Aug 23 17:58:07 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 17:58:08 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 17:58:08 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 17:58:08 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.051s CPU time.
Aug 23 17:59:09 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
