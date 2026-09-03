# Serverio būklė

Sugeneruota: 2026-09-03 12:25:28 CEST

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
HTTP 301, 0.001096s
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
/dev/sda1       291G   25G  266G   9% /
```

## Paskutinis auto-deploy

```
Sep 03 12:18:54 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 03 12:18:56 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 03 12:18:56 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 03 12:18:56 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.549s CPU time.
Sep 03 12:19:59 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 03 12:20:03 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 03 12:20:03 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 03 12:20:03 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 2.317s CPU time.
Sep 03 12:21:06 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 03 12:21:09 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 03 12:21:09 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 03 12:21:09 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.470s CPU time.
Sep 03 12:22:10 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 03 12:22:12 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 03 12:22:12 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 03 12:22:12 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.435s CPU time.
Sep 03 12:23:17 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 03 12:23:19 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 03 12:23:19 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 03 12:23:19 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.307s CPU time.
Sep 03 12:24:25 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 03 12:24:27 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 03 12:24:27 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 03 12:24:27 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.438s CPU time.
Sep 03 12:25:28 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
