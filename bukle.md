# Serverio būklė

Sugeneruota: 2026-08-23 22:04:31 CEST

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
HTTP 301, 0.001006s
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
Aug 23 21:56:22 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 21:56:23 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 21:56:23 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 21:57:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 21:57:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 21:57:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 21:57:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.049s CPU time.
Aug 23 21:58:35 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 21:58:37 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 21:58:37 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 21:59:45 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 21:59:46 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 21:59:46 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 22:00:54 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 22:00:56 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 22:00:56 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 22:00:56 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.263s CPU time.
Aug 23 22:02:05 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 22:02:06 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 22:02:06 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 22:02:06 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.015s CPU time.
Aug 23 22:03:15 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 22:03:16 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 22:03:16 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 22:04:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
