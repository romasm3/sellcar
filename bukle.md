# Serverio būklė

Sugeneruota: 2026-08-24 14:36:14 CEST

## Kodas

```
sukasi:      7139063 chore(ženklas): --brand-paper, .site-logo stiliai ir dokumento papildymas
origin/master: 7139063 chore(ženklas): --brand-paper, .site-logo stiliai ir dokumento papildymas
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M docs/dizaino-sistema.md
   M static/img/logo/autoleft-16.png
   M static/img/logo/autoleft-180.png
   M static/img/logo/autoleft-192.png
   M static/img/logo/autoleft-32.png
   M static/img/logo/autoleft-512.png
   M static/img/logo/autoleft-ikona.svg
   M templates/500.html
   M templates/base.html
   M templates/emails/base_email.html
   M templates/emails/draft_reminder_daily.html
   M templates/emails/draft_reminder_first.html
   M templates/listings/emails/expired.html
   M templates/listings/emails/expiring_soon.html
```

## Servisai

```
gunicorn                 deactivating
nginx                    active
postgresql               active
autoleft-deploy.timer    active
```

## Ar svetainė atsako

```
HTTP 301, 0.848668s
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
Aug 24 14:27:56 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 14:27:57 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 14:27:57 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 14:29:24 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 14:29:25 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 14:29:25 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 14:30:27 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 14:30:29 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 14:30:29 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 14:30:29 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.080s CPU time.
Aug 24 14:31:46 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 14:31:48 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 14:31:48 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 14:32:50 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 14:32:52 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 14:32:52 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 14:32:52 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.098s CPU time.
Aug 24 14:33:54 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 14:33:55 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 14:33:55 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 14:35:00 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 14:35:02 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 14:35:02 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 14:35:02 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.332s CPU time.
Aug 24 14:36:14 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
