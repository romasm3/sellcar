# Serverio būklė

Sugeneruota: 2026-08-25 23:27:27 CEST

## Kodas

```
sukasi:      056083b feat(formos): vieningas privalomų laukų klaidų žymėjimas visose /create/
origin/master: 056083b feat(formos): vieningas privalomų laukų klaidų žymėjimas visose /create/
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
HTTP 301, 0.001213s
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
/dev/sda1       291G   17G  275G   6% /
```

## Paskutinis auto-deploy

```
Aug 25 23:24:56 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 25 23:24:58 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 25 23:24:58 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 25 23:24:58 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.105s CPU time.
Aug 25 23:26:07 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 25 23:26:09 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 25 23:26:09 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 25 23:26:09 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.067s CPU time.
Aug 25 23:27:12 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 25 23:27:12 vmi3306453 autoleft-deploy[894914]: [2026-08-25 23:27:12] === Naujų commit'ų rasta: 4ce84b3 → 056083b ===
Aug 25 23:27:12 vmi3306453 autoleft-deploy[894931]:     056083b feat(formos): vieningas privalomų laukų klaidų žymėjimas visose /create/
Aug 25 23:27:13 vmi3306453 autoleft-deploy[894914]: [2026-08-25 23:27:13] Kodas atnaujintas iki 056083b
Aug 25 23:27:19 vmi3306453 autoleft-deploy[894914]: [2026-08-25 23:27:19] Patikra praėjo
Aug 25 23:27:19 vmi3306453 autoleft-deploy[894977]: [23:27:19] === Deploy pradžia (20260825_232719) ===
Aug 25 23:27:23 vmi3306453 autoleft-deploy[894977]: [23:27:23] DB dumpas: /root/autoleft_backups/db_20260825_232719.sql
Aug 25 23:27:24 vmi3306453 autoleft-deploy[895014]: Operations to perform:
Aug 25 23:27:24 vmi3306453 autoleft-deploy[895014]:   Apply all migrations: accounts, admin, analytics, auth, broadcasts, contenttypes, conversations, listings, payments, sessions
Aug 25 23:27:24 vmi3306453 autoleft-deploy[895014]: Running migrations:
Aug 25 23:27:24 vmi3306453 autoleft-deploy[895014]:   No migrations to apply.
Aug 25 23:27:25 vmi3306453 autoleft-deploy[895026]: 2 static files copied to '/root/autoleft/staticfiles', 159 unmodified.
Aug 25 23:27:25 vmi3306453 autoleft-deploy[894977]: [23:27:25] Restartinam gunicorn.service
Aug 25 23:27:27 vmi3306453 autoleft-deploy[894977]: [23:27:27] Health OK (1/10)
Aug 25 23:27:27 vmi3306453 autoleft-deploy[894977]: [23:27:27] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Aug 25 23:27:27 vmi3306453 autoleft-deploy[894977]: [23:27:27] === Deploy OK ===
Aug 25 23:27:27 vmi3306453 autoleft-deploy[894914]: [2026-08-25 23:27:27] ✅ Deploy OK — gyvai veikia 056083b
```
