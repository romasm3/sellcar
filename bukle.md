# Serverio būklė

Sugeneruota: 2026-08-31 12:58:42 CEST

## Kodas

```
sukasi:      fbefc1c feat(kalbos): grąžintos visos 13 kalbų perjungiklyje
origin/master: fbefc1c feat(kalbos): grąžintos visos 13 kalbų perjungiklyje
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
HTTP 301, 0.001366s
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
/dev/sda1       291G   26G  266G   9% /
```

## Paskutinis auto-deploy

```
Aug 31 12:55:29 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 31 12:55:31 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 31 12:55:31 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 31 12:55:31 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.494s CPU time.
Aug 31 12:56:32 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 31 12:56:35 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 31 12:56:35 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 31 12:56:35 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.671s CPU time.
Aug 31 12:58:07 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 31 12:58:07 vmi3306453 autoleft-deploy[1537171]: [2026-08-31 12:58:07] === Naujų commit'ų rasta: a936f90 → fbefc1c ===
Aug 31 12:58:07 vmi3306453 autoleft-deploy[1537194]:     fbefc1c feat(kalbos): grąžintos visos 13 kalbų perjungiklyje
Aug 31 12:58:07 vmi3306453 autoleft-deploy[1537171]: [2026-08-31 12:58:07] Kodas atnaujintas iki fbefc1c
Aug 31 12:58:16 vmi3306453 autoleft-deploy[1537171]: [2026-08-31 12:58:16] Patikra praėjo
Aug 31 12:58:16 vmi3306453 autoleft-deploy[1537294]: [12:58:16] === Deploy pradžia (20260831_125816) ===
Aug 31 12:58:38 vmi3306453 autoleft-deploy[1537294]: [12:58:38] DB dumpas: /root/autoleft_backups/db_20260831_125816.sql
Aug 31 12:58:39 vmi3306453 autoleft-deploy[1537554]: Operations to perform:
Aug 31 12:58:39 vmi3306453 autoleft-deploy[1537554]:   Apply all migrations: accounts, admin, analytics, auth, broadcasts, contenttypes, conversations, imones, listings, payments, sessions
Aug 31 12:58:39 vmi3306453 autoleft-deploy[1537554]: Running migrations:
Aug 31 12:58:39 vmi3306453 autoleft-deploy[1537554]:   No migrations to apply.
Aug 31 12:58:40 vmi3306453 autoleft-deploy[1537583]: 0 static files copied to '/root/autoleft/staticfiles', 170 unmodified.
Aug 31 12:58:40 vmi3306453 autoleft-deploy[1537294]: [12:58:40] Restartinam gunicorn.service
Aug 31 12:58:42 vmi3306453 autoleft-deploy[1537294]: [12:58:42] Health OK (1/10)
Aug 31 12:58:42 vmi3306453 autoleft-deploy[1537294]: [12:58:42] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Aug 31 12:58:42 vmi3306453 autoleft-deploy[1537294]: [12:58:42] === Deploy OK ===
Aug 31 12:58:42 vmi3306453 autoleft-deploy[1537171]: [2026-08-31 12:58:42] ✅ Deploy OK — gyvai veikia fbefc1c
```
