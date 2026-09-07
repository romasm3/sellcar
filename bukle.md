# Serverio būklė

Sugeneruota: 2026-09-07 11:34:52 CEST

## Kodas

```
sukasi:      acc75a5 fix(ikelimas): nuotraukų įkėlimas neveikė 12 iš 13 kalbų — 404 dėl kalbos priešdėlio
origin/master: acc75a5 fix(ikelimas): nuotraukų įkėlimas neveikė 12 iš 13 kalbų — 404 dėl kalbos priešdėlio
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
HTTP 301, 0.001562s
```

## Skelbimų būsenos

```

Listing — iš viso 36
  active        16   MATOMAS
  draft         10   nematomas
  expired       10   nematomas
  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─
  nematomi dėl būsenos:      20
  iš jų pasibaigę (expires_at praeityje): 10
  aktyvūs, baigsis per 7 d.: 5
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
/dev/sda1       291G   29G  263G  10% /
```

## Paskutinis auto-deploy

```
Sep 07 11:31:05 vmi3306453 autoleft-deploy[1042245]: Sep 07 11:30:58 vmi3306453 autoleft-deploy[1041187]: [11:30:58] Restartinam gunicorn.service
Sep 07 11:31:05 vmi3306453 autoleft-deploy[1042245]: Sep 07 11:31:01 vmi3306453 autoleft-deploy[1041187]: [11:31:01] Health OK (1/10)
Sep 07 11:31:05 vmi3306453 autoleft-deploy[1042245]: Sep 07 11:31:02 vmi3306453 autoleft-deploy[1041187]: [11:31:02] Statiniai OK: style.df8265b02e1b.css (manifestas atnaujintas)
Sep 07 11:31:05 vmi3306453 autoleft-deploy[1042245]: Sep 07 11:31:02 vmi3306453 autoleft-deploy[1041187]: [11:31:02] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Sep 07 11:31:05 vmi3306453 autoleft-deploy[1042245]: Sep 07 11:31:02 vmi3306453 autoleft-deploy[1041187]: [11:31:02] Raktai: .env — vietoje.
Sep 07 11:31:05 vmi3306453 autoleft-deploy[1042245]: Sep 07 11:31:02 vmi3306453 autoleft-deploy[1041187]: [11:31:02] Raktai: google-translate-key.json — vietoje.
Sep 07 11:31:05 vmi3306453 autoleft-deploy[1042245]: Sep 07 11:31:02 vmi3306453 autoleft-deploy[1041187]: [11:31:02] === Deploy OK ===
Sep 07 11:31:05 vmi3306453 autoleft-deploy[1042245]: Sep 07 11:31:02 vmi3306453 autoleft-deploy[1041014]: [2026-09-07 11:31:02] ✅ Deploy OK — gyvai veikia acc75a5
Sep 07 11:31:05 vmi3306453 autoleft-deploy[1042245]: ```
Sep 07 11:31:05 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 07 11:31:05 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 07 11:31:05 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1min 17.599s CPU time.
Sep 07 11:31:05 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 07 11:31:08 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 07 11:31:08 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 07 11:31:08 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.649s CPU time.
Sep 07 11:32:17 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 07 11:32:20 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 07 11:32:20 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 07 11:32:20 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.800s CPU time.
Sep 07 11:33:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 07 11:33:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 07 11:33:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 07 11:33:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.571s CPU time.
Sep 07 11:34:52 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
