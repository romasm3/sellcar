# Serverio būklė

Sugeneruota: 2026-09-02 09:31:28 CEST

## Kodas

```
sukasi:      9a1bfe7 fix(deploy): kritęs deploy'as nebekartojamas kas minutę
origin/master: 9a1bfe7 fix(deploy): kritęs deploy'as nebekartojamas kas minutę
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
HTTP 301, 0.001773s
```

## Skelbimų būsenos

```

Listing — iš viso 35
  active        18   MATOMAS
  draft          9   nematomas
  expired        8   nematomas
  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─
  nematomi dėl būsenos:      17
  iš jų pasibaigę (expires_at praeityje): 8
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
/dev/sda1       291G   46G  245G  16% /
```

## Paskutinis auto-deploy

```
Sep 02 09:28:31 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 09:28:31 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.631s CPU time.
Sep 02 09:29:35 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 09:29:37 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 09:29:37 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 09:29:37 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.618s CPU time.
Sep 02 09:30:36 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 09:30:37 vmi3306453 autoleft-deploy[3475238]: [2026-09-02 09:30:37] === Naujų commit'ų rasta: fc18758 → 9a1bfe7 ===
Sep 02 09:30:37 vmi3306453 autoleft-deploy[3475261]:     9a1bfe7 fix(deploy): kritęs deploy'as nebekartojamas kas minutę
Sep 02 09:30:37 vmi3306453 autoleft-deploy[3475238]: [2026-09-02 09:30:37] Kodas atnaujintas iki 9a1bfe7
Sep 02 09:30:46 vmi3306453 autoleft-deploy[3475238]: [2026-09-02 09:30:46] Patikra praėjo
Sep 02 09:30:46 vmi3306453 autoleft-deploy[3475390]: [09:30:46] === Deploy pradžia (20260902_093046) ===
Sep 02 09:31:22 vmi3306453 autoleft-deploy[3475390]: [09:31:22] DB dumpas: /root/autoleft_backups/db_20260902_093046.sql
Sep 02 09:31:22 vmi3306453 autoleft-deploy[3475390]: [09:31:22] Versija: 9a1bfe7cb7de
Sep 02 09:31:24 vmi3306453 autoleft-deploy[3475772]: Operations to perform:
Sep 02 09:31:24 vmi3306453 autoleft-deploy[3475772]:   Apply all migrations: accounts, admin, analytics, auth, broadcasts, contenttypes, conversations, imones, listings, payments, sessions
Sep 02 09:31:24 vmi3306453 autoleft-deploy[3475772]: Running migrations:
Sep 02 09:31:24 vmi3306453 autoleft-deploy[3475772]:   No migrations to apply.
Sep 02 09:31:25 vmi3306453 autoleft-deploy[3475795]: 0 static files copied to '/root/autoleft/staticfiles', 217 unmodified, 125 post-processed.
Sep 02 09:31:25 vmi3306453 autoleft-deploy[3475390]: [09:31:25] Restartinam gunicorn.service
Sep 02 09:31:27 vmi3306453 autoleft-deploy[3475390]: [09:31:27] Health OK (1/10)
Sep 02 09:31:28 vmi3306453 autoleft-deploy[3475390]: [09:31:28] Statiniai OK: style.df8265b02e1b.css (manifestas atnaujintas)
Sep 02 09:31:28 vmi3306453 autoleft-deploy[3475390]: [09:31:28] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Sep 02 09:31:28 vmi3306453 autoleft-deploy[3475390]: [09:31:28] === Deploy OK ===
Sep 02 09:31:28 vmi3306453 autoleft-deploy[3475238]: [2026-09-02 09:31:28] ✅ Deploy OK — gyvai veikia 9a1bfe7
```
