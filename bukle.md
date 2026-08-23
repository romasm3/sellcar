# Serverio būklė

Sugeneruota: 2026-08-23 15:16:08 CEST

## Kodas

```
sukasi:      9b99d3e test(paieska): telefono filtro pasirinkimo ekrano testai (705 patikros)
origin/master: 9b99d3e test(paieska): telefono filtro pasirinkimo ekrano testai (705 patikros)
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
HTTP 301, 0.001183s
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
Aug 23 15:13:48 vmi3306453 autoleft-deploy[4167299]: Aug 23 15:13:37 vmi3306453 autoleft-deploy[4167096]:     9fd7760 fix(paieska): telefone pasirinkus filtrą nebešokama į rezultatus
Aug 23 15:13:48 vmi3306453 autoleft-deploy[4167299]: Aug 23 15:13:37 vmi3306453 autoleft-deploy[4167096]:     fecac1b fix(templates): /contact/ metė 500 — {% load %} prieš {% extends %}
Aug 23 15:13:48 vmi3306453 autoleft-deploy[4167299]: Aug 23 15:13:37 vmi3306453 autoleft-deploy[4167082]: [2026-08-23 15:13:37] Kodas atnaujintas iki 9b99d3e
Aug 23 15:13:48 vmi3306453 autoleft-deploy[4167299]: Aug 23 15:13:43 vmi3306453 autoleft-deploy[4167082]: [2026-08-23 15:13:43] Patikra praėjo
Aug 23 15:13:48 vmi3306453 autoleft-deploy[4167299]: Aug 23 15:13:43 vmi3306453 autoleft-deploy[4167183]: [15:13:43] === Deploy pradžia (20260823_151343) ===
Aug 23 15:13:48 vmi3306453 autoleft-deploy[4167299]: Aug 23 15:13:45 vmi3306453 autoleft-deploy[4167183]: [15:13:45] DB dumpas: /root/autoleft_backups/db_20260823_151343.sql
Aug 23 15:13:48 vmi3306453 autoleft-deploy[4167299]: Aug 23 15:13:45 vmi3306453 autoleft-deploy[4167198]: Operations to perform:
Aug 23 15:13:48 vmi3306453 autoleft-deploy[4167299]: Aug 23 15:13:45 vmi3306453 autoleft-deploy[4167198]:   Apply all migrations: accounts, admin, analytics, auth, broadcasts, contenttypes, conversations, listings, payments, sessions
Aug 23 15:13:48 vmi3306453 autoleft-deploy[4167299]: Aug 23 15:13:45 vmi3306453 autoleft-deploy[4167198]: Running migrations:
Aug 23 15:13:48 vmi3306453 autoleft-deploy[4167299]: Aug 23 15:13:45 vmi3306453 autoleft-deploy[4167198]:   No migrations to apply.
Aug 23 15:13:48 vmi3306453 autoleft-deploy[4167299]: Aug 23 15:13:46 vmi3306453 autoleft-deploy[4167206]: 0 static files copied to '/root/autoleft/staticfiles', 140 unmodified.
Aug 23 15:13:48 vmi3306453 autoleft-deploy[4167299]: Aug 23 15:13:46 vmi3306453 autoleft-deploy[4167183]: [15:13:46] Restartinam gunicorn.service
Aug 23 15:13:48 vmi3306453 autoleft-deploy[4167299]: Aug 23 15:13:47 vmi3306453 autoleft-deploy[4167183]: [15:13:47] Health OK (1/10)
Aug 23 15:13:48 vmi3306453 autoleft-deploy[4167299]: Aug 23 15:13:47 vmi3306453 autoleft-deploy[4167183]: [15:13:47] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Aug 23 15:13:48 vmi3306453 autoleft-deploy[4167299]: Aug 23 15:13:47 vmi3306453 autoleft-deploy[4167183]: [15:13:47] === Deploy OK ===
Aug 23 15:13:48 vmi3306453 autoleft-deploy[4167299]: Aug 23 15:13:47 vmi3306453 autoleft-deploy[4167082]: [2026-08-23 15:13:47] ✅ Deploy OK — gyvai veikia 9b99d3e
Aug 23 15:13:48 vmi3306453 autoleft-deploy[4167299]: ```
Aug 23 15:13:48 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 15:13:48 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 15:13:48 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 8.407s CPU time.
Aug 23 15:15:00 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 15:15:03 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 15:15:03 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 15:15:03 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.836s CPU time.
Aug 23 15:16:08 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
