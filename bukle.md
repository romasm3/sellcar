# Serverio būklė

Sugeneruota: 2026-09-03 15:08:31 CEST

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
HTTP 301, 0.001252s
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
Sep 03 15:01:07 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 03 15:01:09 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 03 15:01:09 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 03 15:01:09 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.472s CPU time.
Sep 03 15:02:17 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 03 15:02:19 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 03 15:02:19 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 03 15:02:19 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.690s CPU time.
Sep 03 15:03:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 03 15:03:33 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 03 15:03:33 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 03 15:03:33 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.593s CPU time.
Sep 03 15:04:39 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 03 15:04:41 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 03 15:04:41 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 03 15:04:41 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.456s CPU time.
Sep 03 15:05:59 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 03 15:06:01 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 03 15:06:01 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 03 15:06:01 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.548s CPU time.
Sep 03 15:07:08 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 03 15:07:10 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 03 15:07:10 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 03 15:07:10 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.405s CPU time.
Sep 03 15:08:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
