# Serverio būklė

Sugeneruota: 2026-09-06 17:57:28 CEST

## Kodas

```
sukasi:      28672ee vertimai: uzpildytos visos matomos eilutes
origin/master: 28672ee vertimai: uzpildytos visos matomos eilutes
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
HTTP 301, 0.001250s
```

## Skelbimų būsenos

```

Listing — iš viso 35
  active        16   MATOMAS
  expired       10   nematomas
  draft          9   nematomas
  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─
  nematomi dėl būsenos:      19
  iš jų pasibaigę (expires_at praeityje): 10
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
/dev/sda1       291G   28G  263G  10% /
```

## Paskutinis auto-deploy

```
Sep 06 17:50:16 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 17:50:18 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 17:50:18 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 17:50:18 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.529s CPU time.
Sep 06 17:51:24 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 17:51:26 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 17:51:26 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 17:51:26 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.603s CPU time.
Sep 06 17:52:29 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 17:52:31 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 17:52:31 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 17:52:31 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.519s CPU time.
Sep 06 17:53:49 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 17:53:51 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 17:53:51 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 17:53:51 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.519s CPU time.
Sep 06 17:55:03 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 17:55:06 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 17:55:06 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 17:55:06 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.734s CPU time.
Sep 06 17:56:16 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 17:56:18 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 17:56:18 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 17:56:18 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.556s CPU time.
Sep 06 17:57:28 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
