# Serverio būklė

Sugeneruota: 2026-09-02 21:01:22 CEST

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
HTTP 301, 0.006273s
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
Sep 02 20:53:54 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 20:53:56 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 20:53:56 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 20:53:56 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.459s CPU time.
Sep 02 20:55:07 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 20:55:10 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 20:55:10 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 20:55:10 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.539s CPU time.
Sep 02 20:56:18 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 20:56:20 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 20:56:20 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 20:56:20 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.525s CPU time.
Sep 02 20:57:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 20:57:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 20:57:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 20:57:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.413s CPU time.
Sep 02 20:58:54 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 20:58:56 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 20:58:56 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 20:58:56 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.501s CPU time.
Sep 02 20:59:59 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 21:00:01 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 21:00:01 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 21:00:01 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.613s CPU time.
Sep 02 21:01:22 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
