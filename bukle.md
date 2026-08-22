# Serverio būklė

Sugeneruota: 2026-08-22 14:47:29 CEST

## Kodas

```
sukasi:      0b62625 feat(deploy): autodiegimas tikrina testus prieš liesdamas produkciją
origin/master: 0b62625 feat(deploy): autodiegimas tikrina testus prieš liesdamas produkciją
šaka:        master
darbo katalogas: švarus
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

Listing — iš viso 47
  active        32   MATOMAS
  draft         11   nematomas
  expired        4   nematomas
  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─
  nematomi dėl būsenos:      15
  iš jų pasibaigę (expires_at praeityje): 4
  aktyvūs, baigsis per 7 d.: 1
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
/dev/sda1       291G   14G  278G   5% /
```

## Paskutinis auto-deploy

```
Aug 22 14:46:17 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 22 14:46:20 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 22 14:46:20 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 22 14:46:20 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.111s CPU time.
Aug 22 14:47:29 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
