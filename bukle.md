# Serverio būklė

Sugeneruota: 2026-09-01 19:51:24 CEST

## Kodas

```
sukasi:      9f0c6aa fix(pastas): laiškai iškelti iš užklausos į foną
origin/master: 9f0c6aa fix(pastas): laiškai iškelti iš užklausos į foną
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
HTTP 301, 0.002033s
```

## Skelbimų būsenos

```

Listing — iš viso 35
  active        19   MATOMAS
  draft          9   nematomas
  expired        7   nematomas
  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─
  nematomi dėl būsenos:      16
  iš jų pasibaigę (expires_at praeityje): 7
  aktyvūs, baigsis per 7 d.: 5
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
/dev/sda1       291G   44G  247G  16% /
```

## Paskutinis auto-deploy

```
Sep 01 19:51:00 vmi3306453 autoleft-deploy[2870169]: Sep 01 19:48:56 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 01 19:51:00 vmi3306453 autoleft-deploy[2870169]: Sep 01 19:48:56 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 19:51:00 vmi3306453 autoleft-deploy[2870169]: Sep 01 19:48:56 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.489s CPU time.
Sep 01 19:51:00 vmi3306453 autoleft-deploy[2870169]: Sep 01 19:50:05 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 01 19:51:00 vmi3306453 autoleft-deploy[2870169]: Sep 01 19:50:06 vmi3306453 autoleft-deploy[2869434]: [2026-09-01 19:50:06] === Naujų commit'ų rasta: da6c399 → 9f0c6aa ===
Sep 01 19:51:00 vmi3306453 autoleft-deploy[2870169]: Sep 01 19:50:06 vmi3306453 autoleft-deploy[2869459]:     9f0c6aa fix(pastas): laiškai iškelti iš užklausos į foną
Sep 01 19:51:00 vmi3306453 autoleft-deploy[2870169]: Sep 01 19:50:06 vmi3306453 autoleft-deploy[2869434]: [2026-09-01 19:50:06] Kodas atnaujintas iki 9f0c6aa
Sep 01 19:51:00 vmi3306453 autoleft-deploy[2870169]: Sep 01 19:50:16 vmi3306453 autoleft-deploy[2869434]: [2026-09-01 19:50:16] Patikra praėjo
Sep 01 19:51:00 vmi3306453 autoleft-deploy[2870169]: Sep 01 19:50:16 vmi3306453 autoleft-deploy[2869604]: [19:50:16] === Deploy pradžia (20260901_195016) ===
Sep 01 19:51:00 vmi3306453 autoleft-deploy[2870169]: Sep 01 19:50:52 vmi3306453 autoleft-deploy[2869604]: [19:50:52] DB dumpas: /root/autoleft_backups/db_20260901_195016.sql
Sep 01 19:51:00 vmi3306453 autoleft-deploy[2870169]: Sep 01 19:50:54 vmi3306453 autoleft-deploy[2870015]: Operations to perform:
Sep 01 19:51:00 vmi3306453 autoleft-deploy[2870169]: Sep 01 19:50:54 vmi3306453 autoleft-deploy[2870015]:   Apply all migrations: accounts, admin, analytics, auth, broadcasts, contenttypes, conversations, imones, listings, payments, sessions
Sep 01 19:51:00 vmi3306453 autoleft-deploy[2870169]: Sep 01 19:50:54 vmi3306453 autoleft-deploy[2870015]: Running migrations:
Sep 01 19:51:00 vmi3306453 autoleft-deploy[2870169]: Sep 01 19:50:54 vmi3306453 autoleft-deploy[2870015]:   No migrations to apply.
Sep 01 19:51:00 vmi3306453 autoleft-deploy[2870169]: Sep 01 19:50:55 vmi3306453 autoleft-deploy[2870040]: 0 static files copied to '/root/autoleft/staticfiles', 216 unmodified.
Sep 01 19:51:00 vmi3306453 autoleft-deploy[2870169]: Sep 01 19:50:55 vmi3306453 autoleft-deploy[2869604]: [19:50:55] Restartinam gunicorn.service
Sep 01 19:51:00 vmi3306453 autoleft-deploy[2870169]: Sep 01 19:50:57 vmi3306453 autoleft-deploy[2869604]: [19:50:57] Health OK (1/10)
Sep 01 19:51:00 vmi3306453 autoleft-deploy[2870169]: Sep 01 19:50:57 vmi3306453 autoleft-deploy[2869604]: [19:50:57] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Sep 01 19:51:00 vmi3306453 autoleft-deploy[2870169]: Sep 01 19:50:57 vmi3306453 autoleft-deploy[2869604]: [19:50:57] === Deploy OK ===
Sep 01 19:51:00 vmi3306453 autoleft-deploy[2870169]: Sep 01 19:50:57 vmi3306453 autoleft-deploy[2869434]: [2026-09-01 19:50:57] ✅ Deploy OK — gyvai veikia 9f0c6aa
Sep 01 19:51:00 vmi3306453 autoleft-deploy[2870169]: ```
Sep 01 19:51:00 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 01 19:51:00 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 19:51:00 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 22.979s CPU time.
Sep 01 19:51:24 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
