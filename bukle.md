# Serverio būklė

Sugeneruota: 2026-08-23 00:06:43 CEST

## Kodas

```
sukasi:      f58f1d0 fix(mob): kategoriju pikeris pagal etalona — ikona desineje, vardai laužiasi
origin/master: f58f1d0 fix(mob): kategoriju pikeris pagal etalona — ikona desineje, vardai laužiasi
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
HTTP 301, 0.001387s
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
Aug 23 00:05:43 vmi3306453 autoleft-deploy[4035271]: Aug 23 00:03:43 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 00:05:43 vmi3306453 autoleft-deploy[4035271]: Aug 23 00:03:44 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 00:05:43 vmi3306453 autoleft-deploy[4035271]: Aug 23 00:03:44 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 00:05:43 vmi3306453 autoleft-deploy[4035271]: Aug 23 00:05:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 00:05:43 vmi3306453 autoleft-deploy[4035271]: Aug 23 00:05:31 vmi3306453 autoleft-deploy[4035132]: [2026-08-23 00:05:31] === Naujų commit'ų rasta: 300048f → f58f1d0 ===
Aug 23 00:05:43 vmi3306453 autoleft-deploy[4035271]: Aug 23 00:05:31 vmi3306453 autoleft-deploy[4035147]:     f58f1d0 fix(mob): kategoriju pikeris pagal etalona — ikona desineje, vardai laužiasi
Aug 23 00:05:43 vmi3306453 autoleft-deploy[4035271]: Aug 23 00:05:31 vmi3306453 autoleft-deploy[4035132]: [2026-08-23 00:05:31] Kodas atnaujintas iki f58f1d0
Aug 23 00:05:43 vmi3306453 autoleft-deploy[4035271]: Aug 23 00:05:38 vmi3306453 autoleft-deploy[4035132]: [2026-08-23 00:05:38] Patikra praėjo
Aug 23 00:05:43 vmi3306453 autoleft-deploy[4035271]: Aug 23 00:05:38 vmi3306453 autoleft-deploy[4035176]: [00:05:38] === Deploy pradžia (20260823_000538) ===
Aug 23 00:05:43 vmi3306453 autoleft-deploy[4035271]: Aug 23 00:05:39 vmi3306453 autoleft-deploy[4035176]: [00:05:39] DB dumpas: /root/autoleft_backups/db_20260823_000538.sql
Aug 23 00:05:43 vmi3306453 autoleft-deploy[4035271]: Aug 23 00:05:40 vmi3306453 autoleft-deploy[4035191]: Operations to perform:
Aug 23 00:05:43 vmi3306453 autoleft-deploy[4035271]: Aug 23 00:05:40 vmi3306453 autoleft-deploy[4035191]:   Apply all migrations: accounts, admin, analytics, auth, broadcasts, contenttypes, conversations, listings, payments, sessions
Aug 23 00:05:43 vmi3306453 autoleft-deploy[4035271]: Aug 23 00:05:40 vmi3306453 autoleft-deploy[4035191]: Running migrations:
Aug 23 00:05:43 vmi3306453 autoleft-deploy[4035271]: Aug 23 00:05:40 vmi3306453 autoleft-deploy[4035191]:   No migrations to apply.
Aug 23 00:05:43 vmi3306453 autoleft-deploy[4035271]: Aug 23 00:05:40 vmi3306453 autoleft-deploy[4035196]: 0 static files copied to '/root/autoleft/staticfiles', 140 unmodified.
Aug 23 00:05:43 vmi3306453 autoleft-deploy[4035271]: Aug 23 00:05:40 vmi3306453 autoleft-deploy[4035176]: [00:05:40] Restartinam gunicorn.service
Aug 23 00:05:43 vmi3306453 autoleft-deploy[4035271]: Aug 23 00:05:41 vmi3306453 autoleft-deploy[4035176]: [00:05:41] Health OK (1/10)
Aug 23 00:05:43 vmi3306453 autoleft-deploy[4035271]: Aug 23 00:05:41 vmi3306453 autoleft-deploy[4035176]: [00:05:41] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Aug 23 00:05:43 vmi3306453 autoleft-deploy[4035271]: Aug 23 00:05:41 vmi3306453 autoleft-deploy[4035176]: [00:05:41] === Deploy OK ===
Aug 23 00:05:43 vmi3306453 autoleft-deploy[4035271]: Aug 23 00:05:41 vmi3306453 autoleft-deploy[4035132]: [2026-08-23 00:05:41] ✅ Deploy OK — gyvai veikia f58f1d0
Aug 23 00:05:43 vmi3306453 autoleft-deploy[4035271]: ```
Aug 23 00:05:43 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 00:05:43 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 00:05:43 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 8.933s CPU time.
Aug 23 00:06:43 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
