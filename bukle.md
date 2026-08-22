# Serverio būklė

Sugeneruota: 2026-08-22 23:21:15 CEST

## Kodas

```
sukasi:      7debaac feat(laiskai): įsimintų skelbimų sąrašas el. paštu + tikslus peržiūrų skaičius
origin/master: 7debaac feat(laiskai): įsimintų skelbimų sąrašas el. paštu + tikslus peržiūrų skaičius
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/listings/management/commands/sync_draft_email_scenarios.py
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
HTTP 301, 0.001225s
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
Aug 22 23:13:30 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 22 23:13:30 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 22 23:14:37 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 22 23:14:39 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 22 23:14:39 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 22 23:14:39 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.091s CPU time.
Aug 22 23:15:49 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 22 23:15:50 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 22 23:15:50 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 22 23:16:57 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 22 23:16:58 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 22 23:16:58 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 22 23:17:58 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 22 23:18:01 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 22 23:18:01 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 22 23:18:01 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.347s CPU time.
Aug 22 23:18:59 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 22 23:19:01 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 22 23:19:01 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 22 23:19:01 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.129s CPU time.
Aug 22 23:20:05 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 22 23:20:07 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 22 23:20:07 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 22 23:20:07 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.073s CPU time.
Aug 22 23:21:14 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
