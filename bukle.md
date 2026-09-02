# Serverio būklė

Sugeneruota: 2026-09-02 17:00:15 CEST

## Kodas

```
sukasi:      15d2b7f fix(deploy): serverio raktai nebedingsta, kopijos nebeėda disko
origin/master: 15d2b7f fix(deploy): serverio raktai nebedingsta, kopijos nebeėda disko
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
HTTP 301, 0.005085s
```

## Skelbimų būsenos

```

Listing — iš viso 35
  active        18   MATOMAS
  draft          9   nematomas
  expired        8   nematomas
  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─
  nematomi dėl būsenos:      17
  iš jų pasibaigę (expires_at praeityje): 8
  aktyvūs, baigsis per 7 d.: 6
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
/dev/sda1       291G   34G  257G  12% /
```

## Paskutinis auto-deploy

```
Sep 02 16:53:20 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 16:53:23 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 16:53:23 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 16:53:23 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.411s CPU time.
Sep 02 16:54:27 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 16:54:29 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 16:54:29 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 16:54:29 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.456s CPU time.
Sep 02 16:55:37 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 16:55:39 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 16:55:39 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 16:55:39 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.540s CPU time.
Sep 02 16:56:44 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 16:56:46 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 16:56:46 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 16:56:46 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.560s CPU time.
Sep 02 16:57:59 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 16:58:02 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 16:58:02 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 16:58:02 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.672s CPU time.
Sep 02 16:59:04 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 16:59:06 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 16:59:06 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 16:59:06 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.467s CPU time.
Sep 02 17:00:15 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
