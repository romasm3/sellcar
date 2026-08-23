# Serverio būklė

Sugeneruota: 2026-08-23 07:49:52 CEST

## Kodas

```
sukasi:      80644db feat(create): automobilio formos laukai pagal etaloną
origin/master: 80644db feat(create): automobilio formos laukai pagal etaloną
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
HTTP 301, 0.001301s
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
  aktyvūs, baigsis per 7 d.: 2
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
/dev/sda1       291G   14G  277G   5% /
```

## Paskutinis auto-deploy

```
Aug 23 07:40:55 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.117s CPU time.
Aug 23 07:41:59 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 07:42:00 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 07:42:00 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 07:43:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 07:43:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 07:43:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 07:43:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.181s CPU time.
Aug 23 07:44:59 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 07:45:00 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 07:45:00 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 07:45:00 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.081s CPU time.
Aug 23 07:46:24 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 07:46:25 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 07:46:25 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 07:46:25 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.022s CPU time.
Aug 23 07:47:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 07:47:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 07:47:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 07:47:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.114s CPU time.
Aug 23 07:48:42 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 07:48:44 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 07:48:44 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 07:48:44 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.026s CPU time.
Aug 23 07:49:52 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
