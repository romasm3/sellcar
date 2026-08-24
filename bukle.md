# Serverio būklė

Sugeneruota: 2026-08-24 14:43:04 CEST

## Kodas

```
sukasi:      d6b36fd chore(ženklas): naujos spalvos #181B1F / #E14D28 ir logotipo geometrija
origin/master: d6b36fd chore(ženklas): naujos spalvos #181B1F / #E14D28 ir logotipo geometrija
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/listings/management/commands/send_expiry_reminders.py
   D static/fonts/eb-garamond-400-latin-ext.woff2
   D static/fonts/eb-garamond-400-latin.woff2
   D static/img/logo/autoleft-16.png
   D static/img/logo/autoleft-180.png
   D static/img/logo/autoleft-192.png
   D static/img/logo/autoleft-32.png
   D static/img/logo/autoleft-512.png
   D static/img/logo/autoleft-ikona.svg
   M templates/404.html
   M templates/500.html
   M templates/accounts/login.html
   M templates/accounts/password_reset_complete.html
   M templates/accounts/password_reset_confirm.html
   M templates/accounts/register.html
   M templates/base.html
   M templates/emails/base_email.html
   M templates/emails/draft_reminder_daily.html
   M templates/emails/draft_reminder_first.html
   M templates/listings/emails/expired.html
   M templates/listings/emails/expiring_soon.html
   M templates/listings/trucks_listing_edit
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
HTTP 301, 0.001536s
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
Aug 24 14:35:02 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 14:35:02 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.332s CPU time.
Aug 24 14:36:14 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 14:36:16 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 14:36:16 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 14:37:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 14:37:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 14:37:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 14:37:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.018s CPU time.
Aug 24 14:38:37 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 14:38:39 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 14:38:39 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 14:38:39 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.032s CPU time.
Aug 24 14:39:46 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 14:39:48 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 14:39:48 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 14:40:54 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 14:40:55 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 14:40:55 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 14:40:55 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.161s CPU time.
Aug 24 14:41:59 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 14:42:00 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 14:42:00 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 14:42:00 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.101s CPU time.
Aug 24 14:43:03 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
