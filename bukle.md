# Serverio būklė

Sugeneruota: 2026-09-01 15:07:29 CEST

## Kodas

```
sukasi:      1f15a48 docs(taisykles): vieta yra svarbiausias filtras + feat(veliavos): SVG prie vietos
origin/master: 1f15a48 docs(taisykles): vieta yra svarbiausias filtras + feat(veliavos): SVG prie vietos
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
HTTP 301, 0.001178s
```

## Skelbimų būsenos

```

Listing — iš viso 35
  active        19   MATOMAS
  draft          9   nematomas
  expired        7   nematomas
  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─
  nematomi dėl būsenos:      16
  iš jų pasibaigę (expires_at praeityje): 7
  aktyvūs, baigsis per 7 d.: 4
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
/dev/sda1       291G   33G  258G  12% /
```

## Paskutinis auto-deploy

```
Sep 01 15:04:23 vmi3306453 autoleft-deploy[2657276]: Sep 01 15:03:45 vmi3306453 autoleft-deploy[2656809]: [15:03:45] === Deploy pradžia (20260901_150345) ===
Sep 01 15:04:23 vmi3306453 autoleft-deploy[2657276]: Sep 01 15:04:15 vmi3306453 autoleft-deploy[2656809]: [15:04:15] DB dumpas: /root/autoleft_backups/db_20260901_150345.sql
Sep 01 15:04:23 vmi3306453 autoleft-deploy[2657276]: Sep 01 15:04:16 vmi3306453 autoleft-deploy[2657133]: Operations to perform:
Sep 01 15:04:23 vmi3306453 autoleft-deploy[2657276]: Sep 01 15:04:16 vmi3306453 autoleft-deploy[2657133]:   Apply all migrations: accounts, admin, analytics, auth, broadcasts, contenttypes, conversations, imones, listings, payments, sessions
Sep 01 15:04:23 vmi3306453 autoleft-deploy[2657276]: Sep 01 15:04:16 vmi3306453 autoleft-deploy[2657133]: Running migrations:
Sep 01 15:04:23 vmi3306453 autoleft-deploy[2657276]: Sep 01 15:04:16 vmi3306453 autoleft-deploy[2657133]:   No migrations to apply.
Sep 01 15:04:23 vmi3306453 autoleft-deploy[2657276]: Sep 01 15:04:17 vmi3306453 autoleft-deploy[2657158]: 45 static files copied to '/root/autoleft/staticfiles', 170 unmodified.
Sep 01 15:04:23 vmi3306453 autoleft-deploy[2657276]: Sep 01 15:04:18 vmi3306453 autoleft-deploy[2656809]: [15:04:18] Restartinam gunicorn.service
Sep 01 15:04:23 vmi3306453 autoleft-deploy[2657276]: Sep 01 15:04:19 vmi3306453 autoleft-deploy[2656809]: [15:04:19] Health OK (1/10)
Sep 01 15:04:23 vmi3306453 autoleft-deploy[2657276]: Sep 01 15:04:19 vmi3306453 autoleft-deploy[2656809]: [15:04:19] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Sep 01 15:04:23 vmi3306453 autoleft-deploy[2657276]: Sep 01 15:04:20 vmi3306453 autoleft-deploy[2656809]: [15:04:20] === Deploy OK ===
Sep 01 15:04:23 vmi3306453 autoleft-deploy[2657276]: Sep 01 15:04:20 vmi3306453 autoleft-deploy[2656663]: [2026-09-01 15:04:20] ✅ Deploy OK — gyvai veikia 1f15a48
Sep 01 15:04:23 vmi3306453 autoleft-deploy[2657276]: ```
Sep 01 15:04:23 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 01 15:04:23 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 15:04:23 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 21.386s CPU time.
Sep 01 15:04:51 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 01 15:04:53 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 01 15:04:53 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 15:04:53 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.452s CPU time.
Sep 01 15:06:21 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 01 15:06:23 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 01 15:06:23 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 15:06:23 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.442s CPU time.
Sep 01 15:07:29 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
