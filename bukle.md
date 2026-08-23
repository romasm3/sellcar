# Serverio būklė

Sugeneruota: 2026-08-23 16:30:12 CEST

## Kodas

```
sukasi:      62c5b05 fix(paieska): „Detali paieška" telefone — laukai su reikšmių ekranais
origin/master: 62c5b05 fix(paieska): „Detali paieška" telefone — laukai su reikšmių ekranais
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/listings/motogear_views.py
   M apps/listings/search_config/panels.py
   M locale/en/LC_MESSAGES/django.mo
   M locale/en/LC_MESSAGES/django.po
   M templates/listings/motogear_list.html
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
HTTP 301, 0.001627s
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
/dev/sda1       291G   14G  277G   5% /
```

## Paskutinis auto-deploy

```
Aug 23 16:20:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 16:20:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.156s CPU time.
Aug 23 16:21:44 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 16:21:46 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 16:21:46 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 16:23:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 16:23:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 16:23:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 16:24:43 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 16:24:45 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 16:24:45 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 16:25:49 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 16:25:51 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 16:25:51 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 16:26:53 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 16:26:55 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 16:26:55 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 16:28:03 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 16:28:05 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 16:28:05 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 16:28:05 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.173s CPU time.
Aug 23 16:29:10 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 16:29:12 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 16:29:12 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 16:30:12 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
