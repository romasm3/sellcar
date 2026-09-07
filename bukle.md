# Serverio būklė

Sugeneruota: 2026-09-07 19:14:37 CEST

## Kodas

```
sukasi:      c6aa4e6 fix(nuotraukos): trynimas, pertvarkymas ir „pagrindinė" telefone; įkėlimas po vieną
origin/master: 99852f8 docs(deploy): rankiniai darbai po pataisų — #754 nuotraukos, pakibę juodraščiai
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
HTTP 301, 0.001293s
```

## Skelbimų būsenos

```

Listing — iš viso 22
  active        11   MATOMAS
  draft         11   nematomas
  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─
  nematomi dėl būsenos:      11
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
Sep 07 19:14:32 vmi3306453 autoleft-deploy[1325621]:     de5208b fix(skelbimai): pateikus skelbimą — „pavyko" puslapis, o sėkmė žalia
Sep 07 19:14:32 vmi3306453 autoleft-deploy[1325621]:     626d94a feat(nuotraukos): visos 28 create formos valdo nuotraukas vienodai
Sep 07 19:14:32 vmi3306453 autoleft-deploy[1325621]:     0cde182 feat(registracija): pranešimas savininkui apie naują vartotoją
Sep 07 19:14:32 vmi3306453 autoleft-deploy[1325621]:     f4511d0 refactor(nuotraukos): vienas bendras nuotraukų valdymas visoms 28 create formoms
Sep 07 19:14:32 vmi3306453 autoleft-deploy[1325601]: [2026-09-07 19:14:32] Kodas atnaujintas iki 99852f8
Sep 07 19:14:36 vmi3306453 autoleft-deploy[1325737]:     
Sep 07 19:14:36 vmi3306453 autoleft-deploy[1325737]:     ----------------------------------------------------------------------
Sep 07 19:14:36 vmi3306453 autoleft-deploy[1325737]:     Ran 11 tests in 0.201s
Sep 07 19:14:36 vmi3306453 autoleft-deploy[1325737]:     
Sep 07 19:14:36 vmi3306453 autoleft-deploy[1325737]:     FAILED (errors=4)
Sep 07 19:14:36 vmi3306453 autoleft-deploy[1325737]:     Found 11 test(s).
Sep 07 19:14:36 vmi3306453 autoleft-deploy[1325737]:     System check identified no issues (0 silenced).
Sep 07 19:14:36 vmi3306453 autoleft-deploy[1325737]:     ── 3/3  Vertimai: /en/ be lietuvių kalbos, šablonai apvynioti
Sep 07 19:14:36 vmi3306453 autoleft-deploy[1325737]:       File "/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/staticfiles/storage.py", line 182, in _url
Sep 07 19:14:36 vmi3306453 autoleft-deploy[1325737]:         hashed_name = hashed_name_func(*args)
Sep 07 19:14:36 vmi3306453 autoleft-deploy[1325737]:       File "/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/staticfiles/storage.py", line 516, in stored_name
Sep 07 19:14:36 vmi3306453 autoleft-deploy[1325737]:         raise ValueError(
Sep 07 19:14:36 vmi3306453 autoleft-deploy[1325737]:     ValueError: Missing staticfiles manifest entry for 'js/valiuta.js'
Sep 07 19:14:36 vmi3306453 autoleft-deploy[1325737]:     
Sep 07 19:14:36 vmi3306453 autoleft-deploy[1325737]:     ----------------------------------------------------------------------
Sep 07 19:14:36 vmi3306453 autoleft-deploy[1325737]:     Ran 4 tests in 0.323s
Sep 07 19:14:36 vmi3306453 autoleft-deploy[1325737]:     
Sep 07 19:14:36 vmi3306453 autoleft-deploy[1325737]:     FAILED (errors=2)
Sep 07 19:14:36 vmi3306453 autoleft-deploy[1325737]:     
Sep 07 19:14:36 vmi3306453 autoleft-deploy[1325737]:     PATIKRA NEPRAĖJO — nediegti.
```
