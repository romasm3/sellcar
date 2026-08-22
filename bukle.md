# Serverio būklė

Sugeneruota: 2026-08-22 22:39:08 CEST

## Kodas

```
sukasi:      143fa15 Merge remote-tracking branch 'origin/master'
origin/master: 143fa15 Merge remote-tracking branch 'origin/master'
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
HTTP 301, 0.000910s
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
Aug 22 22:34:53 vmi3306453 autoleft-deploy[4015859]: Aug 22 22:34:49 vmi3306453 autoleft-deploy[4015766]: [22:34:49] DB dumpas: /root/autoleft_backups/db_20260822_223448.sql
Aug 22 22:34:53 vmi3306453 autoleft-deploy[4015859]: Aug 22 22:34:50 vmi3306453 autoleft-deploy[4015783]: Operations to perform:
Aug 22 22:34:53 vmi3306453 autoleft-deploy[4015859]: Aug 22 22:34:50 vmi3306453 autoleft-deploy[4015783]:   Apply all migrations: accounts, admin, analytics, auth, broadcasts, contenttypes, conversations, listings, payments, sessions
Aug 22 22:34:53 vmi3306453 autoleft-deploy[4015859]: Aug 22 22:34:50 vmi3306453 autoleft-deploy[4015783]: Running migrations:
Aug 22 22:34:53 vmi3306453 autoleft-deploy[4015859]: Aug 22 22:34:50 vmi3306453 autoleft-deploy[4015783]:   No migrations to apply.
Aug 22 22:34:53 vmi3306453 autoleft-deploy[4015859]: Aug 22 22:34:51 vmi3306453 autoleft-deploy[4015788]: 0 static files copied to '/root/autoleft/staticfiles', 140 unmodified.
Aug 22 22:34:53 vmi3306453 autoleft-deploy[4015859]: Aug 22 22:34:51 vmi3306453 autoleft-deploy[4015766]: [22:34:51] Restartinam gunicorn.service
Aug 22 22:34:53 vmi3306453 autoleft-deploy[4015859]: Aug 22 22:34:52 vmi3306453 autoleft-deploy[4015766]: [22:34:52] Health OK (1/10)
Aug 22 22:34:53 vmi3306453 autoleft-deploy[4015859]: Aug 22 22:34:52 vmi3306453 autoleft-deploy[4015766]: [22:34:52] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Aug 22 22:34:53 vmi3306453 autoleft-deploy[4015859]: Aug 22 22:34:52 vmi3306453 autoleft-deploy[4015766]: [22:34:52] === Deploy OK ===
Aug 22 22:34:53 vmi3306453 autoleft-deploy[4015859]: Aug 22 22:34:52 vmi3306453 autoleft-deploy[4015726]: [2026-08-22 22:34:52] ✅ Deploy OK — gyvai veikia 143fa15
Aug 22 22:34:53 vmi3306453 autoleft-deploy[4015859]: ```
Aug 22 22:34:53 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 22 22:34:53 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 22 22:34:53 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 8.042s CPU time.
Aug 22 22:35:51 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 22 22:35:53 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 22 22:35:53 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 22 22:36:58 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 22 22:36:59 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 22 22:36:59 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 22 22:38:03 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 22 22:38:04 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 22 22:38:04 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 22 22:39:08 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
