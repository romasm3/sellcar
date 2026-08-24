# Serverio būklė

Sugeneruota: 2026-08-24 04:08:23 CEST

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
HTTP 301, 0.001212s
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
Aug 24 04:00:03 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 04:00:03 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 04:00:03 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.403s CPU time.
Aug 24 04:01:09 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 04:01:11 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 04:01:11 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 04:01:11 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.166s CPU time.
Aug 24 04:02:26 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 04:02:28 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 04:02:28 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 04:03:32 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 04:03:33 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 04:03:33 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 04:04:40 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 04:04:42 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 04:04:42 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 04:04:42 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.150s CPU time.
Aug 24 04:05:47 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 04:05:48 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 04:05:48 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 04:05:48 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.052s CPU time.
Aug 24 04:07:16 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 04:07:17 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 04:07:17 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 04:08:23 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
