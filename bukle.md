# Serverio būklė

Sugeneruota: 2026-09-02 15:19:44 CEST

## Kodas

```
sukasi:      e073f92 docs(ekranai): žinutės 360 ir 1600 px bei etalono nuotrauka
origin/master: e073f92 docs(ekranai): žinutės 360 ir 1600 px bei etalono nuotrauka
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
HTTP 301, 0.003143s
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
/dev/sda1       291G   49G  242G  17% /
```

## Paskutinis auto-deploy

```
Sep 02 15:18:18 vmi3306453 autoleft-deploy[3727769]: Sep 02 15:17:29 vmi3306453 autoleft-deploy[3727116]: [2026-09-02 15:17:29] Kodas atnaujintas iki e073f92
Sep 02 15:18:18 vmi3306453 autoleft-deploy[3727769]: Sep 02 15:17:38 vmi3306453 autoleft-deploy[3727116]: [2026-09-02 15:17:38] Patikra praėjo
Sep 02 15:18:18 vmi3306453 autoleft-deploy[3727769]: Sep 02 15:17:38 vmi3306453 autoleft-deploy[3727266]: [15:17:38] === Deploy pradžia (20260902_151738) ===
Sep 02 15:18:18 vmi3306453 autoleft-deploy[3727769]: Sep 02 15:18:07 vmi3306453 autoleft-deploy[3727266]: [15:18:07] DB dumpas: /root/autoleft_backups/db_20260902_151738.sql
Sep 02 15:18:18 vmi3306453 autoleft-deploy[3727769]: Sep 02 15:18:07 vmi3306453 autoleft-deploy[3727266]: [15:18:07] Versija: e073f9244cd7
Sep 02 15:18:18 vmi3306453 autoleft-deploy[3727769]: Sep 02 15:18:08 vmi3306453 autoleft-deploy[3727575]: Operations to perform:
Sep 02 15:18:18 vmi3306453 autoleft-deploy[3727769]: Sep 02 15:18:08 vmi3306453 autoleft-deploy[3727575]:   Apply all migrations: accounts, admin, analytics, auth, broadcasts, contenttypes, conversations, imones, listings, payments, sessions
Sep 02 15:18:18 vmi3306453 autoleft-deploy[3727769]: Sep 02 15:18:08 vmi3306453 autoleft-deploy[3727575]: Running migrations:
Sep 02 15:18:18 vmi3306453 autoleft-deploy[3727769]: Sep 02 15:18:08 vmi3306453 autoleft-deploy[3727575]:   No migrations to apply.
Sep 02 15:18:18 vmi3306453 autoleft-deploy[3727769]: Sep 02 15:18:09 vmi3306453 autoleft-deploy[3727597]: 0 static files copied to '/root/autoleft/staticfiles', 218 unmodified, 126 post-processed.
Sep 02 15:18:18 vmi3306453 autoleft-deploy[3727769]: Sep 02 15:18:09 vmi3306453 autoleft-deploy[3727266]: [15:18:09] Restartinam gunicorn.service
Sep 02 15:18:18 vmi3306453 autoleft-deploy[3727769]: Sep 02 15:18:11 vmi3306453 autoleft-deploy[3727266]: [15:18:11] Health OK (1/10)
Sep 02 15:18:18 vmi3306453 autoleft-deploy[3727769]: Sep 02 15:18:12 vmi3306453 autoleft-deploy[3727266]: [15:18:12] Statiniai OK: style.df8265b02e1b.css (manifestas atnaujintas)
Sep 02 15:18:18 vmi3306453 autoleft-deploy[3727769]: Sep 02 15:18:12 vmi3306453 autoleft-deploy[3727266]: [15:18:12] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Sep 02 15:18:18 vmi3306453 autoleft-deploy[3727769]: Sep 02 15:18:12 vmi3306453 autoleft-deploy[3727266]: [15:18:12] === Deploy OK ===
Sep 02 15:18:18 vmi3306453 autoleft-deploy[3727769]: Sep 02 15:18:12 vmi3306453 autoleft-deploy[3727116]: [2026-09-02 15:18:12] ✅ Deploy OK — gyvai veikia e073f92
Sep 02 15:18:18 vmi3306453 autoleft-deploy[3727769]: ```
Sep 02 15:18:18 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 15:18:18 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 15:18:18 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 21.961s CPU time.
Sep 02 15:18:37 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 15:18:39 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 15:18:39 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 15:18:39 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.409s CPU time.
Sep 02 15:19:43 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
