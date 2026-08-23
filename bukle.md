# Serverio būklė

Sugeneruota: 2026-08-23 15:34:59 CEST

## Kodas

```
sukasi:      4d1d356 fix(paieska): diapazonai telefone — eilutė rodo reikšmę, ekrane abi ribos
origin/master: 4d1d356 fix(paieska): diapazonai telefone — eilutė rodo reikšmę, ekrane abi ribos
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
HTTP 301, 0.001093s
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
Aug 23 15:33:47 vmi3306453 autoleft-deploy[4170456]: Aug 23 15:32:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 15:33:47 vmi3306453 autoleft-deploy[4170456]: Aug 23 15:32:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 15:33:47 vmi3306453 autoleft-deploy[4170456]: Aug 23 15:32:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 15:33:47 vmi3306453 autoleft-deploy[4170456]: Aug 23 15:33:35 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 15:33:47 vmi3306453 autoleft-deploy[4170456]: Aug 23 15:33:36 vmi3306453 autoleft-deploy[4170240]: [2026-08-23 15:33:36] === Naujų commit'ų rasta: 9b99d3e → 4d1d356 ===
Aug 23 15:33:47 vmi3306453 autoleft-deploy[4170456]: Aug 23 15:33:36 vmi3306453 autoleft-deploy[4170254]:     4d1d356 fix(paieska): diapazonai telefone — eilutė rodo reikšmę, ekrane abi ribos
Aug 23 15:33:47 vmi3306453 autoleft-deploy[4170456]: Aug 23 15:33:36 vmi3306453 autoleft-deploy[4170240]: [2026-08-23 15:33:36] Kodas atnaujintas iki 4d1d356
Aug 23 15:33:47 vmi3306453 autoleft-deploy[4170456]: Aug 23 15:33:42 vmi3306453 autoleft-deploy[4170240]: [2026-08-23 15:33:42] Patikra praėjo
Aug 23 15:33:47 vmi3306453 autoleft-deploy[4170456]: Aug 23 15:33:42 vmi3306453 autoleft-deploy[4170340]: [15:33:42] === Deploy pradžia (20260823_153342) ===
Aug 23 15:33:47 vmi3306453 autoleft-deploy[4170456]: Aug 23 15:33:43 vmi3306453 autoleft-deploy[4170340]: [15:33:43] DB dumpas: /root/autoleft_backups/db_20260823_153342.sql
Aug 23 15:33:47 vmi3306453 autoleft-deploy[4170456]: Aug 23 15:33:44 vmi3306453 autoleft-deploy[4170356]: Operations to perform:
Aug 23 15:33:47 vmi3306453 autoleft-deploy[4170456]: Aug 23 15:33:44 vmi3306453 autoleft-deploy[4170356]:   Apply all migrations: accounts, admin, analytics, auth, broadcasts, contenttypes, conversations, listings, payments, sessions
Aug 23 15:33:47 vmi3306453 autoleft-deploy[4170456]: Aug 23 15:33:44 vmi3306453 autoleft-deploy[4170356]: Running migrations:
Aug 23 15:33:47 vmi3306453 autoleft-deploy[4170456]: Aug 23 15:33:44 vmi3306453 autoleft-deploy[4170356]:   No migrations to apply.
Aug 23 15:33:47 vmi3306453 autoleft-deploy[4170456]: Aug 23 15:33:45 vmi3306453 autoleft-deploy[4170361]: 0 static files copied to '/root/autoleft/staticfiles', 140 unmodified.
Aug 23 15:33:47 vmi3306453 autoleft-deploy[4170456]: Aug 23 15:33:45 vmi3306453 autoleft-deploy[4170340]: [15:33:45] Restartinam gunicorn.service
Aug 23 15:33:47 vmi3306453 autoleft-deploy[4170456]: Aug 23 15:33:46 vmi3306453 autoleft-deploy[4170340]: [15:33:46] Health OK (1/10)
Aug 23 15:33:47 vmi3306453 autoleft-deploy[4170456]: Aug 23 15:33:46 vmi3306453 autoleft-deploy[4170340]: [15:33:46] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Aug 23 15:33:47 vmi3306453 autoleft-deploy[4170456]: Aug 23 15:33:46 vmi3306453 autoleft-deploy[4170340]: [15:33:46] === Deploy OK ===
Aug 23 15:33:47 vmi3306453 autoleft-deploy[4170456]: Aug 23 15:33:46 vmi3306453 autoleft-deploy[4170240]: [2026-08-23 15:33:46] ✅ Deploy OK — gyvai veikia 4d1d356
Aug 23 15:33:47 vmi3306453 autoleft-deploy[4170456]: ```
Aug 23 15:33:47 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 15:33:47 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 15:33:47 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 8.247s CPU time.
Aug 23 15:34:59 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
