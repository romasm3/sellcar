# Serverio būklė

Sugeneruota: 2026-09-01 19:31:50 CEST

## Kodas

```
sukasi:      da6c399 fix(skaiciai): metai be skirtuko, kiekiai su tarpu
origin/master: da6c399 fix(skaiciai): metai be skirtuko, kiekiai su tarpu
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
HTTP 301, 0.001341s
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
/dev/sda1       291G   44G  248G  15% /
```

## Paskutinis auto-deploy

```
Sep 01 19:28:09 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 01 19:28:09 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 19:28:09 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.328s CPU time.
Sep 01 19:29:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 01 19:29:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 01 19:29:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 19:29:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.441s CPU time.
Sep 01 19:31:05 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 01 19:31:06 vmi3306453 autoleft-deploy[2854874]: [2026-09-01 19:31:06] === Naujų commit'ų rasta: 7d0a678 → da6c399 ===
Sep 01 19:31:06 vmi3306453 autoleft-deploy[2854896]:     da6c399 fix(skaiciai): metai be skirtuko, kiekiai su tarpu
Sep 01 19:31:06 vmi3306453 autoleft-deploy[2854896]:     0778b6d fix(vieta): SVG matmenys žymėje, stilius bendrame faile
Sep 01 19:31:06 vmi3306453 autoleft-deploy[2854874]: [2026-09-01 19:31:06] Kodas atnaujintas iki da6c399
Sep 01 19:31:15 vmi3306453 autoleft-deploy[2854874]: [2026-09-01 19:31:15] Patikra praėjo
Sep 01 19:31:15 vmi3306453 autoleft-deploy[2855005]: [19:31:15] === Deploy pradžia (20260901_193115) ===
Sep 01 19:31:46 vmi3306453 autoleft-deploy[2855005]: [19:31:46] DB dumpas: /root/autoleft_backups/db_20260901_193115.sql
Sep 01 19:31:47 vmi3306453 autoleft-deploy[2855361]: Operations to perform:
Sep 01 19:31:47 vmi3306453 autoleft-deploy[2855361]:   Apply all migrations: accounts, admin, analytics, auth, broadcasts, contenttypes, conversations, imones, listings, payments, sessions
Sep 01 19:31:47 vmi3306453 autoleft-deploy[2855361]: Running migrations:
Sep 01 19:31:47 vmi3306453 autoleft-deploy[2855361]:   No migrations to apply.
Sep 01 19:31:48 vmi3306453 autoleft-deploy[2855397]: 1 static file copied to '/root/autoleft/staticfiles', 215 unmodified.
Sep 01 19:31:48 vmi3306453 autoleft-deploy[2855005]: [19:31:48] Restartinam gunicorn.service
Sep 01 19:31:50 vmi3306453 autoleft-deploy[2855005]: [19:31:50] Health OK (1/10)
Sep 01 19:31:50 vmi3306453 autoleft-deploy[2855005]: [19:31:50] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Sep 01 19:31:50 vmi3306453 autoleft-deploy[2855005]: [19:31:50] === Deploy OK ===
Sep 01 19:31:50 vmi3306453 autoleft-deploy[2854874]: [2026-09-01 19:31:50] ✅ Deploy OK — gyvai veikia da6c399
```
