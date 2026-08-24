# Serverio būklė

Sugeneruota: 2026-08-24 07:06:24 CEST

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
HTTP 301, 0.002165s
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
Aug 24 06:57:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 06:57:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.040s CPU time.
Aug 24 06:58:54 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 06:58:55 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 06:58:55 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 06:58:55 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.107s CPU time.
Aug 24 07:00:16 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 07:00:18 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 07:00:18 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 07:00:18 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.529s CPU time.
Aug 24 07:01:24 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 07:01:25 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 07:01:25 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 07:01:25 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.224s CPU time.
Aug 24 07:02:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 07:02:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 07:02:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 07:03:54 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 07:03:55 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 07:03:55 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 07:05:16 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 07:05:17 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 07:05:17 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 07:05:17 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.117s CPU time.
Aug 24 07:06:24 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
