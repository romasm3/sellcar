# Serverio būklė

Sugeneruota: 2026-09-01 21:23:39 CEST

## Kodas

```
sukasi:      9f0c6aa fix(pastas): laiškai iškelti iš užklausos į foną
origin/master: ca29580 feat(juosta): šoninės filtrų juostos išvaizda pagal etaloną
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
HTTP 301, 0.001433s
```

## Skelbimų būsenos

```

Listing — iš viso 35
  active        19   MATOMAS
  draft          9   nematomas
  expired        7   nematomas
  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─
  nematomi dėl būsenos:      16
  iš jų pasibaigę (expires_at praeityje): 7
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
/dev/sda1       291G   45G  247G  16% /
```

## Paskutinis auto-deploy

```
Sep 01 21:23:31 vmi3306453 autoleft-deploy[2938320]:     ca29580 feat(juosta): šoninės filtrų juostos išvaizda pagal etaloną
Sep 01 21:23:31 vmi3306453 autoleft-deploy[2938320]:     1f05c01 docs(ekranai): nuotraukos iš GYVOS autoleft.com (SKILL.md 8 taisyklė)
Sep 01 21:23:31 vmi3306453 autoleft-deploy[2938320]:     d75e49d fix(deploy): statinių patikra nutraukdavo visą deploy'ą
Sep 01 21:23:31 vmi3306453 autoleft-deploy[2938320]:     9d7bed7 fix(statiniai): turinio maišas varduose ir talpyklos taisyklės
Sep 01 21:23:31 vmi3306453 autoleft-deploy[2938292]: [2026-09-01 21:23:31] Kodas atnaujintas iki ca29580
Sep 01 21:23:39 vmi3306453 autoleft-deploy[2938421]:         raise ValueError(
Sep 01 21:23:39 vmi3306453 autoleft-deploy[2938421]:     ValueError: Missing staticfiles manifest entry for 'brand/autoleft-icon.svg'
Sep 01 21:23:39 vmi3306453 autoleft-deploy[2938421]:     
Sep 01 21:23:39 vmi3306453 autoleft-deploy[2938421]:     ----------------------------------------------------------------------
Sep 01 21:23:39 vmi3306453 autoleft-deploy[2938421]:     Ran 11 tests in 1.474s
Sep 01 21:23:39 vmi3306453 autoleft-deploy[2938421]:     
Sep 01 21:23:39 vmi3306453 autoleft-deploy[2938421]:     FAILED (errors=4)
Sep 01 21:23:39 vmi3306453 autoleft-deploy[2938421]:     ── 3/3  Vertimai: /en/ be lietuvių kalbos, šablonai apvynioti
Sep 01 21:23:39 vmi3306453 autoleft-deploy[2938421]:       File "/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/staticfiles/storage.py", line 182, in _url
Sep 01 21:23:39 vmi3306453 autoleft-deploy[2938421]:         hashed_name = hashed_name_func(*args)
Sep 01 21:23:39 vmi3306453 autoleft-deploy[2938421]:       File "/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/staticfiles/storage.py", line 516, in stored_name
Sep 01 21:23:39 vmi3306453 autoleft-deploy[2938421]:         raise ValueError(
Sep 01 21:23:39 vmi3306453 autoleft-deploy[2938421]:     ValueError: Missing staticfiles manifest entry for 'brand/autoleft-icon.svg'
Sep 01 21:23:39 vmi3306453 autoleft-deploy[2938421]:     
Sep 01 21:23:39 vmi3306453 autoleft-deploy[2938421]:     ----------------------------------------------------------------------
Sep 01 21:23:39 vmi3306453 autoleft-deploy[2938421]:     Ran 4 tests in 0.320s
Sep 01 21:23:39 vmi3306453 autoleft-deploy[2938421]:     
Sep 01 21:23:39 vmi3306453 autoleft-deploy[2938421]:     FAILED (errors=2)
Sep 01 21:23:39 vmi3306453 autoleft-deploy[2938421]:     
Sep 01 21:23:39 vmi3306453 autoleft-deploy[2938421]:     PATIKRA NEPRAĖJO — nediegti.
```
