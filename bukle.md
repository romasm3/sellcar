# Serverio būklė

Sugeneruota: 2026-09-07 17:54:58 CEST

## Kodas

```
sukasi:      c6aa4e6 fix(nuotraukos): trynimas, pertvarkymas ir „pagrindinė" telefone; įkėlimas po vieną
origin/master: e398e79 fix(kontaktai): el. paštas išsisaugo, o sėkmė nebekrenta į klaidų dėžutę
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
HTTP 301, 0.001436s
```

## Skelbimų būsenos

```

Listing — iš viso 44
  active        21   MATOMAS
  draft         13   nematomas
  expired       10   nematomas
  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─
  nematomi dėl būsenos:      23
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
Sep 07 17:54:54 vmi3306453 autoleft-deploy[1278416]:     de5208b fix(skelbimai): pateikus skelbimą — „pavyko" puslapis, o sėkmė žalia
Sep 07 17:54:54 vmi3306453 autoleft-deploy[1278416]:     626d94a feat(nuotraukos): visos 28 create formos valdo nuotraukas vienodai
Sep 07 17:54:54 vmi3306453 autoleft-deploy[1278416]:     0cde182 feat(registracija): pranešimas savininkui apie naują vartotoją
Sep 07 17:54:54 vmi3306453 autoleft-deploy[1278416]:     f4511d0 refactor(nuotraukos): vienas bendras nuotraukų valdymas visoms 28 create formoms
Sep 07 17:54:54 vmi3306453 autoleft-deploy[1278396]: [2026-09-07 17:54:54] Kodas atnaujintas iki e398e79
Sep 07 17:54:58 vmi3306453 autoleft-deploy[1278472]:         return self.cursor.execute(sql, params)
Sep 07 17:54:58 vmi3306453 autoleft-deploy[1278472]:     django.db.utils.ProgrammingError: column listings_listing.contact_email does not exist
Sep 07 17:54:58 vmi3306453 autoleft-deploy[1278472]:     LINE 1: ...ddress", "listings_listing"."hide_exact_address", "listings_...
Sep 07 17:54:58 vmi3306453 autoleft-deploy[1278472]:                                                                  ^
Sep 07 17:54:58 vmi3306453 autoleft-deploy[1278472]:     
Sep 07 17:54:58 vmi3306453 autoleft-deploy[1278472]:     
Sep 07 17:54:58 vmi3306453 autoleft-deploy[1278472]:     ----------------------------------------------------------------------
Sep 07 17:54:58 vmi3306453 autoleft-deploy[1278472]:     Ran 11 tests in 0.072s
Sep 07 17:54:58 vmi3306453 autoleft-deploy[1278472]:     
Sep 07 17:54:58 vmi3306453 autoleft-deploy[1278472]:     FAILED (errors=4)
Sep 07 17:54:58 vmi3306453 autoleft-deploy[1278472]:     ── 3/3  Vertimai: /en/ be lietuvių kalbos, šablonai apvynioti
Sep 07 17:54:58 vmi3306453 autoleft-deploy[1278472]:     Found 4 test(s).
Sep 07 17:54:58 vmi3306453 autoleft-deploy[1278472]:     System check identified no issues (0 silenced).
Sep 07 17:54:58 vmi3306453 autoleft-deploy[1278472]:     ....
Sep 07 17:54:58 vmi3306453 autoleft-deploy[1278472]:     ----------------------------------------------------------------------
Sep 07 17:54:58 vmi3306453 autoleft-deploy[1278472]:     Ran 4 tests in 0.397s
Sep 07 17:54:58 vmi3306453 autoleft-deploy[1278472]:     
Sep 07 17:54:58 vmi3306453 autoleft-deploy[1278472]:     OK
Sep 07 17:54:58 vmi3306453 autoleft-deploy[1278472]:     
Sep 07 17:54:58 vmi3306453 autoleft-deploy[1278472]:     PATIKRA NEPRAĖJO — nediegti.
```
