# Serverio būklė

Sugeneruota: 2026-09-07 19:13:34 CEST

## Kodas

```
sukasi:      c6aa4e6 fix(nuotraukos): trynimas, pertvarkymas ir „pagrindinė" telefone; įkėlimas po vieną
origin/master: 4fed112 merge master
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
HTTP 301, 0.009610s
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
Sep 07 19:13:29 vmi3306453 autoleft-deploy[1324724]:     de5208b fix(skelbimai): pateikus skelbimą — „pavyko" puslapis, o sėkmė žalia
Sep 07 19:13:29 vmi3306453 autoleft-deploy[1324724]:     626d94a feat(nuotraukos): visos 28 create formos valdo nuotraukas vienodai
Sep 07 19:13:29 vmi3306453 autoleft-deploy[1324724]:     0cde182 feat(registracija): pranešimas savininkui apie naują vartotoją
Sep 07 19:13:29 vmi3306453 autoleft-deploy[1324724]:     f4511d0 refactor(nuotraukos): vienas bendras nuotraukų valdymas visoms 28 create formoms
Sep 07 19:13:29 vmi3306453 autoleft-deploy[1324699]: [2026-09-07 19:13:29] Kodas atnaujintas iki 4fed112
Sep 07 19:13:34 vmi3306453 autoleft-deploy[1324836]:                                                                  ^
Sep 07 19:13:34 vmi3306453 autoleft-deploy[1324836]:     
Sep 07 19:13:34 vmi3306453 autoleft-deploy[1324836]:     
Sep 07 19:13:34 vmi3306453 autoleft-deploy[1324836]:     ----------------------------------------------------------------------
Sep 07 19:13:34 vmi3306453 autoleft-deploy[1324836]:     Ran 11 tests in 0.159s
Sep 07 19:13:34 vmi3306453 autoleft-deploy[1324836]:     
Sep 07 19:13:34 vmi3306453 autoleft-deploy[1324836]:     FAILED (errors=4)
Sep 07 19:13:34 vmi3306453 autoleft-deploy[1324836]:     ── 3/3  Vertimai: /en/ be lietuvių kalbos, šablonai apvynioti
Sep 07 19:13:34 vmi3306453 autoleft-deploy[1324836]:       File "/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/staticfiles/storage.py", line 182, in _url
Sep 07 19:13:34 vmi3306453 autoleft-deploy[1324836]:         hashed_name = hashed_name_func(*args)
Sep 07 19:13:34 vmi3306453 autoleft-deploy[1324836]:       File "/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/staticfiles/storage.py", line 516, in stored_name
Sep 07 19:13:34 vmi3306453 autoleft-deploy[1324836]:         raise ValueError(
Sep 07 19:13:34 vmi3306453 autoleft-deploy[1324836]:     ValueError: Missing staticfiles manifest entry for 'js/valiuta.js'
Sep 07 19:13:34 vmi3306453 autoleft-deploy[1324836]:     
Sep 07 19:13:34 vmi3306453 autoleft-deploy[1324836]:     ----------------------------------------------------------------------
Sep 07 19:13:34 vmi3306453 autoleft-deploy[1324836]:     Ran 4 tests in 0.317s
Sep 07 19:13:34 vmi3306453 autoleft-deploy[1324836]:     
Sep 07 19:13:34 vmi3306453 autoleft-deploy[1324836]:     FAILED (errors=2)
Sep 07 19:13:34 vmi3306453 autoleft-deploy[1324836]:     
Sep 07 19:13:34 vmi3306453 autoleft-deploy[1324836]:     PATIKRA NEPRAĖJO — nediegti.
```
