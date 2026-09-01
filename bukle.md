# Serverio būklė

Sugeneruota: 2026-09-01 17:55:48 CEST

## Kodas

```
sukasi:      3e6b957 feat(veliava): vėliava po pavadinimo ir kortelių vietos eilutėje
origin/master: 3e6b957 feat(veliava): vėliava po pavadinimo ir kortelių vietos eilutėje
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
HTTP 301, 0.001126s
```

## Skelbimų būsenos

```

Listing — iš viso 35
  active        19   MATOMAS
  draft          9   nematomas
  expired        7   nematomas
  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─
  nematomi dėl būsenos:      16
  iš jų pasibaigę (expires_at praeityje): 7
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
/dev/sda1       291G   38G  253G  13% /
```

## Paskutinis auto-deploy

```
Sep 01 17:52:10 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 01 17:52:10 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 17:52:10 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.541s CPU time.
Sep 01 17:53:26 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 01 17:53:28 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 01 17:53:28 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 17:53:28 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.346s CPU time.
Sep 01 17:55:05 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 01 17:55:06 vmi3306453 autoleft-deploy[2783306]: [2026-09-01 17:55:06] === Naujų commit'ų rasta: 9d3bb12 → 3e6b957 ===
Sep 01 17:55:06 vmi3306453 autoleft-deploy[2783338]:     3e6b957 feat(veliava): vėliava po pavadinimo ir kortelių vietos eilutėje
Sep 01 17:55:06 vmi3306453 autoleft-deploy[2783338]:     253dfa7 feat(salis): viena šalies reikšmė visai svetainei
Sep 01 17:55:06 vmi3306453 autoleft-deploy[2783306]: [2026-09-01 17:55:06] Kodas atnaujintas iki 3e6b957
Sep 01 17:55:17 vmi3306453 autoleft-deploy[2783306]: [2026-09-01 17:55:17] Patikra praėjo
Sep 01 17:55:17 vmi3306453 autoleft-deploy[2783481]: [17:55:17] === Deploy pradžia (20260901_175517) ===
Sep 01 17:55:44 vmi3306453 autoleft-deploy[2783481]: [17:55:44] DB dumpas: /root/autoleft_backups/db_20260901_175517.sql
Sep 01 17:55:45 vmi3306453 autoleft-deploy[2783807]: Operations to perform:
Sep 01 17:55:45 vmi3306453 autoleft-deploy[2783807]:   Apply all migrations: accounts, admin, analytics, auth, broadcasts, contenttypes, conversations, imones, listings, payments, sessions
Sep 01 17:55:45 vmi3306453 autoleft-deploy[2783807]: Running migrations:
Sep 01 17:55:45 vmi3306453 autoleft-deploy[2783807]:   No migrations to apply.
Sep 01 17:55:45 vmi3306453 autoleft-deploy[2783826]: 2 static files copied to '/root/autoleft/staticfiles', 214 unmodified.
Sep 01 17:55:46 vmi3306453 autoleft-deploy[2783481]: [17:55:46] Restartinam gunicorn.service
Sep 01 17:55:47 vmi3306453 autoleft-deploy[2783481]: [17:55:47] Health OK (1/10)
Sep 01 17:55:47 vmi3306453 autoleft-deploy[2783481]: [17:55:47] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Sep 01 17:55:48 vmi3306453 autoleft-deploy[2783481]: [17:55:48] === Deploy OK ===
Sep 01 17:55:48 vmi3306453 autoleft-deploy[2783306]: [2026-09-01 17:55:48] ✅ Deploy OK — gyvai veikia 3e6b957
```
