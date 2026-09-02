# Serverio būklė

Sugeneruota: 2026-09-02 15:33:21 CEST

## Kodas

```
sukasi:      70bd6e9 fix(zinutes): nuotrauka burbule — miniatiūra; vertimas atsuktas
origin/master: 70bd6e9 fix(zinutes): nuotrauka burbule — miniatiūra; vertimas atsuktas
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
HTTP 301, 0.001502s
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
/dev/sda1       291G   49G  242G  17% /
```

## Paskutinis auto-deploy

```
Sep 02 15:31:47 vmi3306453 autoleft-deploy[3737442]: Sep 02 15:31:41 vmi3306453 autoleft-deploy[3737291]: Operations to perform:
Sep 02 15:31:47 vmi3306453 autoleft-deploy[3737442]: Sep 02 15:31:41 vmi3306453 autoleft-deploy[3737291]:   Apply all migrations: accounts, admin, analytics, auth, broadcasts, contenttypes, conversations, imones, listings, payments, sessions
Sep 02 15:31:47 vmi3306453 autoleft-deploy[3737442]: Sep 02 15:31:41 vmi3306453 autoleft-deploy[3737291]: Running migrations:
Sep 02 15:31:47 vmi3306453 autoleft-deploy[3737442]: Sep 02 15:31:41 vmi3306453 autoleft-deploy[3737291]:   No migrations to apply.
Sep 02 15:31:47 vmi3306453 autoleft-deploy[3737442]: Sep 02 15:31:42 vmi3306453 autoleft-deploy[3737315]: 1 static file copied to '/root/autoleft/staticfiles', 217 unmodified, 126 post-processed.
Sep 02 15:31:47 vmi3306453 autoleft-deploy[3737442]: Sep 02 15:31:42 vmi3306453 autoleft-deploy[3736919]: [15:31:42] Restartinam gunicorn.service
Sep 02 15:31:47 vmi3306453 autoleft-deploy[3737442]: Sep 02 15:31:44 vmi3306453 autoleft-deploy[3736919]: [15:31:44] Health OK (1/10)
Sep 02 15:31:47 vmi3306453 autoleft-deploy[3737442]: Sep 02 15:31:45 vmi3306453 autoleft-deploy[3736919]: [15:31:45] ❌ Šablonai/statiniai keitėsi, bet CSS vardas liko style.df8265b02e1b.css.
Sep 02 15:31:47 vmi3306453 autoleft-deploy[3737442]: Sep 02 15:31:45 vmi3306453 autoleft-deploy[3736919]: [15:31:45]    Naršyklės gaus seną failą — deploy stabdomas.
Sep 02 15:31:47 vmi3306453 autoleft-deploy[3737442]: Sep 02 15:31:45 vmi3306453 autoleft-deploy[3736919]: [15:31:45] ⚠️  ĮSPĖJIMAS: statinių maišas neatsinaujino, kaip tikėtasi.
Sep 02 15:31:47 vmi3306453 autoleft-deploy[3737442]: Sep 02 15:31:45 vmi3306453 autoleft-deploy[3736919]: [15:31:45] ⚠️  Kodas NEATSUKAMAS — svetainė veikia. Lankytojų naršyklės
Sep 02 15:31:47 vmi3306453 autoleft-deploy[3737442]: Sep 02 15:31:45 vmi3306453 autoleft-deploy[3736919]: [15:31:45] ⚠️  gali kurį laiką rodyti seną CSS; patikrink rankiniu būdu:
Sep 02 15:31:47 vmi3306453 autoleft-deploy[3737442]: Sep 02 15:31:45 vmi3306453 autoleft-deploy[3736919]: [15:31:45] ⚠️    curl -s https://autoleft.com/ | grep -o 'style\.[a-z0-9]*\.css'
Sep 02 15:31:47 vmi3306453 autoleft-deploy[3737442]: Sep 02 15:31:45 vmi3306453 autoleft-deploy[3736919]: [15:31:45] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Sep 02 15:31:47 vmi3306453 autoleft-deploy[3737442]: Sep 02 15:31:45 vmi3306453 autoleft-deploy[3736919]: [15:31:45] === Deploy OK ===
Sep 02 15:31:47 vmi3306453 autoleft-deploy[3737442]: Sep 02 15:31:45 vmi3306453 autoleft-deploy[3736777]: [2026-09-02 15:31:45] ✅ Deploy OK — gyvai veikia 70bd6e9
Sep 02 15:31:47 vmi3306453 autoleft-deploy[3737442]: ```
Sep 02 15:31:47 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 15:31:47 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 15:31:47 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 21.011s CPU time.
Sep 02 15:32:14 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 15:32:16 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 15:32:16 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 15:32:16 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.583s CPU time.
Sep 02 15:33:20 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
