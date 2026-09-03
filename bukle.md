# Serverio būklė

Sugeneruota: 2026-09-03 11:24:39 CEST

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
HTTP 301, 0.001138s
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
Sep 03 11:17:22 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 03 11:17:31 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 03 11:17:31 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 03 11:17:31 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 2.980s CPU time.
Sep 03 11:18:39 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 03 11:18:41 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 03 11:18:41 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 03 11:18:41 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.395s CPU time.
Sep 03 11:20:05 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 03 11:20:08 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 03 11:20:08 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 03 11:20:08 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.817s CPU time.
Sep 03 11:21:16 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 03 11:21:18 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 03 11:21:18 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 03 11:21:18 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.540s CPU time.
Sep 03 11:22:29 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 03 11:22:31 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 03 11:22:31 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 03 11:22:31 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.443s CPU time.
Sep 03 11:23:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 03 11:23:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 03 11:23:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 03 11:23:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.291s CPU time.
Sep 03 11:24:39 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
