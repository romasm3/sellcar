# Serverio būklė

Sugeneruota: 2026-08-23 21:44:47 CEST

## Kodas

```
sukasi:      5eae698 fix(skelbimas): matmenų perskaičiavimas rodomas vieną kartą
origin/master: 5eae698 fix(skelbimas): matmenų perskaičiavimas rodomas vieną kartą
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
HTTP 301, 0.001534s
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
  aktyvūs, baigsis per 7 d.: 4
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
Aug 23 21:36:05 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.279s CPU time.
Aug 23 21:37:25 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 21:37:26 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 21:37:26 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 21:38:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 21:38:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 21:38:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 21:38:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.091s CPU time.
Aug 23 21:39:58 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 21:39:59 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 21:39:59 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 21:39:59 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.212s CPU time.
Aug 23 21:41:13 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 21:41:15 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 21:41:15 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 21:41:15 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.348s CPU time.
Aug 23 21:42:24 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 21:42:26 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 21:42:26 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 21:42:26 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.180s CPU time.
Aug 23 21:43:37 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 21:43:38 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 21:43:38 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 21:43:38 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.107s CPU time.
Aug 23 21:44:47 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
