# Serverio būklė

Sugeneruota: 2026-09-02 10:46:23 CEST

## Kodas

```
sukasi:      c61406f test(juosta): elgsenos patikra ir nuolatinė taisyklė
origin/master: c61406f test(juosta): elgsenos patikra ir nuolatinė taisyklė
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
HTTP 301, 0.002811s
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
/dev/sda1       291G   47G  244G  17% /
```

## Paskutinis auto-deploy

```
Sep 02 10:45:18 vmi3306453 autoleft-deploy[3531289]:     c61406f test(juosta): elgsenos patikra ir nuolatinė taisyklė
Sep 02 10:45:18 vmi3306453 autoleft-deploy[3531289]:     cb96f22 fix(juosta): filtras tik renka reikšmę — puslapis nebeperkraunamas
Sep 02 10:45:18 vmi3306453 autoleft-deploy[3531289]:     97b01c9 fix(paieska): „Galia, kW" pasiūlymai — skaitinės reikšmės
Sep 02 10:45:18 vmi3306453 autoleft-deploy[3531266]: [2026-09-02 10:45:18] Kodas atnaujintas iki c61406f
Sep 02 10:45:28 vmi3306453 autoleft-deploy[3531266]: [2026-09-02 10:45:28] Patikra praėjo
Sep 02 10:45:28 vmi3306453 autoleft-deploy[3531406]: [10:45:28] === Deploy pradžia (20260902_104528) ===
Sep 02 10:45:28 vmi3306453 autoleft-deploy[3531406]: [10:45:28] Šablonai/statiniai keitėsi — tikrinsim CSS vardą.
Sep 02 10:46:17 vmi3306453 autoleft-deploy[3531406]: [10:46:17] DB dumpas: /root/autoleft_backups/db_20260902_104528.sql
Sep 02 10:46:17 vmi3306453 autoleft-deploy[3531406]: [10:46:17] Versija: c61406f6953d
Sep 02 10:46:19 vmi3306453 autoleft-deploy[3531956]: Operations to perform:
Sep 02 10:46:19 vmi3306453 autoleft-deploy[3531956]:   Apply all migrations: accounts, admin, analytics, auth, broadcasts, contenttypes, conversations, imones, listings, payments, sessions
Sep 02 10:46:19 vmi3306453 autoleft-deploy[3531956]: Running migrations:
Sep 02 10:46:19 vmi3306453 autoleft-deploy[3531956]:   No migrations to apply.
Sep 02 10:46:20 vmi3306453 autoleft-deploy[3531981]: 1 static file copied to '/root/autoleft/staticfiles', 216 unmodified, 125 post-processed.
Sep 02 10:46:20 vmi3306453 autoleft-deploy[3531406]: [10:46:20] Restartinam gunicorn.service
Sep 02 10:46:22 vmi3306453 autoleft-deploy[3531406]: [10:46:22] Health OK (1/10)
Sep 02 10:46:23 vmi3306453 autoleft-deploy[3531406]: [10:46:23] ❌ Šablonai/statiniai keitėsi, bet CSS vardas liko style.df8265b02e1b.css.
Sep 02 10:46:23 vmi3306453 autoleft-deploy[3531406]: [10:46:23]    Naršyklės gaus seną failą — deploy stabdomas.
Sep 02 10:46:23 vmi3306453 autoleft-deploy[3531406]: [10:46:23] ⚠️  ĮSPĖJIMAS: statinių maišas neatsinaujino, kaip tikėtasi.
Sep 02 10:46:23 vmi3306453 autoleft-deploy[3531406]: [10:46:23] ⚠️  Kodas NEATSUKAMAS — svetainė veikia. Lankytojų naršyklės
Sep 02 10:46:23 vmi3306453 autoleft-deploy[3531406]: [10:46:23] ⚠️  gali kurį laiką rodyti seną CSS; patikrink rankiniu būdu:
Sep 02 10:46:23 vmi3306453 autoleft-deploy[3531406]: [10:46:23] ⚠️    curl -s https://autoleft.com/ | grep -o 'style\.[a-z0-9]*\.css'
Sep 02 10:46:23 vmi3306453 autoleft-deploy[3531406]: [10:46:23] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Sep 02 10:46:23 vmi3306453 autoleft-deploy[3531406]: [10:46:23] === Deploy OK ===
Sep 02 10:46:23 vmi3306453 autoleft-deploy[3531266]: [2026-09-02 10:46:23] ✅ Deploy OK — gyvai veikia c61406f
```
