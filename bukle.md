# Serverio būklė

Sugeneruota: 2026-09-02 15:58:51 CEST

## Kodas

```
sukasi:      f1886fe feat(zinutes): vertimas tapo jungikliu su išsaugoma būsena
origin/master: f1886fe feat(zinutes): vertimas tapo jungikliu su išsaugoma būsena
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
HTTP 301, 0.001224s
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
/dev/sda1       291G   50G  242G  17% /
```

## Paskutinis auto-deploy

```
Sep 02 15:58:12 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 15:58:13 vmi3306453 autoleft-deploy[3757358]: [2026-09-02 15:58:13] === Naujų commit'ų rasta: e885047 → f1886fe ===
Sep 02 15:58:13 vmi3306453 autoleft-deploy[3757376]:     f1886fe feat(zinutes): vertimas tapo jungikliu su išsaugoma būsena
Sep 02 15:58:13 vmi3306453 autoleft-deploy[3757358]: [2026-09-02 15:58:13] Kodas atnaujintas iki f1886fe
Sep 02 15:58:21 vmi3306453 autoleft-deploy[3757358]: [2026-09-02 15:58:21] Patikra praėjo
Sep 02 15:58:21 vmi3306453 autoleft-deploy[3757488]: [15:58:21] === Deploy pradžia (20260902_155821) ===
Sep 02 15:58:21 vmi3306453 autoleft-deploy[3757488]: [15:58:21] Šablonai/statiniai keitėsi — tikrinsim CSS vardą.
Sep 02 15:58:47 vmi3306453 autoleft-deploy[3757488]: [15:58:47] DB dumpas: /root/autoleft_backups/db_20260902_155821.sql
Sep 02 15:58:47 vmi3306453 autoleft-deploy[3757488]: [15:58:47] Versija: f1886fee35dd
Sep 02 15:58:48 vmi3306453 autoleft-deploy[3757834]: Operations to perform:
Sep 02 15:58:48 vmi3306453 autoleft-deploy[3757834]:   Apply all migrations: accounts, admin, analytics, auth, broadcasts, contenttypes, conversations, imones, listings, payments, sessions
Sep 02 15:58:48 vmi3306453 autoleft-deploy[3757834]: Running migrations:
Sep 02 15:58:48 vmi3306453 autoleft-deploy[3757834]:   Applying conversations.0004_conversationtranslation... OK
Sep 02 15:58:49 vmi3306453 autoleft-deploy[3757848]: 1 static file copied to '/root/autoleft/staticfiles', 217 unmodified, 126 post-processed.
Sep 02 15:58:49 vmi3306453 autoleft-deploy[3757488]: [15:58:49] Restartinam gunicorn.service
Sep 02 15:58:50 vmi3306453 autoleft-deploy[3757488]: [15:58:50] Health OK (1/10)
Sep 02 15:58:51 vmi3306453 autoleft-deploy[3757488]: [15:58:51] ❌ Šablonai/statiniai keitėsi, bet CSS vardas liko style.df8265b02e1b.css.
Sep 02 15:58:51 vmi3306453 autoleft-deploy[3757488]: [15:58:51]    Naršyklės gaus seną failą — deploy stabdomas.
Sep 02 15:58:51 vmi3306453 autoleft-deploy[3757488]: [15:58:51] ⚠️  ĮSPĖJIMAS: statinių maišas neatsinaujino, kaip tikėtasi.
Sep 02 15:58:51 vmi3306453 autoleft-deploy[3757488]: [15:58:51] ⚠️  Kodas NEATSUKAMAS — svetainė veikia. Lankytojų naršyklės
Sep 02 15:58:51 vmi3306453 autoleft-deploy[3757488]: [15:58:51] ⚠️  gali kurį laiką rodyti seną CSS; patikrink rankiniu būdu:
Sep 02 15:58:51 vmi3306453 autoleft-deploy[3757488]: [15:58:51] ⚠️    curl -s https://autoleft.com/ | grep -o 'style\.[a-z0-9]*\.css'
Sep 02 15:58:51 vmi3306453 autoleft-deploy[3757488]: [15:58:51] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Sep 02 15:58:51 vmi3306453 autoleft-deploy[3757488]: [15:58:51] === Deploy OK ===
Sep 02 15:58:51 vmi3306453 autoleft-deploy[3757358]: [2026-09-02 15:58:51] ✅ Deploy OK — gyvai veikia f1886fe
```
