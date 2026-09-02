# Serverio būklė

Sugeneruota: 2026-09-02 19:15:37 CEST

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
HTTP 301, 0.002901s
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
Sep 02 19:13:11 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 19:13:11 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 19:13:11 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.473s CPU time.
Sep 02 19:14:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 19:14:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 19:14:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 19:14:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.314s CPU time.
Sep 02 19:15:37 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
