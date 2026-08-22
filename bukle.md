# Serverio būklė

Sugeneruota: 2026-08-22 14:48:06 CEST

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
HTTP 301, 0.001465s
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
Aug 22 14:47:30 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 22 14:47:30 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 22 14:47:59 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 22 14:48:00 vmi3306453 autoleft-deploy[3950921]: [2026-08-22 14:48:00] === Naujų commit'ų rasta: 9ee9b07 → 0b62625 ===
Aug 22 14:48:00 vmi3306453 autoleft-deploy[3950934]:     0b62625 feat(deploy): autodiegimas tikrina testus prieš liesdamas produkciją
Aug 22 14:48:00 vmi3306453 autoleft-deploy[3950921]: [2026-08-22 14:48:00] Kodas atnaujintas iki 0b62625
Aug 22 14:48:00 vmi3306453 autoleft-deploy[3950940]: [14:48:00] === Deploy pradžia (20260822_144800) ===
Aug 22 14:48:02 vmi3306453 autoleft-deploy[3950940]: [14:48:02] DB dumpas: /root/autoleft_backups/db_20260822_144800.sql
Aug 22 14:48:03 vmi3306453 autoleft-deploy[3950958]: Operations to perform:
Aug 22 14:48:03 vmi3306453 autoleft-deploy[3950958]:   Apply all migrations: accounts, admin, analytics, auth, broadcasts, contenttypes, conversations, listings, payments, sessions
Aug 22 14:48:03 vmi3306453 autoleft-deploy[3950958]: Running migrations:
Aug 22 14:48:03 vmi3306453 autoleft-deploy[3950958]:   No migrations to apply.
Aug 22 14:48:04 vmi3306453 autoleft-deploy[3950962]: 0 static files copied to '/root/autoleft/staticfiles', 140 unmodified.
Aug 22 14:48:04 vmi3306453 autoleft-deploy[3950940]: [14:48:04] Restartinam gunicorn.service
Aug 22 14:48:05 vmi3306453 autoleft-deploy[3950940]: [14:48:05] Health OK (1/10)
Aug 22 14:48:05 vmi3306453 autoleft-deploy[3950940]: [14:48:05] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Aug 22 14:48:06 vmi3306453 autoleft-deploy[3950940]: [14:48:06] === Deploy OK ===
Aug 22 14:48:06 vmi3306453 autoleft-deploy[3950921]: [2026-08-22 14:48:06] ✅ Deploy OK — gyvai veikia 0b62625
```
