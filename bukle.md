# Serverio būklė

Sugeneruota: 2026-09-02 20:40:37 CEST

## Kodas

```
sukasi:      7e171f9 fix(vertimai): masinis užpildymas per paslaugos paskyrą, ne API raktą
origin/master: 7e171f9 fix(vertimai): masinis užpildymas per paslaugos paskyrą, ne API raktą
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
HTTP 301, 0.001519s
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
Sep 02 20:39:26 vmi3306453 autoleft-deploy[3974668]: Sep 02 20:39:17 vmi3306453 autoleft-deploy[3973840]: [20:39:17] Senos kopijos ištrintos: 1 (laikom 5 naujausias).
Sep 02 20:39:26 vmi3306453 autoleft-deploy[3974668]: Sep 02 20:39:17 vmi3306453 autoleft-deploy[3973840]: [20:39:17] Kopijos: 5 vnt.,  viso 653M,  diske laisva 267G (91%).
Sep 02 20:39:26 vmi3306453 autoleft-deploy[3974668]: Sep 02 20:39:17 vmi3306453 autoleft-deploy[3973840]: [20:39:17] Versija: 7e171f9f79e4
Sep 02 20:39:26 vmi3306453 autoleft-deploy[3974668]: Sep 02 20:39:19 vmi3306453 autoleft-deploy[3974441]: Operations to perform:
Sep 02 20:39:26 vmi3306453 autoleft-deploy[3974668]: Sep 02 20:39:19 vmi3306453 autoleft-deploy[3974441]:   Apply all migrations: accounts, admin, analytics, auth, broadcasts, contenttypes, conversations, imones, listings, payments, sessions
Sep 02 20:39:26 vmi3306453 autoleft-deploy[3974668]: Sep 02 20:39:19 vmi3306453 autoleft-deploy[3974441]: Running migrations:
Sep 02 20:39:26 vmi3306453 autoleft-deploy[3974668]: Sep 02 20:39:19 vmi3306453 autoleft-deploy[3974441]:   No migrations to apply.
Sep 02 20:39:26 vmi3306453 autoleft-deploy[3974668]: Sep 02 20:39:19 vmi3306453 autoleft-deploy[3974481]: 0 static files copied to '/root/autoleft/staticfiles', 218 unmodified, 126 post-processed.
Sep 02 20:39:26 vmi3306453 autoleft-deploy[3974668]: Sep 02 20:39:20 vmi3306453 autoleft-deploy[3973840]: [20:39:20] Restartinam gunicorn.service
Sep 02 20:39:26 vmi3306453 autoleft-deploy[3974668]: Sep 02 20:39:22 vmi3306453 autoleft-deploy[3973840]: [20:39:22] Health OK (1/10)
Sep 02 20:39:26 vmi3306453 autoleft-deploy[3974668]: Sep 02 20:39:22 vmi3306453 autoleft-deploy[3973840]: [20:39:22] Statiniai OK: style.df8265b02e1b.css (manifestas atnaujintas)
Sep 02 20:39:26 vmi3306453 autoleft-deploy[3974668]: Sep 02 20:39:22 vmi3306453 autoleft-deploy[3973840]: [20:39:22] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Sep 02 20:39:26 vmi3306453 autoleft-deploy[3974668]: Sep 02 20:39:22 vmi3306453 autoleft-deploy[3973840]: [20:39:22] Raktai: .env — vietoje.
Sep 02 20:39:26 vmi3306453 autoleft-deploy[3974668]: Sep 02 20:39:22 vmi3306453 autoleft-deploy[3973840]: [20:39:22] Raktai: google-translate-key.json — vietoje.
Sep 02 20:39:26 vmi3306453 autoleft-deploy[3974668]: Sep 02 20:39:22 vmi3306453 autoleft-deploy[3973840]: [20:39:22] === Deploy OK ===
Sep 02 20:39:26 vmi3306453 autoleft-deploy[3974668]: Sep 02 20:39:22 vmi3306453 autoleft-deploy[3973655]: [2026-09-02 20:39:22] ✅ Deploy OK — gyvai veikia 7e171f9
Sep 02 20:39:26 vmi3306453 autoleft-deploy[3974668]: ```
Sep 02 20:39:26 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 20:39:26 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 20:39:26 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 44.100s CPU time.
Sep 02 20:39:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 20:39:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 20:39:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 20:39:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.314s CPU time.
Sep 02 20:40:36 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
