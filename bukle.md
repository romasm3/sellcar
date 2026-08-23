# Serverio būklė

Sugeneruota: 2026-08-24 00:16:14 CEST

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
HTTP 301, 0.001080s
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
Aug 24 00:07:27 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 00:07:27 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 00:07:27 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.024s CPU time.
Aug 24 00:08:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 00:08:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 00:08:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 00:08:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.025s CPU time.
Aug 24 00:09:45 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 00:09:47 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 00:09:47 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 00:11:24 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 00:11:25 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 00:11:25 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 00:11:25 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.000s CPU time.
Aug 24 00:12:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 00:12:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 00:12:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 00:13:43 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 00:13:45 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 00:13:45 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 00:15:01 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 00:15:03 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 00:15:03 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 00:15:03 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.623s CPU time.
Aug 24 00:16:13 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
