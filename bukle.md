# Serverio būklė

Sugeneruota: 2026-08-23 17:44:47 CEST

## Kodas

```
sukasi:      d1902a3 style(paieska): kategorijų juosta ir „Daugiau" sąrašas pagal etaloną
origin/master: d1902a3 style(paieska): kategorijų juosta ir „Daugiau" sąrašas pagal etaloną
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
HTTP 301, 0.001082s
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
  aktyvūs, baigsis per 7 d.: 3
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
/dev/sda1       291G   15G  277G   5% /
```

## Paskutinis auto-deploy

```
Aug 23 17:36:02 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.231s CPU time.
Aug 23 17:37:09 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 17:37:10 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 17:37:10 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 17:38:17 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 17:38:18 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 17:38:18 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 17:39:19 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 17:39:21 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 17:39:21 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 17:40:23 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 17:40:24 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 17:40:24 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 17:40:24 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.009s CPU time.
Aug 23 17:41:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 17:41:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 17:41:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 17:41:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.087s CPU time.
Aug 23 17:42:35 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 17:42:37 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 17:42:37 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 17:43:45 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 17:43:46 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 17:43:46 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 17:44:47 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
