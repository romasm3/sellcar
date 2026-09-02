# Serverio būklė

Sugeneruota: 2026-09-02 19:54:22 CEST

## Kodas

```
sukasi:      a336fac feat(vertimai): masinio užpildymo įrankis su keturiomis apsaugomis
origin/master: a336fac feat(vertimai): masinio užpildymo įrankis su keturiomis apsaugomis
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
HTTP 301, 0.001136s
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
  aktyvūs, baigsis per 7 d.: 6
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
/dev/sda1       291G   24G  267G   9% /
```

## Paskutinis auto-deploy

```
Sep 02 19:52:35 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 45.036s CPU time.
Sep 02 19:53:26 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 19:53:26 vmi3306453 autoleft-deploy[3937912]: [2026-09-02 19:53:26] === Naujų commit'ų rasta: 831f4c0 → a336fac ===
Sep 02 19:53:26 vmi3306453 autoleft-deploy[3937933]:     a336fac feat(vertimai): masinio užpildymo įrankis su keturiomis apsaugomis
Sep 02 19:53:26 vmi3306453 autoleft-deploy[3937912]: [2026-09-02 19:53:26] Kodas atnaujintas iki a336fac
Sep 02 19:53:34 vmi3306453 autoleft-deploy[3937912]: [2026-09-02 19:53:34] Patikra praėjo
Sep 02 19:53:34 vmi3306453 autoleft-deploy[3938048]: [19:53:34] === Deploy pradžia (20260902_195334) ===
Sep 02 19:53:34 vmi3306453 autoleft-deploy[3938048]: [19:53:34] Vietos diske: 90% laisva (265G).
Sep 02 19:54:17 vmi3306453 autoleft-deploy[3938048]: [19:54:17] DB dumpas: /root/autoleft_backups/db_20260902_195334.sql.gz (131M)
Sep 02 19:54:17 vmi3306453 autoleft-deploy[3938048]: [19:54:17] Senos kopijos ištrintos: 1 (laikom 5 naujausias).
Sep 02 19:54:17 vmi3306453 autoleft-deploy[3938048]: [19:54:17] Kopijos: 5 vnt.,  viso 648M,  diske laisva 267G (91%).
Sep 02 19:54:17 vmi3306453 autoleft-deploy[3938048]: [19:54:17] Versija: a336faca99a7
Sep 02 19:54:18 vmi3306453 autoleft-deploy[3938600]: Operations to perform:
Sep 02 19:54:18 vmi3306453 autoleft-deploy[3938600]:   Apply all migrations: accounts, admin, analytics, auth, broadcasts, contenttypes, conversations, imones, listings, payments, sessions
Sep 02 19:54:18 vmi3306453 autoleft-deploy[3938600]: Running migrations:
Sep 02 19:54:18 vmi3306453 autoleft-deploy[3938600]:   No migrations to apply.
Sep 02 19:54:19 vmi3306453 autoleft-deploy[3938626]: 0 static files copied to '/root/autoleft/staticfiles', 218 unmodified, 126 post-processed.
Sep 02 19:54:20 vmi3306453 autoleft-deploy[3938048]: [19:54:20] Restartinam gunicorn.service
Sep 02 19:54:21 vmi3306453 autoleft-deploy[3938048]: [19:54:21] Health OK (1/10)
Sep 02 19:54:22 vmi3306453 autoleft-deploy[3938048]: [19:54:22] Statiniai OK: style.df8265b02e1b.css (manifestas atnaujintas)
Sep 02 19:54:22 vmi3306453 autoleft-deploy[3938048]: [19:54:22] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Sep 02 19:54:22 vmi3306453 autoleft-deploy[3938048]: [19:54:22] Raktai: .env — vietoje.
Sep 02 19:54:22 vmi3306453 autoleft-deploy[3938048]: [19:54:22] Raktai: google-translate-key.json — vietoje.
Sep 02 19:54:22 vmi3306453 autoleft-deploy[3938048]: [19:54:22] === Deploy OK ===
Sep 02 19:54:22 vmi3306453 autoleft-deploy[3937912]: [2026-09-02 19:54:22] ✅ Deploy OK — gyvai veikia a336fac
```
