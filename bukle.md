# Serverio būklė

Sugeneruota: 2026-09-07 13:58:30 CEST

## Kodas

```
sukasi:      c6aa4e6 fix(nuotraukos): trynimas, pertvarkymas ir „pagrindinė" telefone; įkėlimas po vieną
origin/master: 0cde182 feat(registracija): pranešimas savininkui apie naują vartotoją
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
HTTP 301, 0.001482s
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
Sep 07 13:58:17 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 07 13:58:18 vmi3306453 autoleft-deploy[1141105]: [2026-09-07 13:58:18] === Naujų commit'ų rasta: c6aa4e6 → 0cde182 ===
Sep 07 13:58:18 vmi3306453 autoleft-deploy[1141128]:     0cde182 feat(registracija): pranešimas savininkui apie naują vartotoją
Sep 07 13:58:18 vmi3306453 autoleft-deploy[1141128]:     f4511d0 refactor(nuotraukos): vienas bendras nuotraukų valdymas visoms 28 create formoms
Sep 07 13:58:18 vmi3306453 autoleft-deploy[1141105]: [2026-09-07 13:58:18] Kodas atnaujintas iki 0cde182
Sep 07 13:58:29 vmi3306453 autoleft-deploy[1141291]:       File "/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/staticfiles/storage.py", line 182, in _url
Sep 07 13:58:29 vmi3306453 autoleft-deploy[1141291]:         hashed_name = hashed_name_func(*args)
Sep 07 13:58:29 vmi3306453 autoleft-deploy[1141291]:       File "/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/staticfiles/storage.py", line 516, in stored_name
Sep 07 13:58:29 vmi3306453 autoleft-deploy[1141291]:         raise ValueError(
Sep 07 13:58:29 vmi3306453 autoleft-deploy[1141291]:     ValueError: Missing staticfiles manifest entry for 'js/nuotrauku_valdymas.js'
Sep 07 13:58:29 vmi3306453 autoleft-deploy[1141291]:     
Sep 07 13:58:29 vmi3306453 autoleft-deploy[1141291]:     ----------------------------------------------------------------------
Sep 07 13:58:29 vmi3306453 autoleft-deploy[1141291]:     Ran 11 tests in 6.606s
Sep 07 13:58:29 vmi3306453 autoleft-deploy[1141291]:     
Sep 07 13:58:29 vmi3306453 autoleft-deploy[1141291]:     FAILED (errors=1)
Sep 07 13:58:29 vmi3306453 autoleft-deploy[1141291]:     ── 3/3  Vertimai: /en/ be lietuvių kalbos, šablonai apvynioti
Sep 07 13:58:29 vmi3306453 autoleft-deploy[1141291]:     Found 4 test(s).
Sep 07 13:58:29 vmi3306453 autoleft-deploy[1141291]:     System check identified no issues (0 silenced).
Sep 07 13:58:29 vmi3306453 autoleft-deploy[1141291]:     ....
Sep 07 13:58:29 vmi3306453 autoleft-deploy[1141291]:     ----------------------------------------------------------------------
Sep 07 13:58:29 vmi3306453 autoleft-deploy[1141291]:     Ran 4 tests in 0.399s
Sep 07 13:58:29 vmi3306453 autoleft-deploy[1141291]:     
Sep 07 13:58:29 vmi3306453 autoleft-deploy[1141291]:     OK
Sep 07 13:58:29 vmi3306453 autoleft-deploy[1141291]:     
Sep 07 13:58:29 vmi3306453 autoleft-deploy[1141291]:     PATIKRA NEPRAĖJO — nediegti.
```
