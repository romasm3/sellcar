# Serverio būklė

Sugeneruota: 2026-09-01 18:33:54 CEST

## Kodas

```
sukasi:      3ee00cc feat(kortele): vietos eilutė su vėliava pagal etaloną
origin/master: 3ee00cc feat(kortele): vietos eilutė su vėliava pagal etaloną
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
HTTP 301, 0.002013s
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
/dev/sda1       291G   40G  251G  14% /
```

## Paskutinis auto-deploy

```
Sep 01 18:31:25 vmi3306453 autoleft-deploy[2809555]: Sep 01 18:30:44 vmi3306453 autoleft-deploy[2809026]: [18:30:44] === Deploy pradžia (20260901_183044) ===
Sep 01 18:31:25 vmi3306453 autoleft-deploy[2809555]: Sep 01 18:31:18 vmi3306453 autoleft-deploy[2809026]: [18:31:18] DB dumpas: /root/autoleft_backups/db_20260901_183044.sql
Sep 01 18:31:25 vmi3306453 autoleft-deploy[2809555]: Sep 01 18:31:20 vmi3306453 autoleft-deploy[2809407]: Operations to perform:
Sep 01 18:31:25 vmi3306453 autoleft-deploy[2809555]: Sep 01 18:31:20 vmi3306453 autoleft-deploy[2809407]:   Apply all migrations: accounts, admin, analytics, auth, broadcasts, contenttypes, conversations, imones, listings, payments, sessions
Sep 01 18:31:25 vmi3306453 autoleft-deploy[2809555]: Sep 01 18:31:20 vmi3306453 autoleft-deploy[2809407]: Running migrations:
Sep 01 18:31:25 vmi3306453 autoleft-deploy[2809555]: Sep 01 18:31:20 vmi3306453 autoleft-deploy[2809407]:   No migrations to apply.
Sep 01 18:31:25 vmi3306453 autoleft-deploy[2809555]: Sep 01 18:31:20 vmi3306453 autoleft-deploy[2809440]: 2 static files copied to '/root/autoleft/staticfiles', 214 unmodified.
Sep 01 18:31:25 vmi3306453 autoleft-deploy[2809555]: Sep 01 18:31:21 vmi3306453 autoleft-deploy[2809026]: [18:31:21] Restartinam gunicorn.service
Sep 01 18:31:25 vmi3306453 autoleft-deploy[2809555]: Sep 01 18:31:23 vmi3306453 autoleft-deploy[2809026]: [18:31:23] Health OK (1/10)
Sep 01 18:31:25 vmi3306453 autoleft-deploy[2809555]: Sep 01 18:31:23 vmi3306453 autoleft-deploy[2809026]: [18:31:23] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Sep 01 18:31:25 vmi3306453 autoleft-deploy[2809555]: Sep 01 18:31:23 vmi3306453 autoleft-deploy[2809026]: [18:31:23] === Deploy OK ===
Sep 01 18:31:25 vmi3306453 autoleft-deploy[2809555]: Sep 01 18:31:23 vmi3306453 autoleft-deploy[2808846]: [2026-09-01 18:31:23] ✅ Deploy OK — gyvai veikia 3ee00cc
Sep 01 18:31:25 vmi3306453 autoleft-deploy[2809555]: ```
Sep 01 18:31:25 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 01 18:31:25 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 18:31:25 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 22.635s CPU time.
Sep 01 18:31:41 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 01 18:31:43 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 01 18:31:43 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 18:31:43 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.347s CPU time.
Sep 01 18:32:49 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 01 18:32:51 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 01 18:32:51 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 18:32:51 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.413s CPU time.
Sep 01 18:33:54 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
