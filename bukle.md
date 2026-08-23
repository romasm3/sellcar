# Serverio būklė

Sugeneruota: 2026-08-24 00:27:25 CEST

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
HTTP 301, 0.001142s
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
Aug 24 00:18:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 00:18:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 00:18:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.147s CPU time.
Aug 24 00:19:42 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 00:19:43 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 00:19:43 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 00:20:59 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 00:21:00 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 00:21:00 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 00:21:00 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.147s CPU time.
Aug 24 00:22:13 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 00:22:15 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 00:22:15 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 00:22:15 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.083s CPU time.
Aug 24 00:23:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 00:23:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 00:23:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 00:25:06 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 00:25:08 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 00:25:08 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 00:25:08 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.265s CPU time.
Aug 24 00:26:24 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 00:26:25 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 00:26:25 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 00:27:25 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
