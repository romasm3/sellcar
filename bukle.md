# Serverio būklė

Sugeneruota: 2026-09-01 18:56:07 CEST

## Kodas

```
sukasi:      7d0a678 fix(kortele): telefone vieta rodoma vieną kartą
origin/master: 7d0a678 fix(kortele): telefone vieta rodoma vieną kartą
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
HTTP 301, 0.001653s
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
/dev/sda1       291G   42G  250G  15% /
```

## Paskutinis auto-deploy

```
Sep 01 18:53:13 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 01 18:53:15 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 01 18:53:15 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 18:53:15 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.348s CPU time.
Sep 01 18:54:17 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 01 18:54:19 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 01 18:54:19 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 18:54:19 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.359s CPU time.
Sep 01 18:55:25 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 01 18:55:26 vmi3306453 autoleft-deploy[2828007]: [2026-09-01 18:55:26] === Naujų commit'ų rasta: 3ee00cc → 7d0a678 ===
Sep 01 18:55:26 vmi3306453 autoleft-deploy[2828027]:     7d0a678 fix(kortele): telefone vieta rodoma vieną kartą
Sep 01 18:55:26 vmi3306453 autoleft-deploy[2828007]: [2026-09-01 18:55:26] Kodas atnaujintas iki 7d0a678
Sep 01 18:55:35 vmi3306453 autoleft-deploy[2828007]: [2026-09-01 18:55:35] Patikra praėjo
Sep 01 18:55:35 vmi3306453 autoleft-deploy[2828141]: [18:55:35] === Deploy pradžia (20260901_185535) ===
Sep 01 18:56:03 vmi3306453 autoleft-deploy[2828141]: [18:56:03] DB dumpas: /root/autoleft_backups/db_20260901_185535.sql
Sep 01 18:56:05 vmi3306453 autoleft-deploy[2828449]: Operations to perform:
Sep 01 18:56:05 vmi3306453 autoleft-deploy[2828449]:   Apply all migrations: accounts, admin, analytics, auth, broadcasts, contenttypes, conversations, imones, listings, payments, sessions
Sep 01 18:56:05 vmi3306453 autoleft-deploy[2828449]: Running migrations:
Sep 01 18:56:05 vmi3306453 autoleft-deploy[2828449]:   No migrations to apply.
Sep 01 18:56:06 vmi3306453 autoleft-deploy[2828473]: 1 static file copied to '/root/autoleft/staticfiles', 215 unmodified.
Sep 01 18:56:06 vmi3306453 autoleft-deploy[2828141]: [18:56:06] Restartinam gunicorn.service
Sep 01 18:56:07 vmi3306453 autoleft-deploy[2828141]: [18:56:07] Health OK (1/10)
Sep 01 18:56:07 vmi3306453 autoleft-deploy[2828141]: [18:56:07] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Sep 01 18:56:07 vmi3306453 autoleft-deploy[2828141]: [18:56:07] === Deploy OK ===
Sep 01 18:56:07 vmi3306453 autoleft-deploy[2828007]: [2026-09-01 18:56:07] ✅ Deploy OK — gyvai veikia 7d0a678
```
