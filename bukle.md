# Serverio būklė

Sugeneruota: 2026-09-07 13:10:20 CEST

## Kodas

```
sukasi:      c6aa4e6 fix(nuotraukos): trynimas, pertvarkymas ir „pagrindinė" telefone; įkėlimas po vieną
origin/master: f4511d0 refactor(nuotraukos): vienas bendras nuotraukų valdymas visoms 28 create formoms
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
HTTP 301, 0.107238s
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
/dev/sda1       291G   29G  263G  10% /
```

## Paskutinis auto-deploy

```
Sep 07 13:09:01 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.494s CPU time.
Sep 07 13:10:08 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 07 13:10:08 vmi3306453 autoleft-deploy[1110999]: [2026-09-07 13:10:08] === Naujų commit'ų rasta: c6aa4e6 → f4511d0 ===
Sep 07 13:10:08 vmi3306453 autoleft-deploy[1111018]:     f4511d0 refactor(nuotraukos): vienas bendras nuotraukų valdymas visoms 28 create formoms
Sep 07 13:10:08 vmi3306453 autoleft-deploy[1110999]: [2026-09-07 13:10:08] Kodas atnaujintas iki f4511d0
Sep 07 13:10:20 vmi3306453 autoleft-deploy[1111205]:       File "/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/staticfiles/storage.py", line 182, in _url
Sep 07 13:10:20 vmi3306453 autoleft-deploy[1111205]:         hashed_name = hashed_name_func(*args)
Sep 07 13:10:20 vmi3306453 autoleft-deploy[1111205]:       File "/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/staticfiles/storage.py", line 516, in stored_name
Sep 07 13:10:20 vmi3306453 autoleft-deploy[1111205]:         raise ValueError(
Sep 07 13:10:20 vmi3306453 autoleft-deploy[1111205]:     ValueError: Missing staticfiles manifest entry for 'js/nuotrauku_valdymas.js'
Sep 07 13:10:20 vmi3306453 autoleft-deploy[1111205]:     
Sep 07 13:10:20 vmi3306453 autoleft-deploy[1111205]:     ----------------------------------------------------------------------
Sep 07 13:10:20 vmi3306453 autoleft-deploy[1111205]:     Ran 11 tests in 7.016s
Sep 07 13:10:20 vmi3306453 autoleft-deploy[1111205]:     
Sep 07 13:10:20 vmi3306453 autoleft-deploy[1111205]:     FAILED (errors=1)
Sep 07 13:10:20 vmi3306453 autoleft-deploy[1111205]:     ── 3/3  Vertimai: /en/ be lietuvių kalbos, šablonai apvynioti
Sep 07 13:10:20 vmi3306453 autoleft-deploy[1111205]:     Found 4 test(s).
Sep 07 13:10:20 vmi3306453 autoleft-deploy[1111205]:     System check identified no issues (0 silenced).
Sep 07 13:10:20 vmi3306453 autoleft-deploy[1111205]:     ....
Sep 07 13:10:20 vmi3306453 autoleft-deploy[1111205]:     ----------------------------------------------------------------------
Sep 07 13:10:20 vmi3306453 autoleft-deploy[1111205]:     Ran 4 tests in 0.438s
Sep 07 13:10:20 vmi3306453 autoleft-deploy[1111205]:     
Sep 07 13:10:20 vmi3306453 autoleft-deploy[1111205]:     OK
Sep 07 13:10:20 vmi3306453 autoleft-deploy[1111205]:     
Sep 07 13:10:20 vmi3306453 autoleft-deploy[1111205]:     PATIKRA NEPRAĖJO — nediegti.
```
