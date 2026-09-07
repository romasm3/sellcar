# Serverio būklė

Sugeneruota: 2026-09-07 15:10:38 CEST

## Kodas

```
sukasi:      c6aa4e6 fix(nuotraukos): trynimas, pertvarkymas ir „pagrindinė" telefone; įkėlimas po vieną
origin/master: de5208b fix(skelbimai): pateikus skelbimą — „pavyko" puslapis, o sėkmė žalia
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
HTTP 301, 0.004849s
```

## Skelbimų būsenos

```

Listing — iš viso 37
  active        18   MATOMAS
  expired       10   nematomas
  draft          9   nematomas
  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─
  nematomi dėl būsenos:      19
  iš jų pasibaigę (expires_at praeityje): 10
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
/dev/sda1       291G   29G  262G  10% /
```

## Paskutinis auto-deploy

```
Sep 07 15:10:27 vmi3306453 autoleft-deploy[1184133]:     de5208b fix(skelbimai): pateikus skelbimą — „pavyko" puslapis, o sėkmė žalia
Sep 07 15:10:27 vmi3306453 autoleft-deploy[1184133]:     626d94a feat(nuotraukos): visos 28 create formos valdo nuotraukas vienodai
Sep 07 15:10:27 vmi3306453 autoleft-deploy[1184133]:     0cde182 feat(registracija): pranešimas savininkui apie naują vartotoją
Sep 07 15:10:27 vmi3306453 autoleft-deploy[1184133]:     f4511d0 refactor(nuotraukos): vienas bendras nuotraukų valdymas visoms 28 create formoms
Sep 07 15:10:27 vmi3306453 autoleft-deploy[1184115]: [2026-09-07 15:10:27] Kodas atnaujintas iki de5208b
Sep 07 15:10:38 vmi3306453 autoleft-deploy[1184282]:       File "/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/staticfiles/storage.py", line 182, in _url
Sep 07 15:10:38 vmi3306453 autoleft-deploy[1184282]:         hashed_name = hashed_name_func(*args)
Sep 07 15:10:38 vmi3306453 autoleft-deploy[1184282]:       File "/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/staticfiles/storage.py", line 516, in stored_name
Sep 07 15:10:38 vmi3306453 autoleft-deploy[1184282]:         raise ValueError(
Sep 07 15:10:38 vmi3306453 autoleft-deploy[1184282]:     ValueError: Missing staticfiles manifest entry for 'js/nuotrauku_valdymas.js'
Sep 07 15:10:38 vmi3306453 autoleft-deploy[1184282]:     
Sep 07 15:10:38 vmi3306453 autoleft-deploy[1184282]:     ----------------------------------------------------------------------
Sep 07 15:10:38 vmi3306453 autoleft-deploy[1184282]:     Ran 11 tests in 7.325s
Sep 07 15:10:38 vmi3306453 autoleft-deploy[1184282]:     
Sep 07 15:10:38 vmi3306453 autoleft-deploy[1184282]:     FAILED (errors=1)
Sep 07 15:10:38 vmi3306453 autoleft-deploy[1184282]:     ── 3/3  Vertimai: /en/ be lietuvių kalbos, šablonai apvynioti
Sep 07 15:10:38 vmi3306453 autoleft-deploy[1184282]:     Found 4 test(s).
Sep 07 15:10:38 vmi3306453 autoleft-deploy[1184282]:     System check identified no issues (0 silenced).
Sep 07 15:10:38 vmi3306453 autoleft-deploy[1184282]:     ....
Sep 07 15:10:38 vmi3306453 autoleft-deploy[1184282]:     ----------------------------------------------------------------------
Sep 07 15:10:38 vmi3306453 autoleft-deploy[1184282]:     Ran 4 tests in 0.435s
Sep 07 15:10:38 vmi3306453 autoleft-deploy[1184282]:     
Sep 07 15:10:38 vmi3306453 autoleft-deploy[1184282]:     OK
Sep 07 15:10:38 vmi3306453 autoleft-deploy[1184282]:     
Sep 07 15:10:38 vmi3306453 autoleft-deploy[1184282]:     PATIKRA NEPRAĖJO — nediegti.
```
