# Serverio būklė

Sugeneruota: 2026-08-24 14:29:24 CEST

## Kodas

```
sukasi:      f0d2f1d feat(skelbimai): naujas /skelbimai/ puslapis ir „Žiūrėti visus" po skirtukais
origin/master: f0d2f1d feat(skelbimai): naujas /skelbimai/ puslapis ir „Žiūrėti visus" po skirtukais
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
HTTP 301, 0.001419s
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
Aug 24 14:20:48 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 14:20:48 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 14:20:48 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.049s CPU time.
Aug 24 14:21:49 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 14:21:51 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 14:21:51 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 14:21:51 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.019s CPU time.
Aug 24 14:23:10 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 14:23:12 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 14:23:12 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 14:23:12 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.026s CPU time.
Aug 24 14:24:25 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 14:24:27 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 14:24:27 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 14:25:35 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 14:25:36 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 14:25:36 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 14:26:46 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 14:26:48 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 14:26:48 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 14:26:48 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.004s CPU time.
Aug 24 14:27:56 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 14:27:57 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 14:27:57 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 14:29:24 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
