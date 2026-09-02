# Serverio būklė

Sugeneruota: 2026-09-02 09:47:07 CEST

## Kodas

```
sukasi:      2daac2c fix(juosta): atidaryti sąrašai nebeišlipa ir nebekerpa teksto
origin/master: 2daac2c fix(juosta): atidaryti sąrašai nebeišlipa ir nebekerpa teksto
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
HTTP 301, 0.002432s
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
/dev/sda1       291G   47G  245G  16% /
```

## Paskutinis auto-deploy

```
Sep 02 09:45:59 vmi3306453 autoleft-deploy[3487687]: Sep 02 09:45:51 vmi3306453 autoleft-deploy[3487459]: Operations to perform:
Sep 02 09:45:59 vmi3306453 autoleft-deploy[3487687]: Sep 02 09:45:51 vmi3306453 autoleft-deploy[3487459]:   Apply all migrations: accounts, admin, analytics, auth, broadcasts, contenttypes, conversations, imones, listings, payments, sessions
Sep 02 09:45:59 vmi3306453 autoleft-deploy[3487687]: Sep 02 09:45:51 vmi3306453 autoleft-deploy[3487459]: Running migrations:
Sep 02 09:45:59 vmi3306453 autoleft-deploy[3487687]: Sep 02 09:45:51 vmi3306453 autoleft-deploy[3487459]:   No migrations to apply.
Sep 02 09:45:59 vmi3306453 autoleft-deploy[3487687]: Sep 02 09:45:52 vmi3306453 autoleft-deploy[3487503]: 1 static file copied to '/root/autoleft/staticfiles', 216 unmodified, 125 post-processed.
Sep 02 09:45:59 vmi3306453 autoleft-deploy[3487687]: Sep 02 09:45:53 vmi3306453 autoleft-deploy[3486815]: [09:45:53] Restartinam gunicorn.service
Sep 02 09:45:59 vmi3306453 autoleft-deploy[3487687]: Sep 02 09:45:54 vmi3306453 autoleft-deploy[3486815]: [09:45:54] Health OK (1/10)
Sep 02 09:45:59 vmi3306453 autoleft-deploy[3487687]: Sep 02 09:45:55 vmi3306453 autoleft-deploy[3486815]: [09:45:55] ❌ Šablonai/statiniai keitėsi, bet CSS vardas liko style.df8265b02e1b.css.
Sep 02 09:45:59 vmi3306453 autoleft-deploy[3487687]: Sep 02 09:45:55 vmi3306453 autoleft-deploy[3486815]: [09:45:55]    Naršyklės gaus seną failą — deploy stabdomas.
Sep 02 09:45:59 vmi3306453 autoleft-deploy[3487687]: Sep 02 09:45:55 vmi3306453 autoleft-deploy[3486815]: [09:45:55] ⚠️  ĮSPĖJIMAS: statinių maišas neatsinaujino, kaip tikėtasi.
Sep 02 09:45:59 vmi3306453 autoleft-deploy[3487687]: Sep 02 09:45:55 vmi3306453 autoleft-deploy[3486815]: [09:45:55] ⚠️  Kodas NEATSUKAMAS — svetainė veikia. Lankytojų naršyklės
Sep 02 09:45:59 vmi3306453 autoleft-deploy[3487687]: Sep 02 09:45:55 vmi3306453 autoleft-deploy[3486815]: [09:45:55] ⚠️  gali kurį laiką rodyti seną CSS; patikrink rankiniu būdu:
Sep 02 09:45:59 vmi3306453 autoleft-deploy[3487687]: Sep 02 09:45:55 vmi3306453 autoleft-deploy[3486815]: [09:45:55] ⚠️    curl -s https://autoleft.com/ | grep -o 'style\.[a-z0-9]*\.css'
Sep 02 09:45:59 vmi3306453 autoleft-deploy[3487687]: Sep 02 09:45:55 vmi3306453 autoleft-deploy[3486815]: [09:45:55] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Sep 02 09:45:59 vmi3306453 autoleft-deploy[3487687]: Sep 02 09:45:55 vmi3306453 autoleft-deploy[3486815]: [09:45:55] === Deploy OK ===
Sep 02 09:45:59 vmi3306453 autoleft-deploy[3487687]: Sep 02 09:45:55 vmi3306453 autoleft-deploy[3486617]: [2026-09-02 09:45:55] ✅ Deploy OK — gyvai veikia 2daac2c
Sep 02 09:45:59 vmi3306453 autoleft-deploy[3487687]: ```
Sep 02 09:45:59 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 09:45:59 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 09:45:59 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 27.370s CPU time.
Sep 02 09:45:59 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 09:46:01 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 09:46:01 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 09:46:01 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.781s CPU time.
Sep 02 09:47:06 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
