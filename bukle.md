# Serverio būklė

Sugeneruota: 2026-08-24 11:33:41 CEST

## Kodas

```
sukasi:      cd36a44 merge: master (išsaugotų skelbimų pastabos)
origin/master: cd36a44 merge: master (išsaugotų skelbimų pastabos)
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
HTTP 301, 0.001895s
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
  aktyvūs, baigsis per 7 d.: 4
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
/dev/sda1       291G   15G  277G   5% /
```

## Paskutinis auto-deploy

```
Aug 24 11:30:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 11:30:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.092s CPU time.
Aug 24 11:32:13 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 11:32:14 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 11:32:14 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 11:33:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 11:33:31 vmi3306453 autoleft-deploy[145558]: [2026-08-24 11:33:31] === Naujų commit'ų rasta: 7551ce1 → cd36a44 ===
Aug 24 11:33:31 vmi3306453 autoleft-deploy[145573]:     cd36a44 merge: master (išsaugotų skelbimų pastabos)
Aug 24 11:33:31 vmi3306453 autoleft-deploy[145573]:     5c4d0cb test(paieska): „Detali paieška" tikrinama pagal advanced_categories()
Aug 24 11:33:31 vmi3306453 autoleft-deploy[145573]:     d12b69b merge: master (kitos sesijos paieškos ir antispam darbas)
Aug 24 11:33:31 vmi3306453 autoleft-deploy[145573]:     9b3a67c feat(valymas): komanda testiniams skelbimams inventorizuoti ir pašalinti
Aug 24 11:33:31 vmi3306453 autoleft-deploy[145558]: [2026-08-24 11:33:31] Kodas atnaujintas iki cd36a44
Aug 24 11:33:36 vmi3306453 autoleft-deploy[145558]: [2026-08-24 11:33:36] Patikra praėjo
Aug 24 11:33:36 vmi3306453 autoleft-deploy[145638]: [11:33:36] === Deploy pradžia (20260824_113336) ===
Aug 24 11:33:38 vmi3306453 autoleft-deploy[145638]: [11:33:38] DB dumpas: /root/autoleft_backups/db_20260824_113336.sql
Aug 24 11:33:39 vmi3306453 autoleft-deploy[145656]: Operations to perform:
Aug 24 11:33:39 vmi3306453 autoleft-deploy[145656]:   Apply all migrations: accounts, admin, analytics, auth, broadcasts, contenttypes, conversations, listings, payments, sessions
Aug 24 11:33:39 vmi3306453 autoleft-deploy[145656]: Running migrations:
Aug 24 11:33:39 vmi3306453 autoleft-deploy[145656]:   No migrations to apply.
Aug 24 11:33:39 vmi3306453 autoleft-deploy[145663]: 0 static files copied to '/root/autoleft/staticfiles', 140 unmodified.
Aug 24 11:33:39 vmi3306453 autoleft-deploy[145638]: [11:33:39] Restartinam gunicorn.service
Aug 24 11:33:40 vmi3306453 autoleft-deploy[145638]: [11:33:40] Health OK (1/10)
Aug 24 11:33:40 vmi3306453 autoleft-deploy[145638]: [11:33:40] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Aug 24 11:33:41 vmi3306453 autoleft-deploy[145638]: [11:33:41] === Deploy OK ===
Aug 24 11:33:41 vmi3306453 autoleft-deploy[145558]: [2026-08-24 11:33:41] ✅ Deploy OK — gyvai veikia cd36a44
```
