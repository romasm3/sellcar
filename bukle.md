# Serverio būklė

Sugeneruota: 2026-08-23 17:55:56 CEST

## Kodas

```
sukasi:      d1902a3 style(paieska): kategorijų juosta ir „Daugiau" sąrašas pagal etaloną
origin/master: d1902a3 style(paieska): kategorijų juosta ir „Daugiau" sąrašas pagal etaloną
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/listings/search_config/isplestine-config.json
   M apps/listings/search_config/panels.py
   M apps/listings/views.py
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
HTTP 301, 0.002119s
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
Aug 23 17:47:05 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 17:47:07 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 17:47:07 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 17:48:11 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 17:48:12 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 17:48:12 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 17:48:12 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.144s CPU time.
Aug 23 17:49:27 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 17:49:29 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 17:49:29 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 17:50:45 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 17:50:46 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
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
```
