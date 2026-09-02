# Serverio būklė

Sugeneruota: 2026-09-02 13:27:04 CEST

## Kodas

```
sukasi:      83fa91a docs(ekranai): kalbos perjungiklis iš GYVOS autoleft.com (a954c27)
origin/master: 83fa91a docs(ekranai): kalbos perjungiklis iš GYVOS autoleft.com (a954c27)
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
HTTP 301, 0.001161s
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
/dev/sda1       291G   48G  243G  17% /
```

## Paskutinis auto-deploy

```
Sep 02 13:24:19 vmi3306453 autoleft-deploy[3645414]: Sep 02 13:24:12 vmi3306453 autoleft-deploy[3644891]: [13:24:12] Versija: 83fa91a71819
Sep 02 13:24:19 vmi3306453 autoleft-deploy[3645414]: Sep 02 13:24:13 vmi3306453 autoleft-deploy[3645264]: Operations to perform:
Sep 02 13:24:19 vmi3306453 autoleft-deploy[3645414]: Sep 02 13:24:13 vmi3306453 autoleft-deploy[3645264]:   Apply all migrations: accounts, admin, analytics, auth, broadcasts, contenttypes, conversations, imones, listings, payments, sessions
Sep 02 13:24:19 vmi3306453 autoleft-deploy[3645414]: Sep 02 13:24:13 vmi3306453 autoleft-deploy[3645264]: Running migrations:
Sep 02 13:24:19 vmi3306453 autoleft-deploy[3645414]: Sep 02 13:24:13 vmi3306453 autoleft-deploy[3645264]:   No migrations to apply.
Sep 02 13:24:19 vmi3306453 autoleft-deploy[3645414]: Sep 02 13:24:14 vmi3306453 autoleft-deploy[3645282]: 0 static files copied to '/root/autoleft/staticfiles', 217 unmodified, 125 post-processed.
Sep 02 13:24:19 vmi3306453 autoleft-deploy[3645414]: Sep 02 13:24:14 vmi3306453 autoleft-deploy[3644891]: [13:24:14] Restartinam gunicorn.service
Sep 02 13:24:19 vmi3306453 autoleft-deploy[3645414]: Sep 02 13:24:16 vmi3306453 autoleft-deploy[3644891]: [13:24:16] Health OK (1/10)
Sep 02 13:24:19 vmi3306453 autoleft-deploy[3645414]: Sep 02 13:24:16 vmi3306453 autoleft-deploy[3644891]: [13:24:16] Statiniai OK: style.df8265b02e1b.css (manifestas atnaujintas)
Sep 02 13:24:19 vmi3306453 autoleft-deploy[3645414]: Sep 02 13:24:17 vmi3306453 autoleft-deploy[3644891]: [13:24:17] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Sep 02 13:24:19 vmi3306453 autoleft-deploy[3645414]: Sep 02 13:24:17 vmi3306453 autoleft-deploy[3644891]: [13:24:17] === Deploy OK ===
Sep 02 13:24:19 vmi3306453 autoleft-deploy[3645414]: Sep 02 13:24:17 vmi3306453 autoleft-deploy[3644750]: [2026-09-02 13:24:17] ✅ Deploy OK — gyvai veikia 83fa91a
Sep 02 13:24:19 vmi3306453 autoleft-deploy[3645414]: ```
Sep 02 13:24:19 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 13:24:19 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 13:24:19 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 21.834s CPU time.
Sep 02 13:24:35 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 13:24:37 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 13:24:37 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 13:24:37 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.354s CPU time.
Sep 02 13:25:52 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 13:25:54 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 13:25:54 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 13:25:54 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.316s CPU time.
Sep 02 13:27:04 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
