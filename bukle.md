# Serverio būklė

Sugeneruota: 2026-08-24 04:23:31 CEST

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
HTTP 301, 0.002153s
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
Aug 24 04:14:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 04:15:44 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 04:15:45 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 04:15:45 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 04:15:45 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.112s CPU time.
Aug 24 04:16:53 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 04:16:54 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 04:16:54 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 04:18:03 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 04:18:05 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 04:18:05 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 04:18:05 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.438s CPU time.
Aug 24 04:19:20 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 04:19:22 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 04:19:22 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 04:19:22 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.168s CPU time.
Aug 24 04:20:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 04:20:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 04:20:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 04:20:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.169s CPU time.
Aug 24 04:21:46 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 04:21:47 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 04:21:47 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 04:21:47 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.010s CPU time.
Aug 24 04:23:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
