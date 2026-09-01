# Serverio būklė

Sugeneruota: 2026-09-01 20:13:39 CEST

## Kodas

```
sukasi:      9f0c6aa fix(pastas): laiškai iškelti iš užklausos į foną
origin/master: 9d7bed7 fix(statiniai): turinio maišas varduose ir talpyklos taisyklės
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
HTTP 301, 0.002296s
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
Sep 01 20:12:33 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.647s CPU time.
Sep 01 20:13:34 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 01 20:13:35 vmi3306453 autoleft-deploy[2887277]: [2026-09-01 20:13:35] === Naujų commit'ų rasta: 9f0c6aa → 9d7bed7 ===
Sep 01 20:13:35 vmi3306453 autoleft-deploy[2887309]:     9d7bed7 fix(statiniai): turinio maišas varduose ir talpyklos taisyklės
Sep 01 20:13:35 vmi3306453 autoleft-deploy[2887277]: [2026-09-01 20:13:35] Kodas atnaujintas iki 9d7bed7
Sep 01 20:13:39 vmi3306453 autoleft-deploy[2887380]:         raise ValueError(
Sep 01 20:13:39 vmi3306453 autoleft-deploy[2887380]:     ValueError: Missing staticfiles manifest entry for 'brand/autoleft-icon.svg'
Sep 01 20:13:39 vmi3306453 autoleft-deploy[2887380]:     
Sep 01 20:13:39 vmi3306453 autoleft-deploy[2887380]:     ----------------------------------------------------------------------
Sep 01 20:13:39 vmi3306453 autoleft-deploy[2887380]:     Ran 11 tests in 0.989s
Sep 01 20:13:39 vmi3306453 autoleft-deploy[2887380]:     
Sep 01 20:13:39 vmi3306453 autoleft-deploy[2887380]:     FAILED (errors=4)
Sep 01 20:13:39 vmi3306453 autoleft-deploy[2887380]:     ── 3/3  Vertimai: /en/ be lietuvių kalbos, šablonai apvynioti
Sep 01 20:13:39 vmi3306453 autoleft-deploy[2887380]:       File "/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/staticfiles/storage.py", line 182, in _url
Sep 01 20:13:39 vmi3306453 autoleft-deploy[2887380]:         hashed_name = hashed_name_func(*args)
Sep 01 20:13:39 vmi3306453 autoleft-deploy[2887380]:       File "/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/staticfiles/storage.py", line 516, in stored_name
Sep 01 20:13:39 vmi3306453 autoleft-deploy[2887380]:         raise ValueError(
Sep 01 20:13:39 vmi3306453 autoleft-deploy[2887380]:     ValueError: Missing staticfiles manifest entry for 'brand/autoleft-icon.svg'
Sep 01 20:13:39 vmi3306453 autoleft-deploy[2887380]:     
Sep 01 20:13:39 vmi3306453 autoleft-deploy[2887380]:     ----------------------------------------------------------------------
Sep 01 20:13:39 vmi3306453 autoleft-deploy[2887380]:     Ran 4 tests in 0.259s
Sep 01 20:13:39 vmi3306453 autoleft-deploy[2887380]:     
Sep 01 20:13:39 vmi3306453 autoleft-deploy[2887380]:     FAILED (errors=2)
Sep 01 20:13:39 vmi3306453 autoleft-deploy[2887380]:     
Sep 01 20:13:39 vmi3306453 autoleft-deploy[2887380]:     PATIKRA NEPRAĖJO — nediegti.
```
