# Serverio būklė

Sugeneruota: 2026-08-23 13:48:01 CEST

## Kodas

```
sukasi:      55cc9dd feat(i18n): ETAPAS 3 - vartotojo zona angliskai
origin/master: 55cc9dd feat(i18n): ETAPAS 3 - vartotojo zona angliskai
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/accounts/views.py
   M apps/listings/listing_helpers.py
   M apps/listings/management/commands/send_daily_emails.py
   M apps/listings/management/commands/send_expiring_soon.py
   M apps/listings/management/commands/send_expiry_reminders.py
   M apps/listings/models.py
   M apps/listings/parts_views.py
   M apps/listings/views.py
   M locale/en/LC_MESSAGES/django.mo
   M locale/en/LC_MESSAGES/django.po
   M templates/emails/listing_expiring_soon.txt
   M templates/listings/listing_edit_hub.html
   M templates/listings/listing_edit_hubb.html
   M templates/listings/listing_select_plan.html
   M templates/listings/my_listings.html
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
HTTP 301, 0.001326s
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
Aug 23 13:39:14 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 13:39:16 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 13:39:16 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 13:40:29 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 13:40:30 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 13:40:30 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 13:41:55 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 13:41:56 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 13:41:56 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 13:41:57 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.043s CPU time.
Aug 23 13:43:08 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 13:43:10 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 13:43:10 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 13:43:10 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.070s CPU time.
Aug 23 13:44:18 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 13:44:19 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 13:44:19 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 13:45:23 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 13:45:25 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 13:45:25 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 13:45:25 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.062s CPU time.
Aug 23 13:46:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 13:46:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 13:46:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 13:48:00 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
