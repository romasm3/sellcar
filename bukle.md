# Serverio būklė

Sugeneruota: 2026-09-02 11:25:11 CEST

## Kodas

```
sukasi:      45f0c22 fix(sarasai): tekstas kairėje ir grąžintos „Varantieji ratai" reikšmės
origin/master: 45f0c22 fix(sarasai): tekstas kairėje ir grąžintos „Varantieji ratai" reikšmės
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
HTTP 301, 0.001871s
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
/dev/sda1       291G   48G  244G  17% /
```

## Paskutinis auto-deploy

```
Sep 02 11:23:33 vmi3306453 autoleft-deploy[3557763]: Sep 02 11:23:26 vmi3306453 autoleft-deploy[3557591]: Operations to perform:
Sep 02 11:23:33 vmi3306453 autoleft-deploy[3557763]: Sep 02 11:23:26 vmi3306453 autoleft-deploy[3557591]:   Apply all migrations: accounts, admin, analytics, auth, broadcasts, contenttypes, conversations, imones, listings, payments, sessions
Sep 02 11:23:33 vmi3306453 autoleft-deploy[3557763]: Sep 02 11:23:26 vmi3306453 autoleft-deploy[3557591]: Running migrations:
Sep 02 11:23:33 vmi3306453 autoleft-deploy[3557763]: Sep 02 11:23:26 vmi3306453 autoleft-deploy[3557591]:   No migrations to apply.
Sep 02 11:23:33 vmi3306453 autoleft-deploy[3557763]: Sep 02 11:23:28 vmi3306453 autoleft-deploy[3557620]: 1 static file copied to '/root/autoleft/staticfiles', 216 unmodified, 125 post-processed.
Sep 02 11:23:33 vmi3306453 autoleft-deploy[3557763]: Sep 02 11:23:28 vmi3306453 autoleft-deploy[3557103]: [11:23:28] Restartinam gunicorn.service
Sep 02 11:23:33 vmi3306453 autoleft-deploy[3557763]: Sep 02 11:23:30 vmi3306453 autoleft-deploy[3557103]: [11:23:30] Health OK (1/10)
Sep 02 11:23:33 vmi3306453 autoleft-deploy[3557763]: Sep 02 11:23:31 vmi3306453 autoleft-deploy[3557103]: [11:23:31] ❌ Šablonai/statiniai keitėsi, bet CSS vardas liko style.df8265b02e1b.css.
Sep 02 11:23:33 vmi3306453 autoleft-deploy[3557763]: Sep 02 11:23:31 vmi3306453 autoleft-deploy[3557103]: [11:23:31]    Naršyklės gaus seną failą — deploy stabdomas.
Sep 02 11:23:33 vmi3306453 autoleft-deploy[3557763]: Sep 02 11:23:31 vmi3306453 autoleft-deploy[3557103]: [11:23:31] ⚠️  ĮSPĖJIMAS: statinių maišas neatsinaujino, kaip tikėtasi.
Sep 02 11:23:33 vmi3306453 autoleft-deploy[3557763]: Sep 02 11:23:31 vmi3306453 autoleft-deploy[3557103]: [11:23:31] ⚠️  Kodas NEATSUKAMAS — svetainė veikia. Lankytojų naršyklės
Sep 02 11:23:33 vmi3306453 autoleft-deploy[3557763]: Sep 02 11:23:31 vmi3306453 autoleft-deploy[3557103]: [11:23:31] ⚠️  gali kurį laiką rodyti seną CSS; patikrink rankiniu būdu:
Sep 02 11:23:33 vmi3306453 autoleft-deploy[3557763]: Sep 02 11:23:31 vmi3306453 autoleft-deploy[3557103]: [11:23:31] ⚠️    curl -s https://autoleft.com/ | grep -o 'style\.[a-z0-9]*\.css'
Sep 02 11:23:33 vmi3306453 autoleft-deploy[3557763]: Sep 02 11:23:31 vmi3306453 autoleft-deploy[3557103]: [11:23:31] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Sep 02 11:23:33 vmi3306453 autoleft-deploy[3557763]: Sep 02 11:23:31 vmi3306453 autoleft-deploy[3557103]: [11:23:31] === Deploy OK ===
Sep 02 11:23:33 vmi3306453 autoleft-deploy[3557763]: Sep 02 11:23:31 vmi3306453 autoleft-deploy[3556974]: [2026-09-02 11:23:31] ✅ Deploy OK — gyvai veikia 45f0c22
Sep 02 11:23:33 vmi3306453 autoleft-deploy[3557763]: ```
Sep 02 11:23:33 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 11:23:33 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 11:23:33 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 26.381s CPU time.
Sep 02 11:23:33 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 11:23:36 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 11:23:36 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 11:23:36 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.576s CPU time.
Sep 02 11:25:11 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
