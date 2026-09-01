# Serverio būklė

Sugeneruota: 2026-09-01 13:29:59 CEST

## Kodas

```
sukasi:      19d2c72 feat(kalbos): perjungiklis telefone — meniu, apatinis lakštas ir poraštė
origin/master: 19d2c72 feat(kalbos): perjungiklis telefone — meniu, apatinis lakštas ir poraštė
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
HTTP 301, 0.002897s
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
/dev/sda1       291G   29G  262G  10% /
```

## Paskutinis auto-deploy

```
Sep 01 13:27:08 vmi3306453 autoleft-deploy[2588990]: Sep 01 13:26:34 vmi3306453 autoleft-deploy[2588559]: [13:26:34] === Deploy pradžia (20260901_132634) ===
Sep 01 13:27:08 vmi3306453 autoleft-deploy[2588990]: Sep 01 13:27:01 vmi3306453 autoleft-deploy[2588559]: [13:27:01] DB dumpas: /root/autoleft_backups/db_20260901_132634.sql
Sep 01 13:27:08 vmi3306453 autoleft-deploy[2588990]: Sep 01 13:27:03 vmi3306453 autoleft-deploy[2588845]: Operations to perform:
Sep 01 13:27:08 vmi3306453 autoleft-deploy[2588990]: Sep 01 13:27:03 vmi3306453 autoleft-deploy[2588845]:   Apply all migrations: accounts, admin, analytics, auth, broadcasts, contenttypes, conversations, imones, listings, payments, sessions
Sep 01 13:27:08 vmi3306453 autoleft-deploy[2588990]: Sep 01 13:27:03 vmi3306453 autoleft-deploy[2588845]: Running migrations:
Sep 01 13:27:08 vmi3306453 autoleft-deploy[2588990]: Sep 01 13:27:03 vmi3306453 autoleft-deploy[2588845]:   No migrations to apply.
Sep 01 13:27:08 vmi3306453 autoleft-deploy[2588990]: Sep 01 13:27:04 vmi3306453 autoleft-deploy[2588871]: 0 static files copied to '/root/autoleft/staticfiles', 170 unmodified.
Sep 01 13:27:08 vmi3306453 autoleft-deploy[2588990]: Sep 01 13:27:04 vmi3306453 autoleft-deploy[2588559]: [13:27:04] Restartinam gunicorn.service
Sep 01 13:27:08 vmi3306453 autoleft-deploy[2588990]: Sep 01 13:27:06 vmi3306453 autoleft-deploy[2588559]: [13:27:06] Health OK (1/10)
Sep 01 13:27:08 vmi3306453 autoleft-deploy[2588990]: Sep 01 13:27:06 vmi3306453 autoleft-deploy[2588559]: [13:27:06] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Sep 01 13:27:08 vmi3306453 autoleft-deploy[2588990]: Sep 01 13:27:06 vmi3306453 autoleft-deploy[2588559]: [13:27:06] === Deploy OK ===
Sep 01 13:27:08 vmi3306453 autoleft-deploy[2588990]: Sep 01 13:27:06 vmi3306453 autoleft-deploy[2588428]: [2026-09-01 13:27:06] ✅ Deploy OK — gyvai veikia 19d2c72
Sep 01 13:27:08 vmi3306453 autoleft-deploy[2588990]: ```
Sep 01 13:27:08 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 01 13:27:08 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 13:27:08 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 21.869s CPU time.
Sep 01 13:27:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 01 13:27:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 01 13:27:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 13:27:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.576s CPU time.
Sep 01 13:28:54 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 01 13:28:56 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 01 13:28:56 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 13:28:56 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.511s CPU time.
Sep 01 13:29:59 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
