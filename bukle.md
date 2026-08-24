# Serverio būklė

Sugeneruota: 2026-08-24 07:50:59 CEST

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
HTTP 301, 0.002148s
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
Aug 24 07:43:00 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 07:43:00 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 07:44:04 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 07:44:05 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 07:44:05 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 07:45:15 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 07:45:16 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 07:45:16 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 07:46:23 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 07:46:24 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 07:46:24 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 07:46:24 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.005s CPU time.
Aug 24 07:47:29 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 07:47:31 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 07:47:31 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 07:47:31 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.062s CPU time.
Aug 24 07:48:31 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 07:48:33 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 07:48:33 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 07:48:33 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.024s CPU time.
Aug 24 07:49:46 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 07:49:47 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 07:49:47 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 07:49:47 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.077s CPU time.
Aug 24 07:50:59 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
