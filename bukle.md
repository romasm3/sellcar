# Serverio būklė

Sugeneruota: 2026-08-24 05:48:49 CEST

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
HTTP 301, 0.001270s
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
Aug 24 05:40:18 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.256s CPU time.
Aug 24 05:41:24 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 05:41:25 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 05:41:25 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 05:41:25 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.321s CPU time.
Aug 24 05:42:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 05:42:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 05:42:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 05:42:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.011s CPU time.
Aug 24 05:43:54 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 05:43:55 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 05:43:55 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 05:43:55 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.071s CPU time.
Aug 24 05:45:01 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 05:45:03 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 05:45:03 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 05:45:03 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.584s CPU time.
Aug 24 05:46:16 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 05:46:17 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 05:46:17 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 05:46:17 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.074s CPU time.
Aug 24 05:47:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 05:47:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 05:47:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 05:48:49 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
