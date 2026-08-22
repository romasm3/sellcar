# Serverio būklė

Sugeneruota: 2026-08-23 00:01:24 CEST

## Kodas

```
sukasi:      300048f fix(mob): kategoriju pikerio eilutes telpa i ekrana
origin/master: 300048f fix(mob): kategoriju pikerio eilutes telpa i ekrana
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
HTTP 301, 0.001156s
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
Aug 23 00:00:20 vmi3306453 autoleft-deploy[4034724]: Aug 22 23:58:49 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 00:00:20 vmi3306453 autoleft-deploy[4034724]: Aug 22 23:58:51 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 00:00:20 vmi3306453 autoleft-deploy[4034724]: Aug 22 23:58:51 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 00:00:20 vmi3306453 autoleft-deploy[4034724]: Aug 22 23:59:59 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 00:00:20 vmi3306453 autoleft-deploy[4034724]: Aug 22 23:59:59 vmi3306453 autoleft-deploy[4034468]: [2026-08-22 23:59:59] === Naujų commit'ų rasta: 2414f26 → 300048f ===
Aug 23 00:00:20 vmi3306453 autoleft-deploy[4034724]: Aug 22 23:59:59 vmi3306453 autoleft-deploy[4034482]:     300048f fix(mob): kategoriju pikerio eilutes telpa i ekrana
Aug 23 00:00:20 vmi3306453 autoleft-deploy[4034724]: Aug 22 23:59:59 vmi3306453 autoleft-deploy[4034468]: [2026-08-22 23:59:59] Kodas atnaujintas iki 300048f
Aug 23 00:00:20 vmi3306453 autoleft-deploy[4034724]: Aug 23 00:00:12 vmi3306453 autoleft-deploy[4034468]: [2026-08-23 00:00:12] Patikra praėjo
Aug 23 00:00:20 vmi3306453 autoleft-deploy[4034724]: Aug 23 00:00:12 vmi3306453 autoleft-deploy[4034635]: [00:00:12] === Deploy pradžia (20260823_000012) ===
Aug 23 00:00:20 vmi3306453 autoleft-deploy[4034724]: Aug 23 00:00:15 vmi3306453 autoleft-deploy[4034635]: [00:00:15] DB dumpas: /root/autoleft_backups/db_20260823_000012.sql
Aug 23 00:00:20 vmi3306453 autoleft-deploy[4034724]: Aug 23 00:00:17 vmi3306453 autoleft-deploy[4034652]: Operations to perform:
Aug 23 00:00:20 vmi3306453 autoleft-deploy[4034724]: Aug 23 00:00:17 vmi3306453 autoleft-deploy[4034652]:   Apply all migrations: accounts, admin, analytics, auth, broadcasts, contenttypes, conversations, listings, payments, sessions
Aug 23 00:00:20 vmi3306453 autoleft-deploy[4034724]: Aug 23 00:00:17 vmi3306453 autoleft-deploy[4034652]: Running migrations:
Aug 23 00:00:20 vmi3306453 autoleft-deploy[4034724]: Aug 23 00:00:17 vmi3306453 autoleft-deploy[4034652]:   No migrations to apply.
Aug 23 00:00:20 vmi3306453 autoleft-deploy[4034724]: Aug 23 00:00:17 vmi3306453 autoleft-deploy[4034656]: 0 static files copied to '/root/autoleft/staticfiles', 140 unmodified.
Aug 23 00:00:20 vmi3306453 autoleft-deploy[4034724]: Aug 23 00:00:18 vmi3306453 autoleft-deploy[4034635]: [00:00:18] Restartinam gunicorn.service
Aug 23 00:00:20 vmi3306453 autoleft-deploy[4034724]: Aug 23 00:00:19 vmi3306453 autoleft-deploy[4034635]: [00:00:19] Health OK (1/10)
Aug 23 00:00:20 vmi3306453 autoleft-deploy[4034724]: Aug 23 00:00:19 vmi3306453 autoleft-deploy[4034635]: [00:00:19] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Aug 23 00:00:20 vmi3306453 autoleft-deploy[4034724]: Aug 23 00:00:19 vmi3306453 autoleft-deploy[4034635]: [00:00:19] === Deploy OK ===
Aug 23 00:00:20 vmi3306453 autoleft-deploy[4034724]: Aug 23 00:00:19 vmi3306453 autoleft-deploy[4034468]: [2026-08-23 00:00:19] ✅ Deploy OK — gyvai veikia 300048f
Aug 23 00:00:20 vmi3306453 autoleft-deploy[4034724]: ```
Aug 23 00:00:20 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 00:00:20 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 00:00:20 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 14.615s CPU time.
Aug 23 00:01:24 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
