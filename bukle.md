# Serverio būklė

Sugeneruota: 2026-08-28 12:13:32 CEST

## Kodas

```
sukasi:      1388b71 feat(pradžia): viena paieškos juosta viršuje, vedanti į skelbimus su žemėlapiu
origin/master: 1388b71 feat(pradžia): viena paieškos juosta viršuje, vedanti į skelbimus su žemėlapiu
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/listings/urls.py
   M templates/listings/partials/_hero_paieska.html
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
HTTP 301, 0.001412s
```

## Skelbimų būsenos

```

Listing — iš viso 35
  active        22   MATOMAS
  draft          9   nematomas
  expired        4   nematomas
  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─
  nematomi dėl būsenos:      13
  iš jų pasibaigę (expires_at praeityje): 4
  aktyvūs, baigsis per 7 d.: 4
  aktyvūs be pabaigos datos: 8 (pvz. testiniai)
Truck: skelbimų nėra.
WheelListing: skelbimų nėra.

Viešame sąraše matomi tik status="active" (+ neseniai parduoti).
Jei tavo seni skelbimai yra "expired" — juos reikia aktyvuoti iš naujo,
o ne taisyti kode.
```

## Vietos diske

```
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       291G   19G  272G   7% /
```

## Paskutinis auto-deploy

```
Aug 28 12:06:24 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 28 12:06:25 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 28 12:06:25 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 28 12:06:25 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.297s CPU time.
Aug 28 12:07:40 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 28 12:07:42 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 28 12:07:42 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 28 12:07:42 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.430s CPU time.
Aug 28 12:08:48 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 28 12:08:50 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 28 12:08:50 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 28 12:08:50 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.221s CPU time.
Aug 28 12:10:01 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 28 12:10:06 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 28 12:10:06 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 28 12:10:06 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 2.552s CPU time.
Aug 28 12:11:19 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 28 12:11:21 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 28 12:11:21 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 28 12:11:21 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.421s CPU time.
Aug 28 12:12:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 28 12:12:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 28 12:12:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 28 12:12:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.380s CPU time.
Aug 28 12:13:32 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
