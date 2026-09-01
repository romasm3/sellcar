# Serverio būklė

Sugeneruota: 2026-09-01 23:04:29 CEST

## Kodas

```
sukasi:      b42c6f9 fix(deploy): po atsukimo darbinis katalogas lieka švarus
origin/master: b42c6f9 fix(deploy): po atsukimo darbinis katalogas lieka švarus
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
HTTP 301, 0.002271s
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
/dev/sda1       291G   46G  246G  16% /
```

## Paskutinis auto-deploy

```
Sep 01 23:03:09 vmi3306453 autoleft-deploy[3013073]: Sep 01 23:02:08 vmi3306453 autoleft-deploy[3012112]: [2026-09-01 23:02:08] Kodas atnaujintas iki b42c6f9
Sep 01 23:03:09 vmi3306453 autoleft-deploy[3013073]: Sep 01 23:02:18 vmi3306453 autoleft-deploy[3012112]: [2026-09-01 23:02:18] Patikra praėjo
Sep 01 23:03:09 vmi3306453 autoleft-deploy[3013073]: Sep 01 23:02:18 vmi3306453 autoleft-deploy[3012326]: [23:02:18] === Deploy pradžia (20260901_230218) ===
Sep 01 23:03:09 vmi3306453 autoleft-deploy[3013073]: Sep 01 23:02:58 vmi3306453 autoleft-deploy[3012326]: [23:02:58] DB dumpas: /root/autoleft_backups/db_20260901_230218.sql
Sep 01 23:03:09 vmi3306453 autoleft-deploy[3013073]: Sep 01 23:02:58 vmi3306453 autoleft-deploy[3012326]: [23:02:58] Versija: b42c6f977a7a
Sep 01 23:03:09 vmi3306453 autoleft-deploy[3013073]: Sep 01 23:03:01 vmi3306453 autoleft-deploy[3012853]: Operations to perform:
Sep 01 23:03:09 vmi3306453 autoleft-deploy[3013073]: Sep 01 23:03:01 vmi3306453 autoleft-deploy[3012853]:   Apply all migrations: accounts, admin, analytics, auth, broadcasts, contenttypes, conversations, imones, listings, payments, sessions
Sep 01 23:03:09 vmi3306453 autoleft-deploy[3013073]: Sep 01 23:03:01 vmi3306453 autoleft-deploy[3012853]: Running migrations:
Sep 01 23:03:09 vmi3306453 autoleft-deploy[3013073]: Sep 01 23:03:01 vmi3306453 autoleft-deploy[3012853]:   No migrations to apply.
Sep 01 23:03:09 vmi3306453 autoleft-deploy[3013073]: Sep 01 23:03:03 vmi3306453 autoleft-deploy[3012898]: 0 static files copied to '/root/autoleft/staticfiles', 217 unmodified, 125 post-processed.
Sep 01 23:03:09 vmi3306453 autoleft-deploy[3013073]: Sep 01 23:03:03 vmi3306453 autoleft-deploy[3012326]: [23:03:03] Restartinam gunicorn.service
Sep 01 23:03:09 vmi3306453 autoleft-deploy[3013073]: Sep 01 23:03:05 vmi3306453 autoleft-deploy[3012326]: [23:03:05] Health OK (1/10)
Sep 01 23:03:09 vmi3306453 autoleft-deploy[3013073]: Sep 01 23:03:06 vmi3306453 autoleft-deploy[3012326]: [23:03:06] Statiniai OK: style.df8265b02e1b.css (manifestas atnaujintas)
Sep 01 23:03:09 vmi3306453 autoleft-deploy[3013073]: Sep 01 23:03:06 vmi3306453 autoleft-deploy[3012326]: [23:03:06] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Sep 01 23:03:09 vmi3306453 autoleft-deploy[3013073]: Sep 01 23:03:06 vmi3306453 autoleft-deploy[3012326]: [23:03:06] === Deploy OK ===
Sep 01 23:03:09 vmi3306453 autoleft-deploy[3013073]: Sep 01 23:03:06 vmi3306453 autoleft-deploy[3012112]: [2026-09-01 23:03:06] ✅ Deploy OK — gyvai veikia b42c6f9
Sep 01 23:03:09 vmi3306453 autoleft-deploy[3013073]: ```
Sep 01 23:03:09 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 01 23:03:09 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 23:03:09 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 24.691s CPU time.
Sep 01 23:03:15 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 01 23:03:17 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 01 23:03:17 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 23:03:17 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.732s CPU time.
Sep 01 23:04:28 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
