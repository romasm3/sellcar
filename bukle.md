# Serverio būklė

Sugeneruota: 2026-08-24 01:24:15 CEST

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
HTTP 301, 0.001190s
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
Aug 24 01:16:14 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 01:16:14 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.138s CPU time.
Aug 24 01:17:15 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 01:17:18 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 01:17:18 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 01:17:18 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.664s CPU time.
Aug 24 01:18:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 01:18:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 01:18:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 01:19:43 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 01:19:45 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 01:19:45 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 01:19:45 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.039s CPU time.
Aug 24 01:20:47 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 01:20:49 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 01:20:49 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 01:20:49 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.008s CPU time.
Aug 24 01:21:50 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 01:21:52 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 01:21:52 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 01:23:02 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 01:23:04 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 01:23:04 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 01:23:04 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.255s CPU time.
Aug 24 01:24:15 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
