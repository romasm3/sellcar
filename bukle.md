# Serverio būklė

Sugeneruota: 2026-08-23 16:20:31 CEST

## Kodas

```
sukasi:      62c5b05 fix(paieska): „Detali paieška" telefone — laukai su reikšmių ekranais
origin/master: 62c5b05 fix(paieska): „Detali paieška" telefone — laukai su reikšmių ekranais
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
HTTP 301, 0.001271s
```

## Skelbimų būsenos

```

Listing — iš viso 47
  active        33   MATOMAS
  draft         11   nematomas
  expired        3   nematomas
  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─
  nematomi dėl būsenos:      14
  iš jų pasibaigę (expires_at praeityje): 3
  aktyvūs, baigsis per 7 d.: 3
  aktyvūs be pabaigos datos: 16 (pvz. testiniai)
Truck: skelbimų nėra.
WheelListing: skelbimų nėra.

Viešame sąraše matomi tik status="active" (+ neseniai parduoti).
Jei tavo seni skelbimai yra "expired" — juos reikia aktyvuoti iš naujo,
o ne taisyti kode.
```

## Vietos diske

```
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       291G   14G  277G   5% /
```

## Paskutinis auto-deploy

```
Aug 23 16:18:57 vmi3306453 autoleft-deploy[4177588]: Aug 23 16:17:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 16:18:57 vmi3306453 autoleft-deploy[4177588]: Aug 23 16:17:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 16:18:57 vmi3306453 autoleft-deploy[4177588]: Aug 23 16:17:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.055s CPU time.
Aug 23 16:18:57 vmi3306453 autoleft-deploy[4177588]: Aug 23 16:18:44 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 16:18:57 vmi3306453 autoleft-deploy[4177588]: Aug 23 16:18:45 vmi3306453 autoleft-deploy[4177385]: [2026-08-23 16:18:45] === Naujų commit'ų rasta: 7e04dd8 → 62c5b05 ===
Aug 23 16:18:57 vmi3306453 autoleft-deploy[4177588]: Aug 23 16:18:45 vmi3306453 autoleft-deploy[4177399]:     62c5b05 fix(paieska): „Detali paieška" telefone — laukai su reikšmių ekranais
Aug 23 16:18:57 vmi3306453 autoleft-deploy[4177588]: Aug 23 16:18:45 vmi3306453 autoleft-deploy[4177385]: [2026-08-23 16:18:45] Kodas atnaujintas iki 62c5b05
Aug 23 16:18:57 vmi3306453 autoleft-deploy[4177588]: Aug 23 16:18:51 vmi3306453 autoleft-deploy[4177385]: [2026-08-23 16:18:51] Patikra praėjo
Aug 23 16:18:57 vmi3306453 autoleft-deploy[4177588]: Aug 23 16:18:51 vmi3306453 autoleft-deploy[4177473]: [16:18:51] === Deploy pradžia (20260823_161851) ===
Aug 23 16:18:57 vmi3306453 autoleft-deploy[4177588]: Aug 23 16:18:53 vmi3306453 autoleft-deploy[4177473]: [16:18:53] DB dumpas: /root/autoleft_backups/db_20260823_161851.sql
Aug 23 16:18:57 vmi3306453 autoleft-deploy[4177588]: Aug 23 16:18:54 vmi3306453 autoleft-deploy[4177491]: Operations to perform:
Aug 23 16:18:57 vmi3306453 autoleft-deploy[4177588]: Aug 23 16:18:54 vmi3306453 autoleft-deploy[4177491]:   Apply all migrations: accounts, admin, analytics, auth, broadcasts, contenttypes, conversations, listings, payments, sessions
Aug 23 16:18:57 vmi3306453 autoleft-deploy[4177588]: Aug 23 16:18:54 vmi3306453 autoleft-deploy[4177491]: Running migrations:
Aug 23 16:18:57 vmi3306453 autoleft-deploy[4177588]: Aug 23 16:18:54 vmi3306453 autoleft-deploy[4177491]:   No migrations to apply.
Aug 23 16:18:57 vmi3306453 autoleft-deploy[4177588]: Aug 23 16:18:54 vmi3306453 autoleft-deploy[4177494]: 0 static files copied to '/root/autoleft/staticfiles', 140 unmodified.
Aug 23 16:18:57 vmi3306453 autoleft-deploy[4177588]: Aug 23 16:18:55 vmi3306453 autoleft-deploy[4177473]: [16:18:55] Restartinam gunicorn.service
Aug 23 16:18:57 vmi3306453 autoleft-deploy[4177588]: Aug 23 16:18:55 vmi3306453 autoleft-deploy[4177473]: [16:18:55] Health OK (1/10)
Aug 23 16:18:57 vmi3306453 autoleft-deploy[4177588]: Aug 23 16:18:55 vmi3306453 autoleft-deploy[4177473]: [16:18:55] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Aug 23 16:18:57 vmi3306453 autoleft-deploy[4177588]: Aug 23 16:18:56 vmi3306453 autoleft-deploy[4177473]: [16:18:56] === Deploy OK ===
Aug 23 16:18:57 vmi3306453 autoleft-deploy[4177588]: Aug 23 16:18:56 vmi3306453 autoleft-deploy[4177385]: [2026-08-23 16:18:56] ✅ Deploy OK — gyvai veikia 62c5b05
Aug 23 16:18:57 vmi3306453 autoleft-deploy[4177588]: ```
Aug 23 16:18:57 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 16:18:57 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 16:18:57 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 9.042s CPU time.
Aug 23 16:20:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
