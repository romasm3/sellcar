# Serverio būklė

Sugeneruota: 2026-08-24 14:05:03 CEST

## Kodas

```
sukasi:      288b7a9 feat(skelbimas): pardavėjo blokas turinyje ir „Kiti pardavėjo skelbimai"
origin/master: 288b7a9 feat(skelbimas): pardavėjo blokas turinyje ir „Kiti pardavėjo skelbimai"
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
HTTP 301, 0.001473s
```

## Skelbimų būsenos

```

Listing — iš viso 35
  active        23   MATOMAS
  draft          9   nematomas
  expired        3   nematomas
  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─
  nematomi dėl būsenos:      12
  iš jų pasibaigę (expires_at praeityje): 3
  aktyvūs, baigsis per 7 d.: 4
  aktyvūs be pabaigos datos: 8 (pvz. testiniai)
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
Aug 24 13:56:18 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 13:56:18 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.054s CPU time.
Aug 24 13:57:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 13:57:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 13:57:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 13:57:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.146s CPU time.
Aug 24 13:58:44 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 13:58:45 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 13:58:45 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 13:58:45 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.138s CPU time.
Aug 24 14:00:01 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 14:00:05 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 14:00:05 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 14:00:05 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 2.161s CPU time.
Aug 24 14:01:12 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 14:01:14 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 14:01:14 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 14:01:14 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.162s CPU time.
Aug 24 14:02:28 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 14:02:30 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 14:02:30 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 14:03:37 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 14:03:38 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 14:03:38 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 14:05:03 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
