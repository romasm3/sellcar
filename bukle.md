# Serverio būklė

Sugeneruota: 2026-09-01 23:12:36 CEST

## Kodas

```
sukasi:      fc18758 docs(ekranai): šoninė juosta iš GYVOS autoleft.com (b42c6f9)
origin/master: fc18758 docs(ekranai): šoninė juosta iš GYVOS autoleft.com (b42c6f9)
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
HTTP 301, 0.002030s
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
/dev/sda1       291G   46G  246G  16% /
```

## Paskutinis auto-deploy

```
Sep 01 23:09:16 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 23:09:16 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.569s CPU time.
Sep 01 23:10:29 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 01 23:10:30 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 01 23:10:30 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 23:10:30 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.328s CPU time.
Sep 01 23:11:46 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 01 23:11:47 vmi3306453 autoleft-deploy[3019848]: [2026-09-01 23:11:47] === Naujų commit'ų rasta: b42c6f9 → fc18758 ===
Sep 01 23:11:47 vmi3306453 autoleft-deploy[3019869]:     fc18758 docs(ekranai): šoninė juosta iš GYVOS autoleft.com (b42c6f9)
Sep 01 23:11:47 vmi3306453 autoleft-deploy[3019848]: [2026-09-01 23:11:47] Kodas atnaujintas iki fc18758
Sep 01 23:11:55 vmi3306453 autoleft-deploy[3019848]: [2026-09-01 23:11:55] Patikra praėjo
Sep 01 23:11:55 vmi3306453 autoleft-deploy[3020035]: [23:11:55] === Deploy pradžia (20260901_231155) ===
Sep 01 23:12:31 vmi3306453 autoleft-deploy[3020035]: [23:12:31] DB dumpas: /root/autoleft_backups/db_20260901_231155.sql
Sep 01 23:12:31 vmi3306453 autoleft-deploy[3020035]: [23:12:31] Versija: fc187581fa51
Sep 01 23:12:32 vmi3306453 autoleft-deploy[3020435]: Operations to perform:
Sep 01 23:12:32 vmi3306453 autoleft-deploy[3020435]:   Apply all migrations: accounts, admin, analytics, auth, broadcasts, contenttypes, conversations, imones, listings, payments, sessions
Sep 01 23:12:32 vmi3306453 autoleft-deploy[3020435]: Running migrations:
Sep 01 23:12:32 vmi3306453 autoleft-deploy[3020435]:   No migrations to apply.
Sep 01 23:12:33 vmi3306453 autoleft-deploy[3020451]: 0 static files copied to '/root/autoleft/staticfiles', 217 unmodified, 125 post-processed.
Sep 01 23:12:33 vmi3306453 autoleft-deploy[3020035]: [23:12:33] Restartinam gunicorn.service
Sep 01 23:12:35 vmi3306453 autoleft-deploy[3020035]: [23:12:35] Health OK (1/10)
Sep 01 23:12:36 vmi3306453 autoleft-deploy[3020035]: [23:12:36] Statiniai OK: style.df8265b02e1b.css (manifestas atnaujintas)
Sep 01 23:12:36 vmi3306453 autoleft-deploy[3020035]: [23:12:36] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Sep 01 23:12:36 vmi3306453 autoleft-deploy[3020035]: [23:12:36] === Deploy OK ===
Sep 01 23:12:36 vmi3306453 autoleft-deploy[3019848]: [2026-09-01 23:12:36] ✅ Deploy OK — gyvai veikia fc18758
```
