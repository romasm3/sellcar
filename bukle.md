# Serverio būklė

Sugeneruota: 2026-09-08 08:41:22 CEST

## Kodas

```
sukasi:      c6aa4e6 fix(nuotraukos): trynimas, pertvarkymas ir „pagrindinė" telefone; įkėlimas po vieną
origin/master: 9debc7b style(listing): kainos vieta ir dydis šoninėje juostoje
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
HTTP 301, 0.002270s
```

## Skelbimų būsenos

```

Listing — iš viso 10
  active        10   MATOMAS
  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─
  nematomi dėl būsenos:      0
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
Sep 08 08:41:19 vmi3306453 autoleft-deploy[1820886]:     de5208b fix(skelbimai): pateikus skelbimą — „pavyko" puslapis, o sėkmė žalia
Sep 08 08:41:19 vmi3306453 autoleft-deploy[1820886]:     626d94a feat(nuotraukos): visos 28 create formos valdo nuotraukas vienodai
Sep 08 08:41:19 vmi3306453 autoleft-deploy[1820886]:     0cde182 feat(registracija): pranešimas savininkui apie naują vartotoją
Sep 08 08:41:19 vmi3306453 autoleft-deploy[1820886]:     f4511d0 refactor(nuotraukos): vienas bendras nuotraukų valdymas visoms 28 create formoms
Sep 08 08:41:19 vmi3306453 autoleft-deploy[1820867]: [2026-09-08 08:41:19] Kodas atnaujintas iki 9debc7b
Sep 08 08:41:22 vmi3306453 autoleft-deploy[1820987]:                                                                  ^
Sep 08 08:41:22 vmi3306453 autoleft-deploy[1820987]:     
Sep 08 08:41:22 vmi3306453 autoleft-deploy[1820987]:     
Sep 08 08:41:22 vmi3306453 autoleft-deploy[1820987]:     ----------------------------------------------------------------------
Sep 08 08:41:22 vmi3306453 autoleft-deploy[1820987]:     Ran 11 tests in 0.101s
Sep 08 08:41:22 vmi3306453 autoleft-deploy[1820987]:     
Sep 08 08:41:22 vmi3306453 autoleft-deploy[1820987]:     FAILED (errors=4)
Sep 08 08:41:22 vmi3306453 autoleft-deploy[1820987]:     ── 3/3  Vertimai: /en/ be lietuvių kalbos, šablonai apvynioti
Sep 08 08:41:22 vmi3306453 autoleft-deploy[1820987]:       File "/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/staticfiles/storage.py", line 182, in _url
Sep 08 08:41:22 vmi3306453 autoleft-deploy[1820987]:         hashed_name = hashed_name_func(*args)
Sep 08 08:41:22 vmi3306453 autoleft-deploy[1820987]:       File "/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/staticfiles/storage.py", line 516, in stored_name
Sep 08 08:41:22 vmi3306453 autoleft-deploy[1820987]:         raise ValueError(
Sep 08 08:41:22 vmi3306453 autoleft-deploy[1820987]:     ValueError: Missing staticfiles manifest entry for 'js/valiuta.js'
Sep 08 08:41:22 vmi3306453 autoleft-deploy[1820987]:     
Sep 08 08:41:22 vmi3306453 autoleft-deploy[1820987]:     ----------------------------------------------------------------------
Sep 08 08:41:22 vmi3306453 autoleft-deploy[1820987]:     Ran 4 tests in 0.276s
Sep 08 08:41:22 vmi3306453 autoleft-deploy[1820987]:     
Sep 08 08:41:22 vmi3306453 autoleft-deploy[1820987]:     FAILED (errors=2)
Sep 08 08:41:22 vmi3306453 autoleft-deploy[1820987]:     
Sep 08 08:41:22 vmi3306453 autoleft-deploy[1820987]:     PATIKRA NEPRAĖJO — nediegti.
```
