# Serverio būklė

Sugeneruota: 2026-09-03 05:22:41 CEST

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
HTTP 301, 0.002216s
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
/dev/sda1       291G   25G  267G   9% /
```

## Paskutinis auto-deploy

```
Sep 03 05:14:59 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 03 05:15:01 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 03 05:15:01 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 03 05:15:01 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.555s CPU time.
Sep 03 05:16:24 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 03 05:16:25 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 03 05:16:25 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 03 05:16:25 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.313s CPU time.
Sep 03 05:17:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 03 05:17:39 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 03 05:17:39 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 03 05:17:39 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 2.965s CPU time.
Sep 03 05:18:51 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 03 05:18:53 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 03 05:18:53 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 03 05:18:53 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.482s CPU time.
Sep 03 05:20:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 03 05:20:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 03 05:20:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 03 05:20:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.370s CPU time.
Sep 03 05:21:38 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 03 05:21:40 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 03 05:21:40 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 03 05:21:40 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.521s CPU time.
Sep 03 05:22:41 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
