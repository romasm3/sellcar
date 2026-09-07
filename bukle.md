# Serverio būklė

Sugeneruota: 2026-09-07 19:08:59 CEST

## Kodas

```
sukasi:      c6aa4e6 fix(nuotraukos): trynimas, pertvarkymas ir „pagrindinė" telefone; įkėlimas po vieną
origin/master: 320dfcb merge master
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
HTTP 301, 0.020250s
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
Sep 07 19:08:54 vmi3306453 autoleft-deploy[1321495]:     de5208b fix(skelbimai): pateikus skelbimą — „pavyko" puslapis, o sėkmė žalia
Sep 07 19:08:54 vmi3306453 autoleft-deploy[1321495]:     626d94a feat(nuotraukos): visos 28 create formos valdo nuotraukas vienodai
Sep 07 19:08:54 vmi3306453 autoleft-deploy[1321495]:     0cde182 feat(registracija): pranešimas savininkui apie naują vartotoją
Sep 07 19:08:54 vmi3306453 autoleft-deploy[1321495]:     f4511d0 refactor(nuotraukos): vienas bendras nuotraukų valdymas visoms 28 create formoms
Sep 07 19:08:54 vmi3306453 autoleft-deploy[1321476]: [2026-09-07 19:08:54] Kodas atnaujintas iki 320dfcb
Sep 07 19:08:59 vmi3306453 autoleft-deploy[1321616]:         return self.cursor.execute(sql, params)
Sep 07 19:08:59 vmi3306453 autoleft-deploy[1321616]:     django.db.utils.ProgrammingError: column listings_listing.contact_email does not exist
Sep 07 19:08:59 vmi3306453 autoleft-deploy[1321616]:     LINE 1: ...ddress", "listings_listing"."hide_exact_address", "listings_...
Sep 07 19:08:59 vmi3306453 autoleft-deploy[1321616]:                                                                  ^
Sep 07 19:08:59 vmi3306453 autoleft-deploy[1321616]:     
Sep 07 19:08:59 vmi3306453 autoleft-deploy[1321616]:     
Sep 07 19:08:59 vmi3306453 autoleft-deploy[1321616]:     ----------------------------------------------------------------------
Sep 07 19:08:59 vmi3306453 autoleft-deploy[1321616]:     Ran 11 tests in 0.210s
Sep 07 19:08:59 vmi3306453 autoleft-deploy[1321616]:     
Sep 07 19:08:59 vmi3306453 autoleft-deploy[1321616]:     FAILED (errors=4)
Sep 07 19:08:59 vmi3306453 autoleft-deploy[1321616]:     ── 3/3  Vertimai: /en/ be lietuvių kalbos, šablonai apvynioti
Sep 07 19:08:59 vmi3306453 autoleft-deploy[1321616]:     Found 4 test(s).
Sep 07 19:08:59 vmi3306453 autoleft-deploy[1321616]:     System check identified no issues (0 silenced).
Sep 07 19:08:59 vmi3306453 autoleft-deploy[1321616]:     ....
Sep 07 19:08:59 vmi3306453 autoleft-deploy[1321616]:     ----------------------------------------------------------------------
Sep 07 19:08:59 vmi3306453 autoleft-deploy[1321616]:     Ran 4 tests in 0.464s
Sep 07 19:08:59 vmi3306453 autoleft-deploy[1321616]:     
Sep 07 19:08:59 vmi3306453 autoleft-deploy[1321616]:     OK
Sep 07 19:08:59 vmi3306453 autoleft-deploy[1321616]:     
Sep 07 19:08:59 vmi3306453 autoleft-deploy[1321616]:     PATIKRA NEPRAĖJO — nediegti.
```
