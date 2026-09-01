# Serverio būklė

Sugeneruota: 2026-09-01 20:43:25 CEST

## Kodas

```
sukasi:      9f0c6aa fix(pastas): laiškai iškelti iš užklausos į foną
origin/master: 1f05c01 docs(ekranai): nuotraukos iš GYVOS autoleft.com (SKILL.md 8 taisyklė)
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
HTTP 301, 0.001770s
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
Sep 01 20:43:21 vmi3306453 autoleft-deploy[2909839]: [2026-09-01 20:43:21] === Naujų commit'ų rasta: 9f0c6aa → 1f05c01 ===
Sep 01 20:43:21 vmi3306453 autoleft-deploy[2909862]:     1f05c01 docs(ekranai): nuotraukos iš GYVOS autoleft.com (SKILL.md 8 taisyklė)
Sep 01 20:43:21 vmi3306453 autoleft-deploy[2909862]:     d75e49d fix(deploy): statinių patikra nutraukdavo visą deploy'ą
Sep 01 20:43:21 vmi3306453 autoleft-deploy[2909862]:     9d7bed7 fix(statiniai): turinio maišas varduose ir talpyklos taisyklės
Sep 01 20:43:21 vmi3306453 autoleft-deploy[2909839]: [2026-09-01 20:43:21] Kodas atnaujintas iki 1f05c01
Sep 01 20:43:25 vmi3306453 autoleft-deploy[2909927]:         raise ValueError(
Sep 01 20:43:25 vmi3306453 autoleft-deploy[2909927]:     ValueError: Missing staticfiles manifest entry for 'brand/autoleft-icon.svg'
Sep 01 20:43:25 vmi3306453 autoleft-deploy[2909927]:     
Sep 01 20:43:25 vmi3306453 autoleft-deploy[2909927]:     ----------------------------------------------------------------------
Sep 01 20:43:25 vmi3306453 autoleft-deploy[2909927]:     Ran 11 tests in 0.943s
Sep 01 20:43:25 vmi3306453 autoleft-deploy[2909927]:     
Sep 01 20:43:25 vmi3306453 autoleft-deploy[2909927]:     FAILED (errors=4)
Sep 01 20:43:25 vmi3306453 autoleft-deploy[2909927]:     ── 3/3  Vertimai: /en/ be lietuvių kalbos, šablonai apvynioti
Sep 01 20:43:25 vmi3306453 autoleft-deploy[2909927]:       File "/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/staticfiles/storage.py", line 182, in _url
Sep 01 20:43:25 vmi3306453 autoleft-deploy[2909927]:         hashed_name = hashed_name_func(*args)
Sep 01 20:43:25 vmi3306453 autoleft-deploy[2909927]:       File "/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/staticfiles/storage.py", line 516, in stored_name
Sep 01 20:43:25 vmi3306453 autoleft-deploy[2909927]:         raise ValueError(
Sep 01 20:43:25 vmi3306453 autoleft-deploy[2909927]:     ValueError: Missing staticfiles manifest entry for 'brand/autoleft-icon.svg'
Sep 01 20:43:25 vmi3306453 autoleft-deploy[2909927]:     
Sep 01 20:43:25 vmi3306453 autoleft-deploy[2909927]:     ----------------------------------------------------------------------
Sep 01 20:43:25 vmi3306453 autoleft-deploy[2909927]:     Ran 4 tests in 0.220s
Sep 01 20:43:25 vmi3306453 autoleft-deploy[2909927]:     
Sep 01 20:43:25 vmi3306453 autoleft-deploy[2909927]:     FAILED (errors=2)
Sep 01 20:43:25 vmi3306453 autoleft-deploy[2909927]:     
Sep 01 20:43:25 vmi3306453 autoleft-deploy[2909927]:     PATIKRA NEPRAĖJO — nediegti.
```
