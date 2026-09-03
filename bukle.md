# Serverio būklė

Sugeneruota: 2026-09-03 16:10:29 CEST

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
HTTP 301, 0.001755s
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
Sep 03 16:03:18 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 03 16:03:21 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 03 16:03:21 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 03 16:03:21 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.383s CPU time.
Sep 03 16:04:29 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 03 16:04:31 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 03 16:04:31 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 03 16:04:31 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.282s CPU time.
Sep 03 16:05:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 03 16:05:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 03 16:05:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 03 16:05:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.374s CPU time.
Sep 03 16:06:56 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 03 16:06:58 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 03 16:06:58 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 03 16:06:58 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.345s CPU time.
Sep 03 16:08:02 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 03 16:08:05 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 03 16:08:05 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 03 16:08:05 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.657s CPU time.
Sep 03 16:09:05 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 03 16:09:08 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 03 16:09:08 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 03 16:09:08 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.684s CPU time.
Sep 03 16:10:29 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
