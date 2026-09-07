# Serverio būklė

Sugeneruota: 2026-09-07 21:26:16 CEST

## Kodas

```
sukasi:      c6aa4e6 fix(nuotraukos): trynimas, pertvarkymas ir „pagrindinė" telefone; įkėlimas po vieną
origin/master: 8b30369 Merge remote-tracking branch 'origin/master' into claude/pasijunge-mes-cy48ei
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
HTTP 301, 0.190107s
```

## Skelbimų būsenos

```

Listing — iš viso 6
  active         6   MATOMAS
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
Sep 07 21:26:11 vmi3306453 autoleft-deploy[1410158]:     de5208b fix(skelbimai): pateikus skelbimą — „pavyko" puslapis, o sėkmė žalia
Sep 07 21:26:11 vmi3306453 autoleft-deploy[1410158]:     626d94a feat(nuotraukos): visos 28 create formos valdo nuotraukas vienodai
Sep 07 21:26:11 vmi3306453 autoleft-deploy[1410158]:     0cde182 feat(registracija): pranešimas savininkui apie naują vartotoją
Sep 07 21:26:11 vmi3306453 autoleft-deploy[1410158]:     f4511d0 refactor(nuotraukos): vienas bendras nuotraukų valdymas visoms 28 create formoms
Sep 07 21:26:11 vmi3306453 autoleft-deploy[1410137]: [2026-09-07 21:26:11] Kodas atnaujintas iki 8b30369
Sep 07 21:26:16 vmi3306453 autoleft-deploy[1410269]:                                                                  ^
Sep 07 21:26:16 vmi3306453 autoleft-deploy[1410269]:     
Sep 07 21:26:16 vmi3306453 autoleft-deploy[1410269]:     
Sep 07 21:26:16 vmi3306453 autoleft-deploy[1410269]:     ----------------------------------------------------------------------
Sep 07 21:26:16 vmi3306453 autoleft-deploy[1410269]:     Ran 11 tests in 0.111s
Sep 07 21:26:16 vmi3306453 autoleft-deploy[1410269]:     
Sep 07 21:26:16 vmi3306453 autoleft-deploy[1410269]:     FAILED (errors=4)
Sep 07 21:26:16 vmi3306453 autoleft-deploy[1410269]:     ── 3/3  Vertimai: /en/ be lietuvių kalbos, šablonai apvynioti
Sep 07 21:26:16 vmi3306453 autoleft-deploy[1410269]:       File "/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/staticfiles/storage.py", line 182, in _url
Sep 07 21:26:16 vmi3306453 autoleft-deploy[1410269]:         hashed_name = hashed_name_func(*args)
Sep 07 21:26:16 vmi3306453 autoleft-deploy[1410269]:       File "/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/staticfiles/storage.py", line 516, in stored_name
Sep 07 21:26:16 vmi3306453 autoleft-deploy[1410269]:         raise ValueError(
Sep 07 21:26:16 vmi3306453 autoleft-deploy[1410269]:     ValueError: Missing staticfiles manifest entry for 'js/valiuta.js'
Sep 07 21:26:16 vmi3306453 autoleft-deploy[1410269]:     
Sep 07 21:26:16 vmi3306453 autoleft-deploy[1410269]:     ----------------------------------------------------------------------
Sep 07 21:26:16 vmi3306453 autoleft-deploy[1410269]:     Ran 4 tests in 0.320s
Sep 07 21:26:16 vmi3306453 autoleft-deploy[1410269]:     
Sep 07 21:26:16 vmi3306453 autoleft-deploy[1410269]:     FAILED (errors=2)
Sep 07 21:26:16 vmi3306453 autoleft-deploy[1410269]:     
Sep 07 21:26:16 vmi3306453 autoleft-deploy[1410269]:     PATIKRA NEPRAĖJO — nediegti.
```
