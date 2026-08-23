# Serverio būklė

Sugeneruota: 2026-08-23 17:11:20 CEST

## Kodas

```
sukasi:      39917e7 feat(paieska): Ratlankiai ir Padangos — dvi atskiros naršymo kategorijos
origin/master: 39917e7 feat(paieska): Ratlankiai ir Padangos — dvi atskiros naršymo kategorijos
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
HTTP 301, 0.001023s
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
Aug 23 17:02:59 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 17:03:00 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 17:03:00 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 17:04:03 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 17:04:04 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 17:04:04 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 17:04:04 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.143s CPU time.
Aug 23 17:05:11 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 17:05:12 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 17:05:12 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 17:06:15 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 17:06:16 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 17:06:16 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 17:06:16 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.019s CPU time.
Aug 23 17:07:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 17:07:31 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 17:07:31 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 17:08:46 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 17:08:47 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 17:08:47 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 17:08:47 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.039s CPU time.
Aug 23 17:10:09 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 17:10:11 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 17:10:11 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 17:11:19 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
