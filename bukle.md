# Serverio būklė

Sugeneruota: 2026-09-02 19:13:09 CEST

## Kodas

```
sukasi:      92e8f95 fix(kalbos): „/" su ne lietuvių kalba nebemeta 404
origin/master: 92e8f95 fix(kalbos): „/" su ne lietuvių kalba nebemeta 404
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
HTTP 301, 0.002266s
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
/dev/sda1       291G   29G  262G  10% /
```

## Paskutinis auto-deploy

```
Sep 02 19:12:59 vmi3306453 autoleft-deploy[3906952]: Sep 02 19:12:08 vmi3306453 autoleft-deploy[3906108]: [2026-09-02 19:12:08] Patikra praėjo
Sep 02 19:12:59 vmi3306453 autoleft-deploy[3906952]: Sep 02 19:12:08 vmi3306453 autoleft-deploy[3906260]: [19:12:08] === Deploy pradžia (20260902_191208) ===
Sep 02 19:12:59 vmi3306453 autoleft-deploy[3906952]: Sep 02 19:12:09 vmi3306453 autoleft-deploy[3906260]: [19:12:09] Vietos diske: 89% laisva (260G).
Sep 02 19:12:59 vmi3306453 autoleft-deploy[3906952]: Sep 02 19:12:51 vmi3306453 autoleft-deploy[3906260]: [19:12:51] DB dumpas: /root/autoleft_backups/db_20260902_191208.sql.gz (130M)
Sep 02 19:12:59 vmi3306453 autoleft-deploy[3906952]: Sep 02 19:12:51 vmi3306453 autoleft-deploy[3906260]: [19:12:51] Senos kopijos ištrintos: 1 (laikom 5 naujausias).
Sep 02 19:12:59 vmi3306453 autoleft-deploy[3906952]: Sep 02 19:12:51 vmi3306453 autoleft-deploy[3906260]: [19:12:51] Kopijos: 5 vnt.,  viso 5.7G,  diske laisva 262G (90%).
Sep 02 19:12:59 vmi3306453 autoleft-deploy[3906952]: Sep 02 19:12:51 vmi3306453 autoleft-deploy[3906260]: [19:12:51] Versija: 92e8f95ab85e
Sep 02 19:12:59 vmi3306453 autoleft-deploy[3906952]: Sep 02 19:12:52 vmi3306453 autoleft-deploy[3906788]: Operations to perform:
Sep 02 19:12:59 vmi3306453 autoleft-deploy[3906952]: Sep 02 19:12:52 vmi3306453 autoleft-deploy[3906788]:   Apply all migrations: accounts, admin, analytics, auth, broadcasts, contenttypes, conversations, imones, listings, payments, sessions
Sep 02 19:12:59 vmi3306453 autoleft-deploy[3906952]: Sep 02 19:12:52 vmi3306453 autoleft-deploy[3906788]: Running migrations:
Sep 02 19:12:59 vmi3306453 autoleft-deploy[3906952]: Sep 02 19:12:52 vmi3306453 autoleft-deploy[3906788]:   No migrations to apply.
Sep 02 19:12:59 vmi3306453 autoleft-deploy[3906952]: Sep 02 19:12:53 vmi3306453 autoleft-deploy[3906815]: 0 static files copied to '/root/autoleft/staticfiles', 218 unmodified, 126 post-processed.
Sep 02 19:12:59 vmi3306453 autoleft-deploy[3906952]: Sep 02 19:12:53 vmi3306453 autoleft-deploy[3906260]: [19:12:53] Restartinam gunicorn.service
Sep 02 19:12:59 vmi3306453 autoleft-deploy[3906952]: Sep 02 19:12:55 vmi3306453 autoleft-deploy[3906260]: [19:12:55] Health OK (1/10)
Sep 02 19:12:59 vmi3306453 autoleft-deploy[3906952]: Sep 02 19:12:56 vmi3306453 autoleft-deploy[3906260]: [19:12:56] Statiniai OK: style.df8265b02e1b.css (manifestas atnaujintas)
Sep 02 19:12:59 vmi3306453 autoleft-deploy[3906952]: Sep 02 19:12:56 vmi3306453 autoleft-deploy[3906260]: [19:12:56] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Sep 02 19:12:59 vmi3306453 autoleft-deploy[3906952]: Sep 02 19:12:56 vmi3306453 autoleft-deploy[3906260]: [19:12:56] Raktai: .env — vietoje.
Sep 02 19:12:59 vmi3306453 autoleft-deploy[3906952]: Sep 02 19:12:56 vmi3306453 autoleft-deploy[3906260]: [19:12:56] Raktai: google-translate-key.json — vietoje.
Sep 02 19:12:59 vmi3306453 autoleft-deploy[3906952]: Sep 02 19:12:56 vmi3306453 autoleft-deploy[3906260]: [19:12:56] === Deploy OK ===
Sep 02 19:12:59 vmi3306453 autoleft-deploy[3906952]: Sep 02 19:12:57 vmi3306453 autoleft-deploy[3906108]: [2026-09-02 19:12:57] ✅ Deploy OK — gyvai veikia 92e8f95
Sep 02 19:12:59 vmi3306453 autoleft-deploy[3906952]: ```
Sep 02 19:12:59 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 19:12:59 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 19:12:59 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 43.562s CPU time.
Sep 02 19:13:09 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
