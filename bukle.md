# Serverio būklė

Sugeneruota: 2026-08-27 13:16:20 CEST

## Kodas

```
sukasi:      374977c feat(antraštė): kompaktiška paieška visuose puslapiuose
origin/master: 374977c feat(antraštė): kompaktiška paieška visuose puslapiuose
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
HTTP 301, 0.001822s
```

## Skelbimų būsenos

```

Listing — iš viso 35
  active        22   MATOMAS
  draft          9   nematomas
  expired        4   nematomas
  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─
  nematomi dėl būsenos:      13
  iš jų pasibaigę (expires_at praeityje): 4
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
/dev/sda1       291G   18G  273G   7% /
```

## Paskutinis auto-deploy

```
Aug 27 13:14:00 vmi3306453 autoleft-deploy[1903022]: Aug 27 13:13:42 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 13:14:00 vmi3306453 autoleft-deploy[1903022]: Aug 27 13:13:42 vmi3306453 autoleft-deploy[1902646]: [2026-08-27 13:13:42] === Naujų commit'ų rasta: 374977c → 0736ac3 ===
Aug 27 13:14:00 vmi3306453 autoleft-deploy[1903022]: Aug 27 13:13:42 vmi3306453 autoleft-deploy[1902646]: [2026-08-27 13:13:42] Kodas atnaujintas iki 0736ac3
Aug 27 13:14:00 vmi3306453 autoleft-deploy[1903022]: Aug 27 13:13:48 vmi3306453 autoleft-deploy[1902646]: [2026-08-27 13:13:48] Patikra praėjo
Aug 27 13:14:00 vmi3306453 autoleft-deploy[1903022]: Aug 27 13:13:48 vmi3306453 autoleft-deploy[1902831]: [13:13:48] === Deploy pradžia (20260827_131348) ===
Aug 27 13:14:00 vmi3306453 autoleft-deploy[1903022]: Aug 27 13:13:55 vmi3306453 autoleft-deploy[1902831]: [13:13:55] DB dumpas: /root/autoleft_backups/db_20260827_131348.sql
Aug 27 13:14:00 vmi3306453 autoleft-deploy[1903022]: Aug 27 13:13:56 vmi3306453 autoleft-deploy[1902905]: Operations to perform:
Aug 27 13:14:00 vmi3306453 autoleft-deploy[1903022]: Aug 27 13:13:56 vmi3306453 autoleft-deploy[1902905]:   Apply all migrations: accounts, admin, analytics, auth, broadcasts, contenttypes, conversations, listings, payments, sessions
Aug 27 13:14:00 vmi3306453 autoleft-deploy[1903022]: Aug 27 13:13:56 vmi3306453 autoleft-deploy[1902905]: Running migrations:
Aug 27 13:14:00 vmi3306453 autoleft-deploy[1903022]: Aug 27 13:13:56 vmi3306453 autoleft-deploy[1902905]:   No migrations to apply.
Aug 27 13:14:00 vmi3306453 autoleft-deploy[1903022]: Aug 27 13:13:57 vmi3306453 autoleft-deploy[1902927]: 0 static files copied to '/root/autoleft/staticfiles', 164 unmodified.
Aug 27 13:14:00 vmi3306453 autoleft-deploy[1903022]: Aug 27 13:13:57 vmi3306453 autoleft-deploy[1902831]: [13:13:57] Restartinam gunicorn.service
Aug 27 13:14:00 vmi3306453 autoleft-deploy[1903022]: Aug 27 13:13:58 vmi3306453 autoleft-deploy[1902831]: [13:13:58] Health OK (1/10)
Aug 27 13:14:00 vmi3306453 autoleft-deploy[1903022]: Aug 27 13:13:58 vmi3306453 autoleft-deploy[1902831]: [13:13:58] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Aug 27 13:14:00 vmi3306453 autoleft-deploy[1903022]: Aug 27 13:13:58 vmi3306453 autoleft-deploy[1902831]: [13:13:58] === Deploy OK ===
Aug 27 13:14:00 vmi3306453 autoleft-deploy[1903022]: Aug 27 13:13:58 vmi3306453 autoleft-deploy[1902646]: [2026-08-27 13:13:58] ✅ Deploy OK — gyvai veikia 0736ac3
Aug 27 13:14:00 vmi3306453 autoleft-deploy[1903022]: ```
Aug 27 13:14:00 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 13:14:00 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 13:14:00 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 10.427s CPU time.
Aug 27 13:14:58 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 13:15:00 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 13:15:00 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 13:15:00 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.182s CPU time.
Aug 27 13:16:20 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
