# Serverio būklė

Sugeneruota: 2026-09-01 14:37:35 CEST

## Kodas

```
sukasi:      9819c58 feat(paieska): šalies juosta virš greitosios paieškos panelės
origin/master: 9819c58 feat(paieska): šalies juosta virš greitosios paieškos panelės
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
HTTP 301, 0.001868s
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
/dev/sda1       291G   31G  260G  11% /
```

## Paskutinis auto-deploy

```
Sep 01 14:34:41 vmi3306453 autoleft-deploy[2636258]: Sep 01 14:34:05 vmi3306453 autoleft-deploy[2635795]: [14:34:05] === Deploy pradžia (20260901_143405) ===
Sep 01 14:34:41 vmi3306453 autoleft-deploy[2636258]: Sep 01 14:34:34 vmi3306453 autoleft-deploy[2635795]: [14:34:34] DB dumpas: /root/autoleft_backups/db_20260901_143405.sql
Sep 01 14:34:41 vmi3306453 autoleft-deploy[2636258]: Sep 01 14:34:35 vmi3306453 autoleft-deploy[2636102]: Operations to perform:
Sep 01 14:34:41 vmi3306453 autoleft-deploy[2636258]: Sep 01 14:34:35 vmi3306453 autoleft-deploy[2636102]:   Apply all migrations: accounts, admin, analytics, auth, broadcasts, contenttypes, conversations, imones, listings, payments, sessions
Sep 01 14:34:41 vmi3306453 autoleft-deploy[2636258]: Sep 01 14:34:35 vmi3306453 autoleft-deploy[2636102]: Running migrations:
Sep 01 14:34:41 vmi3306453 autoleft-deploy[2636258]: Sep 01 14:34:35 vmi3306453 autoleft-deploy[2636102]:   No migrations to apply.
Sep 01 14:34:41 vmi3306453 autoleft-deploy[2636258]: Sep 01 14:34:36 vmi3306453 autoleft-deploy[2636126]: 1 static file copied to '/root/autoleft/staticfiles', 170 unmodified.
Sep 01 14:34:41 vmi3306453 autoleft-deploy[2636258]: Sep 01 14:34:36 vmi3306453 autoleft-deploy[2635795]: [14:34:36] Restartinam gunicorn.service
Sep 01 14:34:41 vmi3306453 autoleft-deploy[2636258]: Sep 01 14:34:38 vmi3306453 autoleft-deploy[2635795]: [14:34:38] Health OK (1/10)
Sep 01 14:34:41 vmi3306453 autoleft-deploy[2636258]: Sep 01 14:34:38 vmi3306453 autoleft-deploy[2635795]: [14:34:38] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Sep 01 14:34:41 vmi3306453 autoleft-deploy[2636258]: Sep 01 14:34:38 vmi3306453 autoleft-deploy[2635795]: [14:34:38] === Deploy OK ===
Sep 01 14:34:41 vmi3306453 autoleft-deploy[2636258]: Sep 01 14:34:38 vmi3306453 autoleft-deploy[2635627]: [2026-09-01 14:34:38] ✅ Deploy OK — gyvai veikia 9819c58
Sep 01 14:34:41 vmi3306453 autoleft-deploy[2636258]: ```
Sep 01 14:34:41 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 01 14:34:41 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 14:34:41 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 22.053s CPU time.
Sep 01 14:35:15 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 01 14:35:17 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 01 14:35:17 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 14:35:17 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.868s CPU time.
Sep 01 14:36:24 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 01 14:36:26 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 01 14:36:26 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 14:36:26 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.463s CPU time.
Sep 01 14:37:34 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
