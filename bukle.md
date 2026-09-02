# Serverio būklė

Sugeneruota: 2026-09-03 01:25:09 CEST

## Kodas

```
sukasi:      7e171f9 fix(vertimai): masinis užpildymas per paslaugos paskyrą, ne API raktą
origin/master: 7e171f9 fix(vertimai): masinis užpildymas per paslaugos paskyrą, ne API raktą
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M docs/vertimo_uzpildymas_ataskaita.txt
   M locale/en/LC_MESSAGES/django.po
   M locale/ru/LC_MESSAGES/django.po
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
HTTP 301, 0.001296s
```

## Skelbimų būsenos

```

Listing — iš viso 35
  active        18   MATOMAS
  draft          9   nematomas
  expired        8   nematomas
  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─
  nematomi dėl būsenos:      17
  iš jų pasibaigę (expires_at praeityje): 8
  aktyvūs, baigsis per 7 d.: 6
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
/dev/sda1       291G   24G  267G   9% /
```

## Paskutinis auto-deploy

```
Sep 03 01:18:24 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 03 01:18:26 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 03 01:18:26 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 03 01:18:26 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.459s CPU time.
Sep 03 01:19:26 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 03 01:19:29 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 03 01:19:29 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 03 01:19:29 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.429s CPU time.
Sep 03 01:20:36 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 03 01:20:38 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 03 01:20:38 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 03 01:20:38 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.443s CPU time.
Sep 03 01:21:47 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 03 01:21:50 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 03 01:21:50 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 03 01:21:50 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.485s CPU time.
Sep 03 01:22:54 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 03 01:22:56 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 03 01:22:56 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 03 01:22:56 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.428s CPU time.
Sep 03 01:24:01 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 03 01:24:03 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 03 01:24:03 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 03 01:24:03 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.741s CPU time.
Sep 03 01:25:08 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
