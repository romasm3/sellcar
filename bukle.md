# Serverio būklė

Sugeneruota: 2026-08-24 09:53:39 CEST

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
HTTP 301, 0.001626s
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
Aug 24 09:46:24 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 09:46:25 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 09:46:25 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 09:46:25 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.233s CPU time.
Aug 24 09:47:46 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 09:47:48 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 09:47:48 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 09:47:48 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.142s CPU time.
Aug 24 09:48:54 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 09:48:55 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 09:48:55 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 09:48:55 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.185s CPU time.
Aug 24 09:50:03 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 09:50:05 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 09:50:05 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 09:50:05 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.713s CPU time.
Aug 24 09:51:24 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 09:51:25 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 09:51:25 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 09:51:25 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.226s CPU time.
Aug 24 09:52:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 09:52:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 09:52:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 09:52:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.340s CPU time.
Aug 24 09:53:39 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
