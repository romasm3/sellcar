# Serverio būklė

Sugeneruota: 2026-08-24 13:57:31 CEST

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
HTTP 301, 0.001416s
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
Aug 24 13:50:38 vmi3306453 autoleft-deploy[186762]: Aug 24 13:50:37 vmi3306453 autoleft-deploy[186527]: [2026-08-24 13:50:37] ✅ Deploy OK — gyvai veikia d734969
Aug 24 13:50:38 vmi3306453 autoleft-deploy[186762]: ```
Aug 24 13:50:38 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 13:50:38 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 13:50:38 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 10.282s CPU time.
Aug 24 13:51:41 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 13:51:43 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 13:51:43 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 13:51:43 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.071s CPU time.
Aug 24 13:52:52 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 13:52:53 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 13:52:53 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 13:53:59 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 13:54:01 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 13:54:01 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 13:54:01 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.091s CPU time.
Aug 24 13:55:07 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 13:55:08 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 13:55:08 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 13:55:08 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.103s CPU time.
Aug 24 13:56:16 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 13:56:18 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 13:56:18 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 13:56:18 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.054s CPU time.
Aug 24 13:57:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
