# Serverio būklė

Sugeneruota: 2026-09-02 15:51:51 CEST

## Kodas

```
sukasi:      e885047 fix(zinutes): vertimo klaida nebeslepia priežasties
origin/master: e885047 fix(zinutes): vertimo klaida nebeslepia priežasties
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
HTTP 301, 0.000970s
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
/dev/sda1       291G   49G  242G  17% /
```

## Paskutinis auto-deploy

```
Sep 02 15:49:26 vmi3306453 autoleft-deploy[3750890]: Sep 02 15:49:19 vmi3306453 autoleft-deploy[3750402]: [15:49:19] Versija: e885047d5021
Sep 02 15:49:26 vmi3306453 autoleft-deploy[3750890]: Sep 02 15:49:20 vmi3306453 autoleft-deploy[3750732]: Operations to perform:
Sep 02 15:49:26 vmi3306453 autoleft-deploy[3750890]: Sep 02 15:49:20 vmi3306453 autoleft-deploy[3750732]:   Apply all migrations: accounts, admin, analytics, auth, broadcasts, contenttypes, conversations, imones, listings, payments, sessions
Sep 02 15:49:26 vmi3306453 autoleft-deploy[3750890]: Sep 02 15:49:20 vmi3306453 autoleft-deploy[3750732]: Running migrations:
Sep 02 15:49:26 vmi3306453 autoleft-deploy[3750890]: Sep 02 15:49:20 vmi3306453 autoleft-deploy[3750732]:   No migrations to apply.
Sep 02 15:49:26 vmi3306453 autoleft-deploy[3750890]: Sep 02 15:49:21 vmi3306453 autoleft-deploy[3750751]: 0 static files copied to '/root/autoleft/staticfiles', 218 unmodified, 126 post-processed.
Sep 02 15:49:26 vmi3306453 autoleft-deploy[3750890]: Sep 02 15:49:21 vmi3306453 autoleft-deploy[3750402]: [15:49:21] Restartinam gunicorn.service
Sep 02 15:49:26 vmi3306453 autoleft-deploy[3750890]: Sep 02 15:49:23 vmi3306453 autoleft-deploy[3750402]: [15:49:23] Health OK (1/10)
Sep 02 15:49:26 vmi3306453 autoleft-deploy[3750890]: Sep 02 15:49:24 vmi3306453 autoleft-deploy[3750402]: [15:49:24] Statiniai OK: style.df8265b02e1b.css (manifestas atnaujintas)
Sep 02 15:49:26 vmi3306453 autoleft-deploy[3750890]: Sep 02 15:49:24 vmi3306453 autoleft-deploy[3750402]: [15:49:24] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Sep 02 15:49:26 vmi3306453 autoleft-deploy[3750890]: Sep 02 15:49:24 vmi3306453 autoleft-deploy[3750402]: [15:49:24] === Deploy OK ===
Sep 02 15:49:26 vmi3306453 autoleft-deploy[3750890]: Sep 02 15:49:24 vmi3306453 autoleft-deploy[3750286]: [2026-09-02 15:49:24] ✅ Deploy OK — gyvai veikia e885047
Sep 02 15:49:26 vmi3306453 autoleft-deploy[3750890]: ```
Sep 02 15:49:26 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 15:49:26 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 15:49:26 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 21.414s CPU time.
Sep 02 15:49:43 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 15:49:45 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 15:49:45 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 15:49:45 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.345s CPU time.
Sep 02 15:50:50 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 15:50:53 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 15:50:53 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 15:50:53 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.527s CPU time.
Sep 02 15:51:51 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
