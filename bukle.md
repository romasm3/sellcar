# Serverio būklė

Sugeneruota: 2026-08-24 09:26:03 CEST

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
HTTP 301, 0.001217s
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
Aug 24 09:17:33 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.262s CPU time.
Aug 24 09:18:54 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 09:18:55 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 09:18:55 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 09:18:55 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.145s CPU time.
Aug 24 09:20:05 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 09:20:07 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 09:20:07 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 09:20:07 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.205s CPU time.
Aug 24 09:21:11 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 09:21:13 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 09:21:13 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 09:21:13 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.160s CPU time.
Aug 24 09:22:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 09:22:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 09:22:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 09:22:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.053s CPU time.
Aug 24 09:23:42 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 09:23:44 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 09:23:44 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 09:23:44 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.053s CPU time.
Aug 24 09:24:58 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 09:24:59 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 09:24:59 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 09:26:03 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
