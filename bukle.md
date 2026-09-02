# Serverio būklė

Sugeneruota: 2026-09-02 19:52:33 CEST

## Kodas

```
sukasi:      831f4c0 feat(vertimai): 404 puslapis rusiškai, nauja patvirtintų terminų partija
origin/master: 831f4c0 feat(vertimai): 404 puslapis rusiškai, nauja patvirtintų terminų partija
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
HTTP 301, 0.002934s
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
  aktyvūs, baigsis per 7 d.: 6
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
/dev/sda1       291G   27G  265G  10% /
```

## Paskutinis auto-deploy

```
Sep 02 19:51:39 vmi3306453 autoleft-deploy[3936471]: [19:51:39] === Deploy pradžia (20260902_195139) ===
Sep 02 19:51:39 vmi3306453 autoleft-deploy[3936471]: [19:51:39] Šablonai/statiniai keitėsi — tikrinsim CSS vardą.
Sep 02 19:51:40 vmi3306453 autoleft-deploy[3936471]: [19:51:40] Vietos diske: 90% laisva (262G).
Sep 02 19:52:27 vmi3306453 autoleft-deploy[3936471]: [19:52:27] DB dumpas: /root/autoleft_backups/db_20260902_195139.sql.gz (131M)
Sep 02 19:52:27 vmi3306453 autoleft-deploy[3936471]: [19:52:27] Senos kopijos ištrintos: 1 (laikom 5 naujausias).
Sep 02 19:52:27 vmi3306453 autoleft-deploy[3936471]: [19:52:27] Kopijos: 5 vnt.,  viso 3.2G,  diske laisva 265G (90%).
Sep 02 19:52:27 vmi3306453 autoleft-deploy[3936471]: [19:52:27] Versija: 831f4c080b6a
Sep 02 19:52:29 vmi3306453 autoleft-deploy[3937098]: Operations to perform:
Sep 02 19:52:29 vmi3306453 autoleft-deploy[3937098]:   Apply all migrations: accounts, admin, analytics, auth, broadcasts, contenttypes, conversations, imones, listings, payments, sessions
Sep 02 19:52:29 vmi3306453 autoleft-deploy[3937098]: Running migrations:
Sep 02 19:52:29 vmi3306453 autoleft-deploy[3937098]:   No migrations to apply.
Sep 02 19:52:30 vmi3306453 autoleft-deploy[3937127]: 0 static files copied to '/root/autoleft/staticfiles', 218 unmodified, 126 post-processed.
Sep 02 19:52:30 vmi3306453 autoleft-deploy[3936471]: [19:52:30] Restartinam gunicorn.service
Sep 02 19:52:32 vmi3306453 autoleft-deploy[3936471]: [19:52:32] Health OK (1/10)
Sep 02 19:52:32 vmi3306453 autoleft-deploy[3936471]: [19:52:32] ❌ Šablonai/statiniai keitėsi, bet CSS vardas liko style.df8265b02e1b.css.
Sep 02 19:52:32 vmi3306453 autoleft-deploy[3936471]: [19:52:32]    Naršyklės gaus seną failą — deploy stabdomas.
Sep 02 19:52:32 vmi3306453 autoleft-deploy[3936471]: [19:52:32] ⚠️  ĮSPĖJIMAS: statinių maišas neatsinaujino, kaip tikėtasi.
Sep 02 19:52:32 vmi3306453 autoleft-deploy[3936471]: [19:52:32] ⚠️  Kodas NEATSUKAMAS — svetainė veikia. Lankytojų naršyklės
Sep 02 19:52:32 vmi3306453 autoleft-deploy[3936471]: [19:52:32] ⚠️  gali kurį laiką rodyti seną CSS; patikrink rankiniu būdu:
Sep 02 19:52:32 vmi3306453 autoleft-deploy[3936471]: [19:52:32] ⚠️    curl -s https://autoleft.com/ | grep -o 'style\.[a-z0-9]*\.css'
Sep 02 19:52:32 vmi3306453 autoleft-deploy[3936471]: [19:52:32] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Sep 02 19:52:33 vmi3306453 autoleft-deploy[3936471]: [19:52:33] Raktai: .env — vietoje.
Sep 02 19:52:33 vmi3306453 autoleft-deploy[3936471]: [19:52:33] Raktai: google-translate-key.json — vietoje.
Sep 02 19:52:33 vmi3306453 autoleft-deploy[3936471]: [19:52:33] === Deploy OK ===
Sep 02 19:52:33 vmi3306453 autoleft-deploy[3936330]: [2026-09-02 19:52:33] ✅ Deploy OK — gyvai veikia 831f4c0
```
