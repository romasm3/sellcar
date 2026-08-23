# Serverio būklė

Sugeneruota: 2026-08-23 17:18:30 CEST

## Kodas

```
sukasi:      39917e7 feat(paieska): Ratlankiai ir Padangos — dvi atskiros naršymo kategorijos
origin/master: 39917e7 feat(paieska): Ratlankiai ir Padangos — dvi atskiros naršymo kategorijos
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/listings/search_config/isplestine-config.json
   M apps/listings/search_config/panels.py
   M apps/listings/templatetags/dict_extras.py
   M apps/listings/views.py
   M locale/en/LC_MESSAGES/django.mo
   M locale/en/LC_MESSAGES/django.po
   M templates/listings/advanced_generic.html
   M templates/listings/partials/fields/_brand.html
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
HTTP 301, 0.477842s
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
Aug 23 17:10:09 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 17:10:11 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 17:10:11 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 17:11:19 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 17:11:21 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 17:11:21 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 17:12:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 17:12:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 17:12:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 17:13:32 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 17:13:34 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 17:13:34 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 17:15:01 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 17:15:03 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 17:15:03 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 17:15:03 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.369s CPU time.
Aug 23 17:16:15 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 17:16:16 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 17:16:16 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 17:16:16 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.022s CPU time.
Aug 23 17:17:18 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 17:17:20 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 17:17:20 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 17:17:20 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.041s CPU time.
Aug 23 17:18:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
