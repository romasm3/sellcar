# Serverio būklė

Sugeneruota: 2026-09-03 02:36:24 CEST

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
HTTP 301, 0.001367s
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
Sep 03 02:28:54 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 03 02:28:56 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 03 02:28:56 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 03 02:28:56 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.386s CPU time.
Sep 03 02:29:59 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 03 02:30:01 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 03 02:30:01 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 03 02:30:01 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.625s CPU time.
Sep 03 02:31:08 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 03 02:31:10 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 03 02:31:10 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 03 02:31:10 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.372s CPU time.
Sep 03 02:32:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 03 02:32:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 03 02:32:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 03 02:32:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.447s CPU time.
Sep 03 02:33:52 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 03 02:33:55 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 03 02:33:55 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 03 02:33:55 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.519s CPU time.
Sep 03 02:35:02 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 03 02:35:05 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 03 02:35:05 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 03 02:35:05 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 2.008s CPU time.
Sep 03 02:36:24 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
