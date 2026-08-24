# Serverio būklė

Sugeneruota: 2026-08-24 10:11:17 CEST

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
HTTP 301, 0.001736s
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
Aug 24 10:02:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 10:02:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 10:02:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.087s CPU time.
Aug 24 10:03:46 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 10:03:48 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 10:03:48 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 10:05:03 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 10:05:05 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 10:05:05 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 10:05:05 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.249s CPU time.
Aug 24 10:06:24 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 10:06:25 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 10:06:25 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 10:07:35 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 10:07:37 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 10:07:37 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 10:08:54 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 10:08:55 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 10:08:55 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 10:08:55 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.076s CPU time.
Aug 24 10:10:01 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 10:10:04 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 10:10:04 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 10:10:04 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.537s CPU time.
Aug 24 10:11:17 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
