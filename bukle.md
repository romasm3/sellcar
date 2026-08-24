# Serverio būklė

Sugeneruota: 2026-08-24 03:47:33 CEST

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
HTTP 301, 0.001222s
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
Aug 24 03:39:35 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 03:39:35 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 03:40:53 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 03:40:55 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 03:40:55 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 03:40:55 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.225s CPU time.
Aug 24 03:42:04 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 03:42:06 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 03:42:06 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 03:42:06 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.008s CPU time.
Aug 24 03:43:07 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 03:43:09 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 03:43:09 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 03:44:11 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 03:44:12 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 03:44:12 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 03:44:12 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.068s CPU time.
Aug 24 03:45:13 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 03:45:15 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 03:45:15 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 03:45:15 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.138s CPU time.
Aug 24 03:46:24 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 03:46:25 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 03:46:25 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 03:47:33 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
