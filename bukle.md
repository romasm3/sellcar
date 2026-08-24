# Serverio būklė

Sugeneruota: 2026-08-24 15:21:00 CEST

## Kodas

```
sukasi:      f81c9ec feat(navigacija): antrinėje juostoje lieka „Pagalba" ir „Apie mus"
origin/master: f81c9ec feat(navigacija): antrinėje juostoje lieka „Pagalba" ir „Apie mus"
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/listings/emails/sender.py
   M apps/listings/management/commands/testiniai_skelbimai.py
   M apps/listings/management/commands/valyti_testinius.py
   M config/settings.py
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
HTTP 301, 0.001717s
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
Aug 24 15:13:23 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.120s CPU time.
Aug 24 15:14:26 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 15:14:28 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 15:14:28 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 15:14:28 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.028s CPU time.
Aug 24 15:15:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 15:15:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 15:15:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 15:15:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.161s CPU time.
Aug 24 15:16:47 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 15:16:48 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 15:16:48 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 15:16:48 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.187s CPU time.
Aug 24 15:17:52 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 15:17:55 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 15:17:55 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 15:17:55 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.368s CPU time.
Aug 24 15:18:54 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 15:18:55 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 15:18:55 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 15:18:55 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.053s CPU time.
Aug 24 15:19:55 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 15:19:57 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 15:19:57 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 15:21:00 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
