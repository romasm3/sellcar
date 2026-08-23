# Serverio būklė

Sugeneruota: 2026-08-23 13:32:07 CEST

## Kodas

```
sukasi:      55cc9dd feat(i18n): ETAPAS 3 - vartotojo zona angliskai
origin/master: 55cc9dd feat(i18n): ETAPAS 3 - vartotojo zona angliskai
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
HTTP 301, 0.001052s
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
/dev/sda1       291G   14G  277G   5% /
```

## Paskutinis auto-deploy

```
Aug 23 13:28:04 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 13:28:05 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 13:28:05 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 13:29:14 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 13:29:16 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 13:29:16 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 13:30:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 13:30:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 13:30:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 13:31:56 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 13:31:56 vmi3306453 autoleft-deploy[4147575]: [2026-08-23 13:31:56] === Naujų commit'ų rasta: 55cc9dd → 31ee12f ===
Aug 23 13:31:56 vmi3306453 autoleft-deploy[4147575]: [2026-08-23 13:31:56] Kodas atnaujintas iki 31ee12f
Aug 23 13:32:03 vmi3306453 autoleft-deploy[4147575]: [2026-08-23 13:32:03] Patikra praėjo
Aug 23 13:32:03 vmi3306453 autoleft-deploy[4147711]: [13:32:03] === Deploy pradžia (20260823_133203) ===
Aug 23 13:32:04 vmi3306453 autoleft-deploy[4147711]: [13:32:04] DB dumpas: /root/autoleft_backups/db_20260823_133203.sql
Aug 23 13:32:05 vmi3306453 autoleft-deploy[4147727]: Operations to perform:
Aug 23 13:32:05 vmi3306453 autoleft-deploy[4147727]:   Apply all migrations: accounts, admin, analytics, auth, broadcasts, contenttypes, conversations, listings, payments, sessions
Aug 23 13:32:05 vmi3306453 autoleft-deploy[4147727]: Running migrations:
Aug 23 13:32:05 vmi3306453 autoleft-deploy[4147727]:   No migrations to apply.
Aug 23 13:32:06 vmi3306453 autoleft-deploy[4147732]: 0 static files copied to '/root/autoleft/staticfiles', 140 unmodified.
Aug 23 13:32:06 vmi3306453 autoleft-deploy[4147711]: [13:32:06] Restartinam gunicorn.service
Aug 23 13:32:07 vmi3306453 autoleft-deploy[4147711]: [13:32:07] Health OK (1/10)
Aug 23 13:32:07 vmi3306453 autoleft-deploy[4147711]: [13:32:07] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Aug 23 13:32:07 vmi3306453 autoleft-deploy[4147711]: [13:32:07] === Deploy OK ===
Aug 23 13:32:07 vmi3306453 autoleft-deploy[4147575]: [2026-08-23 13:32:07] ✅ Deploy OK — gyvai veikia 31ee12f
```
