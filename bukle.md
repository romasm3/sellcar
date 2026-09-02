# Serverio būklė

Sugeneruota: 2026-09-02 13:36:24 CEST

## Kodas

```
sukasi:      7e4bcbe fix(antraste): mobili antraštė ir šalies juosta 1:1 pagal demo
origin/master: 7e4bcbe fix(antraste): mobili antraštė ir šalies juosta 1:1 pagal demo
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
HTTP 301, 0.002020s
```

## Skelbimų būsenos

```

Listing — iš viso 35
  active        18   MATOMAS
  draft          9   nematomas
  expired        8   nematomas
  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─
  nematomi dėl būsenos:      17
  iš jų pasibaigę (expires_at praeityje): 8
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
/dev/sda1       291G   49G  243G  17% /
```

## Paskutinis auto-deploy

```
Sep 02 13:35:59 vmi3306453 autoleft-deploy[3653868]: Sep 02 13:35:17 vmi3306453 autoleft-deploy[3653277]: [13:35:17] === Deploy pradžia (20260902_133517) ===
Sep 02 13:35:59 vmi3306453 autoleft-deploy[3653868]: Sep 02 13:35:18 vmi3306453 autoleft-deploy[3653277]: [13:35:18] Šablonai/statiniai keitėsi — tikrinsim CSS vardą.
Sep 02 13:35:59 vmi3306453 autoleft-deploy[3653868]: Sep 02 13:35:50 vmi3306453 autoleft-deploy[3653277]: [13:35:50] DB dumpas: /root/autoleft_backups/db_20260902_133517.sql
Sep 02 13:35:59 vmi3306453 autoleft-deploy[3653868]: Sep 02 13:35:50 vmi3306453 autoleft-deploy[3653277]: [13:35:50] Versija: 7e4bcbea23b5
Sep 02 13:35:59 vmi3306453 autoleft-deploy[3653868]: Sep 02 13:35:52 vmi3306453 autoleft-deploy[3653696]: Operations to perform:
Sep 02 13:35:59 vmi3306453 autoleft-deploy[3653868]: Sep 02 13:35:52 vmi3306453 autoleft-deploy[3653696]:   Apply all migrations: accounts, admin, analytics, auth, broadcasts, contenttypes, conversations, imones, listings, payments, sessions
Sep 02 13:35:59 vmi3306453 autoleft-deploy[3653868]: Sep 02 13:35:52 vmi3306453 autoleft-deploy[3653696]: Running migrations:
Sep 02 13:35:59 vmi3306453 autoleft-deploy[3653868]: Sep 02 13:35:52 vmi3306453 autoleft-deploy[3653696]:   No migrations to apply.
Sep 02 13:35:59 vmi3306453 autoleft-deploy[3653868]: Sep 02 13:35:53 vmi3306453 autoleft-deploy[3653716]: 1 static file copied to '/root/autoleft/staticfiles', 216 unmodified, 125 post-processed.
Sep 02 13:35:59 vmi3306453 autoleft-deploy[3653868]: Sep 02 13:35:53 vmi3306453 autoleft-deploy[3653277]: [13:35:53] Restartinam gunicorn.service
Sep 02 13:35:59 vmi3306453 autoleft-deploy[3653868]: Sep 02 13:35:55 vmi3306453 autoleft-deploy[3653277]: [13:35:55] Health OK (1/10)
Sep 02 13:35:59 vmi3306453 autoleft-deploy[3653868]: Sep 02 13:35:56 vmi3306453 autoleft-deploy[3653277]: [13:35:56] ❌ Šablonai/statiniai keitėsi, bet CSS vardas liko style.df8265b02e1b.css.
Sep 02 13:35:59 vmi3306453 autoleft-deploy[3653868]: Sep 02 13:35:56 vmi3306453 autoleft-deploy[3653277]: [13:35:56]    Naršyklės gaus seną failą — deploy stabdomas.
Sep 02 13:35:59 vmi3306453 autoleft-deploy[3653868]: Sep 02 13:35:56 vmi3306453 autoleft-deploy[3653277]: [13:35:56] ⚠️  ĮSPĖJIMAS: statinių maišas neatsinaujino, kaip tikėtasi.
Sep 02 13:35:59 vmi3306453 autoleft-deploy[3653868]: Sep 02 13:35:56 vmi3306453 autoleft-deploy[3653277]: [13:35:56] ⚠️  Kodas NEATSUKAMAS — svetainė veikia. Lankytojų naršyklės
Sep 02 13:35:59 vmi3306453 autoleft-deploy[3653868]: Sep 02 13:35:56 vmi3306453 autoleft-deploy[3653277]: [13:35:56] ⚠️  gali kurį laiką rodyti seną CSS; patikrink rankiniu būdu:
Sep 02 13:35:59 vmi3306453 autoleft-deploy[3653868]: Sep 02 13:35:56 vmi3306453 autoleft-deploy[3653277]: [13:35:56] ⚠️    curl -s https://autoleft.com/ | grep -o 'style\.[a-z0-9]*\.css'
Sep 02 13:35:59 vmi3306453 autoleft-deploy[3653868]: Sep 02 13:35:56 vmi3306453 autoleft-deploy[3653277]: [13:35:56] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Sep 02 13:35:59 vmi3306453 autoleft-deploy[3653868]: Sep 02 13:35:56 vmi3306453 autoleft-deploy[3653277]: [13:35:56] === Deploy OK ===
Sep 02 13:35:59 vmi3306453 autoleft-deploy[3653868]: Sep 02 13:35:56 vmi3306453 autoleft-deploy[3653109]: [2026-09-02 13:35:56] ✅ Deploy OK — gyvai veikia 7e4bcbe
Sep 02 13:35:59 vmi3306453 autoleft-deploy[3653868]: ```
Sep 02 13:35:59 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 13:35:59 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 13:35:59 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 23.027s CPU time.
Sep 02 13:36:24 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
