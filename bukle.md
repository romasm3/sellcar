# Serverio būklė

Sugeneruota: 2026-09-02 17:13:29 CEST

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
HTTP 301, 0.001533s
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
Sep 02 17:05:43 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 17:05:46 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 17:05:46 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 17:05:46 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.499s CPU time.
Sep 02 17:06:51 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 17:06:53 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 17:06:53 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 17:06:53 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.524s CPU time.
Sep 02 17:07:56 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 17:07:59 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 17:07:59 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 17:07:59 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 2.056s CPU time.
Sep 02 17:09:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 17:09:33 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 17:09:33 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 17:09:33 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.564s CPU time.
Sep 02 17:11:13 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 17:11:15 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 17:11:15 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 17:11:15 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.579s CPU time.
Sep 02 17:12:16 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 17:12:18 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 17:12:18 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 17:12:18 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.515s CPU time.
Sep 02 17:13:29 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
