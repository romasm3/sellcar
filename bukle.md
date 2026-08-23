# Serverio būklė

Sugeneruota: 2026-08-23 21:18:31 CEST

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
HTTP 301, 0.001523s
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
Aug 23 21:10:02 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 21:10:02 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.482s CPU time.
Aug 23 21:11:24 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 21:11:25 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 21:11:25 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 21:11:25 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.061s CPU time.
Aug 23 21:12:45 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 21:12:46 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 21:12:46 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 21:13:54 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 21:13:55 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 21:13:55 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 21:13:55 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.007s CPU time.
Aug 23 21:15:00 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 21:15:03 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 21:15:03 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 21:15:03 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 2.137s CPU time.
Aug 23 21:16:17 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 21:16:19 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 21:16:19 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 21:17:25 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 21:17:29 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 21:17:29 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 21:17:29 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.777s CPU time.
Aug 23 21:18:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
