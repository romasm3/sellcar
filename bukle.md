# Serverio būklė

Sugeneruota: 2026-09-01 23:00:59 CEST

## Kodas

```
sukasi:      b3e737b fix(deploy): statinių patikra nebeatsuka kodo + versijos žymė
origin/master: b3e737b fix(deploy): statinių patikra nebeatsuka kodo + versijos žymė
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
HTTP 301, 0.003039s
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
/dev/sda1       291G   45G  246G  16% /
```

## Paskutinis auto-deploy

```
Sep 01 22:53:19 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 01 22:53:26 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 01 22:53:26 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 22:53:26 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 2.313s CPU time.
Sep 01 22:54:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 01 22:54:33 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 01 22:54:33 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 22:54:33 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.515s CPU time.
Sep 01 22:56:04 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 01 22:56:06 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 01 22:56:06 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 22:56:06 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.757s CPU time.
Sep 01 22:57:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 01 22:57:33 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 01 22:57:33 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 22:57:33 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.496s CPU time.
Sep 01 22:58:40 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 01 22:58:43 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 01 22:58:43 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 22:58:43 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.624s CPU time.
Sep 01 22:59:50 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 01 22:59:52 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 01 22:59:52 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 22:59:52 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.777s CPU time.
Sep 01 23:00:59 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
