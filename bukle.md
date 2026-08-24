# Serverio būklė

Sugeneruota: 2026-08-24 09:03:24 CEST

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
HTTP 301, 0.001567s
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
Aug 24 08:55:30 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.079s CPU time.
Aug 24 08:56:37 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 08:56:38 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 08:56:38 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 08:57:46 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 08:57:48 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 08:57:48 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 08:57:48 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.069s CPU time.
Aug 24 08:58:54 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 08:58:55 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 08:58:55 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 08:58:55 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.086s CPU time.
Aug 24 09:00:01 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 09:00:04 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 09:00:04 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 09:00:04 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.618s CPU time.
Aug 24 09:01:09 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 09:01:11 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 09:01:11 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 09:01:11 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.158s CPU time.
Aug 24 09:02:19 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 09:02:20 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 09:02:20 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 09:02:20 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.193s CPU time.
Aug 24 09:03:24 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
