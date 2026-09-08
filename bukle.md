# Serverio būklė

Sugeneruota: 2026-09-08 08:46:08 CEST

## Kodas

```
sukasi:      c6aa4e6 fix(nuotraukos): trynimas, pertvarkymas ir „pagrindinė" telefone; įkėlimas po vieną
origin/master: 94c8a27 Merge remote-tracking branch 'origin/master'
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
HTTP 301, 0.001413s
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
Sep 08 08:46:04 vmi3306453 autoleft-deploy[1823969]:     de5208b fix(skelbimai): pateikus skelbimą — „pavyko" puslapis, o sėkmė žalia
Sep 08 08:46:04 vmi3306453 autoleft-deploy[1823969]:     626d94a feat(nuotraukos): visos 28 create formos valdo nuotraukas vienodai
Sep 08 08:46:04 vmi3306453 autoleft-deploy[1823969]:     0cde182 feat(registracija): pranešimas savininkui apie naują vartotoją
Sep 08 08:46:04 vmi3306453 autoleft-deploy[1823969]:     f4511d0 refactor(nuotraukos): vienas bendras nuotraukų valdymas visoms 28 create formoms
Sep 08 08:46:04 vmi3306453 autoleft-deploy[1823950]: [2026-09-08 08:46:04] Kodas atnaujintas iki 94c8a27
Sep 08 08:46:08 vmi3306453 autoleft-deploy[1824074]:         return self.cursor.execute(sql, params)
Sep 08 08:46:08 vmi3306453 autoleft-deploy[1824074]:     django.db.utils.ProgrammingError: column listings_listing.axle_count does not exist
Sep 08 08:46:08 vmi3306453 autoleft-deploy[1824074]:     LINE 1: ...capacity_l", "listings_listing"."sleeping_seats", "listings_...
Sep 08 08:46:08 vmi3306453 autoleft-deploy[1824074]:                                                                  ^
Sep 08 08:46:08 vmi3306453 autoleft-deploy[1824074]:     
Sep 08 08:46:08 vmi3306453 autoleft-deploy[1824074]:     
Sep 08 08:46:08 vmi3306453 autoleft-deploy[1824074]:     ----------------------------------------------------------------------
Sep 08 08:46:08 vmi3306453 autoleft-deploy[1824074]:     Ran 11 tests in 0.092s
Sep 08 08:46:08 vmi3306453 autoleft-deploy[1824074]:     
Sep 08 08:46:08 vmi3306453 autoleft-deploy[1824074]:     FAILED (errors=4)
Sep 08 08:46:08 vmi3306453 autoleft-deploy[1824074]:     ── 3/3  Vertimai: /en/ be lietuvių kalbos, šablonai apvynioti
Sep 08 08:46:08 vmi3306453 autoleft-deploy[1824074]:     Found 4 test(s).
Sep 08 08:46:08 vmi3306453 autoleft-deploy[1824074]:     System check identified no issues (0 silenced).
Sep 08 08:46:08 vmi3306453 autoleft-deploy[1824074]:     ....
Sep 08 08:46:08 vmi3306453 autoleft-deploy[1824074]:     ----------------------------------------------------------------------
Sep 08 08:46:08 vmi3306453 autoleft-deploy[1824074]:     Ran 4 tests in 0.377s
Sep 08 08:46:08 vmi3306453 autoleft-deploy[1824074]:     
Sep 08 08:46:08 vmi3306453 autoleft-deploy[1824074]:     OK
Sep 08 08:46:08 vmi3306453 autoleft-deploy[1824074]:     
Sep 08 08:46:08 vmi3306453 autoleft-deploy[1824074]:     PATIKRA NEPRAĖJO — nediegti.
```
