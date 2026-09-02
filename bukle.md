# Serverio būklė

Sugeneruota: 2026-09-02 09:49:28 CEST

## Kodas

```
sukasi:      2ee1a2e docs(ekranai): atidarytas sąrašas iš GYVOS autoleft.com (2daac2c)
origin/master: 2ee1a2e docs(ekranai): atidarytas sąrašas iš GYVOS autoleft.com (2daac2c)
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
HTTP 301, 0.001712s
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
/dev/sda1       291G   47G  245G  16% /
```

## Paskutinis auto-deploy

```
Sep 02 09:49:28 vmi3306453 autoleft-deploy[3490506]: Sep 02 09:47:09 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.682s CPU time.
Sep 02 09:49:28 vmi3306453 autoleft-deploy[3490506]: Sep 02 09:48:16 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 09:49:28 vmi3306453 autoleft-deploy[3490506]: Sep 02 09:48:17 vmi3306453 autoleft-deploy[3489425]: [2026-09-02 09:48:17] === Naujų commit'ų rasta: 2daac2c → 2ee1a2e ===
Sep 02 09:49:28 vmi3306453 autoleft-deploy[3490506]: Sep 02 09:48:17 vmi3306453 autoleft-deploy[3489448]:     2ee1a2e docs(ekranai): atidarytas sąrašas iš GYVOS autoleft.com (2daac2c)
Sep 02 09:49:28 vmi3306453 autoleft-deploy[3490506]: Sep 02 09:48:17 vmi3306453 autoleft-deploy[3489425]: [2026-09-02 09:48:17] Kodas atnaujintas iki 2ee1a2e
Sep 02 09:49:28 vmi3306453 autoleft-deploy[3490506]: Sep 02 09:48:28 vmi3306453 autoleft-deploy[3489425]: [2026-09-02 09:48:28] Patikra praėjo
Sep 02 09:49:28 vmi3306453 autoleft-deploy[3490506]: Sep 02 09:48:28 vmi3306453 autoleft-deploy[3489634]: [09:48:28] === Deploy pradžia (20260902_094828) ===
Sep 02 09:49:28 vmi3306453 autoleft-deploy[3490506]: Sep 02 09:49:20 vmi3306453 autoleft-deploy[3489634]: [09:49:20] DB dumpas: /root/autoleft_backups/db_20260902_094828.sql
Sep 02 09:49:28 vmi3306453 autoleft-deploy[3490506]: Sep 02 09:49:20 vmi3306453 autoleft-deploy[3489634]: [09:49:20] Versija: 2ee1a2e4ef31
Sep 02 09:49:28 vmi3306453 autoleft-deploy[3490506]: Sep 02 09:49:22 vmi3306453 autoleft-deploy[3490305]: Operations to perform:
Sep 02 09:49:28 vmi3306453 autoleft-deploy[3490506]: Sep 02 09:49:22 vmi3306453 autoleft-deploy[3490305]:   Apply all migrations: accounts, admin, analytics, auth, broadcasts, contenttypes, conversations, imones, listings, payments, sessions
Sep 02 09:49:28 vmi3306453 autoleft-deploy[3490506]: Sep 02 09:49:22 vmi3306453 autoleft-deploy[3490305]: Running migrations:
Sep 02 09:49:28 vmi3306453 autoleft-deploy[3490506]: Sep 02 09:49:22 vmi3306453 autoleft-deploy[3490305]:   No migrations to apply.
Sep 02 09:49:28 vmi3306453 autoleft-deploy[3490506]: Sep 02 09:49:23 vmi3306453 autoleft-deploy[3490351]: 0 static files copied to '/root/autoleft/staticfiles', 217 unmodified, 125 post-processed.
Sep 02 09:49:28 vmi3306453 autoleft-deploy[3490506]: Sep 02 09:49:23 vmi3306453 autoleft-deploy[3489634]: [09:49:23] Restartinam gunicorn.service
Sep 02 09:49:28 vmi3306453 autoleft-deploy[3490506]: Sep 02 09:49:25 vmi3306453 autoleft-deploy[3489634]: [09:49:25] Health OK (1/10)
Sep 02 09:49:28 vmi3306453 autoleft-deploy[3490506]: Sep 02 09:49:25 vmi3306453 autoleft-deploy[3489634]: [09:49:25] Statiniai OK: style.df8265b02e1b.css (manifestas atnaujintas)
Sep 02 09:49:28 vmi3306453 autoleft-deploy[3490506]: Sep 02 09:49:25 vmi3306453 autoleft-deploy[3489634]: [09:49:25] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Sep 02 09:49:28 vmi3306453 autoleft-deploy[3490506]: Sep 02 09:49:25 vmi3306453 autoleft-deploy[3489634]: [09:49:25] === Deploy OK ===
Sep 02 09:49:28 vmi3306453 autoleft-deploy[3490506]: Sep 02 09:49:25 vmi3306453 autoleft-deploy[3489425]: [2026-09-02 09:49:25] ✅ Deploy OK — gyvai veikia 2ee1a2e
Sep 02 09:49:28 vmi3306453 autoleft-deploy[3490506]: ```
Sep 02 09:49:28 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 09:49:28 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 09:49:28 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 25.733s CPU time.
Sep 02 09:49:28 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
