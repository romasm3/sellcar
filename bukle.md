# Serverio būklė

Sugeneruota: 2026-08-24 12:31:49 CEST

## Kodas

```
sukasi:      d91ce8e feat(skelbimai): laiko žyma visiems skelbimams, LT skaičių ir kainų formatas
origin/master: cd36a44 merge: master (išsaugotų skelbimų pastabos)
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
HTTP 301, 0.000821s
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
Aug 24 12:28:24 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 12:28:24 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 12:29:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 12:29:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 12:29:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 12:30:35 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 12:30:36 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 12:30:36 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 12:30:36 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.075s CPU time.
Aug 24 12:31:39 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 12:31:39 vmi3306453 autoleft-deploy[162132]: [2026-08-24 12:31:39] === Naujų commit'ų rasta: d91ce8e → cd36a44 ===
Aug 24 12:31:39 vmi3306453 autoleft-deploy[162132]: [2026-08-24 12:31:39] Kodas atnaujintas iki cd36a44
Aug 24 12:31:45 vmi3306453 autoleft-deploy[162132]: [2026-08-24 12:31:45] Patikra praėjo
Aug 24 12:31:45 vmi3306453 autoleft-deploy[162171]: [12:31:45] === Deploy pradžia (20260824_123145) ===
Aug 24 12:31:46 vmi3306453 autoleft-deploy[162171]: [12:31:46] DB dumpas: /root/autoleft_backups/db_20260824_123145.sql
Aug 24 12:31:47 vmi3306453 autoleft-deploy[162189]: Operations to perform:
Aug 24 12:31:47 vmi3306453 autoleft-deploy[162189]:   Apply all migrations: accounts, admin, analytics, auth, broadcasts, contenttypes, conversations, listings, payments, sessions
Aug 24 12:31:47 vmi3306453 autoleft-deploy[162189]: Running migrations:
Aug 24 12:31:47 vmi3306453 autoleft-deploy[162189]:   No migrations to apply.
Aug 24 12:31:48 vmi3306453 autoleft-deploy[162220]: 1 static file copied to '/root/autoleft/staticfiles', 139 unmodified.
Aug 24 12:31:48 vmi3306453 autoleft-deploy[162171]: [12:31:48] Restartinam gunicorn.service
Aug 24 12:31:49 vmi3306453 autoleft-deploy[162171]: [12:31:49] Health OK (1/10)
Aug 24 12:31:49 vmi3306453 autoleft-deploy[162171]: [12:31:49] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Aug 24 12:31:49 vmi3306453 autoleft-deploy[162171]: [12:31:49] === Deploy OK ===
Aug 24 12:31:49 vmi3306453 autoleft-deploy[162132]: [2026-08-24 12:31:49] ✅ Deploy OK — gyvai veikia cd36a44
```
