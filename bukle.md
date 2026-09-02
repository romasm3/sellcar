# Serverio būklė

Sugeneruota: 2026-09-02 15:15:58 CEST

## Kodas

```
sukasi:      341ea4d feat(zinutes): vardai vietoj el. pašto ir gyvos žinutės be perkrovimo
origin/master: 341ea4d feat(zinutes): vardai vietoj el. pašto ir gyvos žinutės be perkrovimo
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
HTTP 301, 0.001343s
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
Sep 02 15:15:16 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 15:15:16 vmi3306453 autoleft-deploy[3725473]: [2026-09-02 15:15:16] === Naujų commit'ų rasta: a42e0c6 → 341ea4d ===
Sep 02 15:15:16 vmi3306453 autoleft-deploy[3725493]:     341ea4d feat(zinutes): vardai vietoj el. pašto ir gyvos žinutės be perkrovimo
Sep 02 15:15:16 vmi3306453 autoleft-deploy[3725473]: [2026-09-02 15:15:16] Kodas atnaujintas iki 341ea4d
Sep 02 15:15:25 vmi3306453 autoleft-deploy[3725473]: [2026-09-02 15:15:25] Patikra praėjo
Sep 02 15:15:25 vmi3306453 autoleft-deploy[3725607]: [15:15:25] === Deploy pradžia (20260902_151525) ===
Sep 02 15:15:25 vmi3306453 autoleft-deploy[3725607]: [15:15:25] Šablonai/statiniai keitėsi — tikrinsim CSS vardą.
Sep 02 15:15:53 vmi3306453 autoleft-deploy[3725607]: [15:15:53] DB dumpas: /root/autoleft_backups/db_20260902_151525.sql
Sep 02 15:15:54 vmi3306453 autoleft-deploy[3725607]: [15:15:54] Versija: 341ea4d99238
Sep 02 15:15:55 vmi3306453 autoleft-deploy[3725941]: Operations to perform:
Sep 02 15:15:55 vmi3306453 autoleft-deploy[3725941]:   Apply all migrations: accounts, admin, analytics, auth, broadcasts, contenttypes, conversations, imones, listings, payments, sessions
Sep 02 15:15:55 vmi3306453 autoleft-deploy[3725941]: Running migrations:
Sep 02 15:15:55 vmi3306453 autoleft-deploy[3725941]:   No migrations to apply.
Sep 02 15:15:56 vmi3306453 autoleft-deploy[3725962]: 1 static file copied to '/root/autoleft/staticfiles', 217 unmodified, 126 post-processed.
Sep 02 15:15:56 vmi3306453 autoleft-deploy[3725607]: [15:15:56] Restartinam gunicorn.service
Sep 02 15:15:58 vmi3306453 autoleft-deploy[3725607]: [15:15:58] Health OK (1/10)
Sep 02 15:15:58 vmi3306453 autoleft-deploy[3725607]: [15:15:58] ❌ Šablonai/statiniai keitėsi, bet CSS vardas liko style.df8265b02e1b.css.
Sep 02 15:15:58 vmi3306453 autoleft-deploy[3725607]: [15:15:58]    Naršyklės gaus seną failą — deploy stabdomas.
Sep 02 15:15:58 vmi3306453 autoleft-deploy[3725607]: [15:15:58] ⚠️  ĮSPĖJIMAS: statinių maišas neatsinaujino, kaip tikėtasi.
Sep 02 15:15:58 vmi3306453 autoleft-deploy[3725607]: [15:15:58] ⚠️  Kodas NEATSUKAMAS — svetainė veikia. Lankytojų naršyklės
Sep 02 15:15:58 vmi3306453 autoleft-deploy[3725607]: [15:15:58] ⚠️  gali kurį laiką rodyti seną CSS; patikrink rankiniu būdu:
Sep 02 15:15:58 vmi3306453 autoleft-deploy[3725607]: [15:15:58] ⚠️    curl -s https://autoleft.com/ | grep -o 'style\.[a-z0-9]*\.css'
Sep 02 15:15:58 vmi3306453 autoleft-deploy[3725607]: [15:15:58] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Sep 02 15:15:58 vmi3306453 autoleft-deploy[3725607]: [15:15:58] === Deploy OK ===
Sep 02 15:15:58 vmi3306453 autoleft-deploy[3725473]: [2026-09-02 15:15:58] ✅ Deploy OK — gyvai veikia 341ea4d
```
