# Serverio būklė

Sugeneruota: 2026-08-24 12:47:26 CEST

## Kodas

```
sukasi:      f689648 fix(rezultatai): vienas „Išsaugoti paiešką", kortelės be miniatiūrų, akcento spalva
origin/master: f689648 fix(rezultatai): vienas „Išsaugoti paiešką", kortelės be miniatiūrų, akcento spalva
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
HTTP 301, 0.001928s
```

## Skelbimų būsenos

```

Listing — iš viso 35
  active        23   MATOMAS
  draft          9   nematomas
  expired        3   nematomas
  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─
  nematomi dėl būsenos:      12
  iš jų pasibaigę (expires_at praeityje): 3
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
/dev/sda1       291G   15G  277G   5% /
```

## Paskutinis auto-deploy

```
Aug 24 12:43:25 vmi3306453 autoleft-deploy[167541]: Aug 24 12:43:20 vmi3306453 autoleft-deploy[167307]: [2026-08-24 12:43:20] Patikra praėjo
Aug 24 12:43:25 vmi3306453 autoleft-deploy[167541]: Aug 24 12:43:20 vmi3306453 autoleft-deploy[167448]: [12:43:20] === Deploy pradžia (20260824_124320) ===
Aug 24 12:43:25 vmi3306453 autoleft-deploy[167541]: Aug 24 12:43:21 vmi3306453 autoleft-deploy[167448]: [12:43:21] DB dumpas: /root/autoleft_backups/db_20260824_124320.sql
Aug 24 12:43:25 vmi3306453 autoleft-deploy[167541]: Aug 24 12:43:22 vmi3306453 autoleft-deploy[167463]: Operations to perform:
Aug 24 12:43:25 vmi3306453 autoleft-deploy[167541]: Aug 24 12:43:22 vmi3306453 autoleft-deploy[167463]:   Apply all migrations: accounts, admin, analytics, auth, broadcasts, contenttypes, conversations, listings, payments, sessions
Aug 24 12:43:25 vmi3306453 autoleft-deploy[167541]: Aug 24 12:43:22 vmi3306453 autoleft-deploy[167463]: Running migrations:
Aug 24 12:43:25 vmi3306453 autoleft-deploy[167541]: Aug 24 12:43:22 vmi3306453 autoleft-deploy[167463]:   No migrations to apply.
Aug 24 12:43:25 vmi3306453 autoleft-deploy[167541]: Aug 24 12:43:23 vmi3306453 autoleft-deploy[167470]: 0 static files copied to '/root/autoleft/staticfiles', 140 unmodified.
Aug 24 12:43:25 vmi3306453 autoleft-deploy[167541]: Aug 24 12:43:23 vmi3306453 autoleft-deploy[167448]: [12:43:23] Restartinam gunicorn.service
Aug 24 12:43:25 vmi3306453 autoleft-deploy[167541]: Aug 24 12:43:24 vmi3306453 autoleft-deploy[167448]: [12:43:24] Health OK (1/10)
Aug 24 12:43:25 vmi3306453 autoleft-deploy[167541]: Aug 24 12:43:24 vmi3306453 autoleft-deploy[167448]: [12:43:24] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Aug 24 12:43:25 vmi3306453 autoleft-deploy[167541]: Aug 24 12:43:24 vmi3306453 autoleft-deploy[167448]: [12:43:24] === Deploy OK ===
Aug 24 12:43:25 vmi3306453 autoleft-deploy[167541]: Aug 24 12:43:24 vmi3306453 autoleft-deploy[167307]: [2026-08-24 12:43:24] ✅ Deploy OK — gyvai veikia 3f85319
Aug 24 12:43:25 vmi3306453 autoleft-deploy[167541]: ```
Aug 24 12:43:25 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 12:43:25 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 12:43:25 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 8.392s CPU time.
Aug 24 12:44:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 12:44:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 12:44:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 12:44:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.045s CPU time.
Aug 24 12:45:42 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 12:45:43 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 12:45:43 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 12:47:25 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
