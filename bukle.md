# Serverio būklė

Sugeneruota: 2026-08-24 05:20:31 CEST

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
HTTP 301, 0.001366s
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
Aug 24 05:11:47 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.051s CPU time.
Aug 24 05:12:57 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 05:12:58 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 05:12:58 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 05:12:58 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.027s CPU time.
Aug 24 05:14:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 05:14:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 05:14:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 05:15:36 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 05:15:37 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 05:15:37 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 05:15:37 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.104s CPU time.
Aug 24 05:16:45 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 05:16:46 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 05:16:46 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 05:16:46 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.138s CPU time.
Aug 24 05:17:59 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 05:18:03 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 05:18:03 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 05:18:03 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 2.318s CPU time.
Aug 24 05:19:27 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 05:19:29 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 05:19:29 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 05:19:29 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.307s CPU time.
Aug 24 05:20:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
