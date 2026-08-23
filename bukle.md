# Serverio būklė

Sugeneruota: 2026-08-23 17:34:59 CEST

## Kodas

```
sukasi:      5b8bce5 feat(paieska): detali paieška pagal etaloną — ikonų juosta, antraštė, lipnus „Ieškoti"
origin/master: 5b8bce5 feat(paieska): detali paieška pagal etaloną — ikonų juosta, antraštė, lipnus „Ieškoti"
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/listings/search_config/panels.py
   M apps/listings/views.py
   M locale/en/LC_MESSAGES/django.mo
   M locale/en/LC_MESSAGES/django.po
   M templates/listings/advanced_generic.html
   M templates/listings/partials/_adv_rail.html
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
HTTP 301, 0.002128s
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
Aug 23 17:27:07 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 17:27:07 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.031s CPU time.
Aug 23 17:28:13 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 17:28:14 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 17:28:14 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 17:28:14 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.182s CPU time.
Aug 23 17:29:14 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 17:29:16 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 17:29:16 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 17:29:16 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.187s CPU time.
Aug 23 17:30:24 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 17:30:25 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 17:30:25 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 17:30:25 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.026s CPU time.
Aug 23 17:31:36 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 17:31:37 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 17:31:37 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 17:31:37 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.020s CPU time.
Aug 23 17:32:37 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 17:32:38 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 17:32:38 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 17:33:47 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 17:33:48 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 17:33:48 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 17:34:59 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
