# Serverio būklė

Sugeneruota: 2026-09-08 09:05:41 CEST

## Kodas

```
sukasi:      c6aa4e6 fix(nuotraukos): trynimas, pertvarkymas ir „pagrindinė" telefone; įkėlimas po vieną
origin/master: ae14238 fix(deploy): statinių saugyklos perjungimas nebepasikliauja Django signalu
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
HTTP 301, 0.001323s
```

## Skelbimų būsenos

```

Listing — iš viso 12
  active        10   MATOMAS
  draft          2   nematomas
  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─
  nematomi dėl būsenos:      2
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
Sep 08 09:05:37 vmi3306453 autoleft-deploy[1836311]:     de5208b fix(skelbimai): pateikus skelbimą — „pavyko" puslapis, o sėkmė žalia
Sep 08 09:05:37 vmi3306453 autoleft-deploy[1836311]:     626d94a feat(nuotraukos): visos 28 create formos valdo nuotraukas vienodai
Sep 08 09:05:37 vmi3306453 autoleft-deploy[1836311]:     0cde182 feat(registracija): pranešimas savininkui apie naują vartotoją
Sep 08 09:05:37 vmi3306453 autoleft-deploy[1836311]:     f4511d0 refactor(nuotraukos): vienas bendras nuotraukų valdymas visoms 28 create formoms
Sep 08 09:05:37 vmi3306453 autoleft-deploy[1836290]: [2026-09-08 09:05:37] Kodas atnaujintas iki ae14238
Sep 08 09:05:40 vmi3306453 autoleft-deploy[1836418]:         return self.cursor.execute(sql, params)
Sep 08 09:05:40 vmi3306453 autoleft-deploy[1836418]:     django.db.utils.ProgrammingError: column listings_listing.axle_count does not exist
Sep 08 09:05:40 vmi3306453 autoleft-deploy[1836418]:     LINE 1: ...capacity_l", "listings_listing"."sleeping_seats", "listings_...
Sep 08 09:05:40 vmi3306453 autoleft-deploy[1836418]:                                                                  ^
Sep 08 09:05:40 vmi3306453 autoleft-deploy[1836418]:     
Sep 08 09:05:40 vmi3306453 autoleft-deploy[1836418]:     
Sep 08 09:05:40 vmi3306453 autoleft-deploy[1836418]:     ----------------------------------------------------------------------
Sep 08 09:05:40 vmi3306453 autoleft-deploy[1836418]:     Ran 11 tests in 0.094s
Sep 08 09:05:40 vmi3306453 autoleft-deploy[1836418]:     
Sep 08 09:05:40 vmi3306453 autoleft-deploy[1836418]:     FAILED (errors=4)
Sep 08 09:05:40 vmi3306453 autoleft-deploy[1836418]:     ── 3/3  Vertimai: /en/ be lietuvių kalbos, šablonai apvynioti
Sep 08 09:05:40 vmi3306453 autoleft-deploy[1836418]:     Found 4 test(s).
Sep 08 09:05:40 vmi3306453 autoleft-deploy[1836418]:     System check identified no issues (0 silenced).
Sep 08 09:05:40 vmi3306453 autoleft-deploy[1836418]:     ....
Sep 08 09:05:40 vmi3306453 autoleft-deploy[1836418]:     ----------------------------------------------------------------------
Sep 08 09:05:40 vmi3306453 autoleft-deploy[1836418]:     Ran 4 tests in 0.350s
Sep 08 09:05:40 vmi3306453 autoleft-deploy[1836418]:     
Sep 08 09:05:40 vmi3306453 autoleft-deploy[1836418]:     OK
Sep 08 09:05:40 vmi3306453 autoleft-deploy[1836418]:     
Sep 08 09:05:40 vmi3306453 autoleft-deploy[1836418]:     PATIKRA NEPRAĖJO — nediegti.
```
