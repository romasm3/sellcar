# Serverio būklė

Sugeneruota: 2026-09-02 22:52:29 CEST

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
HTTP 301, 0.001435s
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
Sep 02 22:45:01 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 22:45:04 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 22:45:04 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 22:45:04 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 2.221s CPU time.
Sep 02 22:46:07 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 22:46:10 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 22:46:10 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 22:46:10 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.614s CPU time.
Sep 02 22:47:17 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 22:47:19 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 22:47:19 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 22:47:19 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.523s CPU time.
Sep 02 22:48:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 22:48:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 22:48:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 22:48:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.403s CPU time.
Sep 02 22:49:38 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 22:49:40 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 22:49:40 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 22:49:40 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.357s CPU time.
Sep 02 22:50:59 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 22:51:01 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 22:51:01 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 22:51:01 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.569s CPU time.
Sep 02 22:52:29 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
