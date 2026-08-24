# Serverio būklė

Sugeneruota: 2026-08-24 03:15:31 CEST

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
HTTP 301, 0.001516s
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
Aug 24 03:05:55 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 03:05:55 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 03:05:55 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.060s CPU time.
Aug 24 03:07:08 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 03:07:10 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 03:07:10 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 03:07:10 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.011s CPU time.
Aug 24 03:08:26 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 03:08:28 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 03:08:28 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 03:10:14 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 03:10:16 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 03:10:16 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 03:10:16 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.114s CPU time.
Aug 24 03:11:21 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 03:11:23 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 03:11:23 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 03:13:00 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 03:13:02 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 03:13:02 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 03:13:02 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.264s CPU time.
Aug 24 03:14:25 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 03:14:27 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 03:14:27 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 03:15:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
