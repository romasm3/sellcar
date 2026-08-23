# Serverio būklė

Sugeneruota: 2026-08-23 15:46:41 CEST

## Kodas

```
sukasi:      7e04dd8 fix(i18n): telefono filtrų ekranas išverstas — „Gerai" rodė lietuviškai
origin/master: 7e04dd8 fix(i18n): telefono filtrų ekranas išverstas — „Gerai" rodė lietuviškai
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
HTTP 301, 0.001804s
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
Aug 23 15:45:47 vmi3306453 autoleft-deploy[4172378]: Aug 23 15:44:26 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 15:45:47 vmi3306453 autoleft-deploy[4172378]: Aug 23 15:44:26 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 15:45:47 vmi3306453 autoleft-deploy[4172378]: Aug 23 15:44:26 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.024s CPU time.
Aug 23 15:45:47 vmi3306453 autoleft-deploy[4172378]: Aug 23 15:45:32 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 15:45:47 vmi3306453 autoleft-deploy[4172378]: Aug 23 15:45:33 vmi3306453 autoleft-deploy[4172153]: [2026-08-23 15:45:33] === Naujų commit'ų rasta: 4d1d356 → 7e04dd8 ===
Aug 23 15:45:47 vmi3306453 autoleft-deploy[4172378]: Aug 23 15:45:33 vmi3306453 autoleft-deploy[4172169]:     7e04dd8 fix(i18n): telefono filtrų ekranas išverstas — „Gerai" rodė lietuviškai
Aug 23 15:45:47 vmi3306453 autoleft-deploy[4172378]: Aug 23 15:45:33 vmi3306453 autoleft-deploy[4172153]: [2026-08-23 15:45:33] Kodas atnaujintas iki 7e04dd8
Aug 23 15:45:47 vmi3306453 autoleft-deploy[4172378]: Aug 23 15:45:41 vmi3306453 autoleft-deploy[4172153]: [2026-08-23 15:45:41] Patikra praėjo
Aug 23 15:45:47 vmi3306453 autoleft-deploy[4172378]: Aug 23 15:45:41 vmi3306453 autoleft-deploy[4172260]: [15:45:41] === Deploy pradžia (20260823_154541) ===
Aug 23 15:45:47 vmi3306453 autoleft-deploy[4172378]: Aug 23 15:45:43 vmi3306453 autoleft-deploy[4172260]: [15:45:43] DB dumpas: /root/autoleft_backups/db_20260823_154541.sql
Aug 23 15:45:47 vmi3306453 autoleft-deploy[4172378]: Aug 23 15:45:44 vmi3306453 autoleft-deploy[4172277]: Operations to perform:
Aug 23 15:45:47 vmi3306453 autoleft-deploy[4172378]: Aug 23 15:45:44 vmi3306453 autoleft-deploy[4172277]:   Apply all migrations: accounts, admin, analytics, auth, broadcasts, contenttypes, conversations, listings, payments, sessions
Aug 23 15:45:47 vmi3306453 autoleft-deploy[4172378]: Aug 23 15:45:44 vmi3306453 autoleft-deploy[4172277]: Running migrations:
Aug 23 15:45:47 vmi3306453 autoleft-deploy[4172378]: Aug 23 15:45:44 vmi3306453 autoleft-deploy[4172277]:   No migrations to apply.
Aug 23 15:45:47 vmi3306453 autoleft-deploy[4172378]: Aug 23 15:45:44 vmi3306453 autoleft-deploy[4172284]: 0 static files copied to '/root/autoleft/staticfiles', 140 unmodified.
Aug 23 15:45:47 vmi3306453 autoleft-deploy[4172378]: Aug 23 15:45:44 vmi3306453 autoleft-deploy[4172260]: [15:45:44] Restartinam gunicorn.service
Aug 23 15:45:47 vmi3306453 autoleft-deploy[4172378]: Aug 23 15:45:45 vmi3306453 autoleft-deploy[4172260]: [15:45:45] Health OK (1/10)
Aug 23 15:45:47 vmi3306453 autoleft-deploy[4172378]: Aug 23 15:45:45 vmi3306453 autoleft-deploy[4172260]: [15:45:45] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Aug 23 15:45:47 vmi3306453 autoleft-deploy[4172378]: Aug 23 15:45:45 vmi3306453 autoleft-deploy[4172260]: [15:45:45] === Deploy OK ===
Aug 23 15:45:47 vmi3306453 autoleft-deploy[4172378]: Aug 23 15:45:45 vmi3306453 autoleft-deploy[4172153]: [2026-08-23 15:45:45] ✅ Deploy OK — gyvai veikia 7e04dd8
Aug 23 15:45:47 vmi3306453 autoleft-deploy[4172378]: ```
Aug 23 15:45:47 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 15:45:47 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 15:45:47 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 10.549s CPU time.
Aug 23 15:46:40 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
