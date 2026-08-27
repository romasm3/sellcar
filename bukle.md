# Serverio būklė

Sugeneruota: 2026-08-27 17:23:41 CEST

## Kodas

```
sukasi:      715a34c feat(žemėlapis): skelbimai naujame skirtuke, telefone — su grįžimu atgal
origin/master: 715a34c feat(žemėlapis): skelbimai naujame skirtuke, telefone — su grįžimu atgal
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/listings/agriculture_views.py
   M apps/listings/bicycles_views.py
   M apps/listings/boats_views.py
   M apps/listings/camping_views.py
   M apps/listings/construction_views.py
   M apps/listings/electronics_views.py
   M apps/listings/forestry_views.py
   M apps/listings/forms.py
   M apps/listings/loading_views.py
   M apps/listings/models.py
   M apps/listings/moto_part_views.py
   M apps/listings/rental_views.py
   M apps/listings/services_views.py
   M apps/listings/templatetags/contact_block_tags.py
   M apps/listings/trailers_views.py
   M apps/listings/truck_for_parts_views.py
   M apps/listings/truck_parts_views.py
   M apps/listings/trucks_views.py
   M static/js/contact_block.js
   M templates/listings/partials/_contact_select.html
   M templates/listings/partials/contact_block.html
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
HTTP 301, 0.001069s
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
/dev/sda1       291G   18G  273G   7% /
```

## Paskutinis auto-deploy

```
Aug 27 17:16:57 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 17:16:59 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 17:16:59 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 17:16:59 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.042s CPU time.
Aug 27 17:17:59 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 17:18:02 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 17:18:02 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 17:18:02 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.328s CPU time.
Aug 27 17:19:14 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 17:19:16 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 17:19:16 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 17:19:16 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.096s CPU time.
Aug 27 17:20:23 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 17:20:25 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 17:20:25 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 17:20:25 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.067s CPU time.
Aug 27 17:21:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 17:21:33 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 17:21:33 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 17:21:33 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.136s CPU time.
Aug 27 17:22:34 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 17:22:35 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 17:22:35 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 17:22:35 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.024s CPU time.
Aug 27 17:23:41 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
