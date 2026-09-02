# Serverio būklė

Sugeneruota: 2026-09-02 13:41:36 CEST

## Kodas

```
sukasi:      a42e0c6 docs(ekranai): mobili antraštė iš GYVOS autoleft.com (7e4bcbe)
origin/master: a42e0c6 docs(ekranai): mobili antraštė iš GYVOS autoleft.com (7e4bcbe)
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
HTTP 301, 0.001412s
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
/dev/sda1       291G   49G  243G  17% /
```

## Paskutinis auto-deploy

```
Sep 02 13:38:38 vmi3306453 autoleft-deploy[3655900]: Sep 02 13:38:31 vmi3306453 autoleft-deploy[3655395]: [13:38:31] Versija: a42e0c6deefa
Sep 02 13:38:38 vmi3306453 autoleft-deploy[3655900]: Sep 02 13:38:32 vmi3306453 autoleft-deploy[3655750]: Operations to perform:
Sep 02 13:38:38 vmi3306453 autoleft-deploy[3655900]: Sep 02 13:38:32 vmi3306453 autoleft-deploy[3655750]:   Apply all migrations: accounts, admin, analytics, auth, broadcasts, contenttypes, conversations, imones, listings, payments, sessions
Sep 02 13:38:38 vmi3306453 autoleft-deploy[3655900]: Sep 02 13:38:32 vmi3306453 autoleft-deploy[3655750]: Running migrations:
Sep 02 13:38:38 vmi3306453 autoleft-deploy[3655900]: Sep 02 13:38:32 vmi3306453 autoleft-deploy[3655750]:   No migrations to apply.
Sep 02 13:38:38 vmi3306453 autoleft-deploy[3655900]: Sep 02 13:38:33 vmi3306453 autoleft-deploy[3655768]: 0 static files copied to '/root/autoleft/staticfiles', 217 unmodified, 125 post-processed.
Sep 02 13:38:38 vmi3306453 autoleft-deploy[3655900]: Sep 02 13:38:33 vmi3306453 autoleft-deploy[3655395]: [13:38:33] Restartinam gunicorn.service
Sep 02 13:38:38 vmi3306453 autoleft-deploy[3655900]: Sep 02 13:38:35 vmi3306453 autoleft-deploy[3655395]: [13:38:35] Health OK (1/10)
Sep 02 13:38:38 vmi3306453 autoleft-deploy[3655900]: Sep 02 13:38:36 vmi3306453 autoleft-deploy[3655395]: [13:38:36] Statiniai OK: style.df8265b02e1b.css (manifestas atnaujintas)
Sep 02 13:38:38 vmi3306453 autoleft-deploy[3655900]: Sep 02 13:38:36 vmi3306453 autoleft-deploy[3655395]: [13:38:36] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Sep 02 13:38:38 vmi3306453 autoleft-deploy[3655900]: Sep 02 13:38:36 vmi3306453 autoleft-deploy[3655395]: [13:38:36] === Deploy OK ===
Sep 02 13:38:38 vmi3306453 autoleft-deploy[3655900]: Sep 02 13:38:36 vmi3306453 autoleft-deploy[3655240]: [2026-09-02 13:38:36] ✅ Deploy OK — gyvai veikia a42e0c6
Sep 02 13:38:38 vmi3306453 autoleft-deploy[3655900]: ```
Sep 02 13:38:38 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 13:38:38 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 13:38:38 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 20.661s CPU time.
Sep 02 13:38:58 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 13:39:00 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 13:39:00 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 13:39:00 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.398s CPU time.
Sep 02 13:40:29 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 13:40:31 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 13:40:31 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 13:40:31 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.349s CPU time.
Sep 02 13:41:36 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
