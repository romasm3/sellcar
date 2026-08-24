# Serverio būklė

Sugeneruota: 2026-08-24 13:26:07 CEST

## Kodas

```
sukasi:      7f1fa5f fix(detali paieška): telefone juostoje tik ikonos, markės eilutė su pavadinimu
origin/master: 7f1fa5f fix(detali paieška): telefone juostoje tik ikonos, markės eilutė su pavadinimu
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/listings/models.py
   M apps/listings/urls.py
   M apps/listings/views.py
   M locale/en/LC_MESSAGES/django.mo
   M locale/en/LC_MESSAGES/django.po
   M templates/base.html
   M templates/listings/listing_detail.html
   M templates/listings/listing_list.html
   M templates/listings/moto_parts_browse.html
   M templates/listings/motorcycles_list.html
   M templates/listings/truck_parts_browse.html
   M templates/listings/trucks_list.html
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
HTTP 301, 0.002191s
```

## Skelbimų būsenos

```

Listing — iš viso 35
  active        23   MATOMAS
  draft          9   nematomas
  expired        3   nematomas
  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─
  nematomi dėl būsenos:      12
  iš jų pasibaigę (expires_at praeityje): 3
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
/dev/sda1       291G   15G  277G   5% /
```

## Paskutinis auto-deploy

```
Aug 24 13:17:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 13:17:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 13:17:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 13:17:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.017s CPU time.
Aug 24 13:18:46 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 13:18:48 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 13:18:48 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 13:19:55 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 13:19:57 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 13:19:57 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 13:19:57 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.028s CPU time.
Aug 24 13:21:24 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 13:21:25 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 13:21:25 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 13:22:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 13:22:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 13:22:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 13:22:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.151s CPU time.
Aug 24 13:23:46 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 13:23:49 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 13:23:49 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 13:24:57 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 13:24:58 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 13:24:58 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 13:26:07 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
