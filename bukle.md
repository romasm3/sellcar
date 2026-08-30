# Serverio būklė

Sugeneruota: 2026-08-30 20:55:53 CEST

## Kodas

```
sukasi:      8dd8851 feat(vertimai): lt/en per i18n_patterns, įmonių puslapiai išversti, sargybos testai
origin/master: 8dd8851 feat(vertimai): lt/en per i18n_patterns, įmonių puslapiai išversti, sargybos testai
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
HTTP 301, 0.001368s
```

## Skelbimų būsenos

```

Listing — iš viso 35
  active        22   MATOMAS
  draft          9   nematomas
  expired        4   nematomas
  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─
  nematomi dėl būsenos:      13
  iš jų pasibaigę (expires_at praeityje): 4
  aktyvūs, baigsis per 7 d.: 3
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
/dev/sda1       291G   23G  268G   8% /
```

## Paskutinis auto-deploy

```
Aug 30 20:52:17 vmi3306453 autoleft-deploy[857747]: Aug 30 20:51:46 vmi3306453 autoleft-deploy[857207]: [20:51:46] === Deploy pradžia (20260830_205146) ===
Aug 30 20:52:17 vmi3306453 autoleft-deploy[857747]: Aug 30 20:52:07 vmi3306453 autoleft-deploy[857207]: [20:52:07] DB dumpas: /root/autoleft_backups/db_20260830_205146.sql
Aug 30 20:52:17 vmi3306453 autoleft-deploy[857747]: Aug 30 20:52:09 vmi3306453 autoleft-deploy[857552]: Operations to perform:
Aug 30 20:52:17 vmi3306453 autoleft-deploy[857747]: Aug 30 20:52:09 vmi3306453 autoleft-deploy[857552]:   Apply all migrations: accounts, admin, analytics, auth, broadcasts, contenttypes, conversations, imones, listings, payments, sessions
Aug 30 20:52:17 vmi3306453 autoleft-deploy[857747]: Aug 30 20:52:09 vmi3306453 autoleft-deploy[857552]: Running migrations:
Aug 30 20:52:17 vmi3306453 autoleft-deploy[857747]: Aug 30 20:52:09 vmi3306453 autoleft-deploy[857552]:   No migrations to apply.
Aug 30 20:52:17 vmi3306453 autoleft-deploy[857747]: Aug 30 20:52:10 vmi3306453 autoleft-deploy[857589]: 0 static files copied to '/root/autoleft/staticfiles', 170 unmodified.
Aug 30 20:52:17 vmi3306453 autoleft-deploy[857747]: Aug 30 20:52:10 vmi3306453 autoleft-deploy[857207]: [20:52:10] Restartinam gunicorn.service
Aug 30 20:52:17 vmi3306453 autoleft-deploy[857747]: Aug 30 20:52:12 vmi3306453 autoleft-deploy[857207]: [20:52:12] Health OK (1/10)
Aug 30 20:52:17 vmi3306453 autoleft-deploy[857747]: Aug 30 20:52:12 vmi3306453 autoleft-deploy[857207]: [20:52:12] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Aug 30 20:52:17 vmi3306453 autoleft-deploy[857747]: Aug 30 20:52:12 vmi3306453 autoleft-deploy[857207]: [20:52:12] === Deploy OK ===
Aug 30 20:52:17 vmi3306453 autoleft-deploy[857747]: Aug 30 20:52:12 vmi3306453 autoleft-deploy[857038]: [2026-08-30 20:52:12] ✅ Deploy OK — gyvai veikia c853bdf
Aug 30 20:52:17 vmi3306453 autoleft-deploy[857747]: ```
Aug 30 20:52:17 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 30 20:52:17 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 30 20:52:17 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 17.066s CPU time.
Aug 30 20:53:10 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 30 20:53:12 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 30 20:53:12 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 30 20:53:12 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.412s CPU time.
Aug 30 20:54:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 30 20:54:33 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 30 20:54:33 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 30 20:54:33 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.419s CPU time.
Aug 30 20:55:53 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
