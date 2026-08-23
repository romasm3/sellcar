# Serverio būklė

Sugeneruota: 2026-08-24 01:33:40 CEST

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
HTTP 301, 0.001588s
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
Aug 24 01:24:16 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 01:25:22 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 01:25:24 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 01:25:24 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 01:25:24 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.096s CPU time.
Aug 24 01:26:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 01:26:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 01:26:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 01:27:52 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 01:27:53 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 01:27:53 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 01:28:57 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 01:28:59 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 01:28:59 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 01:30:15 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 01:30:17 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 01:30:17 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 01:30:17 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.045s CPU time.
Aug 24 01:31:24 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 01:31:25 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 01:31:25 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 01:32:32 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 01:32:33 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 01:32:33 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 01:33:40 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
