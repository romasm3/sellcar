# Serverio būklė

Sugeneruota: 2026-08-24 08:21:16 CEST

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
HTTP 301, 0.001589s
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
Aug 24 08:12:03 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 08:13:15 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 08:13:16 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 08:13:16 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 08:13:16 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.037s CPU time.
Aug 24 08:14:16 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 08:14:17 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 08:14:17 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 08:15:27 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 08:15:29 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 08:15:29 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 08:15:29 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.046s CPU time.
Aug 24 08:17:16 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 08:17:19 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 08:17:19 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 08:17:19 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.501s CPU time.
Aug 24 08:18:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 08:18:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 08:18:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 08:18:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.220s CPU time.
Aug 24 08:19:57 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 08:19:59 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 08:19:59 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 08:19:59 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.005s CPU time.
Aug 24 08:21:16 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
