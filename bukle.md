# Serverio būklė

Sugeneruota: 2026-08-24 02:26:31 CEST

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
HTTP 301, 0.001122s
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
/dev/sda1       291G   14G  277G   5% /
```

## Paskutinis auto-deploy

```
Aug 24 02:17:56 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 02:17:56 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.297s CPU time.
Aug 24 02:19:15 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 02:19:17 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 02:19:17 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 02:19:17 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.186s CPU time.
Aug 24 02:20:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 02:20:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 02:20:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 02:22:08 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 02:22:10 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 02:22:10 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 02:22:10 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.013s CPU time.
Aug 24 02:23:15 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 02:23:17 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 02:23:17 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 02:24:19 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 02:24:21 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 02:24:21 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 02:24:21 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.042s CPU time.
Aug 24 02:25:23 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 02:25:25 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 02:25:25 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 02:25:25 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.074s CPU time.
Aug 24 02:26:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
