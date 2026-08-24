# Serverio būklė

Sugeneruota: 2026-08-24 13:34:02 CEST

## Kodas

```
sukasi:      29b5720 feat(perziureti): peržiūrėtų skelbimų sąrašas su /perziureti/ puslapiu
origin/master: 29b5720 feat(perziureti): peržiūrėtų skelbimų sąrašas su /perziureti/ puslapiu
šaka:        master
darbo katalogas: švarus
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
HTTP 301, 0.001030s
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
Aug 24 13:26:07 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 13:26:09 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 13:26:09 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 13:27:16 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 13:27:18 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 13:27:18 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 13:28:23 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 13:28:24 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 13:28:24 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 13:29:28 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 13:29:29 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 13:29:29 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 13:30:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 13:30:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 13:30:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 13:30:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.109s CPU time.
Aug 24 13:31:39 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 13:31:41 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 13:31:41 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 13:31:41 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.017s CPU time.
Aug 24 13:32:55 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 13:32:56 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 13:32:56 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 13:32:56 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.037s CPU time.
Aug 24 13:34:02 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
