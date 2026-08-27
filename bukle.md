# Serverio būklė

Sugeneruota: 2026-08-27 12:02:45 CEST

## Kodas

```
sukasi:      2b2510f feat(žemėlapis): žemėlapio paieška dviem stulpeliais su filtrų langu
origin/master: 2b2510f feat(žemėlapis): žemėlapio paieška dviem stulpeliais su filtrų langu
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
HTTP 301, 0.001211s
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
/dev/sda1       291G   18G  274G   6% /
```

## Paskutinis auto-deploy

```
Aug 27 11:59:23 vmi3306453 autoleft-deploy[1858945]: Aug 27 11:59:11 vmi3306453 autoleft-deploy[1858778]: [11:59:11] === Deploy pradžia (20260827_115911) ===
Aug 27 11:59:23 vmi3306453 autoleft-deploy[1858945]: Aug 27 11:59:18 vmi3306453 autoleft-deploy[1858778]: [11:59:18] DB dumpas: /root/autoleft_backups/db_20260827_115911.sql
Aug 27 11:59:23 vmi3306453 autoleft-deploy[1858945]: Aug 27 11:59:19 vmi3306453 autoleft-deploy[1858845]: Operations to perform:
Aug 27 11:59:23 vmi3306453 autoleft-deploy[1858945]: Aug 27 11:59:19 vmi3306453 autoleft-deploy[1858845]:   Apply all migrations: accounts, admin, analytics, auth, broadcasts, contenttypes, conversations, listings, payments, sessions
Aug 27 11:59:23 vmi3306453 autoleft-deploy[1858945]: Aug 27 11:59:19 vmi3306453 autoleft-deploy[1858845]: Running migrations:
Aug 27 11:59:23 vmi3306453 autoleft-deploy[1858945]: Aug 27 11:59:19 vmi3306453 autoleft-deploy[1858845]:   No migrations to apply.
Aug 27 11:59:23 vmi3306453 autoleft-deploy[1858945]: Aug 27 11:59:20 vmi3306453 autoleft-deploy[1858860]: 0 static files copied to '/root/autoleft/staticfiles', 163 unmodified.
Aug 27 11:59:23 vmi3306453 autoleft-deploy[1858945]: Aug 27 11:59:20 vmi3306453 autoleft-deploy[1858778]: [11:59:20] Restartinam gunicorn.service
Aug 27 11:59:23 vmi3306453 autoleft-deploy[1858945]: Aug 27 11:59:21 vmi3306453 autoleft-deploy[1858778]: [11:59:21] Health OK (1/10)
Aug 27 11:59:23 vmi3306453 autoleft-deploy[1858945]: Aug 27 11:59:21 vmi3306453 autoleft-deploy[1858778]: [11:59:21] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Aug 27 11:59:23 vmi3306453 autoleft-deploy[1858945]: Aug 27 11:59:21 vmi3306453 autoleft-deploy[1858778]: [11:59:21] === Deploy OK ===
Aug 27 11:59:23 vmi3306453 autoleft-deploy[1858945]: Aug 27 11:59:21 vmi3306453 autoleft-deploy[1858584]: [2026-08-27 11:59:21] ✅ Deploy OK — gyvai veikia 576a247
Aug 27 11:59:23 vmi3306453 autoleft-deploy[1858945]: ```
Aug 27 11:59:23 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 11:59:23 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 11:59:23 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 10.972s CPU time.
Aug 27 12:00:25 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 12:00:27 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 12:00:27 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 12:00:27 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.156s CPU time.
Aug 27 12:01:34 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 12:01:35 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 12:01:35 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 12:01:35 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.217s CPU time.
Aug 27 12:02:45 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
