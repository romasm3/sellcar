# Serverio būklė

Sugeneruota: 2026-09-07 19:48:14 CEST

## Kodas

```
sukasi:      c6aa4e6 fix(nuotraukos): trynimas, pertvarkymas ir „pagrindinė" telefone; įkėlimas po vieną
origin/master: 7432700 feat(skelbimai): trinti_skelbimus --visus — pilnas skelbimų išvalymas
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
HTTP 301, 0.094823s
```

## Skelbimų būsenos

```

Listing — iš viso 24
  active        13   MATOMAS
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
/dev/sda1       291G   30G  262G  11% /
```

## Paskutinis auto-deploy

```
Sep 07 19:48:08 vmi3306453 autoleft-deploy[1347805]:     de5208b fix(skelbimai): pateikus skelbimą — „pavyko" puslapis, o sėkmė žalia
Sep 07 19:48:08 vmi3306453 autoleft-deploy[1347805]:     626d94a feat(nuotraukos): visos 28 create formos valdo nuotraukas vienodai
Sep 07 19:48:08 vmi3306453 autoleft-deploy[1347805]:     0cde182 feat(registracija): pranešimas savininkui apie naują vartotoją
Sep 07 19:48:08 vmi3306453 autoleft-deploy[1347805]:     f4511d0 refactor(nuotraukos): vienas bendras nuotraukų valdymas visoms 28 create formoms
Sep 07 19:48:09 vmi3306453 autoleft-deploy[1347783]: [2026-09-07 19:48:09] Kodas atnaujintas iki 7432700
Sep 07 19:48:14 vmi3306453 autoleft-deploy[1347949]:     
Sep 07 19:48:14 vmi3306453 autoleft-deploy[1347949]:     ----------------------------------------------------------------------
Sep 07 19:48:14 vmi3306453 autoleft-deploy[1347949]:     Ran 11 tests in 0.131s
Sep 07 19:48:14 vmi3306453 autoleft-deploy[1347949]:     
Sep 07 19:48:14 vmi3306453 autoleft-deploy[1347949]:     FAILED (errors=4)
Sep 07 19:48:14 vmi3306453 autoleft-deploy[1347949]:     Found 11 test(s).
Sep 07 19:48:14 vmi3306453 autoleft-deploy[1347949]:     System check identified no issues (0 silenced).
Sep 07 19:48:14 vmi3306453 autoleft-deploy[1347949]:     ── 3/3  Vertimai: /en/ be lietuvių kalbos, šablonai apvynioti
Sep 07 19:48:14 vmi3306453 autoleft-deploy[1347949]:       File "/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/staticfiles/storage.py", line 182, in _url
Sep 07 19:48:14 vmi3306453 autoleft-deploy[1347949]:         hashed_name = hashed_name_func(*args)
Sep 07 19:48:14 vmi3306453 autoleft-deploy[1347949]:       File "/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/staticfiles/storage.py", line 516, in stored_name
Sep 07 19:48:14 vmi3306453 autoleft-deploy[1347949]:         raise ValueError(
Sep 07 19:48:14 vmi3306453 autoleft-deploy[1347949]:     ValueError: Missing staticfiles manifest entry for 'js/valiuta.js'
Sep 07 19:48:14 vmi3306453 autoleft-deploy[1347949]:     
Sep 07 19:48:14 vmi3306453 autoleft-deploy[1347949]:     ----------------------------------------------------------------------
Sep 07 19:48:14 vmi3306453 autoleft-deploy[1347949]:     Ran 4 tests in 0.465s
Sep 07 19:48:14 vmi3306453 autoleft-deploy[1347949]:     
Sep 07 19:48:14 vmi3306453 autoleft-deploy[1347949]:     FAILED (errors=2)
Sep 07 19:48:14 vmi3306453 autoleft-deploy[1347949]:     
Sep 07 19:48:14 vmi3306453 autoleft-deploy[1347949]:     PATIKRA NEPRAĖJO — nediegti.
```
