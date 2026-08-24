# Serverio būklė

Sugeneruota: 2026-08-24 13:53:59 CEST

## Kodas

```
sukasi:      288b7a9 feat(skelbimas): pardavėjo blokas turinyje ir „Kiti pardavėjo skelbimai"
origin/master: 288b7a9 feat(skelbimas): pardavėjo blokas turinyje ir „Kiti pardavėjo skelbimai"
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
HTTP 301, 0.001195s
```

## Skelbimų būsenos

```

Listing — iš viso 35
  active        23   MATOMAS
  draft          9   nematomas
  expired        3   nematomas
  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─
  nematomi dėl būsenos:      12
  iš jų pasibaigę (expires_at praeityje): 3
  aktyvūs, baigsis per 7 d.: 4
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
/dev/sda1       291G   15G  277G   5% /
```

## Paskutinis auto-deploy

```
Aug 24 13:50:38 vmi3306453 autoleft-deploy[186762]: Aug 24 13:50:31 vmi3306453 autoleft-deploy[186527]: [2026-08-24 13:50:31] Patikra praėjo
Aug 24 13:50:38 vmi3306453 autoleft-deploy[186762]: Aug 24 13:50:31 vmi3306453 autoleft-deploy[186662]: [13:50:31] === Deploy pradžia (20260824_135031) ===
Aug 24 13:50:38 vmi3306453 autoleft-deploy[186762]: Aug 24 13:50:34 vmi3306453 autoleft-deploy[186662]: [13:50:34] DB dumpas: /root/autoleft_backups/db_20260824_135031.sql
Aug 24 13:50:38 vmi3306453 autoleft-deploy[186762]: Aug 24 13:50:35 vmi3306453 autoleft-deploy[186685]: Operations to perform:
Aug 24 13:50:38 vmi3306453 autoleft-deploy[186762]: Aug 24 13:50:35 vmi3306453 autoleft-deploy[186685]:   Apply all migrations: accounts, admin, analytics, auth, broadcasts, contenttypes, conversations, listings, payments, sessions
Aug 24 13:50:38 vmi3306453 autoleft-deploy[186762]: Aug 24 13:50:35 vmi3306453 autoleft-deploy[186685]: Running migrations:
Aug 24 13:50:38 vmi3306453 autoleft-deploy[186762]: Aug 24 13:50:35 vmi3306453 autoleft-deploy[186685]:   No migrations to apply.
Aug 24 13:50:38 vmi3306453 autoleft-deploy[186762]: Aug 24 13:50:35 vmi3306453 autoleft-deploy[186688]: 0 static files copied to '/root/autoleft/staticfiles', 142 unmodified.
Aug 24 13:50:38 vmi3306453 autoleft-deploy[186762]: Aug 24 13:50:36 vmi3306453 autoleft-deploy[186662]: [13:50:36] Restartinam gunicorn.service
Aug 24 13:50:38 vmi3306453 autoleft-deploy[186762]: Aug 24 13:50:37 vmi3306453 autoleft-deploy[186662]: [13:50:37] Health OK (1/10)
Aug 24 13:50:38 vmi3306453 autoleft-deploy[186762]: Aug 24 13:50:37 vmi3306453 autoleft-deploy[186662]: [13:50:37] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Aug 24 13:50:38 vmi3306453 autoleft-deploy[186762]: Aug 24 13:50:37 vmi3306453 autoleft-deploy[186662]: [13:50:37] === Deploy OK ===
Aug 24 13:50:38 vmi3306453 autoleft-deploy[186762]: Aug 24 13:50:37 vmi3306453 autoleft-deploy[186527]: [2026-08-24 13:50:37] ✅ Deploy OK — gyvai veikia d734969
Aug 24 13:50:38 vmi3306453 autoleft-deploy[186762]: ```
Aug 24 13:50:38 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 13:50:38 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 13:50:38 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 10.282s CPU time.
Aug 24 13:51:41 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 13:51:43 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 13:51:43 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 13:51:43 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.071s CPU time.
Aug 24 13:52:52 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 13:52:53 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 13:52:53 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 13:53:59 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
