# Serverio būklė

Sugeneruota: 2026-09-03 00:38:38 CEST

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
HTTP 301, 0.008867s
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
Sep 03 00:30:51 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 03 00:30:53 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 03 00:30:53 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 03 00:30:53 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.414s CPU time.
Sep 03 00:32:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 03 00:32:33 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 03 00:32:33 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 03 00:32:33 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.499s CPU time.
Sep 03 00:33:38 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 03 00:33:40 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 03 00:33:40 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 03 00:33:40 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.411s CPU time.
Sep 03 00:35:18 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 03 00:35:20 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 03 00:35:20 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 03 00:35:20 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.509s CPU time.
Sep 03 00:36:28 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 03 00:36:30 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 03 00:36:30 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 03 00:36:30 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.535s CPU time.
Sep 03 00:37:34 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 03 00:37:35 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 03 00:37:35 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 03 00:37:35 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.259s CPU time.
Sep 03 00:38:37 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
