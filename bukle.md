# Serverio būklė

Sugeneruota: 2026-09-02 17:34:42 CEST

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
HTTP 301, 0.001657s
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
Sep 02 17:26:24 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 17:26:26 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 17:26:26 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 17:26:26 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.374s CPU time.
Sep 02 17:28:07 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 17:28:09 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 17:28:09 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 17:28:09 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.384s CPU time.
Sep 02 17:29:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 17:29:33 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 17:29:33 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 17:29:33 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.689s CPU time.
Sep 02 17:31:07 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 17:31:09 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 17:31:09 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 17:31:09 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.604s CPU time.
Sep 02 17:32:19 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 17:32:22 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 17:32:22 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 17:32:22 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.637s CPU time.
Sep 02 17:33:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 17:33:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 17:33:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 17:33:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.396s CPU time.
Sep 02 17:34:42 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
