# Serverio būklė

Sugeneruota: 2026-08-23 21:56:22 CEST

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
HTTP 301, 0.001290s
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
Aug 23 21:47:17 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 21:47:17 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.242s CPU time.
Aug 23 21:48:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 21:48:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 21:48:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 21:48:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.172s CPU time.
Aug 23 21:49:51 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 21:49:52 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 21:49:52 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 21:49:52 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.127s CPU time.
Aug 23 21:50:59 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 21:51:00 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 21:51:00 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 21:51:00 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.083s CPU time.
Aug 23 21:52:01 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 21:52:03 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 21:52:03 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 21:52:03 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.520s CPU time.
Aug 23 21:53:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 21:53:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 21:53:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 21:54:45 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 21:54:47 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 21:54:47 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 21:56:22 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
