# Serverio būklė

Sugeneruota: 2026-08-23 08:03:38 CEST

## Kodas

```
sukasi:      80644db feat(create): automobilio formos laukai pagal etaloną
origin/master: 80644db feat(create): automobilio formos laukai pagal etaloną
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M locale/lt/LC_MESSAGES/django.mo
   M locale/lt/LC_MESSAGES/django.po
   M templates/listings/listing_create.html
   M templates/listings/listing_create_cars_quick.html
   M templates/listings/listing_edit.html
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
HTTP 301, 0.001287s
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
  aktyvūs, baigsis per 7 d.: 2
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
Aug 23 07:54:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 07:54:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 07:55:57 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 07:55:58 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 07:55:58 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 07:55:58 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.098s CPU time.
Aug 23 07:57:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 07:57:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 07:57:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 07:57:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.000s CPU time.
Aug 23 07:58:44 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 07:58:45 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 07:58:45 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 07:59:55 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 07:59:57 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 07:59:57 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 07:59:57 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.255s CPU time.
Aug 23 08:01:06 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 08:01:08 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 08:01:08 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 08:01:08 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.271s CPU time.
Aug 23 08:02:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 08:02:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 08:02:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 08:03:38 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
