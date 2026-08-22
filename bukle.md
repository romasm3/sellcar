# Serverio būklė

Sugeneruota: 2026-08-22 22:44:32 CEST

## Kodas

```
sukasi:      143fa15 Merge remote-tracking branch 'origin/master'
origin/master: 143fa15 Merge remote-tracking branch 'origin/master'
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/listings/email_settings.py
   M apps/listings/management/commands/send_daily_emails.py
   M apps/listings/views.py
   M templates/emails/listing_views_milestone.txt
   M templates/emails/listing_views_milestone_subject.txt
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
HTTP 301, 0.001090s
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
  aktyvūs, baigsis per 7 d.: 1
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
/dev/sda1       291G   14G  278G   5% /
```

## Paskutinis auto-deploy

```
Aug 22 22:35:53 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 22 22:36:58 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 22 22:36:59 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 22 22:36:59 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 22 22:38:03 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 22 22:38:04 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 22 22:38:04 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 22 22:39:08 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 22 22:39:09 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 22 22:39:09 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 22 22:39:09 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.018s CPU time.
Aug 22 22:40:15 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 22 22:40:16 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 22 22:40:16 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 22 22:40:16 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.206s CPU time.
Aug 22 22:41:20 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 22 22:41:21 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 22 22:41:21 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 22 22:42:23 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 22 22:42:24 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 22 22:42:24 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 22 22:43:27 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 22 22:43:29 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 22 22:43:29 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 22 22:44:32 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
