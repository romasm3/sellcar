# Serverio būklė

Sugeneruota: 2026-08-24 06:01:24 CEST

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
HTTP 301, 0.002010s
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
Aug 24 05:53:54 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 05:53:55 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 05:53:55 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 05:53:55 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.178s CPU time.
Aug 24 05:54:57 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 05:54:58 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 05:54:58 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 05:54:58 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.151s CPU time.
Aug 24 05:56:16 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 05:56:17 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 05:56:17 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 05:56:17 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.148s CPU time.
Aug 24 05:57:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 05:57:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 05:57:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 05:57:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.097s CPU time.
Aug 24 05:58:54 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 05:58:55 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 05:58:55 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 05:58:55 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.057s CPU time.
Aug 24 06:00:16 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 06:00:18 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 06:00:18 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 06:00:18 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.412s CPU time.
Aug 24 06:01:24 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
