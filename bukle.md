# Serverio būklė

Sugeneruota: 2026-09-02 13:22:07 CEST

## Kodas

```
sukasi:      a954c27 fix(antraste): kalbos perjungiklis nebedingsta telefonuose
origin/master: a954c27 fix(antraste): kalbos perjungiklis nebedingsta telefonuose
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
HTTP 301, 0.002910s
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
Sep 02 13:20:31 vmi3306453 autoleft-deploy[3642672]: Sep 02 13:20:23 vmi3306453 autoleft-deploy[3642499]: Operations to perform:
Sep 02 13:20:31 vmi3306453 autoleft-deploy[3642672]: Sep 02 13:20:23 vmi3306453 autoleft-deploy[3642499]:   Apply all migrations: accounts, admin, analytics, auth, broadcasts, contenttypes, conversations, imones, listings, payments, sessions
Sep 02 13:20:31 vmi3306453 autoleft-deploy[3642672]: Sep 02 13:20:23 vmi3306453 autoleft-deploy[3642499]: Running migrations:
Sep 02 13:20:31 vmi3306453 autoleft-deploy[3642672]: Sep 02 13:20:23 vmi3306453 autoleft-deploy[3642499]:   No migrations to apply.
Sep 02 13:20:31 vmi3306453 autoleft-deploy[3642672]: Sep 02 13:20:25 vmi3306453 autoleft-deploy[3642530]: 0 static files copied to '/root/autoleft/staticfiles', 217 unmodified, 125 post-processed.
Sep 02 13:20:31 vmi3306453 autoleft-deploy[3642672]: Sep 02 13:20:25 vmi3306453 autoleft-deploy[3642029]: [13:20:25] Restartinam gunicorn.service
Sep 02 13:20:31 vmi3306453 autoleft-deploy[3642672]: Sep 02 13:20:27 vmi3306453 autoleft-deploy[3642029]: [13:20:27] Health OK (1/10)
Sep 02 13:20:31 vmi3306453 autoleft-deploy[3642672]: Sep 02 13:20:28 vmi3306453 autoleft-deploy[3642029]: [13:20:28] ❌ Šablonai/statiniai keitėsi, bet CSS vardas liko style.df8265b02e1b.css.
Sep 02 13:20:31 vmi3306453 autoleft-deploy[3642672]: Sep 02 13:20:28 vmi3306453 autoleft-deploy[3642029]: [13:20:28]    Naršyklės gaus seną failą — deploy stabdomas.
Sep 02 13:20:31 vmi3306453 autoleft-deploy[3642672]: Sep 02 13:20:28 vmi3306453 autoleft-deploy[3642029]: [13:20:28] ⚠️  ĮSPĖJIMAS: statinių maišas neatsinaujino, kaip tikėtasi.
Sep 02 13:20:31 vmi3306453 autoleft-deploy[3642672]: Sep 02 13:20:28 vmi3306453 autoleft-deploy[3642029]: [13:20:28] ⚠️  Kodas NEATSUKAMAS — svetainė veikia. Lankytojų naršyklės
Sep 02 13:20:31 vmi3306453 autoleft-deploy[3642672]: Sep 02 13:20:28 vmi3306453 autoleft-deploy[3642029]: [13:20:28] ⚠️  gali kurį laiką rodyti seną CSS; patikrink rankiniu būdu:
Sep 02 13:20:31 vmi3306453 autoleft-deploy[3642672]: Sep 02 13:20:28 vmi3306453 autoleft-deploy[3642029]: [13:20:28] ⚠️    curl -s https://autoleft.com/ | grep -o 'style\.[a-z0-9]*\.css'
Sep 02 13:20:31 vmi3306453 autoleft-deploy[3642672]: Sep 02 13:20:28 vmi3306453 autoleft-deploy[3642029]: [13:20:28] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Sep 02 13:20:31 vmi3306453 autoleft-deploy[3642672]: Sep 02 13:20:28 vmi3306453 autoleft-deploy[3642029]: [13:20:28] === Deploy OK ===
Sep 02 13:20:31 vmi3306453 autoleft-deploy[3642672]: Sep 02 13:20:28 vmi3306453 autoleft-deploy[3641902]: [2026-09-02 13:20:28] ✅ Deploy OK — gyvai veikia a954c27
Sep 02 13:20:31 vmi3306453 autoleft-deploy[3642672]: ```
Sep 02 13:20:31 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 13:20:31 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 13:20:31 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 24.552s CPU time.
Sep 02 13:20:56 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 13:20:59 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 13:20:59 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 13:20:59 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.572s CPU time.
Sep 02 13:22:07 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
