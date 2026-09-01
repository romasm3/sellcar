# Serverio būklė

Sugeneruota: 2026-09-01 23:09:14 CEST

## Kodas

```
sukasi:      b42c6f9 fix(deploy): po atsukimo darbinis katalogas lieka švarus
origin/master: b42c6f9 fix(deploy): po atsukimo darbinis katalogas lieka švarus
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
HTTP 301, 0.008935s
```

## Skelbimų būsenos

```

Listing — iš viso 35
  active        19   MATOMAS
  draft          9   nematomas
  expired        7   nematomas
  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─
  nematomi dėl būsenos:      16
  iš jų pasibaigę (expires_at praeityje): 7
  aktyvūs, baigsis per 7 d.: 5
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
/dev/sda1       291G   46G  246G  16% /
```

## Paskutinis auto-deploy

```
Sep 01 23:03:09 vmi3306453 autoleft-deploy[3013073]: ```
Sep 01 23:03:09 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 01 23:03:09 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 23:03:09 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 24.691s CPU time.
Sep 01 23:03:15 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 01 23:03:17 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 01 23:03:17 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 23:03:17 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.732s CPU time.
Sep 01 23:04:28 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 01 23:04:31 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 01 23:04:31 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 23:04:31 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.688s CPU time.
Sep 01 23:05:43 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 01 23:05:45 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 01 23:05:45 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 23:05:45 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.693s CPU time.
Sep 01 23:06:50 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 01 23:06:52 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 01 23:06:52 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 23:06:52 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.368s CPU time.
Sep 01 23:07:58 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 01 23:08:02 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 01 23:08:02 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 23:08:02 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.885s CPU time.
Sep 01 23:09:14 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
