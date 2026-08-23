# Serverio būklė

Sugeneruota: 2026-08-24 00:57:31 CEST

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
HTTP 301, 0.001343s
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
Aug 24 00:47:34 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.056s CPU time.
Aug 24 00:48:41 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 00:48:42 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 00:48:42 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 00:49:49 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 00:49:50 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 00:49:50 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 00:50:56 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 00:50:58 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 00:50:58 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 00:50:58 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.139s CPU time.
Aug 24 00:52:11 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 00:52:12 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 00:52:12 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 00:52:12 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.183s CPU time.
Aug 24 00:53:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 00:53:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 00:53:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 00:54:45 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 00:54:47 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 00:54:47 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 00:56:09 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 00:56:10 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 00:56:10 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 00:57:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
