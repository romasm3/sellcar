# Serverio būklė

Sugeneruota: 2026-08-23 18:07:45 CEST

## Kodas

```
sukasi:      c40a9cd feat(paieska): dalių detali paieška pagal etaloną
origin/master: c40a9cd feat(paieska): dalių detali paieška pagal etaloną
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M templates/listings/partials/_panel_bodies.html
   M templates/listings/partials/_sp_field_styles.html
   M templates/listings/partials/search_panel.html
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
HTTP 301, 0.001618s
```

## Skelbimų būsenos

```

Listing — iš viso 47
  active        33   MATOMAS
  draft         11   nematomas
  expired        3   nematomas
  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─
  nematomi dėl būsenos:      14
  iš jų pasibaigę (expires_at praeityje): 3
  aktyvūs, baigsis per 7 d.: 3
  aktyvūs be pabaigos datos: 16 (pvz. testiniai)
Truck: skelbimų nėra.
WheelListing: skelbimų nėra.

Viešame sąraše matomi tik status="active" (+ neseniai parduoti).
Jei tavo seni skelbimai yra "expired" — juos reikia aktyvuoti iš naujo,
o ne taisyti kode.
```

## Vietos diske

```
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       291G   15G  277G   5% /
```

## Paskutinis auto-deploy

```
Aug 23 17:58:08 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.051s CPU time.
Aug 23 17:59:09 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 17:59:10 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 17:59:10 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 18:00:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 18:00:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 18:00:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 18:01:39 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 18:01:41 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 18:01:41 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 18:01:41 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.050s CPU time.
Aug 23 18:02:59 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 18:03:00 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 18:03:00 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 18:04:08 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 18:04:09 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 18:04:09 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 18:05:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 18:05:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 18:05:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 18:06:38 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 18:06:40 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 18:06:40 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 18:06:40 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.043s CPU time.
Aug 23 18:07:45 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
